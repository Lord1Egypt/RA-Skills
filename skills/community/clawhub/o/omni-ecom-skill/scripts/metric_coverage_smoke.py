"""Every displayed structured value needs a scoped ledger, all examples synthetic."""
import copy
import json
import os
import re
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import report_metric_guard as guard
import generate_pdf_report as pdf
from claim_guard import validate_claims
from claim_source_guard import validate_sources
from quality_gate import sha
import decision_pipeline_smoke as builder_fixture


def write(path,value): path.write_text(json.dumps(value,ensure_ascii=False),encoding='utf-8')


def grouped_fixture(root):
    """Real local synthetic cells for two isolated stores and two months."""
    source=root/'grouped-source.csv'
    source.write_text('月份,平台,金额\n2026-06,tmall,100\n2026-07,tmall,200\n2026-06,jd,400\n2026-07,jd,500\n',encoding='utf-8')
    claims=[]; rows=[]
    for index,(platform,month,value) in enumerate((('tmall','2026-06',100),('tmall','2026-07',200),
                                                  ('jd','2026-06',400),('jd','2026-07',500)),2):
        key=f'C-sales-{index}'
        claims.append(dict(claim_id=key,metric='gmv',unit='元',value=value,status='verified',period=month,
            platform=platform,store=platform+'-synthetic',source_ref=dict(source_id='synthetic',source_file=source.name,
            field='金额',range=f'C{index}',source_sha256=sha(source))))
        rows.append(dict(period=month,platform=platform,store=platform+'-synthetic',inputs={'gmv':value},metric_bindings={'gmv':key}))
    # Deliberately interleave both stores and put current before previous.
    package=dict(run_id='synthetic-grouped',client_scope='synthetic',period='2026-07',team_version='2.0.3',report_revision='R1',
        title='多平台分组与来源合成测试',gate_status='WARN',metrics=[rows[1],rows[3],rows[0],rows[2]],
        scope=dict(platform='cross_platform',store='synthetic-group',members=[dict(platform=p,store=p+'-synthetic') for p in ('tmall','jd')]),
        expert_participation=[dict(agent_id='data-analyst',display_name='合成测试岗',profession='数据检查',
                                  participation_status='synthetic_fixture',agent_task_ids=[],contribution_summary='合成渲染测试，非真实专家返回')])
    ledger=dict(**__import__('artifact_contract').native_claim_identity(package['team_version']),run_id=package['run_id'],client_scope='synthetic',period='2026-07',
                additional_periods=['2026-06'],claims=claims)
    errors,counts=validate_claims(ledger)
    if errors: raise ValueError(str(errors))
    write(root/'claims.json',ledger)
    package['claim_ledger']=dict(file='claims.json',sha256=sha(root/'claims.json'),claims=claims,**counts,source_checks=validate_sources(ledger,root))
    write(root/'report.json',package)
    (root/'report.md').write_text('合成分组检查；'+','.join(c['claim_id'] for c in claims),encoding='utf-8')
    return package


