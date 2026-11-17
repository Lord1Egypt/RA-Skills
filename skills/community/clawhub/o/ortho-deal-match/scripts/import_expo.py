# -*- coding: utf-8 -*-
"""
import_expo.py — 从展会名录导入线索

只读 L1 公开级（展会官方参展商名录，展方已授权公开）。
**不导入任何个人邮箱与电话**——展方公开的是公司信息，个人联系方式不在授权范围内。

导入进来是「线索」(status=lead)，不参与撮合。
要撮合必须先 activate，即由登记人补录经过确认的联系方式。
这一步是刻意的：不能拿公开名录直接当客户名单用。

用法：
  python import_expo.py --source "AAOS 2026" --user U001
  python import_expo.py --kw spine --country 德国 --limit 50 --user U001
  python import_expo.py --dry-run --kw trauma --user U001      # 只看不导入
"""
import argparse
import os
import re
import sqlite3
import sys

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

# 只取 L1：展会官方参展商名录
ALLOWED_TIERS = ("L1",)


# 展会库国家字段里混着两字母码（US 81 条 / 美国 296 条），精确匹配才不会误伤
COUNTRY_CODE = {
    "中国": ["cn", "prc"], "美国": ["us"], "德国": ["de"], "日本": ["jp"],
    "韩国": ["kr"], "英国": ["uk"], "法国": ["fr"], "意大利": ["it"],
    "西班牙": ["es"], "印度": ["in"], "巴西": ["br"], "瑞士": ["ch"],
    "荷兰": ["nl"], "加拿大": ["ca"], "澳洲": ["au"],
    "中国香港": ["hk"], "中国台湾": ["tw"], "中国澳门": ["mo"],
}


def _usable(alias):
    """超短 ASCII 别名（us/eu/cn）不进 LIKE——'%us%' 会把 Australia 当美国"""
    if re.search(r"[\u4e00-\u9fff]", alias):
        return len(alias) >= 2
    return len(alias) >= 3


def country_variants(text):
    """返回 (like_patterns, exact_values)"""
    hits = taxonomy.norm(text, domains=["market"]).get("market", set())
    like, exact = set(), set()
    for h in hits:
        for al in taxonomy.DOMAINS["market"].get(h, []):
            al = al.strip()
            if al and _usable(al):
                like.add(al)
        exact.update(COUNTRY_CODE.get(h, []))
    exact.add(text.strip().lower())
    if not like and not exact:
        like.add(text.strip())
    return sorted(like), sorted(x for x in exact if x)


def kw_variants(text, cap=30):
    """关键词也做中英展开：'spine' 要能命中库房里写作「脊柱」的 24 条"""
    out = set()
    for dom, vals in taxonomy.norm(text).items():
        for v in vals:
            for al in taxonomy.DOMAINS[dom].get(v, []):
                al = al.strip()
                if al and _usable(al):
                    out.add(al)
    out.add(text.strip())
    return sorted(out)[:cap]


def fetch(filters):
    if not os.path.exists(EXPO_DB):
        return None
    # 只读 URI 打开兄弟技能的索引库（工程上固化只读语义）
    uri = "file:" + EXPO_DB.replace("\\", "/") + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    sql = ("SELECT company, country, city, category, website, source, booth "
           "FROM contacts WHERE tier IN ({})".format(",".join("?" * len(ALLOWED_TIERS))))
    args = list(ALLOWED_TIERS)
    if filters.get("source"):
        sql += " AND source LIKE ?"
        args.append(f"%{filters['source']}%")
    if filters.get("country"):
        like, exact = country_variants(filters["country"])
        parts = []
        for v in like:
            parts.append("country LIKE ?")
            args.append(f"%{v}%")
        for v in exact:
            parts.append("lower(country) = ?")
            args.append(v)
        if parts:
            sql += " AND (" + " OR ".join(parts) + ")"
    if filters.get("kw"):
        kws = kw_variants(filters["kw"])
        clause = "(company LIKE ? OR category LIKE ? OR website LIKE ?)"
        sql += " AND (" + " OR ".join([clause] * len(kws)) + ")"
        for k in kws:
            args += [f"%{k}%"] * 3
    sql += " ORDER BY source, company"
    if filters.get("limit"):
        sql += " LIMIT ?"
        args.append(filters["limit"])
    rows = [dict(r) for r in con.execute(sql, args)]
    con.close()
    return rows


def main():
    ap = argparse.ArgumentParser(description="从展会名录导入线索")
    ap.add_argument("--source", help="展会来源，如 'AAOS 2026'")
    ap.add_argument("--country")
    ap.add_argument("--kw", help="关键词，匹配公司名/产品分类/官网")
    ap.add_argument("--limit", type=int, default=100)
    ap.add_argument("--dry-run", action="store_true", help="只看不导入")
    ap.add_argument("--user", required=True)
    a = ap.parse_args()

    ok, msg, u = core.check_access(a.user, "publish", 1)
    if not ok:
        print("  " + msg.replace("\n", "\n  "))
        return 1

    rows = fetch({"source": a.source, "country": a.country,
                  "kw": a.kw, "limit": a.limit})
    if rows is None:
        print(f"  未找到展会名录数据库：{EXPO_DB}")
        print("  请先构建：cd ~/.workbuddy/skills/ortho-expo-contacts && "
              "python scripts/build_index.py")
        return 1
    if not rows:
        print("  没有匹配的记录。放宽条件试试（--source / --country / --kw）")
        return 0

    con = init_db.connect()
    have = {r["name_norm"] for r in con.execute("SELECT name_norm FROM parties")}
    todo = []
    for r in rows:
        if not r.get("company"):
            continue
        key = core._norm_company(r["company"])
        if not key or key in have:
            continue
        have.add(key)
        todo.append((r, key))

    print("=" * 78)
    print(f"  展会名录命中 {len(rows)} 条，去重后新增 {len(todo)} 条线索")
    print("=" * 78)
    if a.dry_run:
        for r, key in todo[:20]:
            print(f"  {r['company'][:38]:<40}{r.get('country') or '-':<8}"
                  f"{(r.get('category') or '')[:22]}")
        if len(todo) > 20:
            print(f"  ... 另有 {len(todo) - 20} 条")
        print("\n  （--dry-run 未写入。去掉该参数才真正导入）")
        con.close()
        return 0

    n = 0
    now = core._now()
    for r, key in todo:
        n += 1
        pid = f"P{int(con.execute('SELECT COUNT(*) FROM parties').fetchone()[0]) + 1:03d}"
        con.execute(
            "INSERT INTO parties (id,name,name_norm,side,country,city,person,title,email,phone,"
            "website,owner,is_self,verified,expo_ref,note,status,created) "
            "VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
            (pid, r["company"].strip(), key, "seller", r.get("country") or "",
             r.get("city") or "", "", "", "", "",
             r.get("website") or "", a.user, 0, 1, r.get("source") or "",
             (r.get("category") or "")[:80], "lead", now))
        con.commit()
    core.audit_log("import_leads", a.user,
                   f"source={a.source or '*'} country={a.country or '*'} "
                   f"kw={a.kw or '*'} 导入 {n} 条线索", cost=1)
    con.close()

    print(f"  已导入 {n} 条线索（status=lead，不参与撮合）")
    print()
    print("  这些只是线索，没有联系方式，也不会进入撮合。")
    print("  确认某家值得接触后，补录联系方式激活：")
    print("    python publish.py activate --lead P0xx --person 姓名 --email 邮箱 --user " + a.user)
    print()
    print("  按分类找线索：python match.py leads --demand D001 --user " + a.user)
    return 0


if __name__ == "__main__":
    sys.exit(main())
