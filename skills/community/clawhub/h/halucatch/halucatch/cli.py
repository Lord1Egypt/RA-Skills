"""HaluCatch 命令行接口：解析参数并协调整个审计流程。"""

import os
import sys
import argparse
from .config import MESSAGES, detect_system_locale
from .scanner import scan_folder
from .classifier import classify_skill
from .evaluators import check_foundation, check_code_risks, check_rules, check_guardrails, check_methodology
from .reporter import generate_report


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

    # Phase 3: 报告（缺省输出到项目根目录 reports/，避免污染目标 Skill 目录）
    print("\n📊 生成报告...")
    default_out = args.output_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')
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
