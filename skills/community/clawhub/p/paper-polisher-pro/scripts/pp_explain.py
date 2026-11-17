#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_explain.py — 报告解读器（v6.1.0 新增；`pp.py explain`）

把 workflow / detect 的 JSON 报告翻译成任何人都能用的三段人话：
  【结论】现在分数多少、处于什么档位、一句话定性
  【证据】分层证据要点：段落 hi/med/lo、门禁判定、术语/规范 findings 概览
  【行动清单】按报告内容给出可直接执行的下一步命令（不是泛泛建议）

设计边界（诚实）：
  - 只解读既有报告，绝不重跑引擎；分数是引擎口径相对参考
  - 降级档/英文/混写等限制沿用报告自带字段如实转述
  - 不评分、不判定，行动清单只指路不代改

零依赖、零网络。
用法:
  python3 pp_explain.py draft.workflow.json
  python3 pp_explain.py detect.json --json
"""
import argparse
import html
import json
import sys
from pathlib import Path


def _load(path):
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"文件不存在: {p}")
    d = json.loads(p.read_text(encoding="utf-8"))
    if "detect" in d:
        wf = d
    elif "overall_ai_score" in d:
        wf = {"detect": d}
    else:
        raise ValueError("不是可解读的报告（需要 workflow JSON 或 detect JSON）")
    return wf


def explain(wf):
    det = wf.get("detect") or {}
    score = det.get("overall_ai_score")
    risk = det.get("overall_risk", "unknown")
    degraded = det.get("degraded_mode")
    paras = wf.get("paragraphs") or {}
    mixed = wf.get("mixed_document") or {}
    gate = wf.get("gate") or {}
    norm = wf.get("style_norm") or {}
    ledger = wf.get("findings_ledger") or {}

    lines = []
    # ── 结论 ──
    mode = "降级档（纯规则+词频谱，无监督模型）" if degraded else "融合档（监督层在位）"
    qual = {"high": "AI 痕迹特征显著", "medium": "存在可疑 AI 痕迹特征，需人工复核",
            "low": "未见明显 AI 痕迹特征", "unknown": "信息不足，无法判定"}.get(risk, risk)
    lines.append("【结论】")
    lines.append(f"  本文档 AI 分 {score}/100，风险带 {risk}——{qual}。当前引擎档位：{mode}。")
    if degraded:
        lines.append("  ⚠️ 降级档下医学文本会被系统性高估：医学内容只采信 @high 判定"
                     "（监督模型获取：python3 scripts/pp_setup.py --guide）。")
    if mixed.get("detected"):
        lines.append("  ⚠️ 检出人机混写信号：文档级分数会被稀释或顶起（原理性局限），"
                     "请以下方段落归因为准逐段处理，不要只看总分。")

    # ── 证据 ──
    lines.append("")
    lines.append("【证据】")
    if paras.get("items") is not None:
        lines.append(f"  段落分级：高 {paras.get('high', '?')} / 中 {paras.get('medium', '?')}"
                     f" / 低 {paras.get('low', paras.get('total', '?'))}（共 {paras.get('total', '?')} 段）")
        items = sorted(paras.get("items", []), key=lambda r: -(r.get("score", 0) or 0))
        for it in items[:3]:
            lines.append(f"    · 段 {it.get('index', '?')}（{it.get('score', '?')} 分，"
                         f"{it.get('class', '?')}）：{str(it.get('excerpt', ''))[:40]}")
    elif det.get("paragraph_scores"):
        ps = sorted(det["paragraph_scores"], key=lambda r: -(r.get("ai_score", 0) or 0))[:3]
        for it in ps:
            lines.append(f"    · 段 {(it.get('index', 0)) + 1}（{it.get('ai_score', '?')} 分）："
                         f"{str(it.get('text', ''))[:40]}")
    gv = {k: gate[k] for k in ("composite", "composite_ai_risk", "verdict") if k in gate}
    if gv:
        lines.append(f"  四层门禁：{gv}")
    sn = norm.get("findings") or []
    if sn:
        names = {"fullwidth": "全半角", "numbers": "数字用法", "abbrev": "缩写定义",
                 "units": "单位格式", "consistency": "术语一致性", "llm_jargon": "LLM 腔"}
        agg = {}
        for f in sn:
            k = names.get(f.get("check"), f.get("check"))
            agg[k] = agg.get(k, 0) + (f.get("count") or 0)
        tops = "、".join(f"{k}×{v}" for k, v in agg.items())
        lines.append(f"  规范自查发现 {norm.get('finding_count', len(sn))} 条：{tops}"
                     "（不评分，供润稿参考）")
    fx = wf.get("fix_suggest") or {}
    if fx.get("stats"):
        st = fx["stats"]
        lines.append(f"  句子级建议：标记 {st.get('flagged_sentences', '?')}/{st.get('total_sentences', '?')}"
                     " 句带可改进特征（详见 pp.py fix）")

    # ── 行动清单 ──
    lines.append("")
    lines.append("【行动清单】（按优先级）")
    acts = []
    if mixed.get("detected"):
        acts.append("逐段人工复核：python3 scripts/pp.py paragraph <文稿>（混写场景下这是唯一可信信号）")
    if fx.get("stats") and (fx["stats"].get("flagged_sentences") or 0) > 0:
        acts.append(f"按句改写：python3 scripts/pp.py fix <文稿> --top 10（只指位+策略，改不改你定）")
    if sn:
        acts.append("规范清理：python3 scripts/pp.py norm <文稿>（全半角/数字/缩写/单位/LLM 腔逐条看）")
    if (wf.get("terms") or {}).get("standardization_rate") not in (None, ""):
        acts.append("术语统一：python3 scripts/pp.py term <文稿>（同概念异写混用会逐条列出）")
    acts.append("多轮改稿后看趋势：python3 scripts/pp.py trend <报告目录>（分数下降≠内容更好，以质量为准）")
    acts.append("投稿前打包自查：python3 scripts/pp.py bundle <文稿>（一条命令产出全部自查产物）")
    for i, a in enumerate(acts, 1):
        lines.append(f"  {i}. {a}")
    notice = wf.get("integrity_notice")
    if notice:
        lines.append("")
        lines.append(f"  ℹ️ {notice}")
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("input", help="workflow JSON 或 detect JSON")
    ap.add_argument("--json", action="store_true", help="额外输出结构化 JSON")
    a = ap.parse_args()
    wf = _load(a.input)
    text = explain(wf)
    print(text)
    if a.json:
        print(json.dumps({"explained": str(a.input)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        sys.exit(main())
    except FileNotFoundError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("  下一步: 检查路径；支持 .workflow.json（pp.py workflow 产物）或 detect 输出 JSON",
              file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        print("  下一步: 先跑 python3 scripts/pp.py workflow <文稿> 生成可解读的报告", file=sys.stderr)
        sys.exit(2)
