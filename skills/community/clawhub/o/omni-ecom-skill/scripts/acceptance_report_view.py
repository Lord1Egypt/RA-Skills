"""Clearly labelled no-client test view, preserving every sealed source."""
import copy
import re


def defaults(item):
    if re.search(r'WorkBuddy|TeamCreate|team-bootstrap|launch-manifest|TaskList|TaskUpdate|宿主|bootstrap|账本|运行事件|任务绑定|工具回包|host_runtime', item, re.I):
        return ('host_mechanism', '仅限制所述宿主的建团、派工或原生任务机制核查，不构成客户经营数据缺口。Codex 运行不以 WorkBuddy 凭证为完成前提。',
                '核对对应宿主的真实 TeamCreate/Agent 返回、team-bootstrap.json、launch-manifest.json 及原生任务记录；不在该宿主运行时明确不适用，另跑该宿主验收。')
    if re.search(r'阶段|实际完成|完成凭证|completion|冻结|复核|delivery-review', item, re.I):
        return ('phase_evidence', '截至该专家回传时，所读材料不能证明对应阶段或全团完成；冻结后进度须由当前真实回传及完成凭证另行证明，不能提前报完成。',
                '核对本轮原生阶段任务状态、真实成员回传、冻结清单、独立复核结果和当前完成凭证；保留专家回传时点的原始限制，不沿用旧任务完成状态。')
    return ('business_data', '无法验证该项经营内容，不支持有关经营结论。',
            '原岗未给出具体补证要求；本次机制验收不请求客户业务报表，另行经营分析须先取得新的授权。')


def enrich(package):
    if not package.get('acceptance_only'):
        return
    for row in package.get('metrics', []):
        row.setdefault('metric_units', {}).update(conversion_rate='ratio', uv_value='元/人')
        row['unit_note'] = '内部 conversion_rate 使用比率；对外转化率按数字索引统一显示百分比。'
    gaps = []
    for member in package.get('mechanism_findings', []):
        for raw in member.get('missing_data', []):
            data = raw if isinstance(raw, dict) else {'item': str(raw)}
            item = data.get('item') or data.get('field') or data.get('name') or '；'.join(data.get('missing_fields', [])) or data.get('reason') or str(raw)
            kind, impact, required_source = defaults(str(item))
            requests = [data[k] for k in ('required_source', 'needed_data', 'required_input', 'required_data') if data.get(k)]
            requests = list(dict.fromkeys(str(value) for value in requests))
            if isinstance(raw, str):
                explicit = re.search(r'补数要求[：:]|补数[：:]', raw)
                requests = [raw[explicit.end():].strip()] if explicit else [raw]
            gaps.append({'gap_id': 'G'+str(len(gaps)+1).zfill(3), 'owner_agent': member['agent_id'],
                'item': item, 'gap_kind':data.get('gap_kind') or kind, 'impact': data.get('impact') or data.get('blocker') or impact,
                'required_source': '；'.join(requests) if requests else required_source,
                'raw_missing_data': copy.deepcopy(raw), 'source_kind': 'sealed_member_handoff'})
    package['missing_data'] = gaps
    package['data_gate']['missing_data'] = copy.deepcopy(gaps)
    package['chapter_plan_source_snapshot'] = copy.deepcopy(package.get('chapter_plan', {}))
    for chapter in package.get('chapter_plan', {}).get('chapters', []):
        if chapter.get('chapter_id') == 'CH05' or '缺口' in str(chapter.get('title', '')):
            chapter['data_gaps'] = copy.deepcopy(gaps)
    package['chapter_plan_enrichment'] = {
        'kind': 'report_view_gap_backfill_from_sealed_handoffs', 'initial_plan_file_modified': False,
        'note': '初始计划原件及专家确认的输入快照不变；报告中的计划视图回填本轮封存交接件的真实缺口。补数要求是请求，不是已取得的数据。',
        'gap_count': len(gaps)}


def cell(value):
    return str(value if value is not None else '未知').replace('|', '\\|').replace('\n', ' ')


