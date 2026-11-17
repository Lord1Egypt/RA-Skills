#!/usr/bin/env python3
"""Synthetic native 2.0 checks for normalization and deterministic metric gating."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

ROOT=Path(__file__).resolve().parents[1]
CORE=ROOT/'skills'/'ecom-diagnosis-core'/'scripts'
NORMALIZE=CORE/'normalize_reports.py'; METRIC=CORE/'metric_gate.py'
VERSION='2.0.3-candidate.1'; RUN='fact-pipeline-run'; CLIENT='synthetic'


class FactPipelineV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.raw=self.root/'交易.csv'
        self.raw.write_text('日期,成交金额,访客数,支付买家数,支付订单数\n2026-09-01,100,10,2,2\n',encoding='utf-8-sig')
        self.normalized=self.root/'normalized.json'; self.metrics=self.root/'metrics.json'

    def tearDown(self): self.tmp.cleanup()

    def call(self,script,*args,expected=0):
        result=subprocess.run([sys.executable,str(script),*map(str,args)],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(expected,result.returncode,result.stdout+result.stderr)
        return result

    def normalize(self,expected=0,client=CLIENT,output=None):
        return self.call(NORMALIZE,self.raw,'--platform','tmall','--run-id',RUN,'--client-scope',client,
                         '--team-version',VERSION,'--output',output or self.normalized,expected=expected)

    def metric(self,input_path=None,expected=0,client=CLIENT,output=None):
        return self.call(METRIC,input_path or self.normalized,'--run-id',RUN,'--client-scope',client,
                         '--team-version',VERSION,'--output',output or self.metrics,expected=expected)

    def test_normalizer_writes_native_source_bound_bundle(self):
        self.normalize(); value=json.loads(self.normalized.read_text(encoding='utf-8'))
        self.assertEqual('omni-ecom.normalized-report',value['contract_name'])
        self.assertEqual(hashlib.sha256(self.raw.read_bytes()).hexdigest(),value['source_manifest']['sha256'])
        schema=json.loads((ROOT/'schemas'/'normalized-report.schema.json').read_text(encoding='utf-8'))
        jsonschema.validate(value,schema)

    def test_metric_gate_consumes_native_bundle_and_binds_hash(self):
        self.normalize(); self.metric(); value=json.loads(self.metrics.read_text(encoding='utf-8'))
        self.assertEqual('PASS',value['gate_status']); self.assertEqual('native_normalized_report',value['source_contract'])
        self.assertEqual(hashlib.sha256(self.normalized.read_bytes()).hexdigest(),value['source_sha256'])
        schema=json.loads((ROOT/'schemas'/'metric-gate.schema.json').read_text(encoding='utf-8'))
        jsonschema.validate(value,schema)

    def test_legacy_or_cross_client_normalized_bundle_is_rejected(self):
        self.normalize(); original=json.loads(self.normalized.read_text(encoding='utf-8'))
        for case,mutate,client in (
            ('legacy',lambda value:value.update(schema_version='1.0'),CLIENT),
            ('cross-client',lambda value:None,'other-client')):
            with self.subTest(case=case):
                value=json.loads(json.dumps(original)); mutate(value)
                self.normalized.write_text(json.dumps(value),encoding='utf-8')
                self.metric(expected=2,client=client)
                self.assertFalse(self.metrics.exists())

    def test_output_cannot_overwrite_normalizer_or_metric_input(self):
        before=self.raw.read_bytes(); self.normalize(expected=2,output=self.raw); self.assertEqual(before,self.raw.read_bytes())
        self.normalize(); before=self.normalized.read_bytes(); self.metric(expected=2,output=self.normalized)
        self.assertEqual(before,self.normalized.read_bytes())

    def test_direct_csv_metric_input_is_scoped_and_native(self):
        direct=self.root/'direct.csv'
        direct.write_text('period,gmv,visitors,buyers,orders\n2026-09,100,10,2,2\n',encoding='utf-8')
        self.metric(input_path=direct); value=json.loads(self.metrics.read_text(encoding='utf-8'))
        self.assertEqual('direct_scoped_csv',value['source_contract'])
        self.assertEqual('omni-ecom.metric-gate',value['contract_name'])


if __name__=='__main__': unittest.main()
