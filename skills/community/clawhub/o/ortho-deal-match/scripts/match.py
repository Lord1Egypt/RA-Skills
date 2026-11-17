# -*- coding: utf-8 -*-
"""
match.py — 撮合引擎

五维打分：产品分类 40 / 工艺 15 / 材料 15 / 资质 15 / 市场 10，加核验与自有加分共 100。
同时列出「缺口」——需求要 CE MDR 但供应方没有，这种信息比分数更有用。

撮合结果默认脱敏：只给主体名（非我方一律打码）、不给联系方式。
联系方式要双方都点头才交换，走 intro.py。

用法：
  python match.py run --demand D001 --user U001
  python match.py run --capability C001 --user U001
  python match.py run --all --user U001 --min-score 50
  python match.py list --user U001
  python match.py show --match M001 --user U001
"""
import argparse
import os
import re
import sys
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import core  # noqa: E402
import init_db  # noqa: E402
import taxonomy  # noqa: E402

W_CAT, W_PROCESS, W_MATERIAL, W_CERT, W_MARKET = 40, 15, 15, 15, 10
BONUS_VERIFIED, BONUS_SELF = 3, 2


def split(s):
    return {x.strip() for x in (s or "").split("/") if x.strip()}


def _hits(a, b, per, cap, label):
    """两个集合的交集打分"""
    inter = a & b
    if not inter:
        return 0, ""
    s = min(per * len(inter), cap)
    return s, f"{label} +{s}：{' / '.join(sorted(inter))}"


def score_pair(d, c, pb, pc):
    """d=需求 c=能力 pb=买方主体 pc=卖方主体"""
    score = 0
    hits, gaps = [], []

    dc, cc = split(d["cat"]), split(c["cat"])
    inter = dc & cc
    if inter:
        score += W_CAT
        hits.append(f"分类契合 +{W_CAT}：{' / '.join(sorted(inter))}")
    elif dc and cc:
        gaps.append(f"分类不符：需 {'/'.join(sorted(dc))} / 供 {'/'.join(sorted(cc))}")
    elif dc or cc:
        gaps.append("分类信息不足，无法判断")

    s, t = _hits(split(d["process"]), split(c["process"]), 5, W_PROCESS, "工艺")
    score += s
    if t:
        hits.append(t)
    if split(d["process"]) and not (split(d["process"]) & split(c["process"])):
        gaps.append(f"工艺缺口：需要 {'/'.join(sorted(split(d['process'])))}")

    s, t = _hits(split(d["material"]), split(c["material"]), 6, W_MATERIAL, "材料")
    score += s
    if t:
        hits.append(t)
    if split(d["material"]) and not (split(d["material"]) & split(c["material"])):
        gaps.append(f"材料缺口：需要 {'/'.join(sorted(split(d['material'])))}")

    need_cert = split(d["cert"])
    s, t = _hits(need_cert, split(c["cert"]), 6, W_CERT, "资质")
    score += s
    if t:
        hits.append(t)
    miss = need_cert - split(c["cert"])
    if miss:
        gaps.append(f"资质缺口：对方尚无 {'/'.join(sorted(miss))}")

    # 市场：需求/能力没写市场时，用主体国别兜底（买方在哪通常就是目标市场之一）
    dmkt = split(d["market"]) or taxonomy.norm(
        pb.get("country", ""), domains=["market"]).get("market", set())
    cmkt = split(c["market"]) or taxonomy.norm(
        pc.get("country", ""), domains=["market"]).get("market", set())
    s, t = _hits(taxonomy.expand_market(dmkt), taxonomy.expand_market(cmkt),
                 5, W_MARKET, "市场")
    score += s
    if t:
        hits.append(t)

    if pc.get("verified"):
        score += BONUS_VERIFIED
        hits.append(f"卖方已核验 +{BONUS_VERIFIED}（{pc.get('expo_ref','')}）")
    if pb.get("is_self") or pc.get("is_self"):
        score += BONUS_SELF
        hits.append(f"我方主体参与 +{BONUS_SELF}")

    return min(score, 100), hits, gaps


