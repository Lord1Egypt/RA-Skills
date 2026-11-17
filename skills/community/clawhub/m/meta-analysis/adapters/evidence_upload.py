"""C1 自备文献上传：把用户自己收集 / 改过的文献清单或 PDF 打包，解析成 C1 接地证据集。

WHY（2026-09-22 用户要求）：
    此前 C1 的证据只能来自两个地方 —— ① 上游 A2 文献集；② Europe PMC 自动检索
    （见 literature_probe.search_evidence）。但真实写稿场景里，作者手上往往已经有
    **自己筛过 / 改过的清单**（Excel 裁决表、Zotero/EndNote 导出的 RIS，或一堆
    下载好的 PDF 全文）。这些是最权威的证据集，却没有任何入口能喂进 C1 ——
    用户只能眼看着初稿引用检索来的（可能不相关的）文献。

本模块只做一件事：把用户上传的文件**归一成与 search_evidence() 同构的 evidence
dict**（primary / synthesis / hit_count / database / ...），于是 block_c 无需区分
来源即可消费。字段一律是**文件里真实写着的书目事实**，不做任何补全或推测：
    文件没写作者 → authors 为空（正文按 Anonymous 处理），绝不臆造。

支持格式：
    - 表格清单：.xlsx / .xls / .csv / .tsv（中英文列名均可，含表头自动识别）
    - 文献管理器导出：.ris / .bib
    - PDF 打包：.zip（内含 PDF / RIS / 表格）或直接上传多个 .pdf
      → 逐份抽标题/DOI/年份（复用 block_a 的 PDF 元数据抽取，仅书目事实）
"""

from __future__ import annotations

import datetime
import os
import re
import tempfile
import unicodedata
import zipfile

# ---------------------------------------------------------------------------
# 常量
# ---------------------------------------------------------------------------

#: 表格列名别名（小写、去空白后比较）。左为归一字段，右为可识别的表头写法。
#: 顺序敏感：`_pick` 取第一个命中的别名，故「文献类型确认」必须排在宽泛的
#: "type" 之前，否则会被更宽的模式抢走。
COLUMN_ALIASES = {
    "title": ["title", "article title", "article", "题名", "标题", "文献标题",
              "论文标题", "论文题目", "研究标题", "题目", "文献", "文章标题"],
    "authors": ["authors", "author", "authorstring", "author string", "first author",
                "作者", "第一作者", "全部作者", "作者列表"],
    "year": ["year", "publication year", "pub year", "pubyear", "published",
             "年份", "发表年份", "出版年", "年"],
    "journal": ["journal", "journal name", "source", "publication", "publication name",
                "venue", "期刊", "刊名", "期刊名", "杂志", "来源", "来源期刊"],
    "doi": ["doi", "digital object identifier", "doi/ pmid", "doi/pmid", "doi号"],
    "pmid": ["pmid", "pubmed id", "pubmedid", "pubmed"],
    "study_type": ["文献类型确认", "研究类型", "文献类型", "研究设计", "设计",
                   "study type", "study design", "design", "document type",
                   "publication type", "type"],
    "abstract": ["abstract", "summary", "摘要", "内容摘要"],
    "cited_by": ["cited by", "citations", "citation count", "被引", "被引次数", "引用次数"],
    "url": ["url", "link", "链接", "网址"],
}

#: 支持的扩展名（小写）。zip 会递归处理内部文件。
TABLE_EXT = (".xlsx", ".xls", ".csv", ".tsv")
REFLIST_EXT = (".ris", ".bib", ".txt")
PDF_EXT = (".pdf",)
BUNDLE_EXT = (".zip",)

#: 安全上限：避免一次上传把内存/磁盘吃满（zip 炸弹或超大打包）。
MAX_FILES = 500
MAX_PDFS = 300
MAX_ZIP_BYTES = 400 * 1024 * 1024        # 解压后总字节上限
MAX_TEXT_BYTES = 8 * 1024 * 1024         # 单个文本/RIS/Bib 文件上限

#: 设计类型归一表（顺序敏感：先长后短，先具体后宽泛）。
_TYPE_RULES = [
    ("meta-analys", "meta-analysis"),
    ("meta analys", "meta-analysis"),
    ("metaanalys", "meta-analysis"),
    ("systematic review", "systematic review"),
    ("systematic literature", "systematic review"),
    ("randomi", "randomized controlled trial"),
    ("randomis", "randomized controlled trial"),
    ("rct", "randomized controlled trial"),
    ("controlled trial", "clinical trial"),
    ("clinical trial", "clinical trial"),
    ("cohort", "observational study"),
    ("case-control", "observational study"),
    ("case control", "observational study"),
    ("cross-sectional", "observational study"),
    ("cross sectional", "observational study"),
    ("observational", "observational study"),
    ("guideline", "guideline"),
    ("consensus", "guideline"),
    ("protocol", "protocol"),
    ("scoping review", "review"),
    ("narrative review", "review"),
    ("literature review", "review"),
    ("review", "review"),
]

