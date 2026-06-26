#!/usr/bin/env python3
"""
论文精读翻译 — 自动化校验脚本
用法: python3 validate_translation.py <markdown_file>

检查项:
1. 章节完整性（摘要/引言/相关工作/方法/实验/结论/参考文献）
2. LaTeX 兼容性（\bm 出现次数必须为 0）
3. 译注标记（> **[译注]** 格式，数量 > 0）
4. 参考文献条数
5. 图片链接格式
6. 首行元信息
"""

import re
import sys
from pathlib import Path


def validate(filepath: str) -> list[dict]:
    """Validate a translation markdown file. Returns list of check results."""
    path = Path(filepath)
    if not path.exists():
        print(f"ERROR: File not found: {filepath}")
        sys.exit(1)

    content = path.read_text(encoding="utf-8")
    lines = content.split("\n")
    results = []

    # --- 1. 章节完整性 ---
    required_sections = {
        "摘要": r"(摘要|Abstract)",
        "引言": r"(引言|Introduction|1[\.\s])",
        "相关工作": r"(相关工作|Related Work)",
        "方法": r"(方法|Method|Approach|Architecture|Model|Framework)",
        "实验": r"(实验|Experiment|Evaluation|Result)",
        "结论": r"(结论|Conclusion|Discussion)",
        "参考文献": r"(参考文献|References|Bibliography)",
    }
    headers = [l for l in lines if l.startswith("#")]
    header_text = " ".join(headers)

    missing = []
    for name, pattern in required_sections.items():
        if not re.search(pattern, header_text, re.IGNORECASE):
            missing.append(name)

    results.append({
        "check": "章节完整性",
        "status": "PASS" if not missing else "WARN",
        "detail": f"缺少: {', '.join(missing)}" if missing else "所有核心章节均存在",
    })

    # --- 2. LaTeX 兼容性 ---
    bm_count = len(re.findall(r"\\bm\b", content))
    results.append({
        "check": "LaTeX 兼容性 (\\bm)",
        "status": "PASS" if bm_count == 0 else "FAIL",
        "detail": f"\\bm 出现 {bm_count} 次" + ("" if bm_count == 0 else " — 必须全部替换为 \\boldsymbol"),
    })

    # --- 3. 译注标记 ---
    notes = re.findall(r">\s*\*\*\[译注\]\*\*", content)
    note_count = len(notes)
    results.append({
        "check": "译注标记",
        "status": "PASS" if note_count > 0 else "WARN",
        "detail": f"共 {note_count} 处译注" + ("" if note_count > 0 else " — 建议至少添加 1 处译注"),
    })

    # --- 4. 参考文献条数 ---
    # 匹配 [数字] 开头的引用条目
    refs = re.findall(r"^\s*\[\d+\]", content, re.MULTILINE)
    results.append({
        "check": "参考文献",
        "status": "INFO",
        "detail": f"共 {len(refs)} 条（请与原文核对）",
    })

    # --- 5. 图片链接 ---
    img_links = re.findall(r"!\[.*?\]\((.*?)\)", content)
    arxiv_imgs = [l for l in img_links if "arxiv.org" in l]
    base64_imgs = [l for l in img_links if l.startswith("data:image")]
    imageid_imgs = [l for l in img_links if not l.startswith("http") and not l.startswith("data:") and len(l) > 5]
    local_imgs = [l for l in img_links if l.startswith("./") or l.startswith("../") or l.startswith("/")]

    results.append({
        "check": "图片链接",
        "status": "WARN" if local_imgs else "PASS",
        "detail": (
            f"ArXiv 外链: {len(arxiv_imgs)}, Base64: {len(base64_imgs)}, "
            f"Image ID: {len(imageid_imgs)}, 本地路径: {len(local_imgs)}"
            + (" — 本地路径在 IMA 上传后会失效!" if local_imgs else "")
        ),
    })

    # --- 6. 首行元信息 ---
    first_lines = "\n".join(lines[:20])
    has_title = bool(re.search(r"(论文|Paper|标题|Title)", first_lines, re.IGNORECASE))
    has_link = bool(re.search(r"arxiv\.org", first_lines))
    has_model = bool(re.search(r"(翻译辅助|大模型|Model|Claude|GPT|Gemini|Opus)", first_lines, re.IGNORECASE))

    meta_items = []
    if not has_title:
        meta_items.append("论文标题")
    if not has_link:
        meta_items.append("ArXiv 链接")
    if not has_model:
        meta_items.append("翻译大模型名称")

    results.append({
        "check": "首行元信息",
        "status": "PASS" if not meta_items else "WARN",
        "detail": f"缺少: {', '.join(meta_items)}" if meta_items else "标题、链接、大模型名称均存在",
    })

    return results


def main():
    if len(sys.argv) < 2:
        print("用法: python3 validate_translation.py <markdown_file>")
        sys.exit(1)

    filepath = sys.argv[1]
    print(f"\n{'='*60}")
    print(f"  论文翻译校验报告")
    print(f"  文件: {filepath}")
    print(f"{'='*60}\n")

    results = validate(filepath)

    pass_count = sum(1 for r in results if r["status"] == "PASS")
    fail_count = sum(1 for r in results if r["status"] == "FAIL")
    warn_count = sum(1 for r in results if r["status"] == "WARN")

    for r in results:
        icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️", "INFO": "ℹ️"}[r["status"]]
        print(f"  {icon} [{r['status']}] {r['check']}: {r['detail']}")

    print(f"\n{'─'*60}")
    print(f"  结果: ✅ {pass_count} 通过 | ❌ {fail_count} 失败 | ⚠️ {warn_count} 警告")
    print(f"{'─'*60}\n")

    if fail_count > 0:
        print("  ❌ 存在 FAIL 项，请修复后重新校验！\n")
        sys.exit(1)
    elif warn_count > 0:
        print("  ⚠️ 存在 WARN 项，建议检查后再上传。\n")
    else:
        print("  ✅ 所有检查通过，可以上传！\n")


if __name__ == "__main__":
    main()
