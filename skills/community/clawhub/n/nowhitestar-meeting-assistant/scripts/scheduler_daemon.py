#!/usr/bin/env python3
"""
事件驱动的会议提醒调度器（替代每分钟 cron 轮询）。

工作原理：
- 由 LaunchAgent 启动并保活，常驻后台
- 读 ~/.config/meeting-assistant/schedule.json，把所有未来事件挂到内部堆
- 主循环 wait 到"下一个事件时间"再唤醒，CPU 占用 0
- 收到 SIGHUP 时重新加载 schedule.json（schedule 命令写完文件后发送）
- 事件触发时 fork 子进程跑 notify.py / meeting_daemon.py，daemon 不阻塞

支持的事件 kind：
  remind        会议前 5 分钟系统通知
  ask_record    会议开始时询问是否录制
  ask_stop      录制超时后询问是否停止录制
"""

import heapq
import json
import os
import signal
import subprocess
import sys
import threading
from datetime import datetime
from pathlib import Path

CONFIG_DIR = Path.home() / ".config" / "meeting-assistant"
SCHEDULE_PATH = CONFIG_DIR / "schedule.json"
PID_PATH = CONFIG_DIR / ".scheduler.pid"
LOG_PATH = CONFIG_DIR / "scheduler.log"
SCRIPT_DIR = Path(__file__).resolve().parent


def log(msg):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)


def parse_iso(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


class Scheduler:
    def __init__(self):
        self.heap = []          # [(epoch, seq, event_dict)]
        self.seq = 0
        self.lock = threading.Lock()
        self.wake = threading.Event()
        self.stopping = False

    def load(self):
        """从 schedule.json 重建事件堆。"""
        with self.lock:
            self.heap = []
            self.seq = 0
            if not SCHEDULE_PATH.exists():
                log("schedule.json 不存在，事件队列为空")
                return
            try:
                with open(SCHEDULE_PATH) as f:
                    data = json.load(f)
            except Exception as e:
                log(f"读取 schedule.json 失败: {e}")
                return

            now = datetime.now().timestamp()
            for ev in data.get("events", []):
                try:
                    at = parse_iso(ev["at"]).timestamp()
                except Exception as e:
                    log(f"跳过非法事件: {ev} ({e})")
                    continue
                if at + 15 < now:  # 15秒宽容（重载调度需要时间）
                    log(f"跳过已过期事件: {ev.get('kind')} @ {ev.get('at')}")
                    continue
                self.seq += 1
                heapq.heappush(self.heap, (at, self.seq, ev))
            log(f"已加载 {len(self.heap)} 个事件")

    def add_runtime(self, ev):
        """运行时动态添加事件（如录制开始后注册 ask_stop）。不写 schedule.json。"""
        try:
            at = parse_iso(ev["at"]).timestamp()
        except Exception as e:
            log(f"add_runtime 解析失败: {e}")
            return
        with self.lock:
            self.seq += 1
            heapq.heappush(self.heap, (at, self.seq, ev))
        self.wake.set()
        log(f"运行时事件已添加: {ev.get('kind')} @ {ev.get('at')}")

    def _next_delay(self):
        with self.lock:
            if not self.heap:
                return None
            return max(0.0, self.heap[0][0] - datetime.now().timestamp())

    def _drain_due(self):
        now = datetime.now().timestamp()
        due = []
        with self.lock:
            while self.heap and self.heap[0][0] <= now:
                _, _, ev = heapq.heappop(self.heap)
                due.append(ev)
        return due

    def run(self):
        while not self.stopping:
            self.wake.clear()
            delay = self._next_delay()
            if delay is None:
                # 没有事件，无限等待直到 SIGHUP / 信号
                self.wake.wait()
            else:
                self.wake.wait(timeout=delay)

            for ev in self._drain_due():
                self._fire(ev)

    def _fire(self, ev):
        kind = ev.get("kind")
        log(f"🔔 触发: {kind} | meeting_id={ev.get('meeting_id')} | title={ev.get('title')}")
        try:
            if kind == "remind":
                self._spawn([
                    sys.executable, str(SCRIPT_DIR / "notify.py"),
                    "remind", "Meeting Assistant",
                    f"会议「{ev.get('title','')}」 5 分钟后开始",
                    ev.get("title", ""),
                ])
            elif kind == "ask_record":
                self._spawn([
                    sys.executable, str(SCRIPT_DIR / "meeting_daemon.py"),
                    "ask_record", ev.get("title", ""), ev.get("meeting_id", ""),
                ])
            elif kind == "ask_stop":
                self._spawn([
                    sys.executable, str(SCRIPT_DIR / "meeting_daemon.py"),
                    "auto_stop",
                ])
            else:
                log(f"⚠️ 未知事件类型: {kind}")
        except Exception as e:
            log(f"事件处理异常: {e}")

    def _spawn(self, cmd):
        subprocess.Popen(
            cmd,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            start_new_session=True,
        )


def main():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    PID_PATH.write_text(str(os.getpid()))
    log(f"📡 scheduler daemon 启动 (pid={os.getpid()})")

    sched = Scheduler()
    sched.load()

    def on_hup(signum, frame):
        log("收到 SIGHUP，重新加载 schedule.json")
        sched.load()
        sched.wake.set()

    def on_term(signum, frame):
        log(f"收到 signal={signum}，退出")
        sched.stopping = True
        sched.wake.set()

    signal.signal(signal.SIGHUP, on_hup)
    signal.signal(signal.SIGTERM, on_term)
    signal.signal(signal.SIGINT, on_term)

    try:
        sched.run()
    finally:
        try:
            PID_PATH.unlink(missing_ok=True)
        except Exception:
            pass
        log("scheduler 已退出")


if __name__ == "__main__":
    main()
