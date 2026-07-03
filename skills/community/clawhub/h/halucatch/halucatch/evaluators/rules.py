"""规则评估：检查口径定义、边界条件、模糊词汇、自洽性等。"""

import re
from ..config import MESSAGES


def check_rules(info):
    """规则评估：检查 SKILL.md 中的业务规则是否明确、无歧义。"""
    md = info['skill_md']
    issues = []

    if not md:
        return {'rating': '🟡 无 SKILL.md', 'issues': [('🟡 未找到 SKILL.md，无法评估规则', 'skip')], 'score': '-'}

    total = 6
    score = 0

    # 1) 分类歧义 — 查找模糊词汇
    fuzzy_words = ['一般', '大概', '酌情', '适当', '差不多', '基本上', '通常', '大致', '左右']
    found_fuzzy = [w for w in fuzzy_words if w in md]
    if found_fuzzy:
        issues.append((f'🟠 存在模糊表述: {found_fuzzy[:3]}', 'warn'))
    else:
        issues.append(('✅ 未检测到模糊词汇', 'pass'))
        score += 1

    # 2) 边界/数值约束
    if re.search(r'(最小|最大|范围|不低于|不超过|>=|<=)', md):
        issues.append(('✅ 定义了数值边界/范围', 'pass'))
        score += 1
    else:
        issues.append(('🟡 未检测到明确的数值边界约束', 'warn'))

    # 3) 公式/计算明确性
    if re.search(r'([+\-*/^]|公式|计算|sum|avg|mean)', md):
        issues.append(('✅ 包含计算/公式说明', 'pass'))
        score += 1
    else:
        issues.append(('🟡 未检测到计算公式', 'info'))

    # 4) 单位一致性
    mult_units = re.findall(r'(元|万元|亿|%|百分比|千分比|bps)', md)
    if len(set(mult_units)) > 2:
        issues.append((f'🟠 多单位混用: {list(set(mult_units))}', 'warn'))
    else:
        issues.append(('✅ 单位使用一致', 'pass'))
        score += 1

    # 5) 异常分支覆盖
    if re.search(r'(如果.*不|若.*不|错误|异常|失败|缺失|为空)', md):
        issues.append(('✅ 有异常分支处理', 'pass'))
        score += 1
    else:
        issues.append(('🟠 缺少异常值/失败场景处理说明', 'warn'))

    # 6) 默认值声明
    if re.search(r'(默认|缺省|default|fallback)', md):
        issues.append(('✅ 声明了默认值/回退策略', 'pass'))
        score += 1
    else:
        issues.append(('🟡 未声明默认值策略 → 建议在 SKILL.md 中声明 fallback 行为（如「缺省使用最近 30 天数据」）', 'warn'))

    pct = score / max(total, 1)
    if pct >= 0.8:
        rating = '🟢 明确'
    elif pct >= 0.4:
        rating = '🟡 有歧义'
    else:
        rating = '🔴 歧义较多'

    return {'rating': rating, 'issues': issues, 'score': f'{score}/{total}'}


def _is_tool_skill(info):
    """工具库型 Skill：专注文件操作/格式转换，不做数据分析。"""
    md = info.get('skill_md', '')
    tool_signals = [
        'create', 'edit', 'convert', 'merge', 'split',
        'spreadsheet', 'workbook', 'presentation',
        'format', 'template', 'validate',
    ]
    analysis_signals = [
        'analyze', 'analysis', '计算', '统计', '分析',
        'visualize', 'report', 'insight',
        'chart', 'graph', 'forecast', 'trend',
    ]
    tool_count = sum(1 for s in tool_signals if s in md.lower())
    analysis_count = sum(1 for s in analysis_signals if s in md.lower())
    return tool_count > analysis_count
