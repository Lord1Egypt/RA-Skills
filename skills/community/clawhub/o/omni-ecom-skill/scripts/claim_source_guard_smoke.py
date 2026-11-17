"""Actual local synthetic sources; no platform authenticity claims."""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from claim_guard import validate_claims
from claim_source_guard import validate_sources
import decision_pipeline_smoke as pipeline


class SourceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.file=self.root/'source.csv'
        self.file.write_text('花费,归因金额\n100,1000\n',encoding='utf-8')
        def claim(key,metric,value,col,field):
            return dict(claim_id=key,metric=metric,value=value,unit='元',status='verified',period='2026-07',
                source_ref=dict(source_file='source.csv',source_id='synthetic',field=field,range=col+'2',
                                source_sha256=hashlib.sha256(self.file.read_bytes()).hexdigest()))
        self.spend=claim('C-spend','ad_spend',100,'A','花费')
        self.gmv=claim('C-gmv','attributed_gmv',1000,'B','归因金额')
        self.roas=dict(claim_id='C-roas',metric='roas',value=10,unit='倍',period='2026-07',status='derived',
            source_ref=copy.deepcopy(self.gmv['source_ref']),inputs=['C-gmv','C-spend'],
            formula=dict(name='roas',numerator='attributed_gmv',denominator='ad_spend',expression='attributed_gmv / ad_spend'),
            attribution=dict(source_id='synthetic',window='2026-07',level='campaign',
                acquisition_mode='manual_platform_export',export_reference='SYNTHETIC-EXPORT-1',
                exported_at='2026-08-01T00:00:00Z',client_scope='synthetic',platform='tmall',
                authenticity_status='source_bound_export_not_platform_authenticated',
                metric_semantics_version='2.0'))
        self.data=dict(**__import__('artifact_contract').native_claim_identity('2.0.3'),run_id='synthetic',client_scope='synthetic',period='2026-07',
                       claims=[self.roas,self.spend,self.gmv])

    def check(self):
        errors,_=validate_claims(self.data)
        self.assertEqual(errors,[])
        return validate_sources(self.data,self.root)

    def test_real_cells_and_forward_references(self):
        self.assertEqual(self.check()[-1]['value'],'10')

    def net_fixture(self):
        attribution=dict(source_id='synthetic',window='7-day-click',level='campaign',
                         refund_basis='matched_attributed_sales',
                         acquisition_mode='manual_platform_export',export_reference='SYNTHETIC-EXPORT-1',
                         exported_at='2026-08-01T00:00:00Z',client_scope='synthetic',platform='tmall',
                         authenticity_status='source_bound_export_not_platform_authenticated',
                         metric_semantics_version='2.0')
        path=self.root/'refund.csv'; path.write_text('归因退款\n200\n',encoding='utf-8')
        refund=dict(claim_id='C-refund',metric='attributed_refund',value=200,unit='元',period='2026-07',
            status='verified',source_ref=dict(source_id='synthetic',source_file=path.name,field='归因退款',
                range='A2',source_sha256=hashlib.sha256(path.read_bytes()).hexdigest()))
        net=dict(claim_id='C-net-sales',metric='attributed_net_sales',value=800,unit='元',period='2026-07',
            status='derived',source_ref=copy.deepcopy(self.gmv['source_ref']),inputs=['C-gmv','C-refund'],
            formula=dict(name='attributed_net_sales',numerator='attributed_gmv',denominator='attributed_refund',
                         expression='attributed_gmv - attributed_refund'))
        self.roas.update(metric='net_roas',value=8,inputs=['C-net-sales','C-spend'],
            formula=dict(name='net_roas',numerator='attributed_net_sales',denominator='ad_spend',
                         expression='attributed_net_sales / ad_spend'))
        self.data['claims'].extend([refund,net])
        for row in self.data['claims']: row['attribution']=copy.deepcopy(attribution)
        return refund,net

    def test_net_roas_recomputes_refund_and_never_certifies_profit(self):
        self.net_fixture()
        checks=self.check()
        result=next(r for r in checks if r['claim_id']=='C-roas')
        self.assertEqual(result['value'],'8')
        self.assertIs(result['net_return']['profit_checked'],False)
        self.assertEqual(len(checks),5)

    def test_net_roas_missing_refund_is_not_zero(self):
        refund,_=self.net_fixture(); refund.update(status='unknown',value=None)
        with self.assertRaisesRegex(ValueError,'unknown_input'): self.check()

    def test_net_roas_refund_must_match_attributed_sales(self):
        refund,_=self.net_fixture(); refund['metric']='refund_amount'
        self.assertIn('net_return_input_metric_mismatch',';'.join(validate_claims(self.data)[0]))

    def test_net_roas_rejects_mismatched_attribution(self):
        refund,_=self.net_fixture(); refund['attribution']['window']='30-day-click'
        self.assertIn('net_return_attribution_mismatch',';'.join(validate_claims(self.data)[0]))

    def test_net_roas_requires_explicit_refund_basis(self):
        self.net_fixture()
        for row in self.data['claims']: row['attribution']['refund_basis']='current_period_all_refunds'
        self.assertIn('net_return_refund_basis_mismatch',';'.join(validate_claims(self.data)[0]))

    def test_roas_requires_source_bound_acquisition_metadata(self):
        self.roas['attribution'].pop('export_reference')
        self.assertIn('acquisition_metadata_missing:export_reference',';'.join(validate_claims(self.data)[0]))

    def test_roas_cannot_claim_platform_authentication_from_manual_export(self):
        self.roas['attribution']['authenticity_status']='platform_authenticated'
        self.assertIn('acquisition_authenticity_overclaim',';'.join(validate_claims(self.data)[0]))

    def test_roas_acquisition_must_match_client_scope(self):
        self.roas['attribution']['client_scope']='other-client'
        self.assertIn('acquisition_client_scope_mismatch',';'.join(validate_claims(self.data)[0]))

    def test_net_roas_rejects_other_store_cost(self):
        self.net_fixture(); self.spend['store']='other'
        with self.assertRaisesRegex(ValueError,'net_return_scope_mismatch'): self.check()

    def test_net_roas_cannot_use_verified_net_sales_without_deduction(self):
        _,net=self.net_fixture(); net['status']='verified'
        self.assertIn('net_return_requires_derivation',';'.join(validate_claims(self.data)[0]))

    def test_net_roas_subtraction_cannot_be_forged(self):
        _,net=self.net_fixture()
        net['formula']['expression']='attributed_gmv * 0 + attributed_refund * 0 + 800'
        with self.assertRaisesRegex(ValueError,'net_return_expression_mismatch'): self.check()

    def test_net_roas_refund_cannot_exceed_matched_sales(self):
        refund,net=self.net_fixture()
        path=self.root/'refund.csv'; path.write_text('归因退款\n1200\n',encoding='utf-8')
        refund.update(value=1200); refund['source_ref']['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        net['value']=-200; self.roas['value']=-2
        with self.assertRaisesRegex(ValueError,'net_return_refund_out_of_range'): self.check()

    def test_net_roas_real_zero_refund_is_allowed(self):
        refund,net=self.net_fixture()
        path=self.root/'refund.csv'; path.write_text('归因退款\n0\n',encoding='utf-8')
        refund.update(value=0); refund['source_ref']['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        net['value']=1000; self.roas['value']=10
        self.check()

    def contribution_fixture(self):
        self.net_fixture()
        attribution=copy.deepcopy(self.roas['attribution'])
        attribution.update(cost_basis='matched_attributed_sales',reconciliation_id='MATCH-SYNTHETIC-1')
        for row in self.data['claims']:
            row['attribution']=copy.deepcopy(attribution)
        path=self.root/'variable-costs.csv'
        path.write_text('优惠,商品成本,平台费用,履约成本\n50,300,20,30\n',encoding='utf-8')
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        definitions=[('C-discount','attributed_discount',50,'A','优惠'),
                     ('C-attributed-product','attributed_product_cost',300,'B','商品成本'),
                     ('C-attributed-platform','attributed_platform_fee',20,'C','平台费用'),
                     ('C-attributed-fulfillment','attributed_fulfillment_cost',30,'D','履约成本')]
        costs=[]
        for key,metric,value,column,field in definitions:
            costs.append(dict(claim_id=key,metric=metric,value=value,unit='元',period='2026-07',status='verified',
                source_ref=dict(source_file=path.name,source_id='synthetic',field=field,range=column+'2',
                                source_sha256=digest),attribution=copy.deepcopy(attribution)))
        contribution=dict(claim_id='C-contribution',metric='attributed_contribution_before_ad',value=400,
            unit='元',period='2026-07',status='derived',source_ref=copy.deepcopy(self.gmv['source_ref']),
            inputs=['C-net-sales',*[row['claim_id'] for row in costs]],attribution=copy.deepcopy(attribution),
            formula=dict(name='attributed_contribution_before_ad',numerator='attributed_net_sales',
                denominator='attributed_fulfillment_cost',
                expression='attributed_net_sales - attributed_discount - attributed_product_cost - attributed_platform_fee - attributed_fulfillment_cost'))
        contribution_roas=dict(claim_id='C-contribution-roas',metric='contribution_roas',value=4,unit='倍',
            period='2026-07',status='derived',source_ref=copy.deepcopy(self.gmv['source_ref']),
            inputs=['C-contribution','C-spend'],attribution=copy.deepcopy(attribution),
            formula=dict(name='contribution_roas',numerator='attributed_contribution_before_ad',
                denominator='ad_spend',expression='attributed_contribution_before_ad / ad_spend'))
        self.data['claims'].extend([*costs,contribution,contribution_roas])
        return costs,contribution,contribution_roas

    def test_contribution_roas_recomputes_matched_variable_costs_without_profit_claim(self):
        _,_,ratio=self.contribution_fixture()
        result=next(row for row in self.check() if row['claim_id']==ratio['claim_id'])['net_return']
        self.assertEqual(result['value'],'4')
        self.assertEqual(result['return_kind'],'contribution_roas')
        self.assertIs(result['profit_checked'],False)

    def test_contribution_roas_missing_cost_is_not_zero(self):
        costs,_,_=self.contribution_fixture()
        costs[0].update(status='unknown',value=None)
        with self.assertRaisesRegex(ValueError,'unknown_input'): self.check()

    def test_contribution_roas_arbitrary_contribution_is_blocked(self):
        _,contribution,_=self.contribution_fixture()
        contribution['formula']['expression']='attributed_net_sales - attributed_discount * 0 - attributed_product_cost * 0 - attributed_platform_fee * 0 - attributed_fulfillment_cost * 0 - 400'
        with self.assertRaisesRegex(ValueError,'net_return_contribution_expression_mismatch'): self.check()

    def test_contribution_roas_requires_matching_cost_reconciliation(self):
        costs,_,_=self.contribution_fixture()
        costs[0]['attribution']['reconciliation_id']='OTHER'
        self.assertIn('net_return_attribution_mismatch',';'.join(validate_claims(self.data)[0]))

    def test_net_roas_chinese_alias_is_not_profit_roi(self):
        self.net_fixture(); self.roas['metric']='净ROAS'
        self.check()
        self.roas['metric']='roi'
        self.assertIn('ratio_definition_mismatch:roi',';'.join(validate_claims(self.data)[0]))

    def net_pdf_fixture(self):
        self.net_fixture()
        errors,counts=validate_claims(self.data); self.assertEqual(errors,[])
        path=self.root/'claims.json'; path.write_text(json.dumps(self.data),encoding='utf-8')
        package=dict(run_id='synthetic',client_scope='synthetic',period='2026-07',team_version='2.0.3',
            report_revision='R1',title='扣退款投产合成测试',gate_status='WARN',
            scope=dict(platform='tmall',store='synthetic'),
            metrics=[dict(period='2026-07',inputs=dict(net_roas=8))],
            expert_participation=[dict(agent_id='ad-profit-optimizer',display_name='合成测试岗',
                profession='数据测试',participation_status='synthetic_fixture',agent_task_ids=[],
                contribution_summary='非真实专家返回')],
            claim_ledger=dict(file=path.name,sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                claims=self.data['claims'],source_checks=validate_sources(self.data,self.root),**counts))
        report=self.root/'report.json'; report.write_text(json.dumps(package),encoding='utf-8')
        (self.root/'report.md').write_text('合成来源检查 '+','.join(c['claim_id'] for c in self.data['claims']),encoding='utf-8')
        return report

    def test_net_roas_pdf_labels_nonprofit_and_rechecks_refund_source(self):
        import pymupdf as fitz
        import generate_pdf_report as pdf
        report=self.net_pdf_fixture()
        result=pdf.generate(report,self.root/'report.pdf',self.root/'pdf-delivery.json',self.root/'pages')
        with fitz.open(self.root/'report.pdf') as document:
            text=''.join(page.get_text() for page in document)
        self.assertIn('扣退款',text); self.assertIn('非利润',text); self.assertIn('8.00倍',text)
        self.assertTrue(any('returns' in str(path) for path in result['chart_files']))
        self.assertIn('refund.csv',json.dumps(result))
        (self.root/'refund.csv').write_text('tampered',encoding='utf-8')
        with self.assertRaises(ValueError):
            pdf.generate(report,self.root/'report.pdf',self.root/'pdf-delivery.json',self.root/'pages')

    def test_return_chart_keeps_zero_without_filling_missing(self):
        import generate_pdf_report as pdf
        from matplotlib.axes import Axes
        from unittest.mock import patch
        original=Axes.bar; captured=[]
        def record(ax,x,height,*args,**kwargs):
            captured.append((list(x),list(height)))
            return original(ax,x,height,*args,**kwargs)
        rows=[dict(period='2026-06',inputs={'roas':None,'net_roas':0}),
              dict(period='2026-07',inputs={'roas':10,'net_roas':8})]
        with patch.object(Axes,'bar',record):
            self.assertTrue(pdf.chart_returns(rows,self.root/'returns.png'))
        self.assertEqual(captured[0][1],[0,10,8])
        self.assertEqual(captured[0][0][0],'2026-06\n扣退款 ROAS')
        self.assertFalse(pdf.chart_returns([dict(period='2026-07',inputs={})],self.root/'none.png'))

    def test_return_chart_shows_negative_contribution_without_calling_it_profit(self):
        import generate_pdf_report as pdf
        from matplotlib.axes import Axes
        from unittest.mock import patch
        original=Axes.bar; captured=[]
        def record(ax,x,height,*args,**kwargs):
            captured.append((list(x),list(height)))
            return original(ax,x,height,*args,**kwargs)
        rows=[dict(period='2026-07',inputs={'contribution_roas':-0.5})]
        with patch.object(Axes,'bar',record):
            self.assertTrue(pdf.chart_returns(rows,self.root/'contribution-returns.png'))
        self.assertEqual(captured[0][1],[-0.5])
        self.assertIn('扣匹配变动成本',captured[0][0][0])

    def ratio_fixture(self, metric, numerator, denominator, a, b, unit, input_units):
        self.file.write_text(f'花费,归因金额\n{a},{b}\n',encoding='utf-8')
        for row in (self.spend,self.gmv):
            row['source_ref']['source_sha256']=hashlib.sha256(self.file.read_bytes()).hexdigest()
        self.spend.update(metric=numerator,value=a,unit=input_units[0])
        self.gmv.update(metric=denominator,value=b,unit=input_units[1])
        self.roas.update(metric=metric,value=a/b,unit=unit,
            formula=dict(name=metric,numerator=numerator,denominator=denominator,
                         expression=f'{numerator} / {denominator}'))
        if metric == 'roi': self.accounting_fixture(a, b)

    def accounting_fixture(self, profit=20, cost=100):
        from accounting_guard import COST_METRICS, METHOD
        metrics=['recognized_revenue','revenue_refund',*COST_METRICS]
        values=[profit+cost,0,cost,*([0]*(len(COST_METRICS)-1))]
        path=self.root/'accounting.csv'
        path.write_text(','.join(metrics)+'\n'+','.join(map(str,values))+'\n',encoding='utf-8')
        rows=[]
        for index,(metric,value) in enumerate(zip(metrics,values)):
            rows.append(dict(claim_id='C-'+metric,metric=metric,value=value,unit='元',
                status='verified',period='2026-07',source_ref=dict(source_file=path.name,
                    source_id='synthetic-accounting',field=metric,range=chr(65+index)+'2',
                    source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())))
        self.data['claims'].extend(rows)
        perimeter=dict(perimeter_id='PERIMETER-SYNTHETIC-202607',accounting_basis='accrual',
            period_status='closed',completeness_status='declared_complete_for_listed_perimeter',
            authenticity_status='source_bound_not_independently_authenticated',
            source_system='synthetic-accounting-export',export_record_id='EXPORT-SYNTHETIC-1',
            exported_at='2026-08-01T00:00:00Z',covered_cost_categories=list(COST_METRICS),
            excluded_items=[])
        treatments={r['metric']:('explicit_zero' if r['value']==0 else 'direct_source') for r in rows[2:]}
        self.roas['accounting']=dict(method=METHOD,scope_note='合成经营利润口径，不代表真实财务审核',
            perimeter=perimeter,
            revenue_claim=rows[0]['claim_id'],refund_claim=rows[1]['claim_id'],
            costs={r['metric']:r['claim_id'] for r in rows[2:]},
            cost_treatment=treatments,allocations={})
        return rows

    def allocated_product_cost_fixture(self):
        from accounting_guard import ALLOCATION_METHOD
        path=self.root/'allocation.csv'
        path.write_text('共享成本池,本范围基数,总基数,分摊表合计\n200,50,100,200\n',encoding='utf-8')
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        definitions=[('C-pool','shared_cost_pool',200,'A','共享成本池'),
                     ('C-scope-base','allocation_scope_base',50,'B','本范围基数'),
                     ('C-total-base','allocation_total_base',100,'C','总基数'),
                     ('C-schedule-total','allocation_schedule_total',200,'D','分摊表合计')]
        support=[]
        for key,metric,value,column,field in definitions:
            support.append(dict(claim_id=key,metric=metric,value=value,unit='元',period='2026-07',
                status='verified',source_ref=dict(source_file=path.name,source_id='synthetic-allocation',
                    field=field,range=column+'2',source_sha256=digest)))
        product=next(row for row in self.data['claims'] if row.get('claim_id')=='C-product_cost')
        product.update(status='derived',inputs=['C-pool','C-scope-base','C-total-base'],
            formula=dict(name='allocated_product_cost',numerator='shared_pool',denominator='total_base',
                expression='shared_pool * scope_base / total_base',
                bindings={'shared_pool':'C-pool','scope_base':'C-scope-base','total_base':'C-total-base'}),
            source_ref=copy.deepcopy(support[0]['source_ref']))
        self.data['claims'].extend(support)
        self.roas['accounting']['cost_treatment']['product_cost']='allocated'
        self.roas['accounting']['allocations']['product_cost']=dict(method=ALLOCATION_METHOD,
            basis_name='实际订单金额',pool_claim='C-pool',scope_base_claim='C-scope-base',
            total_base_claim='C-total-base',schedule_total_claim='C-schedule-total')
        return support

    def test_roi_requires_accounting_not_boolean_flag(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.roas.pop('accounting')
        self.roas['attribution']['cost_complete']=True
        with self.assertRaisesRegex(ValueError,'accounting_contract_required'): self.check()

    def test_accounting_missing_category_is_not_zero(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.roas['accounting']['costs'].pop('tax_cost')
        with self.assertRaisesRegex(ValueError,'cost_categories_incomplete'): self.check()

    def test_accounting_requires_source_bound_closed_perimeter(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.roas['accounting'].pop('perimeter')
        with self.assertRaisesRegex(ValueError,'accounting_perimeter_required'): self.check()

    def test_accounting_cannot_claim_independent_authentication(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.roas['accounting']['perimeter']['authenticity_status']='authenticated'
        with self.assertRaisesRegex(ValueError,'accounting_authenticity_overclaim'): self.check()

    def test_accounting_cost_treatment_cannot_be_omitted(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.roas['accounting']['cost_treatment'].pop('tax_cost')
        with self.assertRaisesRegex(ValueError,'accounting_cost_treatment_incomplete'): self.check()

    def test_accounting_zero_must_be_read_from_source(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        tax=next(row for row in self.data['claims'] if row.get('claim_id')=='C-tax_cost')
        tax.update(status='derived',inputs=['C-platform_fee','C-inventory_loss'],
            formula=dict(name='zero',numerator='platform_fee',denominator='inventory_loss',
                         expression='platform_fee + inventory_loss'))
        with self.assertRaisesRegex(ValueError,'accounting_explicit_zero_not_sourced'): self.check()

    def test_accounting_allocation_is_recomputed_and_receipted(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.allocated_product_cost_fixture()
        result=next(row for row in self.check() if row['claim_id']=='C-roas')['accounting']
        self.assertEqual(result['status'],'declared_source_bound_operating_perimeter_reconciled')
        self.assertEqual(result['allocation_checks'][0]['amount'],'100')
        self.assertEqual(result['authenticity_status'],'source_bound_not_independently_authenticated')

    def test_accounting_allocation_arbitrary_ratio_is_blocked(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.allocated_product_cost_fixture()
        product=next(row for row in self.data['claims'] if row.get('claim_id')=='C-product_cost')
        product['formula']['expression']='shared_pool * 0.5 + scope_base * 0 + total_base * 0'
        with self.assertRaisesRegex(ValueError,'accounting_allocation_expression_mismatch'): self.check()

    def test_accounting_allocation_schedule_must_equal_pool(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        support=self.allocated_product_cost_fixture()
        schedule=next(row for row in support if row['claim_id']=='C-schedule-total')
        path=self.root/'allocation.csv'
        path.write_text('共享成本池,本范围基数,总基数,分摊表合计\n200,50,100,190\n',encoding='utf-8')
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        for row in support: row['source_ref']['source_sha256']=digest
        schedule['value']=190
        with self.assertRaisesRegex(ValueError,'accounting_allocation_schedule_not_reconciled'): self.check()

    def test_accounting_unknown_category_is_not_zero(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.data['claims'][-1].update(status='unknown',value=None)
        with self.assertRaisesRegex(ValueError,'component_unknown'): self.check()

    def test_accounting_cost_total_requires_reconciliation(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.data['claims']=self.data['claims'][:3]
        self.accounting_fixture(40,80)
        with self.assertRaisesRegex(ValueError,'cost_total_mismatch'): self.check()

    def test_accounting_profit_requires_reconciliation(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.data['claims']=self.data['claims'][:3]
        self.accounting_fixture(30,100)
        with self.assertRaisesRegex(ValueError,'accounting_profit_mismatch'): self.check()

    def test_accounting_actual_source_tamper_blocks(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        (self.root/'accounting.csv').write_text('tampered',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'hash_mismatch'): self.check()

    def test_accounting_scope_cannot_borrow_other_store(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.data['claims'][-1]['store']='another-store'
        with self.assertRaisesRegex(ValueError,'component_scope_mismatch'): self.check()

    def test_accounting_duplicate_component_blocked(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.roas['accounting']['costs']['tax_cost']='C-product_cost'
        with self.assertRaisesRegex(ValueError,'duplicate_component'): self.check()

    def test_accounting_renamed_same_source_cell_blocked(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.data['claims'][-1]['source_ref']=copy.deepcopy(self.data['claims'][-2]['source_ref'])
        with self.assertRaisesRegex(ValueError,'source_component_reused'): self.check()

    def test_accounting_receipt_lists_real_components(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        checks=self.check()
        result=next(r for r in checks if r['claim_id']=='C-roas')['accounting']
        self.assertEqual(result['profit'],'20')
        self.assertEqual(result['total_cost'],'100')
        self.assertEqual(len(result['component_claims']),9)
        self.assertIn('not_completeness',result['evidence_kind'])

    def test_accounting_derived_wrapper_cannot_duplicate_cost(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.data['claims'][-1].update(status='derived',inputs=['C-tax_cost','C-platform_fee'],
            formula=dict(name='cost_sum',numerator='tax_cost',denominator='platform_fee',
                         expression='tax_cost + platform_fee'))
        self.roas['accounting']['cost_treatment']['other_operating_cost']='direct_source'
        with self.assertRaisesRegex(ValueError,'source_component_reused'): self.check()

    def test_accounting_overlapping_source_ranges_cannot_duplicate_cost(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        path=self.root/'accounting.csv'
        path.write_text(path.read_text(encoding='utf-8')+','.join(['0']*9)+'\n',encoding='utf-8')
        for row in self.data['claims'][3:]:
            row['source_ref']['source_sha256']=hashlib.sha256(path.read_bytes()).hexdigest()
        self.data['claims'][-1]['source_ref']=copy.deepcopy(self.data['claims'][-2]['source_ref'])
        self.data['claims'][-1]['source_ref'].update(range='H2:H3',aggregation='sum',sheet='fake-csv-sheet')
        with self.assertRaisesRegex(ValueError,'source_component_reused'): self.check()

    def test_accounting_cli_blocks_missing_contract(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.roas.pop('accounting')
        path=self.root/'claims.json'; path.write_text(json.dumps(self.data),encoding='utf-8')
        receipt=self.root/'receipt.json'
        result=subprocess.run([sys.executable,str(Path(__file__).with_name('claim_guard.py')),
            '--claims',str(path),'--output',str(receipt)],capture_output=True,text=True,encoding='utf-8')
        self.assertEqual(result.returncode,2)
        blocked=json.loads(receipt.read_text(encoding='utf-8'))
        self.assertEqual(blocked['status'],'claim_guard_blocked')
        self.assertEqual(blocked['contract_name'],'omni-ecom.failure-diagnostic')
        self.assertFalse(blocked['legacy_compatibility']['current_authority'])
        self.assertIn('accounting_contract_required',receipt.read_text(encoding='utf-8'))

    def test_accounting_contract_schema_accepts_valid_rejects_missing_cost(self):
        from jsonschema import Draft202012Validator
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        schema=json.loads((Path(__file__).resolve().parents[1]/'schemas'/'claim-ledger.schema.json').read_text(encoding='utf-8'))
        validator=Draft202012Validator(schema)
        self.assertEqual(list(validator.iter_errors(self.data)),[])
        self.roas['accounting']['costs'].pop('product_cost')
        self.assertTrue(list(validator.iter_errors(self.data)))

    def test_net_return_flag_cannot_bypass_definition(self):
        self.roas.update(metric='net_roi')
        self.roas['formula']['name']='net_roas'
        self.roas['attribution']['cost_complete']=True
        self.assertIn('claim_1_net_return_definition_unresolved',validate_claims(self.data)[0])

    def test_roi_uses_profit_and_total_cost_including_loss(self):
        self.ratio_fixture('roi','profit','total_cost',-20,100,'ratio',('元','元'))
        self.assertEqual(self.check()[-1]['value'],'-0.2')

    def test_roas_cannot_be_renamed_roi(self):
        self.roas['metric']='ROI'
        errors,_=validate_claims(self.data)
        self.assertIn('claim_1_ratio_definition_mismatch:roi',errors)

    def test_orders_cannot_be_buyer_conversion(self):
        self.ratio_fixture('conversion_rate','orders','visitors',100,1000,'ratio',('单','人'))
        errors,_=validate_claims(self.data)
        self.assertIn('claim_1_ratio_definition_mismatch:conversion_rate',errors)
        self.roas.update(metric='orders_per_visitor',unit='单/人')
        self.roas['formula']['name']='orders_per_visitor'
        self.check()

    def test_percentage_requires_explicit_scale(self):
        self.ratio_fixture('conversion_rate','buyers','visitors',100,1000,'%',('人','人'))
        with self.assertRaisesRegex(ValueError,'percent_expression_requires_scale'): self.check()
        self.roas['formula']['expression']='buyers / visitors * 100'
        self.roas['value']=10
        self.check()

    def test_conversion_buyers_cannot_exceed_visitors(self):
        self.ratio_fixture('conversion_rate','buyers','visitors',1000,100,'ratio',('人','人'))
        with self.assertRaisesRegex(ValueError,'buyers_exceed_visitors'): self.check()

    def test_ratio_input_units_and_currency_must_match(self):
        self.spend['unit']='人'
        self.assertIn('claim_1_ratio_input_unit_mismatch',validate_claims(self.data)[0])
        self.spend['unit']='元'
        for row in self.data['claims']: row['currency']='CNY'
        self.check()
        self.spend['currency']='USD'
        self.assertIn('claim_1_ratio_currency_mismatch',validate_claims(self.data)[0])

    def test_roi_unknown_cost_cannot_compute(self):
        self.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.gmv.update(status='unknown',value=None)
        with self.assertRaisesRegex(ValueError,'unknown_input'): self.check()

    def test_raw_backend_ratio_requires_normalization(self):
        self.roas['status']='verified'
        self.assertIn('claim_1_normalized_ratio_requires_derived',validate_claims(self.data)[0])

    def test_ratio_aliases_bind_actual_source_metrics(self):
        self.ratio_fixture('支付转化率','paid_buyers','uv',100,1000,'ratio',('人','人'))
        self.check()

    def test_adjudication_uses_same_ratio_definitions(self):
        from semantic_adjudication import RECIPES
        from metric_semantics import ADJUDICATION_RECIPES
        for key,value in ADJUDICATION_RECIPES.items(): self.assertEqual(RECIPES[key],value)
        self.assertEqual(RECIPES['ROI'][0],'profit / total_cost')

    def test_invented_spend(self):
        self.spend['value']=8131
        with self.assertRaisesRegex(ValueError,'value_not_reproducible'): self.check()

    def test_invented_roas(self):
        self.roas['value']=9.06
        with self.assertRaisesRegex(ValueError,'value_not_reproducible'): self.check()

    def test_missing_source(self):
        self.file.unlink()
        with self.assertRaisesRegex(ValueError,'outside_or_missing'): self.check()

    def test_changed_source_hash(self):
        self.file.write_text('花费,归因金额\n8131,1000\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'hash_mismatch'): self.check()

    def test_wrong_field_at_correct_range(self):
        self.spend['source_ref']['field']='归因金额'
        with self.assertRaisesRegex(ValueError,'field_mismatch'): self.check()

    def test_multiple_cells_require_explicit_aggregation(self):
        self.file.write_text('花费,归因金额\n40,1000\n60,0\n',encoding='utf-8')
        for row in (self.spend,self.gmv): row['source_ref']['source_sha256']=hashlib.sha256(self.file.read_bytes()).hexdigest()
        self.spend['source_ref']['range']='A2:A3'
        with self.assertRaisesRegex(ValueError,'aggregation_required'): self.check()
        self.spend['source_ref']['aggregation']='sum'
        self.check()

    def test_unknown_not_zero_and_unknown_input_rejected(self):
        self.spend.update(status='unknown',value=None)
        with self.assertRaisesRegex(ValueError,'unknown_input'): self.check()
        self.data['claims']=[self.spend]
        self.assertEqual(self.check()[0]['status'],'unknown_not_recomputed')

    def test_forged_ratio_expression(self):
        self.roas['formula']['expression']='0 * attributed_gmv + 0 * ad_spend + 9.06'
        self.roas['value']=9.06
        with self.assertRaisesRegex(ValueError,'ratio_expression_mismatch'): self.check()

    def test_swapped_ratio_bindings(self):
        self.roas['formula']['bindings']={'attributed_gmv':'C-spend','ad_spend':'C-gmv'}
        self.roas['value']=0.1
        with self.assertRaisesRegex(ValueError,'ratio_binding_mismatch'): self.check()

    def test_renamed_formula_cannot_hide_false_conversion(self):
        self.spend['metric']='paid_buyers'; self.gmv['metric']='visitors'
        self.spend['unit']=self.gmv['unit']='人'
        self.roas.update(metric='conversion_rate',value=9.06,unit='ratio')
        self.roas['formula']=dict(name='custom',numerator='paid_buyers',denominator='visitors',
                                  expression='paid_buyers * 0 + visitors * 0 + 9.06')
        with self.assertRaisesRegex(ValueError,'ratio_expression_mismatch'): self.check()

    def test_cycle(self):
        self.spend.update(status='derived',formula=copy.deepcopy(self.roas['formula']),inputs=['C-roas','C-gmv'])
        with self.assertRaisesRegex(ValueError,'dependency_cycle'): self.check()

    def test_zero_denominator(self):
        self.file.write_text('花费,归因金额\n0,1000\n',encoding='utf-8')
        for row in (self.spend,self.gmv): row['source_ref']['source_sha256']=hashlib.sha256(self.file.read_bytes()).hexdigest()
        self.spend['value']=0
        with self.assertRaisesRegex(ValueError,'zero_denominator'): self.check()

    def test_path_escape(self):
        self.spend['source_ref']['source_file']='../source.csv'
        with self.assertRaisesRegex(ValueError,'path_outside'): self.check()

    def test_explicit_rounding(self):
        self.file.write_text('花费,归因金额\n3,10\n',encoding='utf-8')
        for row in (self.spend,self.gmv): row['source_ref']['source_sha256']=hashlib.sha256(self.file.read_bytes()).hexdigest()
        self.spend['value']=3; self.gmv['value']=10; self.roas['value']=3.33
        with self.assertRaisesRegex(ValueError,'value_not_reproducible'): self.check()
        self.roas['decimal_places']=2
        self.check()

    def test_xlsx_with_offset_header(self):
        import openpyxl
        book=openpyxl.Workbook(); sheet=book.active; sheet.title='数据'
        sheet.append(['合成测试']); sheet.append(['花费']); sheet.append([100])
        path=self.root/'source.xlsx'; book.save(path); book.close()
        self.data['claims']=[self.spend]
        self.spend['source_ref'].update(source_file=path.name,sheet='数据',header_row=2,range='A3',
                                        source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        self.check()

    def test_json_pointer(self):
        path=self.root/'source.json'; path.write_text('{"spend":[100]}',encoding='utf-8')
        self.data['claims']=[self.spend]
        self.spend['source_ref'].update(source_file=path.name,pointer='/spend/0',source_sha256=hashlib.sha256(path.read_bytes()).hexdigest())
        self.check()

    def test_cli_structure_only_cannot_issue_pass(self):
        path=self.root/'claims.json'; path.write_text(json.dumps(self.data),encoding='utf-8')
        script=Path(__file__).with_name('claim_guard.py')
        for flags,status in (([],'claim_guard_passed'),(['--structure-only'],'claim_structure_passed')):
            output=self.root/'receipt.json'
            result=subprocess.run([sys.executable,str(script),'--claims',str(path),'--output',str(output),*flags],
                                  capture_output=True,text=True,encoding='utf-8')
            self.assertEqual(result.returncode,0,result.stderr)
            self.assertEqual(json.loads(output.read_text(encoding='utf-8'))['status'],status)

    def test_builder_rejects_fabrication_before_pdf(self):
        args=pipeline.prepare_builder_sample(self.root,'monthly_report')
        path=self.root/'claims.json'; data=json.loads(path.read_text(encoding='utf-8'))
        data['claims'][0]['value']=8131
        path.write_text(json.dumps(data),encoding='utf-8')
        result=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',env={**os.environ,'PYTHONIOENCODING':'utf-8'})
        self.assertNotEqual(result.returncode,0)
        self.assertIn('value_not_reproducible',result.stdout+result.stderr)
        self.assertFalse((self.root/'report.pdf').exists())


if __name__=='__main__': unittest.main()
