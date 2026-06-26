#!/usr/bin/env python3
"""隐私数据标记系统 - CLI 工具 v2（支持 glob、审计日志）"""

import json
import os
import sys
import argparse
import fnmatch
from datetime import datetime, timezone, timedelta
from pathlib import Path

# Registry 文件位置
WORKSPACE = Path(os.environ.get("WORKSPACE", Path(__file__).parent.parent.parent))
REGISTRY_PATH = WORKSPACE / "data" / "privacy-registry.json"
AUDIT_PATH = WORKSPACE / "data" / "privacy-audit.jsonl"

VALID_LEVELS = ["owner_only", "private", "no_export", "public"]
VALID_ACTIONS = ["share", "export", "display", "internal_use"]
LEVEL_PRIORITY = {"owner_only": 4, "private": 3, "no_export": 2, "public": 1, "unmarked": 0}


def load_registry():
    """加载隐私注册表"""
    if not REGISTRY_PATH.exists():
        return {
            "version": "1.0.0",
            "updated_at": "",
            "rules": {},
            "resources": []
        }
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


def save_registry(registry):
    """保存隐私注册表"""
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    registry["updated_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
    with open(REGISTRY_PATH, "w", encoding="utf-8") as f:
        json.dump(registry, f, ensure_ascii=False, indent=2)


def audit_log(action, resource, level, result, detail=""):
    """记录审计日志"""
    AUDIT_PATH.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone(timedelta(hours=8))).isoformat(),
        "action": action,
        "resource": resource,
        "level": level,
        "result": result,
        "detail": detail
    }
    with open(AUDIT_PATH, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def match_resource(resource, registry):
    """查找资源匹配的隐私规则，支持 glob 模式"""
    matched = None
    match_priority = -1

    for r in registry["resources"]:
        path = r["path"]
        # 精确前缀匹配
        if resource.startswith(path) or path.startswith(resource):
            priority = LEVEL_PRIORITY.get(r["level"], 0)
            if priority > match_priority:
                matched = r
                match_priority = priority
        # glob 模式匹配
        elif any(c in path for c in ['*', '?', '[', ']']):
            if fnmatch.fnmatch(resource, path):
                priority = LEVEL_PRIORITY.get(r["level"], 0)
                if priority > match_priority:
                    matched = r
                    match_priority = priority

    # 检查规则类别
    if not matched:
        for rule_name, rule in registry["rules"].items():
            if rule_name in resource:
                priority = LEVEL_PRIORITY.get(rule["level"], 0)
                if priority > match_priority:
                    matched = {"path": resource, **rule}
                    match_priority = priority

    return matched


def cmd_mark(args):
    """标记资源为隐私数据"""
    registry = load_registry()

    level = args.level
    if level not in VALID_LEVELS:
        print(f"❌ 无效级别: {level}，可选: {', '.join(VALID_LEVELS)}")
        sys.exit(1)

    if args.type == "rule":
        name = args.resource
        registry["rules"][name] = {
            "level": level,
            "reason": args.reason or ""
        }
        print(f"✅ 规则已标记: {name} → {level}")
        audit_log("mark_rule", name, level, "success", args.reason or "")
    else:
        path = args.resource
        existing = [r for r in registry["resources"] if r["path"] == path]
        if existing:
            existing[0]["level"] = level
            existing[0]["reason"] = args.reason or ""
            existing[0]["marked_at"] = datetime.now(timezone(timedelta(hours=8))).isoformat()
            print(f"✅ 已更新: {path} → {level}")
            audit_log("update", path, level, "success", args.reason or "")
        else:
            registry["resources"].append({
                "path": path,
                "level": level,
                "reason": args.reason or "",
                "marked_at": datetime.now(timezone(timedelta(hours=8))).isoformat()
            })
            print(f"✅ 已标记: {path} → {level}")
            audit_log("mark", path, level, "success", args.reason or "")

    save_registry(registry)


def cmd_check(args):
    """检查资源的隐私状态"""
    registry = load_registry()
    resource = args.resource
    action = args.action

    matched = match_resource(resource, registry)

    if not matched:
        print(f"⚠️ 未标记: {resource}")
        print("建议: 默认谨慎处理，如需标记请运行 mark 命令")
        audit_log("check", resource, "unmarked", "not_found", action or "")
        sys.exit(2)

    level = matched.get("level", "unknown")
    print(f"📋 {resource}")
    print(f"   级别: {level}")
    print(f"   原因: {matched.get('reason', '无')}")

    if action:
        print(f"   操作: {action}")
        allowed = check_action_allowed(level, action)
        if allowed:
            print(f"   ✅ 允许")
            audit_log("check", resource, level, "allowed", action)
        else:
            print(f"   ❌ 禁止 — {level} 级别不允许 {action}")
            audit_log("check", resource, level, "denied", action)
            sys.exit(1)
    else:
        audit_log("check", resource, level, "info", "")


def check_action_allowed(level, action):
    """检查某个操作是否允许"""
    rules = {
        "owner_only": ["internal_use"],
        "private": ["internal_use"],
        "no_export": ["internal_use", "display"],
        "public": ["share", "export", "display", "internal_use"]
    }
    return action in rules.get(level, [])


def cmd_list(args):
    """列出所有隐私标记"""
    registry = load_registry()

    print("🔒 隐私注册表\n")

    if registry["rules"]:
        print("📌 规则:")
        for name, rule in registry["rules"].items():
            print(f"   {name}: {rule['level']} — {rule.get('reason', '')}")
        print()

    if registry["resources"]:
        print("📁 资源:")
        for r in registry["resources"]:
            if args.level and r["level"] != args.level:
                continue
            icon = {'owner_only': '🔒', 'private': '🔐', 'no_export': '🚫', 'public': '🌐'}.get(r['level'], '❓')
            print(f"   {icon} {r['path']}: {r['level']} — {r.get('reason', '')}")
    else:
        print("   (空)")


def cmd_unmark(args):
    """移除隐私标记"""
    registry = load_registry()
    resource = args.resource

    before = len(registry["resources"])
    registry["resources"] = [r for r in registry["resources"] if r["path"] != resource]
    after = len(registry["resources"])

    if before > after:
        save_registry(registry)
        print(f"✅ 已移除: {resource}")
        audit_log("unmark", resource, "", "success", "")
    else:
        print(f"⚠️ 未找到: {resource}")


def cmd_audit(args):
    """查看审计日志"""
    if not AUDIT_PATH.exists():
        print("📋 审计日志为空")
        return

    with open(AUDIT_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()

    entries = [json.loads(l) for l in lines if l.strip()]

    if args.deny_only:
        entries = [e for e in entries if e.get("result") == "denied"]

    if args.limit:
        entries = entries[-args.limit:]

    if not entries:
        print("📋 无匹配审计记录")
        return

    print(f"📋 审计日志（最近 {len(entries)} 条）\n")
    for entry in entries:
        result_icon = {"allowed": "✅", "denied": "❌", "success": "✅", "info": "ℹ️", "not_found": "⚠️", "failed": "❌"}.get(entry["result"], "❓")
        print(f"  {entry['timestamp'][:19]} | {result_icon} {entry['action']:12} | {entry['level']:12} | {entry['resource']}")


def main():
    parser = argparse.ArgumentParser(description="隐私数据标记系统 v2")
    subparsers = parser.add_subparsers(dest="command", help="子命令")

    # mark
    p_mark = subparsers.add_parser("mark", help="标记隐私资源")
    p_mark.add_argument("resource", help="资源路径（支持 glob 如 *.jpg）或规则名称")
    p_mark.add_argument("--level", "-l", required=True, choices=VALID_LEVELS, help="隐私级别")
    p_mark.add_argument("--reason", "-r", help="标记原因")
    p_mark.add_argument("--type", "-t", choices=["resource", "rule"], default="resource", help="标记类型")

    # check
    p_check = subparsers.add_parser("check", help="检查隐私状态")
    p_check.add_argument("resource", help="资源路径")
    p_check.add_argument("--action", "-a", choices=VALID_ACTIONS, help="检查操作是否允许")

    # list
    p_list = subparsers.add_parser("list", help="列出所有标记")
    p_list.add_argument("--level", "-l", choices=VALID_LEVELS, help="按级别过滤")

    # unmark
    p_unmark = subparsers.add_parser("unmark", help="移除标记")
    p_unmark.add_argument("resource", help="资源路径")

    # audit
    p_audit = subparsers.add_parser("audit", help="查看审计日志")
    p_audit.add_argument("--deny-only", "-d", action="store_true", help="仅显示被拒绝的记录")
    p_audit.add_argument("--limit", "-n", type=int, default=20, help="显示条数")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    cmds = {
        "mark": cmd_mark,
        "check": cmd_check,
        "list": cmd_list,
        "unmark": cmd_unmark,
        "audit": cmd_audit
    }
    cmds[args.command](args)


if __name__ == "__main__":
    main()
