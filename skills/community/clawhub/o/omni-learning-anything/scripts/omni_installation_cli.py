"""Host-operated bundle inspection and optional managed ZIP installation."""
from pathlib import Path


def configure(sub):
    p=sub.add_parser('installation');actions=p.add_subparsers(dest='install_action',required=True)
    p=actions.add_parser('inspect');p.add_argument('--path',type=Path,default=Path(__file__).resolve().parents[1])
    for name in ('install','update','adopt'):
        p=actions.add_parser(name);p.add_argument('--archive',type=Path,required=True);p.add_argument('--destination',type=Path,required=True);p.add_argument('--sha256',required=True)


def execute(args):
    import omni_installation as i
    if args.install_action=='inspect':return i.inspect(args.path)
    if args.install_action=='adopt':return i.adopt(args.archive,args.destination,args.sha256)
    return i.install(args.archive,args.destination,args.sha256,update=args.install_action=='update')
