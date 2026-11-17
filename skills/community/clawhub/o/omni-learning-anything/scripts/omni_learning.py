#!/usr/bin/env python3
"""Omni Learning Anything deterministic helpers. Run --help for commands."""
import sys
if sys.version_info < (3, 10):
    raise SystemExit("Python 3.10+ required; current interpreter is " + sys.version.split()[0] + ". Select a supported Python interpreter and retry.")

import argparse
import json
import re
from pathlib import Path
import omni_core as c


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    version=re.search(r'^  version: "([0-9]+\.[0-9]+\.[0-9]+)"$',(Path(__file__).resolve().parents[1]/'SKILL.md').read_text(),re.M).group(1)
    parser.add_argument('--version',action='version',version='omni-learning-anything '+version)
    parser.add_argument('--project',type=Path,default=Path.cwd())
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('connect'); p.add_argument('--platform',choices=['notion','feishu','obsidian','dingtalk','tencent']); p.add_argument('--location'); p.add_argument('--connection'); p.add_argument('--save-as'); p.add_argument('--cli-profile'); p.add_argument('--workspace-id'); p.add_argument('--auth-profile'); p.add_argument('--subdir',default='Omni Learning')
    p=sub.add_parser('connection-show'); p.add_argument('--name',required=True)
    sub.add_parser('connection-list')
    p=sub.add_parser('tencent-auth');p.add_argument('action',choices=['login','start','poll','status']);p.add_argument('--name',required=True)
    p=sub.add_parser('doctor'); p.add_argument('--config',type=Path); p.add_argument('--host'); p.add_argument('--host-report',type=Path); p.add_argument('--background',action='store_true')
    p=sub.add_parser('setup-check'); p.add_argument('--platform',required=True); p.add_argument('--mode'); p.add_argument('--material-format')
    p=sub.add_parser('brief-check'); p.add_argument('--input',type=Path,required=True)
    p=sub.add_parser('onboarding-record'); p.add_argument('--event',required=True); p.add_argument('--id',dest='event_id',required=True); p.add_argument('--stage'); p.add_argument('--user-actions',type=int); p.add_argument('--usage',type=Path)
    sub.add_parser('onboarding-status')
    p=sub.add_parser('init'); p.add_argument('--config',type=Path,required=True); p.add_argument('--plan',type=Path,required=True)
    p=sub.add_parser('render'); p.add_argument('--input',type=Path,required=True); p.add_argument('--key',required=True); p.add_argument('--format',dest='formats',action='append',choices=['pdf','markdown','docx','html'])
    p=sub.add_parser('review'); p.add_argument('--key',required=True); p.add_argument('--note',required=True)
    sub.add_parser('approve'); sub.add_parser('next'); sub.add_parser('pause'); sub.add_parser('resume')
    p=sub.add_parser('delivered'); p.add_argument('--day',type=int,required=True)
    p=sub.add_parser('schedule-record'); p.add_argument('--host',required=True); p.add_argument('--job-id',required=True)
    sub.add_parser('delivery-check')
    for command in ('publish','delivery-status'):
        p=sub.add_parser(command); p.add_argument('--key',required=True)
    p=sub.add_parser('receipt-record'); p.add_argument('--key',required=True); p.add_argument('--receipt',type=Path,required=True)
    p=sub.add_parser('reconcile'); p.add_argument('--key',required=True); p.add_argument('--remote-id'); p.add_argument('--url'); p.add_argument('--task-id')
    from omni_quiz_cli import configure
    configure(sub)
    from omni_material_cli import configure as configure_materials
    configure_materials(sub)
    from omni_study_cli import configure as configure_study
    configure_study(sub)
    from omni_installation_cli import configure as configure_installation
    configure_installation(sub)
    from omni_courses_cli import configure as configure_courses
    configure_courses(sub)
    from omni_textbooks_cli import configure as configure_textbooks
    configure_textbooks(sub)
    args=parser.parse_args(); root=args.project.resolve(); result={'ok':True}
    try:
        if args.command=='textbooks':
            from omni_textbooks_cli import execute as execute_textbooks
            result=execute_textbooks(root,args)
        elif args.command=='courses':
            from omni_courses_cli import execute as execute_courses
            result=execute_courses(args)
        elif args.command=='installation':
            from omni_installation_cli import execute as execute_installation
            result=execute_installation(args)
        elif args.command=='setup-check':
            from omni_setup import plan as setup_plan
            result=setup_plan(args.platform,args.mode,material_format=args.material_format)
        elif args.command=='study':
            from omni_study_cli import execute as execute_study
            result=execute_study(root,args)
        elif args.command=='materials':
            from omni_material_cli import execute as execute_materials
            result=execute_materials(root,args)
        elif args.command=='quiz':
            from omni_quiz_cli import execute
            result=execute(root,args)
        elif args.command=='tencent-auth':
            from omni_tencent_auth import Auth,login
            result=login(args.name) if args.action=='login' else getattr(Auth(),args.action)(args.name)
        elif args.command=='connect':
            from omni_connections import connect
            result=connect(args.platform,args.location,connection=args.connection,save_as=args.save_as,cli_profile=args.cli_profile,workspace_id=args.workspace_id,auth_profile=args.auth_profile,subdir=args.subdir)
        elif args.command=='connection-list':
            from omni_connections import list_connections
            result={'connections':list_connections()}
        elif args.command=='connection-show':
            from omni_connections import load
            result={'delivery':load(args.name)}
        elif args.command=='doctor':
            from omni_readiness import diagnose
            result=diagnose(root,c.read(args.host_report) if args.host_report else None,background=args.background,config_path=args.config,host=args.host)
        elif args.command=='brief-check':
            from omni_intake import validate_brief
            result=validate_brief(c.read(args.input))
        elif args.command=='onboarding-record':
            from omni_onboarding import record
            result=record(root,args.event,args.event_id,stage=args.stage,user_actions=args.user_actions,usage=c.read(args.usage) if args.usage else None)
        elif args.command=='onboarding-status':
            from omni_onboarding import status
            result=status(root)
        elif args.command=='init': c.initialize(root,c.read(args.config),c.read(args.plan))
        elif args.command=='render':
            from omni_document import render
            from omni_delivery import default_formats
            m=render(root,args.input,args.key,args.formats or default_formats(c.read(root/'config.json'))); result={k:v for k,v in m.items() if k!='files'}
        elif args.command=='review':
            from omni_document import review
            review(root,args.key,args.note)
        elif args.command=='approve': c.approve(root)
        elif args.command=='next': result=c.next_action(root)
        elif args.command=='delivered': result=c.deliver(root,args.day)
        elif args.command in ('pause','resume'): c.set_status(root,'paused' if args.command=='pause' else 'active')
        elif args.command=='schedule-record': c.record_schedule(root,args.host,args.job_id)
        elif args.command=='delivery-check':
            from omni_delivery import preflight
            result=preflight(c.read(root/'config.json').get('delivery'))
        elif args.command=='publish':
            from omni_delivery import publish
            result=publish(root,args.key)
        elif args.command=='delivery-status':
            from omni_delivery import status
            result=status(root,args.key)
        elif args.command=='receipt-record':
            from omni_delivery import record_receipt
            result=record_receipt(root,args.key,c.read(args.receipt))
        elif args.command=='reconcile':
            from omni_delivery import reconcile
            result=reconcile(root,args.key,args.remote_id,args.url,args.task_id)
    except ModuleNotFoundError as e:
        packages={'requests':'requests','keyring':'keyring','docx':'python-docx','PIL':'Pillow','pypdf':'pypdf','pypdfium2':'pypdfium2','qcloud_cos':'cos-python-sdk-v5'}
        package=packages.get((e.name or '').split('.')[0])
        if not package: raise
        parser.exit(1,json.dumps({'ok':False,'stage':'dependencies','dependency':package,'error':'Install '+package+' in this interpreter using the selected route requirements; run doctor and see references/setup.md.'})+'\n')
    except (ValueError,RuntimeError,OSError,KeyError) as e:
        parser.exit(1,json.dumps({'ok':False,'error':str(e)},ensure_ascii=False)+'\n')
    print(json.dumps(result,ensure_ascii=False,indent=2))

if __name__=='__main__': main()
