"""Portable XeLaTeX rendering and artifact verification; no generated TeX execution."""
from omni_locale import source_labels
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import urlsplit
from pypdf import PdfReader
import omni_core as c
from omni_locale import language, subtitle as localized_subtitle, CJK_FONTS, ARABIC_FONTS


def esc(text):
    table={'\\':r'\textbackslash{}','{':r'\{','}':r'\}','%':r'\%','$':r'\$','&':r'\&','#':r'\#','_':r'\_','~':r'\textasciitilde{}','^':r'\textasciicircum{}'}
    return ''.join(table.get(ch,ch) for ch in str(text))


def visible_text(text,code):
    if code!='ar':return esc(text)
    # Keep Arabic shaping/direction while isolating Latin identifiers and citations.
    # Paragraph breaks must stay outside the non-paragraph \textenglish command.
    parts=re.split(r'((?:\r?\n[ \t]*){2,}|[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+(?:[ \t]+[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]+)*)',str(text))
    return ''.join(esc(part) if part.isspace() or re.search(r'[\u0600-\u06ff\u0750-\u077f\u08a0-\u08ff]',part) else r'\textenglish{'+esc(part)+'}' for part in parts if part)


def executable(name):
    if shutil.which(name): return shutil.which(name)
    roots=[Path.home()/'Library/TinyTeX/bin',Path.home()/'.TinyTeX/bin',Path('/Library/TeX/texbin')]
    for root in roots:
        for path in [root/name,*root.glob('*/'+name)]:
            if path.is_file(): return str(path)
    return None


from omni_document import validate_document, material_markdown


PREAMBLE=r'''\documentclass[11pt]{article}
\usepackage[a4paper,margin=22mm,headheight=16pt]{geometry}
\usepackage{fontspec,xeCJK,xcolor,graphicx,enumitem,fancyhdr,titlesec}
\usepackage{hyperref}
\IfFontExistsTF{Times New Roman}{\setmainfont{Times New Roman}}{\setmainfont{TeX Gyre Termes}}
\IfFontExistsTF{FangSong}{\setCJKmainfont[AutoFakeBold=2]{FangSong}}{\IfFontExistsTF{仿宋}{\setCJKmainfont[AutoFakeBold=2]{仿宋}}{\IfFontExistsTF{FandolFang-Regular.otf}{\setCJKmainfont[AutoFakeBold=2]{FandolFang-Regular.otf}}{\setCJKmainfont{FandolSong-Regular.otf}}}}
\definecolor{ink}{HTML}{173747}\definecolor{accent}{HTML}{227E82}
\hypersetup{colorlinks=true,urlcolor=accent,linkcolor=accent}
\linespread{1.22}\setlength{\parindent}{0pt}\setlength{\parskip}{6pt}
\setlist[itemize]{leftmargin=1.4em,itemsep=3pt}
\titleformat{\section}{\large\bfseries\color{ink}}{}{0pt}{}
\titlespacing*{\section}{0pt}{14pt}{7pt}
\pagestyle{fancy}\fancyhf{}\lhead{\small OMNI LEARNING / 学习手册}\rhead{\small Source-grounded learning}\cfoot{\small\thepage}
\emergencystretch=2em\widowpenalty=10000\clubpenalty=10000
\newcommand{\Needspace}[1]{\par\begingroup\dimen0=#1\relax\vskip0pt plus\dimen0\penalty-100\vskip0pt plus-\dimen0\vskip\dimen0\penalty9999\vskip-\dimen0\vskip0pt\endgroup}
\begin{document}
'''


def font_chain(command, candidates, options=''):
    result=chr(92)+command+options+'{'+candidates[-1]+'}'
    for name in reversed(candidates[:-1]):
        result=r'\IfFontExistsTF{'+name+'}{'+chr(92)+command+options+'{'+name+'}}{'+result+'}'
    return result


def language_preamble(code):
    labels=language(code)
    result=PREAMBLE.replace('学习手册',esc(labels['guide'])).replace('Source-grounded learning',esc(labels['grounded']))
    extra=''
    if code in ('ja','ko'):
        extra+=font_chain('setCJKmainfont',CJK_FONTS[code], '[AutoFakeBold=2]')+'\n'
        extra+=r'\xeCJKsetup{AutoFallBack=true}\setCJKfallbackfamilyfont{\CJKrmdefault}{FandolSong-Regular.otf}'+'\n'
        if code=='ko':extra+=r'\xeCJKsetup{CJKspace=true}'+'\n'
    if code=='ar':
        result=result.replace('OMNI LEARNING / ',r'\textenglish{OMNI LEARNING / }').replace(r'\thepage',r'\textenglish{\thepage}')
        # bidi must load after hyperref/fancyhdr/graphicx; polyglossia selects RTL.
        extra+=r'\usepackage{polyglossia}\setdefaultlanguage{arabic}\setotherlanguage{english}'+'\n'
        extra+=font_chain(r'newfontfamily\arabicfont',ARABIC_FONTS,'[Script=Arabic]')+'\n'
    return result.replace(r'\begin{document}',extra+r'\begin{document}')


