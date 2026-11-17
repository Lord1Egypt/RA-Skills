#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_report_bundle.py — 投稿前自查包（v5.3.0 新增）

把分散的自查工具收口成一个交付物：一条命令产出带时间戳的自查目录——

  bundle_<文件名>_<时间戳>/
    ├── README.md                 清单 + 阅读顺序 + 诚信声明
    ├── workflow.md / .json       端到端综合报告（检测/段落/门禁/术语/翻译腔/文体/质量/标识/规范）
    ├── paragraph_report.html     段落级归因（可视化）
    ├── fix_suggest.txt           句子级改写建议
    └── style_norm.txt            学术写作规范自查

用法:
  python3 pp_report_bundle.py draft.txt --outdir ~/selfcheck
  python3 pp_report_bundle.py thesis.docx            # docx 直读（v5.3.0）

零网络；产物只写到 --outdir（默认与输入同目录）。
"""
import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

_INTEGRITY = ("本自查包由 Paper Polisher Pro 生成，供作者投稿前自查与改进写作质量；"
              "所有分数为引擎口径的相对参考，不与任何机构检测器互换；"
              "请按所在机构政策规范披露 AI 使用（标识合规可用 aigc_label_check.py 自查）。")

_READ_ORDER = """## 阅读顺序建议

1. `workflow.md` — 先看全局：AI 率、段落归因、门禁、术语/翻译腔/文体、质量、合规标识、规范自查（九节一屏）
2. `paragraph_report.html` — 混写/高分段逐段定位（浏览器打开）
3. `fix_suggest.txt` — 逐句改写建议（指位+策略，不代改）
4. `style_norm.txt` — 体例核对（全半角/数字/缩写/单位）
"""


def build_bundle(input_path: str, outdir: str = None, lang: str = "auto") -> dict:
    """生成自查包，返回 {bundle_dir, files:{...}}。输入不合法抛 ValueError 族。"""
    p = Path(input_path)
    if not p.exists():
        raise ValueError(f"文件不存在: {p}")
    from docx_text import read_text_any
    text = read_text_any(p)
    if len(text.strip()) < 100:
        raise ValueError("文本不足 100 字（铁律 2：短文本不出判定），请提交 100 字以上")

    stamp = datetime.now().strftime("%Y%m%d_%H%M")
    bundle_dir = Path(outdir) if outdir else p.parent
    bundle_dir = Path(bundle_dir) / f"selfcheck_{p.stem}_{stamp}"
    bundle_dir.mkdir(parents=True, exist_ok=True)
    files = {}

    # 1) workflow（MD + JSON）
    import pp_workflow
    r = pp_workflow.workflow(text, lang=lang)
    (bundle_dir / "workflow.json").write_text(
        json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    (bundle_dir / "workflow.md").write_text(pp_workflow.to_markdown(r), encoding="utf-8")
    files["workflow"] = ["workflow.md", "workflow.json"]

    # 2) 段落级 HTML（子进程调用，与文档口径一致）
    fd_txt = bundle_dir / "_input.txt"
    fd_txt.write_text(text, encoding="utf-8")
    import subprocess
    subprocess.run([sys.executable, str(HERE / "paragraph_report.py"),
                    str(fd_txt), "--output", str(bundle_dir / "paragraph_report.html")],
                   capture_output=True, text=True)
    if (bundle_dir / "paragraph_report.html").exists():
        files["paragraph"] = ["paragraph_report.html"]

    # 3) 句子级改写建议
    try:
        import pp_fix_suggest
        sug, stats, slang = pp_fix_suggest.analyze(text, lang=lang if lang != "auto" else "auto")
        (bundle_dir / "fix_suggest.txt").write_text(
            pp_fix_suggest.to_text(sug, stats, slang, top=None), encoding="utf-8")
        files["fix_suggest"] = ["fix_suggest.txt"]
    except Exception as e:
        (bundle_dir / "fix_suggest.txt").write_text(f"生成失败: {e}", encoding="utf-8")

    # 4) 学术规范自查
    try:
        import pp_style_norm
        nr = pp_style_norm.style_norm(text)
        (bundle_dir / "style_norm.txt").write_text(
            pp_style_norm.to_text(nr), encoding="utf-8")
        files["style_norm"] = ["style_norm.txt"]
    except Exception as e:
        (bundle_dir / "style_norm.txt").write_text(f"生成失败: {e}", encoding="utf-8")

    # manifest
    d = r["detect"]
    manifest = [
        f"# 投稿前自查包 — {p.name}",
        "",
        f"- 生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ｜ 引擎版本: {r['engine_version']}",
        f"- 文档级 AI 率: {d.get('overall_ai_score')} / 风险档 {d.get('overall_risk')}"
        f"（引擎档位: {'完整（监督层融合）' if d.get('degraded_mode') is False else '降级（纯规则+词频谱）'}）",
        f"- 输入: {p.name}（{r['length_chars']} 字）",
        "",
        _READ_ORDER,
        "",
        "## 产物清单",
        "",
    ]
    for k, names in files.items():
        for n in names:
            manifest.append(f"- `{n}`")
    manifest += ["", "---", "学术诚信声明：" + _INTEGRITY.replace("学术诚信：", "", 1), ""]
    (bundle_dir / "README.md").write_text("\n".join(manifest), encoding="utf-8")
    files["manifest"] = ["README.md"]

    fd_txt.unlink(missing_ok=True)
    return {"bundle_dir": str(bundle_dir), "files": files, "summary": {
        "ai_score": d.get("overall_ai_score"), "risk": d.get("overall_risk"),
        "length": r["length_chars"], "engine_version": r["engine_version"],
    }}


def main():
    ap = argparse.ArgumentParser(description="投稿前自查包（一条命令产出全部自查产物）")
    ap.add_argument("file")
    ap.add_argument("--outdir", default=None, help="输出目录（默认与输入同目录）")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    args = ap.parse_args()
    try:
        r = build_bundle(args.file, outdir=args.outdir, lang=args.lang)
    except ValueError as e:
        from pp_errors import print_friendly
        print_friendly(e)
        return 2
    except Exception as e:
        from pp_errors import print_friendly
        print(f"ERROR: 自查包生成失败", file=sys.stderr)
        print_friendly(e)
        return 1
    s = r["summary"]
    print(f"自查包: {r['bundle_dir']}")
    print(f"概要: AI 率 {s['ai_score']} / {s['risk']} ｜ {s['length']} 字 ｜ 引擎 {s['engine_version']}")
    for k, names in r["files"].items():
        print(f"  · {k}: {', '.join(names)}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