#: 归入 synthesis 层的类型（其余进 primary）。判据：这篇文章本身是「已知证据
#: 的汇总」还是「一份新证据」。与 literature_probe 的两层语义保持一致。
_SYNTH_TYPES = {"meta-analysis", "systematic review", "review", "guideline"}

#: 标题里出现这些词但类型列缺失时用于兜底判型（保守：只认最明确的写法）。
_TITLE_TYPE_HINTS = [
    ("meta-analysis", "meta-analysis"),
    ("meta analysis", "meta-analysis"),
    ("systematic review", "systematic review"),
    ("randomized trial", "randomized controlled trial"),
    ("randomised trial", "randomized controlled trial"),
]


class EvidenceUploadError(ValueError):
    """上传内容无法解析成文献清单（提示文案直接面向用户）。"""


# ---------------------------------------------------------------------------
# 归一化工具
# ---------------------------------------------------------------------------

def _today():
    return datetime.date.today().isoformat()


def _norm_key(s):
    """表头归一：去空白/不可见字符 + 小写 + 全角转半角。"""
    s = unicodedata.normalize("NFKC", str(s or ""))
    return re.sub(r"[\s\u3000_\-/]+", " ", s).strip().lower()


def norm_title(s):
    """标题归一（去空格/标点/大小写），用于去重与匹配。"""
    s = unicodedata.normalize("NFKC", str(s or "")).lower()
    return re.sub(r"[^a-z0-9\u4e00-\u9fff]+", "", s)


def norm_doi(s):
    """DOI 归一：去掉协议前缀与尾部标点，小写。"""
    s = str(s or "").strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    return s.strip(" .;,)").strip()


def _clean_cell(v):
    """单元格 → 干净字符串（float 年份 '2021.0' → '2021'；缺失值 → ''）。

    ⚠️ 必须挡住 pandas 的缺失值： 读表时空格仍是 NaN，而 str(NaN)
    是字符串 "nan" —— 一旦进标题列，参考文献里就会出现一条标题叫 "nan" 的
    条目（单测实测踩到过）。None / NaN / NaT / pd.NA 一律归空串。
    """
    if v is None:
        return ""
    try:
        if v != v:              # NaN 自身不相等（pd.NA 在这里抛 TypeError → 走 except）
            return ""
    except Exception:  # noqa: BLE001
        pass
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    s = unicodedata.normalize("NFKC", str(v))
    if s.strip().lower() in ("nan", "nat", "none", "null", "<na>", "<nat>"):
        return ""
    s = s.replace("\r", " ").replace("\n", " ").replace("\t", " ")
    return re.sub(r"\s{2,}", " ", s).strip()


def parse_year(v):
    """从任意单元格抽出 4 位年份（1900–2099），抽不到返回 None。"""
    s = _clean_cell(v)
    if not s:
        return None
    m = re.search(r"(1[89]\d{2}|20\d{2})", s)
    if not m:
        return None
    y = int(m.group(1))
    return y if 1900 <= y <= 2099 else None


def parse_int(v):
    """从任意单元格抽出整数（'1,204 次' → 1204），抽不到返回 None。"""
    s = re.sub(r"[^\d]", "", _clean_cell(v))
    return int(s) if s else None


def norm_study_type(raw, title=""):
    """把任意写法（'Meta-Analysis' / '随机对照试验' / 'RCT'）归一到短设计标签。

    识别不出来时返回 "study"（而不是猜）—— block_c 只用它做描述性统计，
    猜错比留白更糟。
    """
    s = _norm_key(raw)
    if s:
        # 中文写法先过一遍映射
        zh = {"meta分析": "meta-analysis", "荟萃分析": "meta-analysis",
              "系统评价": "systematic review", "系统综述": "systematic review",
              "随机对照": "randomized controlled trial", "随机化": "randomized controlled trial",
              "队列": "observational study", "观察性": "observational study",
              "病例对照": "observational study", "横断面": "observational study",
              "指南": "guideline", "共识": "guideline", "综述": "review",
              "临床试验": "clinical trial", "方案": "protocol"}
        for k, v in zh.items():
            if k in s:
                return v
        for pat, label in _TYPE_RULES:
            if pat in s:
                return label
    t = _norm_key(title)
    if t:
        for pat, label in _TITLE_TYPE_HINTS:
            if pat in t:
                return label
    return "study"


