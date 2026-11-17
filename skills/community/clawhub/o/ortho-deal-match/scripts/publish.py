# -*- coding: utf-8 -*-
"""
publish.py — 发布主体、需求与能力

双向发布：买方发需求，卖方发能力，我们做撮合。
发布时自动把中英混杂的自由文本归一化到骨科标准词，撮合才对得上。

用法：
  # 1. 登记主体（我方填 --self，联系方式必填）
  python publish.py party --name "示例医疗科技" --side both --country 中国 \
                          --person 张三 --email 本人邮箱 --user U001 --self
  python publish.py party --name "Mueller GmbH" --side buyer --country 德国 --user U001

  # 2. 发需求（买方）
  python publish.py demand --party P001 --title "找钛合金锁定板OEM" \
      --desc "Ti6Al4V 锁定接骨板与髓内钉，年用量约 5000 套，需 ISO13485 + CE MDR" \
      --qty "5000 套/年" --deadline 2026-12-31 --user U001

  # 3. 发能力（卖方）
  python publish.py capability --party P002 --title "创伤类植入物代工" \
      --desc "CNC 加工钛合金与不锈钢，阳极氧化与EO灭菌，ISO13485，产能2万件/月" \
      --capacity "2万件/月" --moq "500件" --lead-time "45天" --user U001

  # 4. 查看 / 关闭
  python publish.py list --user U001
  python publish.py close --demand D001 --user U001
  python publish.py close --capability C001 --user U001
"""
import argparse
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402
import init_db  # noqa: E402
import taxonomy  # noqa: E402

# 展会库位置：默认取兄弟技能目录，可用环境变量 ORTHO_EXPO_DB 覆盖
EXPO_DB = os.environ.get(
    "ORTHO_EXPO_DB",
    os.path.join(os.path.dirname(core.SKILL_DIR),
                 "ortho-expo-contacts", "data", "contacts.db"))
DEFAULT_VALID_DAYS = 180

# ---------------------------------------------------------------- 工具


def con_open():
    return init_db.connect()


def next_id(con, table, prefix):
    n = 0
    for (rid,) in con.execute(f"SELECT id FROM {table}"):
        m = re.match(rf"^{prefix}(\d+)$", rid or "")
        if m:
            n = max(n, int(m.group(1)))
    return f"{prefix}{n + 1:03d}"


def pick(con, table, pid, label):
    if not pid:
        print(f"  请指定{label}编号（--party / --demand / --capability）")
        return None
    r = con.execute(f"SELECT * FROM {table} WHERE id=?", (pid,)).fetchone()
    if not r:
        print(f"  未找到{label} {pid}")
        return None
    return dict(r)


def verify_expo(company):
    """在展会名录里核验主体是否真实存在，返回 (verified, expo_ref, category)"""
    if not company or not os.path.exists(EXPO_DB):
        return 0, "", ""
    key = core._norm_company(company)
    if not key:
        return 0, "", ""
    try:
        # 只读 URI 打开兄弟技能的索引库（工程上固化只读语义）
        uri = "file:" + EXPO_DB.replace("\\", "/") + "?mode=ro"
        con = sqlite3.connect(uri, uri=True)
        con.row_factory = sqlite3.Row
        row = con.execute(
            "SELECT source, category FROM contacts WHERE company_norm=? LIMIT 1", (key,)
        ).fetchone()
        if not row and len(key) >= 6:
            row = con.execute(
                "SELECT source, category FROM contacts WHERE company_norm LIKE ? LIMIT 1",
                (key[:8] + "%",)
            ).fetchone()
        con.close()
        if row:
            return 1, row["source"], row["category"] or ""
    except sqlite3.Error:
        pass  # 展会库不可用时降级为无溯源信息，不影响主流程
    return 0, "", ""


def auto_norm(title, desc, override=None, domain="cat"):
    """显式指定优先，否则从标题+描述里抽"""
    if override:
        return override.strip()
    return taxonomy.join_norm(f"{title or ''} {desc or ''}", domain)


