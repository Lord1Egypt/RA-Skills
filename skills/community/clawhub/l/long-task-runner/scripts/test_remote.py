"""HTTP loopback fixtures prove watcher never submits or cancels a remote job."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import http.server
import json
from pathlib import Path
import subprocess
import sys
import threading
import time
import uuid

counts={}
mutations=[]
guard=threading.Lock()
class Handler(http.server.BaseHTTPRequestHandler):
    def log_message(self,*args):
        pass
    def do_POST(self):
        mutations.append(self.path)
        self.send_error(405)
    do_DELETE=do_POST
    do_PUT=do_POST
    def do_GET(self):
        with guard:
            counts[self.path]=counts.get(self.path,0)+1
            n=counts[self.path]
        if self.path=='/redirect':
            self.send_response(302)
            self.send_header('Location','/ok')
            self.end_headers()
            return
        if self.path=='/auth':
            self.send_error(401)
            return
        if self.path=='/transient' and n==1:
            self.send_error(503)
            return
        state='running' if self.path=='/timeout' or self.path=='/ok' and n<3 else ('failed' if self.path=='/fail' else 'mystery' if self.path=='/unknown' else 'succeeded')
        obj={'id':'wrong' if self.path=='/wrong-id' else 'job-1','status':state}
        b=json.dumps(obj).encode()
        self.send_response(200)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(b)))
        self.end_headers()
        self.wfile.write(b)

p=argparse.ArgumentParser(description=__doc__)
p.add_argument('--root',type=Path,required=True)
p.add_argument('--report',type=Path,required=True)
a=p.parse_args()
root=a.root.resolve()/('remote-'+uuid.uuid4().hex[:10])
root.mkdir(parents=True)
server=http.server.ThreadingHTTPServer(('127.0.0.1',0),Handler)
threading.Thread(target=server.serve_forever,daemon=True).start()
cases={'ok':0,'fail':1,'wrong-id':1,'unknown':1,'redirect':1,'auth':1,'timeout':2,'transient':0}
def run(case):
    name,expected=case
    output=root/(name+'.json')
    cmd=[sys.executable,str(Path(__file__).with_name('remote_watch.py')),'--url',f'http://127.0.0.1:{server.server_port}/{name}',
         '--job-id','job-1','--output',str(output),'--interval','1','--timeout','4' if name!='timeout' else '1.2']
    p=subprocess.run(cmd,capture_output=True,timeout=10)
    assert p.returncode==expected,(name,p.stdout,p.stderr)
    assert output.exists()==(expected==0),(name,'unexpected artifact state')
    if expected==0:
        assert json.loads(output.read_text())['status']=='succeeded'
    return {'case':name,'passed':True,'exit_code':p.returncode,'return_bytes':len(p.stdout)+len(p.stderr)}
start=time.monotonic()
try:
    with ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(run,cases.items()))
    assert not mutations,mutations
    assert counts['/auth']==1
    assert counts['/redirect']==1
    assert counts['/ok']==3
    assert counts['/transient']==2
    report={'passed':len(results),'tests':results,'get_counts':counts,'mutating_requests':mutations,
            'seconds':round(time.monotonic()-start,3),'root':str(root)}
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report))
finally:
    server.shutdown()
    server.server_close()
