#!/usr/bin/env python3
"""octo-mention 人工纠错工具

当模型分析结果有误时，通过本工具进行人工修正。修正自动标记 source:"manual" + locked:true，
后续自动分析不会覆盖被锁定的条目。

操作:
  --show             查看某人当前所有别名+锁定状态
  --add-alias        添加正确别名（自动锁定）
  --remove-alias     删除错误别名
  --move-alias       将别名从一个人转移到另一个人
  --set-name         修正 canonical_name
  --lock-alias       锁定别名（防止自动覆盖）
  --unlock-alias     解锁别名（允许自动分析更新）
  --reject-alias     拒绝词（标记永不识别为该人别名）

用法:
  python3 correct.py --db openclaw.json --uid <uid> --show
  python3 correct.py --db openclaw.json --uid <uid> --add-alias 老李 --conf 1.0 --reason "手动确认"
  python3 correct.py --db openclaw.json --uid <uid> --remove-alias 旭哥
  python3 correct.py --db openclaw.json --move-alias 逸飞 --from <uid_a> --to <uid_b> --reason "绑错人"
  python3 correct.py --db openclaw.json --uid <uid> --set-name 李明
  python3 correct.py --db openclaw.json --uid <uid> --lock-alias 老李
  python3 correct.py --db openclaw.json --uid <uid> --unlock-alias 老李
  python3 correct.py --db openclaw.json --uid <uid> --reject-alias 老板 --reason "通用称呼不应绑定"
"""
import argparse, json, os, sys
from datetime import datetime, timezone, timedelta

CN_TZ = timezone(timedelta(hours=8))


def now_iso():
    return datetime.now(CN_TZ).isoformat(timespec="seconds")


def load_db(path):
    if not os.path.exists(path) or os.path.getsize(path) == 0:
        print(f"错误: 数据库文件不存在或为空: {path}", file=sys.stderr)
        sys.exit(1)
    return json.load(open(path, encoding="utf-8"))


def save_db(db, path):
    db["version"] = db.get("version", 0) + 1
    db["last_updated"] = now_iso()
    os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
    json.dump(db, open(path, "w", encoding="utf-8"), ensure_ascii=False, indent=2)


def get_person(db, uid):
    p = db.get("persons", {}).get(uid)
    if not p:
        print(f"错误: 未找到 uid={uid}", file=sys.stderr)
        sys.exit(1)
    return p


def find_alias_in_list(al_list, alias_name):
    """在 alias 列表中查找指定别名，返回 (index, alias_obj) 或 (None, None)"""
    for i, a in enumerate(al_list):
        if a.get("alias") == alias_name:
            return i, a
    return None, None


def show(db, uid):
    p = get_person(db, uid)
    print(f"=== {p.get('canonical_name', '?')} [{uid}] ({p.get('member_type', '?')}) ===")
    if p.get("previous_names"):
        print(f"  曾用名: {', '.join(pn['name'] for pn in p['previous_names'])}")
    print(f"  出现群: {', '.join(p.get('seen_in_groups', []))}")
    print()
    print("  别名 (aliases):")
    for a in p.get("aliases", []):
        lock = " 🔒" if a.get("locked") else ""
        src = f" [{a['source']}]" if a.get("source") else ""
        print(f"    - {a['alias']} (conf={a.get('confidence', '?')}, type={a.get('alias_type', '?')}, "
              f"ev={a.get('evidence_count', '?')}, groups={a.get('groups', [])}){lock}{src}")
    if p.get("uncertain_aliases"):
        print("  不确定别名 (uncertain):")
        for a in p["uncertain_aliases"]:
            lock = " 🔒" if a.get("locked") else ""
            print(f"    - {a['alias']} (conf={a.get('confidence', '?')}){lock}")
    if p.get("rejected_aliases"):
        print("  拒绝词 (rejected):")
        for r in p["rejected_aliases"]:
            print(f"    - {r['alias']} (reason={r.get('reason', '')})")
    if p.get("conflicts"):
        print("  冲突:")
        for c in p["conflicts"]:
            print(f"    - {c}")


