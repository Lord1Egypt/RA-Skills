# -*- coding: utf-8 -*-
"""
query.py — 骨科展会名录查询（过闸后可用）

未登记 / 未签承诺 / 配额用尽 → 一条都不返回。
默认掩码输出，--reveal 才展开明文，且展开按 3 倍配额计价并重点留痕。

用法：
  python query.py --user U001 --kw spine
  python query.py --user U001 --country Germany --tier L1
  python query.py --user U001 --kw "Zimmer" --reveal
  python query.py --user U001 --source "OMTEC 2025" --kw "engineer" --limit 10
  python query.py --user U001 --has-email --country USA

参数：
  --kw        关键词，匹配公司/人名/职务/产品/国家/城市/展位
  --source    按展会过滤，如 "AAOS 2026" "OMTEC 2025" "DKOU 2026"
  --country   按国家过滤
  --tier      L1 公开级（默认）/ L2 受限级（个人参会者）
  --has-email 只看有邮箱的
  --has-phone 只看有电话的
  --limit     本次最多返回，默认 20，上限 20
  --reveal    展开明文联系方式（按 3 倍配额计价）
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
import gate  # noqa: E402

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(SKILL_DIR, "data", "contacts.db")
MAX_LIMIT = 20
COLLIDE_DAYS = 30


# ---------------------------------------------------------------- 中英别名

# 源表国家字段中英混排（"德国" 108 条 / "Germany" 29 条），不做别名映射会漏掉大半
COUNTRY_ALIASES = {
    "德国": ["德国", "germany", "de"],
    "美国": ["美国", "usa", "u.s.", "united states", "us"],
    "中国": ["中国", "china", "cn", "中国大陆", "中国台湾", "中国香港"],
    "瑞士": ["瑞士", "switzerland", "swiss"],
    "英国": ["英国", "uk", "u.k.", "united kingdom", "england"],
    "法国": ["法国", "france"],
    "意大利": ["意大利", "italy", "italia"],
    "日本": ["日本", "japan"],
    "韩国": ["韩国", "korea", "south korea"],
    "印度": ["印度", "india"],
    "加拿大": ["加拿大", "canada"],
    "瑞典": ["瑞典", "sweden"],
    "荷兰": ["荷兰", "netherlands", "holland"],
    "西班牙": ["西班牙", "spain"],
    "奥地利": ["奥地利", "austria"],
    "澳大利亚": ["澳大利亚", "australia"],
    "巴西": ["巴西", "brazil"],
    "土耳其": ["土耳其", "turkey"],
    "以色列": ["以色列", "israel"],
    "丹麦": ["丹麦", "denmark"],
    "比利时": ["比利时", "belgium"],
    "芬兰": ["芬兰", "finland"],
    "挪威": ["挪威", "norway"],
    "波兰": ["波兰", "poland"],
    "新加坡": ["新加坡", "singapore"],
}

# 骨科品类关键词中英互译 —— 产品分类同样是中英混排
KEYWORD_ALIASES = {
    "spine": ["脊柱", "脊椎"], "脊柱": ["spine", "spinal"],
    "trauma": ["创伤"], "创伤": ["trauma"],
    "joint": ["关节"], "关节": ["joint", "arthro"],
    "knee": ["膝"], "膝": ["knee"],
    "hip": ["髋"], "髋": ["hip"],
    "shoulder": ["肩"], "肩": ["shouder", "shoulder"],
    "screw": ["螺钉", "螺丝"], "螺钉": ["screw"],
    "plate": ["接骨板", "钢板"], "接骨板": ["plate"],
    "nail": ["髓内钉"], "髓内钉": ["nail"],
    "implant": ["植入物", "植入"], "植入物": ["implant"],
    "oem": ["代工", "贴牌"], "代工": ["oem", "odm"],
    "cmf": ["颌面", "颅颌面"], "颌面": ["cmf"],
    "sports": ["运动医学"], "运动医学": ["sports medicine", "sports"],
    "biologics": ["生物制品", "生物材料"], "生物制品": ["biologics"],
    "instrument": ["器械", "工具"], "器械": ["instrument"],
    "3d": ["3d打印", "增材"], "3d打印": ["3d"],
}


def expand_terms(value, table):
    """把用户输入的词展开成同义中英候选列表"""
    v = (value or "").strip()
    if not v:
        return [v]
    low = v.lower()
    out = {v}
    for canon, aliases in table.items():
        pool = [canon] + aliases
        if any(low == p.lower() or low in p.lower() or p.lower() in low
               for p in pool if len(p) >= 2):
            out.update(pool)
    return list(out)


# ---------------------------------------------------------------- 脱敏

def mask_email(e):
    if not e or "@" not in e:
        return e or ""
    u, _, d = e.partition("@")
    return (u[:1] + "***@" + d) if u else "***@" + d


def mask_phone(p):
    if not p:
        return ""
    digits = re.sub(r"\D", "", p)
    if len(digits) < 7:
        return "***"
    return digits[:3] + "****" + digits[-4:]


def mask_person(n):
    if not n:
        return ""
    parts = n.split()
    if len(parts) >= 2:
        return parts[0] + " " + parts[-1][0] + "."
    return n[:1] + "***"


# ---------------------------------------------------------------- 撞车检测

def collide_map():
    """过去 COLLIDE_DAYS 天里，哪些公司被谁查过 —— 用于避免同重复打扰同一家"""
    cutoff = datetime.now() - timedelta(days=COLLIDE_DAYS)
    ids = {}
    for r in gate._load_jsonl(gate.AUDIT_FILE):
        if r.get("action") != "query":
            continue
        try:
            ts = datetime.strptime(r.get("ts", ""), "%Y-%m-%d %H:%M:%S")
        except ValueError:
            continue
        if ts < cutoff:
            continue
        for i in (r.get("ids") or []):
            ids.setdefault(i, set()).add((r.get("user", "?"), r.get("ts", "")[:10]))
    if not ids:
        return {}
    con = sqlite3.connect(DB_PATH)
    q = "SELECT id, company_norm FROM contacts WHERE id IN (%s)" % ",".join("?" * len(ids))
    out = {}
    for cid, cnorm in con.execute(q, list(ids.keys())):
        if cnorm:
            out.setdefault(cnorm, set()).update(ids[cid])
    con.close()
    return out


# ---------------------------------------------------------------- 查询

def build_sql(a):
    where, args = [], []
    if a.kw:
        for token in re.split(r"[,\s]+", a.kw.strip()):
            if not token:
                continue
            # 关键词中英展开：用户输入 spine 时同时匹配"脊柱"
            syns = expand_terms(token, KEYWORD_ALIASES)
            ors, oargs = [], []
            for s in syns:
                ors.append(
                    "(company LIKE ? OR person LIKE ? OR title LIKE ? OR category LIKE ? "
                    "OR country LIKE ? OR city LIKE ? OR booth LIKE ? OR website LIKE ?)")
                oargs += [f"%{s}%"] * 8
            where.append("(" + " OR ".join(ors) + ")")
            args += oargs
    if a.source:
        where.append("source LIKE ?")
        args.append(f"%{a.source}%")
    if a.country:
        syns = expand_terms(a.country, COUNTRY_ALIASES)
        where.append("(" + " OR ".join(["country LIKE ?"] * len(syns)) + ")")
        args += [f"%{s}%" for s in syns]
    if a.has_email:
        where.append("email <> ''")
    if a.has_phone:
        where.append("phone <> ''")
    where.append("tier = ?")
    args.append(a.tier)
    sql = "SELECT * FROM contacts"
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY (CASE WHEN email<>'' THEN 0 ELSE 1 END), company LIMIT ?"
    args.append(a.limit)
    return sql, args


def main():
    ap = argparse.ArgumentParser(description="骨科展会名录查询")
    ap.add_argument("--user", required=True)
    ap.add_argument("--kw", default="")
    ap.add_argument("--source", default="")
    ap.add_argument("--country", default="")
    ap.add_argument("--tier", default="L1", choices=["L1", "L2"])
    ap.add_argument("--has-email", action="store_true")
    ap.add_argument("--has-phone", action="store_true")
    ap.add_argument("--limit", type=int, default=20)
    ap.add_argument("--reveal", action="store_true")
    a = ap.parse_args()

    if not os.path.exists(DB_PATH):
        print("  [x] 索引尚未构建，请先运行：python build_index.py")
        return 1
    if a.limit > MAX_LIMIT:
        print(f"  [x] 单次最多返回 {MAX_LIMIT} 条。这是刻意的限制：本工具不支持批量导出。")
        return 1

    # 闸一 + 闸二：实名登记与反骚扰承诺
    ok, msg, u = gate.check_identity(a.user)
    if not ok:
        print("  " + "=" * 64)
        print("  访问被拒绝")
        print("  " + "=" * 64)
        print("  " + msg.replace("\n", "\n  "))
        gate.audit_log("denied", a.user, f"tier={a.tier} 原因={msg[:60]}")
        return 1

    con = sqlite3.connect(DB_PATH)
    con.row_factory = sqlite3.Row
    sql, args = build_sql(a)
    rows = [dict(r) for r in con.execute(sql, args)]
    con.close()

    # 闸三：按实际命中条数计费，展开明文三倍 —— 拿不到结果就不扣费
    cost = len(rows) * (gate.REVEAL_COST if a.reveal else 1)
    ok, msg = gate.check_quota(a.user, a.tier, cost)
    if not ok:
        print("  " + "=" * 64)
        print("  访问被拒绝")
        print("  " + "=" * 64)
        print("  " + msg.replace("\n", "\n  "))
        gate.audit_log("denied", a.user, f"tier={a.tier} 原因={msg[:60]}")
        return 1

    cond = f"kw={a.kw or '*'} source={a.source or '*'} country={a.country or '*'} tier={a.tier} reveal={int(a.reveal)}"
    gate.audit_log("query", a.user, cond, ids=[r["id"] for r in rows], cost=cost)

    print("  " + "=" * 78)
    print(f"  查询人 {u['name']} / {u['company']}（{a.user}）   条件：{cond}")
    print("  " + "=" * 78)

    if not rows:
        print("  没有匹配的记录。可放宽关键词，或换 --tier / --source 试试。")
        return 0

    collide = collide_map()
    blocked_hit = 0

    for i, r in enumerate(rows, 1):
        cnorm = r["company_norm"] or ""
        blk = gate.is_blocked(cnorm)
        if blk:
            blocked_hit += 1
            print(f"\n  [{i}] {r['company'] or '(无名)'}   [{r['source']} · {r['tier']}]")
            print(f"      [已屏蔽] 该主体在拒访名单中：{blk.get('reason')}（{blk.get('ts')}）")
            print("      依据对方意愿，不再展示其联系方式。")
            continue

        print(f"\n  [{i}] {r['company'] or '(无名)'}   [{r['source']} · {r['tier']}]")
        bits = []
        if r["category"]:
            bits.append("产品: " + r["category"][:60])
        if r["country"] or r["city"]:
            bits.append("地区: " + " ".join(x for x in [r["country"], r["city"]] if x))
        if r["booth"]:
            bits.append("展位: " + r["booth"])
        for b in bits:
            print(f"      {b}")

        person = r["person"]
        if person:
            shown = person if a.reveal else mask_person(person)
            if r["title"]:
                shown += f"（{r['title']}）"
            print(f"      联系人: {shown}")

        if r["website"]:
            print(f"      官网: {r['website']}")

        em = r["email"]
        ph = r["phone"]
        if a.reveal:
            if em:
                print(f"      邮箱: {em}")
            if ph:
                print(f"      电话: {ph}")
            if not em and not ph:
                print("      邮箱/电话: 源表未提供（可走官网联系）")
        else:
            if em:
                print(f"      邮箱: {mask_email(em)}   [掩码]")
            if ph:
                print(f"      电话: {mask_phone(ph)}   [掩码]")
            if (em or ph) and not a.reveal:
                print("      完整联系方式需 --reveal 展开（按 3 倍配额计价并留痕）")

        hits = collide.get(cnorm)
        if hits:
            others = {x for x in hits if x[0] != a.user}
            if others:
                who = "、".join(f"{x[0]}({x[1]})" for x in sorted(others))
                print(f"      [提醒] 该主体近期已被 {who} 查询过，请先内部确认，避免重复打扰")

    print("\n  " + "=" * 78)
    print(f"  返回 {len(rows)} 条" + (f"，其中 {blocked_hit} 条因拒访名单被屏蔽" if blocked_hit else ""))
    left = (gate.QUOTA_L2 if a.tier == "L2" else gate.QUOTA_L1) - gate.quota_used(a.user, a.tier)
    print(f"  本次扣 {cost} 点配额，今日 {a.tier} 剩余 {max(0, left)} 点")
    if not a.reveal:
        print("  当前为掩码模式。加 --reveal 展开完整联系方式。")
    print("  使用约束：仅限正当商务沟通 · 禁止群发轰炸 · 遭拒即停 · 每次沟通须留己方联系方式")
    print("  " + "=" * 78)
    return 0


if __name__ == "__main__":
    sys.exit(main())
