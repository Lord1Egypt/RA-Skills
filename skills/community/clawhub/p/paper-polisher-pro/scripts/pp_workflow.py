#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_workflow.py — 一条命令的端到端自查工作流（v4.6.0 新增）

回应官方评测 docQuality 项：把分散的六个检查收成一次调用，产出单一综合报告。
串联：AI率检测（融合引擎）→ 段落级归因 → 四层降AI门禁 → 术语保护 → 翻译腔 →
文体距离 → 质量报告 → AIGC 合规标识自查，输出 JSON + Markdown 双格式。

用法：
  python3 scripts/pp_workflow.py draft.txt [--outdir 报告目录] [--lang auto]
  # 产物: draft.workflow.json + draft.workflow.md（同目录）

编程接口:
  from pp_api import workflow            # 返回综合 JSON dict（不落盘）
  r = workflow("文本" * 200)
"""
import argparse
import json
import os
import sys
import tempfile
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
GITHUB_URL = "https://github.com/docsor1212/paper-polisher-pro"
SH_URL = "https://skillhub.cn/skills/indiv-sorsor/paper-polisher-pro"
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))


def workflow(text: str, lang: str = "auto") -> dict:
    """端到端自查：一次调用返回全部检查结果（JSON 兼容 dict）。

    键: detect / paragraphs / gate / terms / smell / style / quality /
        aigc_label / integrity_notice / engine_version / generated_at
    异常语义与 pp_api 一致：输入不合法 ValueError，运行失败 RuntimeError。
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    import ai_detector
    import pp_api

    result = {"engine_version": pp_api.engine_version(),
              "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
              "length_chars": len(text)}

    # 1) 融合检测（含监督层/降级披露/混写预警）
    rep = ai_detector.detect(text, lang=lang)
    result["detect"] = pp_api._asdict(rep)

    # 2) 段落级归因（与 paragraph_report.py 同口径：混合段落分+融合阈值分级）
    fc = ai_detector._load_fusion_config() or {}
    thr = fc.get("thresholds", {"medium": 0.35, "high": 0.60})
    tm, th = float(thr["medium"]) * 100, float(thr["high"]) * 100
    paras = ai_detector.split_paragraphs(text)
    blend = ai_detector.blended_paragraph_scores(text, rep)
    rows, n_hi, n_med = [], 0, 0
    for j, p in enumerate(rep.paragraph_scores):
        idx = min(p.get("index", 0), max(len(paras) - 1, 0))
        raw = paras[idx] if idx < len(paras) else p.get("text", "")
        s = blend[j] if j < len(blend) else p.get("ai_score", 0)
        cls = "hi" if s >= th else ("med" if s >= tm else "lo")
        n_hi += cls == "hi"
        n_med += cls == "med"
        rows.append({"index": j + 1, "score": round(float(s), 1), "class": cls,
                     "excerpt": raw.strip().replace("\n", " ")[:60]})
    result["paragraphs"] = {"thresholds": {"medium": round(tm, 1), "high": round(th, 1)},
                            "total": len(rows), "high": n_hi, "medium": n_med,
                            "items": rows}

    # 2b) 混写文档评估（v4.7.0）：段落双峰或引擎混写预警 → 给出段落级定位结论
    n_lo = len(rows) - n_hi - n_med
    mixed_detected = bool(getattr(rep, "mixed_signal", False)) or (len(rows) >= 3 and n_hi > 0 and n_lo > 0)
    # v4.9.0: 段落阈值采用混写基准校准结果（references/para_thresholds.json）
    para_thr = {}
    _pt = HERE.parent / "references" / "para_thresholds.json"
    try:
        para_thr = json.load(open(_pt, encoding="utf-8"))
    except Exception:
        para_thr = {}
    _cal = para_thr.get("recommended_high") or {}
    _honest = para_thr.get("honest_conclusion") or (
        "段落归因排序供人工复核；校准最优工作点精度有限，任何单段标记都需人工确认。")
    result["mixed_document"] = {
        "detected": mixed_detected,
        "hi": n_hi, "medium": n_med, "low": n_lo,
        "ai_paragraph_fraction_est": round((n_hi + 0.5 * n_med) / max(len(rows), 1), 2),
        "measured": {"document_level_auroc": "0.52-0.54",
                     "paragraph_level_auroc": 0.6883,
                     "calibrated_high_threshold": _cal.get("para_high"),
                     "calibrated_precision": _cal.get("precision"),
                     "source": "references/para_thresholds.json + eval/results/mixed_para_20261005.json"},
        "guidance": ("文档级分数不可单独采信（混写会稀释/顶起文档级均分，实测文档级 AUROC 0.52-0.54）。"
                     + _honest) if mixed_detected else "",
    }

    # 3) 四层门禁
    result["gate"] = pp_api.gate_text(text)
    # 3b) 句子级改写建议（v5.0.0）：检测之后的自然下一步——具体哪几句、因为什么、往哪改
    try:
        import pp_fix_suggest
        _sug, _stats, _slang = pp_fix_suggest.analyze(text, lang=lang if lang != "auto" else "auto")
        result["fix_suggest"] = {"stats": _stats, "language": _slang,
                                 "top_issues": [
                                     {"index": s["index"] + 1, "sentence": s["sentence"],
                                      "issues": [{"type": x["type"], "evidence": x["evidence"]}
                                                 for x in s["issues"]]}
                                     for s in _sug[:5]],
                                 "notice": ("改写建议是排序辅助：指位与策略供人工润稿参考，"
                                            "完整版见 pp.py fix（不代写，改写决定权在作者）。")}
    except Exception as e:  # 建议生成失败不阻断工作流（主链路照常交付）
        result["fix_suggest"] = {"stats": None, "error": str(e)}
    # 4-6) 术语 / 翻译腔 / 文体
    result["terms"] = pp_api.term_report(text)
    result["smell"] = pp_api.smell_report(text)
    result["style"] = pp_api.style_report(text)
    # 7) 质量报告 / 8) AIGC 合规标识（文件口径，临时文件中转）
    fd, tmp = tempfile.mkstemp(suffix=".txt")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write(text)
        import quality_report
        result["quality"] = pp_api._asdict(quality_report.generate_report(tmp))
        import aigc_label_check
        result["aigc_label"] = {"evidence": aigc_label_check.check_text(tmp),
                                "note": "显式标识自查；元数据/C2PA 检查用 aigc_label_check.py 对成品文件运行"}
    except Exception as e:
        raise RuntimeError("workflow 质量检查失败: %s" % e) from e
    finally:
        Path(tmp).unlink(missing_ok=True)

    # 9) 学术写作规范自查（v5.2.0）：体例核对，不评分
    try:
        import pp_style_norm
        result["style_norm"] = {"finding_count": 0, "findings": []}
        _nr = pp_style_norm.style_norm(text)
        result["style_norm"] = {"finding_count": _nr["finding_count"],
                                "findings": [{"check": f["check"], "severity": f["severity"],
                                              "count": f["count"], "examples": f["examples"],
                                              "advice": f["advice"]} for f in _nr["findings"]]}
    except Exception as e:  # 规范自查失败不阻断工作流
        result["style_norm"] = {"finding_count": 0, "findings": [], "error": str(e)}

    # 10) findings ledger（v5.5.0，模块 3.5）：各项检查的结论状态一览
    _fx_ok = bool((result.get("fix_suggest") or {}).get("stats"))
    result["findings_ledger"] = {
        "items": [
            {"check": "AI 率检测", "status": "answered",
             "detail": f"文档级 {result['detect'].get('overall_ai_score')}/{result['detect'].get('overall_risk')}"},
            {"check": "段落级归因", "status": "answered",
             "detail": f"hi {result['paragraphs'].get('high')} / medium {result['paragraphs'].get('medium')} / 共 {result['paragraphs'].get('total')}"},
            {"check": "人机混写判定", "status":
                "partially" if (result.get("mixed_document") or {}).get("detected") else "answered",
             "detail": ("混写判定仅排序辅助（校准精度有限，需逐段人工复核）"
                        if (result.get("mixed_document") or {}).get("detected")
                        else "未检出混写信号") },
            {"check": "句子级改写建议", "status": "answered" if _fx_ok else "unresolved",
             "detail": "已生成 top 特征句" if _fx_ok else "生成失败"},
            {"check": "术语/翻译腔/文体/质量", "status": "answered", "detail": "见 §4-§7 数值"},
            {"check": "学术规范自查", "status": "answered" if result.get("style_norm") else "unresolved",
             "detail": f"findings {result.get('style_norm', {}).get('finding_count')}"},
            {"check": "合规标识自查", "status": "answered",
             "detail": "显式标识证据见 §8；元数据/C2PA 用 aigc_label_check 对成品文件复核"},
        ],
        "budget": {"checks_run": 9, "note": "一次工作流调用完成全部检查；无迭代轮次消耗"},
        "note": ("answered=结论已给出；partially=有结论但精度受限（需人工复核）；"
                 "unresolved=该子检查失败，可单独重跑对应脚本。"),
    }

    result["integrity_notice"] = ("本工作流供作者自查与改进写作质量，不用于规避机构 AIGC 检测；"
                                  "请遵循所在机构 AI 使用与披露政策。")
    return result