def _valid_until(days):
    return (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")


# ---------------------------------------------------------------- 主体


def cmd_party(a):
    ok, msg, u = core.check_access(a.user, "publish", 1)
    if not ok:
        print("  " + msg.replace("\n", "\n  "))
        return 1
    if a.self and not (a.email or a.phone):
        print("  我方主体（--self）必须填联系方式，否则对方没法回绝你也没法找你。")
        return 1
    if core.is_blocked(a.name):
        print(f"  {a.name} 在拒访名单中，不能登记。")
        core.audit_log("denied", a.user, f"尝试登记拒访主体 {a.name}")
        return 1

    con = con_open()
    key = core._norm_company(a.name)
    exist = con.execute("SELECT * FROM parties WHERE name_norm=?", (key,)).fetchone()
    if exist:
        print(f"  主体已存在：{exist['id']}  {exist['name']}")
        return 1

    verified, expo_ref, cat = verify_expo(a.name)
    pid = next_id(con, "parties", "P")
    con.execute(
        "INSERT INTO parties (id,name,name_norm,side,country,city,person,title,email,phone,"
        "website,owner,is_self,verified,expo_ref,note,status,created) "
        "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (pid, a.name.strip(), key, a.side, a.country or "", a.city or "",
         a.person or "", a.title or "", a.email or "", a.phone or "", a.website or "",
         a.user, 1 if a.self else 0, verified, expo_ref, a.note or "",
         "active", core._now()))
    con.commit()
    core.audit_log("publish_party", a.user, f"{pid} {a.name} side={a.side}",
                   refs=[pid], cost=1)
    con.close()

    print("=" * 68)
    print(f"  主体已登记   {pid}")
    print("=" * 68)
    print(f"  名称     {a.name}")
    print(f"  角色     {a.side}" + ("  （我方自有）" if a.self else ""))
    if a.country:
        print(f"  国家     {a.country}")
    if a.person:
        print(f"  联系人   {a.person}" + (f" · {a.title}" if a.title else ""))
    if a.email:
        print(f"  邮箱     {a.email}")
    if a.phone:
        print(f"  电话     {a.phone}")
    if verified:
        print(f"  已核验   在展会名录中找到：{expo_ref}")
        if cat:
            print(f"           名录标注业务：{cat[:50]}")
    else:
        print("  未核验   展会名录中无匹配（不影响发布，仅作可信度参考）")
    if not (a.email or a.phone):
        print("  注意     未填联系方式，撮合成功后无法交换，需补齐")
    return 0


# ---------------------------------------------------------------- 需求 / 能力


def _publish(a, kind):
    table = "demands" if kind == "demand" else "capabilities"
    prefix = "D" if kind == "demand" else "C"
    label = "需求" if kind == "demand" else "能力"

    ok, msg, u = core.check_access(a.user, "publish", 1)
    if not ok:
        print("  " + msg.replace("\n", "\n  "))
        return 1

    con = con_open()
    p = pick(con, "parties", a.party, "主体")
    if not p:
        return 1
    if core.is_blocked(p["name"]):
        print(f"  主体 {p['name']} 在拒访名单中，不能发布。")
        return 1

    title = (a.title or "").strip()
    desc = (a.desc or "").strip()
    if not title and not desc:
        print(f"  请至少填写 --title 或 --desc，否则无法撮合")
        return 1

    oid = next_id(con, table, prefix)
    now = core._now()
    blob = f"{title} {desc}"

    if kind == "demand":
        con.execute(
            "INSERT INTO demands (id,party_id,title,raw,cat,process,material,cert,market,"
            "cat_raw,qty,deadline,budget,status,owner,visibility,valid_until,created) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (oid, p["id"], title or desc[:30], desc,
             auto_norm(title, desc, a.cat, "cat"),
             auto_norm(None, blob, a.process, "process"),
             auto_norm(None, blob, a.material, "material"),
             auto_norm(None, blob, a.cert, "cert"),
             auto_norm(None, blob, a.market, "market"),
             a.cat or "", a.qty or "", a.deadline or "", a.budget or "",
             "open", a.user, a.visibility, _valid_until(a.valid_days), now))
    else:
        con.execute(
            "INSERT INTO capabilities (id,party_id,title,raw,cat,process,material,cert,market,"
            "cat_raw,capacity,moq,lead_time,status,owner,visibility,valid_until,created) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (oid, p["id"], title or desc[:30], desc,
             auto_norm(title, desc, a.cat, "cat"),
             auto_norm(None, blob, a.process, "process"),
             auto_norm(None, blob, a.material, "material"),
             auto_norm(None, blob, a.cert, "cert"),
             auto_norm(None, blob, a.market, "market"),
             a.cat or "", a.capacity or "", a.moq or "", a.lead_time or "",
             "open", a.user, a.visibility, _valid_until(a.valid_days), now))
    con.commit()
    core.audit_log(f"publish_{kind}", a.user, f"{oid} {title or desc[:30]}",
                   refs=[oid], cost=1)
    con.close()

    print("=" * 68)
    print(f"  {label}已发布   {oid}   （{p['name']}）")
    print("=" * 68)
    print(f"  标题     {title or desc[:30]}")
    n = taxonomy.norm(blob)
    if n:
        print("  自动识别")
        for dom, vals in n.items():
            print(f"      {taxonomy.DOMAIN_LABEL[dom]:<6} {' / '.join(sorted(vals))}")
    else:
        print("  自动识别 （未命中词典，建议补充 --cat 等字段）")
    extra = []
    if kind == "demand":
        extra = [(x, y) for x, y in (("数量", a.qty), ("截止", a.deadline), ("预算", a.budget)) if y]
    else:
        extra = [(x, y) for x, y in (("产能", a.capacity), ("起订", a.moq), ("交期", a.lead_time)) if y]
    for k, v in extra:
        print(f"  {k}       {v}")
    print(f"  可见性   {a.visibility}    有效期至 {_valid_until(a.valid_days)}")
    print(f"\n  撮合：python match.py run --{kind} {oid} --user {a.user}")
    return 0


