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

退出码: 0 通过 | 1 有违约（--strict 时警告也算违约） | 2 用法/文件错误
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
LATIN_ABBR_RE = re.compile(r"(?<![A-Za-z])([A-Z][A-Za-z0-9]*[A-Z][A-Za-z0-9]*)(?![a-z])")
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


_FW_DIGITS = "０１２３４５６７８９"
_FW_LETTERS = "ＡＢＣＤＥＦＧＨＩＪＫＬＭＮＯＰＱＲＳＴＵＶＷＸＹＺａｂｃｄｅｆｇｈｉｊｋｌｍｎｏｐｑｒｓｔｕｖｗｘｙｚ"
_FW_RUN = re.compile("[" + _FW_DIGITS + _FW_LETTERS + "]{2,}")


def _fullwidth_new_in(new_raw, orig_raw):
    """v2.8.0（邻居 agent 二轮实测实锤）：新稿含全角数字/字母串，且其 NFKC
    半角形态存在于原稿——中文输入法把 2025 打成 ２０２５、IL-6 打成 ＩＬ-6 这类
    形式篡改。NFKC 值比较会把它们判为等值静默 PASS，但学术稿件必须半角，
    按「数字/字符被改写」红线处理。返回描述列表（≤6 个）。"""
    import unicodedata as _ud
    hits = []
    for m in _FW_RUN.finditer(new_raw):
        half = _ud.normalize("NFKC", m.group(0))
        if half in orig_raw and m.group(0) not in orig_raw:
            hits.append("%s（应作 %s）" % (m.group(0)[:20], half[:20]))
        if len(hits) >= 6:
            break
    return hits


def verify(orig, new, terms=None, max_len_change=25.0, max_cjk_shift=0.12,
           expected_new=None):
    """返回 {ok, violations:[{check, code, detail}], warnings:[...], stats:{...}}。"""
    violations = []
    warnings = []

    orig_raw, new_raw = orig, new  # 原始文本（E_NUM_WIDTH/W_SENT_ADDED 检查用，先于 NFKC）
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
    # 1b2) 全角形式篡改（NFKC 等值但字符已变——v2.8.0 邻居二轮实测盲区修复）
    fw = _fullwidth_new_in(new_raw, orig_raw)
    if fw:
        violations.append({"check": "fullwidth", "code": "E_NUM_WIDTH",
                           "detail": "数字/字母被改写为全角（值等价但字符已变——"
                                     "常见于中文输入法；学术稿件必须半角）: "
                                     + "、".join(fw)})

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

    # 7) 整句新增告警（v2.8.0 邻居二轮实测：无数字的整句插入此前零告警）——
    #    改稿中出现原稿没有的完整句（≥8 字符）即提示，W 级不改判定
    _o_sents = set(s for s in hxt_core.split_sentences(_strip_residue(orig_raw)) if len(s) >= 8)
    _known_new = set(expected_new or ())
    _n_sents = [s for s in hxt_core.split_sentences(_strip_residue(new_raw))
                if len(s) >= 8 and s not in _o_sents and s not in _known_new]
    if _n_sents:
        warnings.append({"check": "sentences_added", "code": "W_SENT_ADDED",
                         "detail": "新增原稿没有的句子 %d 句（无数字也须核对是否擅自加内容）: %s"
                                   % (len(_n_sents),
                                      " | ".join(s[:24] for s in _n_sents[:3]))})

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


# v3.9.0 处方化输出（评测 usability 点名「频繁 exit 1 需要人工判断」）：
# 每类违规附「怎么修」处方，数字丢失类附原句上下文——修什么、怎么修一次说清。
_REMEDY = {
    "numbers": "把上述原句里的数字/统计量原样恢复进改稿对应位置（学术红线，不可放宽口径绕过）",
    "fullwidth": "把改稿中的全角数字/字母（２０２５ 类）改回半角后重跑",
    "comparison": "比较方向被反转（如 P<0.05→P>0.05）——恢复原文方向，并核对两臂顺序",
    "doi": "恢复被删/改的 DOI（逐字符核对，含连字符与大小写）",
    "pmid": "恢复被删/改的 PMID（纯数字编号）",
    "latin_abbr": "恢复被中文化或删除的缩写（首次出现处保留「全称（缩写）」格式）",
    "terms": "恢复术语表中被替换的术语；确认非术语再从术语表移除（勿改守卫）",
    "cjk_ratio": "疑似整段被删或被译——对照原稿恢复缺失段落",
    "length": "内容被整段删除——核对删减是否有意，恢复非有意删除的部分",
    "sentences_added": "逐句核对新增内容：删除无原文依据的新增句（编造防线）",
    "numbers_added": "删除凭空新增的数字，或补注来源",
    "number_context": "数字上下文/顺序变化——人工核对两臂与方向后恢复",
    "years": "核对年份引用是否被误删，恢复",
}
_REMEDY_WARN = {
    "sentences_added": "逐句核对新增句：删除无原文依据的新增句",
    "numbers_added": "删除凭空新增的数字，或补注来源",
    "number_context": "人工核对两臂/方向",
    "years": "核对年份引用是否被误删",
}


