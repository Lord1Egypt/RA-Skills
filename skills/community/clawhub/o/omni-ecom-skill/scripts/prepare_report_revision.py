"""Continue a rejected report in a new directory, retaining real analysis returns.

Only report corrections are supported here. Changed business inputs require
the affected analyses to be repeated through the ordinary native workflow.
The predecessor stays immutable history; the successor becomes the sole
current ledger. This program cannot create experts or approve a report.
"""
import argparse
import json
import re
import sqlite3
from datetime import datetime, timezone
from pathlib import Path
import shutil
from host_runtime import Runtime, ROLES, sha, require

MARKER='report-revision-successor.json'
GENERATED={'report.json','report.md','report.pdf','pdf-delivery.json',
           'report-build-receipt.json','claim-receipt.json','public-output-receipt.json',
           'release-receipt.json','completion-receipt.json','candidate-acceptance-receipt.json',
           'acceptance-finalize-receipt.json','revision-preparation-receipt.json'}

def excluded(relative):
    return (relative.parts[0] in ('revisions','.pdf_qa') or relative.name in GENERATED
            or relative.name.startswith(('run-journal.sqlite','review-manifest','review-launch-manifest'))
            or relative.name==MARKER or relative.parts[:2]==('task-cards','review'))

def prepare(source, revision):
    source=Path(source).resolve()
    require(re.fullmatch(r'R[2-9][0-9]*|R1[0-9]+',revision) is not None,'report_revision_invalid')
    require(not (source/MARKER).exists(),'report_revision_predecessor_already_archived')
    old=json.loads((source/'report.json').read_text(encoding='utf-8-sig'))
    require(int(revision[1:])==int(old['report_revision'][1:])+1,'report_revision_must_increment')
    target=source/'revisions'/revision
    require(not target.exists(),'report_revision_directory_already_exists')
    runtime=Runtime(source,old['run_id'],old['client_scope'],read_only=True)
    try:
        state=runtime.status()
        require(not state['waiting'] and not state['challenges_waiting'],'report_revision_tasks_pending')
        require(set(state['selected_returns'])==set(ROLES),'report_revision_analysis_returns_missing')
        events=runtime.journal.events(old['run_id'],old['client_scope'])
        reviews=[e for e in events if e['kind'].startswith('member_') and e['payload'].get('role')=='delivery-review']
        require(bool(reviews) and reviews[-1]['kind']=='member_rejected'
                and reviews[-1]['payload'].get('reason')=='runtime_review_requires_report_revision',
                'report_revision_requires_actual_review_change_request')
        require(not any(e['kind']=='delivery_completed' for e in events),'report_revision_completed_run_not_supported')
        from review_guard import validate_manifest, changed_entries
        manifest=json.loads((source/'review-manifest.json').read_text(encoding='utf-8-sig'))
        validate_manifest(manifest)
        require(not any(changed_entries(manifest)),'report_revision_frozen_predecessor_changed')
        journal_before=sha(source/'run-journal.sqlite')
        inputs={p.relative_to(source).as_posix():sha(p) for p in sorted(source.rglob('*'))
                if p.is_file() and not excluded(p.relative_to(source))}
        require(all((source/n).resolve().is_relative_to(source) for n in inputs),'report_revision_source_outside')
        target.mkdir(parents=True)
        for name,digest in inputs.items():
            destination=target/name;destination.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source/name,destination)
            require(sha(source/name)==sha(destination)==digest,'report_revision_source_changed')
        db=sqlite3.connect(target/'run-journal.sqlite')
        try:runtime.journal.db.backup(db)
        finally:db.close()
        require(sha(source/'run-journal.sqlite')==journal_before,'report_revision_journal_changed')
        quality=json.loads((target/'quality-inputs.json').read_text(encoding='utf-8-sig'))
        quality['report_revision']=revision
        (target/'quality-inputs.json').write_text(json.dumps(quality,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        receipt=dict(status='report_revision_directory_ready_not_delivery',
            run_id=old['run_id'],client_scope=old['client_scope'],team_version=old['team_version'],
            previous_revision=old['report_revision'],report_revision=revision,
            previous_directory=str(source),current_directory=str(target),
            source_journal_sha256=journal_before,retained_analysis_task_ids={r:state['selected_returns'][r]['agent_task_id'] for r in ROLES},
            copied_input_sha256=inputs,created_at=datetime.now(timezone.utc).isoformat(),
            notes='Same run and actual selected analyses; no experts restarted. Predecessor is history. Rebuild and independent review required.')
        with (target/'revision-preparation-receipt.json').open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
        with (source/MARKER).open('x',encoding='utf-8') as f:json.dump(receipt,f,ensure_ascii=False,indent=2)
        return receipt
    finally:runtime.close()

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--run-dir',required=True);p.add_argument('--revision',required=True)
    a=p.parse_args();print(json.dumps(prepare(a.run_dir,a.revision),ensure_ascii=False))
