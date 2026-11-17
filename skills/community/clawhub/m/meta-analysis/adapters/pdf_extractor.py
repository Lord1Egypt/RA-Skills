# -*- coding: utf-8 -*-
"""pdf_extractor — PDF 数据抓取 P1（文本型 PDF + 有框表格 + 叙述句 + 一致性校验）。

设计 spec：contracts/pdf_extraction/v0.1.0/SPEC.md（P1 范围，扫描件暂不支持）。
v0.4 (2026-09-14)：基于 78 篇真实 PDF 实证改进。
  - 新增 T_FOREST_TABLE 模板（森林图/效应量汇总表）
  - 新增 T_META_TABLE 模板（meta 分析纳入研究特征表）
  - 新增 T_POOLED_EFFECT 叙述模板（pooled/overall 句式）
  - 新增 T_SUBGROUP_EFFECT 叙述模板（subgroup 句式）
  - 修复 _rebuild_borderless_table 伪表过滤（min_cols 2→3，数值行占比过滤）
  - 列间距阈值 20pt→12pt
v0.4.1：T_META_TABLE 质量硬化（过滤参考文献/编号引用/期刊缩写）。

流水线（对齐 2026-08-31 设计讨论）：
  ① 版面解析：PyMuPDF 检测文本层，pdfplumber 提取有框表格（vertical_strategy=lines，
     等效 Camelot lattice，不引入新依赖；Camelot 留作后续可选增强）。
  ② 双通道抽取：
     - 表格模板：T_DICHOT（2x2 四格表：events/n × 实验组/对照组）、T_CONTINUOUS
       (n/mean/SD × 两臂)。输出原始计数（ai/bi/ci/di）——供 ③ 勾稽重算。
     - 正文叙述模板：正则候选片段抽取（零幻觉），命中片段带页码锚点。
       P1 覆盖：四格计数 n/N (%)、风险比/均差 + 95%CI。连续结局叙述默认 needs_review。
  ③ 一致性校验（纯代码、零幻觉，正确率的最大杠杆）：
     - 四格表重算 OR/RR 与报告值比对；events ≤ n；跨来源（表格 vs 正文）互证。
     - te/sete 与 95%CI 互推（Woolf / CI 宽度）。
  ④ 置信路由：verified（勾稽全过）→ 自动通过；needs_review（校验不过/来源单一/
     连续结局叙述）→ 人工审核（附页码锚点）；failed（无法定位）→ 人工补录。
  ⑤ 输出直接对接 fullflow A4 闸：rows 形如 b1 可消费的 study 字典 + 审核元数据
     （confidence/checks/anchors）。人工审核通过后走 extraction_guard stamp --confirm。

v0.1 已知限制：
  - 无扫描件通道（P2）；无边框表格（lines 策略抓不到，P2 用 Camelot stream 或 Docling）；
  - 表头模板基于关键词打分匹配，异形表头需人工在审核台指定列映射（P2 交互列映射）；
  - 叙述连续结局只产出候选 + 锚点，不做自动直通。
"""

import os
import re
import math
import json


def _norm_path(p):
    """路径规范化：把 Git Bash 的 /c/... 转 Windows 风格，并解析为绝对路径。"""
    if p is None:
        return p
    # Git Bash 传 /c/foo 时，先转 C:/foo（normpath 在 Windows 上会误拼）
    if re.match(r"^/[a-zA-Z]/", p):
        p = p[1].upper() + ":" + p[2:]
    p = os.path.normpath(p)
    if not os.path.isabs(p):
        p = os.path.abspath(p)
    return p

# ---------------------------------------------------------------------------
# ① 版面解析
# ---------------------------------------------------------------------------

# ===========================================================================
# ⓪ 文本修复层 + 强制类型甄别（v0.3，回流 2026-09-09 15 篇 PDF 实证规律）
# ===========================================================================
#
# 实证来源：Desktop\pdf 15 篇（3 original / 3 review / 9 guideline）逐篇试错→汇聚：
#   R1 综述/指南未被挡在抽取之前 → KDIGO/ESC 各被抽出 85–104 行垃圾 needs_review，
#      是「抽取成功率低」观感的最大来源 → extract() 强制先甄别再抽取。
#   R2 连字编码损坏静默杀死短语正则（TZD 篇 0 行根因）："ti"→"L"/"7"/"8"
#      （ratio→raLo、national→naLonal）→ parse 前套修复层。
#   R3 甄别靠「声明类型 + 自指语境」，全文裸关键词禁用（综述引用他人 RCT/meta
#      会双向误判）：独立成行 article-type 标签 > 声明短语 > 自指信号。
#   R4 疗效事件数常在叙述句而非表格（FIGARO Table 2 是安全性表）→ occurred-in 模板。
#   R5 观察性 Cox 只有 aHR+CI → aHR 通道 + 比较对象上下文标签。

def _repair_text(s):
    """连字编码修复：把损坏 PDF 的 ToUnicode 缺陷映射还原。

    实证（TZD-痴呆 medRxiv 篇）：
      'ti' 连字 → 'L'（小写词内孤立大写 L）：national→naLonal、ratio→raLo；
      'ti' 连字 → '7'/'8'（小写词内孤立数字）：patients→pa7ents、Abbreviations→Abbrevia8ons。
    仅在小写字母**之间**替换，不碰真实词（'Lewis'、页码、数字统计均不受影响）。
    """
    if not s:
        return s
    s = re.sub(r"(?<=[a-z])L(?=[a-z])", "ti", s)
    s = re.sub(r"(?<=[a-z])[78](?=[a-z])", "ti", s)
    return s


# ---- 类型甄别信号（对齐 workspace classify_pdf.py v2 实证规则）----
# 独立成行的 article-type 标签（期刊把 "Review" / "Article" 单独成行印在刊名下方，
# 如 enm-2026-3080 的 "Review\nArticle"；标题里的 "Guidelines" 等词不算）
_STANDALONE_TYPE = [
    (r"(?m)^\s*(systematic\s+)?review\s*$", "review"),
    (r"(?m)^\s*meta[- ]?analysis\s*$", "review"),
    (r"(?m)^\s*guideline\s*$", "guideline"),
    (r"(?m)^\s*consensus\s+statement\s*$", "guideline"),
    (r"(?m)^\s*(study|trial)\s+protocol\s*$", "protocol"),
    (r"(?m)^\s*protocol\s*$", "protocol"),
    (r"(?m)^\s*original\s+(article|research)\s*$", "original"),
    (r"(?m)^\s*research\s+article\s*$", "original"),
]
# 声明短语（head 区：前 ~3500 字符）
_DECLARED_TYPE = [
    (r"review article|literature review|systematic review|meta[- ]?analysis|"
     r"umbrella review|scoping review|narrative review", "review"),
    (r"clinical practice guideline|practice guideline|"
     r"consensus (statement|conference|report)|position statement|"
     r"presidential advisory|expert (consensus|panel)|focus on \w+ (guidelines|guidance)",
     "guideline"),
    (r"study protocol|trial protocol|protocol (for a|of the|paper)|"
     r"protocol article|BMJ Open.*protocol", "protocol"),
    (r"original article|original research|research article|target trial emulation|"
     r"randomized(,? double[- ]blind)?[, ]*(controlled )?trial\b", "original"),
]
# 自指信号（全文：论文「本身就是」该类型的强证据，非引用）
_REVIEW_SELF = [
    r"our (systematic )?review", r"this (systematic |narrative )?review",
    r"in this review", r"we (systematically )?(searched|reviewed|screened)",
    r"prisma", r"we included \d+ (studies|trials|articles)",
    r"prospectively registered", r"(studies|trials) (were )?(included|eligible)",
    r"search strategy", r"(medline|pubmed|embase)[^.]{0,60}(searched|queried)",
]
_GUIDELINE_SELF = [
    r"we recommend", r"the (task force|panel|committee|writing group|work group) recommend",
    r"these (guidelines|recommendations)", r"we suggest",
    r"class (i{1,3}|iv)\b.{0,40}level of evidence",
    r"level of evidence|grade of recommendation",
    r"recommendations? (for|are|were|on)\b",
]
_ORIG_SELF = [
    r"we (enrolled|randomly assigned|prospectively (enrolled|assigned)|conducted)",
    r"we (designed|performed|carried out) (a|an|this) (study|trial|analysis)",
    r"patients? (were )?randomly assigned", r"inclusion criteria",
    r"baseline characteristics", r"we analyzed", r"intention[- ]to[- ]treat",
    r"primary (outcome|endpoint) (was|were)",
]

_REVIEW_HEAD = [r"\breview\b", r"systematic review", r"meta[- ]?analysis",
                r"\bsummary\b", r"advances? in", r"progress in", r"update on"]
_GUIDELINE_HEAD = [r"\bguideline", r"recommendation", r"consensus", r"advisory"]
_ORIG_HEAD = [r"effect of", r"efficacy (and safety )?of", r"association of",
              r"trial\b", r"original (article|research)", r"target trial"]


def classify_pdf(pdf_path, head_chars=3500):
    """强制类型甄别：review（综述）/ guideline（指南·共识·声明）/ original（原创）。

    规律 R3：独立成行标签(权重 100) > 声明短语(head, 4/命中) > 标题词(head, 2) >
    自指信号(全文, 2/命中，封顶 6)。全文裸关键词不参与（R3 双向误判实证）。
    返回 {type, confidence, declared, signals, n_pages}。
    """
    import fitz
    pdf_path = _norm_path(pdf_path)
    try:
        with fitz.open(pdf_path) as doc:
            n_pages = len(doc)
            text = "\n".join(doc[i].get_text() or "" for i in range(min(3, n_pages)))
            if n_pages > 3:  # 自指信号扫描扩展到全文（限制页数防超大指南拖慢）
                text += "\n" + "\n".join(
                    doc[i].get_text() or "" for i in range(3, min(n_pages, 40)))
    except Exception as e:  # noqa: BLE001
        return {"type": "unknown", "confidence": 0.0, "declared": "",
                "signals": [f"open-fail: {e}"], "n_pages": 0}
    text = _repair_text(text)
    head = text[:head_chars]
    head_low, text_low = head.lower(), text.lower()
    signals, declared = [], ""

    # 1) 独立成行 article-type 标签（最强，实证 enm 'Review\nArticle'）
    for pat, t in _STANDALONE_TYPE:
        if re.search(pat, head_low):
            declared = t
            signals.append("standalone-label: " + pat)
            break
    # 2) 声明短语
    if not declared:
        for pat, t in _DECLARED_TYPE:
            if re.search(pat, head_low):
                declared = t
                signals.append("declared: " + pat[:40])
                break
    # 3) 计分
    def _hits(pats, s):
        return sum(1 for p in pats if re.search(p, s))

    s_rev = _hits(_REVIEW_HEAD, head_low) * 2 + min(_hits(_REVIEW_SELF, text_low), 3) * 2
    s_gdl = _hits(_GUIDELINE_HEAD, head_low) * 2 + min(_hits(_GUIDELINE_SELF, text_low), 3) * 2
    s_org = _hits(_ORIG_HEAD, head_low) * 2 + min(_hits(_ORIG_SELF, text_low), 3) * 2
    # protocol（研究方案）：标题/头区 protocol 强短语 + 自指（will be recruited 等）
    s_prt = 0
    if re.search(r"study protocol|trial protocol|protocol (for a|of the)|"
                 r"this protocol|will be (recruited|enrolled|randomised|randomized|"
                 r"reported|estimated|compared|analysed|analyzed)|"
                 r"ethics (approval|and dissemination)", text_low):
        s_prt = 4 if re.search(r"protocol", head_low) else 2
    if declared == "review":
        s_rev += 100
    elif declared == "guideline":
        s_gdl += 100
    elif declared == "protocol":
        s_prt += 100
    elif declared == "original":
        s_org += 100
    total = s_rev + s_gdl + s_org + s_prt
    if total == 0:
        return {"type": "unknown", "confidence": 0.0, "declared": "",
                "signals": ["no-signal"], "n_pages": n_pages}
    scores = {"review": s_rev, "guideline": s_gdl, "original": s_org, "protocol": s_prt}
    best = max(scores, key=scores.get)
    conf = round(scores[best] / total, 2)
    return {"type": best, "confidence": conf, "declared": declared,
            "signals": signals[:6], "n_pages": n_pages}


