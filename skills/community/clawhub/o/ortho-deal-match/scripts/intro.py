# -*- coding: utf-8 -*-
"""
intro.py — 对接与联系方式交换

核心规则：**双方都点头才交换联系方式**。

  request  发起接触意向（任一方）
  accept   确认意向（买方一次 + 卖方一次 = 双方同意）
  decline  拒绝（这次撮合作废；加 --block 则把对方永久列入拒访名单）
  reveal   双方都同意后才能展开联系方式，消耗最严配额并重点留痕
  feedback 记录后续结果（已报价 / 寄样 / 成交 / 无意向）

状态流转：suggested --一方同意--> half --另一方同意--> connected --reveal--> 可联系
        任一步 decline --> declined

用法：
  python intro.py request  --match M001 --side buyer  --user U001 --note "想了解MOQ"
  python intro.py accept   --match M001 --side seller --user U002
  python intro.py decline  --match M001 --side seller --user U002 --reason "产能已满"
  python intro.py reveal   --match M001 --user U001
  python intro.py feedback --match M001 --user U001 --result "已寄样，报价中"
  python intro.py assign   --match M003 --to U002 --by U001   # owner 分派同事跟进

权限：owner 全库可见；member 只能操作自己参与的单（自己发布的、
分派给自己的、自己操作过的）。其余一律拦截并留痕。
"""
import argparse
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402
import init_db  # noqa: E402

SIDE_LABEL = {"buyer": "买方", "seller": "卖方"}
OK_FIELD = {"buyer": "buyer_ok", "seller": "seller_ok"}
OTHER_SIDE = {"buyer": "seller", "seller": "buyer"}


def _load(con, mid):
    m = con.execute("SELECT * FROM matches WHERE id=?", (mid,)).fetchone()
    if not m:
        return None, None, None, None
    d = con.execute("SELECT * FROM demands WHERE id=?", (m["demand_id"],)).fetchone()
    c = con.execute("SELECT * FROM capabilities WHERE id=?", (m["capability_id"],)).fetchone()
    pb = con.execute("SELECT * FROM parties WHERE id=?", (d["party_id"],)).fetchone()
    pc = con.execute("SELECT * FROM parties WHERE id=?", (c["party_id"],)).fetchone()
    return m, d, c, (pb, pc)


def _next_intro_id(con):
    n = 0
    for (iid,) in con.execute("SELECT id FROM intros"):
        mm = re.match(r"^I(\d+)$", iid or "")
        if mm:
            n = max(n, int(mm.group(1)))
    return f"I{n + 1:03d}"


def _log(con, mid, actor, side, action, note=""):
    iid = _next_intro_id(con)
    con.execute("INSERT INTO intros (id,match_id,actor,side,action,note,created) "
                "VALUES (?,?,?,?,?,?,?)", (iid, mid, actor, side, action, note, core._now()))
    return iid


def _touch(con, mid, status):
    con.execute("UPDATE matches SET status=?, updated=? WHERE id=?",
                (status, core._now(), mid))


def _guard(con, uid, mid):
    """member 可见域校验：不相关单直接拦截并留痕。"""
    ok, msg = core.can_access_match(con, uid, mid)
    if not ok:
        print("  访问被拒：" + msg)
        core.audit_log("denied", uid, f"越权访问撮合 {mid}")
        con.close()
    return ok


# ---------------------------------------------------------------- 命令


def cmd_request(a):
    con = init_db.connect()
    m, d, c, parties = _load(con, a.match)
    if not m:
        print(f"  未找到撮合 {a.match}")
        return 1
    if not _guard(con, a.user, a.match):
        return 1
    if m["status"] in ("declined",):
        print(f"  {a.match} 已作废（{m['status']}），不能发起")
        return 1
    p = parties[0] if a.side == "buyer" else parties[1]
    if core.is_blocked(p["name"]):
        print(f"  {p['name']} 在拒访名单中，不能发起接触。")
        con.close()
        return 1
    if not (p.get("email") or p.get("phone")):
        print(f"  {SIDE_LABEL[a.side]} {p['name']} 尚未留联系方式，无法完成对接。")
        print(f"  请先补齐：python publish.py party ... （或联系登记人 {p.get('owner','')}）")
        con.close()
        return 1

    _log(con, a.match, a.user, a.side, "request", a.note or "")
    # 发起方视为已同意自己这一侧
    field = OK_FIELD[a.side]
    con.execute(f"UPDATE matches SET {field}=1 WHERE id=?", (a.match,))
    other_ok = OK_FIELD[OTHER_SIDE[a.side]]
    row = con.execute(f"SELECT {other_ok} FROM matches WHERE id=?", (a.match,)).fetchone()
    _touch(con, a.match, "connected" if row[other_ok] else "half")
    con.commit()
    core.audit_log("intro_request", a.user,
                   f"{a.match} 以{SIDE_LABEL[a.side]}身份发起：{a.note or '（无备注）'}",
                   refs=[a.match])
    con.close()

    print(f"  已发起接触意向：{a.match}（{SIDE_LABEL[a.side]} {p['name']}）")
    st = con_status(a.match)
    if st == "connected":
        print("  双方均已同意，可以交换联系方式：")
        print(f"    python intro.py reveal --match {a.match} --user {a.user}")
    else:
        other = "卖方" if a.side == "buyer" else "买方"
        print(f"  等待{other}确认。对方确认后双方才能看到联系方式。")
    return 0