def to_markdown(r: dict) -> str:
    """综合 JSON → Markdown 报告（人工可读版）。"""
    d = r["detect"]
    p = r["paragraphs"]
    lines = [
        "# 端到端自查报告",
        "",
        "- 引擎版本: %s ｜ 生成时间: %s ｜ 长度: %d 字" % (
            r["engine_version"], r["generated_at"], r["length_chars"]),
        "- **AI 率: %s / 风险档: %s** ｜ 引擎档位: %s" % (
            d.get("overall_ai_score"), d.get("overall_risk"),
            "完整（监督层融合）" if d.get("degraded_mode") is False else "降级（纯规则+词频谱）"),
        "- 诚信声明: %s" % r["integrity_notice"],
        "",
        "## 1. 段落级归因",
        "",
        "阈值 @medium %.0f / @high %.0f ｜ 高风险段 %d / 中风险段 %d / 共 %d 段" % (
            p["thresholds"]["medium"], p["thresholds"]["high"], p["high"], p["medium"], p["total"]),
        "",
    ]
    mx = r.get("mixed_document") or {}
    if mx.get("detected"):
        lines += [
            "> ⚠️ **混写文档**（疑似人机混写：高/低分段并存或引擎混写预警）",
            "> 估计 AI 段占比 ≈ %s ｜ 文档级 AUROC 0.52-0.54（原理性弱）｜ 段落级 AUROC 0.69（可用于定位，非自动判定）" % mx.get("ai_paragraph_fraction_est"),
            "> 以下为高分/中风险段，建议逐段人工复核：",
            "",
        ]
    for it in p["items"]:
        if it["class"] != "lo":
            lines.append("- 段%d [%s %.0f] %s…" % (it["index"], it["class"], it["score"], it["excerpt"]))
    lines += [
        "",
        "## 2. 四层降AI门禁",
        "",
        "- 复合风险: %s ｜ 判定: %s" % (r["gate"].get("composite_ai_risk"), r["gate"].get("verdict")),
        "",
    ]
    fx = r.get("fix_suggest") or {}
    _fs = fx.get("stats") or {}
    if _fs:
        try:
            from pp_fix_suggest import _TYPE_ZH as _fx_names
        except Exception:
            _fx_names = {}
        lines += ["## 3. 句子级改写建议（top5，完整版见 pp.py fix）", ""]
        if _fs.get("flagged_sentences"):
            lines.append("共 %d 句中 %d 句含可改进特征；特征分布：%s" % (
                _fs.get("total_sentences"), _fs.get("flagged_sentences"),
                "、".join(f"{_fx_names.get(k, k)}×{v}" for k, v in
                          sorted((_fs.get("type_counts") or {}).items(), key=lambda kv: -kv[1]))
                or "无"))
            lines.append("")
            for s in fx.get("top_issues", []):
                lines.append("- 句%d「%s…」：%s" % (
                    s["index"], s["sentence"][:24],
                    "；".join(_fx_names.get(x["type"], x["type"]) for x in s["issues"])))
            lines.append("")
        else:
            lines.append("未发现可改进特征句（引擎模式库口径；不构成「无需润色」结论）。")
            lines.append("")
    # 后续节号顺延
    lines += [
        "## 4. 术语保护",
        "",
        "- 标准率: %s%% ｜ 待处理: %s 处" % (r["terms"].get("standardization_rate"), r["terms"].get("total_issues")),
        "",
        "## 5. 翻译腔",
        "",
        "- 命中: %s 处" % r["smell"].get("total_hits"),
        "",
        "## 6. 文体距离",
        "",
        "- 文体分: %s（%s）" % (r["style"].get("style_score"), r["style"].get("verdict")),
        "",
        "## 7. 质量报告",
        "",
    ]
    q = r.get("quality") or {}
    q_labels = (("total_chars", "总字数"), ("total_paragraphs", "总段数"),
                ("readability_score", "可读性"), ("overall_quality", "总体质量"))
    for k, lab in q_labels:
        if k in q:
            lines.append("- %s: %s" % (lab, q[k]))
    lines += [
        "",
        "## 8. AIGC 合规标识自查",
        "",
        "- 显式标识证据: %d 条" % len((r.get("aigc_label") or {}).get("evidence", [])),
        "",
    ]
    _sn = r.get("style_norm") or {}
    if _sn.get("findings"):
        _sn_names = {"fullwidth": "全半角", "numbers": "数字用法",
                     "abbrev": "缩写定义", "units": "单位格式"}
        lines += [
            "## 9. 学术写作规范自查（建议，不评分）",
            "",
        ]
        for _f in _sn["findings"][:8]:
            _ex = "、".join(str(x) for x in _f["examples"][:3])
            lines.append("- %s ×%d（%s）" % (_sn_names.get(_f["check"], _f["check"]),
                                             _f["count"], _ex[:40]))
        lines += [""]
    _fl = r.get("findings_ledger") or {}
    if _fl.get("items"):
        lines += [
            "## 10. Findings Ledger（结论状态一览）",
            "",
        ]
        for _it in _fl["items"]:
            lines.append(f"- {_it['check']}：**{_it['status']}**（{_it['detail']}）")
        lines += ["", _fl.get("note", ""), ""]
    lines += [
        "---",
        "逐项完整数据见同名 .workflow.json。",
        "",
        "> 本文档由 Paper Polisher Pro 生成（[GitHub](https://github.com/docsor1212/paper-polisher-pro) · "
        "[SkillHub](https://skillhub.cn/skills/indiv-sorsor/paper-polisher-pro)）· 觉得有用欢迎 Star / 收藏",
    ]
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("file")
    ap.add_argument("--outdir", default=None, help="报告输出目录（默认与输入同目录）")
    ap.add_argument("--lang", default="auto", choices=["auto", "zh", "en"])
    a = ap.parse_args()
    p = Path(a.file)
    if not p.is_file():
        print("ERROR: 文件不存在: %s" % p, file=sys.stderr)
        return 2
    try:
        from docx_text import read_text_any
        text = read_text_any(p)
    except (ValueError, OSError) as e:
        from pp_errors import print_friendly
        print_friendly(e)
        return 2
    if len(text.strip()) < 100:
        print("ERROR: 文本不足 100 字（铁律 2：短文本不出判定）——请提交 100 字以上（建议 300+）", file=sys.stderr)
        return 2
    try:
        r = workflow(text, lang=a.lang)
    except Exception as e:
        from pp_errors import print_friendly
        print_friendly(e)
        return 1
    outdir = Path(a.outdir) if a.outdir else p.parent
    outdir.mkdir(parents=True, exist_ok=True)
    jf = outdir / (p.stem + ".workflow.json")
    mf = outdir / (p.stem + ".workflow.md")
    jf.write_text(json.dumps(r, ensure_ascii=False, indent=2), encoding="utf-8")
    mf.write_text(to_markdown(r), encoding="utf-8")
    d = r["detect"]
    print("AI率 %s / %s ｜ 段落 hi/med/total = %d/%d/%d ｜ 门禁 %s(%s)" % (
        d.get("overall_ai_score"), d.get("overall_risk"),
        r["paragraphs"]["high"], r["paragraphs"]["medium"], r["paragraphs"]["total"],
        r["gate"].get("verdict"), r["gate"].get("composite_ai_risk")))
    print("报告: %s" % mf)
    print("数据: %s" % jf)
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
