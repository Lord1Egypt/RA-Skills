"""Host-operated study helpers; learners use their normal conversation/cards."""
from pathlib import Path
import omni_core as c


def configure(sub):
    p=sub.add_parser('study');actions=p.add_subparsers(dest='study_action',required=True)
    p=actions.add_parser('plan');p.add_argument('--mode',choices=['balanced','new_first','review_only'],default='balanced');p.add_argument('--minutes',type=int)
    actions.add_parser('profile')
    p=actions.add_parser('report');p.add_argument('--days',type=int,default=7)
    p=actions.add_parser('evidence');p.add_argument('--item',required=True)
    p=actions.add_parser('annotate');p.add_argument('--item',required=True);p.add_argument('--kind',choices=['self_report','exclude','include'],required=True);p.add_argument('--note-file',type=Path,required=True);p.add_argument('--event-id',required=True)
    p=actions.add_parser('settings');p.add_argument('--minutes',type=int,required=True)
    p=actions.add_parser('start');p.add_argument('--item',required=True);p.add_argument('--request-id',required=True);p.add_argument('--consent',required=True)
    p=actions.add_parser('anki');p.add_argument('--output',type=Path,required=True)
    p=actions.add_parser('propose');p.add_argument('--input',type=Path,required=True)
    p=actions.add_parser('proposal');p.add_argument('--id',required=True)
    p=actions.add_parser('apply');p.add_argument('--id',required=True);p.add_argument('--destination',type=Path,required=True);p.add_argument('--consent',required=True)
    p=actions.add_parser('forget');p.add_argument('--confirm',action='store_true')


def execute(root,args):
    import omni_study as s
    a=args.study_action
    if a=='plan':return s.plan(root,mode=args.mode,minutes=args.minutes)
    if a=='profile':return s.profile(root)
    if a=='report':return s.report(root,days=args.days)
    if a=='evidence':return s.evidence(root,args.item)
    if a=='annotate':return s.annotate(root,args.item,args.kind,args.note_file.read_text(encoding='utf-8'),args.event_id)
    if a=='settings':return s.settings(root,minutes=args.minutes)
    if a=='start':return s.start(root,args.item,args.request_id,args.consent)
    if a=='forget':return s.forget(root,confirm=args.confirm)
    if a=='anki':
        from omni_study_export import anki
        return anki(root,args.output)
    import omni_course_revision as r
    if a=='propose':return r.propose(root,c.read(args.input))
    if a=='proposal':return r.inspect(root,args.id)
    return r.apply(root,args.id,args.destination,args.consent)
