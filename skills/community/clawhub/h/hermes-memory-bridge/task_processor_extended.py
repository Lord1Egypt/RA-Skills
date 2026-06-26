"""
hermes-memory-bridge / task_processor_extended.py
任务处理器扩展版 — 添加天气查询功能

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
  weather_query   — 查询天气（新增）

用法（作为模块导入）：
  from task_processor_extended import process_command
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

logger = _get_logger("task_processor_extended")

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

    # 导入原始模块中的函数
    try:
        from task_processor import _search_memory as original_search_memory
        return original_search_memory(params)
    except ImportError:
        # 如果无法导入，返回简化版本
        return {"success": False, "error": "无法导入原始搜索函数"}


def _sync_session(params: dict) -> dict:
    """同步会话摘要到 WorkBuddy 记忆"""
    topic = params.get("topic", "")
    summary = params.get("summary", "")
    if not topic or not summary:
        return {"success": False, "error": "缺少 topic 或 summary 参数"}
    
    try:
        from task_processor import _sync_session as original_sync_session
        return original_sync_session(params)
    except ImportError:
        return {"success": False, "error": "无法导入原始同步函数"}


def _create_task(params: dict) -> dict:
    """在滴答清单创建任务"""
    title = params.get("title", "")
    if not title:
        return {"success": False, "error": "缺少 title 参数"}
    
    try:
        from task_processor import _create_task as original_create_task
        return original_create_task(params)
    except ImportError:
        return {"success": False, "error": "无法导入原始创建任务函数"}


def _complete_task(params: dict) -> dict:
    """标记滴答清单任务完成"""
    task_id = params.get("task_id", "")
    if not task_id:
        return {"success": False, "error": "缺少 task_id 参数"}
    
    try:
        from task_processor import _complete_task as original_complete_task
        return original_complete_task(params)
    except ImportError:
        return {"success": False, "error": "无法导入原始完成任务函数"}


def _list_tasks(params: dict) -> dict:
    """列出滴答清单今日任务"""
    try:
        from task_processor import _list_tasks as original_list_tasks
        return original_list_tasks(params)
    except ImportError:
        return {"success": False, "error": "无法导入原始列出任务函数"}


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


def _weather_query(params: dict) -> dict:
    """查询天气"""
    location = params.get("location", "Beijing")
    format_type = params.get("format", "3")
    
    try:
        # 使用wttr.in查询天气
        cmd = ["curl", "-s", f"wttr.in/{location}?format={format_type}"]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0:
            return {
                "success": True,
                "location": location,
                "weather": result.stdout.strip(),
                "source": "wttr.in"
            }
        else:
            return {
                "success": False,
                "error": f"天气查询失败: {result.stderr.strip()}",
                "location": location
            }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "查询超时", "location": location}
    except Exception as e:
        return {"success": False, "error": str(e), "location": location}


def _unknown(params: dict) -> dict:
    """未知命令"""
    return {
        "success": False,
        "error": f"未知命令类型",
        "hint": "支持的命令类型：search_memory, sync_session, create_task, complete_task, list_tasks, ack, echo, weather_query",
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
    "weather_query":  _weather_query,
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

    parser = argparse.ArgumentParser(description="Hermes → WorkBuddy 任务处理器（扩展版）")
    parser.add_argument("command", help="命令类型")
    parser.add_argument("--params", default="{}", help="JSON 参数字符串")
    parser.add_argument("--signal-id", default="", help="信号 ID（可选）")

    args = parser.parse_args()

    try:
        params = json.loads(args.params)
    except json.JSONDecodeError:
        print(f"❌ JSON 解析失败: {args.params}", file=sys.stderr)
        sys.exit(1)

    result = process_command(args.command, params, args.signal_id)
    print(json.dumps(result, ensure_ascii=False, indent=2))