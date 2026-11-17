"""KingDoc 本地桥接引擎

v4.0 新增：与 wps-office-suite 双向互通。

能力：
- 白名单探测 wps-office-suite 安装路径
- SQLite 维护本地文件路径 ↔ 云端 doc_id 映射表
- 下行：拉取云端文档到本地临时目录 → subprocess 调 wps 脚本（JSON 契约 {action, input, output}）→ 结果回传云端覆盖
- 上行：监听映射表中本地文件 mtime 变化 → 变化后调用本包上传接口同步
- 未安装 wps：本地分析入口隐藏并输出可选装提示，云端功能不受影响
- 子进程超时自动关闭（规则4）

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
from typing import Any, Dict, List, Optional, Tuple


# wps-office-suite 白名单安装路径（按平台）
WPS_WHITELIST_PATHS: Dict[str, List[str]] = {
    "Windows": [
        "C:/Program Files/WPS Office",
        "C:/Program Files (x86)/WPS Office",
        "D:/Program Files/WPS Office",
        "D:/WPS Office",
    ],
    "Darwin": [
        "/Applications/WPS Office.app",
    ],
    "Linux": [
        "/usr/bin/wps",
        "/usr/local/bin/wps",
        "/opt/wps-office",
    ],
}

# wps-office-suite 脚本入口
WPS_SCRIPTS: Dict[str, str] = {
    "word": "wps_word.py",
    "excel": "wps_excel.py",
    "ppt": "wps_ppt.py",
    "common": "wps_common.py",
}

# 子进程默认超时（秒）
SUBPROCESS_TIMEOUT = 120


class WpsDetector:
    """wps-office-suite 安装探测器"""

    @staticmethod
    def detect() -> Optional[str]:
        """探测 wps-office-suite 安装路径

        Returns:
            安装路径，未安装返回 None
        """
        import platform
        system = platform.system()
        paths = WPS_WHITELIST_PATHS.get(system, [])

        for path in paths:
            if os.path.exists(path):
                return path

        # 尝试从 PATH 中查找
        for cmd in ["wps", "et", "wpp"]:
            found = shutil.which(cmd)
            if found:
                return os.path.dirname(found)

        return None

    @staticmethod
    def is_installed() -> bool:
        """检查 wps-office-suite 是否已安装"""
        return WpsDetector.detect() is not None

    @staticmethod
    def get_scripts_dir(install_path: str) -> str:
        """获取 wps-office-suite 脚本目录"""
        scripts_dir = os.path.join(install_path, "scripts")
        if os.path.isdir(scripts_dir):
            return scripts_dir
        # 尝试上级目录
        parent_scripts = os.path.join(os.path.dirname(install_path), "scripts")
        if os.path.isdir(parent_scripts):
            return parent_scripts
        return ""


class MappingTable:
    """本地文件路径 ↔ 云端 doc_id 映射表（SQLite）"""

    def __init__(self, db_path: str = ""):
        if not db_path:
            db_path = str(Path(__file__).resolve().parent.parent.parent / ".kingdoc_bridge_mapping.db")
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """初始化数据库"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mapping (
                doc_id TEXT PRIMARY KEY,
                local_path TEXT NOT NULL,
                file_name TEXT NOT NULL,
                file_type TEXT DEFAULT 'doc',
                mtime REAL DEFAULT 0,
                size INTEGER DEFAULT 0,
                sync_status TEXT DEFAULT 'synced',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_mapping_local_path
            ON mapping(local_path)
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sync_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                doc_id TEXT NOT NULL,
                action TEXT NOT NULL,
                direction TEXT NOT NULL,
                status TEXT NOT NULL,
                message TEXT DEFAULT '',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()

    def add_mapping(self, doc_id: str, local_path: str, file_name: str,
                    file_type: str = "doc") -> Dict:
        """添加映射"""
        try:
            mtime = os.path.getmtime(local_path) if os.path.exists(local_path) else 0
            size = os.path.getsize(local_path) if os.path.exists(local_path) else 0

            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO mapping
                (doc_id, local_path, file_name, file_type, mtime, size, sync_status, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, 'synced', CURRENT_TIMESTAMP)
            """, (doc_id, local_path, file_name, file_type, mtime, size))
            conn.commit()
            conn.close()
            return {"success": True, "doc_id": doc_id, "local_path": local_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_mapping(self, doc_id: str) -> Optional[Dict]:
        """获取映射"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mapping WHERE doc_id = ?", (doc_id,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "doc_id": row[0],
                    "local_path": row[1],
                    "file_name": row[2],
                    "file_type": row[3],
                    "mtime": row[4],
                    "size": row[5],
                    "sync_status": row[6],
                    "created_at": row[7],
                    "updated_at": row[8],
                }
            return None
        except Exception:
            return None

    def get_mapping_by_local_path(self, local_path: str) -> Optional[Dict]:
        """通过本地路径获取映射"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mapping WHERE local_path = ?", (local_path,))
            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "doc_id": row[0],
                    "local_path": row[1],
                    "file_name": row[2],
                    "file_type": row[3],
                    "mtime": row[4],
                    "size": row[5],
                    "sync_status": row[6],
                }
            return None
        except Exception:
            return None

    def update_mtime(self, doc_id: str, mtime: float) -> Dict:
        """更新 mtime"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE mapping SET mtime = ?, sync_status = 'synced', updated_at = CURRENT_TIMESTAMP
                WHERE doc_id = ?
            """, (mtime, doc_id))
            conn.commit()
            conn.close()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_all_mappings(self) -> List[Dict]:
        """获取所有映射"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM mapping ORDER BY updated_at DESC")
            rows = cursor.fetchall()
            conn.close()

            return [
                {
                    "doc_id": row[0],
                    "local_path": row[1],
                    "file_name": row[2],
                    "file_type": row[3],
                    "mtime": row[4],
                    "size": row[5],
                    "sync_status": row[6],
                }
                for row in rows
            ]
        except Exception:
            return []

    def delete_mapping(self, doc_id: str) -> Dict:
        """删除映射"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM mapping WHERE doc_id = ?", (doc_id,))
            conn.commit()
            conn.close()
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def log_sync(self, doc_id: str, action: str, direction: str,
                 status: str, message: str = ""):
        """记录同步日志"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO sync_log (doc_id, action, direction, status, message)
                VALUES (?, ?, ?, ?, ?)
            """, (doc_id, action, direction, status, message))
            conn.commit()
            conn.close()
        except Exception:
            pass

    def get_sync_log(self, doc_id: str = "", limit: int = 50) -> List[Dict]:
        """获取同步日志"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            if doc_id:
                cursor.execute("""
                    SELECT * FROM sync_log WHERE doc_id = ? ORDER BY created_at DESC LIMIT ?
                """, (doc_id, limit))
            else:
                cursor.execute("""
                    SELECT * FROM sync_log ORDER BY created_at DESC LIMIT ?
                """, (limit,))
            rows = cursor.fetchall()
            conn.close()

            return [
                {
                    "id": row[0],
                    "doc_id": row[1],
                    "action": row[2],
                    "direction": row[3],
                    "status": row[4],
                    "message": row[5],
                    "created_at": row[6],
                }
                for row in rows
            ]
        except Exception:
            return []


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
                # 超时：先 terminate，再 kill
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