def parse_pdf(pdf_path):
    """解析文本型 PDF，按「通用 → 专用」多级降级提取表格。

    返回 {pages: [{page, kind, text, table_tiers, tables}], n_pages}。
    每页 table_tiers 为按优先级排列的层级结果：
      T1 pdfplumber-lines   有框表（通用，最稳）；
      T2 pymupdf-word-rebuild  PyMuPDF word 坐标重建（无边框表专用精细抓取）。
    首个非空层即该页数据源（tables 字段 = 该层表格，向后兼容）；
    全部层为空 → 普通正文页（table_tiers=[]）。
    扫描页（无文本层）标记 kind="scanned"（P1 不支持 OCR，如实上报）。
    已评估不采用的中间层：pdfplumber text 对齐策略与 PyMuPDF find_tables
    （后者默认 lines 对无框表 0 检出；前者把正文撕成伪表）。
    """
    import fitz
    import pdfplumber

    pdf_path = _norm_path(pdf_path)
    pages = []
    with fitz.open(pdf_path) as doc:
        n_pages = len(doc)
        # 规律 R2：连字编码损坏会静默杀死所有短语正则 → 解析时统一修复
        texts = [_repair_text(p.get_text() or "") for p in doc]

    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text = texts[i] if i < len(texts) else page.extract_text() or ""
            if not text.strip():
                pages.append({"page": i + 1, "kind": "scanned", "text": "",
                              "table_tiers": [], "tables": []})
                continue
            table_tiers = []
            # T1：有框表（lines 策略，通用）——一页多表都会返回
            t1 = []
            try:
                t1 = page.extract_tables({
                    "vertical_strategy": "lines", "horizontal_strategy": "lines",
                    "snap_tolerance": 3, "intersection_tolerance": 3,
                }) or []
            except Exception:
                t1 = []
            t1 = [t for t in t1 if t and len(t) >= 2 and len(t[0]) >= 2]
            if t1:
                table_tiers.append({"tier": 1, "method": "pdfplumber-lines",
                                    "tables": t1})
            # T2：无边框表（PyMuPDF word 坐标按列/行聚类重建，专用精细）
            if not table_tiers:
                rebuilt = _rebuild_borderless_table(pdf_path, i)
                if rebuilt:
                    table_tiers.append({"tier": 2, "method": "pymupdf-word-rebuild",
                                        "tables": [rebuilt]})
            tables = table_tiers[0]["tables"] if table_tiers else []
            pages.append({"page": i + 1, "kind": "table" if tables else "text",
                          "text": text, "table_tiers": table_tiers,
                          "tables": tables})
    return {"pages": pages, "n_pages": n_pages}


def _rebuild_borderless_table(pdf_path, page_idx, min_rows=3, min_cols=3):
    """无边框表重建：基于 PyMuPDF 字符级 bbox，按 x0 聚类列、y0 聚类行。

    触发前提（由调用方保证）：该页 lines 策略未检出表格。此处再筛：
    页内存在一行含 ≥2 个数值/± 单元格且整体呈多列对齐 → 视为无边框表。
    返回 list[list[str]]（已对齐），或 None。

    v0.4 改进（2026-09-14，基于 78 篇 PDF 实证）：
      - min_cols 从 2 提至 3：2 列重建 99% 是正文分栏（2 列布局的期刊正文），
        真实数据表几乎都 ≥ 3 列（标签 + ≥ 2 数据列）
      - 列间距阈值从 20pt 降到 12pt：避免 5 列表被压成 2 列
      - 增加数值行占比过滤：数值行 < 50% 视为正文段落，不产出伪表
      - 增加行数下限：数值行 < 3 不产出（避免把零星数字当表）
    """
    import fitz
    _path = _norm_path(pdf_path)
    try:
        with fitz.open(_path) as doc:
            if page_idx >= len(doc):
                return None
            pg = doc[page_idx]
            words = pg.get_text("words")  # (x0,y0,x1,y1,text,block,line,word)
    except Exception:
        return None
    if len(words) < min_rows * min_cols:
        return None

    # 按 block 号（word[5]）聚类；标题锚 = 以 'Table N' 开头的短 block
    # （正文里的 '(Table 1)' 引用不是 block 开头，不会误命中）
    from collections import defaultdict
    by_block = defaultdict(list)
    for w in words:
        by_block[w[5]].append(w)
    title_y = None
    for bno, bwords in sorted(by_block.items()):
        btext = " ".join(w[4] for w in bwords).strip()
        if len(bwords) <= 15 and re.match(r"Table\s+\d+", btext):
            title_y = min(w[1] for w in bwords)
            break
    if title_y is None:
        # 无标题锚：回退到数值词最密的 block 顶部
        best, best_n = None, 0
        for bno, bwords in by_block.items():
            n = sum(1 for w in bwords if re.search(r"\d", w[4]) or "±" in w[4])
            if n > best_n:
                best, best_n = min(w[1] for w in bwords), n
        if best_n < 3:
            return None
        title_y = best
    words = [w for w in words if w[1] >= title_y - 2]

    # 行聚类：按 y0 排序、相邻差 <6pt 归同行；行内保留全部词（标签+数据），
    # 仅过滤整行数字词 < min_cols 的行（纯文本段落 / 脚注）
    ws_sorted = sorted(words, key=lambda w: (w[1], w[0]))
    row_groups = []
    for w in ws_sorted:
        if row_groups and w[1] - row_groups[-1][0] < 6:
            row_groups[-1][1].append(w)
        else:
            row_groups.append([w[1], [w]])
    data_rows = []
    for ybase, ws in row_groups:
        nums = [w for w in ws if re.search(r"\d", w[4])]
        if len(nums) >= min_cols:
            data_rows.append((ybase, sorted(ws, key=lambda x: x[0])))
    if len(data_rows) < min_rows:
        return None

    # v0.4：数值行占比过滤 — 数值行 < 50% 视为正文段落
    total_rows = len(row_groups)
    if total_rows > 0 and len(data_rows) / total_rows < 0.5:
        return None

    # 列聚类：收集所有 x0 中位数，按间隔 > 列阈值切分
    xcenters = sorted(set(round((w[0] + w[2]) / 2) for _, ws in data_rows for w in ws))
    if not xcenters:
        return None
    cols, cur = [], [xcenters[0]]
    for x in xcenters[1:]:
        if x - cur[-1] > 12:  # v0.4：列间距阈值从 20pt 降到 12pt
            cols.append(cur)
            cur = [x]
        else:
            cur.append(x)
    cols.append(cur)
    if len(cols) < min_cols:
        return None
    col_centers = [sum(c) / len(c) for c in cols]

    # 组装：每行按列中心归类词，合并同列词文本
    table = []
    for _, ws in data_rows:
        row = [""] * len(col_centers)
        for w in ws:
            cx = (w[0] + w[2]) / 2
            ci = min(range(len(col_centers)), key=lambda i: abs(col_centers[i] - cx))
            row[ci] = (row[ci] + " " + w[4]).strip() if row[ci] else w[4]
        table.append(row)
    if not table:
        return None
    # 对齐列数（短行补空）
    ncol = max(len(r) for r in table)
    table = [r + [""] * (ncol - len(r)) for r in table]
    # 首列作标签列补一行表头占位（模板靠标签识别，无需真表头）
    return table


# ---------------------------------------------------------------------------
# ②A 表格模板
# ---------------------------------------------------------------------------

def _norm(s):
    return re.sub(r"\s+", " ", _repair_text(str(s or ""))).strip().lower()


def _num(cell):
    """单元格 → float（容忍 '12', '12.0', '1,234', '12 (34%)' 里的首个数）。"""
    if cell is None:
        return None
    m = re.search(r"-?\d[\d,]*\.?\d*", str(cell).replace(",", ""))
    return float(m.group()) if m else None


def _frac(cell):
    """单元格 → (events, total)：匹配 '12/34'、'12 / 34 (35.3%)'。"""
    m = re.search(r"(\d+)\s*/\s*(\d+)", str(cell or ""))
    return (int(m.group(1)), int(m.group(2))) if m else None


_DICHOT_ARM_HINTS = ("experimental", "treatment", "intervention", "test",
                     "实验", "治疗", "干预", "试验组", "处理")
_CONTROL_HINTS = ("control", "placebo", "standard", "对照", "安慰剂", "常规")