def _split_authors(raw):
    """作者串 → [{"family": ..., "initials": ...}]（尽力而为，只取姓氏+缩写）。

    兼容四种常见写法（用户自备表格里都能遇到）：
        "Smith J, Doe A"        → Europe PMC 风格
        "Smith J; Doe A"        → 分号分隔
        "John Smith; Jane Doe"  → 名前姓后
        "Smith, John"           → 逗号分隔的姓,名
    """
    s = _clean_cell(raw)
    if not s:
        return []
    # 先按 ; 或 ｜ 切；没有分号时按 ", " 切（但 "Smith, John" 这种姓,名会被切开，
    # 由下面的 token 级启发式再拼回来）。
    chunks = re.split(r"\s*[;；|]\s*", s) if re.search(r"[;；|]", s) else re.split(r"\s*,\s*", s)
    out = []
    for ch in chunks:
        ch = ch.strip().strip(".").strip()
        if not ch or len(ch) < 2:
            continue
        # "etal"/"et al" 之类的占位直接丢
        if _norm_key(ch) in ("etal", "et al", "others", "and others"):
            continue
        out.append(_author_token(ch))
    return [a for a in out if a]


def _bib_author(tok):
    """BibTeX 作者 token → 结构化作者。支持 "Smith, John"（姓,名）与 "John Smith"。"""
    tok = str(tok or "").strip().strip("{}").strip()
    if not tok:
        return {}
    if "," in tok:
        fam, _, given = tok.partition(",")
        fam = fam.strip()
        ini = "".join(w[0] for w in re.split(r"\s+", given.strip()) if w)[:8].upper()
        out = {"family": fam or tok}
        if ini:
            out["initials"] = ini
        return out
    return _author_token(tok)


def _author_token(tok):
    """单个作者 token → {"family": ..., "initials": ...}。"""
    parts = [p for p in re.split(r"\s+", tok) if p]
    if len(parts) == 1:
        return {"family": parts[0].strip(".")}
    # 从后往前找第一个「缩写」token（全大写且长度 ≤3，可带点）
    ini_idx = None
    for i in range(len(parts) - 1, 0, -1):
        p = parts[i].strip(".")
        if p and len(p) <= 3 and p.isupper() and p.isalpha():
            ini_idx = i
            break
    if ini_idx is not None:
        # "van der Berg J" → family "van der Berg"；"Smith J" → "Smith"
        fam = " ".join(parts[:ini_idx]).strip(".")
        ini = "".join(p.strip(".") for p in parts[ini_idx:])[:8]
        return {"family": fam or parts[0], "initials": ini} if ini else {"family": fam or parts[0]}
    # 无缩写 token → 假定「名 姓」，姓氏取最后一个词
    return {"family": parts[-1].strip(".")}


def _split_authors_dupdrop(authors):
    """去重（同一人重复出现）并去掉空姓氏。"""
    seen, out = set(), []
    for a in authors or []:
        f = str((a or {}).get("family") or "").strip()
        if not f:
            continue
        k = f.lower()
        if k in seen:
            continue
        seen.add(k)
        out.append(a)
    return out


# ---------------------------------------------------------------------------
# 表格清单解析（xlsx / xls / csv / tsv）
# ---------------------------------------------------------------------------

def _read_table(path):
    """读成 (表头列表, 行 dict 列表)。优先 pandas，缺失则退到标准库 csv。"""
    low = str(path).lower()
    try:
        import pandas as pd
        if low.endswith(".tsv"):
            df = pd.read_csv(path, sep="\t", dtype=str)
        elif low.endswith((".xlsx", ".xls")):
            df = pd.read_excel(path, dtype=str)
        else:
            df = pd.read_csv(path, sep=None, engine="python", dtype=str)
        cols = [_clean_cell(c) for c in df.columns]
        rows = []
        for rec in df.to_dict(orient="records"):
            rows.append({_clean_cell(k): _clean_cell(v) for k, v in rec.items()})
        return cols, rows
    except ImportError:
        pass
    except Exception as e:  # noqa: BLE001 - 交给 csv 兜底；仍失败则报错
        _fallback_err = e
    else:
        _fallback_err = None
    # 标准库兜底：仅 csv/tsv
    if low.endswith((".xlsx", ".xls")):
        raise EvidenceUploadError(
            "读取 Excel 失败（缺少 pandas/openpyxl 或文件损坏）。"
            "可另存为 CSV 后重新上传。")
    import csv as _csv
    sep = "\t" if low.endswith(".tsv") else ","
    with open(path, "r", encoding="utf-8-sig", errors="replace", newline="") as f:
        sample = f.read(64 * 1024)
        f.seek(0)
        if not low.endswith(".tsv"):
            try:
                sep = _csv.Sniffer().sniff(sample, delimiters=",;\t").delimiter
            except Exception:  # noqa: BLE001
                sep = ","
        rdr = _csv.DictReader(f, delimiter=sep)
        cols = [_clean_cell(c) for c in (rdr.fieldnames or [])]
        rows = [{_clean_cell(k): _clean_cell(v) for k, v in r.items()} for r in rdr]
    return cols, rows


def _pick_column(cols, field):
    """在表头里为某字段找列（先精确匹配别名，再退到「包含」匹配）。"""
    norm = {_norm_key(c): c for c in cols if c}
    for alias in COLUMN_ALIASES[field]:
        if alias in norm:
            return norm[alias]
    for alias in COLUMN_ALIASES[field]:
        # 包含匹配：'Article Title (英文)' 也能认出 title；但要求别名 ≥4 字符，
        # 避免中文单字（「年」「题」）乱命中。
        if len(alias) >= 4:
            for k, c in norm.items():
                if alias in k:
                    return c
    return None