class CoverageTests(unittest.TestCase):
    def setUp(self):
        self.claim=dict(claim_id='C-gmv',metric='gmv',value=100,unit='元',period='2026-07',status='verified')
        self.row=dict(period='2026-07',inputs={'gmv':100})
        self.package=dict(client_scope='synthetic',scope={'platform':'tmall','store':'synthetic'},
                          metrics=[self.row],claim_ledger={'claims':[self.claim]})

    def validate(self): return guard.validate_delivery_metrics(self.package)

    def test_no_adjudication_still_requires_claim(self):
        self.row['inputs']['ad_spend']=8131
        with self.assertRaisesRegex(ValueError,'claim_missing_or_ambiguous:ad_spend'): self.validate()

    def test_matching_values_do_not_change_inputs(self):
        before=copy.deepcopy(self.package)
        self.assertEqual(self.validate()[0]['claim_id'],'C-gmv')
        self.assertEqual(self.package,before)

    def test_unadjudicated_value_mismatch(self):
        self.row['inputs']['gmv']=8131
        with self.assertRaisesRegex(ValueError,'ledger_value_mismatch'): self.validate()

    def test_unknown_is_not_zero(self):
        self.claim.update(status='unknown',value=None); self.row['inputs']['gmv']=0
        with self.assertRaisesRegex(ValueError,'claim_not_known'): self.validate()
        self.row['inputs']['gmv']=None
        self.assertEqual(self.validate()[0]['status'],'missing_not_plotted')

    def test_actual_zero_needs_and_accepts_known_zero(self):
        self.claim['value']=0; self.row['inputs']['gmv']=0
        self.assertEqual(self.validate()[0]['status'],'ledger_value_matched')

    def test_wrong_period_cannot_supply_same_number(self):
        self.claim['period']='2026-06'
        with self.assertRaisesRegex(ValueError,'claim_missing_or_ambiguous'): self.validate()

    def test_ambiguous_sources_need_explicit_selection(self):
        other=copy.deepcopy(self.claim); other['claim_id']='C-other'
        self.package['claim_ledger']['claims'].append(other)
        with self.assertRaisesRegex(ValueError,'claim_missing_or_ambiguous'): self.validate()
        self.row['metric_bindings']={'gmv':'C-gmv'}
        self.assertEqual(self.validate()[0]['claim_id'],'C-gmv')

    def test_explicit_binding_cannot_change_metric_identity(self):
        self.claim['metric']='ad_spend'; self.row['metric_bindings']={'gmv':'C-gmv'}
        with self.assertRaisesRegex(ValueError,'claim_identity_mismatch'): self.validate()

    def test_percent_claim_matches_only_ratio_renderer_values(self):
        self.claim.update(metric='conversion_rate',value=20,unit='%'); self.row['inputs']={'conversion_rate':.2}
        self.validate()
        self.row['inputs']['conversion_rate']=20
        self.row['metric_units']={'conversion_rate':'%'}
        with self.assertRaisesRegex(ValueError,'renderer_unit_mismatch'): self.validate()

    def test_custom_metric_requires_matching_unit(self):
        self.claim.update(metric='new_customers',value=100,unit='人'); self.row['inputs']={'new_customers':100}
        with self.assertRaisesRegex(ValueError,'custom_unit_required'): self.validate()
        self.row['metric_units']={'new_customers':'人'}; self.validate()

    def test_top_level_custom_value_is_not_ignored(self):
        del self.row['inputs']; self.row['custom_budget']=8131
        with self.assertRaisesRegex(ValueError,'claim_missing_or_ambiguous:custom_budget'): self.validate()

    def test_net_sales_reference_is_covered(self):
        self.row['inputs']['net_gmv_reference']=99
        with self.assertRaisesRegex(ValueError,'claim_missing_or_ambiguous:net_gmv_reference'): self.validate()

    def test_channel_cannot_borrow_store_total(self):
        self.row['dimensions']={'channel':'search'}
        with self.assertRaisesRegex(ValueError,'claim_missing_or_ambiguous'): self.validate()
        self.claim['dimensions']={'channel':'search'}; self.validate()

    def test_undeclared_store_is_rejected(self):
        self.row['store']='other'; self.claim['store']='other'
        with self.assertRaisesRegex(ValueError,'scope_mismatch'): self.validate()

    def test_declared_store_pair_is_not_a_cartesian_allowlist(self):
        self.package['scope']['members']=[dict(platform='jd',store='other')]
        self.row.update(platform='tmall',store='other'); self.claim.update(platform='tmall',store='other')
        with self.assertRaisesRegex(ValueError,'scope_mismatch'): self.validate()

    def test_overlapping_periods_cannot_be_compared(self):
        self.package['metrics'].append(dict(period='2026',inputs={'gmv':100}))
        with self.assertRaisesRegex(ValueError,'period_overlap'): self.validate()

    def test_duplicate_period_rows_are_not_previous_current(self):
        self.package['metrics'].append(copy.deepcopy(self.row))
        with self.assertRaisesRegex(ValueError,'duplicate_period'): self.validate()

    def test_weeks_quarters_and_explicit_ranges_have_real_order(self):
        self.assertLess(guard.period_key('2026-W01'),guard.period_key('2026-W02'))
        self.assertLess(guard.period_key('2026-Q1'),guard.period_key('2026-Q2'))
        self.assertEqual(guard.period_key('2026-07-01 至 2026-07-31'),guard.period_key('2026-07'))

    def test_alias_counts_cannot_be_negative(self):
        self.row['inputs']={'paid_buyers':-1}; self.claim.update(metric='buyers',value=-1,unit='人')
        with self.assertRaisesRegex(ValueError,'count_invalid'): self.validate()


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)

    def test_additional_periods_are_explicit_and_inputs_cannot_mix(self):
        package=grouped_fixture(self.root)
        ledger=json.loads((self.root/'claims.json').read_text(encoding='utf-8'))
        self.assertEqual(validate_claims(ledger)[0],[])
        del ledger['additional_periods']
        self.assertTrue(any('period_mismatch' in error for error in validate_claims(ledger)[0]))
        ledger['additional_periods']=['2026-06']
        derived=copy.deepcopy(ledger['claims'][1]); derived.update(claim_id='C-derived',status='derived',
            inputs=['C-sales-2','C-sales-3'],formula=dict(name='ratio',numerator='a',denominator='b',expression='a / b'))
        ledger['claims'].append(derived)
        self.assertTrue(any('derived_input_period_mismatch' in error for error in validate_claims(ledger)[0]))

    def test_grouped_chart_inputs_never_mix_store_or_reverse_dates(self):
        package=grouped_fixture(self.root); before=copy.deepcopy(package)
        guard.validate_delivery_metrics(package)
        captured=[]
        original=pdf.chart_sales
        def capture(rows,out):
            captured.append([(row['platform'],row['period'],row['inputs']['gmv']) for row in rows])
            return original(rows,out)
        with patch.object(pdf,'chart_sales',side_effect=capture): pdf.render_charts(package,self.root/'charts')
        self.assertEqual(captured,[[('tmall','2026-06',100),('tmall','2026-07',200)],
                                   [('jd','2026-06',400),('jd','2026-07',500)]])
        self.assertEqual(before,package)

    def test_data_gate_counts_periods_and_actual_sources_not_rows_or_metadata(self):
        from matplotlib.axes import Axes
        package=grouped_fixture(self.root)
        package['sources']=[{'type':'team_version','source':'version-info.json'}]*7
        observed=[]; original=Axes.bar
        def capture(self,x,height,*args,**kwargs):
            observed.append(list(height)); return original(self,x,height,*args,**kwargs)
        with patch.object(Axes,'bar',capture): pdf.chart_data_gate(package,self.root/'gate.png')
        self.assertEqual(observed,[[2,1,0,0]])

    def test_actual_pdf_has_separate_scoped_tables_and_source_checks(self):
        import pymupdf as fitz
        package=grouped_fixture(self.root)
        result=pdf.generate(self.root/'report.json',self.root/'report.pdf',self.root/'pdf-delivery.json',self.root/'pages')
        with fitz.open(self.root/'report.pdf') as document:
            text=''.join(page.get_text() for page in document).replace(' ','').replace('\n','')
            for page in document:
                captions=re.findall(r'图\d+',page.get_text())
                self.assertEqual(len(captions),len(page.get_image_info()),'图与图注不能跨页分离')
                page_text=page.get_text().replace(' ','').replace('\n','')
                indices=list(re.finditer(r'C-sales-\d+',page_text))
                for index,match in enumerate(indices):
                    end=indices[index+1].start() if index+1<len(indices) else len(page_text)
                    claim=next(c for c in package['claim_ledger']['claims'] if c['claim_id']==match.group())
                    self.assertIn('期间：'+claim['period'],page_text[match.end():end],'短来源条目不能跨页丢开期间')
        for expected in ('tmall-synthetic','jd-synthetic','100.00%','25.00%','C-sales-2','C-sales-5'):
            self.assertIn(expected,text)
        self.assertEqual(result['blank_pages'],[])
        self.assertEqual(result['claim_source_gate']['claims_count'],4)

    def test_actual_builder_rejects_unindexed_cost(self):
        command=builder_fixture.prepare_builder_sample(self.root,'monthly_report')
        write(self.root/'metrics.json',dict(rows=[dict(period='2026-07',inputs={'ad_spend':8131})]))
        result=subprocess.run(command+['--metrics',str(self.root/'metrics.json')],capture_output=True,text=True,encoding='utf-8',
                              env={**os.environ,'PYTHONIOENCODING':'utf-8'})
        self.assertNotEqual(result.returncode,0)
        self.assertIn('claim_missing_or_ambiguous:ad_spend',result.stdout+result.stderr)
        self.assertFalse((self.root/'report.pdf').exists())

    def test_standalone_pdf_rejects_unindexed_cost(self):
        package=grouped_fixture(self.root); package['metrics'][0]['inputs']['ad_spend']=8131
        write(self.root/'report.json',package)
        with self.assertRaisesRegex(ValueError,'claim_missing_or_ambiguous:ad_spend'):
            pdf.generate(self.root/'report.json',self.root/'report.pdf',self.root/'receipt.json',self.root/'pages')

    def test_quality_gate_rejects_unindexed_cost_without_conflict(self):
        import quality_gate_smoke as fixture
        from quality_gate import validate_quality
        fx=fixture.QualityTests(); fx.setUp()
        try:
            fx.report['metrics']=[dict(period=fx.report['period'],inputs={'ad_spend':8131})]
            write(fx.root/'report.json',fx.report)
            with self.assertRaisesRegex(ValueError,'claim_missing_or_ambiguous:ad_spend'):
                validate_quality(fx.root,fx.report)
        finally: fx.tearDown()


if __name__=='__main__': unittest.main()
