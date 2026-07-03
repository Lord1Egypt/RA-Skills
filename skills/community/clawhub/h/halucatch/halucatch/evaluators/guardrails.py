"""护栏评估：检查安全边界、禁止声明、误用风险等。"""

import re
from ..config import MESSAGES
from .rules import _is_tool_skill


def check_guardrails(info, skill_type='code-engineered'):
    """护栏评估：检查解读规则是否到位，防止 AI 自信地输出错误结论。
    code-engineered 分析型: 全 8 项（置信度/数据来源/时效性 全查）;
    code-engineered 工具库型: 精简 5 项（跳过置信度/数据来源/时效性）;
    methodology 型: 精简 5 项（同上）。"""
    md = info['skill_md']
    issues = []

    if not md:
        return {'rating': '🟡 无 SKILL.md', 'issues': [('🟡 未找到 SKILL.md，无法评估护栏', 'skip')], 'score': '-'}

    # 代码工程型拆两档：工具库 vs 分析型
    is_tool = skill_type == 'code-engineered' and _is_tool_skill(info)

    total = 8
    score = 0

    # 1) 输出格式明确
    if re.search(r'(```|json|markdown|table|表格|图表|输出格式|export)', md):
        issues.append(('✅ 明确了输出格式', 'pass'))
        score += 1
    else:
        issues.append(('🟠 未定义输出格式', 'warn'))

    # 2) 禁令/护栏 — 跨语言信号（否定词/大写警告/中文禁止）
    status, text = _prohibition_signal(md)
    issues.append((text, status))
    if status == 'pass':
        score += 1

    # 3) 验证/自检
    if re.search(r'(验证|检查|确认|validate|verify|check|自检)', md):
        issues.append(('✅ 包含验证/自检步骤', 'pass'))
        score += 1
    else:
        issues.append(('🟠 缺少输出验证/自检要求', 'warn'))

    # 4) 置信度（分析型代码工程专属，工具库/方法论跳过）
    if skill_type == 'code-engineered' and not is_tool:
        if re.search(r'(置信|可信度|confidence|uncertainty|reliability|error\s+margin|不确定|风险)', md):
            issues.append(('✅ 涉及置信度/风险评估', 'pass'))
            score += 1
        else:
            issues.append(('🟡 未要求置信度声明', 'info'))
    elif is_tool:
        issues.append(('🟡 工具库型，置信度检查跳过（文件格式类 Skill 不涉统计推断）', 'skip'))
        total -= 1
    else:
        issues.append(('🟡 纯方法论型，置信度检查跳过（无数据操作，不适用置信度评估）', 'skip'))
        total -= 1

    # 5) 数据来源限制（分析型代码工程专属，工具库/方法论跳过）
    if skill_type == 'code-engineered' and not is_tool:
        if re.search(r'(数据.*来源|数据.*范围|数据.*限制|仅.*数据|不包括|data\s+(source|scope)|limited\s+to|coverage)', md):
            issues.append(('✅ 声明了数据来源/范围限制', 'pass'))
            score += 1
        else:
            issues.append(('🟡 未声明数据来源限制', 'info'))
    elif is_tool:
        issues.append(('🟡 工具库型，数据来源检查跳过（不声明自有数据范围）', 'skip'))
        total -= 1
    else:
        issues.append(('🟡 纯方法论型，数据来源检查跳过（不处理外部数据）', 'skip'))
        total -= 1

    # 6) 错误回退
    if re.search(r'(错误|失败|异常|无法|不可用|回退|fallback)', md):
        issues.append(('✅ 定义了错误处理/回退策略', 'pass'))
        score += 1
    else:
        issues.append(('🟠 未定义错误回退策略', 'warn'))

    # 7) 时效性（分析型代码工程专属，工具库/方法论跳过）
    if skill_type == 'code-engineered' and not is_tool:
        if re.search(r'(截至|更新时间|有效期|时效|T\+|交易日|截止|as\s+of|last\s+updated|valid\s+until|expir)', md):
            issues.append(('✅ 声明了数据时效性', 'pass'))
            score += 1
        else:
            issues.append(('🟡 未声明数据时效性约束', 'info'))
    elif is_tool:
        issues.append(('🟡 工具库型，时效性检查跳过（不依赖特定时间窗口的数据）', 'skip'))
        total -= 1
    else:
        issues.append(('🟡 纯方法论型，时效性检查跳过（不依赖时变数据）', 'skip'))
        total -= 1

    # 8) 前提假设
    if re.search(r'(假设|前提|前置|前提条件)', md):
        issues.append(('✅ 声明了前提假设', 'pass'))
        score += 1
    else:
        issues.append(('🟡 未声明前提假设', 'info'))

    pct = score / max(total, 1)
    if pct >= 0.8:
        rating = '🟢 到位'
    elif pct >= 0.5:
        rating = '🟡 缺项'
    else:
        rating = '🔴 薄弱'

    return {'rating': rating, 'issues': issues, 'score': f'{score}/{total}'}


def _branch_density(md):
    """跨语言异常分支覆盖信号：不看具体用词，看结构化密度。"""
    checklist = len(re.findall(r'^\s*[-*]\s', md, re.MULTILINE))
    warn_icons = len(re.findall(r'[⚠️🚨❌✅🔴⛔🟡🟠🟢]', md))
    tables = md.count('|---')
    checkbox = len(re.findall(r'\[ \]|\[x\]', md, re.IGNORECASE))
    signal = checklist + warn_icons * 2 + tables * 3 + checkbox * 2
    if signal >= 5:
        return ('pass', f'✅ 检测到条件分支信号（清单 {checklist} 项 / 图标 {warn_icons} / 表格 {tables}）')
    else:
        return ('warn', '🟡 未检测到足够的条件分支信号，建议 AI 人工审查')


def _prohibition_signal(md):
    """跨语言禁止/护栏声明信号：否定词 + 大写警告词 + 中文禁止词。"""
    negations = len(re.findall(
        r'\b(?:never|not|no|don\'?t|REJECT|DENY|BLOCK|SHALL\s+NOT)\b',
        md, re.IGNORECASE
    ))
    caps_warnings = len(re.findall(r'[A-Z]{5,}', md))
    zh_prohibition = len(re.findall(r'(不要|不能|禁止|切勿|严禁)', md))
    red_flags = len(re.findall(r'RED\s+FLAG|🚨|⛔', md, re.IGNORECASE))
    signal = negations * 2 + caps_warnings + zh_prohibition * 2 + red_flags * 3
    if signal >= 3:
        return ('pass', f'✅ 检测到禁止/护栏声明（否定词 {negations} / 中文禁止 {zh_prohibition}）')
    else:
        return ('warn', '🟡 未检测到明确的禁止操作声明')