def render(root,input_path,key,export_formats=()):
    from omni_document import validate_key
    validate_key(key)
    root=Path(root).resolve(); input_path=Path(input_path).resolve()
    if not input_path.is_relative_to(root): raise ValueError('Input must be inside project.')
    with c.lock(root):
        state=c.read(root/'state.json'); plan=c.read(root/'plan.json'); c.validate_plan(plan)
        data=c.read(input_path)
        if key=='plan':
            if input_path!=root/'plan.json': raise ValueError('Plan renderer must use canonical plan.json.')
            if state['lessons']: raise ValueError('A started curriculum must be preserved; create a new project for revisions.')
            if (root/'manifests/plan.json').exists(): raise ValueError('Plan already rendered. Reuse it, or archive this project and create a revised project.')
        else:
            c.check_approval(root,state)
            day=data.get('day'); action=c.next_action(root)
            if not isinstance(day,int) or key!=f'Day{day:02d}' or action.get('day')!=day or action['action']!='generate': raise ValueError('Render only the next ungenerated lesson; reuse existing artifacts.')
            if data.get('title')!=plan['days'][day-1]['topic']: raise ValueError('Lesson title differs from approved plan.')
            config=c.read(root/'config.json')
            reading=data.get('reading_minutes'); practice=data.get('practice_minutes')
            if type(reading) is not int or reading<1 or type(practice) is not int or practice<0:
                raise ValueError('Reading minutes must be a positive integer; practice minutes a nonnegative integer.')
            mins=reading+practice
            if not 1<=mins<=config['daily_minutes']: raise ValueError('Lesson exceeds agreed time budget.')
        validate_document(data,root)
        from omni_courses import validate_course_plan,with_context
        config=c.read(root/'config.json');validate_course_plan(config,plan)
        data=with_context(data,config,plan)
        compiler=executable('xelatex')
        if not compiler: raise RuntimeError('XeLaTeX missing. Follow references/setup.md; no substitute PDF engine.')
        for d in ('pdf','sources','assets','manifests','previews'): (root/d).mkdir(exist_ok=True)
        safe_topic=re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',plan['topic']).strip(' .')[:70]
        title=re.sub(r'[<>:"/\\|?*\x00-\x1f]','_',data['title']).strip(' .')[:90]
        stem=safe_topic+'_学习计划' if key=='plan' else f'{safe_topic}_每日学习_{key}_{title}'
        figure=(root/data['figure']['path']).resolve()
        img='figure-'+c.digest(figure)[:12]+figure.suffix.lower(); image_path=root/'assets'/img
        if figure!=image_path: shutil.copyfile(figure,image_path)
        config=c.read(root/'config.json'); labels=source_labels(config)
        e=lambda value:visible_text(value,labels['code'])
        subtitle=localized_subtitle(data,plan,config,c.today(root),key)
        tex=[language_preamble(labels['code']),r'{\LARGE\bfseries\color{ink} '+e(data['title'])+r'}\par',e(subtitle)+r'\par\vspace{6pt}']
        md=['# '+data['title'],subtitle]
        for i,s in enumerate(data['sections']):
            tex.extend([r'\Needspace{5\baselineskip}\section*{'+e(s['title'])+'}',e(s['body'])]); md.extend(['## '+s['title'],s['body']])
            if i==min(1,len(data['sections'])-1):
                tex.extend([r'\begin{center}\includegraphics[width=\linewidth,height=0.26\textheight,keepaspectratio]{../assets/'+img+r'}\par',r'{\small '+e(data['figure']['caption'])+r'}\par',r'{\footnotesize '+e(data['figure']['credit'])+r'}\end{center}'])
                md.extend(['!['+data['figure']['caption']+'](../assets/'+img+')',data['figure']['credit']])
        tex.append(r'\Needspace{6\baselineskip}\section*{'+e(labels['further'])+r'}\small '+e(labels['optional'])+r'\begin{enumerate}[leftmargin=1.6em]')
        md.append('## '+labels['further'])
        for s in data['sources']:
            published=' | '+labels['published']+': '
            checked=' | '+labels['checked']+': '
            label=(r'\href{'+esc(s['url'])+'}{'+e(s['title'])+'}') if s.get('url') else e(s['title'])
            tex.append(r'\item ['+e(s['id'])+r'] '+label+' — '+e(s['note'])+r'\par '+e(s['publisher']+published+s['published_at']+checked+s['checked_at']))
            md_title=material_markdown(s['title']) if s.get('material_ref') else s['title']
            md_note=material_markdown(s['note']) if s.get('material_ref') else s['note']
            md_label=f"[{md_title}]({s['url']})" if s.get('url') else md_title
            md.append(f"- [{s['id']}] {md_label}: {md_note}; {s['publisher']}{published}{s['published_at']}{checked}{s['checked_at']}")
        tex.extend([r'\end{enumerate}',r'\end{document}'])
        texfile=root/'sources'/(stem+'.tex'); texfile.write_text('\n\n'.join(tex),encoding='utf-8')
        mdfile=texfile.with_suffix('.md'); mdfile.write_text('\n\n'.join(md)+'\n',encoding='utf-8')
        env=os.environ.copy(); env['PATH']=str(Path(compiler).parent)+os.pathsep+env.get('PATH','')
        for _ in range(2):
            proc=subprocess.run([compiler,'-no-shell-escape','-halt-on-error','-interaction=nonstopmode',texfile.name],cwd=texfile.parent,env=env,capture_output=True,text=True,timeout=120)
            if proc.returncode: raise RuntimeError('XeLaTeX failed: '+proc.stdout[-2500:])
        log=texfile.with_suffix('.log').read_text(errors='replace')
        if 'Missing character:' in log: raise ValueError('Missing font glyphs. Inspect LaTeX log.')
        pdf=root/'pdf'/(stem+'.pdf'); shutil.copyfile(texfile.with_suffix('.pdf'),pdf); texfile.with_suffix('.pdf').unlink()
        report=inspect_pdf(pdf,data['sources'])
        import pypdfium2 as pdfium
        doc=pdfium.PdfDocument(pdf)
        preview_paths=[]
        for n in range(len(doc)):
            target=root/'previews'/f'{key}-{n+1:02d}.png'; doc[n].render(scale=1.25).to_pil().save(target); preview_paths.append(str(target.relative_to(root)))
        doc.close()
        files=[input_path,root/'plan.json',root/'config.json',pdf,texfile,mdfile,image_path,*[root/p for p in preview_paths]]
        artifacts={'pdf':str(pdf.relative_to(root)),'markdown':str(mdfile.relative_to(root))}
        if 'docx' in export_formats:
            from omni_document import write_docx
            docx_path=root/'sources'/(stem+'.docx'); write_docx(docx_path,data,plan,c.read(root/'config.json'),image_path,c.today(root),key)
            files.append(docx_path); artifacts['docx']=str(docx_path.relative_to(root))
        if 'html' in export_formats:
            from omni_html import serialize
            path=root/'sources'/(stem+'.html');path.write_text(serialize(data,plan,config,image_path,c.today(root),key),encoding='utf-8')
            files.append(path);artifacts['html']=str(path.relative_to(root))
        report['figure']=str(image_path.relative_to(root))
        manifest={'input':str(input_path.relative_to(root)),'artifact':str(pdf.relative_to(root)),'artifacts':artifacts,'key':key,'pdf':str(pdf.relative_to(root)),'created_at':c.today(root),'files':{str(p.relative_to(root)):c.digest(p) for p in files},'previews':preview_paths,'reviewed_at':None,'report':report,'layout_warnings':len(re.findall('Overfull',log))}
        c.save(root/'manifests'/(key+'.json'),manifest)
        return manifest


def inspect_pdf(pdf,sources):
    reader=PdfReader(pdf); urls=set(); fonts=set()
    if not reader.pages: raise ValueError('Empty PDF.')
    for page in reader.pages:
        if not page.extract_text().strip(): raise ValueError('Blank PDF page.')
        for a in page.get('/Annots',[]):
            action=a.get_object().get('/A',{})
            if action.get('/URI'): urls.add(str(action['/URI']))
        for f in page.get('/Resources',{}).get('/Font',{}).values():
            font=f.get_object(); fonts.add(str(font.get('/BaseFont','')))
            descriptors=[font.get('/FontDescriptor')]
            descriptors += [d.get_object().get('/FontDescriptor') for d in font.get('/DescendantFonts',[])]
            for descriptor in descriptors:
                if descriptor is not None and not any(k in descriptor.get_object() for k in ('/FontFile','/FontFile2','/FontFile3')): raise ValueError('Font not embedded.')
    if not {s['url'] for s in sources if s.get('url')}.issubset(urls): raise ValueError('Missing PDF links.')
    return {'pages':len(reader.pages),'links':len(urls),'fonts':sorted(fonts)}


def review(root,key,note):
    from omni_document import review as document_review
    return document_review(root,key,note)
