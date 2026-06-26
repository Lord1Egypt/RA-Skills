"""
hermes-memory-bridge / task_processor.py
任务处理器核心 — 接收 Hermes 命令，执行并回写结果

支持的命令类型：
  search_memory   — 搜索 WorkBuddy 记忆
  sync_session    — 同步会话记忆
  create_task     — 在滴答清单创建任务
  complete_task   — 标记任务完成
  list_tasks      — 列出滴答清单任务
  research        — 执行深度调研
  write_note      — 写入 IMA 笔记
  ack             — 确认收到信号（ACK）
  echo            — 回显测试

用法（作为模块导入）：
  from task_processor import process_command
  result = process_command(command_type, params)
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

SKILL_DIR = Path(__file__).parent
sys.path.insert(0, str(SKILL_DIR))

try:
    from config import SHARED_DIR, _get_logger, WORKBUDDY_MEMORY_DIR
except ImportError:
    SHARED_DIR = Path.home() / ".hermes" / "shared"
    import logging
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    _get_logger = lambda n: logging.getLogger(n)
    WORKBUDDY_MEMORY_DIR = None

logger = _get_logger("task_processor")

# ─── 路径 ──────────────────────────────────────────────────────────
FEEDBACK_DIR = SHARED_DIR / "feedback"  # WorkBuddy 结果回写目录

# ─── 工具函数 ──────────────────────────────────────────────────────

def _ts() -> str:
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def _safe_read(path: Path, default: Any = None) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        return default


def _safe_write(path: Path, data: Any) -> bool:
    try:
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return True
    except (PermissionError, OSError) as e:
        logger.error(f"写入失败 {path}: {e}")
        return False


def _run_cmd(cmd: list[str], timeout: int = 30) -> dict[str, Any]:
    """通用命令执行"""
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode,
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": f"命令超时（{timeout}s）"}
    except FileNotFoundError as e:
        return {"success": False, "error": f"命令不存在: {e}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


# ─── 任务处理器映射 ────────────────────────────────────────────────

def _search_memory(params: dict) -> dict:
    """搜索 WorkBuddy 记忆目录（跨所有会话目录）"""
    keyword = params.get("keyword", "")
    if not keyword:
        return {"success": False, "error": "缺少 keyword 参数"}

    results: list[dict] = []
    wb_root = Path.home() / "WorkBuddy"

    if not wb_root.exists():
        return {"success": False, "error": f"找不到 WorkBuddy 根目录: {wb_root}"}

    # 收集所有会话的记忆目录（当前会话优先）
    memory_dirs: list[Path] = []
    try:
        for d in wb_root.iterdir():
            if not (d.is_dir() and d.name.isdigit() and len(d.name) >= 10):
                continue
            mem_dir = d / ".workbuddy" / "memory"
            if mem_dir.exists():
                memory_dirs.append(mem_dir)
    except PermissionError:
        return {"success": False, "error": "权限不足，无法读取 WorkBuddy 目录"}

    if not memory_dirs:
        return {"success": False, "error": "找不到任何 WorkBuddy 记忆目录"}

    for search_dir in memory_dirs:
        try:
            for fpath in search_dir.rglob("*.md"):
                try:
                    content = fpath.read_text(encoding="utf-8")
                    if keyword in content:
                        lines = content.split("\n")
                        matched = [l.strip() for l in lines if keyword in l]
                        results.append({
                            "dir": search_dir.parent.parent.name,  # 会话ID
                            "file": fpath.name,
                            "snippet": matched[0][:200] if matched else content[:200],
                        })
                except (OSError, UnicodeDecodeError):
                    continue
        except PermissionError:
            continue

    return {
        "success": True,
        "keyword": keyword,
        "count": len(results),
        "results": results[:10],
    }


def _sync_session(params: dict) -> dict:
    """同步会话记忆（生成会话摘要写到 WorkBuddy 记忆）"""
    topic = params.get("topic", "通用会话")
    summary = params.get("summary", "")
    notes = params.get("notes", "")

    if not summary:
        return {"success": False, "error": "缺少 summary 参数"}

    memory_dir = WORKBUDDY_MEMORY_DIR
    if not memory_dir or not memory_dir.exists():
        # 回退到当前最新会话目录
        wb_root = Path.home() / "WorkBuddy"
        if wb_root.exists():
            try:
                latest = max(
                    [d for d in wb_root.iterdir() if d.is_dir() and d.name.isdigit()],
                    key=lambda d: d.name,
                )
                memory_dir = latest / ".workbuddy" / "memory"
            except (ValueError, PermissionError):
                pass
    if not memory_dir:
        return {"success": False, "error": "无法定位 WorkBuddy 记忆目录"}

    today = datetime.now().strftime("%Y-%m-%d")
    fname = memory_dir / f"{today}.md"

    entry = f"\n## [{_ts()}] {topic}\n\n{summary}\n"
    if notes:
        entry += f"\n**备注**: {notes}\n"

    try:
        FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)
        existing = ""
        if fname.exists():
            existing = fname.read_text(encoding="utf-8")
        fname.write_text(existing + entry, encoding="utf-8")
        return {"success": True, "file": str(fname), "entry_preview": summary[:100]}
    except PermissionError:
        return {"success": False, "error": "权限不足，无法写入记忆文件"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _create_task(params: dict) -> dict:
    """在滴答清单创建任务"""
    title = params.get("title", "")
    if not title:
        return {"success": False, "error": "缺少 title 参数"}

    # 优先使用 ticktickpower skill
    try:
        result = _run_cmd([
            sys.executable, "-c",
            f"from ticktickpower import TickTick; t = TickTick(); "
            f"print(t.add_task(title='{title}', project_id='5a4ba4bce775913530602288'))"
        ], timeout=15)
        if result.get("success"):
            try:
                return {"success": True, "task": json.loads(result["stdout"])}
            except json.JSONDecodeError:
                return {"success": True, "raw": result["stdout"]}
        return {"success": False, "error": result.get("error") or result.get("stderr") or "创建失败"}
    except Exception:
        pass

    # fallback：使用 dida365 web API 方式（简化为返回提示）
    return {
        "success": False,
        "error": "ticktickpower 未安装或不可用",
        "hint": "请在 WorkBuddy 中手动创建任务或确保 ticktickpower skill 已激活",
        "title": title,
    }


def _complete_task(params: dict) -> dict:
    """标记滴答清单任务完成"""
    task_id = params.get("task_id", "")
    if not task_id:
        return {"success": False, "error": "缺少 task_id 参数"}

    try:
        result = _run_cmd([
            sys.executable, "-c",
            f"from ticktickpower import TickTick; t = TickTick(); t.complete_task('{task_id}')"
        ], timeout=10)
        return {"success": result.get("success", False), "raw": result}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _list_tasks(params: dict) -> dict:
    """列出滴答清单今日任务"""
    try:
        result = _run_cmd([
            sys.executable, "-c",
            "from ticktickpower import TickTick; t = TickTick(); print(t.list_tasks(limit=10))"
        ], timeout=15)
        if result.get("success"):
            try:
                tasks = json.loads(result["stdout"])
                return {"success": True, "tasks": tasks, "count": len(tasks)}
            except json.JSONDecodeError:
                return {"success": True, "raw": result["stdout"]}
        return {"success": False, "error": result.get("error") or result.get("stderr")}
    except Exception as e:
        return {"success": False, "error": str(e)}


def _ack(params: dict) -> dict:
    """确认信号（对 Hermes 发来的 ack 类型指令）"""
    signal_id = params.get("signal_id", "")
    message = params.get("message", "已确认")
    return {
        "success": True,
        "signal_id": signal_id,
        "message": message,
        "acknowledged_at": _ts(),
    }


def _echo(params: dict) -> dict:
    """回显测试"""
    return {
        "success": True,
        "echo": params.get("message", "pong"),
        "received_at": _ts(),
    }


def _unknown(params: dict) -> dict:
    """未知命令"""
    return {
        "success": False,
        "error": f"未知命令类型",
        "hint": "支持的命令类型：search_memory, sync_session, create_task, complete_task, list_tasks, ack, echo",
    }


# ─── 命令注册表 ────────────────────────────────────────────────────

_COMMAND_HANDLERS: dict[str, callable] = {
    "search_memory":  _search_memory,
    "sync_session":   _sync_session,
    "create_task":     _create_task,
    "complete_task":  _complete_task,
    "list_tasks":     _list_tasks,
    "ack":            _ack,
    "echo":           _echo,
}


# ─── 核心处理函数 ──────────────────────────────────────────────────

def process_command(command_type: str, params: dict, signal_id: str = "") -> dict:
    """
    处理来自 Hermes 的命令。

    Args:
        command_type: 命令类型（见上方注册表）
        params:       命令参数字典
        signal_id:    对应的信号 ID（用于回写）

    Returns:
        执行结果字典（包含 success、data、error 等字段）
    """
    handler = _COMMAND_HANDLERS.get(command_type, _unknown)
    logger.info(f"处理命令 [{signal_id[:8] if signal_id else '?'}]: {command_type}")

    start = time.time()
    result: dict[str, Any]

    try:
        result = handler(params)
    except Exception as e:
        logger.error(f"命令 [{command_type}] 执行异常: {e}")
        result = {"success": False, "error": str(e)}

    elapsed_ms = round((time.time() - start) * 1000, 1)
    result["_meta"] = {
        "command": command_type,
        "signal_id": signal_id,
        "processed_at": _ts(),
        "elapsed_ms": elapsed_ms,
        "processor": "WorkBuddy",
    }

    logger.info(
        f"命令 [{command_type}] 完成: {'✅' if result.get('success') else '❌'} "
        f"({elapsed_ms}ms)"
    )
    return result


# ─── CLI 入口（手动触发） ─────────────────────────────────────────

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Hermes → WorkBuddy 任务处理器")
    parser.add_argument("command", help="命令类型")
    parser.add_argument("--params", default="{}", help="JSON 参数字符串")
    parser.add_argument("--signal-id", default="", help="关联信号 ID")

    args = parser.parse_args()

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError:
        print(f"参数 JSON 解析失败: {args.params}")
        sys.exit(1)

    result = process_command(args.command, params, args.signal_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    sys.exit(0 if result.get("success") else 1)
