# -*- coding: utf-8 -*-
"""compare.py — 前后对比：风格特征分变化 + 完整性守卫摘要。

用法:
    python scripts/compare.py 原稿.txt 改稿.txt            # 对比两份
    python scripts/compare.py 原稿.txt -o 改稿.txt         # 先机械清洗再对比并落盘
    python scripts/compare.py 原稿.txt 改稿.txt --terms t.txt
退出码: 0 完成（含完整性 FAIL 也算完成，看报告）| 2 用法/文件错误
"""

import argparse
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core
import transform as tf
import verify as vf


def _read(path):
    try:
        return hxt_core.read_text(path)
    except OSError as e:
        print("错误: 无法读取 %s（%s）" % (path, e), file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)


def _score(text):
    return hxt_core.scan(text)


def main():
    ap = argparse.ArgumentParser(description="风格改写前后对比 + 完整性守卫")
    ap.add_argument("orig", help="原稿")
    ap.add_argument("new", nargs="?", help="改稿（缺省=先做机械清洗）")
    ap.add_argument("-o", "--output", help="机械清洗结果落盘文件（配 new 缺省时）")
    ap.add_argument("-a", "--aggressive", action="store_true")
    ap.add_argument("--terms", help="术语表")
    ap.add_argument("--profile", choices=["academic", "general"], default="academic",
                    help="academic=论文口径（默认）；general=非学术文本")
    ap.add_argument("--html", help="生成单文件 HTML 对照报告（含逐句 diff）到此路径")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--version", action="version", version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    orig = _read(args.orig)
    if not orig.strip():
        print("错误: 输入为空", file=sys.stderr)
        sys.exit(2)
    if args.new:
        new = _read(args.new)
        mode = "对比已有改稿"
    else:
        fixes = tf.load_fixes(None, args.aggressive)
        new, applied = tf.apply_auto_fixes(orig, fixes)
        new, removed = tf.drop_flagged_sentences(new)
        new, nq = tf.normalize_quotes(new)
        if args.output:
            try:
                with open(args.output, "w", encoding="utf-8") as f:
                    f.write(new)
            except OSError as e:
                print("错误: 无法写入 %s（%s）" % (args.output, e), file=sys.stderr)
                sys.exit(2)
        mode = "机械清洗（%d 类修复；深度改写请 agent 按 references 指南执行后重跑本命令）" % len(applied)

    ro = hxt_core.scan(orig, profile=args.profile)
    rn = hxt_core.scan(new, profile=args.profile)
    vr = vf.verify(orig, new,
                   vf.load_terms(args.terms) if args.terms else None)

    if args.html:
        import reporter
        with open(args.html, "w", encoding="utf-8") as hf:
            hf.write(reporter.render_compare(orig, new, ro, rn, vr))
        print("HTML 对照报告已写入 %s" % args.html, file=sys.stderr)

    if args.json:
        print(json.dumps({
            "mode": mode,
            "before": {k: ro[k] for k in ("score", "level", "lang", "units", "sentences")},
            "after": {k: rn[k] for k in ("score", "level", "lang", "units", "sentences")},
            "categories_removed": _delta(ro["categories"], rn["categories"]),
            "verify": vr,
        }, ensure_ascii=False, indent=2))
        sys.exit(0)

    print("=" * 62)
    print("改写前后对比（%s）" % mode)
    print("=" * 62)
    print("风格特征分: %d [%s]  →  %d [%s]  （%+d）" % (
        ro["score"], ro["level"], rn["score"], rn["level"], rn["score"] - ro["score"]))
    if ro["critical_hit"] and not rn["critical_hit"]:
        print("模型残留（硬特征）: 已清除 ✓")
    elif ro["critical_hit"] and rn["critical_hit"]:
        print("⚠ 仍存在模型残留，先跑 transform.py 清理")
    delta = _delta(ro["categories"], rn["categories"])
    if delta:
        print("分类变化（相对原稿）:")
        for label, d in delta:
            if d > 0:
                print("  %-28s 已清除 %d 处" % (label, d))
            else:
                print("  %-28s 新增 %d 处" % (label, -d))
    print()
    print("完整性守卫: %s" % ("PASS ✓" if vr["ok"] else "FAIL ✗"))
    for v in vr["violations"]:
        print("  ✗ [%s] %s" % (v["check"], v["detail"]))
    for w in vr["warnings"]:
        print("  ⚠ [%s] %s" % (w["check"], w["detail"]))
    print()
    if rn["score"] >= 40:
        print("结论: 机械清理后仍有模板腔特征 —— 需要 agent 按 references/style_guide 深改")
        print("      （黑话替换/八股拆解/句式节奏），改完重跑本命令复核。")
    else:
        print("结论: 痕迹已明显下降；深改请仍按指南复核语义自然度（机器分≠官方检测器分）。")
    sys.exit(0)


def _delta(cats_o, cats_n):
    rows = []
    for cid, c in cats_o.items():
        d = c["count"] - cats_n.get(cid, {}).get("count", 0)
        if d:
            rows.append((c["label"], d))
    for cid, c in cats_n.items():
        if cid not in cats_o and c["count"]:
            rows.append((c["label"], c["count"]))
    return sorted(rows, key=lambda x: -abs(x[1]))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