def cmd_demand(a):
    return _publish(a, "demand")


def cmd_capability(a):
    return _publish(a, "capability")


# ---------------------------------------------------------------- 列表 / 关闭


def cmd_list(a):
    con = con_open()
    print("=" * 78)
    print(f"  需求列表（{'我的' if a.mine else '全部'}）")
    print("=" * 78)
    sql_d = ("SELECT d.*, p.name AS pname, p.country FROM demands d "
             "LEFT JOIN parties p ON p.id=d.party_id")
    args = []
    if a.mine:
        sql_d += " WHERE d.owner=?"
        args.append(a.user)
    rows = list(con.execute(sql_d + " ORDER BY d.id", args))
    if not rows:
        print("  （空）")
    for r in rows:
        print(f"  {r['id']}  [{r['status']}] {r['title'][:34]}")
        print(f"        主体 {r['pname']} ({r['country'] or '-'})  "
              f"分类 {r['cat'] or '-'}  {r['visibility']}")
    print()
    print("=" * 78)
    print(f"  能力列表（{'我的' if a.mine else '全部'}）")
    print("=" * 78)
    sql_c = ("SELECT c.*, p.name AS pname, p.country FROM capabilities c "
             "LEFT JOIN parties p ON p.id=c.party_id")
    if a.mine:
        sql_c += " WHERE c.owner=?"
    rows = list(con.execute(sql_c + " ORDER BY c.id", args))
    if not rows:
        print("  （空）")
    for r in rows:
        print(f"  {r['id']}  [{r['status']}] {r['title'][:34]}")
        print(f"        主体 {r['pname']} ({r['country'] or '-'})  "
              f"分类 {r['cat'] or '-'}  {r['visibility']}")
    con.close()
    return 0


