"""
HaluCatch Core — AI Skill 执行可靠性审查骨架脚本

用法：
  python3 halucatch_core.py --skill-dir <目标Skill路径> [--validate]
  python3 halucatch_core.py --skill-dir <目标Skill路径> --output-dir <报告输出路径>
"""

import os
import sys
import re
import argparse
import json
from datetime import date
import locale

# =============================================================================
# 0. 国际化消息字典
# =============================================================================

MESSAGES = {
    'zh-CN': {
        # 错误
        'path_not_exist': '❌ 路径不存在: {path}',
        'file_too_large': '  ⚠️ 超大文件 ({files}) 超过 10MB，跳过内容读取',
        # 扫描
        'scanning': '  📁 扫描: {path}',
        'file_count': '  📄 文件数: {count}',
        'skill_md': '  📝 SKILL.md: {lines} 行',
        'py_files': '  🐍 .py 文件: {count} 个 ({lines} 行)',
        'data_files': '  📊 数据文件: {count} 个',
        # 主流程
        'title': 'HaluCatch — AI Skill 执行可靠性审查',
        'phase_scan': '\n[1/3] 扫描文件...',
        'phase_validate': '\n✅ 文件扫描完成。--validate 模式下不执行评估。',
        'phase_classify': '\n[2/3] 分类: {type}',
        'phase_evaluate': '\n[3/3] 执行评估...',
        'class_code': '代码工程型',
        'class_methodology': '纯方法论型',
        # 评估步骤
        'check_foundation': '  🏗️ 地基检查...',
        'check_code': '  🤖 代码风险扫描...',
        'check_rules': '  📋 规则评估...',
        'check_methodology': '  📝 方法论评估...',
        'check_guardrails': '  🛡️ 护栏评估...',
        'ai_supplement': '  以上为脚本基线检查，AI 应在此基础上补充语义分析',
        # 报告生成
        'generating_report': '\n📊 生成报告...',
        'report_saved': '  📄 报告已生成: {path}',
        'output_to_terminal': '  📺 输出到终端:',
        # 自检
        'self_check_incomplete': '  ⚠️ 自检: 部分评估维度未完成',
        'self_check_ai_supplement': '  ✅ 自检: 四维评估完成（部分维度建议 AI 补充语义分析）',
        'self_check_pass': '  ✅ 自检: 全部通过',
        'complete': '\n✅ HaluCatch 审查完成。',
        'report_saved_to': '   报告已保存至: {path}',
        # 报告模板
        'report_title': 'HaluCatch 审计报告',
        'date': '日期',
        'skill_type': 'Skill 类型',
        'skill_file': '文件',
        'summary': '核心结论',
        'dimensions': '评估维度',
        'recommendations': '改进建议',
        'foundation': '地基',
        'code': '代码',
        'rules': '规则/方法论',
        'guardrails': '护栏',
        'self_check': '自检',
        'self_check_pass_detail': '✅ 全部通过（文件完整、四维评估完整）',
        'self_check_warn_detail': '⚠️ 部分评估维度缺失',
        'report_footer': '本报告由 HaluCatch 生成。',
        # 摘要
        'summary_no_risk': '✅ 未发现风险。',
        'summary_no_block': '📌 无阻塞项，{count} 项需 AI 补充判断。',
        'summary_has_risk': '⚠️ 发现 {critical} 项阻塞、{warnings} 项高危风险。',
        'summary_needs_judgment': ' 另有 {count} 项需 AI 补充判断。',
        'none': '无',
        # 专业版报告模板
        'core_conclusions': '核心结论卡片',
        'dimension': '维度',
        'rating': '评级',
        'score': '分数',
        'findings': '审查发现',
        'file': '文件',
        # 通俗版报告模板
        'simple_report_title': 'HaluCatch 通俗报告',
        'simple_summary': '一句话',
        'simple_findings': '发现的问题',
        'simple_footer': '本报告是专业版的白话版本。如需技术细节，见同目录下的专业版报告。',
        'no_issues': '无发现问题。',
        # AI 行动版报告模板
        'action_report_title': 'HaluCatch AI 行动版',
        'fix_list': '修复清单',
        'no_fix_items': '无修复项',
        'validation_checklist': '修复后验证检查点',
        'check_validate': '运行 `--validate` 通过',
        'check_columns': '所有列名校验通过',
        'check_hardcoded': '无硬编码路径',
        'check_run': '用真实数据跑通一次',
        'check_feedback': '生成 feedback.md',
        'feedback_template': 'feedback.md 模板',
        'feedback_template_content': '# HaluCatch 修复反馈\n\n**时间**: [当前时间]\n\n## 修改清单\n- [ ] 修复项 1\n- [ ] 修复项 2\n\n## 验证输出\n[粘贴 --validate 输出]\n\n## 完整运行\n[粘贴运行输出的最后 10 行]\n\n## 问题\n[无 / 描述]',
        'next_steps': '下一步（请选择）',
        'next_step_fix': '执行修复',
        'next_step_fix_desc': '将本报告发给你的 AI，让它按方案修改目标 Skill。修复后重新运行 `halucatch_core.py --skill-dir <路径>` 验证。',
        'next_step_skip': '不执行',
        'next_step_skip_desc': '不做任何修改，审查结束。',
        'next_step_better': '我有更好的意见',
        'next_step_better_desc': '描述你的修复想法，我据此重新生成修复方案。',
        # 修复建议
        'fix_hardcoded': '硬编码路径 → 改为 `--data-dir` 参数传入',
        'fix_except': '裸 except → 改为 `except Exception as e:` 并打印日志',
        'fix_validate': '缺 validate 模式 → 添加 `--validate` 参数和数据验证函数',
        'fix_input_validation': '缺输入验证 → 添加 check_columns() 函数',
        'fix_embedded_code': '无固化 .py → 生成骨架脚本',
    },
    'en': {
        # Errors
        'path_not_exist': '❌ Path does not exist: {path}',
        'file_too_large': '  ⚠️ Oversized files ({files}) exceed 10MB, skipping content read',
        # Scanning
        'scanning': '  📁 Scanning: {path}',
        'file_count': '  📄 File count: {count}',
        'skill_md': '  📝 SKILL.md: {lines} lines',
        'py_files': '  🐍 .py files: {count} ({lines} lines)',
        'data_files': '  📊 Data files: {count}',
        # Main flow
        'title': 'HaluCatch — AI Skill Execution Reliability Audit',
        'phase_scan': '\n[1/3] Scanning files...',
        'phase_validate': '\n✅ File scan completed. --validate mode skips evaluation.',
        'phase_classify': '\n[2/3] Classification: {type}',
        'phase_evaluate': '\n[3/3] Executing evaluation...',
        'class_code': 'Code-engineered',
        'class_methodology': 'Methodology-only',
        # Evaluation steps
        'check_foundation': '  🏗️ Foundation check...',
        'check_code': '  🤖 Code risk scan...',
        'check_rules': '  📋 Rules evaluation...',
        'check_methodology': '  📝 Methodology evaluation...',
        'check_guardrails': '  🛡️ Guardrails evaluation...',
        'ai_supplement': '  Above is script baseline check, AI should supplement semantic analysis',
        # Report generation
        'generating_report': '\n📊 Generating report...',
        'report_saved': '  📄 Report generated: {path}',
        'output_to_terminal': '  📺 Output to terminal:',
        # Self-check
        'self_check_incomplete': '  ⚠️ Self-check: Some evaluation dimensions incomplete',
        'self_check_ai_supplement': '  ✅ Self-check: 4-dimension evaluation completed (AI supplement recommended for some dimensions)',
        'self_check_pass': '  ✅ Self-check: All passed',
        'complete': '\n✅ HaluCatch audit completed.',
        'report_saved_to': '   Report saved to: {path}',
        # Report template
        'report_title': 'HaluCatch Audit Report',
        'date': 'Date',
        'skill_type': 'Skill Type',
        'skill_file': 'File',
        'summary': 'Summary',
        'dimensions': 'Evaluation Dimensions',
        'recommendations': 'Recommendations',
        'foundation': 'Foundation',
        'code': 'Code',
        'rules': 'Rules/Methodology',
        'guardrails': 'Guardrails',
        'self_check': 'Self-check',
        'self_check_pass_detail': '✅ All passed (files complete, 4-dimension evaluation complete)',
        'self_check_warn_detail': '⚠️ Some evaluation dimensions missing',
        'report_footer': 'This report was generated by HaluCatch.',
        # Summary
        'summary_no_risk': '✅ No risks found.',
        'summary_no_block': '📌 No blocking items, {count} items need AI judgment.',
        'summary_has_risk': '⚠️ Found {critical} blocking items, {warnings} high-risk items.',
        'summary_needs_judgment': ' Also {count} items need AI judgment.',
        'none': 'None',
        # Professional report template
        'core_conclusions': 'Core Conclusions',
        'dimension': 'Dimension',
        'rating': 'Rating',
        'score': 'Score',
        'findings': 'Findings',
        'file': 'File',
        # Simple report template
        'simple_report_title': 'HaluCatch Simple Report',
        'simple_summary': 'Summary',
        'simple_findings': 'Issues Found',
        'simple_footer': 'This report is a plain-language version of the professional report. For technical details, see the professional report in the same directory.',
        'no_issues': '✅ No issues found.',
        # AI Action report template
        'action_report_title': 'HaluCatch AI Action Plan',
        'fix_list': 'Fix List',
        'no_fix_items': 'No fix items',
        'validation_checklist': 'Post-fix Validation Checklist',
        'check_validate': 'Run `--validate` passes',
        'check_columns': 'All column names validated',
        'check_hardcoded': 'No hardcoded paths',
        'check_run': 'Run with real data succeeds',
        'check_feedback': 'Generate feedback.md',
        'feedback_template': 'feedback.md template',
        'feedback_template_content': '# HaluCatch Fix Feedback\n\n**Time**: [current time]\n\n## Fix List\n- [ ] Fix item 1\n- [ ] Fix item 2\n\n## Validation Output\n[Paste --validate output]\n\n## Full Run\n[Paste last 10 lines of run output]\n\n## Issues\n[None / Description]',
        'next_steps': 'Next Steps (Please Choose)',
        'next_step_fix': 'Execute Fix',
        'next_step_fix_desc': 'Send this report to your AI and ask it to modify the target Skill according to the plan. After fixing, re-run `halucatch_core.py --skill-dir <path>` to verify.',
        'next_step_skip': 'Skip',
        'next_step_skip_desc': 'Make no changes. Audit ends.',
        'next_step_better': 'I Have a Better Idea',
        'next_step_better_desc': 'Describe your fix idea, and I will regenerate the fix plan accordingly.',
        # Fix suggestions
        'fix_hardcoded': 'Hardcoded paths → change to `--data-dir` parameter',
        'fix_except': 'Bare except → change to `except Exception as e:` and log',
        'fix_validate': 'Missing validate mode → add `--validate` parameter and data validation function',
        'fix_input_validation': 'Missing input validation → add check_columns() function',
        'fix_embedded_code': 'No固化 .py → generate skeleton script',
    }
}

