"""Agent-operated material commands; users supply files and scope, not JSON."""
from pathlib import Path
import omni_core as c


def configure(sub):
    p=sub.add_parser('materials');actions=p.add_subparsers(dest='material_action',required=True)
    p=actions.add_parser('import');p.add_argument('--file',type=Path,required=True);p.add_argument('--id');p.add_argument('--url');p.add_argument('--retry',action='store_true')
    actions.add_parser('list')
    for name in ('inspect','select'):
        p=actions.add_parser(name);p.add_argument('--id',required=True);p.add_argument('--version',required=True)
        if name=='select':p.add_argument('--pages');p.add_argument('--heading');p.add_argument('--unit',action='append');p.add_argument('--exclude-unit',action='append')
    p=actions.add_parser('search');p.add_argument('--query',required=True);p.add_argument('--selection',type=Path);p.add_argument('--limit',type=int,default=5)
    p=actions.add_parser('cite');p.add_argument('--selection',type=Path,required=True);p.add_argument('--unit',required=True);p.add_argument('--quote-file',type=Path,required=True);p.add_argument('--source-id',required=True);p.add_argument('--checked-at')


def execute(root,args):
    import omni_materials as m
    action=args.material_action
    if action=='import':return m.import_file(root,args.file,material_id=args.id,url=args.url,retry=args.retry)
    if action=='list':return {'materials':m.listing(root)}
    if action=='inspect':return m.inspect(root,args.id,args.version)
    if action=='select':return m.select(root,args.id,args.version,pages=args.pages,heading=args.heading,units=args.unit,exclude=args.exclude_unit)
    if action=='search':return {'evidence':m.search(root,args.query,selection=c.read(args.selection) if args.selection else None,limit=args.limit)}
    return m.citation(root,c.read(args.selection),args.unit,args.quote_file.read_text(encoding='utf-8').strip(),args.source_id,checked_at=args.checked_at)
