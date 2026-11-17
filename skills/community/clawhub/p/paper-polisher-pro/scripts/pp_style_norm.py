#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""pp_style_norm.py — 学术写作规范自查层（v5.2.0 新增）

定位：AI 痕迹检测之外的另一类自查——体例规范核对。四类机械检查：

  1. fullwidth   全半角混用（全角字母/数字 Ａｂｃ１２３；CJK 语境里的半角标点混用）
  2. numbers     数字用法一致性（汉字数字「五例」vs 阿拉伯「5例」混用；百分比写法）
  3. abbrev      缩写首次定义（出现 ≥2 次的缩写全文无定义模式；惯用豁免表）
  4. units       单位格式（数字-单位空格一致性；μ U+03BC vs µ U+00B5 隐形混用；×/x）

诚实边界：本检查是机械体例核对，输出 findings 建议（不评分、无风险带、
不构成任何质量判定）。短文本判定铁律针对 AI 率结论，本工具不受其约束——
但 <100 字时仅在输出中注明样本过小、统计类检查仅供参考。

用法:
  python3 pp_style_norm.py <file> [--json] [--checks fullwidth,numbers,abbrev,units]
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

_INTEGRITY = ("学术诚信：本检查为机械体例核对（格式一致性建议），不评分、不构成任何质量或"
              "合规判定；请按所在机构政策规范披露 AI 使用。")

# 惯用免定义缩写（领域通用，多数期刊不再要求首定义；仅豁免「定义检查」，出现混用仍会提示）
_ABBR_EXEMPT = {"DNA", "RNA", "CT", "MRI", "PCR", "HIV", "AIDS", "WHO", "BMI", "ICU",
                "ELISA", "SD", "SE", "HR", "CI", "OR", "RR", "SPSS", "PDF", "ASCII"}

_RE_FULLWIDTH_ALNUM = re.compile(r"[Ａ-Ｚａ-ｚ０-９]+")
# CJK 邻接的半角标点（前或后 1 字符是 CJK/全角标点 → 应为全角标点）
_RE_HALF_PUNCT = re.compile(r"([\u4e00-\u9fff\u3001-\u303f\uff01-\uff0f\uff1a-\uff1b])"
                            r"([,;:!?])|([,;:!?])"
                            r"([\u4e00-\u9fff\u3001-\u303f\uff01-\uff0f\uff1a-\uff1b])")
_RE_CJK_NUM = re.compile(r"[一二三四五六七八九十百千]+(?:例|名|例次|组|周|月|天|日|年|次|份|篇)")
_RE_ARAB_NUM = re.compile(r"\d+(?:\.\d+)?(?:例|名|例次|组|周|月|天|日|年|次|份|篇)")
_RE_PCT_CN = re.compile(r"百分之[〇一二三四五六七八九十百\d.]+")
_RE_PCT_SYM = re.compile(r"\d+(?:\.\d+)?\s*[%％]")
_RE_ABBR = re.compile(r"\b[A-Z]{2,6}\b")
_RE_DEF_PATTERNS = [
    re.compile(r"[\u4e00-\u9fffA-Za-z -]{2,40}[（(]%s[)）]" % r"A-Z"),      # 中文名（ABBR）
    re.compile(r"\b(%s)\b[（(][\u4e00-\u9fffA-Za-z -]{2,40}[)）]" % r"A-Z{2,6}"),  # ABBR（全称）
    re.compile(r"即[\u4e00-\u9fffA-Za-z -]{2,30}\b"),                        # 「即…」式定义
]
_RE_NUM_UNIT_TIGHT = re.compile(r"\d(?:mg|ml|kg|μg|µg|mm|cm|min|s|h|%)(?![A-Za-z0-9])")
_RE_NUM_UNIT_SPACED = re.compile(r"\d (?:mg|ml|kg|μg|µg|mm|cm|min|s|h|%)(?![A-Za-z0-9])")
_RE_MU_VARIANTS = re.compile(r"(μ|µ)")
_RE_TIMES_X = re.compile(r"\d+\s*[×xX]\s*10")


def _reads(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"文件不存在: {p}")
    from docx_text import read_text_any
    return read_text_any(p)  # DocxError(ValueError 族) 由 main 统一转干净报错