def _context_sentences(orig, numbers, limit=2, width=60):
    """数字丢失处方（v3.9.0）：在原稿里定位含丢失数字的句子，给修复锚点。

    切句保护（v3.9.0 评审 P1）：英文句点仅在后随空白时才视为句界——
    小数（0.003）与缩写点（e.g./Dr.）不再把句子切碎；数字匹配带
    前后界（找 5 不得命中 15/0.5），防子串误锚。"""
    import re as _re
    out, seen = [], set()
    sents = _re.split(r"(?<=[。！？!?])|(?<=\.)\s+|\n", orig)
    for num in numbers[:3]:
        pat = _re.compile(r"(?<![\d.])%s(?![\d])" % _re.escape(num))
        for sent in sents:
            s = sent.strip()
            if s and s not in seen and pat.search(s):
                seen.add(s)
                out.append(s[:width] + ("…" if len(s) > width else ""))
                break
        if len(out) >= limit:
            break
    return out


def build_remedies(orig, r):
    """处方清单（v3.9.0）：违规→[{check, remedy, context}]；JSON 报告同款字段。"""
    import re as _re
    remedies = []
    for v in r["violations"]:
        item = {"check": v["check"],
                "remedy": _REMEDY.get(v["check"], "对照原稿恢复被动过的内容")}
        if v["check"] == "numbers":
            nums = _re.findall(r"\d+(?:\.\d+)?", v.get("detail", ""))
            ctx = _context_sentences(orig, nums)
            if ctx:
                item["context"] = ctx
        remedies.append(item)
    for w in r["warnings"]:
        remedies.append({"check": w["check"],
                         "remedy": _REMEDY_WARN.get(w["check"], "按告警说明人工核对"),
                         "warning": True})
    return remedies


def render_report_html(r, remedies, terms_flag=False):
    """守卫处方报告（v5.7.0 --html；v5.8.0 抽出函数供 --bundle ⑪ 件复用）。

    PASS 简洁卡 / FAIL 处方：违规类别+原句锚点+怎么修+修复三步，打印友好。
    """
    import reporter as _rep
    from html import escape as _esc
    head = "PASS ✓" if r["ok"] else "FAIL ✗（学术安全红线）"
    color = "#1a7f37" if r["ok"] else "#cf222e"
    cards = ["<div class='card'><h1>完整性守卫报告</h1>"
             "<p style='color:%s;font-weight:700'>%s</p>"
             "<p class='meta'>%d → %d 字符 · CJK 漂移 %.3f · 术语表：%s</p></div>" % (
                 color, _esc(head), r["stats"]["orig_chars"],
                 r["stats"]["new_chars"], r["stats"].get("cjk_shift", 0.0),
                 "有" if terms_flag else "无")]
    if r["violations"]:
        lis = []
        for v in r["violations"]:
            rem = next((x["remedy"] for x in remedies
                        if x["check"] == v["check"]), "对照原稿恢复")
            ctxs = next((x.get("context", []) for x in remedies
                         if x["check"] == v["check"]), [])
            ctx_html = "".join("<br>原句锚点: <code>%s</code>" % _esc(c)
                               for c in ctxs[:3])
            lis.append("<li><b>[%s]</b> %s<br><span class='meta'>处方: %s</span>%s</li>"
                       % (_esc(v["check"]), _esc(v.get("detail", "")),
                          _esc(rem), ctx_html))
        cards.append("<div class='card'><h2>违规（%d 项，学术安全红线）</h2><ul>%s</ul></div>"
                     % (len(r["violations"]), "".join(lis)))
    if r["warnings"]:
        lis = ["<li><b>[%s]</b> %s</li>" % (_esc(w["check"]), _esc(w.get("detail", "")))
               for w in r["warnings"]]
        cards.append("<div class='card'><h2>告警（%d 项，人工核对）</h2><ul>%s</ul></div>"
                     % (len(r["warnings"]), "".join(lis)))
    if remedies:
        steps = "".join("<li>%s</li>" % _esc(x["remedy"]) for x in remedies[:8])
        cards.append("<div class='card'><h2>修复三步（按序执行）</h2><ol>%s</ol></div>" % steps)
    cards.append("<div class='card'><p class='meta'>原句锚点=原文原句；修复后重跑本命令复核，"
                 "exit 0 才算过。</p></div>")
    return _rep._page("完整性守卫报告", "".join(cards))


