#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""huo15 计划表单 skill —— 共享底层库。

职责（被 classify / extract / fill / diff / build_clean_templates 复用）：
  1. read_any()        —— .xls/.xlsx/.csv 统一读成二维 list（保留原始单元格类型）
  2. parse_date_header() —— 把五花八门的日期表头解析成 ISO 日期（最难的一块）
  3. match_canonical() —— 把客户文件的乱表头模糊匹配到模板规范列
  4. load_schema()     —— 读 templates_schema.json

不引入除 pandas / openpyxl 之外的第三方依赖。Python 3.8+。
"""
from __future__ import annotations
import os, re, json, datetime as dt
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_PATH = os.path.join(HERE, "..", "reference", "templates_schema.json")
EXCEL_EPOCH = dt.date(1899, 12, 30)          # Excel 1900 日期系统锚点
WEEKDAYS_CN = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]


# ----------------------------------------------------------------------------
# schema
# ----------------------------------------------------------------------------
def load_schema(path: str | None = None) -> dict:
    with open(path or SCHEMA_PATH, encoding="utf-8") as f:
        return json.load(f)


def template_by_id(schema: dict, tid: str) -> dict:
    for t in schema["templates"]:
        if t["id"] == tid:
            return t
    raise KeyError(f"unknown template id: {tid}")


# ----------------------------------------------------------------------------
# 文本规范化 + 别名匹配
# ----------------------------------------------------------------------------
def norm_text(s: Any) -> str:
    """规范化表头文本：去空白/全角转半角/小写拉丁/剥常见装饰。"""
    if s is None:
        return ""
    s = str(s)
    # 全角 -> 半角
    out = []
    for ch in s:
        o = ord(ch)
        if o == 0x3000:
            out.append(" ")
        elif 0xFF01 <= o <= 0xFF5E:
            out.append(chr(o - 0xFEE0))
        else:
            out.append(ch)
    s = "".join(out)
    s = s.replace("\n", "").replace("\r", "").replace("\t", "")
    s = re.sub(r"\s+", "", s)
    s = s.lower()
    # 剥日期/版本类装饰，便于纯文字匹配（保留中文核心词）
    s = s.strip()
    return s


def match_canonical(header: str, columns: list[dict]) -> tuple[str | None, float]:
    """把单个客户表头模糊匹配到模板的规范列。返回 (canonical, score 0..1)。"""
    h = norm_text(header)
    if not h:
        return None, 0.0
    best, best_score = None, 0.0
    for col in columns:
        canon = col["canonical"]
        if canon.startswith("__"):
            continue
        for alias in col.get("aliases", [canon]):
            a = norm_text(alias)
            if not a:
                continue
            if h == a:
                score = 1.0
            elif h == norm_text(canon):
                score = 0.98
            elif a in h or h in a:
                # 越接近完整越高分
                score = 0.6 + 0.3 * (min(len(a), len(h)) / max(len(a), len(h)))
            else:
                # token 重叠（拉丁/数字）
                ta, th = set(re.findall(r"[a-z0-9]+", a)), set(re.findall(r"[a-z0-9]+", h))
                inter = ta & th
                score = 0.5 * (len(inter) / max(1, len(ta | th))) if inter else 0.0
            if score > best_score:
                best, best_score = canon, score
    return (best, round(best_score, 3)) if best_score >= 0.55 else (None, round(best_score, 3))


# ----------------------------------------------------------------------------
# 日期表头解析 —— skill 最关键的鲁棒性来源
# ----------------------------------------------------------------------------
_NON_DATE_HINTS = ("计划", "版", "预测", "新增", "库存", "在制", "已交", "未交",
                   "结余", "合计", "备注", "厂家", "供应商", "数量", "单位",
                   "需求", "新", "目标", "累计")
# 这些库存/交付语义词即便表头带“X月X日”也不是日期列（如“4月27日代理库存”=库存快照，非交期）
_STRONG_NON_DATE = ("库存", "已交", "未交", "在制", "在产", "结余", "预测", "迷你图")


def excel_serial_to_date(n: float) -> dt.date | None:
    try:
        n = float(n)
    except (TypeError, ValueError):
        return None
    if not (20000 <= n <= 80000):       # 约 1954-04 ~ 2089，排除序号/数量
        return None
    return EXCEL_EPOCH + dt.timedelta(days=int(n))


def parse_date_header(raw: Any, year_hint: int | None = None,
                      allow_serial: bool = True) -> dict | None:
    """把一个表头单元格解析成日期。

    返回 {'kind':'day'|'month', 'iso':'YYYY-MM-DD'|'YYYY-MM', 'conf':float, 'raw':str}
    解析不出来返回 None。year_hint 用于补全缺年份的表头（0227 / 5月1日 / 周一）。
    """
    if raw is None:
        return None
    # 1) 已是 datetime / date（pandas 常已解析好 Excel 日期单元格）
    if isinstance(raw, (dt.datetime, dt.date)):
        d = raw.date() if isinstance(raw, dt.datetime) else raw
        return {"kind": "day", "iso": d.isoformat(), "conf": 0.99, "raw": str(raw)}
    # 2) 纯数字 —— Excel 序列号
    if isinstance(raw, (int, float)) and not isinstance(raw, bool):
        if allow_serial:
            d = excel_serial_to_date(raw)
            if d:
                return {"kind": "day", "iso": d.isoformat(), "conf": 0.7, "raw": str(raw)}
        return None

    s = str(raw).strip()
    if not s:
        return None
    sn = norm_text(s)

    # 强语义排除：带库存/已交/未交/在制等词的列，即便含“X月X日”也不是日期列
    if any(h in sn for h in _STRONG_NON_DATE):
        return None

    # 显式排除：计划版本 / 预测 / 月需求 等非交付日期
    # （但 "5月1日"/"5月7号" 这类带 日/号 的仍是日期，下面优先匹配）
    has_day_marker = bool(re.search(r"\d+\s*[日号]", sn)) or bool(re.search(r"\(?(周|星期|周)[一二三四五六日天]", sn))

    # a) YYYY[.-/]M[.-/]D
    m = re.search(r"(20\d{2})[.\-/年](\d{1,2})[.\-/月](\d{1,2})", sn)
    if m:
        y, mo, d = int(m.group(1)), int(m.group(2)), int(m.group(3))
        try:
            return {"kind": "day", "iso": dt.date(y, mo, d).isoformat(), "conf": 0.95, "raw": s}
        except ValueError:
            pass

    # b) M月D日 / M月D号（缺年份用 hint）
    m = re.search(r"(\d{1,2})\s*月\s*(\d{1,2})\s*[日号]", sn)
    if m:
        mo, d = int(m.group(1)), int(m.group(2))
        y = year_hint or _default_year()
        try:
            return {"kind": "day", "iso": dt.date(y, mo, d).isoformat(), "conf": 0.85, "raw": s}
        except ValueError:
            pass

    # c) MMDD(周X) / MMDD(Weekday)  例: 0227(周五) 0403(Friday)
    m = re.match(r"^(\d{2})(\d{2})\s*[\(（]?\s*(周|星期|mon|tue|wed|thu|fri|sat|sun)", sn)
    if not m:
        m = re.match(r"^(\d{2})(\d{2})\s*[\(（]", sn)   # MMDD( 无星期
    if m:
        mo, d = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12 and 1 <= d <= 31:
            y = year_hint or _default_year()
            try:
                return {"kind": "day", "iso": dt.date(y, mo, d).isoformat(), "conf": 0.8, "raw": s}
            except ValueError:
                pass

    # d) 纯 MMDD（4 位数字，且不像年份）
    m = re.match(r"^(\d{2})(\d{2})$", sn)
    if m and has_day_marker is False:
        mo, d = int(m.group(1)), int(m.group(2))
        if 1 <= mo <= 12 and 1 <= d <= 31:
            y = year_hint or _default_year()
            try:
                return {"kind": "day", "iso": dt.date(y, mo, d).isoformat(), "conf": 0.55, "raw": s}
            except ValueError:
                pass

    # e) M月（月粒度，且不是“X月计划/预测/需求”这类版本词）
    m = re.fullmatch(r"(\d{1,2})\s*月", sn)
    if m:
        mo = int(m.group(1))
        if 1 <= mo <= 12:
            y = year_hint or _default_year()
            return {"kind": "month", "iso": f"{y:04d}-{mo:02d}", "conf": 0.6, "raw": s}

    # f) 周X / 星期X（仅星期，需配合上一行真实日期，单独无法定日 -> 返回弱信号）
    for i, wd in enumerate(WEEKDAYS_CN):
        if sn in (wd, wd.replace("周", "星期")):
            return {"kind": "weekday_only", "iso": None, "conf": 0.3, "raw": s, "weekday": i}

    return None


def _default_year() -> int:
    # 不依赖 Math.random/Date.now 在 OpenClaw workflow 之外是安全的；这里允许真实当前年
    try:
        return dt.date.today().year
    except Exception:
        return 2026


def is_probably_non_date(raw: Any) -> bool:
    """快速判断某表头明显不是日期（计划版本/预测/库存等），用于减少误判。"""
    s = norm_text(raw)
    if not s:
        return True
    if re.search(r"20\d{2}[.\-/年]\d", s) or re.search(r"\d+\s*[日号]", s):
        return False
    return any(h in s for h in _NON_DATE_HINTS)


# ----------------------------------------------------------------------------
# 读文件 —— .xls / .xlsx / .csv 统一成二维 list
# ----------------------------------------------------------------------------
def read_any(path: str, sheet: Any = 0, max_rows: int | None = None) -> dict:
    """返回 {'sheets': [名...], 'sheet': 实际sheet名, 'rows': [[...],...]}。
    rows 保留原始单元格类型（datetime/数字/字符串）。"""
    ext = os.path.splitext(path)[1].lower()
    if ext == ".csv":
        import csv
        with open(path, encoding="utf-8-sig", errors="replace") as f:
            rows = list(csv.reader(f))
        if max_rows:
            rows = rows[:max_rows]
        return {"sheets": ["csv"], "sheet": "csv", "rows": rows}

    import warnings
    warnings.filterwarnings("ignore")
    import pandas as pd
    xls = pd.ExcelFile(path)
    sheets = list(xls.sheet_names)
    if isinstance(sheet, int):
        sname = sheets[sheet] if sheet < len(sheets) else sheets[0]
    else:
        sname = sheet if sheet in sheets else sheets[0]
    df = pd.read_excel(path, sheet_name=sname, header=None,
                       nrows=max_rows, dtype=object)
    rows: list[list[Any]] = []
    for _, r in df.iterrows():
        rows.append([_cell(v) for v in r.tolist()])
    return {"sheets": sheets, "sheet": sname, "rows": rows}


def _cell(v: Any) -> Any:
    import pandas as pd
    if v is None:
        return None
    try:
        if pd.isna(v):
            return None
    except (TypeError, ValueError):
        pass
    if hasattr(v, "to_pydatetime"):       # pandas Timestamp
        return v.to_pydatetime()
    return v


def pick_header_row(rows: list[list[Any]], columns: list[dict],
                    scan: int = 8) -> int:
    """在前 scan 行里挑“最像表头”的一行：与规范别名匹配最多的那行。"""
    best_idx, best_hits = 0, -1
    for i in range(min(scan, len(rows))):
        hits = 0
        for cell in rows[i]:
            canon, sc = match_canonical(cell, columns)
            if canon and sc >= 0.7:
                hits += 1
            elif parse_date_header(cell, allow_serial=False):
                hits += 1
        if hits > best_hits:
            best_idx, best_hits = i, hits
    return best_idx


def detect_year_hint(rows: list[list[Any]], header_idx: int) -> int | None:
    """扫表头附近找一个完整日期，确定年份，给缺年份的表头补全用。"""
    for i in (header_idx, header_idx - 1, header_idx + 1):
        if 0 <= i < len(rows):
            for cell in rows[i]:
                d = parse_date_header(cell, allow_serial=True)
                if d and d.get("iso") and d["kind"] == "day":
                    return int(d["iso"][:4])
    return None


if __name__ == "__main__":
    # 自检：日期解析样例
    samples = [46136, "2026.04.17", "2026/5/1假", "0227(周五)", "0403(Friday)",
               "5月1日", "4月25号到货", "周一", "5月计划", "0417版计划", "6月预测",
               dt.datetime(2026, 5, 4), "2026-03-02 00:00:00"]
    for s in samples:
        print(f"{str(s)[:20]:22} -> {parse_date_header(s, year_hint=2026)}")
