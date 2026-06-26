#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把一个或多个规范化 JSON（extract_form.py 产物）填充成干净的标准模板 xlsx。

- 多个输入会合并（行拼接 + 日期区取并集），实现“统一为一个模板文件”。
- 输出从 schema 现搭，天然无示例数据；文件名 = output_name_pattern(数据日期) + 末尾追加生成时刻(精确到分钟)。

用法:
    python fill_template.py <norm1.json> [norm2.json ...] [--template id]
        [--out 输出.xlsx] [--name-date 20260501] [--dedup]
"""
from __future__ import annotations
import sys, os, json, argparse, datetime as dt
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lib_forms import load_schema, template_by_id
from lib_xlsx import write_form


def load_norm(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def dedup_rows(rows, keys):
    """按 diff_key 合并重复标识的行（后者的 series/scalars 覆盖/累加）。"""
    seen = {}
    order = []
    for r in rows:
        k = tuple(str(r["identity"].get(kk, "")) for kk in keys)
        if k == tuple("" for _ in keys):
            order.append(r); continue
        if k in seen:
            base = seen[k]
            base["series"].update(r["series"])
            base["scalars"].update({kk: v for kk, v in r["scalars"].items() if v not in (None, "")})
            base["remark"].update(r["remark"])
            base["identity"].update({kk: v for kk, v in r["identity"].items() if v not in (None, "")})
        else:
            seen[k] = r; order.append(r)
    return order


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("norm", nargs="+", help="一个或多个 .norm.json")
    ap.add_argument("--template", default=None)
    ap.add_argument("--out", default=None)
    ap.add_argument("--name-date", default=None, help="输出文件名里的日期，默认数据最早日期/今天")
    ap.add_argument("--dedup", action="store_true", help="按模板主键合并重复行")
    ap.add_argument("--out-dir", default=".")
    args = ap.parse_args()

    schema = load_schema()
    norms = [load_norm(p) for p in args.norm]
    tid = args.template or norms[0].get("template_id")
    if not tid:
        sys.exit("未指定 --template 且 norm 内无 template_id")
    if any(n.get("template_id") and n["template_id"] != tid for n in norms):
        print("⚠️  多个输入的 template_id 不一致，将统一按", tid, "处理")
    tpl = template_by_id(schema, tid)

    rows = []
    for n in norms:
        rows.extend(n.get("rows", []))
    for r in rows:                      # 容错：缺桶补齐
        for b in ("identity", "scalars", "remark", "series"):
            r.setdefault(b, {})

    if args.dedup:
        rows = dedup_rows(rows, tpl.get("diff_key", []))

    dates = sorted({iso for r in rows for iso in r["series"].keys()})

    # 文件名 = 业务数据日期段 + 末尾追加“生成时刻(精确到分钟)”
    name_date = args.name_date
    if not name_date:
        name_date = (dates[0].replace("-", "") if dates else dt.date.today().strftime("%Y%m%d"))
    gen_ts = dt.datetime.now().strftime("%Y%m%d-%H%M")     # 如 20260602-1430
    fname = tpl["output_name_pattern"].format(date=name_date)
    stem, ext = os.path.splitext(fname)
    fname = f"{stem}_{gen_ts}{ext}"                        # 客户需求排产表_20260227_20260602-1430.xlsx
    out_path = args.out or os.path.join(args.out_dir, fname)

    res = write_form(out_path, tpl, rows=rows, dates=dates)
    print(f"✓ 已生成【{tpl['display_name']}】: {out_path}")
    print(f"   生成时刻={gen_ts.replace('-', ' ')[:13]}（已写入文件名末尾，精确到分钟）")
    print(f"   数据行={res['n_rows']}  列数={res['n_cols']}  日期区={len(dates)}列  "
          f"范围={(dates[0]+'~'+dates[-1]) if dates else '无'}")
    print(f"   来源: {[n['source_file'] for n in norms]}")


if __name__ == "__main__":
    main()