# ---------------------------------------------------------------- 展示


def _show_party(p, mine_uid, connected):
    name = p["name"]
    if not (p.get("is_self") or connected):
        name = core.mask_company(name)
    tags = []
    if p.get("is_self"):
        tags.append("我方")
    if p.get("verified"):
        tags.append(f"已核验·{p.get('expo_ref','')}")
    country = p.get("country") or "-"
    return f"{name}（{country}）" + (f"  [{' · '.join(tags)}]" if tags else "")


def print_match(m, con, mine_uid, verbose=False):
    d = con.execute("SELECT * FROM demands WHERE id=?", (m["demand_id"],)).fetchone()
    c = con.execute("SELECT * FROM capabilities WHERE id=?", (m["capability_id"],)).fetchone()
    pb = con.execute("SELECT * FROM parties WHERE id=?", (d["party_id"],)).fetchone()
    pc = con.execute("SELECT * FROM parties WHERE id=?", (c["party_id"],)).fetchone()
    connected = m["status"] == "connected"

    flag = {"suggested": "待确认", "half": "单方已同意", "connected": "已对接",
            "declined": "已拒绝"}.get(m["status"], m["status"])
    print(f"  {m['id']}  {m['score']:>3} 分   [{flag}]")
    print(f"      需求 {d['id']} {d['title'][:26]}")
    print(f"      能力 {c['id']} {c['title'][:26]}")
    print(f"      买方 {_show_party(pb, mine_uid, connected)}")
    print(f"      卖方 {_show_party(pc, mine_uid, connected)}")
    if m["assignee"]:
        print(f"      跟进 {m['assignee']}")
    if verbose:
        for line in (m["reason"] or "").split("\n"):
            if line.strip():
                print(f"      {line}")
        acts = list(con.execute(
            "SELECT side, action, note, actor, created FROM intros "
            "WHERE match_id=? ORDER BY id LIMIT 6", (m["id"],)))
        for act in acts:
            print(f"      留痕 {act['created']}  {act['side']:<6} "
                  f"{act['action']:<8} {act['actor']}  {act['note'] or ''}")
    print()


# ---------------------------------------------------------------- 命令


