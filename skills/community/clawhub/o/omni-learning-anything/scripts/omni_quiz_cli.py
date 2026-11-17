"""Command adapter for host-operated checks, not learner command-line homework."""
from pathlib import Path
import omni_core as c


def configure(sub):
    parser=sub.add_parser('quiz'); actions=parser.add_subparsers(dest='quiz_action',required=True)
    p=actions.add_parser('prepare');p.add_argument('--input',type=Path,required=True)
    p=actions.add_parser('start');p.add_argument('--key',required=True);p.add_argument('--request-id',required=True);p.add_argument('--consent',required=True);p.add_argument('--revision',type=int);p.add_argument('--new-attempt',action='store_true');p.add_argument('--extra-time',action='store_true')
    for name in ('next','answer','hint','reveal','skip','pause','feedback','correct'):
        p=actions.add_parser(name);p.add_argument('--attempt',required=True)
        if name not in ('next','pause'):p.add_argument('--question',required=True)
        if name!='next':p.add_argument('--event-id',required=True)
        if name in ('answer','feedback','correct'):p.add_argument('--input',type=Path,required=True)
        if name=='answer':p.add_argument('--revise',action='store_true')
        if name=='feedback':p.add_argument('--answer-id',required=True)
        if name=='correct':p.add_argument('--replaces',required=True);p.add_argument('--reason-file',type=Path,required=True)
    actions.add_parser('status')
    p=actions.add_parser('export');p.add_argument('--output',type=Path,required=True);p.add_argument('--format',choices=['json','csv'],required=True)
    p=actions.add_parser('forget');p.add_argument('--confirm',action='store_true');p.add_argument('--scope',choices=['attempts','all'],default='attempts')


def execute(root,args):
    import omni_quiz as q
    action=args.quiz_action
    if action=='prepare':return q.prepare(root,c.read(args.input))
    if action=='start':return q.start(root,args.key,args.request_id,args.consent,revision=args.revision,new_attempt=args.new_attempt,extra_time=args.extra_time)
    if action=='next':return q.next_question(root,args.attempt)
    if action=='answer':return q.submit(root,args.attempt,args.question,args.event_id,c.read(args.input),revise=args.revise)
    if action in ('hint','reveal','skip','pause'):return q.action(root,args.attempt,getattr(args,'question',None),action,args.event_id)
    if action=='feedback':return q.feedback(root,args.attempt,args.question,args.event_id,args.answer_id,c.read(args.input))
    if action=='correct':return q.correct(root,args.attempt,args.question,args.event_id,args.replaces,args.reason_file.read_text(encoding='utf-8'),c.read(args.input))
    if action=='status':return q.status(root)
    from omni_quiz_export import export,forget
    if action=='export':return export(root,args.output,args.format)
    return forget(root,confirm=args.confirm,scope=args.scope)
