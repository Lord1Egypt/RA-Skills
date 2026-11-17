# -*- coding: utf-8 -*-
"""
core.py — 骨科供需撮合的准入与留痕基础设施

三道闸：
  闸一 实名登记   发布和撮合都必须实名，本人联系方式必填
  闸二 承诺确认   七条撮合守则逐条确认，90 天重签
  闸三 配额限速   撮合/交换/发布分别限速，防止批量刷取

审计：
  所有动作进 SHA-256 哈希链（前一条哈希嵌进后一条），篡改即断链。
  撮合场景里这是关键——谁在什么时间接触了谁，事后必须能说清楚。

用法：
  python core.py register --name 张三 --company 某某医疗 --title 国际业务 \
                          --contact 本人邮箱 --purpose 找欧洲代工
  python core.py pledge --user U001 --yes
  python core.py whoami --user U001
  python core.py quota --user U001
  python core.py role --user U002 --set owner    # owner 才能改角色
  python core.py block --company "Acme Corp" --reason "明确拒绝，勿再联系"
  python core.py unblock --company "Acme Corp"
  python core.py blocklist
  python core.py audit --tail 20
  python core.py audit --verify

角色：
  owner   全库视野：能看到并操作所有撮合、所有主体的联系方式（中间人角色）
  member  只能查看/操作「自己的单」：自己发布的任一侧、分派给自己的撮合、
          自己在留痕里操作过的单。其他单连存在都看不到。
"""
import argparse
import hashlib
import json
import os
import re
import sys
from datetime import datetime, timedelta

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SKILL_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(SKILL_DIR, "data")
REG_FILE = os.path.join(SKILL_DIR, "registry", "users.jsonl")
BLOCK_FILE = os.path.join(SKILL_DIR, "registry", "blocklist.jsonl")
AUDIT_FILE = os.path.join(SKILL_DIR, "audit", "audit.log")
DB_PATH = os.path.join(DATA_DIR, "match.db")

PLEDGE_DAYS = 90
QUOTA_MATCH = 40     # 每日可查看撮合候选条数
QUOTA_REVEAL = 8     # 每日可交换联系方式次数（最敏感，最严）
QUOTA_PUBLISH = 20   # 每日可发布需求/能力条数

PLEDGE_ITEMS = [
    "我发布的需求或能力真实准确，不虚构需求试探行情、不夸大产能资质",
    "我只通过本撮合台接触对方，不绕过流程私下找上门",
    "对方明确拒绝或长时间未回应后，我不再重复接触、不换渠道纠缠",
    "我不会把撮合得到的联系方式转售、外传、公开张贴或导入群发系统",
    "每次沟通我都表明真实身份、真实公司与真实来意，并留下可回拨的联系方式",
    "涉及图纸、报价、工艺参数等机密信息，我先签 NDA 再交换，不口头套取",
    "我理解撮合全程留痕、可追溯到我个人，接受据此追责",
]

# ---------------------------------------------------------------- 存储工具


def _ensure():
    for p in (REG_FILE, AUDIT_FILE, BLOCK_FILE):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            open(p, "a", encoding="utf-8").close()
    os.makedirs(DATA_DIR, exist_ok=True)


def _load_jsonl(path):
    if not os.path.exists(path):
        return []
    out = []
    for line in open(path, encoding="utf-8"):
        line = line.strip()
        if line:
            try:
                out.append(json.loads(line))
            except (ValueError, TypeError):
                pass  # 跳过无法解析的行，不影响其余审计记录读取
    return out


def _append_jsonl(path, obj):
    _ensure()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------- 审计链


def _last_hash():
    rows = _load_jsonl(AUDIT_FILE)
    return rows[-1]["hash"] if rows else "0" * 64


def audit_log(action, user="", detail="", refs=None, cost=0):
    """写一条审计记录。prev_hash + 内容 -> 本条 hash，形成防篡改链。"""
    _ensure()
    prev = _last_hash()
    payload = {
        "ts": _now(),
        "action": action,
        "user": user,
        "detail": detail,
        "refs": refs or [],
        "cost": cost,
        "prev": prev,
    }
    body = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    payload["hash"] = hashlib.sha256(body.encode("utf-8")).hexdigest()
    _append_jsonl(AUDIT_FILE, payload)
    return payload["hash"]


