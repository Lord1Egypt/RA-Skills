#!/usr/bin/env python3
"""Create a page-local revision scope without silently widening or overcorrecting feedback."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from workflow_contracts import LOCAL_REVISION_DOMAINS, digest, load_object, validate_revision_changes, write_object


def invalidate(state:dict,plan:dict,text:str,reason:str,state_path:Path)->None:
    pages=[p.get('page') for p in plan.get('pages',[])]
    state.update({'status':'gate_invalidated_by_revision','explicit_approval':None,
        'permitted_render_pages':pages[:1],'blocked_render_pages':pages[1:],
        'gate_invalidation':{'reason':reason,'exact_user_request':text,'at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds')}})
    write_object(state_path,state)

def main()->int:
    p=argparse.ArgumentParser(description='Create a typed page-local revision scope or invalidate the sample gate when required')
    p.add_argument('--render-plan',required=True,type=Path);p.add_argument('--state',required=True,type=Path)
    p.add_argument('--staging-manifest',required=True,type=Path);p.add_argument('--changes',required=True,type=Path,help='JSON object with a changes array')
    p.add_argument('--request-text',required=True,help='Exact user correction request')
    p.add_argument('--impact',required=True,choices=('page-local','sample-style-system'))
    p.add_argument('--output',required=True,type=Path)
    args=p.parse_args()
    try:
        plan=load_object(args.render_plan,'render plan');state=load_object(args.state,'approval state');stage=load_object(args.staging_manifest,'staging manifest');payload=load_object(args.changes,'revision changes')
        if state.get('status') not in {'batch_approved','revision_completed'}:raise ValueError('page-local revisions require an approved batch')
        if digest(args.render_plan)!=state.get('render_plan_sha256'):raise ValueError('render plan changed; return to plan+sample gate')
        text=args.request_text.strip()
        if not text:raise ValueError('exact user request is required')
        valid={int(pg['page']) for pg in plan.get('pages',[])};changes=payload.get('changes');errors=validate_revision_changes(changes,valid)
        if errors:raise ValueError('; '.join(errors))
        sample=int(state.get('sample_page'))
        affected=sorted({int(c['page']) for c in changes})
        nonlocal_domains = sorted({str(c.get('domain')) for c in changes if c.get('domain') not in LOCAL_REVISION_DOMAINS})
        if args.impact=='sample-style-system' or sample in affected or nonlocal_domains:
            reason = ('non-local revision domains: ' + ', '.join(nonlocal_domains)) if nonlocal_domains else ('sample/style/system decision changed' if args.impact=='sample-style-system' else 'approved sample page changed')
            invalidate(state,plan,text,reason,args.state)
            print('Revision invalidated batch approval; rebuild, re-discuss, and re-approve the plan+sample gate',file=sys.stderr);return 5
        stale=sorted({int(c['page']) for c in changes if c['operation']!='preserve_unchanged'})
        if not stale:raise ValueError('revision contains no actionable page change')
        by_page={page:[] for page in stale}
        for change in changes:
            if int(change['page']) in by_page:by_page[int(change['page'])].append(change)
        scoped=copy.deepcopy(plan);scoped['pages']=[pg for pg in scoped['pages'] if int(pg['page']) in stale]
        for pg in scoped['pages']:
            directives=by_page[int(pg['page'])];pg['revision_directives']=directives
            pg['render_prompt']+=' Revision directives (apply literally; do not broaden them): '+ '; '.join(f"{d['operation']} {d['target']}: {d['instruction']}" for d in directives)+'.'
        baseline={str(e['page']):e['sha256'] for e in stage.get('files',[])}
        unchanged=sorted(valid-set(stale))
        state.update({'status':'revision_in_progress','active_revision':{
            'created_at_utc':datetime.now(timezone.utc).isoformat(timespec='seconds'),'exact_user_request':text,
            'impact':'page-local','operations':changes,'affected_pages':affected,'stale_pages':stale,
            'preserve_unchanged_pages':unchanged,'baseline_stage':baseline,'baseline_stage_manifest_sha256':digest(args.staging_manifest)}})
        state.setdefault('revision_ledger',[]).append(state['active_revision']);write_object(args.state,state)
        scoped['render_scope']={'mode':'revision','page_numbers':stale,'unchanged_pages':unchanged,'exact_user_request':text,
            'operation_semantics':{'remove':'delete only the named target','retain_but_simplify':'keep the target while reducing detail/quantity','add_as_secondary':'add subordinate to the existing primary hierarchy','preserve_unchanged':'do not alter the named target'}}
        args.output.parent.mkdir(parents=True,exist_ok=True);write_object(args.output,scoped)
        print(f'Wrote page-local revision scope for pages {stale}; unchanged approved pages {unchanged} are hash-locked')
        return 0
    except ValueError as exc:print(f'Revision scope blocked: {exc}',file=sys.stderr);return 4
if __name__=='__main__':raise SystemExit(main())
