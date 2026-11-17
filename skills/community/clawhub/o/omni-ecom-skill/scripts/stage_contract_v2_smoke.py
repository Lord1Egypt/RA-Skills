#!/usr/bin/env python3
"""Synthetic contract checks for native 2.0 intake, planning and coverage artifacts."""
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import jsonschema

from coverage_guard_smoke import make_inventory,rep

ROOT=Path(__file__).resolve().parents[1]
TRIAGE=Path(__file__).with_name('report_triage.py')
CLUSTER=Path(__file__).with_name('cluster_reports.py')
COVERAGE=Path(__file__).with_name('coverage_guard.py')


class StageContractV2Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.root=Path(self.tmp.name)
        self.inventory=self.root/'inventory.json'
        self.inventory.write_text(json.dumps(make_inventory([
            rep('R001','交易.csv','trade_sales','transaction','analyzable')
        ]),ensure_ascii=False),encoding='utf-8')

    def tearDown(self): self.tmp.cleanup()

    def run_cluster(self,expected=0):
        clusters=self.root/'clusters.json'; plan=self.root/'plan.json'
        result=subprocess.run([sys.executable,str(CLUSTER),'--inventory',str(self.inventory),
            '--output-clusters',str(clusters),'--output-chapter-plan',str(plan)],
            capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(expected,result.returncode,result.stdout+result.stderr)
        return clusters,plan

    def test_triage_writes_native_v2_inventory(self):
        source=self.root/'inputs'; source.mkdir()
        (source/'交易.csv').write_text('日期,支付金额,支付买家数\n2026-09-01,100,2\n',encoding='utf-8-sig')
        output=self.root/'triage.json'
        result=subprocess.run([sys.executable,str(TRIAGE),'--input-root',str(source),'--output',str(output),
            '--run-id','stage-contract-run','--client-scope','synthetic','--team-version','2.0.3-candidate.1'],
            capture_output=True,text=True,encoding='utf-8')
        self.assertIn(result.returncode,(0,3),result.stdout+result.stderr)
        value=json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual('omni-ecom.report-inventory',value['contract_name'])
        schema=json.loads((ROOT/'schemas'/'report-inventory.schema.json').read_text(encoding='utf-8'))
        jsonschema.validate(value,schema)

    def test_cluster_and_plan_are_native_v2_and_schema_valid(self):
        clusters,plan=self.run_cluster()
        for path,schema_name,contract in ((clusters,'report-cluster.schema.json','omni-ecom.report-clusters'),
                                           (plan,'chapter-plan.schema.json','omni-ecom.chapter-plan')):
            value=json.loads(path.read_text(encoding='utf-8'))
            self.assertEqual(contract,value['contract_name'])
            schema=json.loads((ROOT/'schemas'/schema_name).read_text(encoding='utf-8'))
            jsonschema.validate(value,schema)

    def test_coverage_receipt_binds_both_inputs(self):
        _,plan=self.run_cluster(); output=self.root/'coverage.json'
        result=subprocess.run([sys.executable,str(COVERAGE),'--inventory',str(self.inventory),
            '--chapter-plan',str(plan),'--output',str(output)],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(0,result.returncode,result.stdout+result.stderr)
        value=json.loads(output.read_text(encoding='utf-8'))
        self.assertEqual(hashlib.sha256(self.inventory.read_bytes()).hexdigest(),value['inventory_sha256_ref'])
        self.assertEqual(hashlib.sha256(plan.read_bytes()).hexdigest(),value['chapter_plan_sha256_ref'])
        schema=json.loads((ROOT/'schemas'/'coverage-guard.schema.json').read_text(encoding='utf-8'))
        jsonschema.validate(value,schema)

    def test_legacy_inventory_cannot_generate_current_plan(self):
        value=json.loads(self.inventory.read_text(encoding='utf-8')); value['schema_version']='1.0.0'
        self.inventory.write_text(json.dumps(value),encoding='utf-8')
        clusters,plan=self.run_cluster(expected=1)
        self.assertFalse(clusters.exists()); self.assertFalse(plan.exists())


if __name__=='__main__': unittest.main()
