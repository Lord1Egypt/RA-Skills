from __future__ import annotations
import hashlib, json, subprocess, sys, tempfile, unittest, zipfile
from pathlib import Path
from PIL import Image, ImageDraw

ROOT=Path(__file__).resolve().parents[1];BIN=ROOT/'bin'
def run(script,*args,ok=True):
    r=subprocess.run([sys.executable,str(BIN/script),*(str(a) for a in args)],text=True,capture_output=True)
    if ok and r.returncode!=0:raise AssertionError(f"{script} failed {r.returncode}\n{r.stdout}\n{r.stderr}")
    return r

def brief(name):
    return {'subject_priority':name,'thumbnail_read':name,'preserve_anchors':['anchor'],'abstract_or_omit':['minor detail'],
        'material_depth_cues':['depth cue'],'structural_lines':[{'element':'main direction','operation':'retain_but_simplify'}],
        'forbidden_inventions':['invented line']}

class HardeningTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.w=Path(self.tmp.name)
        self.config=self.w/'resolved.json';run('resolve_config.py','--preset',ROOT/'presets/travel-food-journal.json','--output',self.config)
        config=json.loads(self.config.read_text());config['profiles']['composition']['canvas'].update(width=64,height=96);self.config.write_text(json.dumps(config))
    def tearDown(self):self.tmp.cleanup()
    def test_generic_regression_fixture_covers_four_visual_cases(self):
        d=json.loads((ROOT/'tests/fixtures/generic-visual-cases.json').read_text())
        self.assertEqual([p['case'] for p in d['pages']],['open-sky cloud study','courtyard tree','glass facade','high-altitude city'])
        self.assertEqual({x['operation'] for x in d['revision_examples']},{'remove','retain_but_simplify','add_as_secondary','preserve_unchanged'})
    def test_default_config_includes_complete_workflow_and_style_contract(self):
        d=json.loads(self.config.read_text());wf=d['workflow_defaults'];style=d['profiles']['style']
        self.assertTrue(wf['qa']['page_level_required']);self.assertTrue(wf['qa']['set_level_required'])
        self.assertFalse(style['sample_style_contract_defaults']['generated_page_is_style_reference'])
        self.assertIn(style['plate_normalization']['mode'],{'paper-key-soft','alpha-required','disabled'})
    def test_clean_plate_removes_background_and_blocks_frame(self):
        config=json.loads(self.config.read_text());config['profiles']['composition']['canvas'].update(width=96,height=96);self.config.write_text(json.dumps(config))
        raw=self.w/'raw.png';im=Image.new('RGB',(96,96),'white');ImageDraw.Draw(im).line((25,48,70,48),fill='black',width=3);im.save(raw)
        out=self.w/'plate.png';rep=self.w/'plate.json';r=run('clean_plate.py','normalize','--input',raw,'--config',self.config,'--output',out,'--report',rep)
        with Image.open(out) as got:self.assertEqual(got.getpixel((0,0))[3],0);self.assertGreater(got.getpixel((48,48))[3],0)
        cfg=json.loads(self.config.read_text());cfg['profiles']['style']['plate_normalization']={'mode':'alpha-required','frame_policy':'forbid','max_corner_alpha_mean':8,'max_empty_area_noise_ratio':.01};strict=self.w/'strict.json';strict.write_text(json.dumps(cfg))
        framed=self.w/'framed.png';f=Image.new('RGBA',(96,96),(0,0,0,0));d=ImageDraw.Draw(f);d.rectangle((0,0,95,95),outline=(0,0,0,255),width=2);f.save(framed)
        blocked=run('clean_plate.py','validate','--input',framed,'--config',strict,'--report',self.w/'bad.json',ok=False)
        self.assertEqual(blocked.returncode,4)
    def make_plan_state_stage(self):
        import hashlib
        contract={'generated_page_is_style_reference':False}
        sources=[]
        for i in range(1,5):
            source=self.w/f'source-{i}.jpg';Image.new('RGB',(8,8),'white').save(source);sources.append(source)
        h=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
        plan=self.w/'plan.json';plan.write_text(json.dumps({'schema_version':'2.0.0','resolved_config_lock':{'path':str(self.config.resolve()),'sha256':h(self.config)},'sample_style_contract':contract,'pages':[{'page':i,'source_path':str(sources[i-1].resolve()),'source_sha256':h(sources[i-1]),'production_brief':brief(str(i)),'render_prompt':'base'} for i in range(1,5)]}))
        final=self.w/'final';final.mkdir(exist_ok=True)
        for i in range(1,5):Image.new('RGB',(64,96),(241,235,221)).save(final/f'{i:02d}.webp')
        stage=self.w/'stage.json';run('package_verified.py','stage','--input',final,'--output',stage)
        production=self.w/'production.md';production.write_text('approved plan')
        sample=final/'01.webp';plate=self.w/'sample-plate.png';Image.new('RGBA',(64,96),(0,0,0,0)).save(plate)
        validation_report=self.w/'sample-plate-validation.json';run('clean_plate.py','validate','--input',plate,'--config',self.config,'--report',validation_report);plate_validation=json.loads(validation_report.read_text())['analysis']
        receipt=self.w/'renderer-receipt.json';run('renderer_receipt.py','register','--output',receipt,'--renderer-kind','local','--model','fixture-renderer','--model-version','1','--seed','7','--settings-json','{"mode":"fixture"}','--source',f'page-1={sources[0]}','--rendered-output',f'page-1={plate}')
        state=self.w/'state.json';state.write_text(json.dumps({
            'schema_version':'2.0.0','status':'batch_approved','created_at_utc':'2026-08-27T19:00:00+00:00',
            'sample_page':1,'render_plan_path':str(plan.resolve()),'render_plan_sha256':h(plan),
            'production_plan_path':str(production.resolve()),'production_plan_sha256':h(production),
            'sample_style_contract_sha256':hashlib.sha256(json.dumps(contract,sort_keys=True,separators=(',',':')).encode()).hexdigest(),'sample_path':str(sample.resolve()),'sample_sha256':h(sample),
            'sample_plate_path':str(plate.resolve()),'sample_plate_sha256':h(plate),'sample_plate_validation':plate_validation,'renderer_record':{'path':str(receipt.resolve()),'sha256':h(receipt)},
            'sample_registered_at_utc':'2026-08-27T19:01:00+00:00','presented_at_utc':'2026-08-27T19:02:00+00:00',
            'presentation_record':{'mode':'artifact','note':'reviewed','decision_coverage':['ordered-page-briefs','sample-style-contract','sample-scope','finish-qa-delivery'],'plan_decisions_communicated':True,'sample_discussed':True},
            'approved_at_utc':'2026-08-27T19:03:00+00:00','explicit_approval':{'actor':'user','text':'approved'},
            'permitted_render_pages':[2,3,4],'blocked_render_pages':[],'revision_ledger':[]}))
        return plan,state,stage,final
    def test_page_local_revision_preserves_unchanged_and_sample_change_resets_gate(self):
        plan,state,stage,_=self.make_plan_state_stage();changes=self.w/'changes.json';changes.write_text(json.dumps({'changes':[
            {'page':4,'domain':'page-content','operation':'retain_but_simplify','target':'major roads','instruction':'keep fewer wider directions'},
            {'page':4,'domain':'page-content','operation':'preserve_unchanged','target':'high viewpoint','instruction':'retain altitude'}]}))
        out=self.w/'revision.json';run('revision_scope.py','--render-plan',plan,'--state',state,'--staging-manifest',stage,'--changes',changes,'--request-text','roads should be more abstract','--impact','page-local','--output',out)
        scope=json.loads(out.read_text());self.assertEqual(scope['render_scope']['page_numbers'],[4]);self.assertEqual(scope['render_scope']['unchanged_pages'],[1,2,3])
        # fresh state: changing sample page must invalidate instead of emitting a local scope
        plan,state,stage,_=self.make_plan_state_stage();changes.write_text(json.dumps({'changes':[{'page':1,'domain':'page-content','operation':'remove','target':'border','instruction':'remove frame'}]}))
        blocked=run('revision_scope.py','--render-plan',plan,'--state',state,'--staging-manifest',stage,'--changes',changes,'--request-text','remove sample frame','--impact','page-local','--output',out,ok=False)
        self.assertEqual(blocked.returncode,5);self.assertEqual(json.loads(state.read_text())['status'],'gate_invalidated_by_revision')
        # non-local domain cannot be disguised as page-local
        plan,state,stage,_=self.make_plan_state_stage();changes.write_text(json.dumps({'changes':[{'page':4,'domain':'style-reference','operation':'preserve_unchanged','target':'reference technique','instruction':'change shared mark quality'}]}))
        blocked=run('revision_scope.py','--render-plan',plan,'--state',state,'--staging-manifest',stage,'--changes',changes,'--request-text','change the drawing method','--impact','page-local','--output',out,ok=False)
        self.assertEqual(blocked.returncode,5);self.assertEqual(json.loads(state.read_text())['status'],'gate_invalidated_by_revision')
    def test_one_page_batch_scope_is_explicitly_empty_after_approval(self):
        import hashlib
        plan=self.w/'one-plan.json';production=self.w/'one-plan.md';sample=self.w/'sample.png';plate=self.w/'sample-plate.png'
        production.write_text('plan');Image.new('RGBA',(64,96),(0,0,0,0)).save(sample);Image.new('RGBA',(64,96),(0,0,0,0)).save(plate)
        cfg_hash=hashlib.sha256(self.config.read_bytes()).hexdigest();source=self.w/'source.jpg';Image.new('RGB',(8,8),'white').save(source)
        validation_report=self.w/'one-sample-validation.json';run('clean_plate.py','validate','--input',plate,'--config',self.config,'--report',validation_report);plate_validation=json.loads(validation_report.read_text())['analysis']
        receipt=self.w/'one-renderer-receipt.json';run('renderer_receipt.py','register','--output',receipt,'--renderer-kind','local','--model','fixture-renderer','--model-version','1','--seed','7','--settings-json','{"mode":"fixture"}','--source',f'page-1={source}','--rendered-output',f'page-1={plate}')
        plan.write_text(json.dumps({'resolved_config_lock':{'path':str(self.config.resolve()),'sha256':cfg_hash},'style_reference_locks':[],
            'sample_style_contract':{'generated_page_is_style_reference':False},'pages':[{'page':1,'source_path':str(source.resolve()),'source_sha256':hashlib.sha256(source.read_bytes()).hexdigest()}]}))
        state=self.w/'one-state.json';state.write_text(json.dumps({'status':'batch_approved','sample_page':1,'render_plan_path':str(plan.resolve()),
            'render_plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'production_plan_path':str(production.resolve()),
            'production_plan_sha256':hashlib.sha256(production.read_bytes()).hexdigest(),'sample_path':str(sample.resolve()),
            'sample_sha256':hashlib.sha256(sample.read_bytes()).hexdigest(),'sample_plate_path':str(plate.resolve()),
            'sample_plate_sha256':hashlib.sha256(plate.read_bytes()).hexdigest(),'sample_plate_validation':plate_validation,'renderer_record':{'path':str(receipt.resolve()),'sha256':hashlib.sha256(receipt.read_bytes()).hexdigest()},'explicit_approval':{'actor':'user','text':'approved'},'permitted_render_pages':[],'blocked_render_pages':[]}))
        out=self.w/'one-batch.json';run('render_scope.py','--render-plan',plan,'--state',state,'--mode','batch','--output',out)
        self.assertEqual(json.loads(out.read_text())['render_scope']['page_numbers'],[])
    def test_qa_two_dimensions_block_then_verified_package_passes(self):
        plan,state,stage,final=self.make_plan_state_stage()
        plates=self.w/'qa-plates';plates.mkdir();[Image.new('RGBA',(64,96),(0,0,0,0)).save(plates/f'{i:02d}.png') for i in range(1,5)]
        qa=self.w/'qa';run('qa_images.py','--input',final,'--output',qa,'--config',self.config,'--render-plan',plan,'--plates',plates)
        checklist=qa/'review-checklist.json';blocked=run('review_checklist.py','validate','--checklist',checklist,ok=False);self.assertEqual(blocked.returncode,4)
        data=json.loads(checklist.read_text())
        for page in data['page_level_compliance']['pages']:
            for entry in page['checks'].values():entry.update(status='pass',evidence='manual full and phone review')
            page['status']='pass'
        data['page_level_compliance']['status']='pass'
        for entry in data['set_level_cohesion']['checks'].values():entry.update(status='pass',evidence='manual set review')
        data['set_level_cohesion']['status']='pass';checklist.write_text(json.dumps(data))
        run('review_checklist.py','validate','--checklist',checklist)
        plan_data=json.loads(plan.read_text());composition_receipt=self.w/'composition-receipt.json'
        receipt_args=['register','--output',composition_receipt,'--renderer-kind','local','--model','fixture-renderer','--model-version','1','--seed','7','--settings-json','{"mode":"fixture"}']
        plate_entries=[];output_entries=[]
        for page in range(1,5):
            plate=plates/f'{page:02d}.png';source=plan_data['pages'][page-1]['source_path'];out=final/f'{page:02d}.webp'
            receipt_args += ['--source',f'page-{page}={source}','--rendered-output',f'page-{page}={plate}']
            plate_entries.append({'page':page,'path':str(plate.resolve()),'sha256':hashlib.sha256(plate.read_bytes()).hexdigest()})
            output_entries.append({'page':page,'path':str(out.resolve()),'sha256':hashlib.sha256(out.read_bytes()).hexdigest()})
        run('renderer_receipt.py',*receipt_args)
        composition=self.w/'composition-manifest.json';composition.write_text(json.dumps({'schema_version':'1.1.0','deterministic':True,'config_sha256':hashlib.sha256(self.config.read_bytes()).hexdigest(),'render_plan_sha256':hashlib.sha256(plan.read_bytes()).hexdigest(),'renderer_receipt':{'path':str(composition_receipt.resolve()),'sha256':hashlib.sha256(composition_receipt.read_bytes()).hexdigest()},'font':None,'plates':plate_entries,'metadata_policy':{'exif_gps_xmp':'forbidden','verified':True},'outputs':output_entries}))
        z=self.w/'release.zip';manifest=self.w/'release.json';run('package_verified.py','package','--input',final,'--staging-manifest',stage,'--review-checklist',checklist,'--state',state,'--composition-manifest',composition,'--output',z,'--manifest-output',manifest)
        run('package_verified.py','verify','--zip',z,'--manifest',manifest)
        release=json.loads(manifest.read_text())
        self.assertNotIn(str(self.w), json.dumps(release))
        self.assertEqual(release['verification']['composition_manifest_sha256'],hashlib.sha256(composition.read_bytes()).hexdigest())
        composition_data=json.loads(composition.read_text());composition_data['outputs'][0]['sha256']='0'*64;composition.write_text(json.dumps(composition_data))
        blocked=run('package_verified.py','package','--input',final,'--staging-manifest',stage,'--review-checklist',checklist,'--state',state,'--composition-manifest',composition,'--output',self.w/'bad-composition.zip','--manifest-output',self.w/'bad-composition.json',ok=False)
        self.assertEqual(blocked.returncode,4);self.assertIn('composition outputs',blocked.stderr.lower())
        with zipfile.ZipFile(z,'a') as archive:archive.writestr('extra.txt','tamper')
        blocked=run('package_verified.py','verify','--zip',z,'--manifest',manifest,ok=False);self.assertEqual(blocked.returncode,4)

if __name__=='__main__':unittest.main()
