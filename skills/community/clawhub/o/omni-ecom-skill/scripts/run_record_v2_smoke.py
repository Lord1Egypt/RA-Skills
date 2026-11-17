"""Synthetic checks for the single authoritative 2.0 run journal."""
import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
COMMAND=ROOT/'skills'/'ecom-diagnosis-core'/'scripts'/'run_record.py'
VERSION='2.0.3-candidate.1'


class RunRecordV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.run_id='run-v2-record'; self.scope='synthetic'

    def call(self,*args,expected=0):
        result=subprocess.run([sys.executable,'-B','-X','utf8',str(COMMAND),*map(str,args)],
            capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        self.assertEqual(expected,result.returncode,result.stdout+result.stderr)
        return json.loads(result.stdout)

    def init(self):
        return self.call('init','--root',self.root,'--run-id',self.run_id,'--client-scope',self.scope,
                         '--package-version',VERSION,'--task-type','weekly_report')

    def test_init_uses_only_sqlite_and_show_is_native_readonly_snapshot(self):
        self.init(); run_dir=self.root/self.run_id
        self.assertTrue((run_dir/'run-journal.sqlite').is_file())
        self.assertFalse((run_dir/'run.json').exists()); self.assertFalse((run_dir/'events.jsonl').exists())
        value=self.call('show','--run-dir',run_dir,'--run-id',self.run_id,'--client-scope',self.scope)
        self.assertEqual(value['contract_name'],'omni-ecom.run-record')
        self.assertEqual(value['authority'],'derived_from_run_journal_sqlite')
        from jsonschema import Draft202012Validator
        schema=json.loads((ROOT/'schemas'/'run-record.schema.json').read_text(encoding='utf-8'))
        Draft202012Validator.check_schema(schema); Draft202012Validator(schema).validate(value)

    def test_legacy_mutation_commands_are_disabled(self):
        self.init(); run_dir=self.root/self.run_id
        value=self.call('status','--run-dir',run_dir,'--run-id',self.run_id,'--client-scope',self.scope,
                        '--status','verified',expected=1)
        self.assertEqual(value['error'],'legacy_run_record_mutation_disabled_use_host_runtime')
        shown=self.call('show','--run-dir',run_dir,'--run-id',self.run_id,'--client-scope',self.scope)
        self.assertEqual(shown['runtime_status']['selected_returns'],{})

    def test_cross_client_cannot_read_snapshot(self):
        self.init(); run_dir=self.root/self.run_id
        value=self.call('show','--run-dir',run_dir,'--run-id',self.run_id,'--client-scope','other',expected=1)
        self.assertEqual(value['error'],'run_scope_mismatch')

    def test_existing_run_is_not_overwritten(self):
        self.init(); database=self.root/self.run_id/'run-journal.sqlite'; before=database.read_bytes()
        value=self.call('init','--root',self.root,'--run-id',self.run_id,'--client-scope',self.scope,
                        '--package-version',VERSION,'--task-type','weekly_report',expected=1)
        self.assertEqual(value['error'],'run_directory_exists'); self.assertEqual(before,database.read_bytes())


if __name__=='__main__':
    unittest.main()
