"""KingDoc 记忆桥接引擎

v4.0 新增：与 zwjh 记忆库打通。

能力：
- 白名单探测 zwjh mcp_server 是否存在
- stdio JSON-RPC 调用 zwjh 的标准工具（协议公开、不打包其代码）
- 文档关键事件（创建/重要编辑/分享）经 zwjh MCP 总线写入长期记忆
- 未安装则事件写本地待迁移日志，未来安装后一次性导入
- 子进程超时自动关闭（规则4）
- 价值：用户问 zwjh 上周改了什么文档时可答

设计原则：
- 零第三方依赖（仅标准库）
- 硬件自适应（批量操作时读取 hardware.py）
- 零密钥可用（本地降级模式）
- 子进程超时自动关闭，不残留
"""
from __future__ import annotations

import json
import os
import shutil
import sqlite3
import subprocess
import tempfile
import threading
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional


# zwjh mcp_server 白名单路径
ZWJH_WHITELIST_PATHS: Dict[str, List[str]] = {
    "Windows": [
        "C:/Users/Administrator/.workbuddy/skills/zwjh-skill",
        "D:/skill/zwjh-skill",
    ],
    "Darwin": [
        os.path.expanduser("~/.workbuddy/skills/zwjh-skill"),
    ],
    "Linux": [
        os.path.expanduser("~/.workbuddy/skills/zwjh-skill"),
    ],
}

# zwjh mcp_server 脚本入口
ZWJH_MCP_SCRIPT = "scripts/cli.py"

# 子进程默认超时（秒）
SUBPROCESS_TIMEOUT = 30


class ZwjhDetector:
    """zwjh mcp_server 探测器"""

    @staticmethod
    def detect() -> Optional[str]:
        """探测 zwjh mcp_server 路径

        Returns:
            安装路径，未安装返回 None
        """
        import platform
        system = platform.system()
        paths = ZWJH_WHITELIST_PATHS.get(system, [])

        for path in paths:
            mcp_script = os.path.join(path, ZWJH_MCP_SCRIPT)
            if os.path.isfile(mcp_script):
                return path

        return None

    @staticmethod
    def is_installed() -> bool:
        """检查 zwjh 是否已安装"""
        return ZwjhDetector.detect() is not None

    @staticmethod
    def get_mcp_script(install_path: str) -> str:
        """获取 zwjh mcp_server 脚本路径"""
        mcp_script = os.path.join(install_path, ZWJH_MCP_SCRIPT)
        if os.path.isfile(mcp_script):
            return mcp_script
        return ""


class SubprocessRunner:
    """子进程执行器（带超时自动关闭）"""

    @staticmethod
    def run(cmd: List[str], input_data: str = "", timeout: int = SUBPROCESS_TIMEOUT,
            cwd: str = "") -> Dict:
        """执行子进程命令

        Args:
            cmd: 命令列表
            input_data: 输入数据（stdin）
            timeout: 超时时间（秒）
            cwd: 工作目录

        Returns:
            {
                "success": bool,
                "returncode": int,
                "stdout": str,
                "stderr": str,
                "timed_out": bool
            }
        """
        try:
            proc = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE if input_data else None,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd or None,
            )

            try:
                stdout, stderr = proc.communicate(input=input_data, timeout=timeout)
                return {
                    "success": proc.returncode == 0,
                    "returncode": proc.returncode,
                    "stdout": stdout,
                    "stderr": stderr,
                    "timed_out": False,
                }
            except subprocess.TimeoutExpired:
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                return {
                    "success": False,
                    "returncode": -1,
                    "stdout": "",
                    "stderr": f"子进程超时（{timeout}秒）已自动关闭",
                    "timed_out": True,
                }
        except FileNotFoundError:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"命令未找到: {cmd[0]}",
                "timed_out": False,
            }
        except Exception as e:
            return {
                "success": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "timed_out": False,
            }


