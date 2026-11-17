"""Standalone PDF source checks and actual rendered index, all synthetic."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import generate_pdf_report as pdf
from claim_guard import validate_claims
from claim_source_guard import validate_sources,validate_pdf_source_binding
from quality_gate import sha,read


def write(path,value):
    path.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')


def attach_synthetic_sources(root,package,count=1):
    """Renderer fixture values, never native client evidence."""
    source=root/'pdf-source.csv'
    source.write_text('合成金额\n100\n',encoding='utf-8')
    claims=[dict(claim_id=f'C-pdf-{index}',metric='synthetic_probe',unit='元',value=100,
        status='verified',period=package['period'],source_ref=dict(source_id='synthetic',source_file=source.name,
        field='合成金额',range='A2',sheet='csv-metadata-not-a-sheet',source_sha256=sha(source))) for index in range(count)]
    payload=dict(**__import__('artifact_contract').native_claim_identity(package['team_version']),run_id=package['run_id'],client_scope=package['client_scope'],period=package['period'],claims=claims)
    write(root/'claims.json',payload)
    errors,counts=validate_claims(payload)
    if errors: raise ValueError(str(errors))
    package['claim_ledger']=dict(file='claims.json',sha256=sha(root/'claims.json'),claims=claims,**counts,
                               source_checks=validate_sources(payload,root))
    (root/'report.md').write_text('合成渲染测试；'+','.join(row['claim_id'] for row in claims),encoding='utf-8')


class PdfSourceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.package=dict(run_id='synthetic-pdf-source',client_scope='synthetic',team_version='2.0.3',report_revision='R1',
            title='候选数字来源合成测试',gate_status='WARN',period='2026-07',
            expert_participation=[dict(agent_id='data-analyst',display_name='合成测试岗',profession='数据测试',
                                      participation_status='synthetic_fixture',agent_task_ids=[],contribution_summary='仅合成测试')])
        attach_synthetic_sources(self.root,self.package)
        self.save()

    def save(self): write(self.root/'report.json',self.package)

    def render(self):
        return pdf.generate(self.root/'report.json',self.root/'report.pdf',self.root/'pdf-delivery.json',self.root/'pages')

    def test_standalone_rejects_no_ledger(self):
        del self.package['claim_ledger']; self.save()
        with self.assertRaisesRegex(ValueError,'ledger_missing'): self.render()
        self.assertFalse((self.root/'report.pdf').exists())

    def test_standalone_rejects_missing_source(self):
        (self.root/'pdf-source.csv').unlink()
        with self.assertRaisesRegex(ValueError,'outside_or_missing'): self.render()
        self.assertFalse((self.root/'report.pdf').exists())

    def test_standalone_rejects_fabricated_index(self):
        self.package['claim_ledger']['claims'][0]['value']=8131; self.save()
        with self.assertRaisesRegex(ValueError,'projection_mismatch'): self.render()

    def test_no_output_may_overwrite_raw_inputs(self):
        path=self.root/'pdf-source.csv'; original=path.read_bytes()
        with self.assertRaisesRegex(ValueError,'overlaps_inputs'):
            pdf.generate(self.root/'report.json',path,self.root/'pdf-delivery.json',self.root/'pages')
        self.assertEqual(path.read_bytes(),original)

    def test_render_folder_cannot_contain_raw_inputs(self):
        with self.assertRaisesRegex(ValueError,'overlaps_inputs'):
            pdf.generate(self.root/'report.json',self.root/'report.pdf',self.root/'pdf-delivery.json',self.root)

    def test_render_failure_preserves_existing_pdf_and_receipt(self):
        output=self.root/'report.pdf'; receipt=self.root/'pdf-delivery.json'
        output.write_bytes(b'previous delivery placeholder'); receipt.write_text('previous receipt',encoding='utf-8')
        with patch.object(pdf,'inspect_pdf',side_effect=ValueError('synthetic_render_failure')):
            with self.assertRaisesRegex(ValueError,'synthetic_render_failure'): self.render()
        self.assertEqual(output.read_bytes(),b'previous delivery placeholder')
        self.assertEqual(receipt.read_text(encoding='utf-8'),'previous receipt')

    def test_input_change_during_render_does_not_publish(self):
        original=pdf.render_charts
        def mutate(*args):
            charts=original(*args)
            (self.root/'pdf-source.csv').write_text('合成金额\n8131\n',encoding='utf-8')
            return charts
        with patch.object(pdf,'render_charts',side_effect=mutate):
            with self.assertRaisesRegex(ValueError,'inputs_changed_during_render'): self.render()
        self.assertFalse((self.root/'report.pdf').exists())
        self.assertFalse((self.root/'pdf-delivery.json').exists())

    def test_rendered_pdf_lists_every_claim_and_correct_stage(self):
        import pymupdf as fitz
        attach_synthetic_sources(self.root,self.package,count=20); self.save()
        receipt=self.render()
        with fitz.open(self.root/'report.pdf') as document:
            text=''.join(page.get_text() for page in document).replace(' ','').replace('\n','')
        for row in self.package['claim_ledger']['claims']:
            self.assertIn(row['claim_id'],text)
        self.assertIn('数字来源与复算索引',text)
        self.assertIn('pdf-source.csv',text)
        self.assertIn('原表复算',text)
        self.assertIn('单格取值',text)
        self.assertNotIn('csv-metadata-not-a-sheet',text)
        self.assertIn('待冻结和独立复核',text)
        self.assertNotIn('已冻结',text)
        self.assertEqual(receipt['claim_source_gate']['claims_count'],20)
        self.assertEqual(receipt['blank_pages'],[])
        validate_pdf_source_binding(receipt,self.root,self.package)

    def test_pdf_receipt_missing_or_stale_source_binding(self):
        receipt=self.render()
        stale=copy.deepcopy(receipt); del stale['input_fingerprints']
        with self.assertRaisesRegex(ValueError,'fingerprints_missing_or_stale'):
            validate_pdf_source_binding(stale,self.root,self.package)
        stale=copy.deepcopy(receipt); stale['claim_source_gate']['claims_count']=500
        with self.assertRaisesRegex(ValueError,'claim_source_gate_stale'):
            validate_pdf_source_binding(stale,self.root,self.package)
        (self.root/'report.md').write_text('C-pdf-0 changed report',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'fingerprints_missing_or_stale'):
            validate_pdf_source_binding(receipt,self.root,self.package)

    def test_unknown_display_remains_unknown(self):
        import pymupdf as fitz
        path=self.root/'claims.json'; payload=read(path)
        payload['claims'][0].update(value=None,status='unknown',missing_reason='未上传真实投放表')
        write(path,payload)
        errors,counts=validate_claims(payload); self.assertEqual(errors,[])
        self.package['claim_ledger'].update(sha256=sha(path),claims=payload['claims'],**counts,
                                           source_checks=validate_sources(payload,self.root))
        self.save(); self.render()
        with fitz.open(self.root/'report.pdf') as document:
            text=''.join(page.get_text() for page in document).replace(' ','').replace('\n','')
        self.assertIn('未知',text); self.assertIn('缺数，未复算',text)
        self.assertIn('未上传真实投放表',text)


if __name__=='__main__': unittest.main()
