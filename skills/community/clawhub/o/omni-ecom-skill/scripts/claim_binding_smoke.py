"""Freeze/completion source binding; all business and host inputs synthetic."""
import contextlib
import copy
import io
import json
from pathlib import Path
import unittest
from unittest.mock import patch

import claim_guard
import completion_gate
import quality_gate_smoke as quality_fixture
import runtime_binding_smoke as runtime_fixture
from claim_source_guard import validate_sources, validate_report_sources
from quality_gate import validate_quality, sha, read


def write(path,data):
    path.write_text(json.dumps(data,ensure_ascii=False),encoding='utf-8')


class ClaimBindingTests(unittest.TestCase):
    def setUp(self):
        self.fx=quality_fixture.QualityTests(); self.fx.setUp()
        self.addCleanup(self.fx.tearDown)
        self.root,self.report=self.fx.root,self.fx.report

    def save(self): write(self.root/'report.json',self.report)

    def receipt(self,structure=False):
        args=['claim_guard.py','--claims',str(self.root/self.report['claim_ledger']['file']),
              '--report',str(self.root/'report.md'),'--output',str(self.root/'claim-receipt.json')]
        if structure: args.append('--structure-only')
        with patch('sys.argv',args),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(claim_guard.main(),0)
        return read(self.root/'claim-receipt.json')

    def test_recomputes_and_lists_all_freeze_inputs(self):
        result=validate_quality(self.root,self.report)
        files={row['file']:row['sha256'] for row in result['inputs']}
        for name in ('claims.json','claim-source.csv'):
            self.assertEqual(files[name],sha(self.root/name))
        actual=completion_gate.validate_claim_receipt(self.receipt(),self.root)
        self.assertEqual(actual,result['claim_source_gate'])

    def test_missing_ledger_cannot_pass_on_success_receipt(self):
        receipt=self.receipt()
        del self.report['claim_ledger']; self.save()
        with self.assertRaisesRegex(ValueError,'ledger_missing'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_source_removed_after_pass_receipt(self):
        receipt=self.receipt(); (self.root/'claim-source.csv').unlink()
        with self.assertRaisesRegex(ValueError,'outside_or_missing'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_source_changed_after_pass_receipt(self):
        receipt=self.receipt(); (self.root/'claim-source.csv').write_text('合成检查值\n8131\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'hash_mismatch'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_report_cannot_replace_ledger_numbers(self):
        receipt=self.receipt()
        self.report['claim_ledger']['claims'][0]['value']=8131; self.save()
        with self.assertRaisesRegex(ValueError,'projection_mismatch'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_original_ledger_change_is_detected(self):
        receipt=self.receipt(); path=self.root/'claims.json'
        ledger=read(path); ledger['claims'][0]['value']=8131; write(path,ledger)
        with self.assertRaisesRegex(ValueError,'ledger_hash_mismatch'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_forged_claim_value_fails_even_with_updated_hashes(self):
        receipt=self.receipt(); path=self.root/'claims.json'
        ledger=read(path); ledger['claims'][0]['value']=8131; write(path,ledger)
        self.report['claim_ledger'].update(sha256=sha(path),claims=ledger['claims'])
        receipt['claims_sha256']=sha(path); self.save()
        with self.assertRaisesRegex(ValueError,'value_not_reproducible'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_other_customer_receipt_rejected(self):
        receipt=self.receipt(); receipt['client_scope']='another-client'
        with self.assertRaisesRegex(ValueError,'recomputed_mismatch:client_scope'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_other_period_ledger_rejected(self):
        receipt=self.receipt(); path=self.root/'claims.json'; ledger=read(path)
        ledger['period']='2025'; ledger['claims'][0]['period']='2025'; write(path,ledger)
        self.report['claim_ledger'].update(sha256=sha(path),claims=ledger['claims']); self.save()
        with self.assertRaisesRegex(ValueError,'identity_mismatch:period'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_structure_only_and_renamed_structure_receipt_rejected(self):
        receipt=self.receipt(True)
        with self.assertRaisesRegex(ValueError,'claim_guard_not_passed'):
            completion_gate.validate_claim_receipt(receipt,self.root)
        receipt['status']='claim_guard_passed'
        with self.assertRaisesRegex(ValueError,'source_verification_missing'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_forged_receipt_checks_and_boolean_count_rejected(self):
        receipt=self.receipt(); receipt['source_checks'][0]['value']='8131'
        with self.assertRaisesRegex(ValueError,'recomputed_mismatch:source_checks'):
            completion_gate.validate_claim_receipt(receipt,self.root)
        receipt=self.receipt(); receipt['claims_count']=True
        with self.assertRaisesRegex(ValueError,'count_invalid'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_single_point_also_requires_sources(self):
        self.report['collaboration_mode']='single_point'; del self.report['claim_ledger']; self.save()
        config=self.fx.config(); config['handoffs']={'data-analyst':config['handoffs']['data-analyst']}
        write(self.root/'quality-inputs.json',config)
        with self.assertRaisesRegex(ValueError,'ledger_missing'): validate_quality(self.root,self.report)

    def test_nested_ledger_keeps_exact_relative_source_paths(self):
        nested=self.root/'inputs'; nested.mkdir()
        for name in ('claims.json','claim-source.csv'):
            (nested/name).write_bytes((self.root/name).read_bytes())
        self.report['claim_ledger']['file']='inputs/claims.json'; self.save()
        actual=completion_gate.validate_claim_receipt(self.receipt(),self.root)
        self.assertEqual({Path(row['file']).as_posix() for row in actual['inputs']},
                         {'inputs/claims.json','inputs/claim-source.csv'})

    def test_ledger_path_escape_rejected(self):
        self.report['claim_ledger']['file']='../claims.json'; self.save()
        with self.assertRaisesRegex(ValueError,'ledger_path_invalid'):
            validate_quality(self.root,self.report)

    def test_claim_omitted_from_markdown_cannot_complete(self):
        receipt=self.receipt()
        (self.root/'report.md').write_text('R001 交易.csv',encoding='utf-8')
        receipt['report_sha256']=sha(self.root/'report.md')
        with self.assertRaisesRegex(ValueError,'claim_not_referenced'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def replace_ledger(self, ledger):
        path=self.root/'claims.json'; write(path,ledger)
        errors,counts=claim_guard.validate_claims(ledger)
        self.assertEqual(errors,[])
        self.report['claim_ledger'].update(sha256=sha(path),claims=ledger['claims'],
                                           source_checks=validate_sources(ledger,self.root),**counts)
        self.save()

    def test_legacy_numeric_pass_cannot_complete_without_context(self):
        for policy in (None,'legacy_unbound'):
            with self.subTest(policy=policy):
                ledger=read(self.root/'claims.json')
                ledger.pop('source_context_policy',None)
                if policy is not None: ledger['source_context_policy']=policy
                ledger['claims'][0]['source_ref'].pop('contexts',None)
                self.replace_ledger(ledger)
                receipt=self.receipt()
                self.assertEqual(receipt['status'],'claim_guard_passed')
                with self.assertRaisesRegex(ValueError,'source_context_required'):
                    completion_gate.validate_claim_receipt(receipt,self.root)

    def test_formal_gate_not_disabled_by_report_mode_or_version(self):
        ledger=read(self.root/'claims.json'); ledger['source_context_policy']='legacy_unbound'
        del ledger['claims'][0]['source_ref']['contexts']
        self.report.update(collaboration_mode='single_point',source_context_policy='legacy_unbound')
        self.replace_ledger(ledger)
        receipt=self.receipt()
        with self.assertRaisesRegex(ValueError,'source_context_required'):
            completion_gate.validate_claim_receipt(receipt,self.root)
        self.report['team_version']='1.6.0'; self.save()
        with self.assertRaisesRegex(ValueError,'receipt_team_version_mismatch'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_bound_legacy_index_is_rechecked_not_rejected_by_label(self):
        ledger=read(self.root/'claims.json'); ledger.pop('source_context_policy')
        self.replace_ledger(ledger)
        actual=completion_gate.validate_claim_receipt(self.receipt(),self.root)
        self.assertEqual(actual['source_checks'][0]['source_context']['status'],'source_context_verified')

    def test_formal_gate_requires_platform_store_even_with_partial_legacy_context(self):
        ledger=read(self.root/'claims.json'); ledger.pop('source_context_policy')
        ledger.pop('scope'); self.report.pop('scope')
        for key in ('platform','store'): del ledger['claims'][0]['source_ref']['contexts'][key]
        self.replace_ledger(ledger)
        with self.assertRaisesRegex(ValueError,'source_context_store_platform_required'):
            completion_gate.validate_claim_receipt(self.receipt(),self.root)

    def test_forged_all_checked_summary_does_not_override_missing_context(self):
        ledger=read(self.root/'claims.json'); ledger['source_context_policy']='legacy_unbound'
        del ledger['claims'][0]['source_ref']['contexts']; self.replace_ledger(ledger)
        receipt=self.receipt()
        receipt['source_context_summary']=dict(status='all_verified_source_labels_checked',
                                               verified_sources=1,context_checked=1,context_unbound=0)
        with self.assertRaisesRegex(ValueError,'source_context_required'):
            completion_gate.validate_claim_receipt(receipt,self.root)

    def test_unknown_only_is_not_vacuous_formal_success(self):
        ledger=read(self.root/'claims.json'); ledger['claims'][0].update(status='unknown',value=None)
        self.replace_ledger(ledger)
        with self.assertRaisesRegex(ValueError,'formal_source_context_evidence_missing'):
            completion_gate.validate_claim_receipt(self.receipt(),self.root)

    def test_strict_preflight_cli_preserves_legacy_input_bytes(self):
        path=self.root/'claims.json'; ledger=read(path)
        ledger['source_context_policy']='legacy_unbound'; del ledger['claims'][0]['source_ref']['contexts']
        self.replace_ledger(ledger)
        before={name:(self.root/name).read_bytes() for name in ('claims.json','claim-source.csv','report.json','report.md')}
        args=['claim_guard.py','--claims',str(path),'--require-context','--output',str(self.root/'preflight.json')]
        with patch('sys.argv',args),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(claim_guard.main(),2)
        self.assertIn('source_context_required',read(self.root/'preflight.json')['errors'])
        self.assertEqual(before,{name:(self.root/name).read_bytes() for name in before})

    def test_strict_preflight_cli_accepts_bound_source(self):
        args=['claim_guard.py','--claims',str(self.root/'claims.json'),'--require-context',
              '--output',str(self.root/'preflight.json')]
        with patch('sys.argv',args),contextlib.redirect_stdout(io.StringIO()):
            self.assertEqual(claim_guard.main(),0)
        self.assertEqual(read(self.root/'preflight.json')['source_context_summary']['context_checked'],1)

    def test_strict_preflight_cannot_use_structure_only(self):
        args=['claim_guard.py','--claims',str(self.root/'claims.json'),'--require-context','--structure-only',
              '--output',str(self.root/'preflight.json')]
        with patch('sys.argv',args),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(claim_guard.main(),2)
        self.assertIn('claim_context_requires_source_read',read(self.root/'preflight.json')['errors'])

    def test_cli_output_cannot_overwrite_any_input_on_success_or_failure(self):
        for invalid in (False,True):
            for name in ('claims.json','claim-source.csv','report.md','report.json'):
                with self.subTest(invalid=invalid,name=name):
                    args=['claim_guard.py','--claims',str(self.root/'claims.json'),
                          '--report',str(self.root/'report.md'),'--output',str(self.root/name)]
                    if invalid: args.extend(['--require-context','--structure-only'])
                    before={n:(self.root/n).read_bytes() for n in
                            ('claims.json','claim-source.csv','report.md','report.json')}
                    out=io.StringIO()
                    with patch('sys.argv',args),contextlib.redirect_stderr(out):
                        self.assertEqual(claim_guard.main(),2)
                    self.assertIn('claim_output_overlaps_input',out.getvalue())
                    self.assertEqual(before,{n:(self.root/n).read_bytes() for n in before})

    def test_cli_hardlink_output_cannot_overwrite_source(self):
        source=self.root/'claim-source.csv'; alias=self.root/'alias.json'
        alias.hardlink_to(source); before=source.read_bytes()
        args=['claim_guard.py','--claims',str(self.root/'claims.json'),'--output',str(alias)]
        with patch('sys.argv',args),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(claim_guard.main(),2)
        self.assertEqual(source.read_bytes(),before)

    def test_malformed_index_does_not_write_to_unclassified_output(self):
        path=self.root/'claims.json'; path.write_text('{broken',encoding='utf-8')
        source=self.root/'claim-source.csv'; before=source.read_bytes()
        args=['claim_guard.py','--claims',str(path),'--output',str(source)]
        with patch('sys.argv',args),contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(claim_guard.main(),2)
        self.assertEqual(source.read_bytes(),before)


class RuntimeClaimTests(unittest.TestCase):
    def setUp(self):
        self.fx=runtime_fixture.BindingTests(); self.fx.setUp()
        self.addCleanup(self.fx.tearDown)
        self.root,self.report=self.fx.root,self.fx.report

    def test_review_success_cannot_complete_legacy_unbound_source(self):
        path=self.root/'claims.json'; ledger=read(path)
        ledger['source_context_policy']='legacy_unbound'; del ledger['claims'][0]['source_ref']['contexts']
        write(path,ledger)
        self.report['claim_ledger'].update(sha256=sha(path),claims=ledger['claims'],
                                           source_checks=validate_sources(ledger,self.root))
        write(self.root/'report.json',self.report)
        self.fx.freeze(); self.fx.review()
        code,out=self.fx.complete()
        self.assertNotEqual(code,0); self.assertIn('source_context_required',out)
        self.assertFalse((self.root/'completion.json').exists())
        self.assertNotEqual(self.fx.rt.status()['next_action'],'reuse_verified_delivery')

    def test_review_freezes_source_and_ledger(self):
        manifest=self.fx.freeze()
        files={Path(item['path']).name for item in manifest['sources']}
        self.assertTrue({'claims.json','claim-source.csv'}.issubset(files))
        self.fx.review(); code,out=self.fx.complete(); self.assertEqual(code,0,out)
        completion=read(self.root/'completion.json')
        for name in ('claims.json','claim-source.csv'):
            self.assertEqual(completion['input_fingerprints'][name],sha(self.root/name))

    def test_consistent_replacement_after_review_requires_new_review(self):
        self.fx.freeze(); self.fx.review()
        source=self.root/'claim-source.csv'
        source.write_text(source.read_text(encoding='utf-8').replace('\n100,','\n100.00,'),encoding='utf-8')
        path=self.root/'claims.json'; ledger=read(path)
        ledger['claims'][0]['source_ref']['source_sha256']=sha(source); write(path,ledger)
        quality_fixture.write_scope_receipt(self.root,self.report,[source])
        self.report['claim_ledger'].update(sha256=sha(path),claims=ledger['claims'],source_checks=validate_sources(ledger,self.root))
        write(self.root/'report.json',self.report)
        # Even forging a source-consistent render receipt cannot reuse the old
        # independent review. The placeholder PDF is explicitly not render proof.
        from claim_source_guard import validate_report_sources
        render=read(self.root/'pdf-delivery.json')
        render['claim_source_gate']=validate_report_sources(self.report,self.root,(self.root/'report.md').read_text(encoding='utf-8'))
        render['input_fingerprints']={name:sha(self.root/name) for name in ('report.json','report.md')}
        render['input_fingerprints'].update({item['file']:item['sha256'] for item in render['claim_source_gate']['inputs']})
        write(self.root/'pdf-delivery.json',render)
        code,out=self.fx.complete()
        self.assertNotEqual(code,0); self.assertIn('review_stale_blocked',out)
        self.assertFalse((self.root/'completion.json').exists())

    def test_source_change_after_completion_invalidates_reuse(self):
        self.fx.freeze(); self.fx.review()
        code,out=self.fx.complete(); self.assertEqual(code,0,out)
        (self.root/'claim-source.csv').write_text('合成检查值\n8131\n',encoding='utf-8')
        self.assertNotEqual(self.fx.rt.status()['next_action'],'reuse_verified_delivery')

    def test_source_change_during_final_check_prevents_commit(self):
        self.fx.freeze(); self.fx.review()
        original=completion_gate.validate_claim_receipt
        def alter_after_read(*args):
            result=original(*args)
            (self.root/'claim-source.csv').write_text('合成检查值\n8131\n',encoding='utf-8')
            return result
        with patch.object(completion_gate,'validate_claim_receipt',side_effect=alter_after_read):
            code,out=self.fx.complete()
        self.assertNotEqual(code,0); self.assertIn('quality_changed_before_completion',out)
        self.assertFalse((self.root/'completion.json').exists())


if __name__=='__main__': unittest.main()
