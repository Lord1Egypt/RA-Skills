"""Synthetic chart/KPI consistency tests; no source or host authenticity claim."""
import copy
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import report_metric_guard as guard
import generate_pdf_report as pdf
import quality_gate_smoke as quality_fixture
import decision_pipeline_smoke as builder_fixture


class MetricTests(unittest.TestCase):
    def setUp(self):
        self.package=dict(scope={'platform':'tmall','store':'synthetic'},
            metrics=[dict(period='2026-06',inputs={'gmv':100}),dict(period='2026-07',inputs={'gmv':200})],
            adjudicated_claims={'X1':dict(metric='GMV',unit='元',period='2026-07',value=200,
                                         previous_period='2026-06',previous_value=100)})

    def test_matching_values_and_equivalent_months_pass_without_mutation(self):
        self.package['metrics'][1]['period']='202607'
        before=copy.deepcopy(self.package)
        self.assertEqual(2,len(guard.validate(self.package)))
        self.assertEqual(before,self.package)

    def test_old_kpi_value_cannot_survive_adjudication(self):
        self.package['metrics'][1]['inputs']['gmv']=999
        with self.assertRaisesRegex(ValueError,'adjudication_stale'):
            guard.validate(self.package)

    def test_previous_period_value_must_also_match(self):
        self.package['metrics'][0]['inputs']['gmv']=500
        with self.assertRaisesRegex(ValueError,'adjudication_stale'):
            guard.validate(self.package)

    def test_container_precedence_cannot_hide_a_contradictory_value(self):
        row=self.package['metrics'][1]
        row['metrics']={'gmv':999}
        with self.assertRaisesRegex(ValueError,'duplicate_conflict'):
            pdf.metric_value(row,'gmv')

    def test_equal_duplicates_are_not_a_false_conflict(self):
        row=self.package['metrics'][1]
        row['metrics']={'gmv':'200.00'}
        self.assertEqual(200,pdf.metric_value(row,'gmv'))

    def test_missing_is_not_zero_and_boolean_is_not_one(self):
        self.assertIsNone(pdf.metric_value({'inputs':{'gmv':None}},'gmv'))
        self.assertEqual(0,pdf.metric_value({'inputs':{'gmv':0}},'gmv'))
        with self.assertRaisesRegex(ValueError,'boolean_not_number'):
            pdf.metric_value({'inputs':{'gmv':True}},'gmv')

    def test_percentage_claim_is_compared_to_ratio_chart_value(self):
        package=dict(metrics=[dict(period='2026-07',metrics={'conversion_rate':.2})],
            adjudicated_claims={'X1':dict(metric='转化率',unit='%',value=20,period='2026-07')})
        self.assertEqual(1,len(guard.validate(package)))
        package['metrics'][0]['metrics']['conversion_rate']=20
        with self.assertRaisesRegex(ValueError,'adjudication_stale'):
            guard.validate(package)

    def test_ambiguous_current_label_is_not_assumed_to_mean_this_month(self):
        self.package['metrics'][1]['period']='本期'
        with self.assertRaisesRegex(ValueError,'period_unbound'):
            guard.validate(self.package)

    def test_unrecognized_unit_is_not_silently_converted(self):
        self.package['adjudicated_claims']['X1']['unit']='未知货币单位'
        with self.assertRaisesRegex(ValueError,'unit_unbound'):
            guard.validate(self.package)

    def test_old_claim_ledger_value_is_rejected(self):
        self.package['claim_ledger']={'claims':[dict(claim_id='C-gmv',metric='gmv',value=999,unit='元',period='2026-07')]}
        with self.assertRaisesRegex(ValueError,'ledger_adjudication_stale'):
            guard.validate(self.package)

    def test_explicit_other_store_row_cannot_be_treated_as_current_store(self):
        self.package['metrics'][1]['store']='another-store'
        with self.assertRaisesRegex(ValueError,'scope_mismatch'):
            guard.validate(self.package)

    def test_negative_and_fractional_counts_are_rejected(self):
        for value in (-1,.5):
            with self.subTest(value=value),self.assertRaisesRegex(ValueError,'count_invalid'):
                guard.validate({'metrics':[{'inputs':{'buyers':value}}]})

    def test_nonfinite_value_cannot_be_silently_omitted_from_chart(self):
        with self.assertRaisesRegex(ValueError,'number_invalid'):
            pdf.metric_value({'inputs':{'gmv':'NaN'}},'gmv')

    def test_advertising_cost_cannot_disagree_with_adjudication(self):
        package=dict(metrics=[dict(period='2026-07',inputs={'ad_spend':8131})],
            adjudicated_claims={'X1':dict(metric='推广花费',unit='元',value=0,period='2026-07')})
        with self.assertRaisesRegex(ValueError,'adjudication_stale'):
            guard.validate(package)

    def test_unsupported_metric_is_not_reported_as_checked(self):
        result=guard.validate({'adjudicated_claims':{'X1':dict(metric='自定义指标',value=1,period='2026-07')}})
        self.assertEqual('unmapped_not_checked',result[0]['status'])

    def test_quality_gate_checks_the_actual_chart_values(self):
        fixture=quality_fixture.QualityTests(); fixture.setUp()
        try:
            fixture.verdict_fixture()
            fixture.report['metrics']=[dict(period='2026-07',inputs={'gmv':200000})]
            quality_fixture.write(fixture.root/'report.json',fixture.report)
            with self.assertRaisesRegex(ValueError,'adjudication_stale'):
                quality_fixture.validate_quality(fixture.root,fixture.report)
        finally: fixture.tearDown()

    def test_standalone_pdf_cannot_bypass_metric_check(self):
        self.package['metrics'][1]['inputs']['gmv']=999
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory); source=root/'report.json'
            source.write_text(json.dumps(self.package),encoding='utf-8')
            with self.assertRaisesRegex(ValueError,'adjudication_stale'):
                pdf.generate(source,root/'report.pdf',root/'receipt.json',root/'pages')
            self.assertFalse((root/'report.pdf').exists())

    def test_actual_builder_stops_before_writing_stale_pdf(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            command=builder_fixture.prepare_builder_sample(root,'monthly_report')
            builder_fixture.write(root/'metrics.json',{'rows':[dict(period='2026-07',inputs={'gmv':999})]})
            result=subprocess.run(command+['--metrics',str(root/'metrics.json')],capture_output=True,text=True,
                                  encoding='utf-8',timeout=60)
            self.assertNotEqual(0,result.returncode)
            self.assertIn('adjudication_stale',result.stdout+result.stderr)
            self.assertFalse((root/'report.pdf').exists())


class ChartMissingTests(unittest.TestCase):
    def test_missing_previous_rate_is_not_plotted_as_zero(self):
        from matplotlib.axes import Axes
        values=[]; labels=[]; original=Axes.bar; original_ticks=Axes.set_xticks
        def bar(self,x,height,*args,**kwargs):
            values.extend(height); return original(self,x,height,*args,**kwargs)
        def ticks(self,positions,names=None,*args,**kwargs):
            if names is not None: labels.extend(names)
            return original_ticks(self,positions,names,*args,**kwargs)
        rows=[dict(metrics={'conversion_rate':None,'refund_rate_amount':.05}),
              dict(metrics={'conversion_rate':.2,'refund_rate_amount':.1})]
        with tempfile.TemporaryDirectory() as directory,patch.object(Axes,'bar',bar),patch.object(Axes,'set_xticks',ticks):
            pdf.chart_rates(rows,Path(directory)/'rates.png')
        self.assertEqual([5,20,10],values)
        self.assertTrue(any('对比期缺数' in label for label in labels))

    def test_actual_zero_previous_rate_is_retained(self):
        from matplotlib.axes import Axes
        values=[]; original=Axes.bar
        def bar(self,x,height,*args,**kwargs):
            values.extend(height); return original(self,x,height,*args,**kwargs)
        with tempfile.TemporaryDirectory() as directory,patch.object(Axes,'bar',bar):
            pdf.chart_rates([dict(metrics={'conversion_rate':0}),dict(metrics={'conversion_rate':.2})],Path(directory)/'rates.png')
        self.assertEqual([0,20],values)
        self.assertEqual('↑20.00个百分点',pdf.change(.2,0,'rate'))
        self.assertEqual('基期为0，不计算相对变化',pdf.change(100,0,'money'))

    def test_zero_count_uses_linear_axis_and_truthful_title(self):
        from matplotlib.axes import Axes
        scales=[]; titles=[]; original_scale=Axes.set_xscale; original_title=Axes.set_title
        def scale(self,value,*args,**kwargs):
            scales.append(value); return original_scale(self,value,*args,**kwargs)
        def title(self,value,*args,**kwargs):
            titles.append(value); return original_title(self,value,*args,**kwargs)
        with tempfile.TemporaryDirectory() as directory,patch.object(Axes,'set_xscale',scale),patch.object(Axes,'set_title',title):
            pdf.chart_traffic([dict(inputs={'visitors':1000,'buyers':0})],Path(directory)/'traffic.png')
        self.assertEqual('linear',scales[-1])
        self.assertIn('线性刻度',titles[-1])


if __name__=='__main__': unittest.main()
