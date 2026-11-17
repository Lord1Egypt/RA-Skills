"""HaluCatch 配置层：国际化消息字典和语言检测。"""

import locale

# =============================================================================

MESSAGES = {
    'zh-CN': {
        # 错误
        'path_not_exist': '❌ 路径不存在: {path}。请确认目录存在——试试 ls {path} 看看。',
        'file_too_large': '  ⚠️ 超大文件 ({files}) 超过 10MB，跳过内容读取。如需审查，请将大文件移到别处后重新运行。',
        'no_md_files': '  ❌ 目标目录无 Markdown 文件 ({path})，这不是标准的 Skill 目录。请在目录下创建一个 SKILL.md 文件（哪怕只有一行标题也可以开始）。',
        'skill_md_substitute': '  ⚠️ 未找到标准 SKILL.md，使用 "{found}" 作为替代。建议将文件重命名为 {expected}，这样 HaluCatch 能直接识别。',
        'version_detected': '  📌 版本号: {version}',
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
        'check_complexity': '  📐 复杂度评估...',
        'ai_supplement': '  以上为脚本基线检查，AI 应在此基础上补充语义分析',
        # 报告生成
        'generating_report': '\n📊 生成报告...',
        'report_saved': '  📄 报告已生成: {path}',
        'output_to_terminal': '  📺 输出到终端:',
        # 自检
        'self_check_incomplete': '  ⚠️ 检查进度: 部分评估维度未完成',
        'self_check_ai_supplement': '  ✅ 检查进度: HaluCatch 四维评估全部执行完毕（部分维度建议 AI 补充语义分析）',
        'self_check_pass': '  ✅ 检查进度: HaluCatch 四维评估全部执行完毕',
        'complete': '\n✅ HaluCatch 审查完成。',
        'report_saved_to': '   报告已保存至: {path}',
        # 报告模板
        'report_title': 'HaluCatch 审计报告',
        'tldr': '一句话总结',
        'lang_stats': '代码风险细则',
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
        'complexity': '复杂度',
        'self_check': '检查进度',
        'self_check_pass_detail': '✅ HaluCatch 四维评估全部执行完毕',
        'self_check_warn_detail': '⚠️ 部分评估维度未完成',
        'self_check_warn': '⚠️ 检查进度: 部分评估维度未完成',
        'report_footer': '本报告由 HaluCatch 生成。',
        # 摘要
        'summary_no_risk': '✅ 全部检查通过，未发现风险',
        'summary_no_block': '✅ 核心检查通过，💡 {count} 项可优化',
        'summary_has_risk': '🔴 {critical} 严重 · ⚠️ {warnings} 注意',
        'summary_needs_judgment': ' · 💡 {count} 可优化',
        'none': '无',
        # 专业版报告模板
        'core_conclusions': '核心结论卡片',
        'dimension': '维度',
        'rating': '评级',
        'score': '分数',
        'findings': '审查发现',
        'file': '文件',
        # 标准版报告模板
        'simple_report_title': 'HaluCatch 标准报告',
        'simple_result': '审查结果',
        'simple_good': '做得好的方面',
        'simple_attention': '需要注意的方面',
        'simple_summary': '一句话总结',
        'simple_footer': '本报告是标准版本。如需技术细节，见同目录下的专业版报告。',
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
        'path_not_exist': '❌ Path does not exist: {path}. Check that the directory exists — try ls {path}.',
        'file_too_large': '  ⚠️ Oversized files ({files}) exceed 10MB, skipping content read. Move large files elsewhere if you need them reviewed.',
        'no_md_files': '  ❌ No Markdown files in target directory ({path}), not a standard Skill directory. Create a SKILL.md file (even just a title line will do).',
        'skill_md_substitute': '  ⚠️ Standard SKILL.md not found, using "{found}" as substitute. Consider renaming the file to {expected} so HaluCatch can recognize it directly.',
        'version_detected': '  📌 Version: {version}',
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
        'check_complexity': '  📐 Complexity evaluation...',
        'ai_supplement': '  Above is script baseline check, AI should supplement semantic analysis',
        # Report generation
        'generating_report': '\n📊 Generating report...',
        'report_saved': '  📄 Report generated: {path}',
        'output_to_terminal': '  📺 Output to terminal:',
        # Self-check
        'self_check_incomplete': '  ⚠️ Check progress: Some evaluation dimensions incomplete',
        'self_check_ai_supplement': '  ✅ Check progress: HaluCatch 4-dimension evaluation complete (AI supplement recommended for some dimensions)',
        'self_check_pass': '  ✅ Check progress: HaluCatch 4-dimension evaluation complete',
        'complete': '\n✅ HaluCatch audit completed.',
        'report_saved_to': '   Report saved to: {path}',
        # Report template
        'report_title': 'HaluCatch Audit Report',
        'tldr': 'TL;DR',
        'lang_stats': 'Code Risk Breakdown',
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
        'complexity': 'Complexity',
        'self_check': 'Check progress',
        'self_check_pass_detail': '✅ HaluCatch 4-dimension evaluation complete',
        'self_check_warn_detail': '⚠️ Some evaluation dimensions incomplete',
        'self_check_warn': '⚠️ Check progress: Some evaluation dimensions incomplete',
        'report_footer': 'This report was generated by HaluCatch.',
        # Summary
        'summary_no_risk': '✅ All checks passed, no risks found',
        'summary_no_block': '✅ Core checks passed, 💡 {count} suggestions',
        'summary_has_risk': '🔴 {critical} critical · ⚠️ {warnings} warnings',
        'summary_needs_judgment': ' · 💡 {count} suggestions',
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
        'simple_result': 'Audit Result',
        'simple_good': "What's Good",
        'simple_attention': 'Areas of Attention',
        'simple_summary': 'Summary',
        'simple_footer': 'This is the standard report. For technical details, see the professional report in the same directory.',
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



def detect_system_locale():
    """检测系统语言：用于 fallback"""
    try:
        system_lang, _ = locale.getdefaultlocale()
        if system_lang and ('zh' in system_lang.lower() or 'cn' in system_lang.lower()):
            return 'zh-CN'
    except Exception:
        pass
    return 'en'  # 默认英文


# =============================================================================
# 1. 文件扫描
# =============================================================================