class MemoryBridge:
    """记忆桥接引擎

    与 zwjh 记忆库打通的核心引擎。
    """

    def __init__(self, backend: Optional[Any] = None):
        self.backend = backend
        self._local_mode = backend is None
        self.zwjh_path = ZwjhDetector.detect()
        self.mcp_script = ZwjhDetector.get_mcp_script(self.zwjh_path) if self.zwjh_path else ""
        self.runner = SubprocessRunner()
        self._pending_log_path = str(
            Path(__file__).resolve().parent.parent.parent / ".kingdoc_memory_pending.db"
        )
        self._init_pending_db()

    @property
    def is_local_mode(self) -> bool:
        return self._local_mode

    @property
    def zwjh_installed(self) -> bool:
        return self.zwjh_path is not None

    def _init_pending_db(self):
        """初始化待迁移日志数据库"""
        try:
            conn = sqlite3.connect(self._pending_log_path)
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS pending_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    event_type TEXT NOT NULL,
                    doc_id TEXT NOT NULL,
                    file_name TEXT DEFAULT '',
                    action_details TEXT DEFAULT '{}',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    migrated INTEGER DEFAULT 0,
                    migrated_at TIMESTAMP DEFAULT NULL
                )
            """)
            conn.commit()
            conn.close()
        except Exception:
            pass

    def get_status(self) -> Dict:
        """获取记忆桥接状态"""
        # 计算未迁移事件数量
        pending_count = 0
        try:
            conn = sqlite3.connect(self._pending_log_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM pending_events WHERE migrated = 0")
            row = cursor.fetchone()
            pending_count = row[0] if row else 0
            conn.close()
        except Exception:
            pass

        return {
            "zwjh_installed": self.zwjh_installed,
            "zwjh_path": self.zwjh_path,
            "mcp_script": self.mcp_script,
            "local_mode": self._local_mode,
            "pending_events": pending_count,
        }

    # ===========================================================================
    # 核心：发送事件到 zwjh 或本地待迁移日志
    # ===========================================================================

    def deposit_event(self, event_type: str, doc_id: str,
                      file_name: str = "", action_details: Dict = None) -> Dict:
        """发送文档关键事件到 zwjh 长期记忆

        Args:
            event_type: create / edit / share / delete
            doc_id: 文档 ID
            file_name: 文件名
            action_details: 额外详情

        Returns:
            {"success": bool, "message": str, "destination": "zwjh" | "pending"}
        """
        event = {
            "event_type": event_type,
            "doc_id": doc_id,
            "file_name": file_name,
            "action_details": action_details or {},
            "timestamp": datetime.now().isoformat(),
        }

        # 如果 zwjh 安装，直接调用
        if self.zwjh_installed:
            result = self._zwjh_deposit(event)
            if result.get("success"):
                return {
                    "success": True,
                    "destination": "zwjh",
                    "message": "事件已写入 zwjh 长期记忆",
                    "event": event,
                }
            # 失败则降级到待迁移日志
            self._log_pending_event(event)
            return {
                "success": True,
                "destination": "pending",
                "message": "zwjh 调用失败，已写入待迁移日志",
                "event": event,
            }
        else:
            # 未安装，写待迁移日志
            self._log_pending_event(event)
            return {
                "success": True,
                "destination": "pending",
                "message": "zwjh 未安装，事件已写入待迁移日志",
                "event": event,
            }

    def _zwjh_deposit(self, event: Dict) -> Dict:
        """调用 zwjh 的 deposit 工具（stdio JSON-RPC）

        Args:
            event: 事件数据

        Returns:
            {"success": bool, "stdout": str, "stderr": str}
        """
        # 构建 JSON-RPC 请求
        rpc_request = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000) % 1000000,
            "method": "tools/call",
            "params": {
                "name": "deposit",
                "arguments": {
                    "text": self._format_event_text(event),
                    "file_name": event.get("file_name", ""),
                    "doc_id": event.get("doc_id", ""),
                    "event_type": event.get("event_type", ""),
                },
            },
        }

        input_json = json.dumps(rpc_request, ensure_ascii=False)
        result = self.runner.run(
            ["python", self.mcp_script, "--mcp-stdin"],
            input_data=input_json,
            timeout=SUBPROCESS_TIMEOUT,
            cwd=self.zwjh_path,
        )

        if result["timed_out"]:
            return {"success": False, "error": f"调用超时（{SUBPROCESS_TIMEOUT}秒）"}

        if not result["success"]:
            return {"success": False, "error": result["stderr"]}

        # 解析 JSON-RPC 响应
        try:
            response = json.loads(result["stdout"])
            if response.get("error"):
                return {"success": False, "error": response["error"].get("message", "未知错误")}
            return {"success": True, "data": response.get("result", {})}
        except json.JSONDecodeError:
            return {"success": True, "raw_output": result["stdout"]}

    def _format_event_text(self, event: Dict) -> str:
        """将事件格式化为 zwjh deposit 的文本格式"""
        event_type = event.get("event_type", "")
        file_name = event.get("file_name", "")
        doc_id = event.get("doc_id", "")
        timestamp = event.get("timestamp", "")

        type_labels = {
            "create": "创建文档",
            "edit": "编辑文档",
            "share": "分享文档",
            "delete": "删除文档",
        }
        type_label = type_labels.get(event_type, event_type)

        parts = [f"[{timestamp}] {type_label}: {file_name}"]
        if doc_id:
            parts.append(f"文档ID: {doc_id}")

        details = event.get("action_details", {})
        if details:
            for k, v in details.items():
                parts.append(f"{k}: {v}")

        return "\n".join(parts)

    def _log_pending_event(self, event: Dict):
        """写入待迁移日志"""
        try:
            conn = sqlite3.connect(self._pending_log_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO pending_events
                (event_type, doc_id, file_name, action_details)
                VALUES (?, ?, ?, ?)
            """, (
                event.get("event_type", ""),
                event.get("doc_id", ""),
                event.get("file_name", ""),
                json.dumps(event.get("action_details", {}), ensure_ascii=False),
            ))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def get_pending_events(self, limit: int = 100) -> List[Dict]:
        """获取待迁移事件列表"""
        try:
            conn = sqlite3.connect(self._pending_log_path)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT * FROM pending_events WHERE migrated = 0 ORDER BY created_at ASC LIMIT ?
            """, (limit,))
            rows = cursor.fetchall()
            conn.close()

            return [
                {
                    "id": row[0],
                    "event_type": row[1],
                    "doc_id": row[2],
                    "file_name": row[3],
                    "action_details": json.loads(row[4]) if row[4] else {},
                    "created_at": row[5],
                }
                for row in rows
            ]
        except Exception:
            return []

    def migrate_pending_events(self) -> Dict:
        """一次性导入所有待迁移事件到 zwjh

        Returns:
            {"total": int, "success": int, "failed": int, "details": [...]}
        """
        if not self.zwjh_installed:
            return {
                "success": False,
                "error": "zwjh 未安装，无法迁移",
                "hint": "请先安装 zwjh-skill",
            }

        events = self.get_pending_events()
        if not events:
            return {"total": 0, "success": 0, "failed": 0, "message": "无待迁移事件"}

        success = 0
        failed = 0
        details = []

        for event in events:
            result = self._zwjh_deposit(event)
            if result.get("success"):
                success += 1
                # 标记为已迁移
                try:
                    conn = sqlite3.connect(self._pending_log_path)
                    cursor = conn.cursor()
                    cursor.execute("""
                        UPDATE pending_events SET migrated = 1, migrated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (event["id"],))
                    conn.commit()
                    conn.close()
                except Exception:
                    pass
            else:
                failed += 1
            details.append({"event": event, "result": result})

        return {
            "total": len(events),
            "success": success,
            "failed": failed,
            "details": details,
        }

    def cleanup_migrated_events(self, days: int = 30) -> Dict:
        """清理超过指定天数的已迁移事件"""
        cutoff = datetime.now().timestamp() - (days * 86400)
        try:
            conn = sqlite3.connect(self._pending_log_path)
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM pending_events
                WHERE migrated = 1 AND created_at < datetime(?, 'unixepoch')
            """, (cutoff,))
            deleted = cursor.rowcount
            conn.commit()
            conn.close()
            return {"success": True, "deleted": deleted}
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ===========================================================================
    # 便捷接口：文档关键事件
    # ===========================================================================

    def on_doc_created(self, doc_id: str, file_name: str = "",
                       extra: Dict = None) -> Dict:
        """文档创建事件"""
        return self.deposit_event("create", doc_id, file_name, extra)

    def on_doc_edited(self, doc_id: str, file_name: str = "",
                      edit_summary: str = "", extra: Dict = None) -> Dict:
        """文档编辑事件"""
        details = extra or {}
        if edit_summary:
            details["edit_summary"] = edit_summary
        return self.deposit_event("edit", doc_id, file_name, details)

    def on_doc_shared(self, doc_id: str, file_name: str = "",
                      share_target: str = "", extra: Dict = None) -> Dict:
        """文档分享事件"""
        details = extra or {}
        if share_target:
            details["share_target"] = share_target
        return self.deposit_event("share", doc_id, file_name, details)

    def on_doc_deleted(self, doc_id: str, file_name: str = "",
                       extra: Dict = None) -> Dict:
        """文档删除事件"""
        return self.deposit_event("delete", doc_id, file_name, extra)


def get_memory_bridge(backend: Optional[Any] = None) -> MemoryBridge:
    """获取记忆桥接实例"""
    return MemoryBridge(backend=backend)


def detect_zwjh() -> Dict:
    """便捷函数：探测 zwjh"""
    return {
        "installed": ZwjhDetector.is_installed(),
        "path": ZwjhDetector.detect(),
    }
