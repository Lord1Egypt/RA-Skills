#!/usr/bin/env node
import fs from 'node:fs/promises';
import path from 'node:path';
import markdownit from 'markdown-it';
import taskLists from 'markdown-it-task-lists';
import footnote from 'markdown-it-footnote';
import matter from 'gray-matter';

function help() {
  console.log(`
Markdown to HTML Converter

Usage:
  node scripts/markdown_to_html.mjs [options]

Input (choose one):
  --file <path.md>              Input markdown file
  --markdown <string>           Input markdown string
  --input-dir <dir>             Batch convert .md recursively

Output:
  --out <path.html>             Output html file (single mode)
  --output-dir <dir>            Output directory (batch mode)

Options:
  --theme <light|github|minimal>  Built-in style theme (default: light)
  --title <text>                HTML title (override)
  --toc <true|false>            Reserved (default: false)
  --standalone <true|false>     Wrap full HTML document (default: true)
  --embed-css <true|false>      Embed CSS in <style> (default: true)
  --dry-run                     Preview files only
  --help                        Show help

Examples:
  node scripts/markdown_to_html.mjs --file ./a.md --out ./a.html
  node scripts/markdown_to_html.mjs --file ./a.md --out ./a.html --theme github
  node scripts/markdown_to_html.mjs --input-dir ./md --output-dir ./html
`);
}

const CSS = {
  light: `body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Arial,sans-serif;max-width:900px;margin:0 auto;padding:32px;line-height:1.7;color:#222}h1,h2,h3{line-height:1.25}h1{border-bottom:1px solid #eee;padding-bottom:.3em}pre{background:#f6f8fa;padding:12px;border-radius:8px;overflow:auto}code{background:#f2f2f2;padding:.15em .35em;border-radius:4px}table{border-collapse:collapse;width:100%}th,td{border:1px solid #ddd;padding:8px}blockquote{border-left:4px solid #ddd;padding-left:1em;color:#666}`,
  github: `body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;max-width:980px;margin:0 auto;padding:40px;line-height:1.65}pre{background:#f6f8fa;padding:16px;border-radius:6px;overflow:auto}code{background:rgba(175,184,193,.2);padding:.2em .4em;border-radius:6px}table{border-collapse:collapse}th,td{border:1px solid #d0d7de;padding:6px 13px}blockquote{border-left:.25em solid #d0d7de;padding:0 1em;color:#57606a}`,
  minimal: `body{font-family:system-ui,sans-serif;max-width:860px;margin:2rem auto;padding:0 1rem;line-height:1.8}`
};

function parseArgs(argv) {
  const a = {
    theme: 'light',
    toc: false,
    standalone: true,
    embedCss: true,
    dryRun: false,
  };
  for (let i=2;i<argv.length;i++) {
    const k=argv[i], v=argv[i+1];
    switch(k){
      case '--file': a.file=v; i++; break;
      case '--markdown': a.markdown=v; i++; break;
      case '--input-dir': a.inputDir=v; i++; break;
      case '--out': a.out=v; i++; break;
      case '--output-dir': a.outputDir=v; i++; break;
      case '--theme': a.theme=v||'light'; i++; break;
      case '--title': a.title=v||''; i++; break;
      case '--toc': a.toc=(v||'').toLowerCase()==='true'; i++; break;
      case '--standalone': a.standalone=(v||'').toLowerCase()!=='false'; i++; break;
      case '--embed-css': a.embedCss=(v||'').toLowerCase()!=='false'; i++; break;
      case '--dry-run': a.dryRun=true; break;
      case '--help': a.help=true; break;
      default: throw new Error(`Unknown arg: ${k}`);
    }
  }
  return a;
}

function checkArgs(a){
  const cnt=[a.file,a.markdown,a.inputDir].filter(Boolean).length;
  if(cnt===0) throw new Error('need one input: --file|--markdown|--input-dir');
  if(cnt>1) throw new Error('only one input mode at once');
  if(a.inputDir && !a.outputDir) throw new Error('--input-dir requires --output-dir');
  if(!a.inputDir && !a.out) throw new Error('single mode requires --out');
  if(!['light','github','minimal'].includes(a.theme)) throw new Error('--theme must be light|github|minimal');
}

async function walkMdFiles(dir){
  const out=[];
  async function walk(d){
    const xs=await fs.readdir(d,{withFileTypes:true});
    for(const x of xs){
      const p=path.join(d,x.name);
      if(x.isDirectory()) await walk(p);
      else if(/\.md$/i.test(x.name)) out.push(p);
    }
  }
  await walk(dir);
  return out;
}

function render(md, opts={}){
  const m = markdownit({ html:true, linkify:true, typographer:true })
    .use(taskLists, { enabled:true })
    .use(footnote);

  const parsed = matter(md);
  const body = m.render(parsed.content || '');
  const title = opts.title || parsed.data?.title || 'Document';

  if(!opts.standalone) return body;

  const css = opts.embedCss ? `<style>${CSS[opts.theme] || CSS.light}</style>` : '';
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>${String(title).replace(/</g,'&lt;')}</title>
  ${css}
</head>
<body>
${body}
</body>
</html>`;
}

async function writeEnsure(p, c){
  await fs.mkdir(path.dirname(p), {recursive:true});
  await fs.writeFile(p, c, 'utf8');
}

function mapOut(inputDir, outputDir, file){
  const rel=path.relative(inputDir,file).replace(/\.md$/i,'');
  return path.join(outputDir, `${rel}.html`);
}

async function main(){
  const a=parseArgs(process.argv);
  if(a.help) return help();
  checkArgs(a);

  if(a.inputDir){
    const files=await walkMdFiles(a.inputDir);
    console.log(`Found ${files.length} markdown files.`);
    if(a.dryRun){ files.forEach(f=>console.log('-',f)); return; }
    let ok=0, fail=0;
    for(const f of files){
      try{
        const md=await fs.readFile(f,'utf8');
        const html=render(md,a);
        const out=mapOut(a.inputDir,a.outputDir,f);
        await writeEnsure(out,html);
        ok++;
      }catch(e){
        fail++; console.error('[FAIL]',f,e.message);
      }
    }
    console.log(`Done. success=${ok}, failed=${fail}`);
    return;
  }

  const md = a.file ? await fs.readFile(a.file,'utf8') : a.markdown;
  const html = render(md,a);
  await writeEnsure(a.out, html);
  console.log(`OK -> ${a.out}`);
}

main().catch(e=>{ console.error('[ERROR]',e.message); process.exit(1); });
