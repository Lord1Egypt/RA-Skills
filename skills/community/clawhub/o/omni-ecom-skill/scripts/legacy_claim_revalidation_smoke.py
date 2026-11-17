"""Synthetic tests for explicit v1 claim revalidation against real copied exports."""
import hashlib
import json
import tempfile
import unittest
from pathlib import Path

import legacy_migration
from legacy_claim_revalidation import prepare


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding='utf-8')


class RevalidationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name); self.source=self.root/'legacy'; self.source.mkdir()
        self.evidence=self.root/'evidence'; self.evidence.mkdir(); self.output=self.root/'prepared'
        self.scope='synthetic-client'; self.store='示例店铺'; self.run='run-v2'
        csv=self.evidence/'legacy.csv'
        csv.write_text('期间,平台,店铺,单位,GMV\n2026-07,tmall,示例店铺,元,100\n',encoding='utf-8')
        digest=hashlib.sha256(csv.read_bytes()).hexdigest()
        claim=dict(schema_version='1.0',run_id='legacy-run',client_scope=self.scope,period='2026-07',
            scope=dict(platform='tmall',store=self.store),
            claims=[dict(claim_id='C-gmv',metric='gmv',value=100,unit='元',period='2026-07',status='verified',
                source_ref=dict(source_id='legacy-export',source_file='legacy.csv',field='GMV',range='E2',
                    source_sha256=digest))])
        write(self.source/'claims.json',claim)
        plan=dict(client_scope=self.scope,files=[dict(kind='claim',file='claims.json')])
        self.migration=self.root/'migration'
        receipt,self.receipt_sha=legacy_migration.migrate(self.source,plan,self.migration,self.scope,[self.store])
        self.record_id=receipt['records'][0]['record_id']
        self.context=self.root/'scope-context.json'
        self.context_value=dict(client_scope=self.scope,scope=dict(platform='tmall',store=self.store),
            scope_attestation=dict(status='operator_attested_not_platform_authenticated',
                authority_reference='user-confirmed-upload-scope',attested_at='2026-09-08T00:00:00Z'),
            claims={'C-gmv':{
                'period':{'column':'A','field':'期间'},'unit':{'column':'D','field':'单位'},
                'platform':{'column':'B','field':'平台'},'store':{'column':'C','field':'店铺'}}})
        write(self.context,self.context_value)

    def run_prepare(self):
        return prepare(self.migration,self.receipt_sha,self.scope,self.record_id,self.evidence,
                       self.context,self.output,self.run,'2.0.3-candidate.1')

    def test_real_legacy_source_is_copied_recomputed_and_context_checked(self):
        result=self.run_prepare()
        self.assertEqual(result['status'],'source_recomputed_scope_labels_checked_requires_current_report_binding')
        self.assertFalse(result['platform_authenticity_verified'])
        self.assertFalse(result['formal_delivery_completed'])
        ledger=json.loads((self.output/'claim-ledger.json').read_text(encoding='utf-8'))
        self.assertEqual(ledger['contract_name'],'omni-ecom.claim-ledger')
        self.assertEqual(ledger['source_context_policy'],'required')
        self.assertEqual(result['source_checks'][0]['source_context']['status'],'source_context_verified')
        self.assertTrue((self.output/result['source_inputs'][0]['copied_file']).is_file())

    def test_wrong_external_scope_label_blocks_without_output(self):
        self.context_value['scope']['store']='另一个店铺'; write(self.context,self.context_value)
        with self.assertRaisesRegex(ValueError,'source_context_value_mismatch:store'): self.run_prepare()
        self.assertFalse(self.output.exists())

    def test_source_hash_change_blocks_without_output(self):
        (self.evidence/'legacy.csv').write_text('tampered',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'source_hash_mismatch'): self.run_prepare()
        self.assertFalse(self.output.exists())

    def test_scope_attestation_cannot_claim_platform_authentication(self):
        self.context_value['scope_attestation']['status']='platform_authenticated'; write(self.context,self.context_value)
        with self.assertRaisesRegex(ValueError,'scope_attestation_invalid'): self.run_prepare()
        self.assertFalse(self.output.exists())

    def test_context_claim_set_must_match_verified_claims(self):
        self.context_value['claims']['C-other']=self.context_value['claims']['C-gmv']; write(self.context,self.context_value)
        with self.assertRaisesRegex(ValueError,'context_claim_set_mismatch'): self.run_prepare()
        self.assertFalse(self.output.exists())


if __name__=='__main__': unittest.main()
