"""Read-only course catalog commands; writing remains the host's responsibility."""
import json
import omni_courses as courses


def configure(sub):
    parser=sub.add_parser('courses');commands=parser.add_subparsers(dest='course_command',required=True)
    commands.add_parser('list');commands.add_parser('welcome')
    p=commands.add_parser('search');p.add_argument('--query',required=True)
    p=commands.add_parser('show');p.add_argument('--id',required=True)
    p=commands.add_parser('bind');p.add_argument('--id',required=True);p.add_argument('--unit',action='append',dest='units')
    p.add_argument('--pace',choices=['adapted','original_units'],default='adapted')
    p.add_argument('--practice',choices=['light','original_assignments'],default='light')
    p=commands.add_parser('check');p.add_argument('--config',required=True);p.add_argument('--plan',required=True)


def execute(args):
    command=args.course_command
    if command=='list':return courses.listing()
    if command=='welcome':return courses.welcome()
    if command=='search':return courses.resolve(args.query)
    if command=='show':return courses.show(args.id)
    if command=='bind':return courses.bind(args.id,args.units,args.pace,args.practice)
    from pathlib import Path
    config=json.loads(Path(args.config).read_text());plan=json.loads(Path(args.plan).read_text())
    courses.validate_course_plan(config,plan)
    return {'valid':True,'note':'Mapping and snapshot validation only; the host must check source access, pedagogical alignment, workload, and actual user approval.'}