def cmd_run(a):
    con = init_db.connect()

    if a.all:
        pairs = list(con.execute(
            "SELECT d.id AS did, c.id AS cid FROM demands d JOIN capabilities c "
            "WHERE d.status='open' AND c.status='open' AND d.party_id<>c.party_id "
            "AND d.visibility='public' AND c.visibility='public'"))
    elif a.demand:
        pairs = [(a.demand, r[0]) for r in con.execute(
            "SELECT id FROM capabilities WHERE status='open' "
            "AND (visibility='public' OR owner=?)", (a.user,))]
    elif a.capability:
        pairs = [(r[0], a.capability) for r in con.execute(
            "SELECT id FROM demands WHERE status='open' "
            "AND (visibility='public' OR owner=?)", (a.user,))]
    else:
        print("  请指定 --demand / --capability / --all")
        return 1

    # 先算分（不落库），按配额截断后再写库——查不到不扣费
    scored = []
    for did, cid in pairs:
        d = con.execute("SELECT * FROM demands WHERE id=?", (did,)).fetchone()
        c = con.execute("SELECT * FROM capabilities WHERE id=?", (cid,)).fetchone()
        if not d or not c:
            continue
        pb = con.execute("SELECT * FROM parties WHERE id=?", (d["party_id"],)).fetchone()
        pc = con.execute("SELECT * FROM parties WHERE id=?", (c["party_id"],)).fetchone()
        if core.is_blocked(pb["name"]) or core.is_blocked(pc["name"]):
            continue
        s, hits, gaps = score_pair(d, c, pb, pc)
        if s < a.min_score:
            continue
        scored.append((s, did, cid, hits, gaps))

    scored.sort(key=lambda x: -x[0])
    scored = scored[:a.limit]

    ok, msg, u = core.check_access(a.user, "match", len(scored))
    if not ok:
        print("  " + msg.replace("\n", "\n  "))
        core.audit_log("denied", a.user, f"撮合被拒 {msg[:50]}")
        return 1

    now = core._now()
    out = []
    for s, did, cid, hits, gaps in scored:
        exist = con.execute(
            "SELECT * FROM matches WHERE demand_id=? AND capability_id=?", (did, cid)
        ).fetchone()
        if exist:
            out.append(exist)
            continue
        n = 0
        for (mid_old,) in con.execute("SELECT id FROM matches"):
            mm = re.match(r"^M(\d+)$", mid_old or "")
            if mm:
                n = max(n, int(mm.group(1)))
        mid = f"M{n + 1:03d}"
        reason = "\n".join(["契合："] + [f"  {h}" for h in hits if h]
                           + (["缺口："] + [f"  {g}" for g in gaps] if gaps else []))
        con.execute(
            "INSERT INTO matches (id,demand_id,capability_id,score,reason,status,created,updated) "
            "VALUES (?,?,?,?,?,?,?,?)", (mid, did, cid, s, reason, "suggested", now, now))
        out.append(con.execute("SELECT * FROM matches WHERE id=?", (mid,)).fetchone())

    con.commit()
    core.audit_log("match", a.user,
                   f"{'all' if a.all else (a.demand or a.capability)} "
                   f"命中{len(out)}条 min={a.min_score}",
                   refs=[m["id"] for m in out], cost=len(out))
    print("=" * 78)
    print(f"  撮合结果  {len(out)} 条（得分 ≥ {a.min_score}）")
    print("=" * 78)
    print()
    if not out:
        print("  没有匹配的组合。可以：")
        print("    · 降低门槛 --min-score 30")
        print("    · 检查需求/能力的描述是否触发了词典（--cat 等字段可手动指定）")
        con.close()
        return 0
    for m in out:
        print_match(m, con, a.user, verbose=a.verbose)
    con.close()
    print("  联系方式在双方都确认意向后才会交换：")
    print(f"    python intro.py request --match {out[0]['id']} --user {a.user}")
    return 0


def cmd_leads(a):
    """从线索池里按需求找潜在对象——获客入口

    线索来自展会公开名录，只有公司信息，没有个人联系方式。
    看中某家后要 activate 补录联系方式，才能进入撮合。
    """
    con = init_db.connect()

    d = None
    if a.demand:
        d = con.execute("SELECT * FROM demands WHERE id=?", (a.demand,)).fetchone()
        if not d:
            print(f"  未找到需求 {a.demand}")
            return 1
        dcat, dmat, dproc = split(d["cat"]), split(d["material"]), split(d["process"])
    else:
        if not a.kw:
            print("  请指定 --demand 或 --kw")
            return 1
        n = taxonomy.norm(a.kw)
        dcat = n.get("cat", set())
        dmat = n.get("material", set())
        dproc = n.get("process", set())

    leads = list(con.execute(
        "SELECT * FROM parties WHERE status='lead' AND name<>''"))
    if not leads:
        print("  线索池是空的。先从展会名录导入：")
        print("    python import_expo.py --kw spine --limit 50 --user " + a.user)
        con.close()
        return 0

    scored = []
    for p in leads:
        if core.is_blocked(p["name"]):
            continue
        ln = taxonomy.norm(f"{p['note'] or ''} {p['name']}")
        lcat, lmat = ln.get("cat", set()), ln.get("material", set())
        s, why = 0, []
        inter = dcat & lcat
        if inter:
            s += 50
            why.append(f"{' / '.join(sorted(inter))}")
        elif a.require_cat:
            continue
        m = dmat & lmat
        if m:
            s += 20
            why.append(f"材料 {'/'.join(sorted(m))}")
        pr = dproc & ln.get("process", set())
        if pr:
            s += 20
            why.append(f"工艺 {'/'.join(sorted(pr))}")
        if p.get("verified"):
            s += 10
        if s < a.min_score:
            continue
        scored.append((s, p, why, ln))

    scored.sort(key=lambda x: -x[0])
    scored = scored[:a.limit]

    ok, msg, u = core.check_access(a.user, "match", len(scored))
    if not ok:
        print("  " + msg.replace("\n", "\n  "))
        con.close()
        return 1
    core.audit_log("leads", a.user,
                   f"{a.demand or a.kw} 命中{len(scored)}条线索",
                   refs=[p["id"] for _, p, _, _ in scored], cost=len(scored))
    con.close()

    src = f"需求 {a.demand}" if a.demand else f"关键词 {a.kw}"
    print("=" * 78)
    print(f"  线索匹配  {src}   命中 {len(scored)} 条")
    print("=" * 78)
    print()
    if not scored:
        print("  线索池里没有匹配的。可以：")
        print(f"    python import_expo.py --kw {a.kw or 'spine'} --limit 100 --user {a.user}")
        return 0
    for s, p, why, ln in scored:
        print(f"  {p['id']}  {s:>3} 分   {p['name'][:38]}")
        print(f"        {p.get('country') or '-':<10}"
              f"{(p.get('expo_ref') or '无出处'):<14}{(p.get('note') or '')[:34]}")
        if why:
            print(f"        匹配：{' · '.join(why)}")
        print(f"        激活：python publish.py activate --lead {p['id']} "
              f"--person 姓名 --email 邮箱 --user {a.user}")
        print()
    print("  线索只有公司信息，无个人联系方式——这是刻意的。")
    print("  确认对方愿意被接触后再激活，激活后才进入撮合。")
    return 0