def audit_verify():
    rows = _load_jsonl(AUDIT_FILE)
    prev = "0" * 64
    for i, r in enumerate(rows, 1):
        body = {k: v for k, v in r.items() if k != "hash"}
        expect = hashlib.sha256(
            json.dumps(body, ensure_ascii=False, sort_keys=True).encode("utf-8")
        ).hexdigest()
        if r.get("prev") != prev:
            return False, f"第 {i} 条断链：prev_hash 与上一条不匹配（记录被删除或插入）"
        if r.get("hash") != expect:
            return False, f"第 {i} 条内容被篡改（哈希值与内容不符）"
        prev = r["hash"]
    return True, f"校验通过，共 {len(rows)} 条记录，链完整"


# ---------------------------------------------------------------- 用户


def find_user(uid):
    for r in _load_jsonl(REG_FILE):
        if r.get("uid") == uid:
            return r
    return None


def next_uid():
    rows = _load_jsonl(REG_FILE)
    n = 0
    for r in rows:
        m = re.match(r"U(\d+)$", r.get("uid", ""))
        if m:
            n = max(n, int(m.group(1)))
    return f"U{n + 1:03d}"


def cmd_register(a):
    for key, label in (("name", "姓名"), ("company", "公司"),
                       ("title", "职务"), ("contact", "本人联系方式"),
                       ("purpose", "用途")):
        if not getattr(a, key, "").strip():
            print(f"  缺少必填项：{label}（--{key}）")
            print("  撮合台的原则：对方要能找到你、回绝你、投诉你，所以联系方式不能省。")
            return 1
    uid = next_uid()
    # 第一个登记的人是 owner（中间人），之后都是 member（业务同事）
    existing = _load_jsonl(REG_FILE)
    role = "owner" if not existing else "member"
    rec = {
        "uid": uid,
        "name": a.name.strip(),
        "company": a.company.strip(),
        "title": a.title.strip(),
        "contact": a.contact.strip(),
        "purpose": a.purpose.strip(),
        "role": role,
        "registered": _now(),
        "pledged": "",
    }
    _append_jsonl(REG_FILE, rec)
    audit_log("register", uid, f"{a.company} / {a.purpose} role={role}")
    print("=" * 68)
    print(f"  登记成功  编号 {uid}   角色 {role}")
    print("=" * 68)
    print(f"  姓名     {rec['name']}")
    print(f"  公司     {rec['company']}")
    print(f"  职务     {rec['title']}")
    print(f"  联系方式 {rec['contact']}")
    print(f"  用途     {rec['purpose']}")
    if role == "owner":
        print("  角色     owner（首位登记者）：全库视野，负责撮合与分派")
    else:
        print("  角色     member：只能查看与操作自己参与的单")
        print("           需要全库视野请 owner 授权：")
        print(f"           python core.py role --user {uid} --set owner --by <owner编号>")
    print()
    print("  下一步：签署撮合守则")
    print(f"    python core.py pledge --user {uid} --yes")
    return 0


