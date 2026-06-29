r"""
convert.py — LaTeX 引擎转换器

将完整的 pdfLaTeX 文档转换为 LuaLaTeX 兼容语法。
原文件不动，输出新文件 + 转换报告。

支持：
  - 删除 inputenc/fontenc（LuaLaTeX 不需要）
  - 替换 CJK/CJKutf8 → ctex
  - 替换 times/helvet/courier/mathptmx → fontspec + 对应字体命令
  - 删除 pdfLaTeX 特有驱动选项（dvips/dvipdfmx）
  - 输出详细转换报告（改动清单 + 待人工确认项）

用法:
  python scripts/convert.py input.tex --to lualatex
  python scripts/convert.py input.tex --to lualatex --output converted.tex
"""

import argparse
import os
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime


# ── 转换规则表 ────────────────────────────────────────────
# (pattern, replacement, severity, description)
# severity: auto=自动处理, manual=需要人工确认
CONVERSION_RULES = [
    # inputenc — LuaLaTeX 不需要
    (r'^\s*\\usepackage\s*\[.*?\]\s*\{inputenc\}\s*(?:%.*)?$',
     "", "auto", "删除 inputenc（LuaLaTeX 原生 UTF-8）"),
    (r'^\s*\\usepackage\s*\{inputenc\}\s*(?:%.*)?$',
     "", "auto", "删除 inputenc（LuaLaTeX 原生 UTF-8）"),

    # fontenc — LuaLaTeX 不需要
    (r'^\s*\\usepackage\s*\[.*?\]\s*\{fontenc\}\s*(?:%.*)?$',
     "", "auto", "删除 fontenc（LuaLaTeX 使用 fontspec 管理字体编码）"),
    (r'^\s*\\usepackage\s*\{fontenc\}\s*(?:%.*)?$',
     "", "auto", "删除 fontenc"),

    # CJK → ctex
    (r'^\s*\\usepackage\s*(?:\[.*?\])?\s*\{CJKutf8\}\s*(?:%.*)?$',
     r"\usepackage{ctex}", "auto", "CJKutf8 → ctex"),
    (r'^\s*\\usepackage\s*(?:\[.*?\])?\s*\{CJK\}\s*(?:%.*)?$',
     r"\usepackage{ctex}", "auto", "CJK → ctex"),

    # 字体包 → fontspec（用 \n 占位，_replacer 中展开）
    (r'^\s*\\usepackage\s*\{times\}\s*(?:%.*)?$',
     r"__NEWLINES__% \usepackage{fontspec}__NL__% \setmainfont{Times New Roman}  % 取消注释并指定字体（可选）",
     "auto", "times → fontspec（已注释，取消注释并指定字体）"),
    (r'^\s*\\usepackage\s*\{helvet\}\s*(?:%.*)?$',
     r"__NEWLINES__% \setsansfont{Helvetica}  % 取消注释并指定字体（可选）",
     "auto", "helvet → fontspec"),
    (r'^\s*\\usepackage\s*\{courier\}\s*(?:%.*)?$',
     r"__NEWLINES__% \setmonofont{Courier New}  % 取消注释并指定字体（可选）",
     "auto", "courier → fontspec"),
    (r'^\s*\\usepackage\s*\{mathptmx\}\s*(?:%.*)?$',
     r"__NEWLINES__% 数学字体: \usepackage{fontspec}__NL__% \setmainfont{Times New Roman}",
     "auto", "mathptmx → fontspec（已注释，取消注释并指定字体）"),

    # 图形驱动选项 — LuaLaTeX 不需要
    (r'^\s*\\usepackage\s*\[.*?dvips.*?\]\s*\{graphicx\}\s*(?:%.*)?$',
     r"\usepackage{graphicx}", "auto", "删除 graphicx 的 dvips 驱动选项"),
    (r'^\s*\\usepackage\s*\[.*?dvipdfmx.*?\]\s*\{graphicx\}\s*(?:%.*)?$',
     r"\usepackage{graphicx}", "auto", "删除 graphicx 的 dvipdfmx 驱动选项"),

    # xcolor 驱动选项
    (r'^\s*\\usepackage\s*\[.*?dvipsnames.*?\]\s*\{xcolor\}\s*(?:%.*)?$',
     r"\usepackage{xcolor}", "auto", "删除 xcolor 的 dvipsnames 驱动选项"),

    # pdfLaTeX 特有页面尺寸命令
    (r'^\s*\\pdfpagewidth\s*=\s*.*$', "", "auto", "删除 \\pdfpagewidth（LuaLaTeX 用 \\paperwidth）"),
    (r'^\s*\\pdfpageheight\s*=\s*.*$', "", "auto", "删除 \\pdfpageheight（LuaLaTeX 用 \\paperheight）"),

    # 中文引号/破折号兼容（pdfLaTeX 需要特殊配置，LuaLaTeX 原生支持）
    (r'\\usepackage\s*\{textcomp\}\s*', "", "auto", "删除 textcomp（LuaLaTeX 不需要）"),
]

