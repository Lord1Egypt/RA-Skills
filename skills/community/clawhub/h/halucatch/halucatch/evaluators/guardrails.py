"""护栏评估：检查安全边界、禁止声明、误用风险等。"""

import re

from .rules import _is_tool_skill

# 渲染函数名前缀：用于兜底检测 Python 代码中的输出生成函数
_RENDER_FN_PREFIXES = ('render_', 'build_', 'generate_', 'output_', 'export_', 'compile_')
_TEMPLATE_EXTS = frozenset({'.html', '.htm', '.tpl', '.j2', '.jinja2', '.hbs', '.mustache', '.liquid', '.tex'})
_TEMPLATE_SYNTAX = re.compile(r'\{\{|\{%|<%=|%>')


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

    total = 11
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

    # 9) 错误上报 — 出错后是否要求告知用户（非仅内部回退）
    if re.search(r'(告知|通知|报告.*错误|错误.*报告|遇到.*告知|出错.*告知|report\s+.*(?:error|back|issue)|inform\s+.*user|notify|停止.*告知)', md):
        issues.append(('✅ 要求向用户上报错误', 'pass'))
        score += 1
    else:
        issues.append(('🟠 未要求向用户告知错误', 'warn'))

    # 10) 操作确认 — 是否要求先确认再执行破坏性操作
    if re.search(r'(先.*确认|经.*同意|确认.*再.*执行|确认后.*操作|征得.*同意|before\s+.*proceed|proceed\s+.*confir|'
                 r'ask\s+.*before|confirm\s+.*before|先.*检查.*再|请确认.*是否)', md):
        issues.append(('✅ 要求操作前确认', 'pass'))
        score += 1
    else:
        issues.append(('🟠 未要求操作前确认', 'warn'))

    # 11) 输出确定性 — 扫描模板文件中的模板引擎语法
    tpl_status, tpl_text = _check_output_determinism(info)
    issues.append((tpl_text, tpl_status))
    if tpl_status == 'pass':
        score += 1

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


def _check_output_determinism(info):
    """检测输出确定性：两级信号，命中任一级即 pass。

    一级（模板文件）：在 info['files'] 中按后缀筛选候选文件，
    打开读取内容，检测 Jinja2/Handlebars/ERB 等模板引擎语法
    （{{ }} / {% %} / <%= %>）。模板 = 固定渲染管线 = 高置信度。

    二级（渲染函数）：无模板时，扫描 info['py'] 中 Python 函数定义，
    查找 render_/build_/generate_/output_/export_/compile_ 前缀。
    命中说明有代码在管理输出生成。

    已知风险：
    - 仅扫描 Python 代码（info['py']），JS/Go/Shell 中的渲染逻辑会漏掉。
    - 函数名匹配依赖命名约定，AI 可能用任意名称生成输出（如 make_report）。
    - 无直接渲染管线时，输出仍可能经 f-string 拼接或 LLM 结构化指令生成，
      这些模式当前无法可靠检测。
    - 后续方向：跨语言代码扫描、AST 级输出调用链分析。

    Returns (status, text)，status 为 'pass' | 'warn'。
    """
    # 一级：模板文件检测
    candidates = [f for f in info.get('files', [])
                  if f['ext'] in _TEMPLATE_EXTS
                  and not f.get('is_test')
                  and f['size'] < 1024 * 1024]

    found_tpl = []
    if candidates:
        for f in candidates:
            try:
                with open(f['path'], 'r', encoding='utf-8', errors='backslashreplace') as fh:
                    content = fh.read()
                if _TEMPLATE_SYNTAX.search(content):
                    found_tpl.append(f['rel_path'])
            except OSError:
                pass

    if found_tpl:
        first = found_tpl[0]
        tail = ' 等' if len(found_tpl) > 1 else ''
        return ('pass', f'✅ 发现 {len(found_tpl)} 个模板文件（{first}{tail}），输出可复现')

    # 二级：Python 渲染函数名兜底
    py = info.get('py')
    if py:
        for prefix in _RENDER_FN_PREFIXES:
            if f'def {prefix}' in py:
                return ('pass', f'✅ 发现渲染函数 def {prefix}...，输出有代码管')

    return ('warn', '🟠 未发现模板或渲染函数，输出可能由 LLM 自由生成')
