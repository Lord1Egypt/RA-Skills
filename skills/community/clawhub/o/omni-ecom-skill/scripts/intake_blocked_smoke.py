#!/usr/bin/env python3
"""Synthetic checks for a truthful zero-input terminal outcome without a report."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

from artifact_contract import native_run_scope_identity,native_stage_identity
from host_runtime import Runtime

ROOT=Path(__file__).resolve().parents[1]; SCRIPT=Path(__file__).with_name('intake_blocked.py')
VERSION='2.0.3-candidate.1'; RUN='intake-empty-run'; CLIENT='synthetic'


class IntakeBlockedTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        runtime=Runtime(self.root,RUN,CLIENT)
        try: runtime.init(VERSION,'store_diagnosis')
        finally: runtime.close()
        self.inventory=self.root/'report-inventory.json'; self.scope=self.root/'run-scope.json'
        self.inventory.write_text(json.dumps(dict(**native_stage_identity('report_inventory',VERSION),
            run_id=RUN,client_scope=CLIENT,team_version=VERSION,issued_at='2026-09-08T00:00:00+00:00',
            scanned_root='inputs',report_count=0,identification=dict(mode='rule_first_model_fallback',
            type_taxonomy_version='t15-1.0',domain_taxonomy_version='d10-1.0',rule_hits=0,model_hits=0,
            unidentified=0,low_confidence_ids=[],model_review_pending=[]),reports=[]),ensure_ascii=False),encoding='utf-8')
        (self.root/'inputs').mkdir()
        self.scope.write_text(json.dumps(dict(**native_run_scope_identity(VERSION),run_id=RUN,client_scope=CLIENT,
            team_version=VERSION,status='scope_blocked',allowed_roots=['inputs'],input_paths=['inputs'],files=[],
            scanned_files=0,errors=['run_scope_no_files']),ensure_ascii=False),encoding='utf-8')

    def tearDown(self): self.tmp.cleanup()

    def call(self,expected=0,client=CLIENT):
        result=subprocess.run([sys.executable,str(SCRIPT),'--run-dir',str(self.root),'--run-id',RUN,
            '--client-scope',client,'--team-version',VERSION],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(expected,result.returncode,result.stdout+result.stderr)
        return json.loads(result.stdout)

    def status(self):
        runtime=Runtime(self.root,RUN,CLIENT,read_only=True)
        try: return runtime.status()
        finally: runtime.close()

    def test_zero_input_closes_without_report_and_is_idempotent(self):
        first=self.call(); second=self.call()
        self.assertEqual(first['receipt_sha256'],second['receipt_sha256'])
        receipt=json.loads((self.root/'intake-blocked.json').read_text(encoding='utf-8'))
        self.assertFalse(receipt['report_generated']); self.assertFalse(receipt['formal_delivery_completed'])
        self.assertFalse((self.root/'report.pdf').exists())
        self.assertEqual('intake_blocked_no_report',self.status()['terminal_outcome'])
        self.assertEqual(1,self.status()['events'])
        jsonschema.validate(receipt,json.loads((ROOT/'schemas'/'intake-blocked.schema.json').read_text(encoding='utf-8')))
        runtime=Runtime(self.root,RUN,CLIENT,read_only=True)
        try: event=runtime.journal.events(RUN,CLIENT)[0]['payload']
        finally: runtime.close()
        jsonschema.validate(event,json.loads((ROOT/'schemas'/'intake-blocked-event.schema.json').read_text(encoding='utf-8')))

    def test_nonempty_inventory_cannot_use_zero_input_outcome(self):
        value=json.loads(self.inventory.read_text(encoding='utf-8')); value.update(report_count=1,reports=[{'report_id':'R001'}])
        self.inventory.write_text(json.dumps(value),encoding='utf-8')
        self.assertIn('intake_inventory_not_empty',self.call(expected=1)['reason'])
        self.assertIsNone(self.status()['terminal_outcome'])

    def test_started_run_cannot_be_relabelled_as_zero_input(self):
        runtime=Runtime(self.root,RUN,CLIENT)
        try: runtime.journal.append(RUN,CLIENT,'phase-inventory','phase',{'phase':'inventory'})
        finally: runtime.close()
        self.assertIn('intake_blocked_event_invalid',self.call(expected=1)['reason'])
        self.assertIsNone(self.status()['terminal_outcome'])

    def test_cross_client_cannot_close_run(self):
        self.assertIn('run_scope_mismatch',self.call(expected=1,client='other')['reason'])
        self.assertIsNone(self.status()['terminal_outcome'])

    def test_generic_journal_cli_cannot_forge_terminal_outcome(self):
        fake=self.root/'fake.json'; fake.write_text('{}',encoding='utf-8')
        result=subprocess.run([sys.executable,str(ROOT/'scripts'/'run_journal.py'),'--db',str(self.root/'run-journal.sqlite'),
            '--run-id',RUN,'--client-scope',CLIENT,'record','--event-key','fake','--kind','intake_blocked',
            '--payload',str(fake)],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(2,result.returncode); self.assertIn('terminal_outcome_owned_by_gate',result.stdout)


if __name__=='__main__': unittest.main()