def parse_literature_table(path, origin=None):
    """解析表格清单 → {"records": [...], "n_rows": n, "columns": [...], "warnings": [...]}。

    规则：
      - 必须有可识别的标题列；缺标题列直接报错（猜不出哪列是标题，硬猜不可原谅）。
      - 逐行必须有非空标题，空标题行计入 warnings 并跳过（用户表常见空尾行）。
      - 除标题外的字段一律「有则取、无则空」，不做任何补全。
    """
    origin = origin or os.path.basename(str(path))
    cols, rows = _read_table(path)
    if not rows:
        raise EvidenceUploadError(f"{origin}：表格里没有数据行。")
    # 表头行不在第一行时，把前导说明行去掉
    if not _pick_column(cols, "title"):
        raise EvidenceUploadError(
            f"{origin}：未找到标题列（可识别的表头如 标题 / Title / 题名 / Article Title）。"
            f"当前表头：{('、'.join(cols[:12]) or '(空)')}")
    c_title = _pick_column(cols, "title")
    c_auth = _pick_column(cols, "authors")
    c_year = _pick_column(cols, "year")
    c_jour = _pick_column(cols, "journal")
    c_doi = _pick_column(cols, "doi")
    c_pmid = _pick_column(cols, "pmid")
    c_type = _pick_column(cols, "study_type")
    c_abs = _pick_column(cols, "abstract")
    c_cite = _pick_column(cols, "cited_by")
    c_url = _pick_column(cols, "url")

    records, warnings, seen = [], [], set()
    for i, r in enumerate(rows, start=2):   # 2 = 数据从第 2 行起（含表头行）
        title = _clean_cell(r.get(c_title)) if c_title else ""
        if not title:
            warnings.append(f"第 {i} 行标题为空，已跳过")
            continue
        key = norm_title(title)
        if key and key in seen:
            warnings.append(f"第 {i} 行与前面重复（标题相同），已跳过")
            continue
        if key:
            seen.add(key)
        doi = norm_doi(r.get(c_doi)) if c_doi else ""
        records.append({
            "title": title,
            "authors": _split_authors_dupdrop(_split_authors(r.get(c_auth))) if c_auth else [],
            "year": parse_year(r.get(c_year)) if c_year else None,
            "journal": _clean_cell(r.get(c_jour)) if c_jour else "",
            "doi": doi or None,
            "pmid": _clean_cell(r.get(c_pmid)) if c_pmid else None,
            "abstract": _clean_cell(r.get(c_abs)) if c_abs else "",
            "cited_by": parse_int(r.get(c_cite)) if c_cite else None,
            "study_type": norm_study_type(r.get(c_type) if c_type else "", title),
            "source": "author-supplied",
            "origin": origin,
            "url": _clean_cell(r.get(c_url)) if c_url else None,
        })
    if not records:
        raise EvidenceUploadError(f"{origin}：未解析出任何有效文献条目（标题列全空？）")
    return {"records": records, "n_rows": len(rows), "columns": cols,
            "warnings": warnings}


# ---------------------------------------------------------------------------
# 文献管理器导出解析（RIS / BibTeX）
# ---------------------------------------------------------------------------

def _record_from_fields(fields, origin):
    """RIS / BibTeX 字段 dict → 统一 record。"""
    title = _clean_cell((fields.get("title") or [""])[0] if isinstance(fields.get("title"), list)
                        else fields.get("title"))
    if not title:
        return None
    raw_auth = fields.get("authors") or fields.get("author") or []
    if isinstance(raw_auth, str):
        raw_auth = [raw_auth]
    authors = []
    for a in raw_auth:
        authors.extend(_split_authors(a))
    for a in fields.get("bib_authors") or []:
        authors.append(_bib_author(a))
    year = parse_year((fields.get("year") or [""])[0] if isinstance(fields.get("year"), list)
                      else fields.get("year"))
    jour = fields.get("journal") or fields.get("venue") or ""
    if isinstance(jour, list):
        jour = jour[0] if jour else ""
    doi = norm_doi(fields.get("doi") or "")
    pmid = _clean_cell(fields.get("pmid") or "")
    stype = norm_study_type(fields.get("type") or "", title)
    abst = fields.get("abstract") or ""
    if isinstance(abst, list):
        abst = abst[0] if abst else ""
    return {
        "title": title,
        "authors": _split_authors_dupdrop(authors),
        "year": year,
        "journal": _clean_cell(jour),
        "doi": doi or None,
        "pmid": pmid or None,
        "abstract": _clean_cell(abst),
        "cited_by": None,
        "study_type": stype,
        "source": "author-supplied",
        "origin": origin,
        "url": None,
    }


