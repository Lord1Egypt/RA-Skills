#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""deai_gate.py — 四层融合门禁（词级/文体/翻译腔/术语加权综合, deai-medical-writing 系）

四层加权融合综合评分, 替代各层独立判定。

层权重依据 EVAL 判别力(2026-06-25 定稿数据):
  层4 style_distance 文体特征工程 — 正负差距49.2(最强) → 0.45
  层2 ai_detector   词级9层+段落均匀度 → 0.35
  层3 translation_smell 翻译腔+盲区新词 → 0.20
  层1 term_check    术语质量 → 建议性输出, 不计入AI风险分

综合AI风险 = 0.35*ai_score + 0.45*(100-style_score) + 0.20*smell_score
判定: <35 通过 / 35-55 需复核 / ≥55 疑似AI

用法:
  python3 deai_gate.py <file> [--json]
"""
import json
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SCRIPTS = Path(__file__).parent
W_L2, W_L4, W_L3 = 0.35, 0.45, 0.20


def run_py(script, args):
    """运行同目录脚本, 返回 (returncode, stdout, stderr)。超时返回 rc=124(兜底闭环,不裸栈)。
    v4.9.0: 失败重试一次（层偶发超时/负载抖动不再直接吃中性 50 分兜底）。"""
    last = (1, "", "")
    for attempt in (1, 2):
        try:
            p = subprocess.run([sys.executable, str(SCRIPTS / script)] + args,
                               capture_output=True, text=True, encoding="utf-8", timeout=120)
            last = (p.returncode, p.stdout or "", p.stderr or "")
        except subprocess.TimeoutExpired:
            last = (124, "", "layer timeout after 120s" + (" (retried)" if attempt == 2 else ""))
            if attempt == 2:
                return last
            time.sleep(1.0)
            continue
        if last[0] in (0, 1):
            return last  # 0=成功; 1=有合法产出（如 term_check 发现问题）
        if attempt == 2:
            return last  # rc>=2 崩溃：重试一次仍败则原样上抛
        time.sleep(1.0)
    return last


def layer2_ai(text_file):
    """层2: ai_detector 词级检测 → (0-100 AI分, 说明)"""
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False, mode="w") as f:
        out = f.name
    rc, so, se = run_py("ai_detector.py", [text_file, "--lang", "auto",
                                           "--format", "json", "--output", out])
    try:
        r = json.load(open(out, encoding="utf-8"))
        return float(r.get("overall_ai_score", 50)), \
            f"词级{r.get('overall_ai_score')}({r.get('overall_risk')})"
    except Exception:
        return 50.0, f"层2解析失败(rc={rc})"
    finally:
        Path(out).unlink(missing_ok=True)


def layer4_style(text_file):
    """层4: style_distance 文体特征 → (0-100 人类相似分, 说明)"""
    rc, so, se = run_py("style_distance.py", [text_file, "--json"])
    try:
        r = json.loads(so)
        if r.get("style_score") is None:
            return 50.0, "层4:文本过短"
        return float(r["style_score"]), f"文体{r['style_score']}({r['verdict']})"
    except Exception:
        return 50.0, f"层4解析失败(rc={rc})"


def layer3_smell(text_file):
    """层3: translation_smell 翻译腔 → (0-100 可疑度, 说明)。启发式计分。

    v3.5: 解析失败/层超时走中性 50 分兜底——此前失败得 0 分, 会把复合分系统性
    拉低 10 分, 有把垃圾输入推向 pass 带的风险; 真实 0 命中仍得 0 分。"""
    rc, so, se = run_py("translation_smell_check.py", [text_file, "--json"])
    hits = blind = -1
    try:
        r = json.loads(so)
        if isinstance(r, dict):
            v = r.get("hits")
            if isinstance(v, list):
                hits = len(v)
                blind = sum(1 for h in v if isinstance(h, dict)
                            and "盲区" in str(h.get("suggestion", "")))
    except Exception:
        pass
    if hits < 0:
        m = re.search(r'命中\s*(\d+)', so + se)
        if m and rc == 0:
            hits, blind = int(m.group(1)), 0
    if hits < 0:
        return 50.0, f"层3解析失败(rc={rc})"
    score = min(100, hits * 8 + blind * 25)
    return float(score), f"翻译腔命中{hits}(盲区{blind})"


def layer1_term(text_file):
    """层1: term_check 术语质量 → (通过?, 说明)。建议性。"""
    rc, so, se = run_py("term_check.py", [text_file])
    out = so + se
    if rc not in (0, 1):
        return None, f"层1失败(rc={rc})"
    m = re.search(r'标准率\s*(\d+(?:\.\d+)?)\s*%', out)
    if m:
        rate = float(m.group(1))
        return rate >= 97, f"标准率{rate}%"
    if "✅" in out or "术语检查通过" in out:
        return True, "术语检查通过"
    m2 = re.search(r'发现\s*(\d+)\s*处非标准', out)
    if m2:
        return False, f"{m2.group(1)}处非标准术语"
    return None, out.strip()[:50] or "层1无输出"


def gate(text_file, json_out=False):
    # v5.3.0: .docx 输入先抽取到临时 txt，再走原四层管线（用后即删）
    if str(text_file).lower().endswith(".docx"):
        from docx_text import read_text_any, DocxError
        import tempfile as _tf
        try:
            _txt = read_text_any(text_file)
        except DocxError as _e:
            print(f"ERROR: {_e}", file=sys.stderr)
            return {"error": str(_e)} if json_out else None
        _fd, _tmp = _tf.mkstemp(suffix=".txt")
        with os.fdopen(_fd, "w", encoding="utf-8") as _f:
            _f.write(_txt)
        try:
            return _gate_impl(_tmp, json_out=json_out)
        finally:
            Path(_tmp).unlink(missing_ok=True)
    return _gate_impl(text_file, json_out=json_out)


def _gate_impl(text_file, json_out=False):
    ai, ai_note = layer2_ai(text_file)
    style, style_note = layer4_style(text_file)
    smell, smell_note = layer3_smell(text_file)
    term_ok, term_note = layer1_term(text_file)

    composite = W_L2 * ai + W_L4 * (100 - style) + W_L3 * smell
    # v3.8: 层间分歧披露——词级与文体层方向显著矛盾时如实提示（AI 改写稿/混写常见）
    divergence = round(abs(ai - (100 - style)), 1)
    divergence_note = ""
    if divergence >= 30:
        divergence_note = (
            f"层间分歧：词级层({ai:.0f}) 与文体层({style:.0f}) 方向显著矛盾（差 {divergence:.0f}），"
            "常见于刻意模仿人类节奏的改写稿或语域混合，建议人工复核并参考段落级报告。")

    if composite < 35:
        verdict = "pass"
    elif composite < 55:
        verdict = "review"
    else:
        verdict = "ai_suspect"

    result = {
        "composite_ai_risk": round(composite, 1),
        "verdict": verdict,
        "layers": {
            "L2_word_patterns": {"ai_score": ai, "weight": W_L2, "note": ai_note},
            "L4_style_features": {"style_score": style, "weight": W_L4, "note": style_note},
            "L3_translation_smell": {"smell_score": smell, "weight": W_L3, "note": smell_note},
            "L1_terminology": {"advisory": term_ok, "note": term_note},
        },
        "bands": "composite<35 通过 | 35-55 需复核 | >=55 疑似AI",
        "integrity_notice": "本门禁供作者自查与改进写作质量, 不用于规避机构 AIGC 检测; 请遵循所在机构 AI 使用与披露政策。",
        "layer_divergence": divergence,
        "divergence_note": divergence_note,
        "honesty": "文体与词级检测是概率性判断, 不构成定罪; 阈值依据2026-06 EVAL, 建议结合人工审阅",
    }
    if json_out:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        mark = {"pass": "✅", "review": "🟡", "ai_suspect": "🔴"}[verdict]
        print(f"综合AI风险: {composite:.1f}/100 {mark} {verdict}")
        print(f"  层2 词级:   {ai_note}  (权重{W_L2})")
        print(f"  层4 文体:   {style_note}  (权重{W_L4})")
        print(f"  层3 翻译腔: {smell_note}  (权重{W_L3})")
        t = "✅" if term_ok else ("❌" if term_ok is False else "⚠️")
        print(f"  层1 术语:   {t} {term_note}  (建议性)")
        if divergence_note:
            print(f"  ℹ️ {divergence_note}")
        print(f"  判定带: {result['bands']}")
        print("  📘 " + result["integrity_notice"])
        if verdict != "pass":
            print("  ⚠️ 概率性判断非定罪; 建议人工复核, 并参照顶刊范文打磨句式节奏与标点多样性")
    return result


if __name__ == "__main__":
    import sys as _sys
    try:  # v3.5: 中文 Windows 默认 GBK 控制台会因 emoji/警示符崩溃 stdout——统一 UTF-8
        _sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        _sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    # v3.5: 用法守卫——此前 --help 会被当成文件名误跑门禁(实测层解析失败)
    if any(a in ("-h", "--help") for a in sys.argv[1:]):
        print(__doc__.strip())
        sys.exit(0)
    args = [a for a in sys.argv[1:] if a != "--json"]
    if not args:
        print("用法: python3 deai_gate.py <file> [--json]")
        sys.exit(2)
    if not Path(args[0]).exists():
        print(f"Error: File not found: {args[0]}", file=sys.stderr)
        sys.exit(2)
    gate(args[0], json_out="--json" in sys.argv)
