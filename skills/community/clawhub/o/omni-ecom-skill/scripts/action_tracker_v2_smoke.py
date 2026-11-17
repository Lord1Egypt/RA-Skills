#!/usr/bin/env python3
"""Synthetic checks for the disabled 1.x action writer and read-only history view."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT=Path(__file__).resolve().parents[1]
TRACKER=Path(__file__).with_name('action_tracker.py')


class ActionTrackerV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.approvals=self.root/'approvals'; self.approvals.mkdir()
        self.action=self.approvals/'A001.json'
        self.action.write_text(json.dumps(dict(schema_version='1.0',action_id='A001',run_id='legacy-run',
            client_scope='synthetic',status='verified',approval_state='approved',priority='P1',action='legacy')),
            encoding='utf-8')
        self.action.with_suffix('.events.jsonl').write_text(json.dumps({'type':'outcome_recorded'})+'\n',encoding='utf-8')

    def tearDown(self): self.tmp.cleanup()

    def call(self,*args,expected=0):
        result=subprocess.run([sys.executable,str(TRACKER),*map(str,args)],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(expected,result.returncode,result.stdout+result.stderr)
        return json.loads(result.stdout if result.returncode==0 else result.stderr)

    def test_legacy_mutations_are_disabled_without_writes(self):
        before={p.name:p.read_bytes() for p in self.approvals.iterdir()}
        for command in ('create','approve','transition','outcome'):
            with self.subTest(command=command):
                result=self.call(command,'--root',self.root,'--output',self.approvals/'new.json',expected=1)
                self.assertEqual('legacy_action_tracker_write_disabled_use_v2_action_policy_and_gateway',result['error'])
        self.assertEqual(before,{p.name:p.read_bytes() for p in self.approvals.iterdir()})

    def test_show_is_scoped_read_only_v2_view(self):
        value=self.call('show','--action-file',self.action,'--client-scope','synthetic')
        self.assertEqual('omni-ecom.action-history-view',value['contract_name'])
        self.assertFalse(value['legacy_compatibility']['current_execution_authority'])
        self.assertEqual(1,value['count']); self.assertEqual(1,len(value['records'][0]['events']))
        schema=json.loads((ROOT/'schemas'/'action-history-view.schema.json').read_text(encoding='utf-8'))
        jsonschema.validate(value,schema)

    def test_cross_client_history_is_rejected(self):
        value=self.call('show','--action-file',self.action,'--client-scope','other',expected=1)
        self.assertEqual('legacy_action_client_scope_mismatch',value['error'])

    def test_native_v2_action_cannot_enter_legacy_viewer(self):
        value=json.loads(self.action.read_text(encoding='utf-8')); value['schema_version']='2.0'
        self.action.write_text(json.dumps(value),encoding='utf-8')
        result=self.call('show','--action-file',self.action,'--client-scope','synthetic',expected=1)
        self.assertEqual('legacy_action_schema_invalid',result['error'])

    def test_list_filters_scope_and_status_without_mutation(self):
        other=self.approvals/'A002.json'
        other.write_text(json.dumps(dict(schema_version='1.0',action_id='A002',run_id='legacy-run',
            client_scope='other',status='verified')),encoding='utf-8')
        value=self.call('list','--root',self.root,'--client-scope','synthetic','--status','verified')
        self.assertEqual(1,value['count']); self.assertEqual('A001',value['records'][0]['action']['action_id'])


if __name__=='__main__': unittest.main()