def check_fullwidth(text):
    fw = _RE_FULLWIDTH_ALNUM.findall(text)
    findings = []
    if fw:
        findings.append({
            "check": "fullwidth", "severity": "inconsistent",
            "count": len(fw),
            "examples": fw[:5],
            "advice": "发现全角字母/数字（Ａｂｃ１２３ 形态）。学术文本应统一半角："
                      "英文、数字、单位一律半角；中文标点用全角。可全局搜索替换。",
        })
    half_punct = [m.group(0) for m in _RE_HALF_PUNCT.finditer(text)]
    # 按出现形态聚合示例
    if half_punct:
        findings.append({
            "check": "fullwidth", "severity": "suggest",
            "count": len(half_punct),
            "examples": list(dict.fromkeys(half_punct))[:6],
            "advice": "中文语境出现半角标点（, ; : ! ?）。中文句子内标点应使用全角"
                      "（，；：！？）；英文/数字语境的半角标点不受影响。请按语境抽查。",
        })
    return findings


def check_numbers(text):
    cn = _RE_CJK_NUM.findall(text)
    ar = _RE_ARAB_NUM.findall(text)
    findings = []
    if cn and ar:
        findings.append({
            "check": "numbers", "severity": "inconsistent",
            "count": len(cn) + len(ar),
            "examples": cn[:4] + ar[:4],
            "advice": "量词数字两种写法并存（汉字「五例」vs 阿拉伯「5例」）。"
                      "统计与计量数字按 GB/T 15835 建议统一用阿拉伯数字（5 例、3 组）；"
                      "习用语（「进一步」「三甲」等）可保留汉字。",
        })
    pct_cn = _RE_PCT_CN.findall(text)
    pct_sym = _RE_PCT_SYM.findall(text)
    if pct_cn and pct_sym:
        findings.append({
            "check": "numbers", "severity": "inconsistent",
            "count": len(pct_cn) + len(pct_sym),
            "examples": pct_cn[:4] + pct_sym[:4],
            "advice": "百分比两种写法并存（「百分之五十」vs「50%」）。全文统一一种，"
                      "学术文本通常用「N%」。",
        })
    return findings


def check_abbrev(text):
    counts = Counter(m.group(0) for m in _RE_ABBR.finditer(text))
    findings = []
    undefined = []
    for abbr, n in counts.items():
        if n < 2 or abbr in _ABBR_EXEMPT:
            continue
        defined = any(rx.search(text) for rx in _RE_DEF_PATTERNS)
        # 针对该缩写的定义判定：文中存在「（…ABBR…）」或「ABBR（…）」括号定义
        if not defined:
            undefined.append((abbr, n))
    for abbr, n in undefined[:8]:
        findings.append({
            "check": "abbrev", "severity": "suggest",
            "count": n,
            "examples": [abbr],
            "advice": f"缩写 {abbr} 出现 {n} 次但未见首次定义。期刊惯例：首次出现时"
                      f"写「中文全称（{abbr}）」后文再用缩写。",
        })
    return findings


def check_units(text):
    findings = []
    tight = _RE_NUM_UNIT_TIGHT.findall(text)
    spaced = _RE_NUM_UNIT_SPACED.findall(text)
    if tight and spaced:
        minority, form = ((spaced, "数字+空格+单位") if len(spaced) <= len(tight)
                          else (tight, "数字紧贴单位"))
        findings.append({
            "check": "units", "severity": "inconsistent",
            "count": len(minority),
            "examples": list(dict.fromkeys(minority))[:6],
            "advice": f"数字与单位两种间距并存。全文统一为「{form}」"
                      "（多数期刊接受紧贴式，关键是全文一致）。",
        })
    mus = _RE_MU_VARIANTS.findall(text)
    if len(set(mus)) > 1:
        findings.append({
            "check": "units", "severity": "inconsistent",
            "count": len(mus),
            "examples": [f"U+{ord(c):04X}" for c in set(mus)],
            "advice": "希腊字母 μ 出现两种 Unicode 形态（U+03BC 希腊小写 mu / U+00B5 微符号），"
                      "显示与检索都不一致——统一为 U+03BC（μg）。",
        })
    if _RE_TIMES_X.search(text) and re.search(r"\d+\s*[xX]\s*10", text) and re.search(r"\d+\s*×\s*10", text):
        findings.append({
            "check": "units", "severity": "suggest",
            "count": 2,
            "examples": ["×", "x"],
            "advice": "科学计数乘号混用（× 与字母 x）。统一用乘号 ×。",
        })
    return findings