def con_status(mid):
    con = init_db.connect()
    r = con.execute("SELECT status FROM matches WHERE id=?", (mid,)).fetchone()
    con.close()
    return r["status"] if r else ""


def cmd_accept(a):
    con = init_db.connect()
    m, d, c, parties = _load(con, a.match)
    if not m:
        print(f"  未找到撮合 {a.match}")
        return 1
    if not _guard(con, a.user, a.match):
        return 1
    if m["status"] == "declined":
        print(f"  {a.match} 已作废，不能确认")
        return 1
    field = OK_FIELD[a.side]
    other = OK_FIELD[OTHER_SIDE[a.side]]
    if m[field]:
        print(f"  {SIDE_LABEL[a.side]}已确认过，无需重复")
        con.close()
        return 0

    p = parties[0] if a.side == "buyer" else parties[1]
    con.execute(f"UPDATE matches SET {field}=1 WHERE id=?", (a.match,))
    _log(con, a.match, a.user, a.side, "accept", a.note or "")
    both = con.execute(f"SELECT {other} FROM matches WHERE id=?", (a.match,)).fetchone()[other]
    if both:
        _touch(con, a.match, "connected")
    else:
        _touch(con, a.match, "half")
    con.commit()
    core.audit_log("intro_accept", a.user,
                   f"{a.match} {SIDE_LABEL[a.side]}确认意向", refs=[a.match])
    con.close()

    if both:
        print("=" * 68)
        print(f"  双方均已确认  {a.match}")
        print("=" * 68)
        print(f"  {SIDE_LABEL[a.side]} {p['name']} 已确认，另一侧此前也已确认。")
        print("  现在可以交换联系方式：")
        print(f"    python intro.py reveal --match {a.match} --user {a.user}")
    else:
        other_side = "卖方" if a.side == "buyer" else "买方"
        print(f"  {SIDE_LABEL[a.side]}已确认，等待{other_side}确认后才能交换联系方式。")
    return 0


def cmd_decline(a):
    con = init_db.connect()
    m, d, c, parties = _load(con, a.match)
    if not m:
        print(f"  未找到撮合 {a.match}")
        return 1
    if not _guard(con, a.user, a.match):
        return 1
    p = parties[0] if a.side == "buyer" else parties[1]
    _touch(con, a.match, "declined")
    _log(con, a.match, a.user, a.side, "decline", a.reason or "")
    con.commit()
    core.audit_log("intro_decline", a.user,
                   f"{a.match} {SIDE_LABEL[a.side]}拒绝：{a.reason or '（无理由）'}",
                   refs=[a.match])
    con.close()

    print(f"  {a.match} 已作废。{SIDE_LABEL[a.side]}不参与本次对接，联系方式不会交换。")
    if a.block:
        core.cmd_block(argparse.Namespace(
            company=p["name"], reason=a.reason or f"{a.match} 对接中拒绝", by=a.user))
    else:
        print(f"  如对方明确表示「不要再联系」，请加 --block 记入拒访名单。")
    return 0


def cmd_reveal(a):
    con = init_db.connect()
    m, d, c, parties = _load(con, a.match)
    if not m:
        print(f"  未找到撮合 {a.match}")
        return 1
    if not _guard(con, a.user, a.match):
        return 1
    pb, pc = parties

    if m["status"] != "connected":
        print("=" * 68)
        print("  还不能交换联系方式")
        print("=" * 68)
        print(f"  当前状态：{m['status']}（需要 connected）")
        need = []
        if not m["buyer_ok"]:
            need.append(f"买方确认：python intro.py accept --match {a.match} --side buyer --user ...")
        if not m["seller_ok"]:
            need.append(f"卖方确认：python intro.py accept --match {a.match} --side seller --user ...")
        for line in need:
            print("  " + line)
        con.close()
        return 1

    if core.is_blocked(pb["name"]) or core.is_blocked(pc["name"]):
        print("  该撮合涉及拒访名单主体，不能交换联系方式。")
        con.close()
        return 1

    missing = [p["name"] for p in (pb, pc) if not (p.get("email") or p.get("phone"))]
    if missing:
        print(f"  以下主体尚未留联系方式，无法交换：{'、'.join(missing)}")
        con.close()
        return 1

    ok, msg, u = core.check_access(a.user, "reveal", 1)
    if not ok:
        print("  " + msg.replace("\n", "\n  "))
        core.audit_log("denied", a.user, f"reveal 被拒 {a.match}")
        con.close()
        return 1

    _log(con, a.match, a.user, "system", "reveal", "联系方式已交换")
    con.commit()
    core.audit_log("reveal", a.user,
                   f"{a.match} 交换 {pb['name']} <-> {pc['name']}",
                   refs=[a.match], cost=1)
    con.close()

    print("=" * 74)
    print(f"  联系方式已交换   {a.match}   撮合分 {m['score']}")
    print("=" * 74)
    for label, p, dcap in (("买方", pb, d), ("卖方", pc, c)):
        print(f"  {label}  {p['name']}（{p.get('country') or '-'}）")
        if p.get("person"):
            print(f"        联系人 {p['person']}" + (f" · {p['title']}" if p.get("title") else ""))
        if p.get("email"):
            print(f"        邮箱   {p['email']}")
        if p.get("phone"):
            print(f"        电话   {p['phone']}")
        if p.get("website"):
            print(f"        官网   {p['website']}")
        print(f"        事项   {dcap['title'][:36]}")
        print()
    print("  " + "-" * 70)
    print("  本次交换已写入审计链（不可篡改）。以下行为会留下记录：")
    print("    · 把这些信息转给第三方、导入群发系统或公开张贴")
    print("    · 对方表示不感兴趣后继续纠缠或换渠道联系")
    print("    · 未签 NDA 就索取图纸、报价、工艺参数")
    print()
    print(f"  后续结果请回写：python intro.py feedback --match {a.match} "
          f"--user {a.user} --result \"已报价\"")
    return 0


