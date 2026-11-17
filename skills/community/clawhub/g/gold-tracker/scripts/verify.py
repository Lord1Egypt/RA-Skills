#!/usr/bin/env python3
"""一键自检（P0-1 / P1-11）。

检查：配置完整性、依赖可用性、目录可写、调度是否挂载（心跳）、数据新鲜度、
通知管线可达性（不真实发送）、数据完整性。也负责初始化（取代旧 setup.py）。

用法:
    python3 scripts/verify.py init              # 初始化目录与状态文件
    python3 scripts/verify.py check [--dry-run] # 完整自检（默认）
    python3 scripts/verify.py check --fix       # 自检并尝试修复（重建归档索引）
"""

import json
import shutil
import sys

from common import paths, config, heartbeat, notify_core, timeutil

errors = []
warnings = []


def err(msg):
    errors.append(msg)
    print("  [✗] {}".format(msg))


def warn(msg):
    warnings.append(msg)
    print("  [!] {}".format(msg))


def ok(msg):
    print("  [✓] {}".format(msg))


# ---------- 检查项 ----------
def check_python():
    v = sys.version_info
    if v < (3, 8):
        err("Python {} < 3.8".format("{}.{}.{}".format(v.major, v.minor, v.micro)))
    else:
        ok("Python {}.{}.{}".format(v.major, v.minor, v.micro))


