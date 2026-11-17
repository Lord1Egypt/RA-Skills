# -*- coding: utf-8 -*-
"""detect.py — 风格特征自查（本地启发式，非任何官方检测分数）。

用法:
    python scripts/detect.py 文件.txt
    python scripts/detect.py 文件.txt -j          # JSON 输出
    python scripts/detect.py 文件.txt -s          # 只看分数
    python scripts/detect.py 文件.txt --lang zh   # 强制语言
    echo "文本" | python scripts/detect.py        # stdin

退出码: 0 正常 | 2 用法/文件错误
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core

LEVELS = {"低": "基本无模板腔特征", "中": "有一定模板腔特征", "高": "模板腔特征明显", "极高": "模板腔特征极重/含模型残留"}


def main():
    ap = argparse.ArgumentParser(description="写作风格特征自查（本地启发式）")
    ap.add_argument("file", nargs="?", help="文本文件；缺省读 stdin（--batch 模式下传目录）")
    ap.add_argument("-j", "--json", action="store_true", help="JSON 输出")
    ap.add_argument("-s", "--score", action="store_true", help="只输出分数与档位")
    ap.add_argument("--lang", choices=["zh", "en", "mix", "auto"], default="auto")
    ap.add_argument("--profile", choices=["academic", "general"], default="academic",
                    help="academic=论文口径（默认）；general=非学术文本，八股/公文信号降权")
    ap.add_argument("--suggestions", help="输出修订建议工作单（markdown 侧车）到此路径")
    ap.add_argument("--html", help="生成单文件 HTML 报告到此路径")
    ap.add_argument("--batch", help="批量模式：扫描目录内全部 .txt/.md/.docx，输出汇总 CSV 到此路径（与 --html 可同用）")
    ap.add_argument("--structure", action="store_true",
                    help="章节感知：识别论文结构（摘要/引言/方法/结果/讨论），分章节评分（方法/结果自动降权）")
    ap.add_argument("--version", action="version", version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    if args.batch:
        root = args.batch
        if not os.path.isdir(root):
            print("错误: --batch 需要目录（%s）" % root, file=sys.stderr)
            sys.exit(2)
        rows_out = []
        for fn in sorted(os.listdir(root)):
            if not fn.lower().endswith((".txt", ".md", ".docx")):
                continue
            fp = os.path.join(root, fn)
            try:
                t = hxt_core.read_text(fp)
                if not t.strip():
                    rows_out.append((fn, -1, "空文件", False, "-"))
                    continue
                rr = (hxt_core.scan_chunked(t, lang=None if args.lang == "auto" else args.lang,
                                            profile=args.profile)
                      if len(t) > 1_000_000 else
                      hxt_core.scan(t, lang=None if args.lang == "auto" else args.lang,
                                    profile=args.profile))
                rows_out.append((fn, rr["score"], rr["level"], rr["critical_hit"], rr["lang"]))
            except (OSError, ValueError) as e:
                rows_out.append((fn, -1, "错误: %s" % str(e)[:40], False, "-"))
        if args.json:
            print(json.dumps([{"file": f, "score": s, "level": l, "critical": c, "lang": g}
                              for f, s, l, c, g in rows_out], ensure_ascii=False, indent=2))
        else:
            print("批量扫描 %d 个文件：" % len(rows_out))
            for f, s, l, c, g in rows_out:
                mark = (" %s/%s%s" % (s, l, " ⚠残留" if c else "")) if s >= 0 else (" %s" % l)
                print("  %-36s%s" % (f, mark))
        if args.html:
            import reporter
            trs = "".join("<tr><td>%s</td><td>%s</td></tr>" % (
                reporter.esc(f),
                ("%d [%s]%s" % (s, reporter.esc(l), " ⚠残留" if c else "")) if s >= 0
                else "<span class='bad'>%s</span>" % reporter.esc(l))
                for f, s, l, c, g in rows_out)
            body = ("<div class='card'><h1>批量扫描汇总</h1><p class='meta'>%d 个文件 · %s · "
                    "%s 模式</p></div>" % (len(rows_out), reporter.esc(root),
                                           "academic" if args.profile == "academic" else "general"))
            body += ("<div class='card'><table><tr><th>文件</th><th>结果</th></tr>%s</table></div>"
                     % trs) + reporter._FOOT.format(ts=reporter._now())
            with open(args.html, "w", encoding="utf-8") as hf:
                hf.write(reporter._page("批量扫描汇总", body))
            print("HTML 汇总已写入 %s" % args.html, file=sys.stderr)
        sys.exit(0)

    if args.file:
        try:
            text = hxt_core.read_text(args.file)
        except OSError as e:
            print("错误: 无法读取文件 %s（%s）" % (args.file, e), file=sys.stderr)
            sys.exit(2)
        except ValueError as e:
            print("错误: %s" % e, file=sys.stderr)
            sys.exit(2)
    else:
        text = sys.stdin.buffer.read().decode("utf-8-sig", errors="replace")

    if not text.strip():
        print("错误: 输入为空", file=sys.stderr)
        sys.exit(2)

    if args.structure:
        rs = hxt_core.scan_sections(text, lang=None if args.lang == "auto" else args.lang,
                                    profile=args.profile)
        if args.html:
            import reporter
            with open(args.html, "w", encoding="utf-8") as hf:
                hf.write(reporter.render_sections(rs, source=args.file or "(stdin)"))
            print("章节报告已写入 %s" % args.html, file=sys.stderr)
        if args.suggestions:
            print("[提示] --structure 模式暂不生成 --suggestions 工作单（工作单面向整文诊断）",
                  file=sys.stderr)
        if args.json:
            print(json.dumps(rs, ensure_ascii=False, indent=2))
            sys.exit(0)
        print("=" * 62)
        print("章节感知扫描（论文结构模式）")
        print("=" * 62)
        print("综合: %d [%s]" % (rs["overall_score"], rs["overall_level"]))
        for x in rs["sections"]:
            sc = ("%d [%s]" % (x["score"], x["level"])) if x["score"] is not None else "不扫描（引用列表）"
            print("  %-10s %s（%d 字符）" % (x["label"], sc, x["chars"]))
        if rs["missing_sections"]:
            print("  ⚠ 未识别到章节: %s（非 IMRaD 结构可忽略）" % "/".join(rs["missing_sections"]))
        print("口径: 方法/结果段已自动降权（文体常态）；本地启发式，非官方分数")
        sys.exit(0)

    if len(text) > 1_000_000:
        r = hxt_core.scan_chunked(text, lang=None if args.lang == "auto" else args.lang,
                                  profile=args.profile)
    else:
        r = hxt_core.scan(text, lang=None if args.lang == "auto" else args.lang,
                          profile=args.profile)

    if args.suggestions:
        guide = {"zh": "references/style_guide_zh.md",
                 "en": "references/style_guide_en.md"}.get(r["lang"],
                                                           "references/style_guide_zh.md")
        try:
            with open(args.suggestions, "w", encoding="utf-8") as f:
                f.write(hxt_core.build_suggestions(text, r, guide))
            print("修订建议工作单已写入 %s" % args.suggestions, file=sys.stderr)
        except OSError as e:
            print("错误: 无法写入 %s（%s）" % (args.suggestions, e), file=sys.stderr)
            sys.exit(2)

    if args.html:
        import reporter
        with open(args.html, "w", encoding="utf-8") as hf:
            hf.write(reporter.render_detect(text, r, source=args.file or "(stdin)"))
        print("HTML 报告已写入 %s" % args.html, file=sys.stderr)

    if args.score:
        print("%d/%s" % (r["score"], r["level"]))
        sys.exit(0)

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        sys.exit(0)

    # ---- 人类可读报告 ----
    lang_disp = {"zh": "中文", "en": "英文", "mix": "中英混合"}[r["lang"]]
    print("=" * 62)
    print("写作风格特征自查（本地启发式 · 非任何官方检测分数）")
    print("=" * 62)
    if args.file:
        print("文件: %s" % args.file)
    print("语言: %s | 规模: %s 单元 / %d 句 | 模式: %s" % (
        lang_disp, r["units"], r["sentences"],
        "学术论文(academic)" if r.get("profile") == "academic" else "非学术(general)"))
    print()
    print("综合评分: %d/100  [%s]" % (r["score"], r["level"]))
    if r["critical_hit"]:
        print("级别依据: 含模型残留/聊天客套/知识截止声明等硬特征 → 直接判「极高」")
    print()
    if r["categories"]:
        print("分类明细:")
        for cid in sorted(r["categories"], key=lambda k: -r["categories"][k]["count"] * r["categories"][k]["weight"]):
            c = r["categories"][cid]
            mark = " [可自动修]" if cid in hxt_core.AUTO_FIXABLE else ""
            print("  · %-28s %3d 处%s" % (c["label"], c["count"], mark))
            for s in c["samples"][:4]:
                print("      - %s" % s)
    else:
        print("未发现明显的模板腔/模型残留特征。")
    print()
    st = r["stats"]
    extra = []
    if st.get("burstiness_cv") is not None:
        extra.append("句长变异系数 %.2f" % st["burstiness_cv"])
    if st.get("connector_density") is not None:
        extra.append("连接词 %.2f/句" % st["connector_density"])
    if st.get("em_dash_density") is not None:
        extra.append("破折号 %.1f/千词" % st["em_dash_density"])
    if extra:
        print("节奏统计: %s" % " | ".join(extra))
    for note in st.get("notes", []):
        print("  ⚠ %s" % note)
    if r["guards_applied"]:
        print("术语保护: 豁免正当用法 %d 处（%s）" % (
            len(r["guards_applied"]),
            ", ".join("%s←%s" % (g["hit"], g["guard"]) for g in r["guards_applied"][:5])))
    if r["suggestions"]:
        print("改写建议(前%d条): " % len(r["suggestions"]))
        for s in r["suggestions"][:6]:
            print("  · 「%s」→ 「%s」" % (s["from"], s["to"]))
    print()
    print("下一步: python scripts/transform.py <文件> -o out.txt   # 机械清洗")
    print("       深度改写按 SKILL.md 工作流（agent 依指南执行）")
    print("       python scripts/compare.py 原稿.txt 改稿.txt      # 前后对比+完整性")
    sys.exit(0)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