def cmd_assign(a):
    """owner 把撮合分派给同事跟进。member 的可见域包含「分派给自己的」。"""
    con = init_db.connect()
    if not core.is_owner(a.by):
        print("  只有 owner 能分派撮合。")
        core.audit_log("denied", a.by, f"越权尝试分派 {a.match}")
        con.close()
        return 1
    m = con.execute("SELECT * FROM matches WHERE id=?", (a.match,)).fetchone()
    if not m:
        print(f"  未找到撮合 {a.match}")
        con.close()
        return 1
    target = core.find_user(a.to)
    if not target:
        print(f"  被分派人 {a.to} 未登记。先：python core.py register ...")
        con.close()
        return 1
    if a.clear:
        con.execute("UPDATE matches SET assignee=NULL, updated=? WHERE id=?",
                    (core._now(), a.match))
        con.commit()
        core.audit_log("assign", a.by, f"{a.match} 分派已撤销", refs=[a.match])
        con.close()
        print(f"  {a.match} 的分派已撤销。")
        return 0
    con.execute("UPDATE matches SET assignee=?, updated=? WHERE id=?",
                (a.to, core._now(), a.match))
    _log(con, a.match, a.by, "system", "assign", f"分派给 {target['uid']} {target['name']}")
    con.commit()
    core.audit_log("assign", a.by, f"{a.match} -> {a.to} {target['name']}", refs=[a.match])
    con.close()
    print(f"  {a.match} 已分派给 {a.to} {target['name']}。")
    print(f"  {a.to} 现在可以查看与跟进这条撮合（含双向确认与交换联系方式）。")
    print(f"  其余 member 看不到这条单，owner 全库可见。")
    return 0


def cmd_feedback(a):
    con = init_db.connect()
    m, d, c, parties = _load(con, a.match)
    if not m:
        print(f"  未找到撮合 {a.match}")
        return 1
    if not _guard(con, a.user, a.match):
        return 1
    _log(con, a.match, a.user, "system", "feedback", a.result or "")
    con.commit()
    core.audit_log("feedback", a.user, f"{a.match} 结果：{a.result}", refs=[a.match])
    con.close()
    print(f"  已记录 {a.match}：{a.result}")
    return 0


def main():
    ap = argparse.ArgumentParser(description="对接与联系方式交换")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("request", help="发起接触意向")
    p.add_argument("--match", required=True)
    p.add_argument("--side", required=True, choices=["buyer", "seller"])
    p.add_argument("--note", default="")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_request)

    p = sub.add_parser("accept", help="确认意向")
    p.add_argument("--match", required=True)
    p.add_argument("--side", required=True, choices=["buyer", "seller"])
    p.add_argument("--note", default="")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_accept)

    p = sub.add_parser("decline", help="拒绝")
    p.add_argument("--match", required=True)
    p.add_argument("--side", required=True, choices=["buyer", "seller"])
    p.add_argument("--reason", default="")
    p.add_argument("--block", action="store_true", help="同时永久列入拒访名单")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_decline)

    p = sub.add_parser("reveal", help="交换联系方式（需双方都已确认）")
    p.add_argument("--match", required=True)
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_reveal)

    p = sub.add_parser("feedback", help="回写对接结果")
    p.add_argument("--match", required=True)
    p.add_argument("--result", required=True)
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_feedback)

    p = sub.add_parser("assign", help="owner 分派撮合给同事跟进")
    p.add_argument("--match", required=True)
    p.add_argument("--to", help="被分派人编号 U00x")
    p.add_argument("--clear", action="store_true", help="撤销分派")
    p.add_argument("--by", required=True, help="操作人编号（须为 owner）")
    p.set_defaults(func=cmd_assign)

    a = ap.parse_args()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
