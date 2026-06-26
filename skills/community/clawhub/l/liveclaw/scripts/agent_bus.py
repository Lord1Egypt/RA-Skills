#!/usr/bin/env python3
"""
Agent Event Bus — 实时记录 agent 工作状态
Agent 执行任务时调用 emit()，Dashboard 读取展示
跨平台：Linux / Windows / macOS
"""
import json, os, time, datetime, tempfile
from pathlib import Path

try:
    from platform_utils import get_work_dir
except ImportError:
    import sys
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    from platform_utils import get_work_dir

_WORK_DIR  = get_work_dir()
_WORK_DIR.mkdir(parents=True, exist_ok=True)
BUS_FILE   = str(_WORK_DIR / "agent_events.jsonl")
STATE_FILE = str(_WORK_DIR / "agent_state.json")
MAX_EVENTS = 200  # 最多保留最近200条
_emit_count = 0   # emit 计数器（优化：避免每次都读文件检查行数）
_DEDUP_SEC = 5    # 同 kind+text 在此秒数内不重复写入（文件级去重，跨进程生效）

ICONS = {
    "task":     "[TASK]",
    "tool":     "[TOOL]",
    "think":    "[THINK]",
    "result":   "[OK]",
    "error":    "[ERR]",
    "info":     "[INFO]",
    "search":   "[SRCH]",
    "write":    "[WRITE]",
    "exec":     "[EXEC]",
    "fetch":    "[FETCH]",
    "memory":   "[MEM]",
    "stream":   "[LIVE]",
}

def _is_duplicate(kind: str, text: str) -> bool:
    """文件级去重：读取 JSONL 最后几行，检查是否有相同 kind+text 且间隔 < _DEDUP_SEC 秒。
    跨进程生效（每次 CLI 调用都是独立进程）。
    """
    try:
        p = Path(BUS_FILE)
        if not p.exists():
            return False
        # 只读文件末尾 4KB（足够覆盖最近几条事件，避免全量读取）
        size = p.stat().st_size
        with open(BUS_FILE, "r", encoding="utf-8") as f:
            if size > 4096:
                f.seek(size - 4096)
                f.readline()  # 丢弃不完整的首行
            lines = f.readlines()
        now = datetime.datetime.now()
        # 从后往前检查最近几条，找同 kind+text 的事件
        for line in reversed(lines[-10:]):
            line = line.strip()
            if not line:
                continue
            try:
                ev = json.loads(line)
            except json.JSONDecodeError:
                continue
            if ev.get("kind") == kind and ev.get("text", "")[:80] == text[:80]:
                # 检查时间差
                try:
                    ev_time = datetime.datetime.fromisoformat(ev["ts"])
                    delta = (now - ev_time).total_seconds()
                    if 0 <= delta < _DEDUP_SEC:
                        return True
                except Exception:
                    pass
    except Exception:
        pass
    return False

def emit(kind: str, text: str, detail: str = ""):
    """向事件总线写入一条事件（文件级去重：同 kind+text 在 5s 内不重复写入，跨进程生效）"""
    global _emit_count
    # ── 文件级去重（跨进程） ──
    if _is_duplicate(kind, text):
        return  # 重复事件，静默跳过

    event = {
        "ts": datetime.datetime.now().isoformat(),
        "kind": kind,
        "icon": ICONS.get(kind, "•"),
        "text": text,
        "detail": detail,
    }
    # append to JSONL
    with open(BUS_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    # update state
    state = {
        "current": event,
        "state": kind,
        "updated_at": event["ts"],
    }
    with open(STATE_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    # 优化：每 50 次 emit 才检查一次 trim（减少 95% 的文件全量读取）
    _emit_count += 1
    if _emit_count % 50 == 0:
        _trim()

def _trim():
    """修剪事件文件，保留最近 MAX_EVENTS 条
    使用 temp file + os.replace() 原子替换，避免读写竞争导致空文件/部分写入
    """
    try:
        lines = Path(BUS_FILE).read_text(encoding="utf-8").strip().splitlines()
        if len(lines) > MAX_EVENTS:
            trimmed = "\n".join(lines[-MAX_EVENTS:]) + "\n"
            # 原子写入：先写临时文件，再 rename 替换
            dir_name = os.path.dirname(BUS_FILE) or "."
            fd, tmp_path = tempfile.mkstemp(dir=dir_name, suffix=".tmp")
            fd_closed = False
            try:
                os.write(fd, trimmed.encode("utf-8"))
                os.close(fd)
                fd_closed = True
                os.replace(tmp_path, BUS_FILE)  # 原子替换
            except Exception:
                if not fd_closed:
                    try:
                        os.close(fd)
                    except OSError:
                        pass
                try:
                    os.unlink(tmp_path)
                except OSError:
                    pass
    except Exception:
        pass

def read_events(n=50):
    """读取最近 n 条事件，跳过残缺行（防止并发写入竞争）"""
    try:
        lines = Path(BUS_FILE).read_text(encoding="utf-8").strip().splitlines()
        out = []
        for l in lines[-n:]:
            l = l.strip()
            if l:
                try:
                    out.append(json.loads(l))
                except json.JSONDecodeError:
                    pass  # 跳过残缺行
        return out
    except Exception:
        return []

def read_state():
    try:
        return json.loads(Path(STATE_FILE).read_text(encoding="utf-8"))
    except Exception:
        return {"state": "idle", "current": None}

if __name__ == "__main__":
    import sys
    if len(sys.argv) >= 3:
        emit(sys.argv[1], sys.argv[2], sys.argv[3] if len(sys.argv) > 3 else "")
        print(f"Event emitted: [{sys.argv[1]}] {sys.argv[2]}")
    else:
        print("Usage: agent_bus.py <kind> <text> [detail]")
