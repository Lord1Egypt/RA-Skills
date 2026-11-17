"""Synthetic integration of dispatch, freeze, review and completion binding.

Host exports and the PDF/public receipts are explicit fixture data. These
tests exercise orchestration integrity, NOT native host proof, PDF rendering,
platform data authenticity, or the public guard implementation. The claim
receipt is produced by the actual guard against an isolated synthetic source.
"""
import contextlib
import io
import json
import unittest
from pathlib import Path
from argparse import Namespace
from datetime import datetime, timezone
from unittest.mock import patch

import quality_gate_smoke as quality_fixture
import completion_gate
import review_guard
import build_report_package
import behavior_audit
import claim_guard
from jsonschema import Draft202012Validator
from host_runtime import Runtime, ROLES, load, sha, validate_analysis_binding, validate_review_binding


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False), encoding='utf-8')


class BindingTests(unittest.TestCase):
    def setUp(self):
        self.fixture=quality_fixture.QualityTests()
        self.fixture.setUp()
        self.root=self.fixture.root
        self.report=self.fixture.report
        self.report['task_type']='monthly_report'
        self.rt=Runtime(self.root,self.report['run_id'],self.report['client_scope'])
        self.rt.init('2.0.3','monthly_report')
        self.tasks={r:f'11111111-1111-4111-8111-{i:012d}' for i,r in enumerate((*ROLES,'delivery-review'),1)}
        self.report['expert_participation']=[
            dict(agent_id=role,participation_status='pending_review' if role=='delivery-review' else 'contributed',
                 agent_task_ids=[self.tasks[role]] if role in ROLES else [],contribution_summary='合成测试贡献')
            for role in ('omni-ecom-team-lead',*ROLES,'delivery-review')]
        write(self.root/'report.json',self.report)
        self.config=load(self.root/'quality-inputs.json')
        for role in ROLES:
            body=load(self.root/self.config['handoffs'][role])
            body['client_scope']=self.report['client_scope']
            self.begin(role)
            self.finish(role,body)
            self.config['handoffs'][role]=f'sealed/{role}.json'
        write(self.root/'quality-inputs.json',self.config)

    def tearDown(self):
        self.rt.close()
        self.fixture.tearDown()

    def begin(self,role,attempt='a1'):
        obs=dict(run_id=self.report['run_id'],client_scope=self.report['client_scope'],host='codex',
                 task_id=self.tasks[role],state='running',evidence_kind='synthetic_fixture')
        path=f'{role}-{attempt}-started.json'
        write(self.root/path,obs)
        self.rt.start(role,'codex',self.tasks[role],attempt,path)

    def finish(self,role,body,attempt='a1'):
        raw=f'{role}-{attempt}-raw.json'
        ret=f'{role}-{attempt}.return.json'
        obs=f'{role}-{attempt}-completed.json'
        write(self.root/raw,body)
        write(self.root/ret,dict(run_id=self.report['run_id'],agent_id=role,agent_task_id=self.tasks[role],
                                returned_at=datetime.now(timezone.utc).isoformat(),
                                attempt_id=attempt,return_status='completed',handoff_sha256=sha(self.root/raw),
                                contribution_summary='合成测试贡献',response={'result':'ok'}))
        write(self.root/obs,dict(run_id=self.report['run_id'],client_scope=self.report['client_scope'],
                                host='codex',task_id=self.tasks[role],state='completed',evidence_kind='synthetic_fixture'))
        self.rt.accept(role,'codex',self.tasks[role],attempt,raw,ret,obs,f'sealed/{role}.json')

    def freeze(self):
        # An explicit placeholder PDF isolates runtime checks from the renderer.
        (self.root/'report.pdf').write_bytes(b'%PDF-synthetic-placeholder-not-a-render-test')
        from claim_source_guard import validate_report_sources
        claims=validate_report_sources(self.report,self.root,(self.root/'report.md').read_text(encoding='utf-8'))
        fingerprints={name:sha(self.root/name) for name in ('report.json','report.md')}
        fingerprints.update({item['file']:item['sha256'] for item in claims['inputs']})
        write(self.root/'pdf-delivery.json',dict(**__import__('artifact_contract').native_receipt_identity('pdf_delivery','2.0.3'),status='pdf_render_verified',team_version='2.0.3',
              run_id=self.report['run_id'],client_scope=self.report['client_scope'],
              input_fingerprints=fingerprints,claim_source_gate=claims,
              report_revision='R1',report_file='report.pdf',report_sha256=sha(self.root/'report.pdf'),
              chart_count=3,page_count=1,blank_pages=[],evidence_kind='synthetic_fixture'))
        review_guard.prepare(Namespace(run_id=self.report['run_id'],client_scope=self.report['client_scope'],
              team_version='2.0.3',report_revision='R1',output=str(self.root/'review-manifest.json'),
              artifact=[str(self.root/n) for n in completion_gate.CORE_ARTIFACTS],
              source=[str(self.root/self.config['baseline'])]))
        return load(self.root/'review-manifest.json')

    def review(self):
        manifest=load(self.root/'review-manifest.json')
        self.begin('delivery-review','r1')
        body=dict(**__import__('artifact_contract').native_receipt_identity('review_result','2.0.3'),
                  run_id=self.report['run_id'],client_scope=self.report['client_scope'],
                  agent_id='delivery-review',agent_version='2.0.3',agent_task_id=self.tasks['delivery-review'],
                  review_attempt_id='r1',report_revision='R1',return_status='completed',review_status='passed',
                  findings=[],required_changes=[],contribution_summary='合成复核结果',
                  returned_at=datetime.now(timezone.utc).isoformat(),
                  reviewed_manifest_sha256=manifest['manifest_sha256'],
                  reviewed_artifacts=[dict(file=i['file'],sha256=i['sha256']) for i in manifest['artifacts']])
        self.finish('delivery-review',body,'r1')
        review_guard.attest_result(Namespace(manifest=str(self.root/'review-manifest.json'),
             review_result=str(self.root/'delivery-review-r1-raw.json'),
             agent_task_id=self.tasks['delivery-review'],review_attempt_id='r1',
             output=str(self.root/'attestation.json')))
        review_guard.verify(Namespace(manifest=str(self.root/'review-manifest.json'),
             attestation=str(self.root/'attestation.json'),receipt=str(self.root/'release-receipt.json')))

    def complete(self, version_info=None):
        write(self.root/'public-guard.json',dict(**__import__('artifact_contract').native_receipt_identity('public_output_guard','2.0.3'),status='public_output_guard_passed',
             artifacts=[dict(file=n,sha256=sha(self.root/n)) for n in ('report.json','report.md','report.pdf')],
             scanned=['report.json','report.md','report.pdf'],registered_terms_checked=0,
             evidence_kind='synthetic_fixture'))
        claim_args=['claim_guard.py','--claims',str(self.root/self.report['claim_ledger']['file']),
                    '--report',str(self.root/'report.md'),'--output',str(self.root/'claim-guard.json')]
        with patch('sys.argv',claim_args),contextlib.redirect_stdout(io.StringIO()),contextlib.redirect_stderr(io.StringIO()):
            claim_code=claim_guard.main()
        if claim_code:
            return claim_code,json.dumps(load(self.root/'claim-guard.json'))
        write(self.root/'version-info.json',version_info or dict(team_version='2.0.3',release_status='released',release_ready=True))
        args=['completion_gate.py','--report-dir',str(self.root),'--public-guard-receipt',str(self.root/'public-guard.json'),
              '--claim-receipt',str(self.root/'claim-guard.json'),'--version-info',str(self.root/'version-info.json'),
              '--manifest',str(self.root/'review-manifest.json'),'--attestation',str(self.root/'attestation.json'),
              '--release-receipt',str(self.root/'release-receipt.json'),'--output',str(self.root/'completion.json')]
        out=io.StringIO()
        with patch('sys.argv',args),contextlib.redirect_stdout(out),contextlib.redirect_stderr(out):
            result=completion_gate.main()
        return result,out.getvalue()

    def test_candidate_metadata_cannot_issue_formal_completion(self):
        self.freeze(); self.review()
        candidate=dict(team_version='2.0.3-candidate.1',release_status='candidate',release_ready=False,release_date=None)
        code,output=self.complete(candidate)
        self.assertNotEqual(code,0); self.assertIn('candidate_version_not_release_ready',output)
        self.assertFalse((self.root/'completion.json').exists())

    def test_full_synthetic_binding_with_codex_ids(self):
        manifest=self.freeze(); self.review()
        code,output=self.complete()
        self.assertEqual(code,0,output)
        receipt=load(self.root/'completion.json')
        self.assertEqual(receipt['runtime_gate']['analysis'],manifest['runtime_gate'])
        self.assertEqual(receipt['review_agent_task_id'],self.tasks['delivery-review'])
        self.assertEqual(len(receipt['runtime_gate']['analysis']['members']),4)
        self.assertEqual(self.rt.status()['next_action'],'reuse_verified_delivery')

    def test_generated_receipts_conform_to_schemas(self):
        self.freeze(); self.review()
        code,output=self.complete(); self.assertEqual(code,0,output)
        schemas=Path(__file__).resolve().parents[1]/'schemas'
        mapping={'review-manifest.json':'review-manifest.schema.json',
                 'delivery-review-r1-raw.json':'review-result.schema.json',
                 'attestation.json':'review-attestation.schema.json',
                 'release-receipt.json':'review-release.schema.json',
                 'claim-guard.json':'claim-guard-receipt.schema.json',
                 'public-guard.json':'public-output-receipt.schema.json',
                 'completion.json':'completion-receipt.schema.json',
                 'sealed/data-analyst.json':'handoff.schema.json'}
        for output,schema in mapping.items():
            with self.subTest(output=output):
                validator=Draft202012Validator(load(schemas/schema))
                self.assertEqual([e.message for e in validator.iter_errors(load(self.root/output))],[])

    def test_restart_recognizes_receipt_and_audit_event(self):
        self.freeze(); self.review()
        code,output=self.complete(); self.assertEqual(code,0,output)
        self.rt.close()
        self.rt=Runtime(self.root,self.report['run_id'],self.report['client_scope'],read_only=True)
        status=self.rt.status()
        self.assertEqual(status['completion']['status'],'formal_delivery_complete')
        self.assertEqual(status['next_action'],'reuse_verified_delivery')

    def test_changed_report_invalidates_reuse(self):
        self.freeze(); self.review()
        code,output=self.complete(); self.assertEqual(code,0,output)
        (self.root/'report.md').write_text('changed after delivery',encoding='utf-8')
        status=self.rt.status()
        self.assertEqual(status['completion']['status'],'completion_invalidated')
        self.assertNotEqual(status['next_action'],'reuse_verified_delivery')

    def test_changed_receipt_invalidates_reuse(self):
        self.freeze(); self.review()
        code,output=self.complete(); self.assertEqual(code,0,output)
        receipt=load(self.root/'completion.json')
        receipt['completed_at']='changed'
        write(self.root/'completion.json',receipt)
        self.assertEqual(self.rt.status()['completion']['status'],'completion_invalidated')

    def test_orphan_receipt_does_not_mean_completed(self):
        write(self.root/'completion.json',dict(status='formal_delivery_complete'))
        self.assertNotEqual(self.rt.status()['next_action'],'reuse_verified_delivery')
        self.assertNotIn('completion',self.rt.status())

    def test_comprehensive_report_cannot_hide_as_single_point(self):
        self.report['collaboration_mode']='single_point'
        write(self.root/'report.json',self.report)
        self.freeze()
        code,output=self.complete()
        self.assertEqual(code,2)
        self.assertIn('comprehensive_task_cannot_degrade',output)

    def test_missing_journal_blocks_without_creating_one(self):
        self.rt.close()
        (self.root/'run-journal.sqlite').rename(self.root/'saved.sqlite')
        with self.assertRaisesRegex(ValueError,'runtime_journal_missing'):
            validate_analysis_binding(self.root,self.report,self.config['handoffs'])
        self.assertFalse((self.root/'run-journal.sqlite').exists())

    def test_raw_unsealed_selection_blocked(self):
        bad=dict(self.config['handoffs'],**{'data-analyst':'data-analyst-a1-raw.json'})
        with self.assertRaisesRegex(ValueError,'runtime_selected_handoff_mismatch'):
            validate_analysis_binding(self.root,self.report,bad)

    def test_raw_return_tamper_blocks(self):
        write(self.root/'data-analyst-a1.return.json',{})
        with self.assertRaisesRegex(ValueError,'runtime_evidence_changed'):
            validate_analysis_binding(self.root,self.report,self.config['handoffs'])

    def test_report_client_cannot_use_other_journal(self):
        with self.assertRaisesRegex(ValueError,'run_scope_mismatch'):
            validate_analysis_binding(self.root,dict(self.report,client_scope='another-client'),self.config['handoffs'])

    def test_returned_member_cannot_open_attempt_that_would_invalidate_completion(self):
        self.freeze(); self.review()
        with self.assertRaisesRegex(ValueError,'member_already_returned'):
            self.begin('data-analyst','a2')
        selected,_=validate_analysis_binding(self.root,self.report,self.config['handoffs'])
        self.assertEqual(4,len(selected['members']))

    def test_unbound_activity_table_blocks(self):
        self.report['expert_participation'][1]['agent_task_ids']=['agent-invented']
        write(self.root/'report.json',self.report)
        self.freeze(); self.review()
        code,output=self.complete()
        self.assertEqual(code,2)
        self.assertIn('runtime_activity_task_mismatch',output)

    def test_reviewer_start_binds_frozen_manifest(self):
        self.freeze(); self.begin('delivery-review','r1')
        manifest=load(self.root/'review-manifest.json')
        manifest['created_at']='2000-01-01T00:00:00+00:00'
        manifest['manifest_sha256']=review_guard.payload_sha256(manifest,{'manifest_sha256'})
        write(self.root/'review-manifest.json',manifest)
        body=dict(run_id=self.report['run_id'],client_scope=self.report['client_scope'],
                  agent_id='delivery-review',agent_version='2.0.3')
        with self.assertRaisesRegex(ValueError,'runtime_review_manifest_changed'):
            self.finish('delivery-review',body,'r1')

    def test_fabricated_pass_cannot_override_actual_reviewer(self):
        self.freeze(); self.review()
        attestation=load(self.root/'attestation.json')
        attestation['contribution_summary']='not the returned result'
        with self.assertRaisesRegex(ValueError,'runtime_review_result_mismatch'):
            validate_review_binding(self.root,self.report,load(self.root/'review-manifest.json'),attestation)

    def test_review_receipt_binds_exact_attestation(self):
        self.freeze(); self.review()
        receipt=load(self.root/'release-receipt.json')
        receipt['review_attestation_sha256']='0'*64
        write(self.root/'release-receipt.json',receipt)
        code,output=self.complete()
        self.assertEqual(code,2)
        self.assertIn('review_release_attestation_mismatch',output)

    def test_one_native_task_cannot_impersonate_two_roles(self):
        self.tasks['delivery-review']=self.tasks['data-analyst']
        self.freeze()
        with self.assertRaisesRegex(ValueError,'task_reused_across_roles'):
            self.begin('delivery-review','r1')

    def test_runtime_snapshot_stable_after_reviewer_events(self):
        before,_=validate_analysis_binding(self.root,self.report,self.config['handoffs'])
        self.freeze(); self.review()
        after,_=validate_analysis_binding(self.root,self.report,self.config['handoffs'])
        self.assertEqual(before,after)

    def test_frozen_sources_cover_runtime_evidence_not_mutable_db(self):
        manifest=self.freeze()
        files={i['file'] for i in manifest['sources']}
        self.assertIn('data-analyst-a1-started.json',files)
        self.assertIn('data-analyst-a1.return.json',files)
        self.assertNotIn('run-journal.sqlite',files)

    def test_quality_scan_automatically_enters_behavior_snapshot(self):
        self.freeze()
        result=behavior_audit.snapshot(self.root,self.report['run_id'],self.report['client_scope'])
        scans=[s for s in result['samples'] if s['terminal_kind']=='quality_scan']
        self.assertEqual(len(scans),1)
        self.assertFalse(scans[0]['has_conflict'])
        self.assertEqual(scans[0]['evidence_kind'],'synthetic_fixture')

    def test_report_builder_accepts_real_id_format_and_return_timestamp(self):
        primary=load(self.root/self.config['handoffs']['data-analyst'])
        primary['agent_id']='omni-ecom-team-lead'
        path=self.root/'lead.json'; write(path,primary)
        args=Namespace(collaboration_mode='comprehensive',
                       member_handoff=[str(self.root/f) for f in self.config['handoffs'].values()])
        participation,status,_=build_report_package.load_collaboration(args,primary,path)
        self.assertEqual(status,'awaiting_delivery_review')
        data=next(i for i in participation if i['agent_id']=='data-analyst')
        self.assertEqual(data['agent_task_ids'],[self.tasks['data-analyst']])
        self.assertTrue(data['agent_returned_at'])


if __name__=='__main__': unittest.main()