# ── 待人工确认的模式（仅标记，不自动转换） ────────────────
MANUAL_CHECK_PATTERNS = [
    (r'\\special\s*\{', "\\special 命令（pdfLaTeX 特有，需要人工检查）"),
    (r'\\includegraphics\s*\[.*?\]\s*\{.*?\.[eE][pP][sS]\}', "EPS 图片（LuaLaTeX 直接支持 PNG/PDF/JPG，EPS 需转换）"),
    (r'\\psfig', "psfig 命令已过时，建议替换为 \\includegraphics"),
    (r'\\epsfig', "epsfig 命令已过时，建议替换为 \\includegraphics"),
    (r'\\pstricks', "PSTricks（pdfLaTeX 特有，LuaLaTeX 需 \\usepackage{pstricks} 或改用 TikZ）"),
]


def _replace(pattern, replacement, text):
    """包装 re.sub，正确处理 LaTeX 反斜杠和 __NL__ 换行符"""
    def _replacer(m):
        result = replacement
        # 展开换行符（__NL__ → \n, __NEWLINES__ → \n\n）
        result = result.replace("__NEWLINES__", "\n")
        result = result.replace("__NL__", "\n")
        return result
    return re.sub(pattern, _replacer, text, flags=re.MULTILINE)


def convert_pdflatex_to_lualatex(source_path: str) -> dict:
    """将 pdfLaTeX 文档转换为 LuaLaTeX

    Returns:
        {success, output_path, changes, manual_items, warnings, stats}
    """
    result = {
        "success": False,
        "input": source_path,
        "output_path": "",
        "changes": [],
        "manual_items": [],
        "warnings": [],
        "stats": {"auto": 0, "manual": 0},
    }
    try:
        with open(source_path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        result["error"] = f"读取源文件失败: {e}"
        return result

    # 逐条应用转换规则
    new_content = content
    for pattern, replacement, severity, description in CONVERSION_RULES:
        matches = list(re.finditer(pattern, new_content, re.MULTILINE))
        if matches:
            new_content = _replace(pattern, replacement, new_content)
            for m in matches:
                result["changes"].append({
                    "severity": severity,
                    "description": description,
                    "original": m.group().strip()[:60],
                    "line": content[:m.start()].count("\n") + 1,
                })
                result["stats"][severity] = result["stats"].get(severity, 0) + 1

    # 扫描待人工确认项
    for pattern, description in MANUAL_CHECK_PATTERNS:
        for m in re.finditer(pattern, new_content, re.MULTILINE | re.IGNORECASE):
            result["manual_items"].append({
                "description": description,
                "content": m.group().strip()[:60],
                "line": content[:m.start()].count("\n") + 1,
            })

    # 写入输出文件
    base, ext = os.path.splitext(source_path)
    output_path = f"{base}_lualatex{ext}"
    try:
        from safe_write import safe_write
        sw = safe_write(output_path, new_content)
        if not sw["success"]:
            result["warnings"].append(f"安全写入失败，使用 fallback: {sw.get('error', '')}")
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(new_content)
    except Exception as e:
        result["warnings"].append(f"写入输出文件失败: {e}")
        return result

    result["output_path"] = output_path
    result["success"] = True
    return result


def print_report(r: dict):
    """打印转换报告"""
    print("=" * 60)
    print("  pdfLaTeX → LuaLaTeX 转换报告")
    print("=" * 60)
    print(f"  源文件: {r['input']}")
    print(f"  输出文件: {r['output_path']}")
    print(f"  自动转换: {r['stats'].get('auto', 0)} 处")
    print(f"  待人工确认: {len(r['manual_items'])} 项")
    print()

    if r["changes"]:
        auto_changes = [c for c in r["changes"] if c["severity"] == "auto"]
        if auto_changes:
            print(f"--- 自动转换 ({len(auto_changes)} 处) ---")
            for c in auto_changes:
                print(f"  行 {c['line']:>4d} | {c['description']}")
                print(f"        原: {c['original']}")

    if r["manual_items"]:
        print()
        print("--- ⚠ 需要人工确认的项 ---")
        print("  以下内容可能影响文档外观，请检查后决定是否调整：")
        for item in r["manual_items"]:
            print(f"  行 {item['line']:>4d} | {item['description']}")
            print(f"        内容: {item['content']}")

    print()
    print("  原文件未修改。新文件已保存至:")
    print(f"    {r['output_path']}")
    print()
    print("  下一步建议:")
    print(f"    1. 用 LuaLaTeX 编译新文件:")
    print(f"       lualatex {os.path.basename(r['output_path'])}")
    print(f"    2. 检查编译结果和文档外观")
    print(f"    3. 处理待人工确认的项")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="LaTeX 引擎转换器 — pdfLaTeX → LuaLaTeX",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )

    parser.add_argument("source", help="源 .tex 文件")
    parser.add_argument("--to", default="lualatex", choices=["lualatex"],
                        help="目标引擎（当前仅支持 lualatex）")
    parser.add_argument("--output", "-o", default="", help="输出文件路径（默认: 源文件名_lualatex.tex）")
    args = parser.parse_args()

    if not os.path.isfile(args.source):
        print(f"[ERROR] 文件不存在: {args.source}")
        sys.exit(1)

    r = convert_pdflatex_to_lualatex(args.source)

    if args.output and r["output_path"]:
        shutil.move(r["output_path"], args.output)
        r["output_path"] = args.output

    print_report(r)


if __name__ == "__main__":
    main()
