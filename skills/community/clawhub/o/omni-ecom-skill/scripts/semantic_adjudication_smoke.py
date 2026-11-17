"""Synthetic original rows exercise semantic adjudication, not causal proof."""
import copy
import json
import unittest
from unittest.mock import patch

import quality_gate_smoke as fixture
import conflict_scan
from adjudication_guard import fingerprint
from quality_gate import read,sha,validate_quality
from semantic_adjudication import period,check_period_cells,contract_for,RECIPES
from artifact_contract import native_analysis_identity


class AccountingBridgeTests(unittest.TestCase):
    def setUp(self):
        import claim_source_guard_smoke as sources
        self.fx=sources.SourceTests(); self.fx.setUp(); self.addCleanup(self.fx.doCleanups)
        self.fx.ratio_fixture('roi','profit','total_cost',20,100,'ratio',('元','元'))
        self.root=self.fx.root; self.ledger=self.fx.data
        self.ledger.update(scope={'platform':'tmall','store':'synthetic'},source_context_policy='required')
        for path in (self.fx.file,self.root/'accounting.csv'):
            lines=path.read_text(encoding='utf-8').splitlines(); n=len(lines[0].split(','))
            path.write_text(lines[0]+',期间,平台,店铺,单位\n'+lines[1]+',2026-07,tmall,synthetic,元\n',encoding='utf-8')
            for row in self.ledger['claims']:
                if row['status']=='verified' and row['source_ref']['source_file']==path.name:
                    row['source_ref'].update(source_sha256=sha(path),contexts={
                        key:dict(column=chr(65+n+i),field=label) for i,(key,label) in enumerate(
                            [('period','期间'),('platform','平台'),('store','店铺'),('unit','单位')])})
        self.report={k:self.ledger[k] for k in ('run_id','client_scope','period','scope')}
        self.report.update(team_version='2.0.3',report_revision='R1')
        (self.root/'report.md').write_text('合成财务裁决 '+ ' '.join(r['claim_id'] for r in self.ledger['claims']),encoding='utf-8')
        self.save()
        self.contract=dict(unit='ratio',profit_scope='文字说明',total_cost_scope='文字说明')
        self.data=dict(period='2026-07',value=0.2,accounting_claim_id=self.fx.roas['claim_id'])

    def save(self):
        from claim_guard import validate_claims
        from claim_source_guard import validate_sources
        fixture.write(self.root/'claims.json',self.ledger)
        errors,counts=validate_claims(self.ledger); self.assertEqual(errors,[])
        self.report['claim_ledger']=dict(file='claims.json',sha256=sha(self.root/'claims.json'),
            claims=self.ledger['claims'],source_checks=validate_sources(self.ledger,self.root),**counts)
        fixture.write(self.root/'report.json',self.report)

    def check(self):
        from semantic_adjudication import measure
        return measure(self.data,self.contract,'profit / total_cost',{'profit':{},'total_cost':{}},
                       lambda name:(self.root/name).resolve(),{},self.report,self.ledger['scope'])

    def test_reconciled_roi_uses_same_sources_and_freezes_components(self):
        value,window,values,sources=self.check()
        self.assertEqual(str(value),'0.2'); self.assertEqual(values['profit'],20)
        self.assertEqual({__import__('pathlib').Path(p).name for p in sources},
                         {'claims.json',self.fx.file.name,'accounting.csv'})

    def test_free_text_scope_and_raw_totals_cannot_bypass_accounting(self):
        self.data=dict(period='2026-07',value=0.2,inputs={'profit':{},'total_cost':{}})
        with self.assertRaisesRegex(ValueError,'accounting_binding_required'): self.check()

    def test_other_metric_cannot_impersonate_profit_roi(self):
        self.data['accounting_claim_id']=self.fx.spend['claim_id']
        with self.assertRaisesRegex(ValueError,'accounting_claim_invalid'): self.check()

    def test_ledger_component_change_blocks_adjudication(self):
        (self.root/'accounting.csv').write_text('tampered',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'hash_mismatch'): self.check()

    def test_another_period_cannot_borrow_current_roi(self):
        self.data['period']='2026-06'
        with self.assertRaisesRegex(ValueError,'accounting_period_unit_mismatch'): self.check()

    def test_other_baseline_store_cannot_borrow_verified_roi(self):
        from semantic_adjudication import measure
        with self.assertRaisesRegex(ValueError,'accounting_baseline_scope_mismatch'):
            measure(self.data,self.contract,'profit / total_cost',{'profit':{},'total_cost':{}},
                    lambda name:(self.root/name).resolve(),{},self.report,{'platform':'tmall','store':'other'})

    def test_wrong_declared_return_rejected(self):
        self.data['value']=2.91
        with self.assertRaisesRegex(ValueError,'measurement_value_mismatch'): self.check()

    def test_root_dimension_and_currency_are_inherited_and_bound(self):
        self.ledger['scope'].update(dimensions={'channel':'search'},currency='CNY')
        for row in self.ledger['claims']:
            if row['status']=='verified':
                path=self.root/row['source_ref']['source_file']
                lines=path.read_text(encoding='utf-8').splitlines()
                if '渠道' not in lines[0]:
                    path.write_text(lines[0]+',渠道,币种\n'+lines[1]+',search,CNY\n',encoding='utf-8')
                headings=path.read_text(encoding='utf-8').splitlines()[0].split(',')
                row['source_ref']['source_sha256']=sha(path)
                row['source_ref']['contexts'].update({
                    'dimensions.channel':dict(column=chr(65+headings.index('渠道')),field='渠道'),
                    'currency':dict(column=chr(65+headings.index('币种')),field='币种')})
        self.save()
        value,_,_,_=self.check(); self.assertEqual(str(value),'0.2')

    def test_claim_cannot_override_root_dimension_or_currency(self):
        from accounting_guard import scope
        self.ledger['scope'].update(dimensions={'channel':'search'},currency='CNY')
        self.fx.roas.update(dimensions={'channel':'organic'})
        with self.assertRaisesRegex(ValueError,'accounting_scope_conflict'):
            scope(self.ledger,self.fx.roas)

        self.fx.roas.pop('dimensions')
        self.ledger['claims'][-1]['currency']='USD'
        with self.assertRaisesRegex(ValueError,'accounting_scope_conflict'):
            scope(self.ledger,self.ledger['claims'][-1])