# =============================================================================
# 0.1 语言检测
# =============================================================================

def detect_system_locale():
    """检测系统语言：用于 fallback"""
    try:
        system_lang, _ = locale.getdefaultlocale()
        if system_lang and ('zh' in system_lang.lower() or 'cn' in system_lang.lower()):
            return 'zh-CN'
    except:
        pass
    return 'en'  # 默认英文


# =============================================================================
# 1. 文件扫描
# =============================================================================

def scan_folder(path, msg):
    """递归扫描文件夹，返回文件清单和 SKILL.md / .py 内容。"""
    if not os.path.isdir(path):
        print(msg['path_not_exist'].format(path=path))
        return None

    files = []
    skill_md_content = None
    py_contents = []
    skill_md_path = None
    py_paths = []

    skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'node_modules', '.venv', 'venv', 'avatars'}

    for root, dirs, filenames in os.walk(path):
        dirs[:] = [d for d in dirs if d not in skip_dirs and not d.startswith('.')]
        for fname in filenames:
            fpath = os.path.join(root, fname)
            size = os.path.getsize(fpath)
            ext = os.path.splitext(fname)[1].lower()
            fpath_rel = os.path.relpath(fpath, path)
            files.append({'name': fname, 'ext': ext, 'size': size, 'path': fpath, 'rel_path': fpath_rel})

    # 尺寸保护：跳过超大文件避免 OOM
    SZ_LIMIT = 10 * 1024 * 1024  # 10MB
    oversized = []
    for f in files:
        if f['size'] > SZ_LIMIT:
            oversized.append(f['name'])
    if oversized:
        print(msg['file_too_large'].format(files="', '".join(oversized)))
    oversized_set = set(oversized)

    for f in files:
        if f['name'] in oversized_set:
            continue
        if f['name'].lower() in ['skill.md', 'toolcard.md']:
            skill_md_path = f['path']
            with open(f['path'], 'r', encoding='utf-8', errors='backslashreplace') as fh:
                skill_md_content = fh.read()

        if f['ext'] == '.py':
            py_paths.append(f['path'])
            with open(f['path'], 'r', encoding='utf-8', errors='backslashreplace') as fh:
                py_contents.append(fh.read())

    has_data = any(f['ext'] in ['.xlsx', '.xls', '.csv'] for f in files)

    py_content = '\n'.join(py_contents) if py_contents else None
    py_path = py_paths[0] if py_paths else None
    max_py_lines = max(len(c.splitlines()) for c in py_contents) if py_contents else 0

    print(msg['scanning'].format(path=path))
    print(msg['file_count'].format(count=len(files)))
    if skill_md_content:
        print(msg['skill_md'].format(lines=len(skill_md_content.splitlines())))
    if py_paths:
        total_py_lines = sum(len(c.splitlines()) for c in py_contents)
        print(msg['py_files'].format(count=len(py_paths), lines=total_py_lines))
    if has_data:
        data_count = sum(1 for f in files if f['ext'] in ['.xlsx', '.xls', '.csv'])
        print(msg['data_files'].format(count=data_count))

    return {
        'files': files,
        'skill_md': skill_md_content,
        'skill_md_path': skill_md_path,
        'py': py_content,
        'py_path': py_path,
        'py_count': len(py_paths),
        'max_py_lines': max_py_lines,
        'has_data': has_data,
    }


