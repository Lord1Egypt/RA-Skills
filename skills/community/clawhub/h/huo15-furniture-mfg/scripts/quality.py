#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quality.py — 质检查询 + 拍照质检（P3）

查询命令
  todo [--limit N]           待检清单（quality_state = none）
  recent [--days 7]          最近质检记录
  fail [--days 30]           不合格清单
  stats [--days 30]          合格率统计（按检查项目分组）

写命令（确认制：默认 dry-run，--yes 执行）
  attach <QC号或MO号> --image <路径> [--image ...] [--yes]
                             把现场照片挂到质检单（多图，huo15_quality_multi_picture）
                             传 MO 号时自动定位其待检质检单
  detach <附件id> [--yes]     删除误传照片（attach 成功时会打印附件 id）
  judge <QC号> --result pass|fail [--yes]
                             质检判定（调 do_pass / do_fail，不可随意撤销，慎用）

示例
  python3 quality.py todo
  python3 quality.py attach MO-260604-643 --image /tmp/qc1.jpg --image /tmp/qc2.jpg
  python3 quality.py judge QC00618 --result pass
"""

from __future__ import annotations

import argparse
import base64
import mimetypes
import sys
from pathlib import Path

from actions import _confirm_gate
from odoo_client import Odoo, OdooError
from odoo_utils import QC_STATE, days_ago_utc, from_utc, label, m2o_name, render_table

# 注意：quality.check 的状态字段是 quality_state（none/pass/fail），没有 state 字段
QC_FIELDS = ["name", "title", "product_id", "quality_state", "control_date",
             "picking_id", "production_id", "user_id", "team_id"]


def _qc_rows(checks: list[dict]) -> list[list]:
    rows = []
    for c in checks:
        src = m2o_name(c.get("production_id")) or m2o_name(c.get("picking_id"))
        rows.append([c["name"], c.get("title") or "", m2o_name(c["product_id"]),
                     label(QC_STATE, c["quality_state"]),
                     from_utc(c["control_date"], "%m-%d %H:%M") if c.get("control_date") else "",
                     src, m2o_name(c.get("user_id"))])
    return rows


HEADERS = ["质检单", "项目", "产品", "结果", "时间", "来源单据", "责任人"]


def cmd_todo(args):
    odoo = Odoo()
    checks = odoo.search_read("quality.check", [["quality_state", "=", "none"]],
                              QC_FIELDS, limit=args.limit, order="id desc")
    if not checks:
        print("✅ 没有待检的质检单。")
        return
    total = odoo.search_count("quality.check", [["quality_state", "=", "none"]])
    print(f"🔍 待检质检单（共 {total} 张，显示 {len(checks)} 张）\n")
    print(render_table(_qc_rows(checks), HEADERS))


def cmd_recent(args):
    odoo = Odoo()
    domain = [["control_date", ">=", days_ago_utc(args.days)]]
    checks = odoo.search_read("quality.check", domain, QC_FIELDS,
                              limit=args.limit, order="control_date desc")
    print(f"🔍 最近 {args.days} 天质检记录（{len(checks)} 张）\n")
    print(render_table(_qc_rows(checks), HEADERS))


def cmd_fail(args):
    odoo = Odoo()
    domain = [["quality_state", "=", "fail"]]
    if args.days:
        domain.append(["control_date", ">=", days_ago_utc(args.days)])
    checks = odoo.search_read("quality.check", domain, QC_FIELDS,
                              limit=args.limit, order="control_date desc")
    if not checks:
        print(f"✅ 最近 {args.days} 天没有不合格记录。")
        return
    print(f"❌ 最近 {args.days} 天不合格质检（{len(checks)} 张）\n")
    print(render_table(_qc_rows(checks), HEADERS))


def cmd_stats(args):
    # 本库 94% 质检单不挂 product_id（质检点挂在作业类型上），按检查项目 title 分组才有意义
    odoo = Odoo()
    domain = [["control_date", ">=", days_ago_utc(args.days)],
              ["quality_state", "in", ["pass", "fail"]]]
    groups = odoo.read_group("quality.check", domain, [],
                             ["title", "quality_state"], lazy=False)
    stat: dict[str, dict] = {}
    for g in groups:
        tname = g.get("title") or "(未命名检查)"
        s = stat.setdefault(tname, {"pass": 0, "fail": 0})
        s[g["quality_state"]] = g.get("__count", 0)
    if not stat:
        print(f"最近 {args.days} 天没有已完成的质检。")
        return
    rows, tp, tf = [], 0, 0
    for tname, s in sorted(stat.items(), key=lambda kv: -(kv[1]["pass"] + kv[1]["fail"])):
        total = s["pass"] + s["fail"]
        tp += s["pass"]; tf += s["fail"]
        rows.append([tname, total, s["pass"], s["fail"], f"{s['pass'] / total * 100:.1f}%"])
    print(f"📊 最近 {args.days} 天质检合格率（总 {tp + tf} 检，合格率 {tp / (tp + tf) * 100:.1f}%）\n")
    print(render_table(rows, ["检查项目", "检数", "合格", "不合格", "合格率"]))


def _resolve_qc(odoo: Odoo, ref: str) -> dict:
    """QC 号直查；MO 号 → 该制造单上最新的待检质检单。"""
    fields = ["name", "title", "quality_state", "production_id", "picking_id", "picture_ids"]
    qcs = odoo.search_read("quality.check", [["name", "ilike", ref]], fields, limit=1)
    if qcs:
        return qcs[0]
    mos = odoo.search_read("mrp.production", [["name", "ilike", ref]], ["name"], limit=1)
    if mos:
        qcs = odoo.search_read(
            "quality.check",
            [["production_id", "=", mos[0]["id"]], ["quality_state", "=", "none"]],
            fields, limit=1, order="id desc")
        if qcs:
            return qcs[0]
        raise OdooError(f"{mos[0]['name']} 上没有待检的质检单。")
    raise OdooError(f"找不到质检单或制造单：{ref}")


def cmd_attach(args):
    odoo = Odoo()
    qc = _resolve_qc(odoo, args.ref)
    paths = []
    for p in args.image:
        path = Path(p).expanduser()
        if not path.is_file():
            raise OdooError(f"图片不存在：{p}")
        mime = mimetypes.guess_type(path.name)[0] or ""
        if not mime.startswith("image/"):
            raise OdooError(f"不是图片文件：{p}（{mime or '未知类型'}）")
        paths.append((path, mime))

    src = m2o_name(qc.get("production_id")) or m2o_name(qc.get("picking_id"))
    print("📷 将要执行：质检单挂照片")
    print(f"   质检单: {qc['name']} {qc.get('title') or ''}（{label(QC_STATE, qc['quality_state'])}）"
          + (f" | 来源 {src}" if src else ""))
    print(f"   已有照片: {len(qc.get('picture_ids') or [])} 张，本次新增 {len(paths)} 张：")
    for path, _ in paths:
        print(f"     · {path.name}（{path.stat().st_size / 1024:.0f} KB）")
    _confirm_gate(args.yes)

    att_ids = []
    for path, mime in paths:
        att_id = odoo.create("ir.attachment", {
            "name": path.name,
            "datas": base64.b64encode(path.read_bytes()).decode(),
            "res_model": "quality.check",   # 归属直接挂质检单（模块 wizard 同款修正）
            "res_id": qc["id"],
            "mimetype": mime,
        })
        odoo.write("quality.check", qc["id"], {"picture_ids": [(4, att_id)]})
        att_ids.append(att_id)
    print(f"✅ 已挂 {len(att_ids)} 张照片到 {qc['name']}（附件 id: {att_ids}）")
    print(f"   误传可撤：python3 quality.py detach {' '.join(map(str, att_ids))} --yes")


def cmd_detach(args):
    odoo = Odoo()
    ids = [int(i) for i in args.attachment_id]
    atts = odoo.search_read("ir.attachment",
                            [["id", "in", ids], ["res_model", "=", "quality.check"]],
                            ["name", "res_id"])
    if not atts:
        print("没有找到对应的质检照片附件（可能已删除）。")
        return
    print("🗑 将要执行：删除质检照片")
    for a in atts:
        print(f"   · attachment {a['id']} {a['name']}（质检单 id={a['res_id']}）")
    _confirm_gate(args.yes)
    odoo.unlink("ir.attachment", [a["id"] for a in atts])
    print(f"✅ 已删除 {len(atts)} 张。")


def cmd_judge(args):
    odoo = Odoo()
    qc = _resolve_qc(odoo, args.ref)
    if qc["quality_state"] != "none":
        raise OdooError(
            f"{qc['name']} 已是「{label(QC_STATE, qc['quality_state'])}」，不能重复判定。")
    n_pic = len(qc.get("picture_ids") or [])
    src = m2o_name(qc.get("production_id")) or m2o_name(qc.get("picking_id"))
    verdict = "合格 (pass)" if args.result == "pass" else "不合格 (fail)"
    print("🔍 将要执行：质检判定（判定后状态不可随意撤销，请确认照片/检验已完成）")
    print(f"   质检单: {qc['name']} {qc.get('title') or ''}"
          + (f" | 来源 {src}" if src else "") + f" | 已挂照片 {n_pic} 张")
    print(f"   判定结果: {verdict}")
    _confirm_gate(args.yes)
    odoo.call("quality.check", "do_pass" if args.result == "pass" else "do_fail", [qc["id"]])
    after = odoo.read("quality.check", [qc["id"]], ["quality_state"])[0]
    print(f"✅ 已判定：{qc['name']} → {label(QC_STATE, after['quality_state'])}")


def build_parser():
    p = argparse.ArgumentParser(description="质检查询 + 拍照质检")
    sub = p.add_subparsers(dest="cmd", required=True)
    t = sub.add_parser("todo", help="待检清单")
    t.add_argument("--limit", type=int, default=30)
    r = sub.add_parser("recent", help="最近质检")
    r.add_argument("--days", type=int, default=7)
    r.add_argument("--limit", type=int, default=30)
    f = sub.add_parser("fail", help="不合格清单")
    f.add_argument("--days", type=int, default=30)
    f.add_argument("--limit", type=int, default=30)
    s = sub.add_parser("stats", help="合格率统计")
    s.add_argument("--days", type=int, default=30)

    a = sub.add_parser("attach", help="质检单挂照片（确认制）")
    a.add_argument("ref", help="QC 号或 MO 号")
    a.add_argument("--image", action="append", required=True, help="图片路径，可重复")
    a.add_argument("--yes", action="store_true")
    d = sub.add_parser("detach", help="删除误传照片（确认制）")
    d.add_argument("attachment_id", nargs="+")
    d.add_argument("--yes", action="store_true")
    j = sub.add_parser("judge", help="质检判定 pass/fail（确认制）")
    j.add_argument("ref", help="QC 号或 MO 号")
    j.add_argument("--result", required=True, choices=["pass", "fail"])
    j.add_argument("--yes", action="store_true")
    return p


def main(argv=None):
    args = build_parser().parse_args(argv)
    try:
        {"todo": cmd_todo, "recent": cmd_recent, "fail": cmd_fail, "stats": cmd_stats,
         "attach": cmd_attach, "detach": cmd_detach, "judge": cmd_judge}[args.cmd](args)
    except OdooError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
