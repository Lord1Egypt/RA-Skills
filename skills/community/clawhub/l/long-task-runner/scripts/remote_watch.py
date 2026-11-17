"""Read-only watcher for an ALREADY SUBMITTED HTTP JSON job. Never submits/cancels."""
import argparse
import json
import os
from pathlib import Path
import time
import urllib.error
import urllib.parse
import urllib.request

from runner import atomic


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise RuntimeError('Redirect refused; use the verified final status URL')


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--url',required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--job-id',required=True)
    p.add_argument('--id-field',default='id')
    p.add_argument('--status-field',default='status')
    p.add_argument('--success',nargs='+',default=['succeeded','completed'])
    p.add_argument('--failure',nargs='+',default=['failed','cancelled','canceled'])
    p.add_argument('--pending',nargs='+',default=['queued','pending','running','processing'])
    p.add_argument('--interval',type=float,default=15)
    p.add_argument('--timeout',type=float,default=3600)
    p.add_argument('--request-timeout',type=float,default=20)
    p.add_argument('--token-env',help='Optional bearer token ENVIRONMENT VARIABLE NAME, not its value')
    a=p.parse_args()
    u=urllib.parse.urlsplit(a.url)
    if u.username or u.password or not u.hostname or not (u.scheme=='https' or u.scheme=='http' and u.hostname in {'localhost','127.0.0.1','::1'}):
        p.error('Use HTTPS; HTTP only for loopback fixtures. Credentials in URLs forbidden.')
    if not 1<=a.interval<=300 or not 1<=a.timeout<=2592000 or not .1<=a.request_timeout<=60:
        p.error('interval 1..300, timeout 1..2592000, request-timeout .1..60')
    if len(set(a.success+a.failure+a.pending)) != len(a.success+a.failure+a.pending):
        p.error('status groups must be disjoint')
    headers={'Accept':'application/json'}
    if a.token_env:
        token=os.environ.get(a.token_env)
        if not token:
            p.error('Token environment variable is unset')
        headers['Authorization']='Bearer '+token
    opener=urllib.request.build_opener(NoRedirect())
    deadline=time.monotonic()+a.timeout
    errors=0
    queries=0
    previous=None
    a.output.parent.mkdir(parents=True,exist_ok=True)
    status_path=a.output.with_name(a.output.name+'.status.json')
    try:
        while time.monotonic()<deadline:
            delay=a.interval
            try:
                queries+=1
                remaining=deadline-time.monotonic()
                with opener.open(urllib.request.Request(a.url,headers=headers,method='GET'), timeout=min(a.request_timeout,max(.1,remaining))) as resp:
                    data=resp.read(1048577)
                if len(data)>1048576:
                    raise RuntimeError('Status payload exceeds 1 MiB')
                obj=json.loads(data)
                if not isinstance(obj,dict) or str(obj.get(a.id_field))!=a.job_id:
                    raise RuntimeError('Response job ID mismatch or non-object response')
                state=obj.get(a.status_field)
                if not isinstance(state,str) or state not in a.pending+a.failure+a.success:
                    raise RuntimeError('Unknown remote status; adapter contract needs review')
                errors=0
                if state!=previous:
                    atomic(status_path,{'job_id':a.job_id,'status':state,'queries':queries,'updated_at':time.time()})
                    previous=state
                if state in a.success:
                    atomic(a.output,obj)
                    print(json.dumps({'status':state,'queries':queries,'artifact':str(a.output.resolve())}))
                    return 0
                if state in a.failure:
                    print(json.dumps({'error':'E_REMOTE_FAILED','status':state,'queries':queries}))
                    return 1
            except (urllib.error.URLError,TimeoutError,OSError) as e:
                if isinstance(e,urllib.error.HTTPError):
                    if e.code not in {408,429,500,502,503,504}:
                        raise RuntimeError('Non-retryable HTTP status '+str(e.code)) from e
                    retry_after=e.headers.get('Retry-After','')
                    if retry_after.isdecimal():
                        delay=max(delay,min(300,int(retry_after)))
                errors+=1
                if errors>3:
                    raise RuntimeError('Read-only query failed more than 3 consecutive times') from e
                delay=max(delay,min(300,a.interval*2**(errors-1)))
            time.sleep(max(0,min(delay,deadline-time.monotonic())))
        print(json.dumps({'error':'E_REMOTE_TIMEOUT','queries':queries,'remote_cancelled':False}))
        return 2
    except (RuntimeError,ValueError) as e:
        print(json.dumps({'error':'E_REMOTE_PROTOCOL','detail':str(e)[:160],'queries':queries}))
        return 1


if __name__=='__main__':
    raise SystemExit(main())
