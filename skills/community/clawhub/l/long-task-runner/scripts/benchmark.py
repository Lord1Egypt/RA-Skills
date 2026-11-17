"""Compare real CLI return bytes; does NOT measure model requests or tokens."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
import time
import uuid
sys.stdout.reconfigure(encoding='utf-8')

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--directory',type=Path,required=True)
p.add_argument('--report',type=Path,required=True)
p.add_argument('--seconds',type=float,default=6)
a=p.parse_args()
if not 2<=a.seconds<=20:
    p.error('seconds must be 2..20')
root=a.directory.resolve()/('bench-'+uuid.uuid4().hex[:10])
here=Path(__file__).resolve().parent
rows=[]
for mode in ['status_every_1s','bounded_wait']:
    d=root/mode
    subprocess.run([sys.executable,str(here/'make_demo.py'),'--directory',str(d),'--seconds',str(a.seconds)],check=True,capture_output=True)
    calls=[]
    def call(action,*more):
        cmd=[sys.executable,str(here/'runner.py'),action,'--job',str(d/'job'),*map(str,more)]
        before=time.monotonic()
        proc=subprocess.run(cmd,capture_output=True,timeout=40)
        calls.append({'action':action,'bytes':len(proc.stdout)+len(proc.stderr),'seconds':round(time.monotonic()-before,3)})
        if proc.returncode not in [0,3]:
            raise RuntimeError(proc.stdout.decode('utf-8','replace'))
        return json.loads(proc.stdout)
    start=time.monotonic()
    call('start','--spec',d/'demo.json')
    if mode=='bounded_wait':
        result=call('wait','--seconds',25)
    else:
        while True:
            result=call('status')
            if result['status']=='succeeded':
                break
            if time.monotonic()-start>30:
                raise TimeoutError(result)
            time.sleep(1)
    if result['status']!='succeeded':
        raise RuntimeError(result)
    rows.append({'mode':mode,'wall_seconds':round(time.monotonic()-start,3),'cli_calls':len(calls),
                 'return_bytes':sum(x['bytes'] for x in calls),'calls':calls,'status':result['status']})
report={'root':str(root),'task_seconds':a.seconds,'rows':rows,
        'measurement':'Actual CLI stdout+stderr bytes. Both consumer patterns were executed by one local script. These are interface calls, not observed model/API requests; token usage not measured.'}
a.report.parent.mkdir(parents=True,exist_ok=True)
a.report.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'rows':[{k:v for k,v in row.items() if k!='calls'} for row in rows],'report':str(a.report.resolve())},ensure_ascii=False))