def _arm_columns(header, body):
    """在表列里定位（实验列, 对照列）与计数列。返回 dict 或 None。

    策略：优先找 'n/N' 型计数列（_frac 可解析且数据行过半可解析）；若无，找事件数+n 列。
    两臂列按表头关键词打分；打分失败但恰两数据列时按左=实验、右=对照约定（并在
    checks 里提示人工确认臂方向——方向错误是四格表最致命错误）。
    """
    n_cols = max((len(r) for r in [header] + body), default=0)
    frac_cols, ev_cols = [], []
    for c in range(n_cols):
        col = [r[c] if c < len(r) else None for r in body]
        vals = [v for v in col if v not in (None, "")]
        if not vals:
            continue
        if sum(1 for v in vals if _frac(v)) >= max(1, len(vals) // 2):
            frac_cols.append(c)
        elif sum(1 for v in vals if _num(v) is not None) >= max(1, len(vals) // 2):
            ev_cols.append(c)

    # 表头臂打分
    exp_col = ctrl_col = None
    for c in range(n_cols):
        h = _norm(header[c] if c < len(header) else "")
        if any(k in h for k in _DICHOT_ARM_HINTS):
            exp_col = exp_col if exp_col is not None else c
        elif any(k in h for k in _CONTROL_HINTS):
            ctrl_col = ctrl_col if ctrl_col is not None else c

    if frac_cols:
        if exp_col is not None and ctrl_col is not None:
            return {"exp": exp_col, "ctrl": ctrl_col, "style": "frac",
                    "colmap": "keyword"}
        # 恰两个 n/N 计数列：按列序
        if len(frac_cols) >= 2:
            return {"exp": frac_cols[0], "ctrl": frac_cols[1], "style": "frac",
                    "colmap": "positional"}
        return None
    return None


def t_dichot(table, page_no, table_idx=0):
    """四格表模板。输入 pdfplumber 表（list[list]），返回 rows（0 或多条）。

    行选择：数据行须至少两臂列都含 n/N 计数。study 名取行首非空单元格。
    """
    if not table or len(table) < 2:
        return []
    header, body = table[0], [r for r in table[1:] if r and any(r)]
    if not body:
        return []
    cols = _arm_columns(header, body)
    if not cols:
        return []

    rows, skipped = [], []
    for r in body:
        # 标签 = 首列文本（可含数字如 "Death at 30d"；只排除 n/N 计数与纯数值单元格）
        first = str(r[0]).strip() if r and r[0] not in (None, "") else ""
        label = first if (first and _frac(first) is None
                          and not re.fullmatch(r"[\d.,\s()%/-]+", first)) else None
        fe = _frac(r[cols["exp"]] if cols["exp"] < len(r) else None)
        fc = _frac(r[cols["ctrl"]] if cols["ctrl"] < len(r) else None)
        if not (fe and fc and label):
            if fe or fc:
                skipped.append(label or "?")
            continue
        rows.append({
            "study": label,
            "ai": fe[0], "bi": fe[1] - fe[0],   # 实验组：事件 / 非事件
            "ci": fc[0], "di": fc[1] - fc[0],   # 对照组：事件 / 非事件
            "_meta": {"source": "table", "page": page_no, "table": table_idx,
                      "template": "T_DICHOT", "colmap": cols["colmap"],
                      "anchor": f"p{page_no} table#{table_idx + 1} row '{label}'"},
        })
    return rows


def t_continuous(table, page_no, table_idx=0):
    """连续结局模板：找 n / mean / SD × 两臂 列（关键词打分）。

    输出 te=mean差、sete 由 SD 与 n 合成（原始数值附 raw，供校验/人工）。
    匹配不到明确 mean/SD 结构 → 返回 []（宁缺勿错）。
    """
    if not table or len(table) < 2:
        return []
    header, body = table[0], [r for r in table[1:] if r and any(r)]
    # 表级防御：纯基线特征表（baseline/demographic/age… 且无结局词）不产效应量
    flat_hdr = " ".join(str(c or "") for c in header).lower()
    flat_body = " ".join(str(c or "") for r in body for c in r).lower()
    is_outcome = bool(_OUTCOME_KW.search(flat_hdr + " " + flat_body))
    if _BASELINE_KW.search(flat_hdr) and not is_outcome:
        return []
    # n (%) 计数表防御：表内声明 'n (%)'/'no. (%)' → 全表为计数+百分数，
    # '2216 (93.4)' 会被 mean±(sd) 行内正则误配成对 → 跳过
    if re.search(r"n\s*\(%\)|no\.\s*\(%\)|number\s*\(%\)", flat_hdr + " " + flat_body):
        return []
    # n (%) 计数表防御 2：无声明但数值对几乎全为整数对（真实 m±SD 几乎必含小数）
    m_all = re.compile(r"(-?\d+\.?\d*)\s*[±(]\s*(\d+\.?\d*)")
    all_pairs = [q for r in body for v in r if v is not None and "/" not in str(v)
                 for q in m_all.findall(str(v))]
    if all_pairs and sum(1 for a, b in all_pairs
                         if "." not in a and "." not in b) >= 0.8 * len(all_pairs):
        return []
    n_cols = max((len(r) for r in [header] + body), default=0)
    kinds = {}
    for c in range(n_cols):
        h = _norm(header[c] if c < len(header) else "")
        col = [r[c] if c < len(r) else None for r in body]
        vals = [v for v in col if v not in (None, "")]
        if not vals:
            continue
        if re.search(r"\bn\b|no\.|样本|例数", h) and all(_num(v) is not None and _num(v) == int(_num(v)) for v in vals[:3]):
            kinds.setdefault("n", c)
        elif re.search(r"mean|均值|均数", h):
            kinds.setdefault("mean", c)
        elif re.search(r"\bsd\b|s\.d\.|std|标准差", h):
            kinds.setdefault("sd", c)
        elif re.search(r"\bse\b|标准误", h):
            kinds.setdefault("se", c)
    if not {"n", "mean"}.issubset(kinds) or ("sd" not in kinds and "se" not in kinds):
        kinds = None  # 列模式不成立；仍可走行内 'mean (sd)' 文本模式

    # 两臂拆分：优先行内 'mean (sd)' 文本对（P1 主路径）；列模式留 P2 扩展
    out = []
    m_re = re.compile(r"(-?\d+\.?\d*)\s*[±(]\s*(\d+\.?\d*)")
    for r in body:
        first = str(r[0]).strip() if r and r[0] not in (None, "") else ""
        label = first if (first and _frac(first) is None
                          and not re.fullmatch(r"[\d.,\s()%/-]+", first)
                          and not m_re.search(first)) else None
        # 行内文本 'mean (sd)' 对（排除 n/N 型单元格：'30/100 (30.0%)' 会误配 '100 (30.0'》）
        pairs = [m_re.findall(str(v)) for v in r
                 if v is not None and "/" not in str(v)]
        pairs = [p for p in pairs if p]
        # 恰好 2 组 m±SD 才配两臂；>2 组是基线多臂/未知结构，宁缺勿错
        if label and len(pairs) == 2:
            (m1, s1), (m2, s2) = pairs[0][0], pairs[1][0]
            n1 = _num(r[kinds["n"]]) if kinds and kinds.get("n") is not None \
                and kinds["n"] < len(r) else None
            n2 = None
            # n 列缺失时回退：行内整数对（如 n 列值与另一个 n）
            nums = [_num(v) for v in r if v is not None and _num(v) is not None]
            ints = [x for x in nums if x and x == int(x)]
            if n1 is None and len(ints) >= 1:
                n1 = ints[0]
                if n2 is None and len(ints) >= 2:
                    n2 = ints[1]
                if n1 and n2 is None:
                    # 单 n 回退：两组共用同一 n（常见于同 n 设计），交人工确认
                    n2 = n1
            if n1 and n2 and float(s1) > 0 and float(s2) > 0:
                diff = float(m1) - float(m2)
                se = math.sqrt(float(s1) ** 2 / n1 + float(s2) ** 2 / n2)
                out.append({
                    "study": label, "te": round(diff, 6), "sete": round(se, 6),
                    "_meta": {"source": "table", "page": page_no,
                              "table": table_idx + 1, "template": "T_CONTINUOUS",
                              "raw": {"m1": float(m1), "sd1": float(s1), "n1": n1,
                                      "m2": float(m2), "sd2": float(s2), "n2": n2},
                              "anchor": f"p{page_no} table#{table_idx + 1} row '{label}'"},
                })
    return out


# ===========================================================================
# ②A-2 数值解析硬化 + 效应量/连续型结局增强（v0.2，经 12 篇 PDF 实证）
# ===========================================================================
#
# 相对原 t_continuous 的增强：
#   1. 数值解析硬化 _f：支持前导点(.27)、千分位、四种连字符；CI 分隔符类 _SEP。
#   2. 效应量叙述模板 EXTRACTION_TEMPLATES（HR/OR/RR/MD），命中即回填 te/sete
#      （te=ln(est) 仅比值度量；MD 用原值；sete=(ln(hi)-ln(lo))/3.92 对称 CI）。
#   3. 效应量表格模板 t_effect_table：森林图结局表（2×2 内嵌 + HR 列 → 双源）。
#   4. 连续型结局表格模板 t_cont_table：重复测量表（Changes/Beta 列）、标准两臂表。
#   5. 连续型叙述 narrative_continuous：正文 MD (95% CI)。
# 置信策略（HITL·准确度优先）：双源(2×2↔HR列)或带报告OR交叉验证→verified；
#   单源叙述/表格→needs_review（报告数字逐字+确定变换，人工一键确认进 Block B）。

# 分隔符类：to / en-dash / em-dash / ascii 连字符 / 数学减号(U+2212) / ~
_SEP = r"(?:to|–|—|-|−|~)"
# 通用浮点（支持前导点 .27 与千分位）
_FNUM = r"-?(?:\d[\d,]*\.?\d*|\.\d+)"
_F = re.compile(_FNUM)


def _f(cell):
    """单元格 → float，容忍 '12'、'12.0'、'.27'、'1,234'、'-0.161'、'−0.161'(U+2212)。"""
    if cell is None:
        return None
    # 统一数学减号 U+2212 → ascii '-'
    s = str(cell).replace("−", "-")
    m = _F.search(s.replace(",", ""))
    return float(m.group()) if m else None


# CI 紧凑式（表格常见）：'0.74 (0.65–0.85)' / '0.74 [0.65 to 0.85]'
_EFFECT_CI = re.compile(
    rf"({_FNUM})\s*[\(\[]\s*({_FNUM})\s*{_SEP}\s*({_FNUM})\s*[\)\]]")


def _effect_re(label_alt):
    """按度量标签构造 'label te ; 95% CI lo-hi' 正则（间隔段禁括号、放行 95% 中的数字）。

    te 与 CI 锚之间允许一个 '(' —— 支持 BMC 系嵌套括号写法
    '(odds ratio 1.71 (95% CI 0.93 to 3.16))'。
    """
    return re.compile(
        rf"(?:{label_alt})\b"
        r"[^0-9\-–—−()]{0,6}?"
        rf"(?P<te>{_FNUM})"
        # te→CI 锚间隔允许括号（BMC 系嵌套写法 '(OR 1.71 (95% CI 0.93 to 3.16))'）；
        # 误越界由 _effect_from_match 的 lo<=te<=hi 校验兜底
        r".{0,80}?"
        r"(?:95\s*%\s*(?:confidence interval)?\s*(?:\[ci\])?\s*|ci)\b"
        r"[ ,:(\n]*"  # CI 锚与 lo 间允许换行（PDF 文本 '95% CI,\n0.76-0.92' 常见）
        rf"(?P<lo>{_FNUM})\s*{_SEP}\s*(?P<hi>{_FNUM})",
        re.IGNORECASE)


EXTRACTION_TEMPLATES = {
    # 规律 R5：aHR（adjusted hazard ratio）通道 —— "aHR 0.87 (95% CI 0.36–2.27)"
    # (?<![a-z])ahrs? 排除 'pharmacy' 等词内命中，并兼容复数 "(aHRs)"
    "HR": {"measure": "HR",
           "re": _effect_re(r"adjusted hazard ratio|hazard ratio|(?<![a-z])ahrs?\b|\bhr\b")},
    "OR": {"measure": "OR", "re": _effect_re(r"odds ratio|\bor\b")},
    "RR": {"measure": "RR", "re": _effect_re(r"risk ratio|relative risk|rate ratio|\brr\b")},
    "MD": {"measure": "MD", "re": _effect_re(r"mean difference|difference in means|\bmd\b")},
}

_PVAL = re.compile(
    r"(?:p[\s-]?value|(?<![a-zA-Z])p)\s*[=<]\s*"
    r"(\.?\d[\d,]*\.?\d*(?:[eE][-+]?\d+)?)\s*(?:\(|\)|\b|,|\.|;|$)",
    re.IGNORECASE)

_EMBED_2X2 = re.compile(r"(\d+)\s*/\s*(\d+)\s+(\d+)\s*/\s*(\d+)")
_CONT_PAIR = re.compile(rf"(?P<m>{_FNUM})\s*(?:±|\+/-|±)\s*(?P<s>{_FNUM})", re.IGNORECASE)
_CONT_BETA_CI = re.compile(
    rf"(?P<beta>{_FNUM})\s*[\(\[]\s*(?P<lo>{_FNUM})\s*(?:{_SEP}|,)\s*(?P<hi>{_FNUM})\s*[\)\]]")
_OUTCOME_KW = re.compile(
    r"change|changes|δ|Δ|after\s*[-–]?\s*before|post[-\s]?treatment|"
    r"beta|coefficient|difference|outcome|effect|vs\.?\s*placebo|"
    r"干预|变化|差值|效应|结局", re.IGNORECASE)
_BASELINE_KW = re.compile(r"baseline|demographic|characteristic|age|体重|bmi", re.IGNORECASE)
_DESCR_KW = re.compile(r"point difference|proportion|percentage|%|patients with|"
                        r"subjects with|n\s*=|no\. of", re.I)


def _effect_from_match(measure, m, page, text):
    """由叙述正则命中构造效应量记录（比值度量 te=ln；MD 用原值）。

    规律 R5：观察性研究效应量锚在「比较对象」上（'TZD vs DPP-4: aHR 0.87 …'、
    'compared with DPP-4 (aHR 0.87…)'）→ 回看 160 字符提取比较上下文做 study 标签，
    否则退回普通前置词标签。
    """
    try:
        te = float(m.group("te").replace(",", ""))
        lo = float(m.group("lo").replace(",", ""))
        hi = float(m.group("hi").replace(",", ""))
    except (ValueError, AttributeError):
        return None
    if not (lo > 0 and hi > lo and lo <= te <= hi):
        return None
    sete = (math.log(hi) - math.log(lo)) / 3.92 if lo > 0 else None
    if sete is None or sete <= 0:
        return None
    pre = text[max(0, m.start() - 50):m.start()].strip()
    # 比较上下文标签（R5）：优先 'X vs Y' / 'compared with/to Y' / 'X versus Y'
    # 尾部容忍 '('（'(aHR 0.87…' 括号紧贴标签）；词首允许数字（SGLT2 / DPP-4）
    ctx = re.sub(r"\s+", " ", text[max(0, m.start() - 160):m.start()].replace("\n", " ")).strip()
    ctx = re.sub(r"[\(\[\{]+$", "", ctx).strip()
    study = ""
    cm = re.search(
        r"([A-Za-z0-9][\w\-/]*(?:\s+[\w\-/]+){0,3}?)\s+(?:vs\.?|versus)\s+"
        r"([A-Za-z0-9][\w\-/]*(?:\s+[\w\-/]+){0,3}?)\s*$",
        ctx)
    if cm:
        study = f"{cm.group(1)} vs {cm.group(2)}"[-60:]
    else:
        cm2 = re.search(
            r"compared (?:with|to)\s+([A-Za-z0-9][\w\-/]*(?:\s+[\w\-/]+){0,3}?)\s*$",
            ctx)
        if cm2:
            study = f"vs {cm2.group(1)}"[-60:]
    if not study:
        labs = re.findall(r"[A-Za-z][A-Za-z ]{0,45}", pre)
        study = labs[-1].strip() if labs and " " in labs[-1] else ""
        if not study or len(study) > 40:
            study = f"{measure} (p{page})"
        else:
            study = study[-40:]
    snippet = text[max(0, m.start() - 60):m.end() + 40].replace("\n", " ").strip()
    rec = {
        "study": study,
        "measure": measure,
        "te": round(math.log(te), 6) if measure != "MD" else round(te, 6),
        "sete": round(sete, 6),
        "reported": {"est": round(te, 4), "ci": [round(lo, 4), round(hi, 4)]},
        "_meta": {"source": "narrative", "page": page,
                  "template": f"T_{measure}_CI",
                  "anchor": f"p{page} text: …{snippet[:80]}…",
                  "snippet": snippet},
    }
    return rec


def narrative_effects(pages):
    """扫描正文，返回效应量候选（HR/OR/RR/MD/P）。"""
    out = []
    for p in pages:
        if p["kind"] == "scanned":
            continue
        text = p["text"]
        for measure, spec in EXTRACTION_TEMPLATES.items():
            for m in spec["re"].finditer(text):
                rec = _effect_from_match(measure, m, p["page"], text)
                if rec:
                    out.append(rec)
        # v0.4：pooled/overall 句式（meta 分析论文高频）
        for rec in _narrative_pooled_effects(text, p["page"]):
            out.append(rec)
        for m in _PVAL.finditer(text):
            try:
                pv = float(m.group(1).replace(",", ""))
            except ValueError:
                continue
            if pv > 1:  # P 值域 [0,1]；拦截 'group 30' 类残网命中
                continue
            out.append({
                "kind": "pvalue",
                "measure": "P",
                "reported": {"p": round(pv, 6), "sig": pv < 0.05},
                "_meta": {"source": "narrative", "page": p["page"],
                          "template": "T_PVALUE",
                          "anchor": f"p{p['page']} text: …{text[max(0,m.start()-50):m.end()+20].replace(chr(10),' ').strip()}…"},
            })
    return out


# v0.4：pooled/overall 效应量句式（meta 分析论文高频）
# 典型句式：
#   "The pooled OR was 1.25 (95% CI 1.08 to 1.45)"
#   "Overall, the hazard ratio was 0.87 (95% CI 0.76–0.98)"
#   "Meta-analysis showed a significant reduction (RR 0.49, 95% CI 0.28 to 0.85)"
#   "The combined estimate was HR 0.82 (0.71–0.95)"
#   "Pooled analysis: OR = 1.35 (95% CI 1.12–1.63)"
_POOLED_EFFECT_RE = re.compile(
    r"(?:pooled|overall|combined|summary|meta[- ]?analysis|total)\s*"
    r"(?:analysis|estimate|effect|result|outcome|was|showed|indicated|demonstrated|:\s*|\s+)"
    r"(?:[\w\s,]{0,40}?)?"
    r"(?:hazard ratio|odds ratio|risk ratio|relative risk|rate ratio|HR|OR|RR|MD|mean difference)?"
    r"[\s:=]*"
    rf"(?P<te>{_FNUM})"
    r"[\s,]*"
    r"(?:\(?\s*95\s*%\s*(?:confidence interval|CI)?\s*\)?\s*)?"
    rf"[\(\[]\s*(?P<lo>{_FNUM})\s*{_SEP}\s*(?P<hi>{_FNUM})\s*[\)\]]",
    re.IGNORECASE)

# 反向句式："HR 0.87 (95% CI 0.76–0.98) overall" / "OR 1.25 (1.08-1.45) in the pooled analysis"
_POOLED_EFFECT_RE_V2 = re.compile(
    rf"(?P<te>{_FNUM})\s*"
    r"(?:\(?\s*95\s*%\s*(?:confidence interval|CI)?\s*\)?\s*)?"
    rf"[\(\[]\s*(?P<lo>{_FNUM})\s*{_SEP}\s*(?P<hi>{_FNUM})\s*[\)\]]"
    r"\s*,?\s*(?:pooled|overall|combined|summary|meta[- ]?analysis|total)",
    re.IGNORECASE)


def _narrative_pooled_effects(text, page):
    """抽取 pooled/overall 句式的效应量。"""
    out = []
    for regex, direction in [(_POOLED_EFFECT_RE, "prefix"), (_POOLED_EFFECT_RE_V2, "suffix")]:
        for m in regex.finditer(text):
            try:
                te = float(m.group("te").replace(",", ""))
                lo = float(m.group("lo").replace(",", ""))
                hi = float(m.group("hi").replace(",", ""))
            except (ValueError, AttributeError):
                continue
            if not (lo > 0 and hi > lo and lo <= te <= hi):
                continue
            sete = (math.log(hi) - math.log(lo)) / 3.92
            if sete <= 0:
                continue
            # 判断度量类型
            measure = "HR"  # 默认
            ctx = text[max(0, m.start() - 80):m.end() + 40].lower()
            if "odds ratio" in ctx or re.search(r"\bor\b", ctx):
                measure = "OR"
            elif "risk ratio" in ctx or "relative risk" in ctx or "rate ratio" in ctx or re.search(r"\brr\b", ctx):
                measure = "RR"
            elif "mean difference" in ctx or re.search(r"\bmd\b", ctx):
                measure = "MD"
            elif "hazard ratio" in ctx or re.search(r"\bhr\b", ctx):
                measure = "HR"
            snippet = text[max(0, m.start() - 60):m.end() + 40].replace("\n", " ").strip()
            out.append({
                "study": f"pooled (p{page})",
                "measure": measure,
                "te": round(math.log(te), 6) if measure != "MD" else round(te, 6),
                "sete": round(sete, 6),
                "reported": {"est": round(te, 4), "ci": [round(lo, 4), round(hi, 4)]},
                "_meta": {"source": "narrative", "page": page,
                          "template": "T_POOLED_EFFECT",
                          "anchor": f"p{page} text: …{snippet[:80]}…",
                          "snippet": snippet},
            })
    # v0.4：subgroup 句式
    for rec in _narrative_subgroup_effects(text, page):
        out.append(rec)
    return out


# v0.4：subgroup 分析句式
# 典型："Subgroup analysis showed that HR was 0.78 (95% CI 0.65–0.94) in patients aged <65"
#        "In the subgroup of patients with diabetes, the OR was 1.45 (95% CI 1.12–1.88)"
#        "Among patients receiving intervention A, the pooled RR was 0.62 (0.48–0.80)"
_SUBGROUP_EFFECT_RE = re.compile(
    r"(?:subgroup\s+analysis|in\s+the\s+subgroup|among\s+(?:patients|subjects|participants)|"
    r"in\s+(?:patients|subjects|participants)\s+(?:with|receiving|aged|having))"
    r"[\w\s,]{0,60}?"
    r"(?:hazard ratio|odds ratio|risk ratio|relative risk|rate ratio|HR|OR|RR|MD|mean difference)?"
    r"[\s:=]*"
    rf"(?P<te>{_FNUM})"
    r"[\s,]*"
    r"(?:\(?\s*95\s*%\s*(?:confidence interval|CI)?\s*\)?\s*)?"
    rf"[\(\[]\s*(?P<lo>{_FNUM})\s*{_SEP}\s*(?P<hi>{_FNUM})\s*[\)\]]",
    re.IGNORECASE)


def _narrative_subgroup_effects(text, page):
    """抽取 subgroup 句式的效应量。"""
    out = []
    for m in _SUBGROUP_EFFECT_RE.finditer(text):
        try:
            te = float(m.group("te").replace(",", ""))
            lo = float(m.group("lo").replace(",", ""))
            hi = float(m.group("hi").replace(",", ""))
        except (ValueError, AttributeError):
            continue
        if not (lo > 0 and hi > lo and lo <= te <= hi):
            continue
        sete = (math.log(hi) - math.log(lo)) / 3.92
        if sete <= 0:
            continue
        measure = "HR"
        ctx = text[max(0, m.start() - 80):m.end() + 40].lower()
        if "odds ratio" in ctx or re.search(r"\bor\b", ctx):
            measure = "OR"
        elif "risk ratio" in ctx or "relative risk" in ctx or "rate ratio" in ctx or re.search(r"\brr\b", ctx):
            measure = "RR"
        elif "mean difference" in ctx or re.search(r"\bmd\b", ctx):
            measure = "MD"
        # 提取 subgroup 标签
        pre = text[max(0, m.start() - 120):m.start()].strip()
        subgroup_m = re.search(
            r"(?:subgroup\s+(?:of\s+)?|among\s+|in\s+(?:patients|subjects|participants)\s+(?:with|receiving|aged|having)\s+)"
            r"([\w\s\-/]{3,50}?)(?:,|\s+(?:the|HR|OR|RR|MD))",
            pre, re.IGNORECASE)
        subgroup_label = subgroup_m.group(1).strip() if subgroup_m else "subgroup"
        snippet = text[max(0, m.start() - 60):m.end() + 40].replace("\n", " ").strip()
        out.append({
            "study": f"{subgroup_label} (p{page})",
            "measure": measure,
            "te": round(math.log(te), 6) if measure != "MD" else round(te, 6),
            "sete": round(sete, 6),
            "reported": {"est": round(te, 4), "ci": [round(lo, 4), round(hi, 4)]},
            "_meta": {"source": "narrative", "page": page,
                      "template": "T_SUBGROUP_EFFECT",
                      "anchor": f"p{page} text: …{snippet[:80]}…",
                      "snippet": snippet},
        })
    return out


def t_effect_table(table, page_no, table_idx=0):
    """效应量（HR/OR/RR）表格模板。返回行（可同时含 ai/bi/ci/di + te/sete）。

    触发条件（防误抓连续型「均值±CI」列）：
      - 表头列含 HR/OR/RR/hazard/odds/risk 等效应量关键词，或
      - 首列内嵌 2×2 计数（森林图典型特征：'386/2371 502/2371'）。
    二者皆无 → 视为非效应量表，返回 []（交 t_cont_table / 跳过）。
    """
    if not table or len(table) < 2:
        return []
    header, body = table[0], [r for r in table[1:] if r and any(r)]
    if not body:
        return []

    n_cols = max((len(r) for r in [header] + body), default=0)
    eff_col = None
    hdr_effect = False
    for c in range(n_cols):
        col = [r[c] if c < len(r) else None for r in body]
        vals = [str(v) for v in col if v not in (None, "")]
        if not vals:
            continue
        h = _norm(header[c] if c < len(header) else "")
        is_eff = any(k in h for k in ("hr", "hazard", "odds", "or", "risk",
                                     "rr", "relative", "ratio", "hazard ratio"))
        if is_eff and eff_col is None:
            eff_col, hdr_effect = c, True
        if sum(1 for v in vals if _EFFECT_CI.search(v)) >= max(1, len(vals) // 3):
            eff_col = eff_col if eff_col is not None else c

    lbl_col = 0
    label_has_2x2 = any(_EMBED_2X2.search(str(r[lbl_col])) for r in body
                        if lbl_col < len(r) and r[lbl_col])

    if eff_col is None or not (hdr_effect or label_has_2x2):
        return []

    if hdr_effect:
        h0 = _norm(header[eff_col])
        if "hazard" in h0 or " hr" in h0:
            measure = "HR"
        elif "odds" in h0 or re.search(r"\bor\b", h0):
            measure = "OR"
        elif "risk" in h0 or "rr" in h0 or "relative" in h0:
            measure = "RR"
        else:
            measure = "HR/OR/RR"
    else:
        measure = "HR"

    rows = []
    for r in body:
        cell = r[eff_col] if eff_col < len(r) else None
        if not cell:
            continue
        m = _EFFECT_CI.search(str(cell))
        if not m:
            continue
        te0, lo, hi = _f(m.group(1)), _f(m.group(2)), _f(m.group(3))
        if not (lo > 0 and hi > lo and lo <= te0 <= hi):
            continue
        label = str(r[lbl_col]).strip() if lbl_col < len(r) and r[lbl_col] else ""
        label_clean = re.sub(r"\s*\d+/\d+\s+\d+/\d+.*$", "", label).strip() or label
        rec = {
            "study": label_clean[:60],
            "measure": measure,
            "te": round(math.log(te0), 6),
            "sete": round((math.log(hi) - math.log(lo)) / 3.92, 6),
            "reported": {"est": round(te0, 4), "ci": [round(lo, 4), round(hi, 4)]},
            "_meta": {"source": "table", "page": page_no, "table": table_idx + 1,
                      "template": "T_EFFECT_TABLE",
                      "anchor": f"p{page_no} table#{table_idx + 1} row '{label_clean[:40]}'"},
        }
        em = _EMBED_2X2.search(label)
        if em:
            ae, ne, ac, nc = (int(em.group(i)) for i in (1, 2, 3, 4))
            if ne >= ae and nc >= ac:
                rec["ai"], rec["bi"] = ae, ne - ae
                rec["ci"], rec["di"] = ac, nc - ac
        rows.append(rec)
    return rows


def _cont_pairs(cell):
    """从单元格抽取所有 (mean, sd) 对（仅真正的 ± 符号）。"""
    if cell is None:
        return []
    return [(float(a.replace(",", "")), float(b.replace(",", "")))
            for a, b in _CONT_PAIR.findall(str(cell))]


def t_forest_table(table, page_no, table_idx=0):
    """森林图/效应量汇总表模板 — meta 分析论文最常见表格式。

    特征：
      - 首列：研究名 + 出版年（如 "Smith 2020" 或 "Smith et al., 2020"）
      - 效应列：估计值 + CI，如 "1.25 (1.08-1.45)" 或 "1.25 (95% CI 1.08 to 1.45)"
      - 可选权重列：如 "15.2%" 或 "●●●" (star plot)
      - 可选 Overall/Subtotal 行

    与 t_effect_table 的区别：
      - t_effect_table 要求表头含 HR/OR/RR 关键词，适合 RCT 森林图表
      - t_forest_table 更宽松：只要数据列含 (lo-hi) 格式即可，适合 meta 分析汇总表

    v0.4 新增（2026-09-14，基于 78 篇 PDF 实证：meta 论文最常见的表格式）。
    """
    if not table or len(table) < 2:
        return []
    header, body = table[0], [r for r in table[1:] if r and any(r)]
    if not body:
        return []

    n_cols = max((len(r) for r in [header] + body), default=0)
    if n_cols < 2:
        return []

    # 找效应列：含 (lo-hi) 格式数据最多的列
    best_col = None
    best_score = 0
    for c in range(1, n_cols):
        col = [r[c] if c < len(r) else None for r in body]
        vals = [str(v) for v in col if v not in (None, "")]
        if not vals:
            continue
        ci_hits = sum(1 for v in vals if _EFFECT_CI.search(v))
        pct_hits = sum(1 for v in vals if re.search(r"^\s*\d+(\.\d+)?\s*%\s*$", v))
        # CI 命中优先，权重百分比列次之
        score = ci_hits * 3 + pct_hits
        if score > best_score:
            best_score = score
            best_col = c

    if best_col is None or best_score < 2:
        return []

    # 判断效应量类型
    hdr_low = " ".join(str(c or "") for c in header).lower()
    measure = "HR"
    if any(k in hdr_low for k in ("or", "odds ratio")):
        measure = "OR"
    elif any(k in hdr_low for k in ("rr", "risk ratio", "relative risk", "rate ratio")):
        measure = "RR"
    elif any(k in hdr_low for k in ("md", "mean difference", "smd", "wmd", "weighted")):
        measure = "MD"
    elif any(k in hdr_low for k in ("hr", "hazard ratio")):
        measure = "HR"
    else:
        # 根据列位置和数据推断：第2列通常是效应量
        # 检查首列是否有研究名特征（含年份或 "et al."）
        label_col = [r[0] for r in body if r and r[0]]
        study_pattern = re.compile(r"\b\d{4}\b|et al|vs\.|cohort|trial|study", re.I)
        if sum(1 for l in label_col if study_pattern.search(str(l))) >= len(label_col) * 0.3:
            measure = "HR"  # 默认假设为 HR（最常见）
        else:
            measure = "HR/OR/RR"

    rows = []
    for r in body:
        cell = r[best_col] if best_col < len(r) else None
        if not cell:
            continue
        m = _EFFECT_CI.search(str(cell))
        if not m:
            continue
        te0 = _f(m.group(1))
        lo = _f(m.group(2))
        hi = _f(m.group(3))
        if te0 is None or lo is None or hi is None:
            continue
        if not (lo > 0 and hi > lo and lo <= te0 <= hi):
            continue

        label = str(r[0]).strip() if r and r[0] else ""
        label_clean = re.sub(r"\s+", " ", label).strip()[:60]
        if not label_clean:
            continue

        rec = {
            "study": label_clean,
            "measure": measure,
            "te": round(math.log(te0), 6) if measure != "MD" else round(te0, 6),
            "sete": round((math.log(hi) - math.log(lo)) / 3.92, 6) if measure != "MD" else None,
            "reported": {"est": round(te0, 4), "ci": [round(lo, 4), round(hi, 4)]},
            "_meta": {
                "source": "table", "page": page_no, "table": table_idx + 1,
                "template": "T_FOREST_TABLE",
                "anchor": f"p{page_no} table#{table_idx + 1} row '{label_clean[:40]}'",
            },
        }
        # 提取权重（如果有的话）
        for c in range(1, len(r)):
            if c == best_col:
                continue
            w = r[c] if c < len(r) else None
            if w and re.search(r"^\s*\d+(\.\d+)?\s*%\s*$", str(w)):
                rec["weight"] = round(_f(w) / 100, 4) if _f(w) else None
                break
        rows.append(rec)
    return rows


def t_meta_table(table, page_no, table_idx=0):
    """Meta 分析纳入研究特征表模板。

    典型格式（meta 分析论文 Table 1/Table 2）：
      | Study | Year | Design | n | Age | Intervention | ... |
      | Smith et al. | 2020 | RCT | 256 | 58±12 | Drug A vs Placebo | ... |

    特点：每行是一项研究，不含效应量数据。
    用途：提取研究特征信息供后续分析（研究数量、总样本量等）。

    v0.4 新增（2026-09-14，meta 论文 Table 1/2 高频）。
    """
    if not table or len(table) < 3:
        return []
    header, body = table[0], [r for r in table[1:] if r and any(r)]
    if not body:
        return []

    n_cols = max((len(r) for r in [header] + body), default=0)
    if n_cols < 3:
        return []

    # v0.4.1：表头必须含特征关键词（至少 2 个）
    flat_hdr = " ".join(str(c or "") for c in header).lower()
    study_kw = ("study", "author", "year", "design", "n ", "sample", "age",
                "intervention", "country", "population", "participants",
                "characteristic", "baseline")
    kw_hits = sum(1 for k in study_kw if k in flat_hdr)
    if kw_hits < 2:
        return []

    # 判断每行是否为研究行（首列含年份或研究名模式）
    study_rows = []
    for r in body:
        if not r or not r[0]:
            continue
        label = str(r[0]).strip()
        if len(label) < 3 or len(label) > 100:
            continue
        # v0.4.1：过滤参考文献特征（含期刊卷号、页码范围、DOI）
        if re.search(r"\b\d{1,2}\s*[\(\[]\s*\d{1,2}\s*[\)\]]|pp?\s*\d+|doi:|vol(ume)?\s*\d+|http", label, re.I):
            continue
        # v0.4.1：过滤期刊引用缩写（如 "Clin. Nutr." "Chem Res" "JAMA" 等）
        if re.search(r"\b[A-Z][a-z]{1,4}\.\s*[A-Z][a-z]{1,4}\.?\s*$|^\d+\s+[A-Z][a-z]{2,}\s*$", label):
            continue
        # v0.4.1：过滤编号引用（如 "294. " "716. " 开头）
        if re.match(r"^\d{1,4}\.\s", label):
            continue
        # v0.4.1：过滤期刊名特征（含 "J " 或 "J." 后跟大写字母，如 "Eur Heart J"）
        if re.search(r"\b[A-Z][a-z]{1,3}\s+[A-Z][a-z]{2,}\s+J\b", label):
            continue
        # v0.4.1：过滤子组标签（以 • 或 - 开头，或全小写+数字）
        if re.match(r"^[•\-\*]\s", label) or re.match(r"^[a-z]+\s+\d+$", label):
            continue
        # 研究名特征：含年份、"et al"、或首字母大写的作者名
        has_year = re.search(r"\b(19|20)\d{2}\b", label)
        has_author = re.search(r"[A-Z][a-z]+,?\s+(?:et al|[A-Z])", label)
        has_study_kw = re.search(r"\b(trial|study|cohort|registry|analysis)\b", label, re.I)
        if has_year or has_author or has_study_kw:
            # v0.4.1：要求至少一个非首列含数值（样本量、年龄等）
            has_numeric = False
            for cell in r[1:]:
                if cell and re.search(r"\d+", str(cell)):
                    has_numeric = True
                    break
            if not has_numeric:
                continue
            study_rows.append({
                "study": re.sub(r"\s+", " ", label)[:60],
                "_meta": {
                    "source": "table", "page": page_no, "table": table_idx + 1,
                    "template": "T_META_TABLE",
                    "anchor": f"p{page_no} table#{table_idx + 1} row '{label[:40]}'",
                    "n_studies_in_table": 0,  # 后填
                }
            })

    if len(study_rows) >= 2:
        for sr in study_rows:
            sr["_meta"]["n_studies_in_table"] = len(study_rows)
        return study_rows
    return []


def t_cont_table(table, page_no, table_idx=0):
    """连续型结局表格模板。返回 MD 效应量行（供 Block B 连续型 meta）。

    适用：重复测量表（Before/After/Changes 三态 + 两组并排，或 Beta 列）或标准两臂表。
    不适用：纯基线特征表（仅 Before 两列、无 change/β 标记）→ 返回 []。
    """
    if not table or len(table) < 2:
        return []
    header, body = table[0], [r for r in table[1:] if r and any(r)]
    if not body:
        return []

    flat_hdr = " ".join(str(c or "") for c in header).lower()
    flat_body = " ".join(str(c or "") for r in body for c in r).lower()
    is_outcome = bool(_OUTCOME_KW.search(flat_hdr + " " + flat_body))
    is_pure_baseline = _BASELINE_KW.search(flat_hdr) and not is_outcome
    if is_pure_baseline or not is_outcome:
        return []

    n_cols = max((len(r) for r in [header] + body), default=0)
    rows = []
    beta_col = None
    for c in range(n_cols):
        h = _norm(header[c] if c < len(header) else "")
        if re.search(r"beta|coefficient|回归系数|β", h):
            beta_col = c
            break

    parent_label = ""
    for r in body:
        label = ""
        if r and r[0] is not None:
            first = str(r[0]).strip()
            if first and not re.fullmatch(r"[\d.,\s()%±/\-–—−]+", first) \
               and _frac(first) is None:
                label = first
        if label:
            if not re.fullmatch(r"(before|after|changes?|δ|Δ|baseline)",
                                label.strip(), re.IGNORECASE):
                parent_label = label
        else:
            if len(r) > 1 and r[1] is not None:
                sub = str(r[1]).strip()
                if re.fullmatch(r"(before|after|changes?|δ|Δ|baseline)",
                                sub, re.IGNORECASE):
                    label = (parent_label + " " + sub).strip() if parent_label else sub
                elif sub and not re.fullmatch(r"[\d.,\s()%±/\-–—−]+", sub):
                    label = sub
        if not label:
            continue
        if re.fullmatch(r"(male|female|yes|no|former|current)", label.strip(), re.IGNORECASE):
            continue

        # 形态 A：Beta (95% CI) 列 → 直接 MD(95%CI)
        if beta_col is not None and beta_col < len(r) and r[beta_col]:
            m = _CONT_BETA_CI.search(str(r[beta_col]))
            if m:
                beta0 = _f(m.group("beta"))
                lo, hi = _f(m.group("lo")), _f(m.group("hi"))
                if lo < hi and lo <= beta0 <= hi:
                    se = (hi - lo) / 3.92
                    rows.append({
                        "study": label[:50], "measure": "MD",
                        "te": round(beta0, 6), "sete": round(se, 6),
                        "reported": {"est": round(beta0, 4), "ci": [round(lo, 4), round(hi, 4)]},
                        "_meta": {"source": "table", "page": page_no, "table": table_idx + 1,
                                  "template": "T_CONT_BETA",
                                  "raw": {"beta": beta0, "lo": lo, "hi": hi},
                                  "anchor": f"p{page_no} table#{table_idx+1} row '{label[:30]}' (Beta col)"},
                    })
                    continue

        # 形态 B/C：行内两组 mean±SD 对 → MD（或 'x (lo,hi)' 形态）
        pairs = []
        for c in range(1, len(r)):
            for m_, s_ in _cont_pairs(r[c]):
                pairs.append((m_, s_, c))
        pairs = [(m_, s_, c) for m_, s_, c in pairs if s_ > 0]
        row_text = " ".join(str(c_) for c_ in r if c_ is not None).lower()
        is_change_row = ("change" in row_text or "δ" in row_text or "Δ" in row_text
                         or " vs " in row_text or "compared" in row_text
                         or ("post" in row_text and "pre" in row_text))
        if not is_change_row:
            continue
        if _DESCR_KW.search(label) or _DESCR_KW.search(row_text):
            continue
        if len(pairs) >= 2:
            (m1, s1, _), (m2, s2, _) = pairs[0], pairs[1]
            n1 = n2 = None
            group_nums = re.findall(r"\((\d+)\)", " ".join(str(c_) for c_ in r if c_ is not None))
            ints = [int(x) for x in group_nums if int(x) > 5]
            if ints:
                n1 = ints[0]
                n2 = ints[1] if len(ints) >= 2 else n1
            diff = m1 - m2
            se = math.sqrt(s1 ** 2 / n1 + s2 ** 2 / n2) if (n1 and n2) else None
            rows.append({
                "study": label[:50], "measure": "MD",
                "te": round(diff, 6), "sete": round(se, 6) if se else None,
                "reported": {"m1": round(m1, 4), "sd1": round(s1, 4), "n1": n1,
                             "m2": round(m2, 4), "sd2": round(s2, 4), "n2": n2},
                "_meta": {"source": "table", "page": page_no, "table": table_idx + 1,
                          "template": "T_CONT_CHANGE" if is_change_row else "T_CONT_TWOARM",
                          "raw": {"m1": m1, "sd1": s1, "n1": n1, "m2": m2, "sd2": s2, "n2": n2,
                                  "diff": diff, "se": se},
                          "anchor": f"p{page_no} table#{table_idx+1} row '{label[:30]}'"},
            })
        else:
            ci_cells = [c for c in r[1:] if c and _CONT_BETA_CI.search(str(c))]
            bare = [_f(c) for c in r[1:] if c and re.search(_FNUM, str(c))
                    and not _CONT_BETA_CI.search(str(c))]
            if len(ci_cells) >= 2:
                betas = [_f(_CONT_BETA_CI.search(str(c)).group("beta")) for c in ci_cells[:2]]
                m1, m2 = betas[0], betas[1]
                diff = m1 - m2
                se = None
                for cc in ci_cells[:2]:
                    mm = _CONT_BETA_CI.search(str(cc))
                    if mm:
                        lo, hi = _f(mm.group("lo")), _f(mm.group("hi"))
                        se = max(se or 0, (hi - lo) / 3.92)
                rows.append({
                    "study": label[:50], "measure": "MD",
                    "te": round(diff, 6), "sete": round(se, 6) if se else None,
                    "reported": {"m1": round(m1, 4), "m2": round(m2, 4),
                                 "ci_width_se": round(se, 4) if se else None},
                    "_meta": {"source": "table", "page": page_no, "table": table_idx + 1,
                              "template": "T_CONT_CHANGE_CI",
                              "anchor": f"p{page_no} table#{table_idx+1} row '{label[:30]}'"},
                })
    return rows


def narrative_continuous(pages):
    """正文连续型效应量（MD / mean difference (95% CI)）。"""
    out = []
    md_re = EXTRACTION_TEMPLATES["MD"]["re"]
    for p in pages:
        if p["kind"] == "scanned":
            continue
        text = p["text"]
        for m in md_re.finditer(text):
            rec = _effect_from_match("MD", m, p["page"], text)
            if rec:
                out.append(rec)
        for m in re.finditer(
                rf"(?:mean difference|difference in means|weighted mean difference|"
                rf"standardized mean difference|md)\b[^()]{0,80}?\(?\s*"
                rf"(?P<te>{_FNUM})\s*(?:,|;|\(|\[)?\s*(?:95%\s*ci|ci)\s*"
                rf"[\(\[:\s]*\s*(?P<lo>{_FNUM})\s*{_SEP}\s*(?P<hi>{_FNUM})",
                text, re.IGNORECASE):
            try:
                te = _f(m.group("te"))
                lo = _f(m.group("lo"))
                hi = _f(m.group("hi"))
            except (ValueError, AttributeError):
                continue
            if not (lo < hi and lo <= te <= hi):
                continue
            se = (hi - lo) / 3.92
            pre = text[max(0, m.start() - 50):m.start()].strip()
            labs = re.findall(r"[A-Za-z][A-Za-z ]{0,45}", pre)
            study = labs[-1].strip() if labs and " " in labs[-1] else "MD"
            out.append({
                "study": study[-40:], "measure": "MD",
                "te": round(te, 6), "sete": round(se, 6),
                "reported": {"est": round(te, 4), "ci": [round(lo, 4), round(hi, 4)]},
                "_meta": {"source": "narrative", "page": p["page"],
                          "template": "T_MD_CI",
                          "anchor": f"p{p['page']} text: …{text[max(0,m.start()-50):m.end()+20].replace(chr(10),' ').strip()[:80]}…"},
            })
    return out


# ---------------------------------------------------------------------------
# ②B 正文叙述模板（正则候选，零幻觉）
# ---------------------------------------------------------------------------

_N_DICHOT = re.compile(
    r"(?P<a>\d+)\s*/\s*(?P<b>\d+)\s*(?:\((?P<pct>[\d.]+)\s*%?\))?")
_MD_CI = re.compile(
    r"(?:mean difference|difference in means|均差|md)\D{0,80}?(-?\d+\.?\d*)\s*"
    r"(?:\(?\s*95\s*%?\s*ci|\[)\s*(-?\d+\.?\d*)\s*(?:to|,|—|–|~)\s*(-?\d+\.?\d*)",
    re.IGNORECASE)
_OR_CI = re.compile(
    r"(?:odds ratio|or)\D{0,40}?(\d+\.?\d*)\s*(?:\(?\s*95\s*%?\s*ci|\[)\s*"
    r"(\d+\.?\d*)\s*(?:to|,|—|–|~)\s*(\d+\.?\d*)", re.IGNORECASE)


def narrative_candidates(pages):
    """扫描正文，返回候选片段列表（全部 needs_review，除与表格互证通过者）。

    每个候选：{kind, page, snippet, payload}。不做臂方向推断——四格计数候选只给
    原文片段，由人工（或上下文 LLM，P2）指认实验/对照组。
    """
    out = []
    for p in pages:
        if p["kind"] == "scanned":
            continue
        for m in _N_DICHOT.finditer(p["text"]):
            a, b = int(m.group("a")), int(m.group("b"))
            if a <= b <= 100000 and b >= 10:
                s = max(0, m.start() - 90)
                out.append({"kind": "dichot_counts", "page": p["page"],
                            "snippet": p["text"][s:m.end() + 60].replace("\n", " "),
                            "payload": {"events": a, "total": b}})
        for m in _MD_CI.finditer(p["text"]):
            s = max(0, m.start() - 90)
            out.append({"kind": "md_ci", "page": p["page"],
                        "snippet": p["text"][s:m.end() + 40].replace("\n", " "),
                        "payload": {"te": float(m.group(1)),
                                    "ci": [float(m.group(2)), float(m.group(3))]}})
        for m in _OR_CI.finditer(p["text"]):
            s = max(0, m.start() - 90)
            out.append({"kind": "or_ci", "page": p["page"],
                        "snippet": p["text"][s:m.end() + 40].replace("\n", " "),
                        "payload": {"te": float(m.group(1)),
                                    "ci": [float(m.group(2)), float(m.group(3))]}})
    return out


# ---------------------------------------------------------------------------
# ②C occurred-in 叙述句模板（规律 R4，FIGARO-DKD 实证）
# ---------------------------------------------------------------------------
# NEJM 系惯用句："A primary outcome event occurred in 458 of 3686 patients
# (12.4%) in the finerenone group and in 519 of 3666 (14.2%) in the placebo
# group (hazard ratio, 0.87; 95% CI, 0.76–0.98; P = 0.03)."
# 要点：① 第二臂可省略 'patients'；② 结尾须兼容 '; P = 0.03)'；
#      ③ HR 括号段可选（无则仍产出纯 2×2 行，交人工补效应量）。

_OCCURRED_RE = re.compile(
    rf"(?:occurred\s+in|occurred\s+in)\s+"
    rf"(?P<a>\d[\d,]*)\s+of\s+(?P<na>\d[\d,]*)\s+(?:patients?|participants?|subjects?)\s*"
    rf"\((?P<pcta>[\d.]+)\s*%\)\s*(?:in\s+)?(?:the\s+)?(?P<arma>[^,()]+?)\s+group\s+"
    rf"and\s+(?:in\s+)?(?P<c>\d[\d,]*)\s+of\s+(?P<nc>\d[\d,]*)\s*"
    rf"(?:(?:patients?|participants?|subjects?)\s*)?\((?P<pctc>[\d.]+)\s*%\)\s*"
    rf"(?:in\s+)?(?:the\s+)?(?P<armb>[^,()]+?)\s+group\s*"
    rf"(?:\(\s*(?:hazard ratio|odds ratio|risk ratio)\s*,\s*"
    rf"(?P<te>{_FNUM})\s*;\s*95\s*%\s*(?:confidence\s+interval\s*(?:\[ci\])?|ci)\s*,\s*"
    rf"(?P<lo>{_FNUM})\s*{_SEP}\s*(?P<hi>{_FNUM})"
    rf"(?:\s*;\s*p\s*[<=]\s*[\d.]+\s*)?\)\s*)?",
    re.IGNORECASE)

# 结局标签：命中前的「… outcome」短语（'A primary outcome event occurred in…'）
_OUTCOME_LABEL_RE = re.compile(
    r"([A-Za-z][A-Za-z\-/ ]{2,60}?(?:composite\s+)?outcome)\s+(?:event|occurred)",
    re.IGNORECASE)


def narrative_occurred_in(pages):
    """扫正文 occurred-in 句式 → 2×2 四格行（含可选报告 HR/OR 供勾稽）。

    全部标 needs_review（单源叙述）；若同文表格给出同计数则由 ③ 跨源互证升级。
    """
    out = []
    for p in pages:
        if p["kind"] == "scanned":
            continue
        text = p["text"]
        for m in _OCCURRED_RE.finditer(text):
            try:
                a = int(m.group("a").replace(",", ""))
                na = int(m.group("na").replace(",", ""))
                c = int(m.group("c").replace(",", ""))
                nc = int(m.group("nc").replace(",", ""))
            except ValueError:
                continue
            if not (0 <= a <= na <= 200000 and 0 <= c <= nc <= 200000
                    and min(na, nc) >= 10):
                continue
            lm = _OUTCOME_LABEL_RE.search(text[max(0, m.start() - 200):m.start()])
            label = lm.group(1).strip() if lm else "outcome"
            label = re.sub(r"^(a|an|the)\s+", "", label, flags=re.I)[-60:]
            rec = {
                "study": label,
                "ai": a, "bi": na - a,      # 实验臂（第一臂）
                "ci": c, "di": nc - c,      # 对照臂（第二臂）
                "_meta": {"source": "narrative", "page": p["page"],
                          "template": "T_OCCURRED_IN",
                          "arms": [m.group("arma").strip(), m.group("armb").strip()],
                          "anchor": f"p{p['page']} text: …{text[max(0,m.start()-80):m.end()+20].replace(chr(10),' ').strip()[:90]}…"},
            }
            if m.group("te"):
                try:
                    te0 = float(m.group("te").replace(",", ""))
                    lo = float(m.group("lo").replace(",", ""))
                    hi = float(m.group("hi").replace(",", ""))
                except ValueError:
                    te0 = None
                if te0 and lo > 0 and hi > lo and lo <= te0 <= hi:
                    rec["measure"] = "HR"
                    rec["te"] = round(math.log(te0), 6)
                    rec["sete"] = round((math.log(hi) - math.log(lo)) / 3.92, 6)
                    rec["reported"] = {"est": round(te0, 4), "ci": [round(lo, 4), round(hi, 4)]}
            out.append(rec)
    return out


# ---------------------------------------------------------------------------
# ③ 一致性校验（纯代码，零幻觉）
# ---------------------------------------------------------------------------

def _ln(v):
    return math.log(v) if v > 0 else None


def check_dichot(row, reported_or=None, reported_ci=None):
    """四格表校验。返回 (ok: bool, checks: [str], recomputed: {or, ci})。

    - events ≤ total 两臂；ai+ci ≥ 1（避免 OR=0/∞ 崩溃交人工）；
    - 重算 OR 与报告值比对（相对误差 ≤1%）；
    - CI 由 Woolf 公式重算并与报告 CI 比对（≤2%）。
    """
    checks = []
    a, b_, c, d = row["ai"], row["bi"], row["ci"], row["di"]
    nt, nc = a + b_, c + d
    if not (0 <= a <= nt and 0 <= c <= nc):
        return False, ["events>total：事件数超过组总数"], None
    if nt == 0 or nc == 0:
        return False, ["zero-total：某组总数为 0"], None
    if min(a, b_, c, d) == 0:
        checks.append("zero-cell：存在零格，OR 重算需连续性校正（交人工确认）")
        return False, checks, None
    orn = (a * d) / (b_ * c)
    se = math.sqrt(1 / a + 1 / b_ + 1 / c + 1 / d)
    lo, hi = orn * math.exp(-1.96 * se), orn * math.exp(1.96 * se)
    if reported_or is not None:
        rel = abs(_ln(orn) - _ln(reported_or)) / max(abs(_ln(reported_or)), 1e-12)
        if rel > 0.01:
            return False, [f"or-mismatch：重算 lnOR={math.log(orn):.4f} vs 报告 "
                           f"{math.log(reported_or):.4f}（>{1}%）"], None
        checks.append("or-recompute-pass")
    if reported_ci is not None:
        if abs(lo - reported_ci[0]) / max(abs(reported_ci[0]), 1e-12) > 0.02 or \
           abs(hi - reported_ci[1]) / max(abs(reported_ci[1]), 1e-12) > 0.02:
            # CI 不匹配仍返回 rec：te/se 可由原始计数重算供人工参考，置信度单独降级
            return False, ["ci-mismatch：重算 95%CI 与报告值偏差 >2%"], \
                {"or": round(orn, 4), "ci": [round(lo, 4), round(hi, 4)]}
        checks.append("ci-recompute-pass")
    checks.append("counts-consistent")
    return True, checks, {"or": round(orn, 4),
                          "ci": [round(lo, 4), round(hi, 4)]}


def check_te_sete(te, sete, ci=None):
    """te/sete ↔ 95%CI 互推校验（Woolf：ci = te ± 1.96·sete）。"""
    checks = []
    if sete <= 0:
        return False, ["sete<=0"], None
    lo, hi = te - 1.96 * sete, te + 1.96 * sete
    if ci is not None:
        # CI 应近似对称于 te
        d_lo, d_hi = abs(te - ci[0]), abs(ci[1] - te)
        if d_lo == 0 or d_hi == 0:
            return False, ["ci-degenerate"], None
        if max(d_lo, d_hi) / min(d_lo, d_hi) > 1.25:
            # 阈值 1.25：报告值四舍五入会使 ln 空间轻微不对称（实测 ≤1.12），
            # 真正取错数值（如把不同 HR 拼接）比值远超此界（实测 4.6）
            return False, ["ci-asymmetric：CI 关于 te 明显不对称，疑似取错数值"], None
        w_re, w_rep = 3.92 * sete, (ci[1] - ci[0])
        if abs(w_re - w_rep) / max(w_rep, 1e-12) > 0.05:
            return False, [f"ci-width-mismatch：sete 推得宽度 {w_re:.4f} vs 报告 {w_rep:.4f}"], None
        checks.append("ci-recompute-pass")
    checks.append("te-sete-consistent")
    return True, checks, {"ci": [round(lo, 4), round(hi, 4)]}


# ---------------------------------------------------------------------------
# ④ 置信路由 + ⑤ 组装 A4 行
# ---------------------------------------------------------------------------

def extract(pdf_path, study_id=None, reported_summary=None):
    """主入口。返回 {rows, candidates, n_pages, review_summary}。

    rows：可直接喂 fullflow A4 extraction_table / b1 的字典列表：
      - 四格表行：{study, ai, bi, ci, di, te, sete, _review{...}}
      - 连续行：{study, te, sete, _review{...}}
    candidates：正文候选（均 needs_review）。
    reported_summary: 可选 {study_label: {"or": x, "ci": [lo, hi]}}，来自正文
      or_ci 候选——用于表格↔正文互证；未提供时四格表行只做结构勾稽。

    表格抓取按「通用 → 专用」逐页降级：T1 有框表（pdfplumber lines）→
    T2 无框表重建（PyMuPDF word 坐标）→ 叙述文本通道（独立，不降级）。
    页级命中即停（_review.tier/_review.method 可审计）；确实无法解析的页
    如实列入 review_summary.unresolved（不硬造、不误抓）。
    """
    reported_summary = reported_summary or {}
    pdf_path = _norm_path(pdf_path)

    # ── 类型甄别：**仅作标注，不再是抽取前置门**（2026-09-10 规则变更）──
    # 规则：人工（A3 裁决表）确认文献类型后，下层一律不再做类型判断；
    # 需要改类型只能由人工确认、或人工主动发起。故此处保留 classify_pdf 的分类
    # 结果作**提示**（review_summary.type_notice），但绝不短路抽取——否则与人工
    # 裁决打架，并会引出 _skip_page_screen 之类的豁免补丁（已删除）。
    # 历史：规律 R1 曾对 review/guideline/protocol 直接排除（KDIGO/ESC 实证各被
    # 误抽 85–104 行垃圾）。该风险现改由 🔴 人工闸位 + review_note 提示承担。
    # 探测失败（如缺 PyMuPDF）不得阻断抽取 → 降级为 unknown。
    try:
        cls = classify_pdf(pdf_path)
    except Exception as e:  # noqa: BLE001
        cls = {"type": "unknown", "confidence": 0.0, "declared": "",
               "signals": [f"classify-fail: {type(e).__name__}: {e}"], "n_pages": 0}
    doc_type = cls["type"]
    _TYPE_CN = {"review": "综述", "guideline": "指南/共识/声明",
                "protocol": "研究方案（protocol，无结果数据）"}

    doc = parse_pdf(pdf_path)
    rows, candidates = [], []

    def _run_templates(tab, page_no, ti):
        return (t_dichot(tab, page_no, ti)
                + t_continuous(tab, page_no, ti)
                + t_effect_table(tab, page_no, ti)
                + t_cont_table(tab, page_no, ti)
                + t_forest_table(tab, page_no, ti)
                + t_meta_table(tab, page_no, ti))

    # 逐页逐层降级：命中该页即停；全层失败 → unresolved 如实记录
    tier_report, unresolved = {}, []
    for p in doc["pages"]:
        if p["kind"] == "scanned":
            unresolved.append({"page": p["page"], "reason": "scanned",
                               "note": "扫描页无文本层，P1 不支持 OCR，需人工/OCR 处理"})
            tier_report[p["page"]] = {"tiers": [], "n_rows": 0}
            continue
        page_rows, tiers_tried = [], []
        for tier in p.get("table_tiers", []):
            trs = []
            for ti, tab in enumerate(tier["tables"]):
                for r in _run_templates(tab, p["page"], ti):
                    meta = r.get("_meta")
                    if isinstance(meta, dict):
                        meta["tier"] = tier["tier"]
                        meta["method"] = tier["method"]
                    trs.append(r)
            tiers_tried.append({"tier": tier["tier"], "method": tier["method"],
                                "n_tables": len(tier["tables"]),
                                "n_rows": len(trs)})
            if trs:  # 该页在此层命中 → 采用，不再降级
                page_rows = trs
                break
        tier_report[p["page"]] = {"tiers": tiers_tried, "n_rows": len(page_rows)}
        if page_rows:
            rows.extend(page_rows)
        elif tiers_tried:
            # 检出了表格结构但所有模板层都不命中 → 如实上报（不硬造）
            has_table_title = bool(re.search(
                r"Table\s+\d+", p.get("text") or "", re.IGNORECASE))
            unresolved.append({
                "page": p["page"], "reason": "all-tiers-no-template-hit",
                "note": ("页面检出表格且含 Table 标题，但无模板命中"
                         "（表结构非标准，建议人工录入）" if has_table_title
                         else "页面检出表格结构但无模板命中（非效应量表或版式未覆盖）"),
                "tiers": tiers_tried})
        # 无表格候选的纯正文页不属失败：叙述通道仍会扫其文本

    # 叙述效应量（HR/OR/RR/MD/P）→ 直接成行（已回填 te/sete）
    effects = narrative_effects(doc["pages"])
    rows.extend([e for e in effects if e.get("measure") != "P"])
    rows.extend(narrative_continuous(doc["pages"]))
    # 规律 R4：occurred-in 句式 → 2×2 四格行（FIGARO 等叙述句报告主结局）
    rows.extend(narrative_occurred_in(doc["pages"]))
    # 候选：① p 值（measure='P'，供显著性参考）；② 正文/表中「事件/总数」计数提及
    # （narrative_candidates，零幻觉，全部 needs_review，供人工判断是否为可入 2×2 的计数）
    # —— 之前 narrative_candidates 定义后从未被调用，导致综述类文献下载后界面一片空白。
    ncs = narrative_candidates(doc["pages"])
    candidates = [e for e in effects if e.get("measure") == "P"]
    candidates.extend(ncs)

    # 校验 + 置信路由
    review = []
    for r in rows:
        meta = r.pop("_meta", {})
        checks, conf = [], None
        if {"ai", "bi", "ci", "di"}.issubset(r):
            ok, checks, rec = check_dichot(r)
            if rec:
                # 重算值仅在行缺 te/sete 时回填，不覆盖表格自带的报告值
                # （sete 全模块统一 Woolf 约定：(lnhi-lnlo)/3.92 = se(lnOR)）
                r["te"] = r.get("te") or (round(math.log(rec["or"]), 4)
                                          if rec["or"] > 0 else None)
                r["sete"] = r.get("sete") or round(
                    (math.log(rec["ci"][1]) - math.log(rec["ci"][0])) / 3.92, 4)
            # 双源命中（森林表 2×2 计数列 + 相邻 HR 列）→ verified；其余 needs_review
            is_forest = "T_EFFECT_TABLE" in meta.get("template", "") and \
                {"ai", "bi", "ci", "di", "te"}.issubset(r)
            conf = ("verified" if (ok and is_forest) else
                    "needs_review" if ok else "failed")
        elif "sete" in r and r.get("te") is not None:
            if r.get("sete") is None:
                # 连续型 MD 缺 n → 无法算 SE，数据不完整，待人工补 n
                checks, conf = ["missing-n: SE not computable"], "needs_review"
            else:
                # check_te_sete 的 ci 需与 te 同尺度：HR/OR/RR 的 te 为 ln 值，
                # reported.ci 是原始尺度 → 先取 ln 再校验；MD 的 te 本就是原值
                rep_ci = (r.get("reported") or {}).get("ci")
                if rep_ci is not None and r.get("measure") in (
                        "HR", "OR", "RR", "HR/OR/RR") and min(rep_ci) > 0:
                    rep_ci = [math.log(rep_ci[0]), math.log(rep_ci[1])]
                ok, checks, rec = check_te_sete(r["te"], r["sete"], ci=rep_ci)
                # 效应量(CI)/连续型表格行：单源，预填 te/sete 但标 needs_review
                # （报告数字逐字取自 PDF + 确定变换，人工一键确认即可进 Block B）
                conf = "needs_review" if ok else "failed"
        else:
            ok, checks, conf = False, ["no-template"], "failed"
        r["_review"] = {"confidence": conf, "checks": checks, **meta}
        review.append({"study": r.get("study"), "measure": r.get("measure"),
                       "confidence": conf, "anchor": meta.get("anchor"),
                       "checks": checks})

    # 正文候选全部列为 needs_review 项（供审核台逐条处理）
    for cand in candidates:
        meta = cand.get("_meta") or {}
        if cand.get("kind") == "pvalue":
            review.append({"kind": "pvalue", "confidence": "needs_review",
                           "page": meta.get("page"), "reported": cand.get("reported"),
                           "anchor": meta.get("anchor")})
        else:
            review.append({"kind": cand.get("kind", "candidate"),
                           "confidence": "needs_review", "page": cand.get("page"),
                           "snippet": cand.get("snippet"),
                           "payload": cand.get("payload")})

    n_v = sum(1 for x in review if x.get("confidence") == "verified")
    n_r = sum(1 for x in review if x.get("confidence") == "needs_review")
    return {"rows": rows, "candidates": candidates,
            "n_pages": doc["n_pages"],
            "doc_type": doc_type, "doc_type_confidence": cls["confidence"],
            "review_summary": {
                "n_rows": len(rows), "verified": n_v, "needs_review": n_r,
                # 类型仅作标注：excluded 恒 False（键位保留以兼容旧消费点）
                "excluded": False,
                "doc_type": doc_type,
                "doc_type_confidence": cls["confidence"],
                "signals": cls.get("signals") or [],
                "type_notice": (("疑似%s（置信 %s）——本类文献通常不含原始 2×2 表，"
                                 "抽取为 0 行属正常；是否保留由人工在闸位确认"
                                 % (_TYPE_CN[doc_type], cls["confidence"]))
                                if doc_type in _TYPE_CN else None),
                "tier_report": tier_report,
                "unresolved": unresolved,
                "note": "verified 行仍建议抽检；needs_review 行必须人工确认后"
                        "经 extraction_guard stamp --confirm 方可进 Block B。"
                        "unresolved 页为多级降级后仍无法解析者，如实上报待人工"
                        "（scanned=需 OCR；all-tiers-no-template-hit=表结构"
                        "非标准/版式未覆盖），不硬造、不误抓"}}


def to_a4_rows(result, study_prefix="S"):
    """提取结果 → fullflow A4 extraction_table 兼容行。

    兼容原行为：剥掉 _ 前缀内部字段。但**保留**可溯源的公开元数据
    （source_page / anchor / confidence / measure / arm），供工作台「逐篇文档展示」
    把抽取值与原文页码锚点对应起来（pdf_extractor v0.1.1 起）。
    """
    out = []
    for i, r in enumerate(result.get("rows", []), 1):
        row = {k: v for k, v in r.items() if not k.startswith("_") and v is not None}
        # 从 _review 提升溯源字段（原名 page 易与 row 内字段冲突 → 改名 source_page）
        rev = r.get("_review") or {}
        if "source_page" not in row and rev.get("page") is not None:
            row["source_page"] = rev["page"]
        if "anchor" not in row and rev.get("anchor"):
            row["anchor"] = rev["anchor"]
        if "confidence" not in row and rev.get("confidence"):
            row["confidence"] = rev["confidence"]
        row["study"] = row.get("study") or f"{study_prefix}{i}"
        out.append(row)
    return out


def extract_sections(pdf_path, max_chars_per_section=6000):
    """从 PDF 按章节切片文本（用于 C 档写作参考，非数据抽取）。

    返回 {abstract, introduction, methods, results, discussion, conclusion, other}
    每个字段为该章节的全文切片（截到 max_chars_per_section）。

    策略：纯 fitz 文本 + 正则锚点分节，不依赖表格/布局检测。
    章节标题允许编号前缀（"1 Introduction"、"2. Methods"、"RESULTS" 等）。
    若 PDF 无明确章节锚点 → 全部进 'other'。
    """
    import fitz as _fitz
    import re as _re
    pdf_path = _norm_path(pdf_path)
    if not os.path.isfile(pdf_path):
        return {}

    try:
        with _fitz.open(pdf_path) as doc:
            pages = [p.get_text() or "" for p in doc]
    except Exception:
        return {}

    if not pages:
        return {}

    full_text = "\f".join(pages)

    _SECTION_PATTERNS = [
        ("abstract",      r"(?:^|\n|\f)(?:[ \t]*\d+\.?[ \t]+)?(?:abstract|summary|executive\s+summary|opinion\s+statement)\b"),
        ("introduction",  r"(?:^|\n|\f)(?:[ \t]*\d+\.?[ \t]+)?(?:introduction|background|rationale)\b"),
        ("methods",       r"(?:^|\n|\f)(?:[ \t]*\d+\.?[ \t]+)?(?:methods?|methodology|materials?\s+and\s+methods?|study\s+design|search\s+strategy)\b"),
        ("results",       r"(?:^|\n|\f)(?:[ \t]*\d+\.?[ \t]+)?(?:results?|\bfindings\b(?!\s+(?:in|of|from|that|are|were|suggest|show|indicate|reveal|demonstrate|confirm))|outcomes\b(?!\s+(?:for|of|in|and|were|was|are|is|data))|analysis)\b"),
        ("discussion",    r"(?:^|\n|\f)(?:[ \t]*\d+\.?[ \t]+)?(?:discussion\b(?!\s+(?:and|of|section))|commentary|interpretation)\b"),
        ("conclusion",    r"(?:^|\n|\f)(?:[ \t]*\d+\.?[ \t]+)?(?:conclusions?|concluding|summary\s+and\s+conclusion|implications?\s+of)\b"),
    ]

    lower = full_text.lower()
    anchors = []
    for key, pat in _SECTION_PATTERNS:
        for m in _re.finditer(pat, lower, _re.MULTILINE):
            anchors.append((m.start(), key))
            break
    anchors.sort(key=lambda x: x[0])

    out = {k: "" for k, _ in _SECTION_PATTERNS}
    out["other"] = ""

    if not anchors:
        out["other"] = full_text[:max_chars_per_section * 3]
        return out

    for i, (start, key) in enumerate(anchors):
        end = anchors[i + 1][0] if i + 1 < len(anchors) else len(full_text)
        chunk = full_text[start:end].strip()
        if len(chunk) > max_chars_per_section:
            trunc = chunk[:max_chars_per_section]
            last_para = trunc.rfind("\n\n")
            if last_para > int(max_chars_per_section * 0.7):
                chunk = trunc[:last_para]
            else:
                chunk = trunc
        out[key] = chunk

    pre = full_text[:anchors[0][0]].strip()
    if pre:
        out["other"] = (pre[:max_chars_per_section] +
                        (("\n\n" + out["other"]) if out["other"] else ""))

    return out


if __name__ == "__main__":  # 供 CLI 冒烟：python pdf_extractor.py <pdf>
    import sys
    if len(sys.argv) > 2 and sys.argv[1] == "--sections":
        secs = extract_sections(sys.argv[2])
        print(json.dumps({k: (v[:200] + "..." if len(v) > 200 else v)
                          for k, v in secs.items() if v},
                         ensure_ascii=False, indent=2))
    else:
        res = extract(sys.argv[1])
        print(json.dumps(res["review_summary"], ensure_ascii=False, indent=2))
        for r in res["rows"]:
            print(json.dumps({k: r[k] for k in r if k != "_review"},
                             ensure_ascii=False))
