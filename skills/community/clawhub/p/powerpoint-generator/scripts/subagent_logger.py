#!/usr/bin/env python3
"""Subagent Logger -- 记录 Subagent 阶段命令的 stdout/stderr 到 Runtime 日志

用法:
  python subagent_logger.py --session-id SESSION_ID --stage "PageAgent-3" --log runtime/logs/pageagent-3.log

  python subagent_logger.py --session-id SESSION_ID \
      --command "python3 scripts/html2svg.py slides/ -o svg/" \
      --log runtime/logs/step2-stderr.log \
      --tee
"""

import argparse
import json
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path


# -------------------------------------------------------------------
# 日志格式
# -------------------------------------------------------------------
def log_entry(session_id: str, stage: str, event: str, data: dict = None) -> dict:
    """生成标准日志条目。"""
    return {
        "timestamp": datetime.now().isoformat(),
        "session_id": session_id,
        "stage": stage,
        "event": event,
        "data": data or {},
    }


def write_log(log_path: Path, entry: dict):
    """写入日志文件（JSONL 格式）。"""
    log_path.parent.mkdir(parents=True, exist_ok=True)
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def read_logs(log_path: Path, session_id: str = None, stage: str = None) -> list:
    """读取日志文件。"""
    if not log_path.exists():
        return []

    logs = []
    with open(log_path, encoding="utf-8") as f:
        for line in f:
            try:
                entry = json.loads(line.strip())
                if session_id and entry.get("session_id") != session_id:
                    continue
                if stage and entry.get("stage") != stage:
                    continue
                logs.append(entry)
            except json.JSONDecodeError:
                continue
    return logs


# -------------------------------------------------------------------
# 命令执行 + 记录
# -------------------------------------------------------------------
def run_and_log(command: str, log_path: Path, session_id: str, stage: str, cwd: Path = None) -> int:
    """执行命令并同时记录 stdout/stderr 到日志文件。"""
    write_log(log_path, log_entry(session_id, stage, "command_start", {"command": command}))

    start_time = time.time()
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        cwd=str(cwd) if cwd else None,
    )

    stdout, stderr = process.communicate()
    elapsed = time.time() - start_time

    result = {
        "return_code": process.returncode,
        "elapsed_seconds": round(elapsed, 2),
        "stdout_size": len(stdout),
        "stderr_size": len(stderr),
    }

    # 写入 stdout/stderr 到日志
    if stdout:
        write_log(log_path, log_entry(session_id, stage, "stdout", {"size": len(stdout), "excerpt": stdout[:500].decode("utf-8", errors="replace")}))
    if stderr:
        write_log(log_path, log_entry(session_id, stage, "stderr", {"size": len(stderr), "excerpt": stderr[:500].decode("utf-8", errors="replace")}))

    write_log(log_path, log_entry(session_id, stage, "command_end", result))

    return process.returncode


# -------------------------------------------------------------------
# 主函数
# -------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Subagent Logger")
    parser.add_argument("--session-id", required=True, help="Subagent session ID")
    parser.add_argument("--stage", required=True, help="Stage name (e.g. PageAgent-3)")
    parser.add_argument("--command", help="Command to run (mutually exclusive with --log)")
    parser.add_argument("--log", type=Path, required=True, help="Log file path")
    parser.add_argument("--cwd", type=Path, help="Working directory")
    parser.add_argument("--read", action="store_true", help="Read and print existing logs")
    parser.add_argument("--events", action="store_true", help="List events only (for --read)")

    args = parser.parse_args()

    if args.read:
        logs = read_logs(args.log, args.session_id, args.stage)
        if args.events:
            for entry in logs:
                ts = entry.get("timestamp", "")
                event = entry.get("event", "")
                print(f"[{ts}] {entry.get('stage', '')}: {event}")
        else:
            print(json.dumps(logs, ensure_ascii=False, indent=2))
        return

    if not args.command:
        print("ERROR: --command is required (or use --read)", file=sys.stderr)
        sys.exit(1)

    return_code = run_and_log(
        args.command,
        args.log,
        args.session_id,
        args.stage,
        args.cwd
    )

    sys.exit(return_code)


if __name__ == "__main__":
    main()
