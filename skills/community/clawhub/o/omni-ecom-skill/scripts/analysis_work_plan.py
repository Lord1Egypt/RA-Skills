"""Describe responsibility and source routing without generating expert findings."""
from pathlib import Path
from task_input_projection import report_index
ROLES = ('data-analyst', 'platform-ops', 'content-live-growth', 'ad-profit-optimizer')
RESPONSIBILITY = {
    'data-analyst': '共享指标口径、总体变化与异常拆解；给出证据冲突，团长负责最终裁决。',
    'platform-ops': '商品、搜索推荐、活动会员和店铺转化；引用共享总览，不重写全店经营摘要。',
    'content-live-growth': '内容、直播、达人及其转化链路；按现有数据核查，不扩写通用运营教程。',
    'ad-profit-optimizer': '付费渠道、费用归因和利润边界；缺成本时逐项说明限制，不推算缺失费用。',
}


def published_cards(attempt_dir, role, attempt):
    """Exclude in-progress staging directories from preparation and progress views."""
    root = Path(attempt_dir)
    pattern = role+'-a1.json' if attempt == 'a1' else 'batch-*/'+role+'-a2.json'
    return [p for p in root.glob(pattern) if (p.parent/'launch-manifest.json').is_file()]


def plan(role, chapters, inventory):
    if role not in ROLES:
        raise ValueError('work_plan_role_invalid')
    reports = inventory.get('reports', [])
    index = {r['report_id']: r for r in reports if isinstance(r, dict) and r.get('report_id')}
    if len(index) != len(reports):
        raise ValueError('work_plan_report_identity_invalid')
    owned = [c for c in chapters if c.get('owner_agent') == role]
    owned_ids = list(dict.fromkeys(rid for c in owned for rid in c.get('source_report_ids', [])))
    if set(owned_ids) - set(index):
        raise ValueError('work_plan_source_not_in_inventory')
    return {
        'status': 'assigned_not_executed', 'expert_findings_generated': False,
        'responsibility': RESPONSIBILITY[role],
        'owned_chapter_ids': [c.get('chapter_id') for c in owned],
        'primary_sources': [report_index(index[rid]) for rid in owned_ids],
        'shared_source_ids': [rid for rid in owned_ids if any(
            rid in c.get('source_report_ids', []) and c.get('owner_agent') != role for c in chapters)],
        'all_inventory_report_ids': list(index),
        'coverage_requirement': '逐个完成所属章节的来源与最小分析集；必要的跨章节反证可以查全清单。来源路由不裁剪授权资料，也不替代全量覆盖检查。',
        'writing_requirement': '每项独立发现保留事实、证据、限制和本岗判断；同一证据只登记一次并用 evidence_ids 引用。不要在事实、风险、贡献摘要之间反复复制全文。完整发现没有数量上限。',
        'missing_data_requirement': '缺数据时完成可核查部分，并逐项写明缺字段、影响和补数要求；按实际深度降级。不反复推演不可回答的问题。',
    }
