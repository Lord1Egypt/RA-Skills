# -*- coding: utf-8 -*-
"""
gate.py — 骨科展会名录查询的准入闸门

四道闸：
  闸一 实名登记   查询者必须留下姓名/公司/职务/联系方式/用途，否则一条都不给
  闸二 反骚扰承诺 逐条确认"五不一必须"，承诺 90 天有效，过期重签
  闸三 配额限速   L1 每日 30 条 / L2 每日 10 条；展开明文 3 倍计价
  闸四 审计留痕   每条查询进哈希链日志，被投诉可追溯到人，篡改即断链

用法：
  python gate.py register --name 张三 --company 某某医疗 --title 国际业务 \
                          --contact 本人邮箱 --purpose 寻找欧洲OEM代工伙伴
  python gate.py pledge --user U001 --yes
  python gate.py whoami --user U001
  python gate.py quota --user U001
  python gate.py block --company "Acme Corp" --reason "电话中明确拒绝，勿再联系"
  python gate.py unblock --company "Acme Corp"
  python gate.py blocklist
  python gate.py audit --verify
  python gate.py audit --tail 20
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
REG_FILE = os.path.join(SKILL_DIR, "registry", "users.jsonl")
AUDIT_FILE = os.path.join(SKILL_DIR, "audit", "audit.log")
BLOCK_FILE = os.path.join(SKILL_DIR, "registry", "blocklist.jsonl")

PLEDGE_DAYS = 90          # 承诺有效期
QUOTA_L1 = 30             # L1 公开级 每日条数
QUOTA_L2 = 10             # L2 受限级 每日条数
REVEAL_COST = 3           # 展开明文的价格倍数

PLEDGE_ITEMS = [
    "我不会群发邮件、批量拨号或以任何方式轰炸式联系对方",
    "我只把这些信息用于与骨科医疗器械相关的正当商务沟通",
    "我不会转售、外传、公开张贴或把这些名录导入任何营销群发系统",
    "联系时我会表明真实身份、真实公司与真实来意，不伪造身份",
    "对方一旦表示不感兴趣或要求停止，我立即停止且不再通过其他渠道联系",
    "我会在每次沟通中留下自己的真实联系方式，方便对方回绝或投诉",
]

# ---------------------------------------------------------------- 存储工具

def _ensure():
    for p in (REG_FILE, AUDIT_FILE, BLOCK_FILE):
        os.makedirs(os.path.dirname(p), exist_ok=True)
        if not os.path.exists(p):
            open(p, "a", encoding="utf-8").close()


def _load_jsonl(path):
    if not os.path.exists(path):
        return []
    out = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    out.append(json.loads(line))
                except json.JSONDecodeError:
                    pass
    return out


def _append_jsonl(path, obj):
    _ensure()
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")


def _now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------- 哈希链审计

def _last_hash():
    if not os.path.exists(AUDIT_FILE):
        return "0" * 64
    last = ""
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                last = line.strip()
    if not last:
        return "0" * 64
    try:
        return json.loads(last).get("hash", "0" * 64)
    except json.JSONDecodeError:
        return "0" * 64


def audit_log(action, user="", detail="", ids=None, cost=0):
    """写一条审计记录，prev_hash + hash 形成防篡改链"""
    _ensure()
    prev = _last_hash()
    payload = {
        "ts": _now(),
        "action": action,
        "user": user,
        "detail": detail,
        "ids": ids or [],
        "cost": cost,
        "prev": prev,
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True)
    h = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    payload["hash"] = h
    with open(AUDIT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=False) + "\n")
    return h


def audit_verify():
    """校验审计链：任何一条被删改都会断链"""
    prev = "0" * 64
    n = 0
    with open(AUDIT_FILE, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
            except json.JSONDecodeError:
                print(f"  [!] 第 {i} 行不是合法 JSON，链已损坏")
                return False
            stored = rec.pop("hash", "")
            raw = json.dumps(rec, ensure_ascii=False, sort_keys=True)
            calc = hashlib.sha256(raw.encode("utf-8")).hexdigest()
            if calc != stored:
                print(f"  [!] 第 {i} 行内容被篡改（重算哈希不匹配）")
                return False
            if rec.get("prev") != prev:
                print(f"  [!] 第 {i} 行前向哈希对不上，中间有记录被删除")
                return False
            prev = stored
            n += 1
    print(f"  审计链完整：{n} 条记录，哈希全部校验通过")
    return True


# ---------------------------------------------------------------- 用户与配额

def _next_uid():
    users = _load_jsonl(REG_FILE)
    mx = 0
    for u in users:
        m = re.match(r"U(\d+)", u.get("uid", ""))
        if m:
            mx = max(mx, int(m.group(1)))
    return f"U{mx + 1:03d}"


def find_user(uid):
    for u in _load_jsonl(REG_FILE):
        if u.get("uid") == uid:
            return u
    return None


def quota_used(uid, tier):
    """今日该用户在某级别上已消耗的配额点数（按实际返回条数累计，reveal 三倍）"""
    today = datetime.now().strftime("%Y-%m-%d")
    return sum(
        r.get("cost", 0) for r in _load_jsonl(AUDIT_FILE)
        if r.get("user") == uid and r.get("action") == "query"
        and r.get("ts", "").startswith(today)
        and r.get("detail", "").find(f"tier={tier}") >= 0
    )


def check_identity(uid):
    """闸一（实名登记） + 闸二（反骚扰承诺），返回 (ok, msg, user)"""
    u = find_user(uid)
    if not u:
        return False, (
            f"未登记用户 {uid}。请先登记：\n"
            "  python gate.py register --name 姓名 --company 公司 --title 职务 \\\n"
            "                          --contact 邮箱或手机 --purpose 查询用途"
        ), None

    # 闸二：承诺有效期
    pledged = u.get("pledged_at", "")
    if not pledged:
        return False, "尚未签署反骚扰承诺，请先运行：python gate.py pledge --user " + uid, u
    try:
        pa = datetime.strptime(pledged, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return False, "承诺记录时间格式异常，请重新签署", u
    if datetime.now() - pa > timedelta(days=PLEDGE_DAYS):
        return False, (f"承诺已超过 {PLEDGE_DAYS} 天（签署于 {pledged}），请重新签署："
                       f"python gate.py pledge --user {uid} --yes"), u
    return True, "", u


def check_quota(uid, tier, cost):
    """闸三：配额限速。返回 (ok, msg)"""
    limit = QUOTA_L2 if tier == "L2" else QUOTA_L1
    used = quota_used(uid, tier)
    if used + cost > limit:
        return False, (
            f"今日 {tier} 配额不足：已用 {used} / 上限 {limit}，本次需要 {cost}。"
            f"配额每日 0 点重置。这是为了防止批量抓取与群发。"
        )
    return True, ""


# ---------------------------------------------------------------- 拒访名单

def is_blocked(company_norm):
    for b in _load_jsonl(BLOCK_FILE):
        if b.get("company_norm") == company_norm and not b.get("unblocked"):
            return b
    return None


def norm_key(name):
    s = re.sub(r"[^\w\s]", " ", str(name or "").lower())
    s = re.sub(r"\b(inc|llc|ltd|limited|corp|corporation|co|company|gmbh|ag|sa|srl|bv|nv|ab|plc|pte|pty)\b", " ", s)
    return re.sub(r"\s+", "", s).strip()


# ---------------------------------------------------------------- 命令

def cmd_register(a):
    _ensure()
    if not all([a.name, a.company, a.contact]):
        print("  [x] --name / --company / --contact 为必填（必须留下真实联系方式才能查询）")
        return 1
    if "@" not in a.contact and not re.search(r"\d{7,}", a.contact):
        print("  [x] --contact 必须是有效邮箱或手机号，否则对方无法回绝或投诉")
        return 1
    users = _load_jsonl(REG_FILE)
    for u in users:
        if u.get("contact") == a.contact:
            print(f"  该联系方式已登记过：{u['uid']}（{u['name']} / {u['company']}）")
            return 0
    uid = _next_uid()
    rec = {
        "uid": uid, "name": a.name, "company": a.company, "title": a.title,
        "contact": a.contact, "purpose": a.purpose,
        "registered_at": _now(), "pledged_at": "",
    }
    _append_jsonl(REG_FILE, rec)
    audit_log("register", uid, f"{a.name} / {a.company} / {a.contact}")
    print("=" * 66)
    print(f"  登记成功  用户编号：{uid}")
    print("=" * 66)
    print(f"  姓名  {a.name}   公司  {a.company}   职务  {a.title or '-'}")
    print(f"  联系方式  {a.contact}")
    print(f"  用途  {a.purpose or '-'}")
    print(f"\n  下一步必须签署反骚扰承诺后才能查询：")
    print(f"    python gate.py pledge --user {uid} --yes")
    return 0


def cmd_pledge(a):
    _ensure()
    u = find_user(a.user)
    if not u:
        print(f"  [x] 用户 {a.user} 不存在")
        return 1
    print("=" * 66)
    print("  反骚扰使用承诺 —— 请逐条确认")
    print("=" * 66)
    for i, t in enumerate(PLEDGE_ITEMS, 1):
        print(f"   {i}. {t}")
    print("=" * 66)
    if not a.yes:
        ans = input("\n  以上六条是否全部接受？(y/N) ").strip().lower()
        if ans != "y":
            print("  已取消。未签署承诺不能查询。")
            return 1
    # 更新 pledged_at
    users = _load_jsonl(REG_FILE)
    with open(REG_FILE, "w", encoding="utf-8") as f:
        for x in users:
            if x.get("uid") == a.user:
                x["pledged_at"] = _now()
                x["pledge_version"] = "v1"
            f.write(json.dumps(x, ensure_ascii=False) + "\n")
    audit_log("pledge", a.user, "签署反骚扰承诺 v1")
    print(f"\n  承诺已签署（{_now()}），有效期 {PLEDGE_DAYS} 天。")
    print(f"  配额：L1 公开级 {QUOTA_L1} 条/日，L2 受限级 {QUOTA_L2} 条/日。")
    print(f"  现在可以查询：python query.py --user {a.user} --kw 关键词")
    return 0


def cmd_whoami(a):
    u = find_user(a.user)
    if not u:
        print(f"  [x] 用户 {a.user} 不存在")
        return 1
    print(f"  用户 {u['uid']}  {u['name']} / {u['company']} / {u.get('title') or '-'}")
    print(f"  联系方式 {u['contact']}")
    print(f"  登记时间 {u.get('registered_at')}   承诺 {'已签 ' + u['pledged_at'] if u.get('pledged_at') else '未签'}")
    return 0


def cmd_quota(a):
    for tier, limit in (("L1", QUOTA_L1), ("L2", QUOTA_L2)):
        used = quota_used(a.user, tier)
        left = max(0, limit - used)
        bar = "#" * int(used / limit * 20) + "." * (20 - int(used / limit * 20))
        print(f"  {tier}: {used:>3} / {limit:<3} [{bar}]  剩余 {left}")
    return 0


def cmd_block(a):
    key = norm_key(a.company)
    for b in _load_jsonl(BLOCK_FILE):
        if b.get("company_norm") == key and not b.get("unblocked"):
            print(f"  已在拒访名单中：{b['company']}（{b.get('ts')}，{b.get('reason')}）")
            return 0
    _append_jsonl(BLOCK_FILE, {
        "company": a.company, "company_norm": key,
        "reason": a.reason, "by": a.by, "ts": _now(), "unblocked": False,
    })
    audit_log("block", a.by, f"加入拒访名单 {a.company}：{a.reason}")
    print(f"  已加入拒访名单：{a.company}")
    print("  此后任何人查询该主体都会被拦截并提示原因。")
    return 0


def cmd_unblock(a):
    key = norm_key(a.company)
    rows = _load_jsonl(BLOCK_FILE)
    hit = False
    with open(BLOCK_FILE, "w", encoding="utf-8") as f:
        for b in rows:
            if b.get("company_norm") == key:
                b["unblocked"] = True
                b["unblocked_at"] = _now()
                hit = True
            f.write(json.dumps(b, ensure_ascii=False) + "\n")
    if hit:
        audit_log("unblock", a.by, f"移出拒访名单 {a.company}")
        print(f"  已移出拒访名单：{a.company}")
    else:
        print("  未在名单中找到该主体")
    return 0


def cmd_blocklist(a):
    rows = [b for b in _load_jsonl(BLOCK_FILE) if not b.get("unblocked")]
    if not rows:
        print("  拒访名单为空")
        return 0
    print(f"  拒访名单（{len(rows)} 条）—— 这些主体已表示拒绝，禁止再联系：")
    for b in rows:
        print(f"   - {b['company']}  |  {b.get('ts')}  |  {b.get('reason')}")
    return 0


def cmd_audit(a):
    _ensure()
    if a.verify:
        return 0 if audit_verify() else 1
    rows = _load_jsonl(AUDIT_FILE)
    for r in rows[-a.tail:]:
        ids = r.get("ids") or []
        extra = f"  命中{len(ids)}条" if ids else ""
        print(f"  {r.get('ts')}  {r.get('action'):<10} {r.get('user'):<6} {r.get('detail')}{extra}")
    print(f"\n  共 {len(rows)} 条审计记录（哈希链防篡改）")
    return 0


def main():
    ap = argparse.ArgumentParser(description="骨科展会名录查询准入闸门")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("register", help="实名登记")
    p.add_argument("--name", required=True)
    p.add_argument("--company", required=True)
    p.add_argument("--title", default="")
    p.add_argument("--contact", required=True, help="邮箱或手机，对方可据此回绝/投诉")
    p.add_argument("--purpose", default="")
    p.set_defaults(func=cmd_register)

    p = sub.add_parser("pledge", help="签署反骚扰承诺")
    p.add_argument("--user", required=True)
    p.add_argument("--yes", action="store_true")
    p.set_defaults(func=cmd_pledge)

    p = sub.add_parser("whoami")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_whoami)

    p = sub.add_parser("quota")
    p.add_argument("--user", required=True)
    p.set_defaults(func=cmd_quota)

    p = sub.add_parser("block", help="加入拒访名单")
    p.add_argument("--company", required=True)
    p.add_argument("--reason", required=True)
    p.add_argument("--by", default="owner")
    p.set_defaults(func=cmd_block)

    p = sub.add_parser("unblock")
    p.add_argument("--company", required=True)
    p.add_argument("--by", default="owner")
    p.set_defaults(func=cmd_unblock)

    p = sub.add_parser("blocklist")
    p.set_defaults(func=cmd_blocklist)

    p = sub.add_parser("audit")
    p.add_argument("--verify", action="store_true")
    p.add_argument("--tail", type=int, default=20)
    p.set_defaults(func=cmd_audit)

    a = ap.parse_args()
    _ensure()
    return a.func(a)


if __name__ == "__main__":
    sys.exit(main())