def cmd_list(a):
    con = init_db.connect()
    where, args = core.scope_where(a.user)
    rows = list(con.execute(
        "SELECT * FROM matches m WHERE " + where + " ORDER BY "
        "CASE status WHEN 'half' THEN 0 WHEN 'suggested' THEN 1 WHEN 'connected' THEN 2 ELSE 3 END, "
        "score DESC", args))
    print("=" * 78)
    print(f"  撮合记录  {len(rows)} 条"
          + ("（全库）" if core.is_owner(a.user) else "（仅我参与的单）"))
    print("=" * 78)
    print()
    if not rows:
        print("  （空）先跑 python match.py run --all --user " + a.user)
        con.close()
        return 0
    for m in rows:
        print_match(m, con, a.user, verbose=a.verbose)
    con.close()
    return 0


def cmd_show(a):
    con = init_db.connect()
    ok, msg = core.can_access_match(con, a.user, a.match)
    if not ok:
        print("  访问被拒：" + msg)
        core.audit_log("denied", a.user, f"越权查看撮合 {a.match}")
        con.close()
        return 1
    m = con.execute("SELECT * FROM matches WHERE id=?", (a.match,)).fetchone()
    if not m:
        print(f"  未找到撮合 {a.match}")
        return 1
    print("=" * 78)
    print(f"  撮合详情 {m['id']}" + (f"   跟进人 {m['assignee']}" if m["assignee"] else ""))
    print("=" * 78)
    print()
    print_match(m, con, a.user, verbose=True)
    con.close()
    return 0


def main():
    ap = argparse.ArgumentParser(description="撮合引擎")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("run", help="跑撮合")
    p.add_argument("--demand"), p.add_argument("--capability")
    p.add_argument("--all", action="store_true", help="全池撮合")
    p.add_argument("--min-score", type=int, default=40)
    p.add_argument("--limit", type=int, default=15)
    p.add_argument("--verbose", action="store_true", help="显示打分依据与缺口")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("leads", help="从线索池找潜在对象（获客入口）")
    p.add_argument("--demand", help="按某条需求找")
    p.add_argument("--kw", help="或直接给关键词，如 'PEEK spine'")
    p.add_argument("--min-score", type=int, default=30)
    p.add_argument("--limit", type=int, default=10)
    p.add_argument("--require-cat", action="store_true", help="分类不符的直接跳过")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_leads)

    p = sub.add_parser("list", help="查看已有撮合")
    p.add_argument("--verbose", action="store_true")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("show", help="查看单条撮合详情")
    p.add_argument("--match", required=True)
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_show)

    a = ap.parse_args()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
