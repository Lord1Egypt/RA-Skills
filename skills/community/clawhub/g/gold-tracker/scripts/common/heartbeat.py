"""心跳：记录各命令最近运行时间，供 verify 判断调度是否真的在运行（P0-1）。

每个脚本在成功执行后调用 record("<命令名>")；verify.py 读取最近运行时间，
与 config.general.expected_run_interval_minutes 比较，超时即报「可能未在运行」。
"""

import json
from datetime import datetime

from . import paths, atomic, timeutil


def heartbeat_file():
    return paths.resolve("cache") / "heartbeat.json"


def load():
    f = heartbeat_file()
    if f.exists():
        try:
            data = json.loads(f.read_text(encoding="utf-8"))
            return data if isinstance(data, dict) else {}
        except Exception:
            pass
    return {}


def record(command):
    data = load()
    data[command] = timeutil.now_iso()
    atomic.atomic_write_json(heartbeat_file(), data)


def get(command):
    return load().get(command)


def age_seconds(command, tz="Asia/Shanghai"):
    ts = get(command)
    if not ts:
        return None
    try:
        dt = datetime.fromisoformat(ts)
        return (datetime.now(timeutil.get_tz(tz)) - dt).total_seconds()
    except Exception:
        return None