# =============================================================================
# 2. 技能分类
# =============================================================================

def classify_skill(info):
    """判断 Skill 类型：代码工程型 / 纯方法论型。"""
    has_py = info['py'] is not None
    has_data = info['has_data']
    has_pd = info['skill_md'] and ('pd.read_' in info['skill_md'] or 'pandas' in info['skill_md'].lower())
    has_md_py = info['skill_md'] and ('```python' in info['skill_md'])

    if has_py or has_data or has_pd or has_md_py:
        return 'code-engineered'
    return 'methodology'


# =============================================================================
# 3. 评估函数
# =============================================================================

def check_foundation(info):
    """地基检查：有 .py？路径写死？有 validate？"""
    issues = []
    score = 0
    total = 6

    # 1) 有固化脚本
    if info['py']:
        issues.append(('✅ 有固化 .py 脚本', 'pass'))
        score += 1
    else:
        issues.append(('🔴 无固化 .py 脚本——AI 须自行编写全部代码', 'fail'))

    # 2) 路径参数化
    if info['py']:
        matches = re.findall(r"['\"](/[^'\"]+?)['\"]", info['py'])
        hardcoded = [m for m in matches if 'Users/' in m or 'home/' in m or 'C:' in m]
        if hardcoded:
            issues.append((f'🔴 发现 {len(hardcoded)} 处硬编码路径: {hardcoded[:3]}', 'fail'))
        else:
            issues.append(('✅ 路径已参数化或无本地绝对路径', 'pass'))
            score += 1
    else:
        issues.append(('🟡 无 .py 文件，无法检查路径', 'skip'))

    # 3) validate 模式
    if info['py'] and '--validate' in info['py']:
        issues.append(('✅ 有 --validate 验证模式', 'pass'))
        score += 1
    elif info['py']:
        issues.append(('🟠 有 .py 但缺少 --validate 验证模式 → 建议在 argparse 中添加 `--validate` 参数', 'warn'))
    else:
        issues.append(('🟡 无 .py 文件，无法检查验证模式', 'skip'))

    # 4) 列名预检/输入验证
    if info['py'] and ('check_columns' in info['py'] or 'required_' in info['py'] or '列名预检' in info['py'] or '列名' in info['py']):
        issues.append(('✅ 有输入验证/列名校验', 'pass'))
        score += 1
    elif info['py']:
        issues.append(('🟠 有 .py 但缺少输入验证 → 建议添加 check_columns() 或 required_ 字段预检', 'warn'))
    else:
        issues.append(('🟡 无 .py 文件，无法检查输入验证', 'skip'))

    # 5) 文件发现机制
    if info['py']:
        if 'glob' in info['py'] or 'os.listdir' in info['py']:
            issues.append(('✅ 使用通配符/自动发现文件', 'pass'))
            score += 1
        else:
            issues.append(('🟠 有 .py 但缺少文件自动发现机制（建议用 glob）', 'warn'))
    else:
        issues.append(('🟡 无 .py 文件，跳过文件发现检查', 'skip'))

    # 6) 依赖声明
    if info['skill_md'] and ('依赖' in info['skill_md'] or 'requirements' in info['skill_md'].lower()):
        issues.append(('✅ SKILL.md 声明了依赖', 'pass'))
        score += 1
    else:
        issues.append(('🟡 SKILL.md 未声明依赖', 'warn'))

    # 评级
    pct = score / max(total, 1)
    if pct >= 0.8:
        rating = '🟢 稳固'
    elif pct >= 0.4:
        rating = '🟡 有隐患'
    else:
        rating = '🔴 无地基'

    return {'rating': rating, 'issues': issues, 'score': f'{score}/{total}'}


