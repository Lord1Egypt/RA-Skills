#!/usr/bin/env python3
"""Gmail Connect entry point; no dependency installation or OpenClaw config writes."""
import argparse
import json
import os
from pathlib import Path
import random
import shutil
import signal
import subprocess
import sys
import threading
from gmail_connect.core import Gmail, Store, Problem

def doctor(gmail):
    binary=shutil.which('openclaw')
    version=None
    if binary:
        try:
            r=subprocess.run([binary,'--version'],capture_output=True,text=True,timeout=20)
            version=r.stdout.strip()[:200] if r.returncode==0 else 'Version probe failed'
        except subprocess.TimeoutExpired:version='Version probe timed out'
    osrel=Path('/etc/os-release')
    distro=osrel.read_text() if osrel.exists() else ''
    return {'python':sys.version.split()[0],'ubuntu':'ID=ubuntu' in distro,'openclaw':version,
            'openclawFound':bool(binary),'referenceRelease':'2026.9.6','compatibility':'Skills + host exec required; no gateway internals used.',
            'gmail':gmail.status(),'checks':'Read-only checks; no OpenClaw installation, upgrade, restart, or configuration changes.'}

def main():
    os.umask(0o077)
    p=argparse.ArgumentParser(description='Gmail Connect local wizard and agent CLI')
    sub=p.add_subparsers(dest='cmd',required=True)
    w=sub.add_parser('wizard');w.add_argument('--port',type=int,default=8766);w.add_argument('--no-browser',action='store_true')
    sub.add_parser('doctor');sub.add_parser('status');sub.add_parser('check');sub.add_parser('sync')
    q=sub.add_parser('search');q.add_argument('--query',default='in:inbox');q.add_argument('--limit',type=int,default=20);q.add_argument('--page')
    r=sub.add_parser('read');r.add_argument('id')
    sub.add_parser('events')
    d=sub.add_parser('draft');d.add_argument('--to',required=True);d.add_argument('--subject',required=True);d.add_argument('--body-file',required=True)
    m=sub.add_parser('monitor');m.add_argument('--interval',type=int,default=60)
    args=p.parse_args()
    if os.geteuid()==0:
        raise Problem('Run as the Ubuntu user who runs OpenClaw, without sudo.')
    g=Gmail(Store())
    if args.cmd=='wizard':
        from gmail_connect.server import serve
        serve(g,args.port,not args.no_browser);return
    if args.cmd=='monitor':
        stop=threading.Event()
        signal.signal(signal.SIGTERM,lambda *_:stop.set())
        signal.signal(signal.SIGINT,lambda *_:stop.set())
        failures=0
        while not stop.is_set():
            try:g.sync();failures=0
            except Problem as e:
                failures=min(failures+1,6)
                print(json.dumps({'error':str(e),'status':e.status}),flush=True)
            stop.wait(min(3600,max(30,args.interval)*(2**failures))+random.uniform(0,5))
        return
    if args.cmd=='doctor':out=doctor(g)
    elif args.cmd=='status':out=g.status()
    elif args.cmd=='check':out=g.api('profile')
    elif args.cmd=='sync':out=g.sync()
    elif args.cmd=='search':out=g.search(args.query,args.limit,args.page)
    elif args.cmd=='read':out=g.message(args.id,True)
    elif args.cmd=='events':out=g.events()
    elif args.cmd=='draft':
        source=Path(args.body_file)
        if source.stat().st_size>100000:raise Problem('Draft body exceeds 100,000 bytes.')
        out=g.draft(args.to,args.subject,source.read_text())
    print(json.dumps(out,indent=2))

if __name__=='__main__':
    try:main()
    except Problem as e:
        print(json.dumps({'error':str(e),'status':e.status}),file=sys.stderr);sys.exit(1)
    except (OSError,ValueError):
        print(json.dumps({'error':'Local file or input error; check paths, permissions, and available disk space.'}),file=sys.stderr);sys.exit(1)