def cmd_activate(a):
    """把线索提升为可撮合主体：必须补录经过确认的联系方式"""
    ok, msg, u = core.check_access(a.user, "publish", 1)
    if not ok:
        print("  " + msg.replace("\n", "\n  "))
        return 1
    if not (a.email or a.phone):
        print("  激活必须填联系方式（--email 或 --phone）")
        print("  线索来自公开展会名录，本身不含个人联系方式。")
        print("  只有在你确认对方愿意被接触之后，才应该激活。")
        return 1

    con = con_open()
    p = con.execute("SELECT * FROM parties WHERE id=? AND status='lead'", (a.lead,)).fetchone()
    if not p:
        print(f"  未找到线索 {a.lead}（只有 status=lead 的主体能激活）")
        return 1
    if core.is_blocked(p["name"]):
        print(f"  {p['name']} 在拒访名单中，不能激活。")
        return 1
    con.execute(
        "UPDATE parties SET status='active', person=?, title=?, email=?, phone=?, "
        "side=?, note=? WHERE id=?",
        (a.person or "", a.title or "", a.email or "", a.phone or "",
         a.side, a.note or p["note"], a.lead))
    con.commit()
    core.audit_log("activate", a.user, f"{a.lead} {p['name']} 线索已激活", refs=[a.lead], cost=1)
    con.close()

    print("=" * 68)
    print(f"  线索已激活   {a.lead}  {p['name']}")
    print("=" * 68)
    print(f"  来源     {p.get('expo_ref') or '-'}（展会公开名录）")
    print(f"  联系人   {a.person or '-'}" + (f" · {a.title}" if a.title else ""))
    print(f"  邮箱     {a.email or '-'}")
    print(f"  角色     {a.side}")
    print()
    print("  现在可以为它发布能力：")
    print(f"    python publish.py capability --party {a.lead} --title ... --desc ... --user {a.user}")
    return 0


def cmd_close(a):
    con = con_open()
    if a.demand:
        r = con.execute("UPDATE demands SET status='closed' WHERE id=?", (a.demand,))
        oid, kind = a.demand, "需求"
    elif a.capability:
        r = con.execute("UPDATE capabilities SET status='closed' WHERE id=?", (a.capability,))
        oid, kind = a.capability, "能力"
    else:
        print("  请指定 --demand 或 --capability")
        return 1
    con.commit()
    if r.rowcount == 0:
        print(f"  未找到 {oid}")
        return 1
    core.audit_log("close", a.user, f"{kind} {oid} 已关闭", refs=[oid])
    print(f"  {kind} {oid} 已关闭，不再参与撮合")
    con.close()
    return 0


# ---------------------------------------------------------------- CLI


def main():
    ap = argparse.ArgumentParser(description="发布主体、需求与能力")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("party", help="登记主体")
    p.add_argument("--name", required=True)
    p.add_argument("--side", default="both", choices=["buyer", "seller", "both"])
    p.add_argument("--country", default="")
    p.add_argument("--city", default="")
    p.add_argument("--person", default="")
    p.add_argument("--title", default="")
    p.add_argument("--email", default="")
    p.add_argument("--phone", default="")
    p.add_argument("--website", default="")
    p.add_argument("--note", default="")
    p.add_argument("--self", action="store_true", help="我方自有主体")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_party)

    for name, label in (("demand", "需求"), ("capability", "能力")):
        p = sub.add_parser(name, help=f"发布{label}")
        p.add_argument("--party", required=True)
        p.add_argument("--title")
        p.add_argument("--desc", help="自由描述，中英文都行，自动归一化")
        p.add_argument("--cat", help="产品分类（覆盖自动识别）")
        p.add_argument("--process"), p.add_argument("--material")
        p.add_argument("--cert"), p.add_argument("--market")
        if name == "demand":
            p.add_argument("--qty"), p.add_argument("--deadline"), p.add_argument("--budget")
        else:
            p.add_argument("--capacity"), p.add_argument("--moq"), p.add_argument("--lead-time")
        p.add_argument("--visibility", default="public", choices=["public", "private"])
        p.add_argument("--valid-days", type=int, default=DEFAULT_VALID_DAYS)
        p.add_argument("--user", required=True)
        p.set_defaults(func=cmd_demand if name == "demand" else cmd_capability)

    p = sub.add_parser("activate", help="把线索提升为可撮合主体")
    p.add_argument("--lead", required=True)
    p.add_argument("--person"), p.add_argument("--title")
    p.add_argument("--email"), p.add_argument("--phone")
    p.add_argument("--side", default="seller", choices=["buyer", "seller", "both"])
    p.add_argument("--note", default="")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_activate)

    p = sub.add_parser("list", help="查看已发布")
    p.add_argument("--mine", action="store_true", help="只看我发布的")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("close", help="关闭需求或能力")
    p.add_argument("--demand"), p.add_argument("--capability")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_close)

    a = ap.parse_args()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
