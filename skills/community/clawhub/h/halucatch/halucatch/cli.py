"""HaluCatch 命令行接口：解析参数并协调整个审计流程。"""

import argparse
import os
import re
import sys
import traceback

from .classifier import classify_skill
from .config import MESSAGES, detect_system_locale
from .evaluators import (
    check_code_risks,
    check_complexity,
    check_foundation,
    check_guardrails,
    check_methodology,
    check_rules,
)
from .reporter import generate_report
from .scanner import scan_folder


def _read_config_lang():
    """从 HaluCatch 包内 .halucatch_config.yaml 读取默认语言。"""
    cfg_path = os.path.join(os.path.dirname(__file__), '.halucatch_config.yaml')
    if os.path.exists(cfg_path):
        try:
            with open(cfg_path, 'r', encoding='utf-8') as f:
                for line in f:
                    m = re.match(r'^lang:\s*(\S+)', line)
                    if m:
                        return m.group(1)
        except Exception:
            pass
    return None


def _friendly_error(lang):
    """返回当前语言的异常提示消息。"""
    return {
        'zh-CN': {
            'permission': '❌ 权限不足：无法读取或写入目标路径。→ 检查文件权限，或用 --output-dir 指定可写目录。',
            'file_not_found': '❌ 目录不存在或路径错误。→ 用 ls 确认目标路径，检查拼写。',
            'disk_full': '❌ 磁盘空间不足：无法写入报告文件。→ 清理磁盘后重试。',
            'empty_dir': '❌ 目标目录为空或不包含可审查的文件。→ 确认目录内有 SKILL.md 或 .py/.js 文件。',
            'unexpected': '❌ 程序遇到意外错误。→ 复制下方的错误信息，贴到 github.com/CoderMoray/HaluCatch/issues 反馈。详情：',
            'interrupted': '\n⏹️  操作已取消。',
        },
        'en': {
            'permission': '❌ Permission denied. → Check file permissions or use --output-dir to specify a writable path.',
            'file_not_found': '❌ Directory not found. → Verify the path exists with ls, check for typos.',
            'disk_full': '❌ Disk full: cannot write report. → Free up space and retry.',
            'empty_dir': '❌ Target directory is empty or contains no scannable files. → Ensure SKILL.md or .py/.js files exist.',
            'unexpected': '❌ Unexpected error. → Copy the details below and report at github.com/CoderMoray/HaluCatch/issues. Details:',
            'interrupted': '\n⏹️  Operation cancelled.',
        },
    }[lang]


def main():
    args = None
    lang = 'zh-CN'

    try:
        parser = argparse.ArgumentParser(description='HaluCatch — AI Skill 执行可靠性审查')
        parser.add_argument('--skill-dir', required=True, help='目标 Skill 文件夹路径')
        parser.add_argument('--output-dir', default=None, help='报告输出目录（缺省则输出到终端）')
        parser.add_argument('--lang', default='auto',
                            choices=['auto', 'zh-CN', 'en'],
                            help='输出语言 (默认: auto 自动检测)')
        parser.add_argument('--validate', action='store_true', help='仅扫描文件清单，不执行评估')
        args = parser.parse_args()

        # 语言检测：CLI --lang > 系统 locale > config.yaml 默认
        config_lang = _read_config_lang()
        lang = args.lang
        if lang == 'auto':
            lang = config_lang or detect_system_locale()
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
            print(msg["check_complexity"])
            results['complexity'] = check_complexity(info, skill_type)
            print(f"     {results['complexity']['rating']}")
        else:
            print(msg["check_methodology"])
            results['rules'] = check_methodology(info)
            results['foundation'] = {'rating': '🟢 纯方法论', 'issues': [('✅ 纯方法论型 Skill，地基检查不适用', 'pass')], 'score': '-'}
            results['code'] = {'rating': '🟢 纯方法论', 'issues': [('✅ 纯方法论型 Skill，代码风险不适用', 'pass')], 'score': '-'}
            print(msg["check_guardrails"])
            results['guardrails'] = check_guardrails(info, skill_type)
            print(f"     {results['guardrails']['rating']}")
            results['guardrails']['issues'].append((msg["ai_supplement"], 'info'))
            print(msg["check_complexity"])
            results['complexity'] = check_complexity(info, skill_type)
            print(f"     {results['complexity']['rating']}")

        # Phase 3: 报告
        print("\n📊 生成报告...")
        default_out = args.output_dir or os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'reports')
        _reports = generate_report(info, results, default_out, lang)

        # 自检
        dims = ['foundation', 'code', 'rules', 'guardrails', 'complexity']
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

    except KeyboardInterrupt:
        print(_friendly_error(lang)['interrupted'])
        sys.exit(130)
    except PermissionError as e:
        print(_friendly_error(lang)['permission'])
        print(f'  {e}')
        sys.exit(1)
    except FileNotFoundError as e:
        print(_friendly_error(lang)['file_not_found'])
        print(f'  {e}')
        sys.exit(1)
    except OSError as e:
        if getattr(e, 'errno', None) == 28:
            print(_friendly_error(lang)['disk_full'])
        else:
            print(_friendly_error(lang)['unexpected'])
        print(f'  {e}')
        sys.exit(1)
    except Exception as e:
        print(_friendly_error(lang)['unexpected'])
        print(f'  {e}')
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()
