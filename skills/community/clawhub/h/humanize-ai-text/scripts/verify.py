# -*- coding: utf-8 -*-
"""verify.py — 完整性守卫：改写不得动数据、引用与术语。

学术安全红线（任何一条违约 → exit 1）:
  - 数字保全：所有数值（统计量/p 值/百分比/样本量）多集一致
  - 引用保全：DOI / PMID / 年份 不丢失
  - 拉丁缩写保全：DNA/PCR/MRI 等连续大写串不丢失
  - 术语保全：--terms 术语表（每行一个）逐个仍在且次数不减
  - 语言一致：中文字符占比漂移 ≤ --max-cjk-shift（默认 0.12）
  - 长度警戒：字符数变化 ≤ --max-length-change %（默认 25）

用法:
    python scripts/verify.py 原稿.txt 改稿.txt
    python scripts/verify.py 原稿.txt 改稿.txt --terms terms.txt --json

退出码: 0 通过 | 1 有违约 | 2 用法/文件错误
"""

import argparse
import json
import re
import sys
import os
import unicodedata
from collections import Counter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hxt_core

DOI_RE = re.compile(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", re.IGNORECASE)
PMID_RE = re.compile(r"PMID:?\s*(\d+)", re.IGNORECASE)
YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
NUM_RE = re.compile(r"(?<!\d)-?\d+(?:\.\d+)?%?")  # 负号仅在前面不是数字时成立（2024-01-15 是日期不是减法）
CMP_RE = re.compile(r"[<>≤≥]\s*-?\d+(?:\.\d+)?%?")
NUM_CTX_RE = re.compile(r"-?\d+(?:\.\d+)?%?[^，。；;（）()]{0,20}")
LATIN_ABBR_RE = re.compile(r"\b[A-Z]{2,8}\b")
CJK_RE = re.compile(r"[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


def _strip_residue(text):
    """剥离各模型残留标记后再提取数字——[cite: 1] 的索引不是学术数据。"""
    for code in ("zh", "en"):
        for item in hxt_core.load_patterns(code)["model_artifacts"]:
            text = item["_re"].sub("", text)
    return text


_DASHES = "\u2010\u2012\u2013\u2014\u2015\u2212"  # hyphen bullet / figure / en / em / horizontal bar / math minus


def _norm_text(text):
    """等值排版归一：全角→半角（NFKC）、各类连字符/负号统一、千分位逗号、
    数字与 % 之间的空格。6-8→6–8、1,234→1234、−3.2→-3.2、P＜0.05→P<0.05
    这类语义无损改写不应触发守卫。"""
    text = unicodedata.normalize("NFKC", text)
    for dsh in _DASHES:
        text = text.replace(dsh, "-")
    text = re.sub(r"(?<=\d),(?=\d)", "", text)
    text = re.sub(r"(?<=%)\s+(?=\d)|(?<=\d)\s+(?=%)", "", text)
    return text


def _num_key(tok):
    """数字 token → 数值键（0.5 与 .5、50% 与 50% 归一为同一键）。"""
    pct = tok.endswith("%")
    if pct:
        tok = tok[:-1]
    try:
        return (round(float(tok), 6), pct)
    except ValueError:
        return (tok, pct)


def _read(path):
    try:
        return hxt_core.read_text(path)
    except OSError as e:
        print("错误: 无法读取 %s（%s）" % (path, e), file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)


def _missing(orig_c, new_c):
    """orig 有而 new 缺的项（按次数）。"""
    miss = []
    for k, v in orig_c.items():
        d = v - new_c.get(k, 0)
        if d > 0:
            miss.extend([k] * d)
    return miss


def verify(orig, new, terms=None, max_len_change=25.0, max_cjk_shift=0.12):
    """返回 {ok, violations:[{check, detail}], warnings:[...], stats:{...}}。"""
    violations = []
    warnings = []

    orig, new = _norm_text(orig), _norm_text(new)

    def multiset(rex, text, normalize=lambda x: x):
        return Counter(normalize(m.group(0)) for m in rex.finditer(text))

    # 1) 数字（残留剥离+归一后按「数值」比对：0.5==.5、50%==50 %、2024-01-15==2024年1月15日）
    orig_s, new_s = _strip_residue(orig), _strip_residue(new)

    def fmt(k):
        num = ("%.0f" % k[0]) if float(k[0]).is_integer() else ("%.6g" % k[0])
        return num + ("%" if k[1] else "")

    miss = _missing(multiset(NUM_RE, orig_s, _num_key), multiset(NUM_RE, new_s, _num_key))
    if miss:
        violations.append({"check": "numbers", "code": "E_NUM_LOST",
                           "detail": "数字丢失/被改: %s" % ", ".join(fmt(k) for k in miss[:12]) +
                                     ("…" if len(miss) > 12 else "")})
    # 1b) 新增数字（多重集反方向）：深改时凭空出现的数字=编造风险，立即警示
    added = _missing(multiset(NUM_RE, new_s, _num_key), multiset(NUM_RE, orig_s, _num_key))
    if added:
        warnings.append({"check": "numbers_added", "code": "W_NUM_ADDED",
                         "detail": "出现原稿没有的数字: %s——若非原文数据立即删除（防编造）"
                                   % ", ".join(fmt(k) for k in added[:8])})
    # 1c) 数字上下文指纹：多集一致但上下文变化 → 两臂互换/方位错位类静默改写
    ctx_o = multiset(NUM_CTX_RE, orig_s, lambda s: re.sub(r"\s+", "", s))
    ctx_n = multiset(NUM_CTX_RE, new_s, lambda s: re.sub(r"\s+", "", s))
    ctx_miss = _missing(ctx_o, ctx_n)
    if ctx_miss and not miss:
        warnings.append({"check": "number_context", "code": "W_CTX_SWAP",
                         "detail": "数字上下文/顺序变化（如两臂互换）: %s——人工核对方向"
                                   % " | ".join(ctx_miss[:4])})
    # 1d) 比较方向（P < 0.05 改成 P > 0.05 是结论反转，直接红线）
    cmp_o = multiset(CMP_RE, orig_s, lambda s: re.sub(r"\s+", "", s))
    cmp_n = multiset(CMP_RE, new_s, lambda s: re.sub(r"\s+", "", s))
    cmp_miss = _missing(cmp_o, cmp_n)
    if cmp_miss:
        violations.append({"check": "comparison", "code": "E_CMP_FLIP",
                           "detail": "比较方向/比较数字被改: %s" % ", ".join(cmp_miss[:8])})
    # 2) DOI / PMID / 年份
    miss_doi = _missing(multiset(DOI_RE, orig, lambda s: s.lower()), multiset(DOI_RE, new, lambda s: s.lower()))
    if miss_doi:
        violations.append({"check": "doi", "code": "E_DOI_LOST", "detail": "DOI 丢失: %s" % ", ".join(miss_doi[:5])})
    miss_pm = _missing(multiset(PMID_RE, orig), multiset(PMID_RE, new))
    if miss_pm:
        violations.append({"check": "pmid", "code": "E_PMID_LOST", "detail": "PMID 丢失: %s" % ", ".join(miss_pm[:5])})
    miss_y = _missing(multiset(YEAR_RE, orig), multiset(YEAR_RE, new))
    if miss_y:
        warnings.append({"check": "years", "code": "W_YEARS", "detail": "年份数量变化: 减少 %s" % ", ".join(miss_y[:8])})
    # 3) 拉丁缩写
    miss_ab = _missing(multiset(LATIN_ABBR_RE, orig), multiset(LATIN_ABBR_RE, new))
    if miss_ab:
        violations.append({"check": "latin_abbr", "code": "E_ABBR_LOST",
                           "detail": "大写缩写丢失（DNA/PCR/MRI 类）: %s" % ", ".join(sorted(set(miss_ab))[:10])})
    # 4) 用户术语表
    if terms:
        miss_t = []
        for t in terms:
            t = t.strip()
            if not t or t.startswith("#"):
                continue
            if orig.count(t) > new.count(t):
                miss_t.append("%s(%d→%d)" % (t, orig.count(t), new.count(t)))
        if miss_t:
            violations.append({"check": "terms", "code": "E_TERMS_LOST", "detail": "术语表缺失/减少: %s" % "; ".join(miss_t[:10])})
    # 5) CJK 占比漂移（短文本容忍度放宽：年月日这类写法转换会推高占比；
    #    整段被删或被译的漂移远超阈值，长文维持严格线）
    def cjk_ratio(t):
        return len(CJK_RE.findall(t)) / max(1, len(t))
    shift = abs(cjk_ratio(orig) - cjk_ratio(new))
    eff_shift = max_cjk_shift if len(orig) >= 500 else max(max_cjk_shift, 0.25)
    if shift > eff_shift:
        violations.append({"check": "cjk_ratio", "code": "E_CJK_SHIFT",
                           "detail": "中英占比漂移 %.2f > %.2f（可能整段被删或被译）" % (shift, eff_shift)})
    # 6) 长度变化（短文本阈值放宽：删一两句客套话就能占小文本的 30%+；
    #    论文级长文本维持 ±25% 严格线。--max-length-change 可显式覆盖）
    eff_max = max_len_change if len(orig) >= 500 else max(max_len_change, 50.0)
    delta = (len(new) - len(orig)) / max(1, len(orig)) * 100.0
    if abs(delta) > eff_max:
        violations.append({"check": "length", "code": "E_LEN_DRIFT",
                           "detail": "长度变化 %.1f%% 超过警戒线 ±%.0f%%" % (delta, eff_max)})
    elif abs(delta) > eff_max * 0.7:
        warnings.append({"check": "length", "code": "E_LEN_DRIFT", "detail": "长度变化 %.1f%%，接近警戒线" % delta})

    return {"ok": not violations,
            "violations": violations,
            "warnings": warnings,
            "stats": {"orig_chars": len(orig), "new_chars": len(new),
                      "length_delta_pct": round(delta, 1),
                      "cjk_shift": round(shift, 3)}}


def load_terms(path):
    # 经 read_text：剥 BOM（Windows 记事本术语表首词失检教训）+ 大小/二进制守卫
    try:
        return hxt_core.read_text(path).splitlines()
    except OSError as e:
        print("错误: 无法读取术语表 %s（%s）" % (path, e), file=sys.stderr)
        sys.exit(2)
    except ValueError as e:
        print("错误: %s" % e, file=sys.stderr)
        sys.exit(2)


def main():
    ap = argparse.ArgumentParser(description="完整性守卫（改写不得动数据/引用/术语）")
    ap.add_argument("orig", help="原稿")
    ap.add_argument("new", help="改稿")
    ap.add_argument("--terms", help="术语表文件（每行一个术语，# 开头为注释）")
    ap.add_argument("--max-length-change", type=float, default=25.0)
    ap.add_argument("--max-cjk-shift", type=float, default=0.12)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--version", action="version", version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    orig, new = _read(args.orig), _read(args.new)
    if not orig.strip() or not new.strip():
        print("错误: 输入为空", file=sys.stderr)
        sys.exit(2)
    terms = load_terms(args.terms) if args.terms else None
    r = verify(orig, new, terms, args.max_length_change, args.max_cjk_shift)

    if args.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("=" * 62)
        print("完整性守卫 verify：%s" % ("PASS ✓" if r["ok"] else "FAIL ✗（学术安全红线）"))
        print("=" * 62)
        print("规模: %d → %d 字符（%+.1f%%）| CJK 占比漂移 %.3f"
              % (r["stats"]["orig_chars"], r["stats"]["new_chars"],
                 r["stats"]["length_delta_pct"], r["stats"]["cjk_shift"]))
        for v in r["violations"]:
            print("  ✗ [%s] %s" % (v["check"], v["detail"]))
        for w in r["warnings"]:
            print("  ⚠ [%s] %s" % (w["check"], w["detail"]))
        if r["ok"] and not r["warnings"]:
            print("  数字/DOI/PMID/缩写/术语 全部保全。")
        print("判定: %s" % ("通过" if r["ok"] else "未通过——请修复改稿后重跑"))
    sys.exit(0 if r["ok"] else 1)


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    main()