class SemanticTests(unittest.TestCase):
    def setUp(self):
        self.fx=fixture.QualityTests(); self.fx.setUp()
        self.root,self.report=self.fx.root,self.fx.report
        self.config=read(self.root/'quality-inputs.json')
        self.source=self.root/'交易.csv'
        self.source.write_text('月份,金额,买家,访客\n2026-06,100,10,100\n2026-07,200,20,100\n',encoding='utf-8')
        self.prepare('direction')

    def tearDown(self): self.fx.tearDown()

    def bind_inventory(self):
        path=self.root/self.config['inventory']; value=read(path)
        value['reports'][0].update(file_path=str(self.source),sha256=sha(self.source))
        fixture.write(path,value)

    def prepare(self,kind):
        self.bind_inventory(); self.kind=kind
        baseline=read(self.root/self.config['baseline'])
        self.metric='GMV' if kind=='direction' else '转化率'
        if kind=='direction':
            self.contract=dict(definition='支付金额',formula='SUM(支付金额)',unit='元',denominator='无',
                dedupe_rule='平台期间汇总',attribution_window='支付发生期间',
                calculation=dict(expression='gmv',inputs={'gmv':dict(source_field='金额',unit='元',aggregation='value')}))
            current_value,previous_value=200,100
        else:
            self.contract=dict(definition='支付买家数/同范围去重访客',formula='buyers / visitors * 100',unit='%',
                denominator='同范围去重访客',dedupe_rule='期间内平台去重人数',attribution_window='同一支付发生期间',
                calculation=dict(expression='buyers / visitors * 100',inputs={
                    'buyers':dict(source_field='买家',unit='人',aggregation='value'),
                    'visitors':dict(source_field='访客',unit='人',aggregation='value')}))
            current_value,previous_value=20,10
        baseline['metric_contract'][self.metric]=self.contract
        fixture.write(self.root/self.config['baseline'],baseline)
        baseline_hash=sha(self.root/self.config['baseline'])
        bodies={}
        for role,path in self.config['handoffs'].items():
            body=read(self.root/path)
            body['analysis_depth']['baseline_ack']['baseline_sha256']=baseline_hash
            body['facts']=[dict(id='F1',claim='合成原始数据',evidence_ids=['E1'])]
            body['judgments']=[]
            body['evidence_ledger']=[dict(id='E1',source='交易.csv',period='2026-07',metric=self.metric,
                                        value=current_value,status='verified')]
            if kind=='direction' and role in ('data-analyst','platform-ops'):
                body['judgments']=[dict(id='J1',claim='GMV 上升' if role=='data-analyst' else 'GMV 下降',
                                       confidence='medium',evidence_ids=['E1'],counter_conditions=['期间或口径不一致时需重核'])]
            elif kind=='caliber':
                body['evidence_ledger'][0]['formula']='gmv / visitors' if role=='platform-ops' else 'buyers / visitors'
            fixture.write(self.root/path,body); bodies[role]=body
        rows=[r for role,b in bodies.items() for r in conflict_scan.evidence_rows(b,role)]
        causal_review=conflict_scan.review_handoffs(
            bodies,self.report['run_id'],self.report['client_scope'],self.report['team_version'])
        self.found=(conflict_scan.scan_numeric(rows,0.02)+conflict_scan.scan_caliber(rows,bodies)+
                    conflict_scan.scan_direction(bodies)+conflict_scan.causal_conflicts(causal_review))
        self.assertEqual(len(self.found),1)
        self.cid=self.found[0]['conflict_id']
        def measurement(index,value,month):
            return dict(period=month,value=value,inputs={name:dict(report_id='R001',file=self.source.name,
                sha256=sha(self.source),column=binding['source_field'],rows=[index],aggregation='value',period_column='月份')
                for name,binding in self.contract['calculation']['inputs'].items()})
        self.row=dict(conflict_id=self.cid,method='trend_recomputation' if kind=='direction' else 'caliber_recomputation',
            decision='采用原始表与下发口径',not_adopted_disposition=[dict(agent_id='platform-ops',reason='口径或方向错误')],
            residual_risk='合成数据不代表实际经营',baseline_sha256=baseline_hash,metric=self.metric,unit=self.contract['unit'],
            current=measurement(1,current_value,'2026-07'),downstream=[],no_downstream_reason='合成报告无经营动作')
        claim=dict(metric=self.metric,unit=self.contract['unit'],value=current_value,period='2026-07',
                   baseline_sha256=baseline_hash,caliber_sha256=fingerprint(self.contract))
        if kind=='direction':
            self.row.update(previous=measurement(0,previous_value,'2026-06'),direction='up',
                            comparability_note='对比相邻自然月，天数分别为 31 和 30；只比较各月金额，不作因果推断')
            claim.update(previous_value=previous_value,previous_period='2026-06',direction='up',absolute_change=100,
                         comparability_note=self.row['comparability_note'],current_days=31,previous_days=30)
        self.report['adjudicated_claims']={self.cid:claim}
        self.verdict=dict(**native_analysis_identity('conflict_verdict',self.report['team_version']),
                          **{k:self.report[k] for k in ('run_id','client_scope','team_version','report_revision')},
                          conflicts_sha256=fingerprint(self.found),verdicts=[self.row])
        self.config['adjudication']='verdict.json'; fixture.write(self.root/'quality-inputs.json',self.config)
        self.save()

    def save(self):
        fixture.write(self.root/'verdict.json',self.verdict)
        fixture.present_verdict(self.root,self.report,self.verdict)

    def validate(self):
        self.save(); return validate_quality(self.root,self.report)

    def test_trend_recomputes_two_actual_periods(self):
        result=self.validate()['adjudications'][0]
        self.assertEqual(result['direction'],'up'); self.assertEqual(result['absolute_change'],'100')
        self.assertEqual(result['current_days'],31); self.assertEqual(result['previous_days'],30)

    def test_caliber_uses_buyers_not_gmv(self):
        self.prepare('caliber')
        result=self.validate()['adjudications'][0]
        self.assertEqual(result['value'],'20.0'); self.assertEqual(result['unit'],'%')

    def test_wrong_direction_is_rejected(self):
        self.row['direction']='down'
        with self.assertRaisesRegex(ValueError,'direction_mismatch'): self.validate()

    def test_report_cannot_keep_old_trend(self):
        self.report['adjudicated_claims'][self.cid]['direction']='down'
        with self.assertRaisesRegex(ValueError,'semantic_report_stale'): self.validate()

    def test_same_name_file_cannot_substitute_another_source(self):
        alternative=self.root/'other'; alternative.mkdir()
        (alternative/self.source.name).write_bytes(self.source.read_bytes())
        self.row['current']['inputs']['gmv']['file']='other/交易.csv'
        with self.assertRaisesRegex(ValueError,'source_inventory_mismatch'): self.validate()

    def test_unknown_source_id_cannot_pass_on_filename(self):
        self.row['current']['inputs']['gmv']['report_id']='R999'
        with self.assertRaisesRegex(ValueError,'source_id_unknown'): self.validate()

    def test_raw_period_not_declared_label_controls_comparison(self):
        self.row['current']['inputs']['gmv']['rows']=[0]
        self.row['current']['value']=100
        with self.assertRaisesRegex(ValueError,'source_period_mismatch'): self.validate()

    def test_reused_period_cannot_be_called_a_comparison(self):
        self.row['previous']=copy.deepcopy(self.row['current'])
        with self.assertRaisesRegex(ValueError,'periods_overlap_or_reversed'): self.validate()

    def test_missing_period_column_not_silently_accepted(self):
        del self.row['current']['inputs']['gmv']['period_column']
        with self.assertRaisesRegex(ValueError,'period_column_missing'): self.validate()

    def test_comparison_note_is_required(self):
        del self.row['comparability_note']
        with self.assertRaisesRegex(ValueError,'comparability_missing'): self.validate()

    def change_contract(self,update):
        path=self.root/self.config['baseline']; base=read(path); update(base['metric_contract'][self.metric])
        fixture.write(path,base)
        for file in self.config['handoffs'].values():
            body=read(self.root/file); body['analysis_depth']['baseline_ack']['baseline_sha256']=sha(path); fixture.write(self.root/file,body)
        self.row['baseline_sha256']=sha(path)

    def test_gmv_per_visitor_cannot_be_called_conversion(self):
        self.prepare('caliber')
        self.change_contract(lambda c:c['calculation'].update(expression='gmv / visitors * 100'))
        with self.assertRaisesRegex(ValueError,'metric_formula_mismatch'): self.validate()

    def test_cross_period_people_sum_is_blocked(self):
        self.prepare('caliber')
        self.change_contract(lambda c:c['calculation']['inputs']['visitors'].update(aggregation='sum'))
        with self.assertRaisesRegex(ValueError,'people_cannot_sum'): self.validate()

    def test_unit_mismatch_is_blocked(self):
        self.row['unit']='%'
        with self.assertRaisesRegex(ValueError,'metric_scope_mismatch'): self.validate()

    def test_stale_baseline_cannot_be_adopted(self):
        self.row['baseline_sha256']='0'*64
        with self.assertRaisesRegex(ValueError,'baseline_changed'): self.validate()

    def test_wrong_measurement_total_is_blocked(self):
        self.row['current']['value']=999
        with self.assertRaisesRegex(ValueError,'measurement_value_mismatch'): self.validate()

    def test_numeric_downstream_must_use_recomputed_trend(self):
        self.row['downstream']=[dict(claim_id='delta',formula='adjudicated - previous',result='100')]
        self.report['adjudicated_downstream']={'delta':{'value':100}}
        self.validate()
        self.report['adjudicated_downstream']['delta']['value']=-100
        with self.assertRaisesRegex(ValueError,'downstream_report_stale'): self.validate()

    def test_period_missing_day_does_not_masquerade_as_complete(self):
        self.source.write_text('日期,金额\n2026-07-01,20\n2026-07-03,30\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'source_period_gap'):
            check_period_cells(self.source,dict(period_column='日期',rows=[0,1]),period(dict(start='2026-07-01',end='2026-07-03')))

    def test_json_period_pointer_reads_original(self):
        path=self.root/'data.json'; fixture.write(path,dict(period='2026-07',gmv=200))
        check_period_cells(path,dict(period_pointer='/period'),period('2026-07'))
        with self.assertRaisesRegex(ValueError,'source_period_mismatch'):
            check_period_cells(path,dict(period_pointer='/period'),period('2026-06'))

    def test_excel_period_column_with_offset_header(self):
        import openpyxl
        path=self.root/'periods.xlsx'; book=openpyxl.Workbook(); sheet=book.active
        sheet.append(['标题']); sheet.append(['月份','金额']); sheet.append(['2026-07',200]); book.save(path); book.close()
        check_period_cells(path,dict(sheet='Sheet',header_row=2,rows=[0],period_column='月份'),period('2026-07'))

    def test_new_baseline_contract_validates_against_schema(self):
        from jsonschema import Draft202012Validator
        from pathlib import Path
        self.prepare('caliber')
        schema=read(Path(__file__).resolve().parents[1]/'schemas'/'baseline-pack.schema.json')
        self.assertEqual(list(Draft202012Validator(schema).iter_errors(read(self.root/self.config['baseline']))),[])

    def test_missing_period_cell_is_a_controlled_error(self):
        self.source.write_text('金额,月份\n20\n',encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'period_cell_missing'):
            check_period_cells(self.source,dict(period_column='月份',rows=[0]),period('2026-07'))

    def test_recipe_units_and_variables_are_consistent(self):
        for metric,(expression,units,unit) in RECIPES.items():
            for representation in (('ratio','%') if unit=='ratio' else (unit,)):
                with self.subTest(metric=metric,unit=representation):
                    formula='('+expression+') * 100' if representation=='%' else expression
                    contract=dict(definition='合成已声明指标',formula=formula,unit=representation,denominator='合成分母口径',
                        dedupe_rule='原始期间汇总',attribution_window='当期',calculation=dict(expression=formula,
                        inputs={key:dict(source_field=key,unit=u,aggregation='value') for key,u in units.items()}))
                    actual,expr,bindings=contract_for(metric,dict(metric_contract={metric:contract}))
                    self.assertEqual(expr,formula); self.assertEqual(set(bindings),set(units))

    def full_runtime(self):
        import runtime_binding_smoke
        import challenge_runtime_smoke
        import challenge_runtime
        runtime_fixture=runtime_binding_smoke.BindingTests()
        # Reuse these already-created synthetic sources before real binding code
        # records all four exported fixture tasks; do not edit sealed handoffs.
        with patch.object(runtime_binding_smoke.quality_fixture,'QualityTests',return_value=self.fx), patch.object(self.fx,'setUp'):
            runtime_fixture.setUp()
        try:
            challenges=challenge_runtime_smoke.ChallengeTests()
            challenges.fx=runtime_fixture
            challenges.root,challenges.rt,challenges.report=self.root,runtime_fixture.rt,self.report
            challenges.identity,challenges.round_id,challenges.targets,_,_=challenge_runtime.context(runtime_fixture.rt,self.report)
            challenges.all_returns()
            manifest=runtime_fixture.freeze(); runtime_fixture.review()
            code,output=runtime_fixture.complete()
            self.assertEqual(code,0,output)
            self.assertEqual(manifest['quality_gate']['adjudications'][0]['metric'],self.metric)
            self.assertEqual(runtime_fixture.rt.status()['next_action'],'reuse_verified_delivery')
        finally: runtime_fixture.rt.close()

    def test_trend_through_bound_challenge_freeze_review_completion(self):
        self.full_runtime()

    def test_caliber_through_bound_challenge_freeze_review_completion(self):
        self.prepare('caliber'); self.full_runtime()


if __name__=='__main__': unittest.main()
