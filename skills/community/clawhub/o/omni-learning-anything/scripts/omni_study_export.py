"""Explicit one-way, literal-text Anki CSV; never modifies learning evidence."""
import csv
import io
import os
from pathlib import Path
import omni_core as c
import omni_study as study
from omni_quiz_schema import require


def safe(value):
    return "'"+value if value.lstrip().startswith(('=','+','-','@')) or value.startswith(('\t','\r')) else value


def anki(root, output):
    root=Path(root).resolve();output=Path(output).absolute()
    require(output.suffix.lower()=='.csv' and not output.is_symlink(), 'Choose a fresh non-symlink CSV file.')
    # Never allow an export path to overwrite a private course artifact.
    require(not output.resolve().is_relative_to(root), 'Export outside the course archive to keep evidence and manifests immutable.')
    with c.lock(root):
        items=[x for x in study.derived(root) if not x['retired'] and not x['excluded'] and x['lightweight'] and x['judgment'] in ('review','assisted','independent')]
        require(bool(items), 'No validated, undisputed lightweight questions to export.')
        buffer=io.StringIO(newline='');buffer.write('#separator:Comma\n#html:false\n#tags column:3\n#columns:Front,Back,Tags\n');writer=csv.writer(buffer,lineterminator='\n')
        for item in items:
            question=item['_question'];front=question['prompt']
            if question['kind']=='choice':
                front+='\n'+'\n'.join(chr(65+i)+'. '+o['text'] for i,o in enumerate(question['options']))
                answer=next(o['text'] for o in question['options'] if o['id']==question['answer_id'])
            else:answer=question['expected_answer']
            # Anki deduplicates the first field. A version identity separates identical prompts from different courses/revisions.
            front+='\nOmni-ID: '+item['id']
            back=answer+'\n'+question['explanation']
            for ref in item['source_refs']:
                source=next(s for s in item['sources'] if s['id']==ref['source_id'])
                back+='\n['+source['id']+'] '+source['title']+' | '+str(source.get('url') or source.get('material_ref',''))
                back+=' | section '+str(ref['section_index']+1)+': '+ref['quote']
            writer.writerow([safe(front),safe(back),'Omni '+item['key']+' v'+str(item['revision'])])
        content=buffer.getvalue().encode('utf-8')
        if output.exists():require(output.read_bytes()==content, 'Export exists with different contents; choose a new filename.')
        else:
            output.parent.mkdir(parents=True,exist_ok=True)
            fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'wb') as stream:stream.write(content)
        return {'output':str(output),'cards':len(items),'format':'anki_csv',
                'note':'Explicit private one-way export; no Anki result sync. Import into Basic and map Front/Back/Tags; preview before import. Same-version first fields are stable.'}