def parse_ris(path, origin=None):
    origin = origin or os.path.basename(str(path))
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        text = f.read(MAX_TEXT_BYTES)
    # RIS 标签映射
    tag_map = {"TI": "title", "T1": "title", "BT": "title", "CT": "title",
               "AU": "authors", "A1": "authors", "A2": "authors",
               "PY": "year", "Y1": "year", "DA": "year",
               "JO": "journal", "JF": "journal", "JA": "journal", "T2": "journal",
               "DO": "doi", "AB": "abstract", "N2": "abstract",
               "AN": "pmid", "TY": "type", "UR": "url"}
    records, cur, started = [], {}, False
    for raw in text.splitlines():
        m = re.match(r"^([A-Z][A-Z0-9])\s{0,2}-\s?(.*)$", raw.rstrip())
        if not m:
            continue
        tag, val = m.group(1), m.group(2).strip()
        if tag == "ER":
            rec = _record_from_fields(cur, origin)
            if rec:
                records.append(rec)
            cur, started = {}, False
            continue
        if tag == "TY":
            started = True
            cur.setdefault("type", val)
            continue
        started = True
        key = tag_map.get(tag)
        if not key:
            continue
        if key in ("authors",):
            cur.setdefault("authors", []).append(val)
        else:
            cur.setdefault(key, val)
    rec = _record_from_fields(cur, origin) if started else None
    if rec:
        records.append(rec)
    if not records:
        raise EvidenceUploadError(f"{origin}：未解析出 RIS 条目（文件里没有 TI/AU 记录？）")
    return {"records": _dedup_records(records), "n_rows": len(records), "columns": ["RIS"],
            "warnings": []}


def parse_bib(path, origin=None):
    origin = origin or os.path.basename(str(path))
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        text = f.read(MAX_TEXT_BYTES)
    records = []
    for entry in re.finditer(r"@(\w+)\s*\{", text):
        etype = entry.group(1).lower()
        body = _bib_body(text, entry.end() - 1)
        if body is None:
            continue
        fields = _bib_fields(body)
        fields.setdefault("type", etype)
        rec = _record_from_fields(fields, origin)
        if rec:
            records.append(rec)
    if not records:
        raise EvidenceUploadError(f"{origin}：未解析出 BibTeX 条目（文件里没有 @article{...}？）")
    return {"records": _dedup_records(records), "n_rows": len(records),
            "columns": ["BibTeX"], "warnings": []}


def _bib_body(text, brace_pos):
    """从 '{' 位置取出配平的花括号内容。"""
    depth, i = 0, brace_pos
    while i < len(text):
        ch = text[i]
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            if depth == 0:
                return text[brace_pos + 1:i]
        i += 1
    return None


def _bib_fields(body):
    """BibTeX entry body → {field: value}（值已去掉外层花括号/引号）。"""
    # 跳过 entry key（第一个逗号之前）
    idx = body.find(",")
    if idx < 0:
        return {}
    body = body[idx + 1:]
    out = {}
    for m in re.finditer(r'(\w+)\s*=\s*(\{|")', body):
        val = _bib_body(body, m.end() - 1) if m.group(2) == "{" else _bib_quoted(body, m.end() - 1)
        if val is None:
            continue
        val = re.sub(r"\s+", " ", re.sub(r"[{}]", "", val)).strip()
        key = m.group(1).lower()
        if key in ("author", "authors"):
            out.setdefault("bib_authors", []).extend(
                [a.strip() for a in re.split(r"\s+and\s+|;", val) if a.strip()])
        elif key in ("title", "journal", "journaltitle", "year", "date", "doi",
                     "abstract", "url", "type"):
            out.setdefault({"journaltitle": "journal", "date": "year"}.get(key, key), val)
    return out


def _bib_quoted(text, quote_pos):
    end = text.find('"', quote_pos + 1)
    return text[quote_pos + 1:end] if end > 0 else None


def _dedup_records(records):
    """按 DOI → 归一标题去重（保留首现）。"""
    seen_doi, seen_title, out = set(), set(), []
    for r in records:
        d = norm_doi(r.get("doi"))
        t = norm_title(r.get("title"))
        if d and d in seen_doi:
            continue
        if t and t in seen_title:
            continue
        if d:
            seen_doi.add(d)
        if t:
            seen_title.add(t)
        out.append(r)
    return out


# ---------------------------------------------------------------------------
# PDF 打包解析
# ---------------------------------------------------------------------------