def check_consistency(text):
    """v5.5.0: 同概念异写混用检测（references/term_variants.json 变体组）。

    检测的是「混用」而非对错——组内写法本身都合法，同文档并存才提示统一。
    """
    import json as _json
    bank_p = HERE.parent / "references" / "term_variants.json"
    findings = []
    try:
        bank = _json.load(open(bank_p, encoding="utf-8")).get("groups", [])
    except Exception as e:
        return [{"check": "consistency", "severity": "suggest", "count": 0,
                 "examples": [], "advice": f"变体组词库读取失败（{e}），本检查跳过。"}]
    for grp in bank:
        variants = grp.get("variants") or []
        present = [(v, text.count(v)) for v in variants if v and text.count(v) > 0]
        if len(present) >= 2:
            top = sorted(present, key=lambda x: -x[1])
            findings.append({
                "check": "consistency", "severity": "suggest",
                "count": sum(n for _, n in present),
                "examples": [f"{v}×{n}" for v, n in top[:4]],
                "advice": f"同概念异写混用（组：{grp.get('canonical')}）："
                          f"全文统一为其中一种（建议「{top[0][0]}」，占比最高；"
                          + (grp.get("note", "组内写法等价。") if grp.get("note") else "组内写法等价。") + "）",
            })
    return findings


_JARGON_L1 = ("兜底 兜住 抓手 赋能 闭环 打通 落地 对齐 拉齐 颗粒度 底层逻辑 赛道 打法 组合拳 护城河 卡点 痛点 "
              "拆解 沉淀 复盘 顶层设计 叙事 图景 蓝图 密码 钥匙 答卷 命题 画像 注脚 伏笔 终章 序章 篇章 乐章 "
              "交响 变奏 涟漪 回响 回声 底色 基调 底座 收拢 读懂 讲透 带走 串成 串起 编织 勾勒 面孔 账单 领土 "
              "探针 破门 一网打尽 浮出水面 洪流 底细 主场 接力棒 命运 互相渗透 另一面 多管齐下 对号入座 零件 "
              "出厂 车间 拼图 版图 主角 配角 剧本 舞台 破防 失守 失灵 塌方 点燃 登场 送进 站上 行动清单 "
              "窗口前移 主力人群 第一站").split()
_JARGON_L2 = ("克制 口径 边界 维度 格局 图谱 锚定 倒逼 亟待 彰显 范式 重塑 重构 生态 至关重要 举足轻重 "
              "毋庸置疑 不言而喻 众所周知 里程碑 革命性 颠覆 窗口 支柱 主线 陷阱").split()
_JARGON_L3 = ["不是…而是…", "与其说…不如说", "首先…其次", "综上所述", "总而言之",
              "值得注意的是", "更重要的是", "与此同时", "由此可见"]


def check_llm_jargon(text):
    """v5.6.0 第 7 查：LLM 中文输出高频 AI 腔（三层词表+判例库对照）。

    词表与判例来源=免疫深读产线 2026-08-31 真实判废复盘（跨线移植）：
    L1 隐喻滥用（命中即改）／L2 语气词（评审判断）／L3 句式模式。
    只提示不计分；判例库给「原句→改句」对照。白名单句式另附。
    """
    import json as _json
    findings = []
    l1 = sorted({w for w in _JARGON_L1 if w in text})
    l2 = sorted({w for w in _JARGON_L2 if w in text})
    l3 = [s for s in _JARGON_L3
          if (s.split("…")[0] in text and (len(s.split("…")) < 2 or s.split("…")[-1] in text))]
    cases = []
    cases_p = HERE.parent / "references" / "style_guard_cases.json"
    try:
        cases = _json.load(open(cases_p, encoding="utf-8")).get("cases", [])
    except Exception:
        cases = []

    # v5.7.0: 命中句上下文定位（帮作者直接找到位置，而非只给词表）
    sents = [s.strip() for s in __import__("re").split(r"(?<=[。！？；!?;])", text) if s.strip()]
    loc = {}
    for w in l1 + l2:
        for s in sents:
            if w in s:
                loc.setdefault(w, s[:60])
                break
    if l1:
        hit_cases = [c for c in cases if c.get("word") in l1][:4]
        extra = "；判例对照：" + "；".join(
            f"「{c['wrong']}」→「{c['right']}」" for c in hit_cases) if hit_cases else ""
        findings.append({
            "check": "llm_jargon", "severity": "inconsistent",
            "count": len(l1) + sum(text.count(w) for w in l1),
            "examples": l1[:8],
            "sentences": [{"word": w, "sentence": loc.get(w, "")} for w in l1[:5] if loc.get(w)],
            "advice": ("L1 隐喻滥用词（LLM 中文输出高频特征，命中即改）：" + "、".join(l1[:10]) + "。"
                       + "策略：隐喻改直陈——保留医学事实，去掉拟人/战争/工厂/旅程类比喻。" + extra),
        })
    if l2:
        findings.append({
            "check": "llm_jargon", "severity": "suggest",
            "count": len(l2),
            "examples": l2[:8],
            "advice": ("L2 语气词（语境敏感，逐处评审）：底线是别用空泛强调替代证据——"
                       "「至关重要/毋庸置疑/众所周知」类改为给出具体依据或直接删除；"
                       "「范式/重塑/生态」类仅在术语本义使用。"),
        })
    if l3:
        findings.append({
            "check": "llm_jargon", "severity": "suggest",
            "count": len(l3),
            "examples": l3[:5],
            "advice": ("L3 句式模式（AI 高频句式）：拆掉对仗结构——"
                       "「不是A而是B」改为直接陈述B；「首先…其次」改为按逻辑分段；"
                       "「综上所述」改为一句具体的结论句。"),
        })
    if l1 or l2 or l3:
        wl = []
        cp = HERE.parent / "references" / "style_guard_cases.json"
        try:
            wl = _json.load(open(cp, encoding="utf-8")).get("whitelist_styles", [])
        except Exception:
            pass
        if wl:
            findings[-1]["advice"] += "医学语体推荐句式（白名单）：" + "／".join(wl[:6]) + "。"
    return findings