def main():
    ap = argparse.ArgumentParser(description="完整性守卫（改写不得动数据/引用/术语）")
    ap.add_argument("orig", help="原稿")
    ap.add_argument("new", help="改稿")
    ap.add_argument("--terms", help="术语表文件（每行一个术语，# 开头为注释）")
    ap.add_argument("--max-length-change", type=float, default=25.0)
    ap.add_argument("--max-cjk-shift", type=float, default=0.12)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--strict", action="store_true",
                    help="警告升级：任何 warning（如新增句子）也判失败 exit 1"
                         "（缺省警告不拦停，仅人工核对；分级表见 references/errors.md）")
    ap.add_argument("--html", help="守卫处方报告（v5.7.0）：单页 HTML——PASS 简洁卡/"
                    "FAIL 违规类别+原句锚点+怎么修+修复三步，可直接呈导师/编辑")
    ap.add_argument("--version", action="version", version="%(prog)s " + hxt_core.__version__)
    args = ap.parse_args()

    orig, new = _read(args.orig), _read(args.new)
    if not orig.strip() or not new.strip():
        print("错误: 输入为空", file=sys.stderr)
        sys.exit(2)
    terms = load_terms(args.terms) if args.terms else None
    r = verify(orig, new, terms, args.max_length_change, args.max_cjk_shift)
    remedies = build_remedies(orig, r)

    if args.html:
        with open(args.html, "w", encoding="utf-8") as hf:
            hf.write(render_report_html(r, remedies, terms_flag=bool(args.terms)))
        print("守卫处方报告已写入 %s" % args.html, file=sys.stderr)
    if args.json:
        r["remedies"] = remedies
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print("=" * 62)
        _head = "PASS ✓" if r["ok"] else "FAIL ✗（学术安全红线）"
        if r.get("warnings"):
            _head += "（%d 条警告，缺省不拦停；--strict 会判失败）" % len(r["warnings"])
        print("完整性守卫 verify：%s" % _head)
        print("=" * 62)
        print("规模: %d → %d 字符（%+.1f%%）| CJK 占比漂移 %.3f"
              % (r["stats"]["orig_chars"], r["stats"]["new_chars"],
                 r["stats"]["length_delta_pct"], r["stats"]["cjk_shift"]))
        for v in r["violations"]:
            print("  ✗ [%s] %s" % (v["check"], v["detail"]))
            rem = next((x for x in remedies if x["check"] == v["check"]
                        and not x.get("warning")), None)
            if rem:
                for ctx in rem.get("context", [])[:2]:
                    print("      原句锚点: %s" % ctx)
                print("      怎么修: %s" % rem["remedy"])
        for w in r["warnings"]:
            print("  ⚠ [%s] %s" % (w["check"], w["detail"]))
        if r["ok"] and not r["warnings"]:
            print("  数字/DOI/PMID/缩写/术语 全部保全。")
        print("判定: %s" % ("通过" if r["ok"] else "未通过——请修复改稿后重跑"))
        if not r["ok"]:
            print("修复三步: ①按上方「怎么修」逐条恢复改稿（术语误伤用 learn_guards.py "
                  "固化豁免，不要绕守卫）")
            print("          ②重跑本命令至 PASS ③交付前建议再跑 compare.py 留档")
    # 分级语义（v5.10.0 HR2）：violations=硬失败；warnings=人工核对不拦停；
    # --strict 把警告升级为失败（集成方需要零警告门禁时用）
    strict_fail = args.strict and bool(r.get("warnings"))
    if strict_fail:
        print("--strict：%d 条警告按失败处理（分级表见 references/errors.md）"
              % len(r["warnings"]), file=sys.stderr)
    _failed = (not r["ok"]) or strict_fail
    sys.exit(1 if _failed else 0)


if __name__ == "__main__":
    hxt_core.cli_entry(main)