def _pdf_record(path, origin=None):
    """从单份 PDF 抽书目事实（标题 / DOI / 年份 / 作者）——只读，不臆造。

    复用 block_a 的抽取器（与 A4 上传 PDF 同一套口径，避免两处标题识别漂移）；
    block_a 不可用（缺 fitz）时退到文件名当标题，并如实标注。
    """
    origin = origin or os.path.basename(str(path))
    title, doi, authors, year = "", "", [], None
    try:
        import block_a
        title = block_a._extract_pdf_title(path) or ""
        doi = block_a._extract_pdf_doi(path) or ""
    except Exception:  # noqa: BLE001 - 抽取器不可用不该阻断上传
        pass
    if not title:
        # 退回文件名（去扩展名、把 _/- 换成空格）—— 明确标注来源，不伪装成真实标题
        base = os.path.splitext(os.path.basename(str(path)))[0]
        title = re.sub(r"[_\-]+", " ", base).strip()
    try:
        import fitz
        with fitz.open(path) as doc:
            meta = doc.metadata or {}
            if not authors:
                au = meta.get("author") or ""
                if au:
                    authors = _split_authors(au)
            head = ""
            for pi in range(min(2, doc.page_count)):
                head += (doc[pi].get_text("text") or "") + "\n"
            if authors:
                pass
            else:
                authors = _authors_from_text(head, title)
            year = parse_year(head[:4000]) if head else None
    except Exception:  # noqa: BLE001
        pass
    return {
        "title": title,
        "authors": _split_authors_dupdrop(authors),
        "year": year,
        "journal": "",
        "doi": norm_doi(doi) or None,
        "pmid": None,
        "abstract": "",
        "cited_by": None,
        "study_type": norm_study_type("", title),
        "source": "author-supplied",
        "origin": origin,
        "pdf": str(path),
        "url": None,
    }


def _authors_from_text(head, title):
    """首页文本里找作者块：标题下方、含 2–6 个「名 姓」片段的短行。"""
    if not head:
        return []
    lines = [re.sub(r"\s{2,}", " ", l).strip() for l in head.splitlines()]
    lines = [l for l in lines if l]
    tkey = norm_title(title)[:40]
    start = 0
    if tkey:
        for i, l in enumerate(lines[:20]):
            if tkey and tkey[:20] in norm_title(l):
                start = i + 1
                break
    for l in lines[start:start + 8]:
        if len(l) > 300 or len(l) < 6:
            continue
        if "@" in l or re.search(r"\b(abstract|keywords|doi|http)\b", l, re.I):
            continue
        cand = [c.strip() for c in re.split(r"[;,]|\band\b", l) if c.strip()]
        name_like = [c for c in cand if re.match(r"^[A-Z][A-Za-z'\-]+(\s+[A-Z][A-Za-z.\-]*){1,3}$", c)]
        if len(name_like) >= 2:
            return [a for c in name_like[:12] for a in _split_authors(c)]
    return []


# ---------------------------------------------------------------------------
# 入口：把一批上传文件解析成统一 evidence dict
# ---------------------------------------------------------------------------

def collect_uploads(paths, pdf_dir=None):
    """解析一批已落盘的上传文件 → evidence dict（与 search_evidence 同构）。

    Args:
        paths: 上传文件的本地路径列表（zip 会递归展开）。
        pdf_dir: 可选，落盘 zip 内 PDF 的目录（默认临时目录，仅本次有效）。

    Returns:
        evidence dict，额外字段：
          source = "user_upload"、user_files = [{name, kind, n_records, error}]
        解析彻底失败（一条都没解析出来）→ raise EvidenceUploadError（提示面向用户）。
    """
    records, files_meta, warnings = [], [], []
    for p in paths or []:
        if len(files_meta) >= MAX_FILES:
            warnings.append(f"文件数超过上限 {MAX_FILES}，其余已忽略")
            break
        name = os.path.basename(str(p))
        ext = os.path.splitext(name)[1].lower()
        try:
            if ext in BUNDLE_EXT:
                got, meta = _collect_zip(p, pdf_dir)
            elif ext in TABLE_EXT:
                got = parse_literature_table(p, name)["records"]
                meta = {"name": name, "kind": "table", "n_records": len(got)}
            elif ext in REFLIST_EXT:
                # .txt 可能是 RIS，也可能是纯文本清单（一行一篇）→ 依次尝试
                if ext == ".txt":
                    try:
                        got = parse_ris(p, name)["records"]
                    except EvidenceUploadError:
                        got = _parse_plain_lines(p, name)
                    if not got:
                        got = _parse_plain_lines(p, name)
                    meta = {"name": name, "kind": "reflist", "n_records": len(got)}
                else:
                    fn = parse_ris if ext == ".ris" else parse_bib
                    got = fn(p, name)["records"]
                    meta = {"name": name, "kind": "reflist", "n_records": len(got)}
            elif ext in PDF_EXT:
                rec = _pdf_record(_stage_pdf(p, pdf_dir, name), name)
                got = [rec]
                meta = {"name": name, "kind": "pdf", "n_records": 1}
            else:
                meta = {"name": name, "kind": "unsupported", "n_records": 0,
                        "error": f"不支持的文件类型 {ext or '(无扩展名)'}"}
                warnings.append(f"{name}：{meta['error']}")
                files_meta.append(meta)
                continue
        except EvidenceUploadError as e:
            meta = {"name": name, "kind": "error", "n_records": 0, "error": str(e)}
            warnings.append(str(e))
            files_meta.append(meta)
            continue
        except Exception as e:  # noqa: BLE001 - 单个文件失败不该炸掉整批
            meta = {"name": name, "kind": "error", "n_records": 0,
                    "error": f"{type(e).__name__}: {e}"}
            warnings.append(f"{name}：解析失败 {meta['error']}")
            files_meta.append(meta)
            continue
        records.extend(got)
        files_meta.append(meta)

    records = _dedup_records(records)
    if not records:
        detail = "；".join(warnings[:4]) or "没有可解析的条目"
        raise EvidenceUploadError(f"未能从上传文件解析出任何文献条目（{detail}）")

    return build_evidence(records, files_meta, warnings=warnings)