def check_code_risks(info):
    """代码风险扫描：常见 AI 复现篡改点。"""
    issues = []
    total_checks = 0
    found_risks = 0

    if not info['py']:
        return {'rating': '🟡 无嵌入式代码', 'issues': [('🟡 无 .py 文件，无法扫描代码风险', 'skip')], 'score': '-'}

    patterns = [
        ('异常处理', r'except\s*:\s*pass', '裸 except: pass — 可能吞掉内存错误等关键异常'),
        ('浮点比较', r'\w+\s*==\s*0\.0', '浮点数精确相等比较 — 可能漏判接近 0 的值'),
        ('除零风险', r'return\s+[^/]*/\s*\w+', 'return 中直接返回除法结果 — 分母为 0 时无保护'),
        ('硬编码阈值', r'skiprows\s*=\s*\d', '固定的 skiprows — 格式漂移时数据错位'),
        ('路径拼接', r'[\'\"][/\w]+\s*\+\s*[\'\"\/]|[\'\"\/]\s*\+\s*[\'\"][\w/]+', '字符串拼接路径 — 建议用 os.path.join'),
        ('静默覆盖', r'open\([^)]*,\s*[\'\"]w[\'\"]', '写模式打开文件 — 未警告覆盖已有内容'),
        ('超时缺失', r'requests\.(get|post|put|delete)\([^)]*\)', 'HTTP 请求未设置 timeout — 可能无限挂起'),
    ]

    for name, pattern, desc in patterns:
        total_checks += 1
        if re.search(pattern, info['py']):
            issues.append((f'🟠 [{name}] {desc}', 'warn'))
            found_risks += 1

    if found_risks == 0:
        issues.append(('✅ 未检测到常见篡改点', 'pass'))

    # 评级基于嵌入代码行数（取最大单文件）
    lines = info.get('max_py_lines', len(info['py'].splitlines()) if info['py'] else 0)
    py_count = info.get('py_count', 1 if info['py'] else 0)
    if lines > 200:
        if py_count > 1:
            issues.append((f'🟡 嵌入代码 {py_count} 个 .py 文件，最大单文件 {lines} 行 — 文件较多，AI 复现时可能遗漏', 'warn'))
        else:
            issues.append((f'🟡 嵌入代码 {lines} 行 — 较长，AI 复现时可能遗漏或篡改', 'warn'))

    if found_risks == 0 and lines <= 200:
        rating = '🟢 低风险'
    elif found_risks <= 2:
        rating = '🟠 有风险'
    else:
        rating = '🔴 高风险'

    return {'rating': rating, 'issues': issues, 'score': f'{found_risks}/{total_checks}'}


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

    pct = score / total
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

    pct = score / total
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


