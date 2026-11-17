#!/usr/bin/env python3
"""唯一通知管线入口（P0-3 / P0-4 / P0-7 / P0-8）。

把「组装消息 → 去重 → 发送 → 重试 → 状态记录」收敛到 common/notify_core.py，
本脚本只做 CLI 编排。所有可变参数（通知器、收件人、超时、重试）都在 config.yaml。

用法:
    python3 scripts/notify.py send alerts [--dry-run]
    python3 scripts/notify.py send summary [--dry-run]
    python3 scripts/notify.py retry [--dry-run]
    python3 scripts/notify.py status
    python3 scripts/notify.py test [--dry-run]
"""

import sys

from common import paths, config, notify_core, heartbeat

import alert_manager
import summary


def _dry_run(args):
    return "--dry-run" in args


def _cfg():
    return config.load()


def send_alerts(cfg, dry_run=False):
    pending = alert_manager.list_pending()
    if not pending:
        print("[信息] 暂无待发送提醒")
        return 0

    sent = failed = 0
    for alert in pending:
        alert_id = alert.get("alert_id")
        msg = alert.get("message", "")
        results, any_ok = notify_core.dispatch(cfg, msg, dry_run=dry_run)
        if any_ok:
            delivered = [k for k, v in results.items() if v]
            alert_manager.mark_sent(alert_id, delivered)
            print("[成功] {} 已送达: {}".format(alert_id, ", ".join(delivered)))
            sent += 1
        else:
            alert_manager.mark_failed(alert_id, "全员发送失败")
            print("[失败] {} 发送失败，保留 pending 待下周期重试".format(alert_id))
            failed += 1

    heartbeat.record("notify_send")
    print("[完成] 成功 {} 条，失败 {} 条（失败将自动重试）".format(sent, failed))
    return 1 if failed else 0


def send_summary(cfg, dry_run=False):
    text = summary.generate_brief()
    if notify_core.is_duplicate(cfg, text):
        print("[信息] 内容与上次相同，已去重跳过")
        return 0
    results, any_ok = notify_core.dispatch(cfg, text, dry_run=dry_run)
    if any_ok:
        notify_core.record_fingerprint(cfg, text)
        print("[成功] 简报已送达")
        return 0
    print("[失败] 简报发送失败（将保留，可下周期重试）")
    return 1


def show_status():
    pending = alert_manager.list_pending()
    print("待发送(pending): {} 条".format(len(pending)))
    for a in pending:
        print("  - [{}] {}".format(a.get("alert_id"), a.get("message", "")))
        if a.get("last_error"):
            print("        上次错误: {}".format(a["last_error"]))
    active = alert_manager.get_active_alerts()
    sent = [a for a in active if a.get("status") == "sent"]
    print("已发送(sent): {} 条".format(len(sent)))


def main():
    paths.ensure_env()
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    args = sys.argv[1:]
    cfg = _cfg()

    if not cfg.get("notification", {}).get("enabled", True) and not _dry_run(args):
        print("[信息] 通知已禁用（config.notification.enabled=false）")
        sys.exit(0)

    action = args[0]
    dry_run = _dry_run(args)

    if action == "send":
        what = args[1] if len(args) > 1 and not args[1].startswith("--") else "alerts"
        if what == "summary":
            code = send_summary(cfg, dry_run)
        else:
            code = send_alerts(cfg, dry_run)
        sys.exit(code)

    elif action == "retry":
        sys.exit(send_alerts(cfg, dry_run))

    elif action == "status":
        show_status()

    elif action == "test":
        msg = "[gold-tracker 测试消息] 通知管线连通性自检"
        results, any_ok = notify_core.dispatch(cfg, msg, dry_run=dry_run)
        print("[测试] 各通知器结果: {}".format(results))
        print("[测试] 至少一个成功: {}".format(any_ok))
        sys.exit(0 if any_ok else 1)

    else:
        print("未知操作: {}".format(action))
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
