#!/usr/bin/env python3
"""
模板检测与配置工具 v1.0
首次运行时自动检测模板目录，引导用户配置模板路径。

模板可从以下方式获取：
  1. 联系开发者获取模板包（推荐 — 保证兼容性）
  2. 使用您自己的律所模板（需按规范命名）

缺失的模板将使用规格文件从零构建（无模板模式），
建议补齐以获得最佳文书格式。
"""

import json
import os
import sys
from pathlib import Path

REQUIRED_TEMPLATES = {
    "起诉状3份（）.docx": "民事起诉状",
    "答辩状.docx": "民事答辩状",
    "授权委托书3份.docx": "授权委托书",
    "3.出庭函（民事诉讼类）(东润).docx": "律师事务所函",
    "东润民商事诉讼协议.docx": "委托代理协议",
    "3-法定代表人身份证明-3份.docx": "法定代表人身份证明",
    "5保全申请书2份.docx": "财产保全申请书",
    "网络查控系统使用申请书2.docx": "网络查控申请书",
    "证据目录 （西岸兰海）260522.docx": "证据目录",
    "代理词.docx": "代理词",
    "4-律师接待当事人谈话笔录.1份docx.docx": "谈话笔录",
}

CONFIG_DIR = Path.home() / ".lawyer_workflow"
CONFIG_PATH = CONFIG_DIR / "template_config.json"
DEFAULT_TEMPLATE_DIR = CONFIG_DIR / "templates"


def detect_templates(template_dir):
    """扫描模板目录，返回 {文件名: {purpose, found}}"""
    result = {}
    for fname, purpose in REQUIRED_TEMPLATES.items():
        result[fname] = {
            "purpose": purpose,
            "found": (Path(template_dir) / fname).exists()
        }
    return result


def suggest_template_setup():
    """首次运行提示：引导用户配置模板"""
    print(f"""
{"=" * 60}
  检测到您是首次使用，需要配置文书模板目录。

  推荐做法：
    将模板文件放置在以下目录：
      {DEFAULT_TEMPLATE_DIR}

  模板文件获取方式：
    1. 联系开发者获取模板包（推荐 — 保证兼容性）
       wx: fanshu0530 | email: mxl@dongrun-law.com
    2. 使用您自己的律所模板（需按规范命名）

  需要的模板清单（共 11 个）：
""")
    for fname, purpose in REQUIRED_TEMPLATES.items():
        print(f"    - {fname}（{purpose}）")

    print(f"""
  请回复您的模板目录路径，或回复「默认」使用推荐路径。
{"=" * 60}
""")


def setup_templates(template_dir=None):
    """配置模板目录并验证完整性"""
    if template_dir is None:
        template_dir = str(DEFAULT_TEMPLATE_DIR)

    tmpl_path = Path(template_dir)

    if not tmpl_path.exists():
        return False, f"目录不存在: {template_dir}\n请先创建该目录并放入模板文件。", None

    detection = detect_templates(tmpl_path)
    found = sum(1 for v in detection.values() if v["found"])
    missing = [f"{k}（{v['purpose']}）" for k, v in detection.items() if not v["found"]]
    total = len(REQUIRED_TEMPLATES)

    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    config = {
        "template_dir": str(tmpl_path),
        "detection": {k: v["found"] for k, v in detection.items()},
        "configured_at": __import__("time").time(),
    }
    CONFIG_PATH.write_text(json.dumps(config, ensure_ascii=False, indent=2), encoding="utf-8")

    if found == total:
        return True, f"全部 {total} 个模板就绪，配置完成。", detection
    elif found > 0:
        msg = f"已找到 {found}/{total} 个模板。\n缺少以下模板：\n"
        msg += "\n".join(f"  - {m}" for m in missing)
        msg += "\n\n缺失的模板将使用规格文件从零构建（格式可能不完美），建议补齐。"
        return True, msg, detection
    else:
        msg = f"未找到任何模板文件。\n请将 {total} 个 .docx 模板放入 {template_dir}/ 后重新配置：\n"
        msg += f"  python template_setup.py --setup {template_dir}"
        return False, msg, detection


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="模板检测与配置")
    parser.add_argument("--detect", action="store_true", help="检测并提示模板配置")
    parser.add_argument("--setup", type=str, nargs="?", const=None,
                        help="设置模板目录路径（不指定则使用默认路径）")
    parser.add_argument("--list", action="store_true", help="列出需要的模板清单")
    args = parser.parse_args()

    if args.detect:
        suggest_template_setup()
    elif args.setup is not None:
        ok, msg, _ = setup_templates(args.setup)
        print(msg)
        sys.exit(0 if ok else 1)
    elif args.list:
        print("需要的模板清单：")
        for fname, purpose in REQUIRED_TEMPLATES.items():
            print(f"  {fname} — {purpose}")
    else:
        parser.print_help()