def check_methodology(info):
    """纯方法论型 Skill 评估。"""
    md = info['skill_md']
    issues = []

    if not md:
        return {'rating': '🟡 无 SKILL.md', 'issues': [('🟡 未找到 SKILL.md', 'skip')], 'score': '-'}

    total = 5
    score = 0

    # 1) 步骤清晰
    if re.search(r'(步骤|Step|##\s+\d|第[一二三四五六七八九十\d]+步)', md):
        issues.append(('✅ 有结构化步骤', 'pass'))
        score += 1
    else:
        issues.append(('🟠 缺少结构化步骤描述', 'warn'))

    # 2) 边界处理 — 跨语言结构信号（清单/图标/表格密度）
    status, text = _branch_density(md)
    issues.append((text, status))
    if status == 'pass':
        score += 1

    # 3) 输出格式定义 — 关键词 + 代码块检测
    has_output_kw = re.search(r'(输出|产出|结果|report|生成|respond\s+with|returns?\s+the)', md) is not None
    code_blocks = len(re.findall(r'```', md)) // 2
    if has_output_kw or code_blocks >= 2:
        issues.append(('✅ 定义了输出格式', 'pass'))
        score += 1
    else:
        issues.append(('🟡 未明确定义输出格式', 'warn'))

    # 4) 有示例
    if '例如' in md or '示例' in md or 'e.g.' in md.lower() or 'eg' in md.lower() or '```' in md:
        issues.append(('✅ 包含示例', 'pass'))
        score += 1
    else:
        issues.append(('🟡 缺少示例说明', 'warn'))

    # 5) 自洽 — 检查 SKILL.md 引用的文件是否在文件夹中存在
    mentioned_files = re.findall(r'[`"]([a-zA-Z0-9_./-]*[a-zA-Z0-9_]+\.(?:py|md|xlsx|xls|csv|json|yaml|yml|toml))[`"]', md)
    existing_names = {f['name'] for f in info.get('files', [])}
    existing_paths = {f.get('rel_path', f['name']) for f in info.get('files', [])}
    # 优先用完整相对路径匹配，退化为 basename
    missing = [m for m in mentioned_files if m not in existing_paths and os.path.basename(m) not in existing_names]
    if missing:
        issues.append((f'🟠 引用了不存在的文件: {missing[:3]}', 'warn'))
    elif mentioned_files:
        issues.append((f'✅ 引用文件均在文件夹中（{len(mentioned_files)} 个）', 'pass'))
        score += 1
    else:
        issues.append(('🟡 未在 SKILL.md 中检测到文件引用，跳过自洽检查', 'skip'))

    issues.append(('📝 以上为结构信号基线，语义判断（分支是否完备、逻辑是否正确）请由 AI 补充', 'info'))

    pct = score / total
    if pct >= 0.8:
        rating = '🟢 可靠'
    elif pct >= 0.4:
        rating = '🟡 有改进空间'
    else:
        rating = '🔴 不可靠'

    return {'rating': rating, 'issues': issues, 'score': f'{score}/{total}'}