def _stage_pdf(src, pdf_dir, name):
    """把上传的 PDF 落到目标目录（缺省用临时目录），返回落盘路径。"""
    import shutil
    if not pdf_dir:
        return src
    try:
        os.makedirs(pdf_dir, exist_ok=True)
        dst = os.path.join(pdf_dir, _safe_name(name))
        shutil.copyfile(src, dst)
        return dst
    except Exception:  # noqa: BLE001 - 落盘失败就直接读源文件
        return src


def _safe_name(name):
    stem, ext = os.path.splitext(os.path.basename(str(name)))
    stem = re.sub(r"[^\w\u4e00-\u9fff.\-]+", "_", stem)[:80] or "file"
    return stem + (ext or "")


def _collect_zip(zip_path, pdf_dir):
    """展开 zip：内部 PDF / 表格 / RIS 逐个解析，统计进同一个 files_meta。

    PDF 落盘到 pdf_dir（会话级目录）以便后续 C3 核验复用；未给 pdf_dir 时
    解到临时目录（元数据仍可用，路径仅本次有效）。
    """
    base = os.path.splitext(os.path.basename(str(zip_path)))[0]
    target = pdf_dir or tempfile.mkdtemp(prefix="ma_zip_")
    os.makedirs(target, exist_ok=True)
    got, meta, total = [], {"name": os.path.basename(str(zip_path)), "kind": "zip",
                            "n_records": 0, "inner": [], "errors": []}, 0
    try:
        zf = zipfile.ZipFile(zip_path)
    except Exception as e:  # noqa: BLE001
        raise EvidenceUploadError(f"{base}.zip 无法打开：{type(e).__name__}: {e}")
    with zf:
        infos = [i for i in zf.infolist() if not i.is_dir()]
        total = sum(i.file_size for i in infos)
        if total > MAX_ZIP_BYTES:
            raise EvidenceUploadError(
                f"{base}.zip 解压后约 {total / 1024 / 1024:.0f} MB，超过上限 "
                f"{MAX_ZIP_BYTES // 1024 // 1024} MB；请拆包后再上传。")
        n_pdf = 0
        tmp = tempfile.mkdtemp(prefix="ma_zx_")
        for info in infos:
            inner_name = os.path.basename(info.filename)
            ext = os.path.splitext(inner_name)[1].lower()
            if not inner_name or inner_name.startswith("."):
                continue
            if ext not in TABLE_EXT + REFLIST_EXT + PDF_EXT:
                continue
            if ext in PDF_EXT:
                n_pdf += 1
                if n_pdf > MAX_PDFS:
                    meta["errors"].append(f"PDF 数超过上限 {MAX_PDFS}，其余已忽略")
                    break
            try:
                with zf.open(info) as src:
                    data = src.read()
            except Exception as e:  # noqa: BLE001
                meta["errors"].append(f"{inner_name} 解压失败：{e}")
                continue
            if ext in PDF_EXT:
                dst = os.path.join(target, _safe_name(inner_name))
                with open(dst, "wb") as f:
                    f.write(data)
                path, origin = dst, f"{base}.zip / {inner_name}"
            else:
                path = os.path.join(tmp, _safe_name(inner_name))
                with open(path, "wb") as f:
                    f.write(data[:MAX_TEXT_BYTES])
                origin = f"{base}.zip / {inner_name}"
            try:
                if ext in TABLE_EXT:
                    inner = parse_literature_table(path, origin)["records"]
                elif ext in PDF_EXT:
                    inner = [_pdf_record(path, origin)]
                elif ext == ".txt":
                    try:
                        inner = parse_ris(path, origin)["records"]
                    except EvidenceUploadError:
                        inner = _parse_plain_lines(path, origin)
                else:
                    fn = parse_ris if ext == ".ris" else parse_bib
                    inner = fn(path, origin)["records"]
            except EvidenceUploadError as e:
                meta["errors"].append(str(e))
                continue
            except Exception as e:  # noqa: BLE001
                meta["errors"].append(f"{inner_name} 解析失败：{type(e).__name__}: {e}")
                continue
            got.extend(inner)
            meta["inner"].append({"name": inner_name, "n_records": len(inner)})
    meta["n_records"] = len(got)
    return got, meta


