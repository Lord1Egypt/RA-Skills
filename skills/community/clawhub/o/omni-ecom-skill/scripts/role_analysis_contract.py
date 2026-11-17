"""One role question contract; prepares questions, never answers or findings."""
import hashlib
import json

QUESTIONS = {
    'data-analyst': [
        '来源、客户、期间、单位及指标口径是否一致？',
        '数据闸门和禁止输出的结论是什么？',
        '核心指标发生了哪些可比变化？',
        '变化集中在哪些渠道、商品或人群？',
        '异常订单、退款及去重对判断有什么影响？',
        '可支持哪些结论，哪些需要补数或验证？'],
    'platform-ops': [
        '商品贡献、结构与库存有哪些变化？',
        '搜索、推荐和活动流量的效率如何？',
        '店铺转化链路的掉点在哪里？',
        '价格、促销与会员的作用是否有证据？',
        '退款、客服或履约是否影响经营？',
        '应优先做什么，如何验收与停止？'],
    'content-live-growth': [
        '内容、直播和达人资料是否足以分析？',
        '曝光、互动、进店、支付漏斗哪里掉点？',
        '内容或场次差异是否有足够样本？',
        '成交归因与跨平台贡献能否核实？',
        '内容承诺与退款、服务是否存在关联？',
        '最小验证实验、观察窗口和停止条件是什么？'],
    'ad-profit-optimizer': [
        '投放渠道、期间、归因及费用资料是否齐全？',
        'ROAS、净 ROAS 和利润 ROI 哪些可算？',
        '渠道、人群、商品的效率差异是什么？',
        '退款、优惠、佣金和履约成本如何影响边界？',
        '哪些因素最敏感，反证条件是什么？',
        '预算方案是否有依据、审批和停止条件？'],
}

def questions(role, mode='business'):
    if role not in QUESTIONS:
        raise ValueError('analysis_role_invalid')
    if mode not in ('business','mechanism'):
        raise ValueError('analysis_question_mode_invalid')
    titles=QUESTIONS[role] if mode=='business' else [
        '本岗共享输入指纹与任务卡是否一致？', '本岗章节与来源是否正确绑定？',
        '本次客户、运行和版本身份是否一致？', '全量清单及来源范围是否可定位？',
        '本岗正式回传格式和单次通信契约是否明确？', '已有证据能证明什么，哪些真实执行状态尚不能证明？']
    return [{'question_id': role+'-Q'+str(i).zfill(2), 'question': title,
             'status': 'pending', 'answer': '', 'blocker': '', 'evidence_ids': []}
            for i, title in enumerate(titles, 1)]

def contract(role, mode='business'):
    rows = questions(role, mode)
    digest = hashlib.sha256(json.dumps(rows, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
    return {'version': '1', 'role': role, 'mode':mode,'question_ids': [r['question_id'] for r in rows], 'sha256': digest}

def check_questions(role, depth):
    expected = contract(role,depth.get('question_contract',{}).get('mode','business'))
    if depth.get('question_contract') != expected:
        raise ValueError('minimum_analysis_contract_mismatch')
    rows = depth.get('minimum_analysis_set')
    if not isinstance(rows, list) or len(rows) != len(expected['question_ids']):
        raise ValueError('minimum_analysis_questions_missing')
    ids = [r.get('question_id') if isinstance(r, dict) else None for r in rows]
    if len(set(ids)) != len(ids) or set(ids) != set(expected['question_ids']):
        raise ValueError('minimum_analysis_question_identity_invalid')
    titles = {row['question_id']: row['question'] for row in questions(role, expected['mode'])}
    if any(row.get('question') != titles[row['question_id']] for row in rows):
        raise ValueError('minimum_analysis_question_text_changed')