_CHECKS = {"fullwidth": check_fullwidth, "numbers": check_numbers,
           "abbrev": check_abbrev, "units": check_units,
           "consistency": check_consistency, "llm_jargon": check_llm_jargon}


def style_norm(text: str, checks=None) -> dict:
    """学术写作规范自查，返回 JSON 兼容 dict（无评分）。

    checks: 子集选择，默认全部四类。
    """
    if not isinstance(text, str) or not text.strip():
        raise ValueError("text 必须是非空字符串")
    checks = checks or list(_CHECKS)
    unknown = [c for c in checks if c not in _CHECKS]
    if unknown:
        raise ValueError(f"未知检查项: {unknown}（可选：{list(_CHECKS)}）")
    findings = []
    for c in checks:
        findings.extend(_CHECKS[c](text))
    import pp_api
    return {
        "engine_version": pp_api.engine_version(),
        "length_chars": len(text),
        "checks_run": checks,
        "finding_count": len(findings),
        "findings": findings,
        "notice": ("本检查为机械体例核对：不评分、无风险带，建议均需结合语境人工确认；"
                   "与 AI 率检测相互独立。"),
        "short_sample": len(text.strip()) < 100,
        "integrity_notice": _INTEGRITY,
    }


_TYPE_ADVICE = "advice"  # findings 自带 advice，文本渲染直接用


def to_text(r: dict) -> str:
    lines = [f"── 学术写作规范自查（{r['length_chars']} 字，检查 {len(r['checks_run'])} 类）──"]
    if r["short_sample"]:
        lines.append("样本不足 100 字：统计类检查（数字/缩写）仅供参考。")
    if not r["findings"]:
        lines.append("未发现体例问题（机械核对口径）。这不构成「无需润色」的结论。")
    else:
        cur = None
        for f in r["findings"]:
            if f["check"] != cur:
                cur = f["check"]
                names = {"fullwidth": "全半角", "numbers": "数字用法",
                         "abbrev": "缩写定义", "units": "单位格式"}
                lines.append(f"\n[{names.get(cur, cur)}]")
            ex = "、".join(str(x) for x in f["examples"][:5])
            lines.append(f"  · ({f['severity']}) ×{f['count']}：{ex}")
            lines.append(f"    → {f['advice']}")
    lines.append("")
    lines.append(r["notice"])
    lines.append(r["integrity_notice"])
    return "\n".join(lines)


def main():
    ap = argparse.ArgumentParser(description="学术写作规范自查（体例核对，不评分）")
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--checks", default=None,
                    help="逗号分隔子集：fullwidth,numbers,abbrev,units,consistency,llm_jargon（默认全部）")
    args = ap.parse_args()
    try:
        text = _reads(args.file)
    except (FileNotFoundError, ValueError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    checks = args.checks.split(",") if args.checks else None
    try:
        r = style_norm(text, checks=checks)
    except (ValueError, FileNotFoundError) as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
    else:
        print(to_text(r))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