def cmd_pledge(a):
    u = find_user(a.user)
    if not u:
        print(f"  未找到用户 {a.user}，请先登记：python core.py register --help")
        return 1
    if not a.yes:
        print("=" * 68)
        print("  骨科供需撮合守则")
        print("=" * 68)
        for i, it in enumerate(PLEDGE_ITEMS, 1):
            print(f"  {i}. {it}")
        print()
        print(f"  确认请加 --yes：python core.py pledge --user {a.user} --yes")
        return 0
    rows = _load_jsonl(REG_FILE)
    for r in rows:
        if r.get("uid") == a.user:
            r["pledged"] = _now()
    with open(REG_FILE, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    audit_log("pledge", a.user, f"{len(PLEDGE_ITEMS)} 条守则已确认")
    print(f"  {a.user} 已签署撮合守则，有效期 {PLEDGE_DAYS} 天（至 "
          f"{(datetime.now() + timedelta(days=PLEDGE_DAYS)).strftime('%Y-%m-%d')}）")
    return 0


def cmd_role(a):
    """查看/调整成员角色。调整仅 owner 可操作（--by 传 owner 编号）。"""
    op = find_user(a.user)
    if not op:
        print(f"  未找到用户 {a.user}")
        return 1
    if a.set is None:
        print(f"  {op['uid']} {op['name']} 角色：{op.get('role', 'member')}")
        print("  调整（仅 owner）：python core.py role --user <编号> --set owner|member --by <owner编号>")
        return 0
    if not is_owner(a.by):
        print(f"  只有 owner 能调整角色（--by 请传 owner 编号）。")
        audit_log("denied", a.by, f"越权尝试调整 {a.user} 角色 -> {a.set}")
        return 1
    if a.set not in ("owner", "member"):
        print("  角色只能是 owner 或 member")
        return 1
    rows = _load_jsonl(REG_FILE)
    for r in rows:
        if r.get("uid") == a.user:
            r["role"] = a.set
    with open(REG_FILE, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    audit_log("role_change", a.by, f"{a.user} -> {a.set}")
    print(f"  {a.user} 角色已改为 {a.set}")
    return 0


def is_owner(uid):
    u = find_user(uid)
    return bool(u) and u.get("role", "member") == "owner"


# ---------------------------------------------------------------- 数据可见域


def can_access_match(con, uid, mid):
    """member 的可见域：自己发布的任一侧 / 分派给自己的 / 自己留痕操作过的。

    owner 全库可见。返回 (ok, msg)。
    """
    if is_owner(uid):
        return True, ""
    u = find_user(uid)
    if not u:
        return False, "未登记用户"
    own = con.execute(
        "SELECT 1 FROM matches m "
        "JOIN demands d ON d.id=m.demand_id "
        "JOIN capabilities c ON c.id=m.capability_id "
        "WHERE m.id=? AND (d.owner=? OR c.owner=?)", (mid, uid, uid)).fetchone()
    if own:
        return True, ""
    part = con.execute(
        "SELECT 1 FROM matches WHERE id=? AND assignee=?", (mid, uid)).fetchone()
    if part:
        return True, ""
    acted = con.execute(
        "SELECT 1 FROM intros WHERE match_id=? AND actor=?", (mid, uid)).fetchone()
    if acted:
        return True, ""
    return False, (f"该撮合与 {uid} 无关。member 只能访问自己参与的单"
                   "（自己发布的、分派给自己的、自己操作过的）。"
                   f"需要全库视野请 owner 授权：python core.py role --user {uid} --set owner --by <owner编号>；"
                   f"或由 owner 分派：python intro.py assign --match {mid} --to {uid} --by <owner编号>")


def scope_where(uid):
    """给 matches 查询加可见域过滤，返回 (sql 片段, 参数)。owner 返回恒真。"""
    if is_owner(uid):
        return "1=1", []
    sql = ("(m.id IN (SELECT m2.id FROM matches m2 "
           "JOIN demands d2 ON d2.id=m2.demand_id "
           "JOIN capabilities c2 ON c2.id=m2.capability_id "
           "WHERE d2.owner=? OR c2.owner=?) "
           "OR m.assignee=? "
           "OR m.id IN (SELECT match_id FROM intros WHERE actor=?))")
    return sql, [uid, uid, uid, uid]


# ---------------------------------------------------------------- 配额


def used_today(uid, action):
    """按 action 前缀统计今日消耗。

    publish_party / publish_demand / publish_capability 都算进 publish 配额。
    """
    today = datetime.now().strftime("%Y-%m-%d")
    return sum(
        int(r.get("cost") or 0)
        for r in _load_jsonl(AUDIT_FILE)
        if r.get("user") == uid and r.get("action", "").startswith(action)
        and r.get("ts", "").startswith(today)
    )


def check_access(uid, action, need=1):
    """闸一 + 闸二 + 闸三。action ∈ {match, reveal, publish}"""
    u = find_user(uid)
    if not u:
        return False, ("尚未登记。撮合台不对匿名用户开放：\n"
                       "    python core.py register --name 姓名 --company 公司 "
                       "--title 职务 --contact 你的邮箱 --purpose 用途"), u

    pledged = u.get("pledged", "")
    if not pledged:
        return False, (f"尚未签署撮合守则：\n"
                       f"    python core.py pledge --user {uid}\n"
                       f"    先不加 --yes 可以看条款全文"), u
    try:
        pa = datetime.strptime(pledged, "%Y-%m-%d %H:%M:%S")
    except (ValueError, TypeError):
        pa = datetime.min  # 时间戳格式异常按最旧处理，触发重新签署
    if datetime.now() - pa > timedelta(days=PLEDGE_DAYS):
        return False, (f"守则签署已超过 {PLEDGE_DAYS} 天（签署于 {pledged}），请重新签署：\n"
                       f"    python core.py pledge --user {uid} --yes"), u

    limit = {"match": QUOTA_MATCH, "reveal": QUOTA_REVEAL, "publish": QUOTA_PUBLISH}.get(action)
    if limit is not None:
        used = used_today(uid, action)
        if used + need > limit:
            return False, (f"今日 {action} 配额不足：已用 {used} / 上限 {limit}，本次需要 {need}。\n"
                           f"    配额每日 0 点重置。限速是为了防止批量抓取与群发。"), u
    return True, "", u


# ---------------------------------------------------------------- 拒访名单


def _norm_company(s):
    s = (s or "").strip().lower()
    s = re.sub(r"[\s,._\-()（）]+", "", s)
    for suf in ("inc", "ltd", "llc", "gmbh", "co", "corp", "limited", "sa", "bv",
                "有限公司", "股份", "公司", "集团"):
        if s.endswith(suf) and len(s) > len(suf) + 2:
            s = s[: -len(suf)]
    return s


def blocklist():
    return {r["key"]: r for r in _load_jsonl(BLOCK_FILE) if r.get("key")}


def is_blocked(company):
    return _norm_company(company) in blocklist()


def cmd_block(a):
    key = _norm_company(a.company)
    if not key:
        print("  请提供公司名称：--company")
        return 1
    rows = [r for r in _load_jsonl(BLOCK_FILE) if r.get("key") != key]
    rows.append({"key": key, "company": a.company.strip(), "reason": a.reason.strip(),
                 "by": a.by.strip(), "ts": _now()})
    with open(BLOCK_FILE, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    audit_log("block", a.by, f"{a.company} 原因：{a.reason}")
    print(f"  已加入拒访名单：{a.company}")
    print("  此后该主体不再出现在任何撮合结果中，任何人都无法再接触。")
    return 0


def cmd_unblock(a):
    key = _norm_company(a.company)
    rows = [r for r in _load_jsonl(BLOCK_FILE) if r.get("key") != key]
    if len(rows) == len(_load_jsonl(BLOCK_FILE)):
        print(f"  拒访名单中没有：{a.company}")
        return 1
    with open(BLOCK_FILE, "w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    audit_log("unblock", a.by, a.company)
    print(f"  已移出拒访名单：{a.company}")
    return 0


def cmd_blocklist(a):
    rows = _load_jsonl(BLOCK_FILE)
    print("=" * 68)
    print(f"  拒访名单（{len(rows)} 家）")
    print("=" * 68)
    if not rows:
        print("  （空）")
        return 0
    for r in rows:
        print(f"  {r['company']}")
        print(f"      原因 {r.get('reason','')} | {r.get('by','')} @ {r.get('ts','')}")
    return 0


# ---------------------------------------------------------------- 脱敏


def mask_email(s):
    s = (s or "").strip()
    if "@" not in s:
        return ""
    name, dom = s.rsplit("@", 1)
    n = len(name)
    keep = 1 if n <= 2 else 2
    return f"{name[:keep]}{'*' * max(n - keep, 1)}@{dom}"


def mask_phone(s):
    s = (s or "").strip()
    digits = re.sub(r"\D", "", s)
    if len(digits) < 6:
        return ""
    return f"{digits[:3]}{'*' * (len(digits) - 6)}{digits[-3:]}" if len(digits) > 6 else "*" * len(digits)


def mask_company(s):
    """公司名脱敏：保留首字母与末尾，中间打码"""
    s = (s or "").strip()
    if len(s) <= 4:
        return s
    return f"{s[:2]}{'*' * min(len(s) - 4, 8)}{s[-2:]}"


# ---------------------------------------------------------------- CLI


def main():
    ap = argparse.ArgumentParser(description="骨科供需撮合 — 准入与留痕")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("register", help="实名登记")
    p.add_argument("--name", required=True)
    p.add_argument("--company", required=True)
    p.add_argument("--title", required=True)
    p.add_argument("--contact", required=True, help="本人联系方式，对方要能找到你")
    p.add_argument("--purpose", required=True)
    p.set_defaults(func=cmd_register)

    p = sub.add_parser("pledge", help="签署撮合守则")
    p.add_argument("--user", required=True)
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_pledge)

    p = sub.add_parser("whoami", help="查看我的登记与配额")
    p.add_argument("--user", required=True)
    p.set_defaults(func=lambda a: _cmd_whoami(a))

    p = sub.add_parser("role", help="查看/调整成员角色（调整仅 owner）")
    p.add_argument("--user", help="目标成员编号")
    p.add_argument("--set", choices=["owner", "member"], default=None)
    p.add_argument("--by", default="", help="操作人编号（调整时必填且须为 owner）")
    p.set_defaults(func=cmd_role)

    p = sub.add_parser("block", help="加入拒访名单")
    p.add_argument("--company", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--by", default="owner")
    p.set_defaults(func=cmd_block)

    p = sub.add_parser("unblock", help="移出拒访名单")
    p.add_argument("--company", required=True)
    p.add_argument("--by", default="owner")
    p.set_defaults(func=cmd_unblock)

    p = sub.add_parser("blocklist", help="查看拒访名单")
    p.set_defaults(func=cmd_blocklist)

    p = sub.add_parser("audit", help="审计日志")
    p.add_argument("--tail", type=int, default=0)
    p.add_argument("--verify", action="store_true")
    p.set_defaults(func=lambda a: _cmd_audit(a))

    a = ap.parse_args()
    return a.func(a)


def _cmd_whoami(a):
    u = find_user(a.user)
    if not u:
        print(f"  未找到用户 {a.user}")
        return 1
    print("=" * 68)
    print(f"  {u['uid']}  {u['name']}  {u['company']} · {u['title']}   "
          f"角色 {u.get('role', 'member')}")
    print("=" * 68)
    print(f"  联系方式 {u['contact']}")
    print(f"  登记用途 {u['purpose']}")
    print(f"  登记时间 {u['registered']}")
    if u.get("pledged"):
        pa = datetime.strptime(u["pledged"], "%Y-%m-%d %H:%M:%S")
        left = PLEDGE_DAYS - (datetime.now() - pa).days
        print(f"  守则签署 {u['pledged']}（剩余 {max(left,0)} 天）")
    else:
        print("  守则签署 未签署")
    print()
    for act, limit in (("match", QUOTA_MATCH), ("reveal", QUOTA_REVEAL), ("publish", QUOTA_PUBLISH)):
        print(f"  今日 {act:<8} {used_today(a.user, act):>3} / {limit}")
    return 0


def _cmd_audit(a):
    if a.verify:
        ok, msg = audit_verify()
        print(("  审计链" + ("完好：" if ok else "异常：")) + msg)
        return 0 if ok else 1
    rows = _load_jsonl(AUDIT_FILE)
    for r in rows[-a.tail if a.tail else 0:]:
        print(f"  {r['ts']}  {r['action']:<10} {r['user']:<7} {r['detail']}")
    print(f"\n  共 {len(rows)} 条")
    return 0


if __name__ == "__main__":
    sys.exit(main())