# =============================================================================
# 4. 报告生成
# =============================================================================


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

> {msg['report_footer']}: {self_check_msg}
"""

    # 通俗版 — 附带语境解释
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
        # === 代码风险通用 ===
        '除零风险': '代码里直接做了除法但没有检查分母会不会是零——万一分母为零程序就崩了',
        '路径拼接': '用加号拼接文件路径，换台电脑可能就找不到文件——建议用专业的路径拼接方法',
        '静默覆盖': '打开文件直接往里面写内容，会把原来的内容悄悄盖掉不留备份',
        '超时缺失': '发网络请求没设超时时间——万一网络卡了会一直等到天荒地老',
        # === 信号输出 ===
        '条件分支信号': '说明书写了不同情况下该怎么处理，考虑得比较周全',
        '禁止/护栏声明': '说明书写了 AI 不能做什么事，有一定的安全底线',
        # === skip 项 ===
        '检查跳过': '这项检查跟这个 Skill 不沾边，跳过不影响评分',
        '置信度检查跳过': '不涉及数据分析和统计推断，不需要考虑置信度',
        '数据来源检查跳过': '不处理外部数据，不需要声明数据来源',
        '时效性检查跳过': '不依赖时变数据，不需要声明数据时效性',
    }
    
    # 英文版语境解释
    context_map_en = {
        '硬编码路径': 'The script has hardcoded file paths from someone\'s computer. It won\'t run on another machine.',
        '裸 except': 'Exceptions are silently swallowed. No error messages when something goes wrong, making debugging difficult.',
        'skiprows': 'When data format differs from expected, forcibly skipping rows causes data misalignment.',
        '自动发现': 'No mechanism to auto-discover files. Must manually specify files each time.',
        '未检测到异常分支': 'When encountering unexpected situations, the AI doesn\'t know what to do and may give wrong results.',
        '缺少输出': 'No specification of what the output should look like. Different AIs may give completely different formats.',
        '缺少结构化步骤': 'Instructions are like a running account. AI may skip key steps or mix up order.',
        '缺少示例': 'No examples. AI can only guess and is prone to misunderstanding.',
        '缺少验证': 'No validation steps. AI may confidently output incorrect content without verification.',
        '未声明前提假设': 'Does not state under what conditions this Skill can work properly.',
        '未定义错误回退': 'No fallback plan when execution fails. AI will get stuck.',
        '未声明数据来源限制': 'Does not state where data comes from or what it covers. Different AIs may use different data sources, results not comparable.',
        '未要求置信度声明': 'Does not require AI to indicate confidence level. Easy to state uncertain things as certain.',
        '引用.*不存在的文件': 'The documentation mentions a file to use, but it\'s not in the folder — likely a typo or forgot to include.',
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
    }
    
    # 根据语言选择 context_map
    if lang == 'en':
        context_map = context_map_en

    simple_issues = []
    for iss in issues:
        if iss[1] == 'info':
            continue  # 通俗版不展示 info 级提示
        text = iss[0].replace('🔴', '❌').replace('🟠', '⚠️').replace('🟡', '📌')
        hint = ''
        for key, val in context_map.items():
            if key in text:
                hint = f'（{val}）' if lang == 'zh-CN' else f' ({val})'
                break
        simple_issues.append(f'- {text}{hint}')

    simple_body = '\n'.join(simple_issues) if simple_issues else '✅ ' + msg['no_issues']

    simple_report = f"""# {msg['simple_report_title']} — {skill_name}

