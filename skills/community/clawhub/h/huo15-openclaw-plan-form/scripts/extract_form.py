#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把任意格式的客户 Excel 熔解（melt）成规范化 JSON，对齐到目标模板的规范列。

规范化记录: {identity:{规范列:值}, scalars:{}, remark:{}, series:{ISO日期:数量}}

用法:
    python extract_form.py <文件> --template <模板id> [--sheet 名] [--header-row N]
        [--data-start N] [--mapping map.json] [--out norm.json] [--year 2026]

脚本会“自动猜”每列角色并打印映射报告；agent 复核后可用 --mapping 覆盖任何一列：
    {"sheet":"3月","header_row":1,"data_start":2,
     "columns":{"2":{"role":"identity","canonical":"客户料号"},
                "30":{"role":"date","iso":"2026-03-02"},
                "5":{"role":"ignore"}}}
key 用列序号(从0)或表头原文均可。
"""
from __future__ import annotations
import sys, os, json, argparse, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_forms import (load_schema, template_by_id, read_any, match_canonical,
                       parse_date_header, is_probably_non_date, norm_text,
                       pick_header_row, detect_year_hint)


def pick_best_sheet(path, template, scan_rows=6):
    """没指定 sheet 时，自动挑“最像主表”的 sheet（别名命中 + 日期列最多），跳过空 sheet。"""
    import warnings; warnings.filterwarnings("ignore")
    import pandas as pd
    try:
        sheets = pd.ExcelFile(path).sheet_names
    except Exception:
        return 0
    best, best_score = sheets[0], -1
    for sn in sheets[:12]:
        try:
            info = read_any(path, sheet=sn, max_rows=scan_rows)
        except Exception:
            continue
        rows = info["rows"]
        if not rows:
            continue
        # 标识列命中权重高，日期列封顶——避免“纯日期辅助表”盖过有标识的主表
        score = 0
        for r in rows:
            id_hits, date_hits = 0, 0
            for cell in r:
                canon, sc = match_canonical(cell, template["columns"])
                if canon and sc >= 0.7:
                    role = next((c["role"] for c in template["columns"] if c["canonical"] == canon), "")
                    id_hits += 1 if role == "identity" else 0
                elif not is_probably_non_date(cell):
                    d = parse_date_header(cell, allow_serial=True)
                    if d and d.get("kind") in ("day", "month"):
                        date_hits += 1
            score = max(score, id_hits * 3 + min(date_hits, 10))
        if score > best_score:
            best, best_score = sn, score
    return best


def role_of_canonical(template, canon):
    for c in template["columns"]:
        if c["canonical"] == canon:
            return c["role"]
    return "scalar"


def resolve_weekday_dates(rows, header_idx):
    """对“周一/周二”这种只有星期的表头，用相邻行里的真实日期补成 ISO。
    返回 {col_index: iso}。"""
    out = {}
    if header_idx < 0:
        return out
    hdr = rows[header_idx]
    for j, cell in enumerate(hdr):
        d = parse_date_header(cell)
        if d and d.get("kind") == "weekday_only":
            for around in (header_idx - 1, header_idx + 1):
                if 0 <= around < len(rows) and j < len(rows[around]):
                    d2 = parse_date_header(rows[around][j], allow_serial=True)
                    if d2 and d2.get("iso") and d2["kind"] == "day":
                        out[j] = d2["iso"]
                        break
    return out


def auto_map_columns(header, rows, header_idx, template, year_hint):
    """对每个源列判定 role/canonical/iso。返回 mapping 列表与报告。"""
    cols = template["columns"]
    wd_dates = resolve_weekday_dates(rows, header_idx)
    used_canon = set()
    mapping = []
    for j, raw in enumerate(header):
        entry = {"index": j, "header": (str(raw) if raw is not None else ""),
                 "role": "ignore", "canonical": None, "iso": None, "conf": 0.0}
        # 1) 日期列优先（但排除明显非日期）
        if not is_probably_non_date(raw):
            d = parse_date_header(raw, year_hint=year_hint, allow_serial=True)
            if d and d.get("iso") and d["kind"] in ("day", "month"):
                entry.update(role="date", iso=d["iso"], conf=d["conf"]); mapping.append(entry); continue
            if j in wd_dates:
                entry.update(role="date", iso=wd_dates[j], conf=0.75); mapping.append(entry); continue
        # 2) 规范列模糊匹配
        canon, sc = match_canonical(raw, cols)
        if canon and canon not in used_canon:
            r = role_of_canonical(template, canon)
            bucket = "identity" if r == "identity" else ("remark" if r == "remark" else "scalar")
            entry.update(role=bucket, canonical=canon, conf=sc)
            used_canon.add(canon)
        mapping.append(entry)
    return mapping


def apply_override(mapping, override_cols, header):
    if not override_cols:
        return mapping
    by_idx = {m["index"]: m for m in mapping}
    hdr_idx = {norm_text(h): i for i, h in enumerate(header)}
    for key, spec in override_cols.items():
        idx = int(key) if str(key).lstrip("-").isdigit() else hdr_idx.get(norm_text(key))
        if idx is None or idx not in by_idx:
            continue
        m = by_idx[idx]
        m["role"] = spec.get("role", m["role"])
        m["canonical"] = spec.get("canonical", m["canonical"])
        m["iso"] = spec.get("iso", m["iso"])
        m["conf"] = 1.0
    return mapping


def is_totals_or_empty(row, id_indexes):
    txt = " ".join(norm_text(row[i]) for i in id_indexes if i < len(row))
    if any(w in txt for w in ("合计", "总计", "小计", "汇总", "total")):
        return True
    return not any(row[i] is not None and str(row[i]).strip() not in ("", "0") for i in id_indexes)


def to_number(v):
    if v is None:
        return None
    if isinstance(v, bool):
        return None
    if isinstance(v, (int, float)):
        return None if (isinstance(v, float) and v != v) else v   # 滤 NaN
    if isinstance(v, (dt.datetime, dt.date, dt.time)):
        return None
    s = str(v).replace(",", "").strip()
    if s in ("", "-", "无", "/", "—"):
        return None
    try:
        f = float(s)
        return int(f) if f.is_integer() else round(f, 4)
    except ValueError:
        return None


def extract(path, template, sheet=None, header_row=None, data_start=None,
            override=None, year_hint=None):
    override = override or {}
    sheet = override.get("sheet", sheet)
    auto_sheet = False
    if sheet is None:
        sheet = pick_best_sheet(path, template)
        auto_sheet = True
    info = read_any(path, sheet=sheet)
    rows = info["rows"]
    if not rows:
        raise ValueError(f"sheet '{info['sheet']}' 为空，请用 --sheet 指定有数据的 sheet（可先跑 inspect_form.py 查看）")

    hidx = override.get("header_row", header_row)
    if hidx is None:
        hidx = pick_header_row(rows, template["columns"])
    header = rows[hidx]
    if year_hint is None:
        year_hint = detect_year_hint(rows, hidx)

    mapping = auto_map_columns(header, rows, hidx, template, year_hint)
    mapping = apply_override(mapping, override.get("columns"), header)

    id_idx = [m["index"] for m in mapping if m["role"] == "identity"]
    if not id_idx:  # 没识别到标识列就退而用前几非日期非空列
        id_idx = [m["index"] for m in mapping if m["role"] != "date"][:3]

    dstart = override.get("data_start", data_start)
    if dstart is None:
        dstart = hidx + 1
        # 跳过紧邻表头的子表头/合计行
        while dstart < len(rows) and is_totals_or_empty(rows[dstart], id_idx):
            dstart += 1

    out_rows = []
    for r in rows[dstart:]:
        if is_totals_or_empty(r, id_idx):
            continue
        rec = {"identity": {}, "scalars": {}, "remark": {}, "series": {}}
        for m in mapping:
            j = m["index"]
            v = r[j] if j < len(r) else None
            if m["role"] == "date" and m["iso"]:
                q = to_number(v)
                if q is not None:
                    rec["series"][m["iso"]] = rec["series"].get(m["iso"], 0) + q
            elif m["role"] == "identity" and m["canonical"]:
                if v is not None and str(v).strip() != "":
                    rec["identity"][m["canonical"]] = _clean(v)
            elif m["role"] == "scalar" and m["canonical"]:
                q = to_number(v)
                rec["scalars"][m["canonical"]] = q if q is not None else _clean(v)
            elif m["role"] == "remark" and m["canonical"]:
                if v is not None and str(v).strip() != "":
                    rec["remark"][m["canonical"]] = _clean(v)
        if rec["identity"] or rec["series"]:
            out_rows.append(rec)

    dates = sorted({iso for rr in out_rows for iso in rr["series"].keys()})
    result = {
        "source_file": os.path.basename(path), "template_id": template["id"],
        "sheet": info["sheet"], "header_row": hidx, "data_start": dstart,
        "year_hint": year_hint, "n_rows": len(out_rows),
        "date_range": [dates[0], dates[-1]] if dates else None,
        "n_dates": len(dates), "dates": dates,
        "auto_sheet": auto_sheet, "all_sheets": info["sheets"],
        "mapping": mapping, "rows": out_rows,
    }
    return result


def _clean(v):
    if v is None:
        return None
    if isinstance(v, (dt.datetime, dt.date)):
        return v.isoformat()[:10]
    if isinstance(v, dt.time):
        return v.strftime("%H:%M:%S")
    if isinstance(v, float):
        if v != v:                 # NaN
            return None
        return int(v) if v.is_integer() else v
    if isinstance(v, (str, int, bool)):
        return v.strip() if isinstance(v, str) else v
    return str(v)                  # 兜底：任何非 JSON 原生类型转字符串


def print_report(res):
    print(f"📄 {res['source_file']}  ➜ 模板 {res['template_id']}")
    print(f"   sheet='{res['sheet']}'  表头行={res['header_row']}  数据起始行={res['data_start']}  年份提示={res['year_hint']}")
    if res.get("auto_sheet") and len([s for s in res.get("all_sheets", [])]) > 1:
        print(f"   ⚠️  sheet 为自动选取，工作簿含多个 sheet={res['all_sheets']}；"
              f"若选错请 --sheet 指定（建议先跑 inspect_form.py 看清各 sheet）")
    print(f"   数据行={res['n_rows']}  日期列={res['n_dates']}  日期范围={res['date_range']}")
    print("   —— 列映射（请复核，可用 --mapping 覆盖）——")
    for m in res["mapping"]:
        tag = {"identity": "标识", "scalar": "数值", "remark": "备注", "date": "日期", "ignore": "—略"}.get(m["role"], m["role"])
        extra = m["canonical"] or m["iso"] or ""
        h = (m["header"] or "")[:18]
        flag = "  ⚠️低" if (m["role"] != "ignore" and m["conf"] < 0.7) else ""
        print(f"     [{m['index']:>2}] {h:20} → {tag:4} {str(extra):14} conf={m['conf']}{flag}")
    unmapped = [m for m in res["mapping"] if m["role"] == "ignore" and m["header"]]
    if unmapped:
        print(f"   未映射(丢弃)列: {[m['header'][:12] for m in unmapped]}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("file")
    ap.add_argument("--template", required=True)
    ap.add_argument("--sheet", default=None)
    ap.add_argument("--header-row", type=int, default=None)
    ap.add_argument("--data-start", type=int, default=None)
    ap.add_argument("--mapping", default=None, help="覆盖映射的 JSON 文件")
    ap.add_argument("--year", type=int, default=None)
    ap.add_argument("--out", default=None, help="写规范化 JSON 到此路径")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()

    schema = load_schema()
    tpl = template_by_id(schema, args.template)
    override = {}
    if args.mapping:
        with open(args.mapping, encoding="utf-8") as f:
            override = json.load(f)
    res = extract(args.file, tpl, sheet=args.sheet, header_row=args.header_row,
                  data_start=args.data_start, override=override, year_hint=args.year)
    if not args.quiet:
        print_report(res)
    out = args.out or (os.path.splitext(args.file)[0] + ".norm.json")
    with open(out, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1, default=str)
    if not args.quiet:
        print(f"   ✓ 规范化数据已写出: {out}")


if __name__ == "__main__":
    main()