def markdown(package):
    lines = ['# '+package['title'], '',
        '- 专家团版本：'+package['team_version_label'],
        '- 上一版本：'+str(package.get('team_previous_version')),
        '- 报告修订：'+package['report_revision'], '- 运行：'+package['run_id'],
        '- 客户范围：'+package['client_scope'], '- 期间：'+str(package['period']),
        '- 数据闸门：'+package['gate_status']+'（仅机制）；经营范围：BLOCKED',
        '- 状态：'+package['status']+'；待独立复核，未完成交付', '',
        '> '+package['acceptance_notice'], '', '本次版本变更：', '']
    lines.extend('- '+str(item) for item in package.get('team_version_changes', []))
    lines.extend(['', '## 零、数据概览与覆盖', '', '### 报表清单', '',
        '| 报表编号 | 文件 | 类型 | 期间 | 可分析性 |', '| --- | --- | --- | --- | --- |'])
    for item in package.get('report_inventory', {}).get('reports', []):
        period = item.get('time_scope', {})
        period = period.get('note') or str(period.get('start'))+' ~ '+str(period.get('end'))
        lines.append('| '+' | '.join(cell(v) for v in [item.get('report_id'),item.get('file_name'),item.get('report_type_label'),period,item.get('verdict')])+' |')
    lines.extend(['', '### 归类结果', '', '| 归类编号 | 业务域 | 名称 | 包含报表 | 状态 |', '| --- | --- | --- | --- | --- |'])
    for item in package.get('report_clusters', {}).get('clusters', []):
        lines.append('| '+' | '.join(cell(v) for v in [item.get('cluster_id'),item.get('domain'),item.get('label'),', '.join(item.get('members', [])),item.get('sufficiency')])+' |')
    lines.extend(['', '### 章节与报表映射', '', '| 章节 | 标题 | 负责人 | 来源报表 |', '| --- | --- | --- | --- |'])
    for item in package.get('chapter_plan', {}).get('chapters', []):
        lines.append('| '+' | '.join(cell(v) for v in [item.get('chapter_id'),item.get('title'),item.get('owner_agent'),', '.join(item.get('source_report_ids', [])) or '无直接报表'])+' |')
    lines.extend(['', '## 一、核心指标速览', '', '以下仅为固定测试值，不是客户经营表现；转化率对外统一为百分比。', '',
        '| 期间 | 指标 | 数值 | 单位 | Claim ID |', '| --- | --- | ---: | --- | --- |'])
    for item in package['claim_ledger'].get('claims', []):
        lines.append('| '+' | '.join(cell(v) for v in [item.get('period') or package['period'],item.get('metric'),item.get('value'),item.get('unit'),item.get('claim_id')])+' |')
    lines.extend(['', '## 二、关键图表', '', '六张内嵌图表见 report.pdf：固定测试销售额、固定测试人次、固定测试转化率，以及机制事实、数据缺口、协作状态。过程图不能替代来源指标图。', '',
                  '## 三、事实、判断与限制', ''])
    for fact in package.get('facts', []):
        lines.append('- '+str(fact.get('claim', ''))+'（证据：'+', '.join(fact.get('evidence_ids', []))+'）')
    lines.extend(['', '没有客户经营判断、因果结论或预算建议。', '', '## 四、优先行动', '',
                  '无经营执行行动；补数要求见第七节，不代表已取得数据或已执行。', '', '## 五、专家协作与版本凭证', '',
                  '| 专家 | 状态 | 真实子任务 | 贡献摘要 | 封存交接件 |', '| --- | --- | --- | --- | --- |'])
    for item in package.get('expert_participation', []):
        state = '待冻结后独立复核' if item.get('agent_id') == 'delivery-review' else item.get('participation_status')
        lines.append('| '+' | '.join(cell(v) for v in [item.get('agent_id'),state,', '.join(item.get('agent_task_ids', [])) or '主任务/待启动',item.get('contribution_summary'),', '.join(item.get('handoff_files', []))])+' |')
    for item in package.get('mechanism_findings', []):
        lines.extend(['', '### '+item['agent_id']+' 独立机制核查', '', '岗位闸门：'+item['gate_status'], ''])
        for fact in item['facts']:
            lines.append('- '+str(fact.get('claim', ''))+'（证据：'+', '.join(fact.get('evidence_ids', []))+'）')
    quality = package.get('collaboration_quality', {})
    lines.extend(['', '### 协作质量记录', '', '共享基线 SHA256：'+str(quality.get('baseline_sha256')), '深度检查：'+str(quality.get('depth_guard_status')),
        '冲突扫描：'+str(quality.get('conflict_scan_status')), '', '## 六、数字来源与复算索引', '',
        '| Claim ID | 指标 | 数值 | 单位 | 状态 | 来源字段 | 公式 |', '| --- | --- | ---: | --- | --- | --- | --- |'])
    for item in package['claim_ledger'].get('claims', []):
        source = item.get('source_ref', {})
        lines.append('| '+' | '.join(cell(v) for v in [item.get('claim_id'),item.get('metric'),item.get('value'),item.get('unit'),item.get('status'),'/'.join(str(source.get(k) or '') for k in ('source_file','sheet','range','field') if source.get(k)),item.get('formula', {}).get('expression') or '—'])+' |')
    lines.extend(['', '## 七、验收缺口与限制（CH05）', '', package['chapter_plan_enrichment']['note'], '',
        '| 缺口编号 | 岗位 | 缺口项目 | 对结论的影响 | 补数要求 |', '| --- | --- | --- | --- | --- |'])
    for gap in package['missing_data']:
        lines.append('| '+' | '.join(cell(gap[k]) for k in ('gap_id','owner_agent','item','impact','required_source'))+' |')
    lines.extend(['', '### 来源索引', ''])
    lines.extend('- '+cell(item.get('type'))+': '+cell(item.get('source'))+'；SHA256='+cell(item.get('sha256')) for item in package.get('sources', []))
    lines.extend(['', '---', '候选版本仅可记录 candidate_pipeline_complete，以 candidate-acceptance-receipt.json 为依据，不构成正式交付。' if '-candidate.' in package['team_version'] else '本稿尚待独立复核；只有当前 completion-receipt.json 证明完成后才可报告本轮安装验收完成，仍不证明客户经营结论。', ''])
    return '\n'.join(lines)