**{msg['date']}**: {today}


## {msg['simple_summary']}
{summary}

## {msg['simple_findings']}
{simple_body}

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
- [ ] {msg['check_feedback']}

## {msg['feedback_template']}

```markdown
{msg['feedback_template_content']}
```

---

## {msg['next_steps']}

1. **{msg['next_step_fix']}** — {msg['next_step_fix_desc']}
2. **{msg['next_step_skip']}** — {msg['next_step_skip_desc']}
3. **{msg['next_step_better']}** — {msg['next_step_better_desc']}
"""

    # 落盘
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.join(output_dir, f'HaluCatch-report-{today}')
        for suffix, content in [('', report), ('-通俗版', simple_report), ('-行动版', action_report)]:
            path = f'{base}{suffix}.md'
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(msg['report_saved'].format(path=path))
    else:
        print(msg['output_to_terminal'])

    return {'professional': report, 'simple': simple_report, 'action': action_report}
def main():
    parser = argparse.ArgumentParser(description='HaluCatch — AI Skill 执行可靠性审查')
    parser.add_argument('--skill-dir', required=True, help='目标 Skill 文件夹路径')
    parser.add_argument('--output-dir', default=None, help='报告输出目录（缺省则输出到终端）')
    parser.add_argument('--lang', default='auto',
                        choices=['auto', 'zh-CN', 'en'],
                        help='输出语言 (默认: auto 自动检测)')
    parser.add_argument('--validate', action='store_true', help='仅扫描文件清单，不执行评估')
    args = parser.parse_args()
    
    # 语言检测
    if args.lang == 'auto':
        lang = detect_system_locale()
    else:
        lang = args.lang
    msg = MESSAGES[lang]
    
    print("=" * 60)
    print(f"  {msg['title']}")
    print("=" * 60)

    # Phase 1: 扫描
    print("\n[1/3] 扫描文件...")
    info = scan_folder(args.skill_dir, msg)
    if info is None:
        return

    if args.validate:
        print("\n✅ 文件扫描完成。--validate 模式下不执行评估。")
        return

    # Phase 0: 分类
    skill_type = classify_skill(info)
    print(f"\n[2/3] 分类: {'代码工程型' if skill_type == 'code-engineered' else '纯方法论型'}")

    # Phase 2: 评估
    print("\n[3/3] 执行评估...")
    results = {}

    if skill_type == 'code-engineered':
        print(msg["check_foundation"])
        results['foundation'] = check_foundation(info)
        print(f"     {results['foundation']['rating']}")
        print(msg["check_code"])
        results['code'] = check_code_risks(info)
        print(f"     {results['code']['rating']}")
        print(msg["check_rules"])
        results['rules'] = check_rules(info)
        print(f"     {results['rules']['rating']}")
        results['rules']['issues'].append((msg["ai_supplement"], 'info'))
        print(msg["check_guardrails"])
        results['guardrails'] = check_guardrails(info, skill_type)
        print(f"     {results['guardrails']['rating']}")
        results['guardrails']['issues'].append((msg["ai_supplement"], 'info'))
    else:
        print(msg["check_methodology"])
        results['rules'] = check_methodology(info)
        results['foundation'] = {'rating': '🟢 纯方法论', 'issues': [('✅ 纯方法论型 Skill，地基检查不适用', 'pass')], 'score': '-'}
        results['code'] = {'rating': '🟢 纯方法论', 'issues': [('✅ 纯方法论型 Skill，代码风险不适用', 'pass')], 'score': '-'}
        print(msg["check_guardrails"])
        results['guardrails'] = check_guardrails(info, skill_type)
        print(f"     {results['guardrails']['rating']}")
        results['guardrails']['issues'].append((msg["ai_supplement"], 'info'))

    # Phase 3: 报告（缺省输出到自身 reports/ 目录，避免污染目标 Skill 目录）
    print("\n📊 生成报告...")
    default_out = args.output_dir or os.path.join(os.path.dirname(os.path.abspath(__file__)), 'reports')
    reports = generate_report(info, results, default_out, lang)

    # 自检
    dims = ['foundation', 'code', 'rules', 'guardrails']
    all_dims_done = all(d in results and 'rating' in results[d] for d in dims)
    has_info_items = any(
        any(i[1] == 'info' for i in results[d].get('issues', []))
        for d in dims
    )
    if not all_dims_done:
        print(msg["self_check_incomplete"])
    elif has_info_items:
        print(msg["self_check_ai_supplement"])
    else:
        print(msg["self_check_pass"])

    print("\n✅ HaluCatch 审查完成。")
    print(msg["report_saved_to"].format(path=default_out))


if __name__ == '__main__':
    main()