class LocalBridge:
    """本地桥接引擎

    与 wps-office-suite 双向互通的核心引擎。
    """

    def __init__(self, backend: Optional[Any] = None):
        self.backend = backend
        self._local_mode = backend is None
        self.wps_path = WpsDetector.detect()
        self.scripts_dir = WpsDetector.get_scripts_dir(self.wps_path) if self.wps_path else ""
        self.mapping = MappingTable()
        self.runner = SubprocessRunner()

    @property
    def is_local_mode(self) -> bool:
        return self._local_mode

    @property
    def wps_installed(self) -> bool:
        return self.wps_path is not None

    def get_status(self) -> Dict:
        """获取桥接状态"""
        return {
            "wps_installed": self.wps_installed,
            "wps_path": self.wps_path,
            "scripts_dir": self.scripts_dir,
            "local_mode": self._local_mode,
            "mapping_count": len(self.mapping.get_all_mappings()),
        }

    # ===========================================================================
    # 下行：云端 → 本地 → wps 处理 → 云端覆盖
    # ===========================================================================

    def downstream_download(self, file_id: str, file_name: str = "",
                           file_type: str = "doc") -> Dict:
        """下行：拉取云端文档到本地

        Args:
            file_id: 云端文档 ID
            file_name: 文件名
            file_type: 文件类型

        Returns:
            {"success": bool, "local_path": str, "message": str}
        """
        if self._local_mode:
            return {
                "success": False,
                "error": "本地降级模式：无法拉取云端文档",
                "hint": "请配置金山 App Key 后使用",
            }

        if not file_name:
            file_name = f"doc_{file_id}"

        # 创建临时目录
        temp_dir = tempfile.mkdtemp(prefix="kingdoc_bridge_dl_")
        local_path = os.path.join(temp_dir, file_name)

        try:
            # 调用云端下载 API
            result = self.backend.kdoc_file_download(file_id, local_path)
            if not os.path.exists(local_path):
                return {
                    "success": False,
                    "error": f"下载失败: {result}",
                }

            # 添加映射
            self.mapping.add_mapping(file_id, local_path, file_name, file_type)
            self.mapping.log_sync(file_id, "download", "downstream", "success", f"下载到 {local_path}")

            return {
                "success": True,
                "file_id": file_id,
                "local_path": local_path,
                "file_name": file_name,
                "message": f"文档已下载到本地: {local_path}",
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"下载失败: {e}",
            }

    def downstream_process(self, file_id: str, action: str,
                           params: Dict = None) -> Dict:
        """下行：调用 wps 脚本处理本地文档

        Args:
            file_id: 云端文档 ID
            action: 操作类型（analyze/convert/format/extract）
            params: 额外参数

        Returns:
            {"success": bool, "result": Dict, "message": str}
        """
        if not self.wps_installed:
            return {
                "success": False,
                "error": "wps-office-suite 未安装",
                "hint": "请安装 wps-office-suite 后使用本地分析功能",
            }

        # 获取映射
        mapping = self.mapping.get_mapping(file_id)
        if not mapping:
            return {
                "success": False,
                "error": f"未找到文档映射: {file_id}",
                "hint": "请先调用 downstream_download 下载文档",
            }

        local_path = mapping["local_path"]
        if not os.path.exists(local_path):
            return {
                "success": False,
                "error": f"本地文件不存在: {local_path}",
            }

        # 构建 JSON 契约
        contract = {
            "action": action,
            "input": local_path,
            "output": local_path + ".out",
            "params": params or {},
        }

        # 选择 wps 脚本
        file_type = mapping.get("file_type", "doc")
        script_name = WPS_SCRIPTS.get(file_type, "wps_common.py")
        script_path = os.path.join(self.scripts_dir, script_name)

        if not os.path.exists(script_path):
            return {
                "success": False,
                "error": f"wps 脚本不存在: {script_path}",
            }

        # 执行子进程
        input_json = json.dumps(contract, ensure_ascii=False)
        result = self.runner.run(
            ["python", script_path, "--bridge-stdin"],
            input_data=input_json,
            timeout=SUBPROCESS_TIMEOUT,
        )

        if result["timed_out"]:
            self.mapping.log_sync(file_id, action, "downstream", "timeout", "子进程超时")
            return {
                "success": False,
                "error": f"wps 处理超时（{SUBPROCESS_TIMEOUT}秒）",
                "hint": "文档过大或操作复杂，请分批处理",
            }

        if not result["success"]:
            self.mapping.log_sync(file_id, action, "downstream", "error", result["stderr"])
            return {
                "success": False,
                "error": f"wps 处理失败: {result['stderr']}",
            }

        # 解析结果
        try:
            output = json.loads(result["stdout"]) if result["stdout"] else {}
        except json.JSONDecodeError:
            output = {"raw_output": result["stdout"]}

        self.mapping.log_sync(file_id, action, "downstream", "success", str(output)[:200])

        return {
            "success": True,
            "file_id": file_id,
            "action": action,
            "result": output,
            "message": f"wps 处理完成: {action}",
        }

    def downstream_upload(self, file_id: str, local_path: str = "") -> Dict:
        """下行：将处理后的结果上传覆盖云端

        Args:
            file_id: 云端文档 ID
            local_path: 本地文件路径（空则使用映射中的路径）

        Returns:
            {"success": bool, "message": str}
        """
        if self._local_mode:
            return {
                "success": False,
                "error": "本地降级模式：无法上传",
            }

        if not local_path:
            mapping = self.mapping.get_mapping(file_id)
            if not mapping:
                return {
                    "success": False,
                    "error": f"未找到文档映射: {file_id}",
                }
            local_path = mapping["local_path"]

        if not os.path.exists(local_path):
            return {
                "success": False,
                "error": f"本地文件不存在: {local_path}",
            }

        try:
            result = self.backend.kdoc_file_upload(local_path)
            self.mapping.log_sync(file_id, "upload", "downstream", "success", f"上传 {local_path}")
            return {
                "success": True,
                "file_id": file_id,
                "message": f"文档已上传覆盖: {local_path}",
            }
        except Exception as e:
            self.mapping.log_sync(file_id, "upload", "downstream", "error", str(e))
            return {
                "success": False,
                "error": f"上传失败: {e}",
            }

    # ===========================================================================
    # 上行：本地 mtime 变化 → 上传同步
    # ===========================================================================

    def upstream_check(self, doc_id: str) -> Dict:
        """上行：检查本地文件是否变化

        Args:
            doc_id: 云端文档 ID

        Returns:
            {"changed": bool, "current_mtime": float, "stored_mtime": float}
        """
        mapping = self.mapping.get_mapping(doc_id)
        if not mapping:
            return {"changed": False, "error": "未找到映射"}

        local_path = mapping["local_path"]
        if not os.path.exists(local_path):
            return {"changed": False, "error": "本地文件不存在"}

        current_mtime = os.path.getmtime(local_path)
        stored_mtime = mapping.get("mtime", 0)

        return {
            "changed": current_mtime > stored_mtime,
            "current_mtime": current_mtime,
            "stored_mtime": stored_mtime,
        }

    def upstream_sync(self, doc_id: str) -> Dict:
        """上行：同步本地文件到云端

        Args:
            doc_id: 云端文档 ID

        Returns:
            {"success": bool, "message": str}
        """
        check = self.upstream_check(doc_id)
        if not check.get("changed"):
            return {
                "success": True,
                "message": "文件未变化，无需同步",
                "synced": False,
            }

        mapping = self.mapping.get_mapping(doc_id)
        local_path = mapping["local_path"]

        result = self.downstream_upload(doc_id, local_path)
        if result.get("success"):
            # 更新 mtime
            new_mtime = os.path.getmtime(local_path)
            self.mapping.update_mtime(doc_id, new_mtime)
            self.mapping.log_sync(file_id, "sync", "upstream", "success", "mtime 变化同步")

        return {**result, "synced": result.get("success")}

    def upstream_sync_all(self) -> Dict:
        """上行：同步所有变化的本地文件

        Returns:
            {"total": int, "synced": int, "failed": int, "details": [...]}
        """
        mappings = self.mapping.get_all_mappings()
        synced = 0
        failed = 0
        details = []

        for mapping in mappings:
            doc_id = mapping["doc_id"]
            result = self.upstream_sync(doc_id)
            if result.get("synced"):
                synced += 1
            elif result.get("error"):
                failed += 1
            details.append({"doc_id": doc_id, **result})

        return {
            "total": len(mappings),
            "synced": synced,
            "failed": failed,
            "details": details,
        }

    # ===========================================================================
    # 监听器：后台线程定期检查 mtime
    # ===========================================================================

    def start_listener(self, interval: int = 30) -> Dict:
        """启动 mtime 监听器（后台线程）

        Args:
            interval: 检查间隔（秒）

        Returns:
            {"success": bool, "message": str}
        """
        if hasattr(self, '_listener_thread') and self._listener_thread.is_alive():
            return {"success": False, "message": "监听器已在运行"}

        self._listener_running = True

        def _listen():
            while self._listener_running:
                try:
                    self.upstream_sync_all()
                except Exception:
                    pass
                time.sleep(interval)

        self._listener_thread = threading.Thread(target=_listen, daemon=True)
        self._listener_thread.start()
        return {
            "success": True,
            "message": f"监听器已启动（间隔 {interval} 秒）",
            "interval": interval,
        }

    def stop_listener(self) -> Dict:
        """停止 mtime 监听器"""
        self._listener_running = False
        if hasattr(self, '_listener_thread'):
            self._listener_thread.join(timeout=5)
        return {"success": True, "message": "监听器已停止"}


def get_local_bridge(backend: Optional[Any] = None) -> LocalBridge:
    """获取本地桥接实例"""
    return LocalBridge(backend=backend)


def detect_wps() -> Dict:
    """便捷函数：探测 wps-office-suite"""
    return {
        "installed": WpsDetector.is_installed(),
        "path": WpsDetector.detect(),
    }
