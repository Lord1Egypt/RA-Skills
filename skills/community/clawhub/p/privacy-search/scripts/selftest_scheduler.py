#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
定时 selftest + 引擎失效告警（V1.6 新增）

功能：定期（每日/每小时）自动执行 selftest，发现引擎失效时主动告警。
目标：引擎失效 T+1 发现（不再依赖用户手动跑 --selftest）。

遵循死规则 13：不生成 __pycache__。
遵循死规则 10：定时任务需控制资源占用，不影响用户电脑。

配置（config.yaml）：
  selftest_schedule:
    enabled: true
    interval: daily       # daily / hourly
    alert_channel: log    # log / webhook / both
    webhook_url: ""       # 企业微信/webhook 地址
    notify_on: failure    # all / failure（failure = 只在异常时通知）
"""

import asyncio
import json
import os
import sys
import time
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional

sys.dont_write_bytecode = True

try:
    from version_util import get_current_version
except ImportError:
    from .version_util import get_current_version


# ============================================================
# 告警通道
# ============================================================

def _alert_to_log(message: str, details: Optional[Dict[str, Any]] = None) -> None:
    """写入日志文件"""
    log_path = os.path.expanduser("~/.workbuddy/output/privacy-search-selftest.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
        if details:
            if "report" in details:
                for entry in details["report"]:
                    status = "✓" if entry.get("ok") else "✗"
                    f.write(f"  {status} {entry.get('engine', '?')}: "
                            f"{entry.get('count', 0)}条 | "
                            f"{entry.get('diagnosis', 'unknown')}\n")
            if "failed" in details and details["failed"]:
                f.write(f"  失效引擎: {', '.join(details['failed'])}\n")


def _alert_to_webhook(message: str, webhook_url: str, details: Optional[Dict[str, Any]] = None) -> bool:
    """
    发送 webhook 告警（企业微信/钉钉格式）

    纯 urllib 实现，不依赖第三方库。
    """
    if not webhook_url:
        return False
    payload = {
        "msgtype": "text",
        "text": {
            "content": message,
        },
    }
    try:
        import urllib.request
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            webhook_url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except Exception:
        return False


# ============================================================
# 定时调度器
# ============================================================

class SelftestScheduler:
    """
    定时 selftest 调度器

    资源控制：
      - 单次 selftest 并发不超过 3（避免高频外网请求）
      - 检测完成后释放连接资源
      - 通过 asyncio.run 隔离每次任务，避免长时间占用
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        sched_cfg = config.get("selftest_schedule", {}) or {}
        self.enabled = sched_cfg.get("enabled", True)
        self.interval = sched_cfg.get("interval", "daily")
        self.alert_channel = sched_cfg.get("alert_channel", "log")
        self.webhook_url = sched_cfg.get("webhook_url", "")
        self.notify_on = sched_cfg.get("notify_on", "failure")

    def _build_orchestrator(self):
        """构建 SearchOrchestrator 实例"""
        try:
            from search import SearchOrchestrator
        except ImportError:
            from .search import SearchOrchestrator
        return SearchOrchestrator(self.config)

    async def _run_selftest(self) -> Dict[str, Any]:
        """执行一次 selftest 并返回报告"""
        orchestrator = self._build_orchestrator()
        report = await orchestrator.selftest()
        failed = [e for e in report if not e.get("ok")]
        return {
            "report": report,
            "total": len(report),
            "ok_count": len(report) - len(failed),
            "failed_count": len(failed),
            "failed": [e.get("engine", "?") for e in failed],
            "timestamp": datetime.now().isoformat(),
        }

    def _format_alert_message(self, result: Dict[str, Any]) -> str:
        """格式化告警消息"""
        if result["failed_count"] == 0:
            return (
                f"🔒 隐私搜索 selftest 完成\n"
                f"版本: v{get_current_version()}\n"
                f"时间: {result['timestamp']}\n"
                f"引擎状态: {result['ok_count']}/{result['total']} 正常"
            )
        failed_list = ", ".join(result["failed"])
        return (
            f"⚠️ 隐私搜索引擎告警\n"
            f"版本: v{get_current_version()}\n"
            f"时间: {result['timestamp']}\n"
            f"可用引擎: {result['ok_count']}/{result['total']}\n"
            f"失效引擎: {failed_list}\n"
            f"建议: 执行 --selftest 查看详情，或更新到最新版本"
        )

    def run_once(self) -> Dict[str, Any]:
        """
        执行一次 selftest 并发送告警（如果满足条件）

        Returns:
            selftest 报告字典
        """
        if not self.enabled:
            return {"enabled": False}

        result = asyncio.run(self._run_selftest())

        # 判断是否需要告警
        should_alert = (
            self.notify_on == "all" or
            (self.notify_on == "failure" and result["failed_count"] > 0)
        )

        if should_alert:
            message = self._format_alert_message(result)
            details = {"report": result["report"], "failed": result["failed"]}

            if self.alert_channel in ("log", "both"):
                _alert_to_log(message, details)
            if self.alert_channel in ("webhook", "both"):
                _alert_to_webhook(message, self.webhook_url, details)

        return result

    def run_loop(self) -> None:
        """
        阻塞式定时循环（用于独立进程或定时任务触发）

        生产环境推荐用系统 cron / Task Scheduler 触发 run_once()，
        本方法仅用于「用户主动跑 --selftest-schedule start」的场景。
        """
        if not self.enabled:
            print("selftest 调度已禁用")
            return

        interval_seconds = 3600 if self.interval == "hourly" else 86400
        print(f"selftest 调度已启动（间隔: {self.interval}）")
        while True:
            try:
                result = self.run_once()
                print(f"[{datetime.now().strftime('%H:%M:%S')}] "
                      f"selftest 完成: {result.get('ok_count', '?')}/{result.get('total', '?')} 正常")
            except Exception as e:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] selftest 异常: {e}")
            time.sleep(interval_seconds)


# ============================================================
# CLI 入口
# ============================================================

def main():
    import argparse

    parser = argparse.ArgumentParser(description="定时 selftest 调度（V1.6 新增）")
    parser.add_argument("action", choices=["run", "status"], help="run=执行一次, status=查看上次结果")
    parser.add_argument("--config", help="配置文件路径")
    args = parser.parse_args()

    # 加载配置
    from search import load_config
    config = load_config(args.config)

    scheduler = SelftestScheduler(config)

    if args.action == "run":
        result = scheduler.run_once()
        if not result.get("enabled"):
            print("selftest 调度已禁用")
            return
        print(f"selftest 完成: {result['ok_count']}/{result['total']} 引擎正常")
        if result["failed"]:
            print(f"失效引擎: {', '.join(result['failed'])}")
        else:
            print("所有引擎正常")

    elif args.action == "status":
        # 读取上次日志
        log_path = os.path.expanduser("~/.workbuddy/output/privacy-search-selftest.log")
        if not os.path.exists(log_path):
            print("尚未执行过 selftest")
            return
        with open(log_path, "r", encoding="utf-8") as f:
            lines = f.readlines()
        # 显示最后 20 行
        for line in lines[-20:]:
            print(line.rstrip())


if __name__ == "__main__":
    main()
