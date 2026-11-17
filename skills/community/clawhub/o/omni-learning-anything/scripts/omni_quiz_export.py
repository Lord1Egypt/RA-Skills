"""Explicit private exports and assessment-only removal; never sends data remotely."""
import csv
import io
import json
import os
import shutil
from pathlib import Path
import omni_core as c
import omni_learning_store as store
from omni_quiz_schema import require


def export(root, output, format):
    root=Path(root).resolve(); output=Path(output).absolute()
    require(format in ('json','csv') and output.suffix.lower()=='.'+format, 'Choose a JSON/CSV output file.')
    require(not output.is_symlink(), 'Export target must not be a symlink.')
    with c.lock(root):
        records=store.records(root)
        quizzes=[c.read(store.path(root,'quizzes',p.name)) for p in store.quizzes(root)]
        if format=='json':
            content=json.dumps({'schema':1,'quizzes':quizzes,'records':records},ensure_ascii=False,indent=2,allow_nan=False)+'\n'
        else:
            buffer=io.StringIO(newline=''); writer=csv.writer(buffer)
            writer.writerow(['attempt_id','lesson','revision','event_id','kind','question','event_json'])
            for a in records['attempts'].values():
                for event in a['events']:
                    row=[a['id'],a['key'],a['revision'],event['id'],event['kind'],event.get('question',''),json.dumps(event,ensure_ascii=False)]
                    writer.writerow(["'"+x if isinstance(x,str) and (x.lstrip().startswith(('=','+','-','@')) or x.startswith(('\t','\r'))) else x for x in row])
            content=buffer.getvalue()
        if output.exists():
            require(output.read_bytes()==content.encode(), 'Export already exists with different contents; choose a new file.')
        else:
            output.parent.mkdir(parents=True,exist_ok=True)
            fd=os.open(output,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
            with os.fdopen(fd,'w',encoding='utf-8',newline='') as stream: stream.write(content)
        return {'output':str(output),'format':format,'attempts':len(records['attempts']),
                'note':'Private explicit export. JSON preserves raw events; CSV formula-like cells are escaped. No cloud upload.'}


def forget(root, *, confirm=False, scope='attempts'):
    require(confirm is True and scope in ('attempts','all'), 'Explicit learner confirmation is required for assessment deletion.')
    root=Path(root).resolve()
    with c.lock(root):
        base=store.path(root)
        if scope=='all':
            if base.exists(): shutil.rmtree(base)
        else:
            target=store.path(root,'records.json')
            if target.exists(): target.unlink()
    return {'removed':scope,'note':'Course plan/config/delivery/receipts are unchanged. Previously exported copies are not removed.'}
