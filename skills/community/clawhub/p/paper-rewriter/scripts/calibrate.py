# -*- coding: utf-8 -*-
"""calibrate — 密度阈值校准证据工具（v5.9.0）。

把评分里的密度阈值（em-dash/「——」/段落开头五信号（词密度/段落占比两类））从文档声明变成
可复核证据：在指定语料目录上逐文件实测信号密度，输出「阈值 vs 人稿/AI 稿
分布」校准表。口径与运行时评分完全一致——阈值单一真源 =
`hxt_core.DENSITY_THRESHOLDS`（本工具与 scan() 共用同一张表，不存在第二处
字面量）。

校准判据（机器可验，exit code 承载）：
  - 人稿语料（文件名 human_ 开头）不得触发任何密度信号——触发即 exit 1
    （阈值把正当修辞误伤 = 校准失效，必须回炉）；
  - AI 稿语料（ai_ 开头）触发与否只记录不判定（演示语料非金标，命中数据
    仅供分布参考，不构成检测力声明——本工具不做也不支持「检测器」口径）。

语料：
  - 包内随附精简演示语料 `references/calib_corpus/`（合成演示句段，6 文件，
    非任何真实稿件、非任何外部项目语料）；
  - 开发仓库另有全量 `tests/corpus_*.txt`，用 `--corpus-dir tests` 指定；
  - 任意目录皆可（`--corpus-dir 你的目录`，按 ai_*/human_* 前缀分组）。

零网络、零子进程、只读语料与包内模块、不写盘。

用法：
  python scripts/calibrate.py                 # 人读校准表
  python scripts/calibrate.py --corpus-dir tests
  python scripts/calibrate.py --json          # 机器可读
"""
import json
import os
import re
import sys
import glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.dont_write_bytecode = True
sys.path.insert(0, HERE)

import hxt_core

TH = hxt_core.DENSITY_THRESHOLDS


def _scan_file(path):
    with open(path, encoding="utf-8", errors="replace") as f:
        text = f.read()
    lang = hxt_core.detect_language(text)
    r = hxt_core.scan(text, lang=None, profile="academic", source_ext=".txt")
    st = r.get("stats") or {}
    return {
        "file": os.path.basename(path),
        "group": "human" if "human" in os.path.basename(path).lower() else "ai",
        "lang": r.get("lang") or lang,
        "score": r.get("score"),
        "densities": {sig: st.get(spec[0]) for sig, spec in TH.items()},
        "counts": {sig: st.get(spec[5]) for sig, spec in TH.items()},
        "scales": {sig: (st.get(spec[3]) if spec[3] else None)
                   for sig, spec in TH.items()},
        "hit_categories": sorted(r.get("categories") or {}),
    }


def calibrate(corpus_dir):
    files = sorted(glob.glob(os.path.join(corpus_dir, "*.txt")))
    if not files:
        raise ValueError("语料目录无 .txt：%s" % corpus_dir)
    entries = [_scan_file(f) for f in files]

    rows = []
    for sig, spec in TH.items():
        _, thr, min_hits, scale_key, scale_min, _cnt, desc = spec
        human_hit = [e for e in entries if e["group"] == "human"
                     and e["densities"][sig] is not None
                     and (scale_key is None
                          or (e["scales"][sig] or 0) >= (scale_min or 0))
                     and e["densities"][sig] >= thr
                     and (e["counts"][sig] or 0) >= min_hits]
        human_d = [e["densities"][sig] for e in entries
                   if e["group"] == "human" and e["densities"][sig] is not None]
        ai_d = [e["densities"][sig] for e in entries
                if e["group"] == "ai" and e["densities"][sig] is not None]
        rows.append({
            "signal": sig,
            "threshold": thr,
            "min_hits": min_hits,
            "scale_gate": ("%s≥%s" % (scale_key, scale_min)) if scale_key else "段落≥5",
            "human_max": max(human_d) if human_d else None,
            "ai_values": sorted(ai_d, reverse=True),
            # 与运行时完全同款条件（规模门槛 AND 密度达标 AND 命中数达标）=human_clears False
            # 才算真正触发；只到密度未到命中数的属「贴近但未触发」，不算失效
            "human_clears": not human_hit,
            "human_hit_files": [e["file"] for e in human_hit],
            "desc": desc,
        })

    human_files = [e["file"] for e in entries if e["group"] == "human"]
    if not human_files:
        rows.append({"signal": "__warning__", "threshold": None,
                     "min_hits": None, "scale_gate": None, "human_max": None,
                     "ai_values": [], "human_clears": True,
                     "human_hit_files": [],
                     "desc": "人稿组为空（目录内无 human* 文件）——本次校准无人稿判据，"
                             "CALIBRATION_OK 属空真，请补 human_* 语料后重跑"})
    violations = ["%s: 人稿 %s 触发（密度=%.2f ≥ %.2f 且命中 ≥%d）=校准失效"
                  % (r["signal"], ",".join(r["human_hit_files"]) or "?",
                     r["human_max"], r["threshold"], r["min_hits"])
                  for r in rows if not r["human_clears"]]
    return {"corpus_dir": os.path.relpath(corpus_dir, ROOT),
            "files": entries, "table": rows, "violations": violations}


def _render(rep):
    lines = ["=" * 66,
             "密度阈值校准表（阈值真源 = hxt_core.DENSITY_THRESHOLDS）",
             "语料: %s（%d 文件，ai_*/human_* 前缀分组）" % (
                 rep["corpus_dir"], len(rep["files"])),
             "=" * 66]
    for r in rep["table"]:
        if r["signal"] == "__warning__":
            lines.append("⚠ %s" % r["desc"])
            continue
        hm = "无数据" if r["human_max"] is None else "%.3f" % r["human_max"]
        ai = " ".join("%.2f" % v for v in r["ai_values"]) or "无数据"
        ok = "✓ 人稿未触发" if r["human_clears"] else "✗ 人稿触发: %s（校准失效）" % ",".join(r["human_hit_files"])
        lines.append("信号 %s｜阈值 %s（%s）" % (r["signal"], r["threshold"], r["scale_gate"]))
        lines.append("  %s" % r["desc"])
        lines.append("  人稿最大密度: %s | AI 稿密度: %s → %s" % (hm, ai, ok))
    lines.append("-" * 66)
    if rep["violations"]:
        lines.append("CALIBRATION_FAIL（%d 项）:" % len(rep["violations"]))
        lines.extend("  - " + v for v in rep["violations"])
    else:
        lines.append("CALIBRATION_OK（全部密度信号在人稿语料上低于阈值——校准成立）")
    return "\n".join(lines)


def main():
    argv = sys.argv[1:]
    as_json = "--json" in argv
    pos = [a for a in argv if not a.startswith("--")]
    cdir = None
    if "--corpus-dir" in argv:
        i = argv.index("--corpus-dir")
        if i + 1 >= len(argv) or argv[i + 1].startswith("--"):
            print("错误: --corpus-dir 需要目录参数", file=sys.stderr)
            sys.exit(2)
        cdir = argv[i + 1]
    if not cdir:
        bundled = os.path.join(ROOT, "references", "calib_corpus")
        cdir = bundled if os.path.isdir(bundled) else os.path.join(ROOT, "tests")
    try:
        rep = calibrate(cdir)
    except ValueError as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)
    if as_json:
        print(json.dumps(rep, ensure_ascii=False, indent=1))
    else:
        print(_render(rep))
    sys.exit(1 if rep["violations"] else 0)


if __name__ == "__main__":
    main()
