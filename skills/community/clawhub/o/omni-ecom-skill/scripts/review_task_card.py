"""Prepare blank reviewer format for a frozen business or acceptance manifest."""
import json
from pathlib import Path
from artifact_contract import native_receipt_identity
from review_guard import validate_manifest, changed_entries


def add_format(card, manifest, plugin_dir):
    card['review_analysis_file']=str(Path(card['raw_review_result']).with_suffix('.analysis.json'))
    card['review_navigation'] = {
        'status': 'prepared_not_reviewed', 'review_decision_generated': False,
        'manifest_path': card.get('manifest'),
        'artifact_count': len(manifest['artifacts']), 'source_count': len(manifest.get('sources', [])),
        'check_order': [
            '先核对全部冻结文件指纹；用 manifest 的路径直接定位，避免反复找目录。',
            '核对报告和章节覆盖、指标口径与数字索引；有问题明确列出问题所在文件和字段。',
            '核对五岗实际任务身份及四份交接件、冲突与裁决；不要把格式模板当分析结果。',
            '逐页看实际 PDF，检查图表、单位、摘要、缺口和排版；读表结果不能代替视觉检查。',
            '每个独立问题只写一条 findings，关联所有受影响位置；必改项写入 required_changes。',
        ],
    }
    card['raw_review_result_template'] = {
        **card['raw_result_identity'], 'return_status': 'completed', 'returned_at': '',
        'review_status': 'rejected', 'reviewed_manifest_sha256': manifest['manifest_sha256'],
        'reviewed_artifacts': [{'file': item['file'], 'sha256': item['sha256']} for item in manifest['artifacts']],
        'findings': [], 'required_changes': [], 'contribution_summary': '',
    }
    card['rules'].extend([
        '先运行 input_verification_command，一次核对全部冻结文件指纹；它只证明文件一致，不替代你的独立业务、覆盖、协作和逐页视觉复核。',
        'raw_review_result_template 是空白格式，默认 rejected；亲自检查 manifest 所列材料和 PDF 页面后填写真实结论、问题、必改项、时间和贡献。格式不是通过证据。',
        '直接使用模板和 return_command，无需查目录、读脚本源码或猜字段；发现问题按 conditional_pass/rejected 回传，不改冻结文件。',
    ])
    card['review_analysis_template']={'review_status':'rejected','findings':[],
        'required_changes':[],'contribution_summary':''}
    card['rules'].append('优先亲自填写 review_analysis_template 并写 review_analysis_file，再执行 return_command；程序仅装配本人的实际复核结论与固定身份、指纹，不替你决定 passed。无需抄写全量固定元数据。')
    card['rules'].append('回执成功后，WorkBuddy 原样使用返回的 native_message_parameters 发送一次 SendMessage；Codex 向真实父代理发送返回的 short_message。不要把贡献摘要、数字复算或逐页复核内容再写一遍到聊天；完整记录保留在独立复核原件。然后结束。')
    from report_presentation import review_index
    reports=[r for r in manifest['artifacts'] if r['file'].endswith('report.json')]
    if reports:
        report=json.loads(Path(reports[0]['path']).read_text(encoding='utf-8-sig'))
        card['review_navigation']['report_index']=review_index(report)
        pdfs=[r for r in manifest['artifacts'] if r['file'].endswith('pdf-delivery.json')]
        if pdfs:
            pdf=json.loads(Path(pdfs[0]['path']).read_text(encoding='utf-8-sig'))
            card['review_navigation']['pdf_pages']=pdf['page_count']
            if pdf.get('render_directory'):
                card['review_navigation']['page_files']=[str(Path(pdfs[0]['path']).parent/pdf['render_directory']/r['render']) for r in pdf.get('rendered_pages',[])]
            else:
                card['review_navigation']['page_names']=[r['render'] for r in pdf.get('rendered_pages',[])]
    card['review_navigation']['files']=[{'file':r['file'],'path':r['path']} for r in manifest['artifacts']+manifest.get('sources',[])]
    return card


def prepare(manifest_path, plugin_dir, host, attempt='a1'):
    manifest_path = Path(manifest_path).resolve(); plugin_dir = Path(plugin_dir).resolve()
    manifest = json.loads(manifest_path.read_text(encoding='utf-8-sig'))
    validate_manifest(manifest)
    if any(changed_entries(manifest)): raise ValueError('review_frozen_files_changed')
    if host not in {'workbuddy', 'codex'}: raise ValueError('review_host_invalid')
    # This entry creates the first review only. Retry authorization stays in runtime.
    if attempt != 'a1': raise ValueError('review_retry_requires_runtime_authorization')
    run_dir = manifest_path.parent
    revision = manifest['report_revision']
    review_id = 'delivery-review-'+revision.lower()+'-'+attempt
    card_path = run_dir/'task-cards/review'/(review_id+'.json')
    raw = run_dir/'review'/revision/(review_id+'.return.json')
    ret = run_dir/'agent-returns/delivery-review'/(revision.lower()+'-'+attempt+'.return.json')
    if any(p.exists() for p in (card_path, raw, ret)): raise ValueError('review_attempt_already_exists')
    card = dict(schema_version='2.0', artifact_type='delivery_review_task_card', immutable_after_launch=True,
        run_id=manifest['run_id'], client_scope=manifest['client_scope'], team_version=manifest['team_version'], host=host,
        agent_id='delivery-review', attempt_id=review_id, report_revision=revision,
        raw_result_identity={**native_receipt_identity('review_result',manifest['team_version']),
            'run_id':manifest['run_id'],'client_scope':manifest['client_scope'],'agent_id':'delivery-review',
            'agent_version':manifest['team_version'],'review_attempt_id':review_id,'report_revision':revision},
        manifest=str(manifest_path), manifest_sha256=manifest['manifest_sha256'], raw_review_result=str(raw), return_file=str(ret),
        raw_result_schema=str(plugin_dir/'schemas/review-result.schema.json'),
        return_command=f'python -B "{plugin_dir / "scripts/write_delivery_review_return.py"}" --task-card "{card_path}"',
        input_verification_command=f'python -B "{plugin_dir / "scripts/check_review_inputs.py"}" --task-card "{card_path}"',
        rules=['独立检查全部冻结材料和图表 PDF，不能改稿；完成后执行固定 return_command，只向 team-lead 回传一次并结束。'])
    add_format(card,manifest,plugin_dir)
    card_path.parent.mkdir(parents=True, exist_ok=True)
    with card_path.open('x',encoding='utf-8') as stream: json.dump(card,stream,ensure_ascii=False,indent=2)
    return dict(status='delivery_review_ready',card_path=str(card_path),review_attempt_id=review_id,
        launch_prompt=f'读取并执行复核任务卡：{card_path}。独立复核后只回传一次并结束。',return_file=str(ret))
