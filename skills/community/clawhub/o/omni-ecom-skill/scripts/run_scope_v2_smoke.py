#!/usr/bin/env python3
"""Synthetic checks for the source-bound native 2.0 run-scope receipt."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

from host_runtime import Runtime


ROOT=Path(__file__).resolve().parents[1]
GUARD=ROOT/'skills'/'ecom-diagnosis-core'/'scripts'/'context_guard.py'
VERSION='2.0.3-candidate.1'


class RunScopeV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.root=Path(self.tmp.name)
        self.inputs=self.root/'inputs'; self.inputs.mkdir()
        self.source=self.inputs/'source.csv'
        self.source.write_text('metric,value\nGMV,100\n',encoding='utf-8')
        runtime=Runtime(self.root,'run-scope-test','synthetic')
        try: runtime.init(VERSION,'weekly_report')
        finally: runtime.close()

    def tearDown(self):
        self.tmp.cleanup()

    def call(self,*extra,expected=0,output=None,client='synthetic',selected=None):
        output=Path(output or self.root/'run-scope.json')
        selected=Path(selected or self.source)
        command=[sys.executable,str(GUARD),'--run-dir',str(self.root),
                 '--run-id','run-scope-test','--client-scope',client,
                 '--team-version',VERSION,'--allowed-root',str(self.inputs),
                 '--path',str(selected),'--output',str(output),*map(str,extra)]
        result=subprocess.run(command,text=True,capture_output=True,encoding='utf-8')
        self.assertEqual(expected,result.returncode,result.stdout+result.stderr)
        return json.loads(output.read_text(encoding='utf-8'))

    def test_valid_receipt_is_native_source_bound(self):
        receipt=self.call()
        self.assertEqual('omni-ecom.run-scope',receipt['contract_name'])
        self.assertEqual('2.0',receipt['schema_version'])
        self.assertEqual('scope_verified',receipt['status'])
        self.assertEqual(1,receipt['scanned_files'])
        self.assertEqual('inputs/source.csv',receipt['files'][0]['file'])
        self.assertEqual(64,len(receipt['files'][0]['sha256']))
        schema=json.loads((ROOT/'schemas'/'run-scope.schema.json').read_text(encoding='utf-8'))
        jsonschema.validate(receipt,schema)

    def test_forbidden_cross_scope_term_blocks(self):
        self.source.write_text('客户,PRIVATE_TEST_BRAND\n',encoding='utf-8')
        receipt=self.call('--forbid-term','PRIVATE_TEST_BRAND',expected=1)
        self.assertEqual('scope_blocked',receipt['status'])
        self.assertIn('forbidden_cross_scope_term:inputs/source.csv',receipt['errors'])

    def test_cross_client_runtime_scope_blocks(self):
        receipt=self.call(client='other-client',expected=1)
        self.assertEqual('scope_blocked',receipt['status'])
        self.assertTrue(any('run_scope_mismatch' in value for value in receipt['errors']))

    def test_output_inside_selected_input_blocks(self):
        receipt=self.call(output=self.inputs/'run-scope.json',selected=self.inputs,expected=1)
        self.assertEqual('scope_blocked',receipt['status'])
        self.assertIn('scope_output_inside_input_path',receipt['errors'])


if __name__=='__main__':
    unittest.main()