def add_alias(db, uid, alias_name, confidence=1.0, alias_type="manual", reason=""):
    p = get_person(db, uid)
    aliases = p.setdefault("aliases", [])
    idx, existing = find_alias_in_list(aliases, alias_name)
    if existing:
        # 已存在，更新为手动锁定
        existing["confidence"] = confidence
        existing["source"] = "manual"
        existing["locked"] = True
        existing["corrected_at"] = now_iso()
        if reason:
            existing["reason"] = reason
        print(f"已更新并锁定: {alias_name} -> {p.get('canonical_name')} (conf={confidence})")
    else:
        new_alias = {
            "alias": alias_name,
            "alias_type": alias_type,
            "confidence": confidence,
            "evidence_count": 0,
            "evidence": [],
            "groups": [],
            "source": "manual",
            "locked": True,
            "corrected_at": now_iso(),
            "reason": reason or "人工添加",
        }
        aliases.append(new_alias)
        print(f"已添加并锁定: {alias_name} -> {p.get('canonical_name')} (conf={confidence})")
    # 如果在 rejected 里有同名，移除
    rejected = p.get("rejected_aliases", [])
    p["rejected_aliases"] = [r for r in rejected if r.get("alias") != alias_name]


def remove_alias(db, uid, alias_name):
    p = get_person(db, uid)
    for list_name in ("aliases", "uncertain_aliases"):
        al_list = p.get(list_name, [])
        idx, existing = find_alias_in_list(al_list, alias_name)
        if existing is not None:
            al_list.pop(idx)
            print(f"已从 {list_name} 删除: {alias_name} (原属于 {p.get('canonical_name')})")
            return
    print(f"未找到别名 '{alias_name}' 在 uid={uid} 的记录中", file=sys.stderr)
    sys.exit(1)


def move_alias(db, from_uid, to_uid, alias_name, reason=""):
    from_p = get_person(db, from_uid)
    to_p = get_person(db, to_uid)

    # 从源头找到并移除
    moved = None
    for list_name in ("aliases", "uncertain_aliases"):
        al_list = from_p.get(list_name, [])
        idx, existing = find_alias_in_list(al_list, alias_name)
        if existing is not None:
            moved = al_list.pop(idx)
            break

    if not moved:
        print(f"错误: 未在 {from_uid} ({from_p.get('canonical_name')}) 中找到别名 '{alias_name}'",
              file=sys.stderr)
        sys.exit(1)

    # 加到目标，标记为手动锁定
    moved["source"] = "manual"
    moved["locked"] = True
    moved["corrected_at"] = now_iso()
    moved["reason"] = reason or f"从 {from_p.get('canonical_name')} 转移"

    to_aliases = to_p.setdefault("aliases", [])
    _, existing_in_target = find_alias_in_list(to_aliases, alias_name)
    if existing_in_target:
        # 目标已有同名别名，合并证据
        existing_in_target.update({
            "source": "manual", "locked": True,
            "corrected_at": now_iso(),
            "confidence": max(existing_in_target.get("confidence", 0), moved.get("confidence", 0)),
            "reason": reason or f"从 {from_p.get('canonical_name')} 转移并合并",
        })
        print(f"已转移并合并: {alias_name}: {from_p.get('canonical_name')} -> {to_p.get('canonical_name')}")
    else:
        to_aliases.append(moved)
        print(f"已转移: {alias_name}: {from_p.get('canonical_name')} -> {to_p.get('canonical_name')}")


def set_name(db, uid, new_name):
    p = get_person(db, uid)
    old_name = p.get("canonical_name")
    if old_name and old_name != new_name:
        prev = p.setdefault("previous_names", [])
        if not any(pn.get("name") == old_name for pn in prev):
            prev.append({"name": old_name, "corrected_at": now_iso()})
    p["canonical_name"] = new_name
    p.setdefault("manual_corrections", []).append({
        "field": "canonical_name", "old": old_name, "new": new_name, "at": now_iso()
    })
    print(f"已修正标准名: {old_name} -> {new_name} [{uid}]")


def lock_alias(db, uid, alias_name):
    p = get_person(db, uid)
    for list_name in ("aliases", "uncertain_aliases"):
        _, existing = find_alias_in_list(p.get(list_name, []), alias_name)
        if existing:
            existing["locked"] = True
            existing["source"] = existing.get("source") or "manual"
            existing["corrected_at"] = now_iso()
            print(f"已锁定: {alias_name} ({p.get('canonical_name')}) 🔒")
            return
    print(f"未找到别名 '{alias_name}' 在 uid={uid} 的记录中", file=sys.stderr)
    sys.exit(1)