def check_config(cfg):
    if not paths.resolve("config.yaml").exists():
        err("config.yaml 不存在")
        return
    ok("config.yaml 可解析")
    # 占位符检查：提示未替换的占位值
    def _scan(node, path=""):
        if isinstance(node, dict):
            for k, v in node.items():
                _scan(v, path + "." + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                _scan(v, "{}[{}]".format(path, i))
        elif isinstance(node, str) and ("YOUR_" in node or "example.com" in node):
            warn("{} 含占位符，需替换: {}".format(path or "(root)", node))
    _scan(cfg)


def check_dirs(cfg):
    for key in ("logs", "archive", "alerts", "cache", "notifications"):
        d = paths.resolve(config.dig(cfg, "paths.{}".format(key), key))
        try:
            d.mkdir(parents=True, exist_ok=True)
            probe = d / ".write_test"
            probe.write_text("x", encoding="utf-8")
            probe.unlink()
            ok("{}/ 可写".format(config.dig(cfg, "paths.{}".format(key), key)))
        except Exception as e:
            err("{} 不可写: {}".format(key, e))


def check_scripts():
    required = ["fetch.py", "analyze_check.py", "alert_manager.py", "notify.py",
                "archive.py", "summary.py", "verify.py", "log_fetch.py"]
    for s in required:
        if (paths.ROOT / "scripts" / s).exists():
            ok("scripts/{} 存在".format(s))
        else:
            err("scripts/{} 缺失".format(s))


def check_dependencies(cfg):
    # Python 相关命令由当前解释器保证；检查通知器依赖（curl/sendmail/bash）
    deps = set()
    for n in notify_core.load_notifiers(cfg):
        cmd = n.get("command", "")
        if not cmd:
            continue
        resolved = paths.resolve(cmd)
        if resolved.exists():
            continue
        deps.add(cmd.split()[0])
    for d in sorted(deps):
        if shutil.which(d):
            ok("依赖 {} 可用".format(d))
        else:
            warn("依赖 {} 未在 PATH 中找到（若该通知器禁用可忽略）".format(d))


def check_state_freshness(cfg):
    f = paths.resolve("state.json")
    if not f.exists():
        err("state.json 不存在（运行 fetch.py 生成）")
        return
    try:
        data = json.loads(f.read_text(encoding="utf-8"))
    except Exception as e:
        err("state.json 解析失败: {}".format(e))
        return
    interval = int(config.dig(cfg, "general.expected_run_interval_minutes", 30))
    grace = int(config.dig(cfg, "general.scheduler_grace_multiplier", 3))
    lu = data.get("last_update")
    if lu:
        try:
            from datetime import datetime
            dt = datetime.fromisoformat(lu)
            age = (timeutil.now() - dt).total_seconds()
            if age > interval * 60 * grace:
                err("数据过期：state.json 最后更新于 {:.0f} 分钟前".format(age / 60))
            else:
                ok("数据新鲜（最后更新 {:.0f} 分钟前）".format(age / 60))
        except Exception:
            warn("无法解析 last_update: {}".format(lu))
    else:
        warn("state.json 缺少 last_update")


def check_scheduler(cfg):
    interval = int(config.dig(cfg, "general.expected_run_interval_minutes", 30))
    grace = int(config.dig(cfg, "general.scheduler_grace_multiplier", 3))
    limit = interval * 60 * grace
    for cmd, label in [("fetch", "数据抓取"), ("alert_detect", "提醒检测")]:
        age = heartbeat.age_seconds(cmd)
        if age is None:
            err("{} 从未运行（heartbeat 无记录）—— 可能未挂载任何调度器".format(label))
        elif age > limit:
            err("{} 已 {:.0f} 分钟未运行（超过 {:.0f} 分钟阈值）—— 提醒引擎可能未在运行".format(
                label, age / 60, limit / 60))
        else:
            ok("{} 最近运行于 {:.0f} 分钟前".format(label, age / 60))


def check_notifiers(cfg):
    notifiers = notify_core.load_notifiers(cfg)
    if not notifiers:
        warn("无启用的通知器（通知会静默；如需通知请在 config.yaml 配置 notifiers）")
        return
    for n in notifiers:
        name = n.get("name") or n.get("command")
        cmd = n.get("command", "")
        resolved = paths.resolve(cmd) if cmd else None
        if resolved is not None and resolved.exists():
            ok("通知器 {} 脚本存在".format(name))
        elif cmd and shutil.which(cmd.split()[0]):
            ok("通知器 {} 命令可用".format(name))
        else:
            err("通知器 {} 的命令不可用: {}".format(name, cmd))


def check_data_integrity(cfg):
    # 提醒 JSON 可解析 + alert_id 唯一
    alerts_dir = paths.resolve("alerts")
    if alerts_dir.exists():
        for f in sorted(alerts_dir.iterdir()):
            if f.suffix != ".json":
                continue
            try:
                data = json.loads(f.read_text(encoding="utf-8"))
                ids = [a.get("alert_id") for a in data if isinstance(a, dict)]
                if len(ids) != len(set(ids)):
                    warn("{} 存在重复 alert_id".format(f.name))
            except Exception as e:
                err("{} 解析失败: {}".format(f.name, e))
    # 归档索引可解析
    idx = paths.resolve("archive") / "index.json"
    if idx.exists():
        try:
            json.loads(idx.read_text(encoding="utf-8"))
            ok("归档索引可解析")
        except Exception as e:
            err("归档索引损坏: {}（运行 archive.py rebuild 修复）".format(e))


# ---------- 初始化 ----------
def do_init(cfg):
    for key in ("logs", "archive", "alerts", "cache", "notifications"):
        paths.resolve(config.dig(cfg, "paths.{}".format(key), key)).mkdir(parents=True, exist_ok=True)
    state_file = paths.resolve("state.json")
    if not state_file.exists():
        initial = {
            "date": timeutil.today_str(config.dig(cfg, "general.timezone", "Asia/Shanghai")),
            "current_price": 0.0, "last_price": 0.0, "change_pct": 0.0, "change_abs": 0.0,
            "price_cny_per_gram": 0.0, "usd_cny": 0.0,
            "last_update": timeutil.now_iso(config.dig(cfg, "general.timezone", "Asia/Shanghai")),
            "sources": {}, "prev_close": None, "data_stale": False,
        }
        from common import atomic
        atomic.atomic_write_json(state_file, initial)
        ok("state.json 已初始化")
    else:
        ok("state.json 已存在，跳过")
    hb = paths.resolve("cache") / "heartbeat.json"
    if not hb.exists():
        from common import atomic
        atomic.atomic_write_json(hb, {})
    print("\n初始化完成。下一步: python3 scripts/fetch.py")


def main():
    paths.ensure_env()
    args = sys.argv[1:]
    cfg = config.load()

    if args and args[0] == "init":
        do_init(cfg)
        sys.exit(0)

    print("=" * 56)
    print("黄金追踪 - 一键自检")
    print("=" * 56)

    check_python()
    check_config(cfg)
    check_dirs(cfg)
    check_scripts()
    check_dependencies(cfg)
    check_state_freshness(cfg)
    check_scheduler(cfg)
    check_notifiers(cfg)
    check_data_integrity(cfg)

    if "--fix" in args:
        print("\n尝试修复…")
        import archive
        archive.rebuild_index()
        print("  已重建归档索引")

    print()
    print("=" * 56)
    print("结果: {} 个错误, {} 个警告".format(len(errors), len(warnings)))
    print("=" * 56)
    if errors:
        print("[未通过] 请根据上述错误修复后重新运行")
        sys.exit(1)
    print("[通过] 环境自检通过")


if __name__ == "__main__":
    main()