def _parse_plain_lines(path, origin):
    """退路：把纯文本一行当一条标题（用户在 txt 里手抄清单的情况）。"""
    out = []
    with open(path, "r", encoding="utf-8-sig", errors="replace") as f:
        for line in f.read(MAX_TEXT_BYTES).splitlines():
            t = line.strip().strip("-•*").strip()
            if len(t) < 12:
                continue
            m_doi = re.search(r"10\.\d{4,9}/[-._;()/:A-Za-z0-9]+", t)
            doi_val = m_doi.group(0).rstrip(".;)") if m_doi else None
            # 年份只能从「去掉 DOI 之后」的文本里取：doi 里的 "2035790" 曾被误读成 2035 年
            rest = (t[:m_doi.start()] + " " + t[m_doi.end():]) if m_doi else t
            rest = re.sub(r"\b(doi|https?://\S*)\b[:：]?", " ", rest, flags=re.I)
            title_clean = re.sub(r"[\s,;:]+$", "", re.sub(r"^[\s,;:]+", "", rest))
            out.append({
                "title": title_clean or t, "authors": [], "year": parse_year(title_clean),
                "journal": "", "doi": doi_val,
                "pmid": None, "abstract": "", "cited_by": None,
                "study_type": norm_study_type("", t),
                "source": "author-supplied", "origin": origin, "url": None,
            })
    if not out:
        raise EvidenceUploadError(f"{origin}：纯文本清单里没有可用的标题行")
    return out


def build_evidence(records, files_meta=None, warnings=None, db_label=None):
    """records → 与 literature_probe.search_evidence() 同构的 evidence dict。

    `primary` / `synthesis` 两层按设计类型切分（与自动检索两层语义一致）：
    汇总性文献（meta 分析 / 系统评价 / 综述 / 指南）进 synthesis，其余进 primary。
    """
    prim = [r for r in records if str(r.get("study_type") or "") not in _SYNTH_TYPES]
    synth = [r for r in records if str(r.get("study_type") or "") in _SYNTH_TYPES]
    names = [f.get("name") for f in (files_meta or []) if f.get("name")]
    label_zh = db_label or ("作者自备文献（上传：" + "、".join(names[:3])
                            + ("…" if len(names) > 3 else "") + "）")
    # query 字段会被 C1 写进稿件正文的 "Search terms/syntax" —— 稿件是英文，
    # 这里**必须**是英文（文件名可能是中文，绝不能让中文渗进正文；出处由
    # block_c 的英文说明句交代）。中文标签另走 database_label，只给中文界面用。
    label_en = "author-supplied reference list (uploaded by the user)"
    return {
        "ok": True,
        "error": None,
        "source": "user_upload",
        "query": {"primary": label_en, "synthesis": label_en},
        "hit_count": {"primary": len(prim), "synthesis": len(synth)},
        "primary": prim,
        "synthesis": synth,
        "database": "author-supplied reference list (user-uploaded file)",
        "database_label": label_zh,
        # 作者自备清单**没有"检索日期/检索期"这回事** —— 留 None，避免稿件方法学
        # 里凭空生成一句 "searched from database inception to <今天>"。
        "searched_on": None,
        "uploaded_on": _today(),
        "user_files": files_meta or [],
        "warnings": warnings or [],
    }


def summary_line(ev):
    """给提示文案用的一行摘要。"""
    if not ev:
        return ""
    n_p = len(ev.get("primary") or [])
    n_s = len(ev.get("synthesis") or [])
    files = ev.get("user_files") or []
    names = "、".join(str(f.get("name")) for f in files[:3])
    if len(files) > 3:
        names += f" 等 {len(files)} 个文件"
    return f"{n_p + n_s} 篇（原始研究 {n_p} / 汇总性文献 {n_s}；来源：{names}）"


def evidence_file_kinds(ev):
    """上传文件类型概要（用于 UI 展示：'Excel 清单 1 个 / PDF 打包 1 个（12 篇）'）。"""
    out = []
    for f in (ev or {}).get("user_files") or []:
        kind = {"table": "表格清单", "reflist": "文献库导出", "pdf": "PDF",
                "zip": "PDF/文件打包"}.get(f.get("kind"), f.get("kind") or "文件")
        out.append(f"{kind}：{f.get('name')}（{f.get('n_records') or 0} 篇）")
    return out


if __name__ == "__main__":  # pragma: no cover - 手动自检
    import json
    import sys
    if len(sys.argv) < 2:
        print("用法：python evidence_upload.py <文件...>")
        raise SystemExit(2)
    try:
        ev = collect_uploads(sys.argv[1:])
    except EvidenceUploadError as e:
        print("解析失败：", e)
        raise SystemExit(1)
    print("解析成功：", summary_line(ev))
    for line in evidence_file_kinds(ev):
        print("  -", line)
    for w in ev.get("warnings") or []:
        print("  ! ", w)
    print(json.dumps((ev["primary"] + ev["synthesis"])[:2], ensure_ascii=False, indent=2))
