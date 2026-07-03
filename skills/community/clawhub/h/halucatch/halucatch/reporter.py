"""HaluCatch 报告生成器：生成专业版、标准版、AI 行动版三份报告。"""

import re
import os
from datetime import date
from .config import MESSAGES
from .classifier import classify_skill


def generate_report(info, results, output_dir=None, lang='zh-CN'):
    """生成审查报告三版本（支持中英文）。"""
    msg = MESSAGES[lang]
    skill_name = 'Unknown'
    if info['skill_md']:
        m = re.search(r'name:\s*(.+)', info['skill_md'])
        if m:
            skill_name = m.group(1).strip()

    today = date.today().isoformat()
    skill_type = classify_skill(info)

    # 评级
    f = results['foundation']
    c = results['code']
    r = results['rules']
    g = results['guardrails']

    # 摘要
    all_items = f['issues'] + c['issues'] + r['issues'] + g['issues']
    issues = [i for i in all_items if i[1] in ['fail', 'warn']]
    infos = [i for i in all_items if i[1] == 'info']
    if not issues and not infos:
        summary = msg['summary_no_risk']
    elif not issues:
        summary = msg['summary_no_block'].format(count=len(infos))
    else:
        critical = sum(1 for i in issues if i[1] == 'fail')
        warnings = sum(1 for i in issues if i[1] == 'warn')
        summary = msg['summary_has_risk'].format(critical=critical, warnings=warnings)
        if infos:
            summary += msg['summary_needs_judgment'].format(count=len(infos))

    # 议题文本
    def fmt_issues(iss):
        lines = []
        for text, status in iss:
            lines.append(f'- {text}')
        return '\n'.join(lines) if lines else '- ' + msg['none']

    f_rating = f['rating']
    f_score = f['score']
    c_rating = c['rating']
    c_score = c['score']
    r_rating = r['rating']
    r_score = r['score']
    g_rating = g['rating']
    g_score = g['score']
    fi = fmt_issues(f['issues'])
    ci = fmt_issues(c['issues'])
    ri = fmt_issues(r['issues'])
    gi = fmt_issues(g['issues'])
    sp = info.get('skill_md_path', '')

    # 专业版
    self_check_passed = all(k in results for k in ['foundation', 'code', 'rules', 'guardrails'])
    self_check_msg = msg['self_check_pass'] if self_check_passed else msg['self_check_warn']

    report = f"""# {msg['report_title']} — {skill_name}

**{msg['date']}**: {today}
**{msg['skill_type']}**: {skill_type}
**{msg['file']}**: {sp}

---

## 📌 TL;DR

{summary}

---

## 🎯 {msg['core_conclusions']}

| {msg['dimension']} | {msg['rating']} | {msg['score']} |
|------|------|------|
| 🏗️ {msg['foundation']} | {f_rating} | {f_score} |
| 🤖 {msg['code']} | {c_rating} | {c_score} |
| 📝 {msg['rules']} | {r_rating} | {r_score} |
| 🛡️ {msg['guardrails']} | {g_rating} | {g_score} |

---

## 🔍 {msg['findings']}

### 🏗️ {msg['foundation']}
{fi}

### 🤖 {msg['code']}
{ci}

### 📝 {msg['rules']}
{ri}

### 🛡️ {msg['guardrails']}
{gi}

---

> {msg['report_footer']} {self_check_msg}
"""

    # 标准版 — 附带语境解释，优化为非技术用户的可读布局
    context_map = {
        '硬编码路径': '脚本里写死了某个人的电脑路径，换台机器就跑不了',
        '裸 except': '异常被静默吞掉，出错时没有任何提示，很难排查',
        'skiprows': '数据格式跟预期不一样时，强行跳过行会导致数据错位',
        '自动发现': '没有自动发现文件的机制，每次都得手动指定文件',
        '未检测到异常分支': '遇到意外情况时，AI 不知道该怎么做，可能给出错误结果',
        '缺少输出': '没说输出长什么样，不同 AI 可能给出格式完全不同的结果',
        '缺少结构化步骤': '指令像流水账，AI 可能跳过关键步骤或顺序混乱',
        '缺少示例': '没有例子，AI 只能靠猜，容易理解偏差',
        '缺少验证': '没有检查步骤，AI 可能自信地输出错误内容不做验证',
        '未声明前提假设': '没说明在什么条件下这个 Skill 才能正常工作',
        '未定义错误回退': '执行失败时没有备用方案，AI 会卡住',
        '未声明数据来源限制': '没说明数据从哪里来、覆盖什么范围，不同 AI 可能用不同数据源，结果不可比',
        '未要求置信度声明': '没要求 AI 标注对结论有多大把握，容易把不确定的事说得很肯定',
        '引用.*不存在的文件': '说明书写了要用某个文件，但文件夹里没有——大概率是文件名写错了或忘了放',
        '除零风险': '代码里直接做了除法但没有检查分母会不会是零——万一分母为零程序就崩了',
        '路径拼接': '用加号拼接文件路径，换台电脑可能就找不到文件——建议用专业的路径拼接方法',
        '静默覆盖': '打开文件直接往里面写内容，会把原来的内容悄悄盖掉不留备份',
        '超时缺失': '发网络请求没设超时时间——万一网络卡了会一直等到天荒地老',
        '条件分支信号': '说明书写了不同情况下该怎么处理，考虑得比较周全',
        '禁止/护栏声明': '说明书写了 AI 不能做什么事，有一定的安全底线',
        '检查跳过': '这项检查跟这个 Skill 不沾边，跳过不影响评分',
        '置信度检查跳过': '不涉及数据分析和统计推断，不需要考虑置信度',
        '数据来源检查跳过': '不处理外部数据，不需要声明数据来源',
        '时效性检查跳过': '不依赖时变数据，不需要声明数据时效性',
        '有固化': '有独立的程序来跑核心任务，不是全靠 AI 即兴发挥',
        '多单位混用': '说明里同时用了不同的计量单位，容易让 AI 混淆',
        '嵌入代码': '程序文件数量偏多，AI 要看很多文件才可能复现',
        '检测到.*测试': '有测试代码，说明作者管得住代码质量',
        '未检测到常见篡改点': '代码里没有除零、裸异常等常见坑',
    }
    
    # 英文版语境解释
    context_map_en = {
        '硬编码路径': "The script has hardcoded file paths from someone's computer. It won't run on another machine.",
        '裸 except': 'Exceptions are silently swallowed. No error messages when something goes wrong, making debugging difficult.',
        'skiprows': 'When data format differs from expected, forcibly skipping rows causes data misalignment.',
        '自动发现': 'No mechanism to auto-discover files. Must manually specify files each time.',
        '未检测到异常分支': "When encountering unexpected situations, the AI doesn't know what to do and may give wrong results.",
        '缺少输出': 'No specification of what the output should look like. Different AIs may give completely different formats.',
        '缺少结构化步骤': 'Instructions are like a running account. AI may skip key steps or mix up order.',
        '缺少示例': 'No examples. AI can only guess and is prone to misunderstanding.',
        '缺少验证': 'No validation steps. AI may confidently output incorrect content without verification.',
        '未声明前提假设': 'Does not state under what conditions this Skill can work properly.',
        '未定义错误回退': 'No fallback plan when execution fails. AI will get stuck.',
        '未声明数据来源限制': 'Does not state where data comes from or what it covers. Different AIs may use different data sources, results not comparable.',
        '未要求置信度声明': 'Does not require AI to indicate confidence level. Easy to state uncertain things as certain.',
        '引用.*不存在的文件': "The documentation mentions a file to use, but it's not in the folder — likely a typo or forgot to include.",
        '除零风险': 'Code does division without checking if denominator is zero — program crashes if denominator is zero.',
        '路径拼接': 'Using string concatenation for file paths. May not find files on another computer — use proper path joining methods.',
        '静默覆盖': 'Opening a file and writing directly overwrites original content without backup.',
        '超时缺失': 'Network requests have no timeout set — will wait forever if network hangs.',
        '条件分支信号': 'Documentation specifies how to handle different cases. Well-considered.',
        '禁止/护栏声明': 'Documentation specifies what the AI must NOT do. Has safety boundaries.',
        '检查跳过': 'This check is not relevant to this Skill. Skipping does not affect scoring.',
        '置信度检查跳过': 'Does not involve data analysis and statistical inference. No need to consider confidence.',
        '数据来源检查跳过': 'Does not process external data. No need to declare data source.',
        '时效性检查跳过': 'Does not depend on time-varying data. No need to declare data timeliness.',
        '有固化': 'Has standalone scripts to run core tasks, not relying solely on AI improvisation.',
        '多单位混用': 'Multiple unit types in the documentation, which can confuse AI.',
        '嵌入代码': 'Many program files — AI needs to read many files at once to reproduce.',
        '检测到.*测试': 'Has test code, indicating good quality control.',
        '未检测到常见篡改点': 'No common code pitfalls like division by zero or bare exceptions.',
    }

    if lang == 'en':
        context_map = context_map_en

    # 提取 pass 和 warn/fail 项
    standard_good = []
    standard_attention = []
    for iss in all_items:
        text, status = iss[0], iss[1]
        if status in ['info', 'skip']:
            continue
        if status == 'pass':
            clean = text.replace('✅ ', '').replace('🟢 ', '')
            standard_good.append(f'- {clean}')
        elif status in ['warn', 'fail']:
            sev = {'fail': '❌', 'warn': '⚠️'}.get(status, '')
            clean = re.sub(r'^[🔴🟠🟡]\s*', '', text)
            # 查找语境解释
            hint = ''
            for key, val in context_map.items():
                if re.search(key, clean):
                    hint = f'（{val}）' if lang == 'zh-CN' else f' ({val})'
                    break
            standard_attention.append(f'> {sev} **{clean}**{hint}')

    standard_good_block = '\n'.join(standard_good) if standard_good else '- 暂无显著亮点'
    standard_attention_block = '\n'.join(standard_attention) if standard_attention else f'> ✅ {msg["no_issues"]}'

    simple_report = f"""# {msg['simple_report_title']} — {skill_name}

**{msg['date']}**: {today}

## {msg['simple_result']}

| 🏗️ {msg['foundation']} | 🤖 {msg['code']} | 📝 {msg['rules']} | 🛡️ {msg['guardrails']} |
|--------|--------|--------|--------|
| {f_rating} {f_score} | {c_rating} {c_score} | {r_rating} {r_score} | {g_rating} {g_score} |

### {msg['simple_good']}
{standard_good_block}

### {msg['simple_attention']}
{standard_attention_block}

### {msg['simple_summary']}
{summary}

---

> {msg['simple_footer']}
"""

    # AI 行动版
    fix_items = []
    for iss in issues:
        if '硬编码路径' in iss[0] or 'hardcoded' in iss[0].lower():
            fix_items.append('- ' + msg['fix_hardcoded'])
        elif 'except' in iss[0]:
            fix_items.append('- ' + msg['fix_except'])
        elif 'validate' in iss[0]:
            fix_items.append('- ' + msg['fix_validate'])
        elif '输入验证' in iss[0] or 'input validation' in iss[0].lower():
            fix_items.append('- ' + msg['fix_input_validation'])
        elif '嵌入式代码' in iss[0] or 'embedded code' in iss[0].lower():
            fix_items.append('- ' + msg['fix_embedded_code'])
        else:
            fix_items.append(f'- {iss[0]}')

    action_report = f"""# {msg['action_report_title']} — {skill_name}

**{msg['date']}**: {today}

## {msg['fix_list']}
{chr(10).join(fix_items) if fix_items else msg['no_fix_items']}

## {msg['validation_checklist']}
- [ ] {msg['check_validate']}
- [ ] {msg['check_columns']}
- [ ] {msg['check_hardcoded']}
- [ ] {msg['check_run']}

---

## {msg['next_steps']}

1. **{msg['next_step_fix']}** — {msg['next_step_fix_desc']}
2. **{msg['next_step_skip']}** — {msg['next_step_skip_desc']}
3. **{msg['next_step_better']}** — {msg['next_step_better_desc']}
"""

    # 落盘
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        version = info.get('version')
        ver_tag = f'-v{version}' if version else ''
        base = os.path.join(output_dir, f'HaluCatch-report{ver_tag}-{today}')
        for suffix, content in [('', report), ('-标准版', simple_report), ('-行动版', action_report)]:
            path = f'{base}{suffix}.md'
            # 防覆盖：如果存在则加序号
            counter = 1
            original_path = path
            while os.path.exists(path):
                stem, ext = os.path.splitext(original_path)
                path = f'{stem}-{counter}{ext}'
                counter += 1
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(msg['report_saved'].format(path=path))
    else:
        print(msg['output_to_terminal'])

    return {'professional': report, 'simple': simple_report, 'action': action_report}