def unlock_alias(db, uid, alias_name):
    p = get_person(db, uid)
    for list_name in ("aliases", "uncertain_aliases"):
        _, existing = find_alias_in_list(p.get(list_name, []), alias_name)
        if existing:
            existing["locked"] = False
            existing["corrected_at"] = now_iso()
            print(f"已解锁: {alias_name} ({p.get('canonical_name')}) 🔓")
            return
    print(f"未找到别名 '{alias_name}' 在 uid={uid} 的记录中", file=sys.stderr)
    sys.exit(1)


def reject_alias(db, uid, alias_name, reason=""):
    p = get_person(db, uid)
    # 从现有别名里移除（如果存在）
    for list_name in ("aliases", "uncertain_aliases"):
        al_list = p.get(list_name, [])
        idx, _ = find_alias_in_list(al_list, alias_name)
        if idx is not None:
            al_list.pop(idx)

    # 加入拒绝列表
    rejected = p.setdefault("rejected_aliases", [])
    if not any(r.get("alias") == alias_name for r in rejected):
        rejected.append({
            "alias": alias_name,
            "source": "manual",
            "rejected_at": now_iso(),
            "reason": reason or "人工标记为不应绑定",
        })
    print(f"已拒绝: {alias_name} 不再识别为 {p.get('canonical_name')} 的别名")


def main():
    ap = argparse.ArgumentParser(description="octo-mention 人工纠错工具")
    ap.add_argument("--db", required=True, help="映射数据库路径")
    ap.add_argument("--uid", help="目标 uid")
    ap.add_argument("--show", action="store_true", help="查看某人所有别名")
    ap.add_argument("--add-alias", metavar="ALIAS", help="添加别名")
    ap.add_argument("--remove-alias", metavar="ALIAS", help="删除别名")
    ap.add_argument("--move-alias", metavar="ALIAS", help="转移别名")
    ap.add_argument("--set-name", metavar="NAME", help="修正标准名")
    ap.add_argument("--lock-alias", metavar="ALIAS", help="锁定别名")
    ap.add_argument("--unlock-alias", metavar="ALIAS", help="解锁别名")
    ap.add_argument("--reject-alias", metavar="ALIAS", help="拒绝词")
    ap.add_argument("--conf", type=float, default=1.0, help="置信度 (默认 1.0)")
    ap.add_argument("--alias-type", default="manual", help="别名类型 (默认 manual)")
    ap.add_argument("--reason", default="", help="修正原因")
    ap.add_argument("--from", dest="from_uid", help="转移来源 uid (配合 --move-alias)")
    ap.add_argument("--to", dest="to_uid", help="转移目标 uid (配合 --move-alias)")

    args = ap.parse_args()
    db = load_db(args.db)

    if args.show:
        if not args.uid:
            print("--show 需要 --uid", file=sys.stderr); sys.exit(1)
        show(db, args.uid)
        return

    if args.add_alias:
        if not args.uid:
            print("--add-alias 需要 --uid", file=sys.stderr); sys.exit(1)
        add_alias(db, args.uid, args.add_alias, args.conf, args.alias_type, args.reason)
        save_db(db, args.db)
    elif args.remove_alias:
        if not args.uid:
            print("--remove-alias 需要 --uid", file=sys.stderr); sys.exit(1)
        remove_alias(db, args.uid, args.remove_alias)
        save_db(db, args.db)
    elif args.move_alias:
        if not args.from_uid or not args.to_uid:
            print("--move-alias 需要 --from 和 --to", file=sys.stderr); sys.exit(1)
        move_alias(db, args.from_uid, args.to_uid, args.move_alias, args.reason)
        save_db(db, args.db)
    elif args.set_name:
        if not args.uid:
            print("--set-name 需要 --uid", file=sys.stderr); sys.exit(1)
        set_name(db, args.uid, args.set_name)
        save_db(db, args.db)
    elif args.lock_alias:
        if not args.uid:
            print("--lock-alias 需要 --uid", file=sys.stderr); sys.exit(1)
        lock_alias(db, args.uid, args.lock_alias)
        save_db(db, args.db)
    elif args.unlock_alias:
        if not args.uid:
            print("--unlock-alias 需要 --uid", file=sys.stderr); sys.exit(1)
        unlock_alias(db, args.uid, args.unlock_alias)
        save_db(db, args.db)
    elif args.reject_alias:
        if not args.uid:
            print("--reject-alias 需要 --uid", file=sys.stderr); sys.exit(1)
        reject_alias(db, args.uid, args.reject_alias, args.reason)
        save_db(db, args.db)
    else:
        ap.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
