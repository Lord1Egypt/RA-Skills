"""Generate an absolute-path demo spec; uses only the local Python interpreter."""
import argparse
import json
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--directory',type=Path,required=True)
p.add_argument('--seconds',type=float,default=3)
a=p.parse_args()
root=a.directory.resolve()
root.mkdir(parents=True,exist_ok=True)
spec={'version':1,'name':'local demo','total_timeout_s':max(30,a.seconds+20),
      'tasks':[{'id':'demo','argv':[sys.executable,str(Path(__file__).with_name('demo_task.py')),'--seconds',str(a.seconds)],
                'cwd':str(root),'timeout_s':max(15,a.seconds+5),'effect':'local','replay_safe':True,
                'artifacts':[{'kind':'json','path':'result.json','equals':{'ok':True}}]}]}
path=root/'demo.json'
if path.exists():
    raise SystemExit('Refusing to overwrite demo.json; choose a fresh directory')
path.write_text(json.dumps(spec,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'spec':str(path),'job':str(root/'job')},ensure_ascii=False))
