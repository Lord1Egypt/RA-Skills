#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MiniVCS Skill - 轻量级文件版本管理系统
- 修改：保存增量 Diff + 修改前完整快照（支持回滚）
- 删除：保存完整文件到 trash（支持恢复）

留存策略：
- 普通文件：7 天
- 重要文件：14 天（系统路径、配置文件、入口文件等）

每次 record 操作后，自动扫描整体记录表（从早到晚），
返回已到期可清理的记录列表，供 Agent 向用户确认。
"""

import os
import sys
import json
import time
import shutil
import difflib
import argparse
from datetime import datetime
from typing import List, Dict, Any, Optional

# -------------------------------------------------------------------
# 重要文件判定规则
# -------------------------------------------------------------------
IMPORTANT_PATH_PREFIXES = [
    "/etc/",
    "/root/",
    "/usr/local/etc/",
    "/opt/",
]

IMPORTANT_FILENAME_PATTERNS = [
    # 配置文件后缀
    ".yaml",
    ".yml",
    ".toml",
    ".ini",
    ".cfg",
    ".conf",
    ".env",
    # 常见入口文件名（精确匹配）
    "main.py",
    "app.py",
    "server.py",
    "wsgi.py",
    "asgi.py",
    "index.ts",
    "index.js",
    "main.ts",
    "main.go",
    "main.rs",
    "manage.py",
    "settings.py",
    "config.py",
    "dockerfile",
    "docker-compose.yml",
    "docker-compose.yaml",
    "makefile",
    "cmakelists.txt",
]

RETENTION_NORMAL_DAYS = 7
RETENTION_IMPORTANT_DAYS = 14


def is_important_file(file_path: str) -> bool:
    """判断文件是否为重要文件（需要更长留存期）"""
    abs_path = os.path.abspath(file_path)
    home_dir = os.path.expanduser("~")

    # macOS/Linux：home 目录下的文件视为重要
    if abs_path.startswith(home_dir + os.sep):
        return True

    # Windows：C 盘视为重要
    if sys.platform == "win32" and (abs_path.lower().startswith("c:\\") or abs_path.lower().startswith("c:/")):
        return True

    # 系统路径前缀
    for prefix in IMPORTANT_PATH_PREFIXES:
        if abs_path.startswith(prefix):
            return True

    # 文件名模式（小写匹配）
    filename = os.path.basename(abs_path).lower()
    for pattern in IMPORTANT_FILENAME_PATTERNS:
        if filename == pattern or filename.endswith(pattern):
            return True

    return False


def get_retention_days(file_path: str) -> int:
    """根据文件重要性返回留存天数"""
    return RETENTION_IMPORTANT_DAYS if is_important_file(file_path) else RETENTION_NORMAL_DAYS


def _make_safe_path(relative_path: str) -> str:
    """
    将相对路径转换为可用于文件名的安全字符串。
    使用完整相对路径（非仅文件名），避免同名文件冲突。
    """
    return relative_path.replace(os.sep, "__").replace("/", "__")


# -------------------------------------------------------------------
# LogManager
# -------------------------------------------------------------------


class LogManager:
    """日志管理器 - 负责JSON格式的变更记录读写操作"""

    def __init__(self, vcs_root: str):
        self.vcs_root = vcs_root
        self.log_file = os.path.join(vcs_root, "logs.json")
        self._ensure_log_file()

    def _ensure_log_file(self):
        if not os.path.exists(self.log_file):
            os.makedirs(os.path.dirname(self.log_file), exist_ok=True)
            with open(self.log_file, "w", encoding="utf-8") as f:
                json.dump({"version": "1.0", "records": []}, f, ensure_ascii=False, indent=2)

    def _read_log(self) -> Dict[str, Any]:
        try:
            with open(self.log_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {"version": "1.0", "records": []}

    def _write_log(self, data: Dict[str, Any]):
        # 原子写入：先写临时文件，再 rename，防止进程崩溃损坏 logs.json
        tmp_file = self.log_file + ".tmp"
        with open(tmp_file, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp_file, self.log_file)

    def append_record(self, record: Dict[str, Any]) -> str:
        data = self._read_log()
        record_id = record.get("recordId", f"{int(time.time() * 1000)}")
        record["recordId"] = record_id

        now_ms = int(time.time() * 1000)
        if "timestamp" not in record:
            record["timestamp"] = now_ms
        if "datetime" not in record:
            record["datetime"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # 若未设置 expireAt，根据 retentionDays 自动计算
        if "expireAt" not in record:
            retention_days = record.get("retentionDays", RETENTION_NORMAL_DAYS)
            record["expireAt"] = record["timestamp"] + retention_days * 24 * 60 * 60 * 1000
        if "expireAtDatetime" not in record:
            record["expireAtDatetime"] = datetime.fromtimestamp(record["expireAt"] / 1000).strftime("%Y-%m-%d %H:%M:%S")

        data["records"].append(record)
        self._write_log(data)
        return record_id

    def update_record(self, record_id: str, updates: Dict[str, Any]) -> bool:
        """更新指定记录的字段"""
        data = self._read_log()
        for record in data["records"]:
            if record.get("recordId") == record_id:
                record.update(updates)
                self._write_log(data)
                return True
        return False

    def get_history_by_file(self, file_path: str, descending: bool = True) -> List[Dict[str, Any]]:
        data = self._read_log()
        records = [r for r in data["records"] if r.get("filePath") == file_path]
        records.sort(key=lambda x: x.get("timestamp", 0), reverse=descending)
        return records

    def get_all_history(self, descending: bool = True) -> List[Dict[str, Any]]:
        data = self._read_log()
        records = list(data["records"])
        records.sort(key=lambda x: x.get("timestamp", 0), reverse=descending)
        return records

    def get_due_for_cleanup(self) -> List[Dict[str, Any]]:
        """
        返回已到期（expireAt <= 当前时间）的记录，按 expireAt 从早到晚排序。
        跳过已恢复/已回滚的记录。
        """
        data = self._read_log()
        current_time = int(time.time() * 1000)
        skip_actions = {"RESTORED", "ROLLED_BACK"}
        due = [
            r
            for r in data["records"]
            if r.get("expireAt") is not None and r["expireAt"] <= current_time and r.get("action") not in skip_actions
        ]
        due.sort(key=lambda x: x.get("expireAt", 0))
        return due

    def extend_record_expiry(self, record_id: str, additional_ms: int) -> bool:
        """将指定记录的 expireAt 延后 additional_ms 毫秒"""
        data = self._read_log()
        for record in data["records"]:
            if record.get("recordId") == record_id:
                record["expireAt"] = record.get("expireAt", int(time.time() * 1000)) + additional_ms
                record["expireAtDatetime"] = datetime.fromtimestamp(record["expireAt"] / 1000).strftime("%Y-%m-%d %H:%M:%S")
                self._write_log(data)
                return True
        return False

    def get_expired_records(self, days: int) -> List[Dict[str, Any]]:
        """兼容旧接口：按固定天数查过期记录"""
        data = self._read_log()
        current_time = int(time.time() * 1000)
        expire_ms = days * 24 * 60 * 60 * 1000
        return [r for r in data["records"] if current_time - r.get("timestamp", 0) > expire_ms]

    def delete_record(self, record_id: str) -> bool:
        data = self._read_log()
        original_count = len(data["records"])
        data["records"] = [r for r in data["records"] if r.get("recordId") != record_id]
        if len(data["records"]) < original_count:
            self._write_log(data)
            return True
        return False

    def clean_expired_records(self, days: int) -> Dict[str, Any]:
        expired = self.get_expired_records(days)
        deleted_count = sum(1 for r in expired if self.delete_record(r.get("recordId", "")))
        return {"deleted_count": deleted_count, "deleted_records": expired}

    def get_record_by_id(self, record_id: str) -> Optional[Dict[str, Any]]:
        data = self._read_log()
        for record in data["records"]:
            if record.get("recordId") == record_id:
                return record
        return None


# -------------------------------------------------------------------
# DiffEngine
# -------------------------------------------------------------------


class DiffEngine:
    """Diff引擎 - 生成文件变更差异"""

    @staticmethod
    def generate_diff(old_content: str, new_content: str, context: int = 3) -> str:
        old_lines = old_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)
        diff = difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile="original",
            tofile="modified",
            lineterm="\n",
            n=context,
        )
        return "".join(diff)

    @staticmethod
    def parse_diff_summary(diff_text: str) -> Dict[str, int]:
        added = removed = 0
        for line in diff_text.splitlines():
            if line.startswith("+") and not line.startswith("+++"):
                added += 1
            elif line.startswith("-") and not line.startswith("---"):
                removed += 1
        return {
            "added": added,
            "removed": removed,
            "summary": f"+{added} lines, -{removed} lines" if added or removed else "No changes",
        }


# -------------------------------------------------------------------
# FileManager
# -------------------------------------------------------------------


class FileManager:
    """文件管理器 - 负责物理文件操作"""

    def __init__(self, vcs_root: str, project_root: str):
        self.vcs_root = vcs_root
        self.project_root = project_root
        self.trash_dir = os.path.join(vcs_root, "trash")
        self.diffs_dir = os.path.join(vcs_root, "diffs")
        self.bases_dir = os.path.join(vcs_root, "bases")
        self.snapshots_dir = os.path.join(vcs_root, "snapshots")  # 文本文件修改前完整快照，用于回滚
        self.backups_dir = os.path.join(vcs_root, "backups")  # 二进制文件完整副本备份
        os.makedirs(self.trash_dir, exist_ok=True)
        os.makedirs(self.diffs_dir, exist_ok=True)
        os.makedirs(self.bases_dir, exist_ok=True)
        os.makedirs(self.snapshots_dir, exist_ok=True)
        os.makedirs(self.backups_dir, exist_ok=True)

    def get_file_content(self, file_path: str) -> Optional[str]:
        if not os.path.exists(file_path):
            return None
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            try:
                with open(file_path, "rb") as f:
                    return f.read().decode("utf-8", errors="ignore")
            except Exception:
                return None

    def is_binary_file(self, file_path: str) -> bool:
        """检测是否为二进制文件（简单启发式：读取开头1KB，检查是否含有 NUL 字节）"""
        try:
            with open(file_path, "rb") as f:
                chunk = f.read(1024)
            return b"\x00" in chunk
        except Exception:
            return False

    def save_to_trash(self, file_path: str) -> str:
        """将删除的文件移入 trash 目录（保留完整内容）"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        timestamp = int(time.time() * 1000)
        filename = os.path.basename(file_path)
        trash_filename = f"{timestamp}_{filename}.bak"
        trash_path = os.path.join(self.trash_dir, trash_filename)
        shutil.move(file_path, trash_path)
        return trash_path

    def restore_from_trash(self, trash_path: str, target_path: str) -> bool:
        """从 trash 目录恢复文件（move，原备份消失）"""
        try:
            if not os.path.exists(trash_path):
                return False
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.move(trash_path, target_path)
            return True
        except Exception:
            return False

    def save_binary_backup(self, file_path: str) -> str:
        """将二进制文件完整复制到 backups 目录，以 .bak 扩展名保存（不删除原文件）"""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        timestamp = int(time.time() * 1000)
        filename = os.path.basename(file_path)
        backup_filename = f"{timestamp}_{filename}.bak"
        backup_path = os.path.join(self.backups_dir, backup_filename)
        shutil.copy2(file_path, backup_path)
        return backup_path

    def restore_binary_backup(self, backup_path: str, target_path: str) -> bool:
        """从 backups 目录将 .bak 文件复制回原路径（覆盖当前文件，保留备份）"""
        try:
            if not os.path.exists(backup_path):
                return False
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            shutil.copy2(backup_path, target_path)
            return True
        except Exception:
            return False

    def save_diff(self, relative_path: str, diff_content: str) -> str:
        """保存差异补丁到 diffs 目录，使用完整相对路径命名（避免同名文件冲突）"""
        timestamp = int(time.time() * 1000)
        safe_path = _make_safe_path(relative_path)
        diff_path = os.path.join(self.diffs_dir, f"{timestamp}_{safe_path}.patch")
        with open(diff_path, "w", encoding="utf-8") as f:
            f.write(diff_content)
        return diff_path

    def save_snapshot(self, relative_path: str, content: str) -> str:
        """保存文件修改前的完整快照，用于回滚"""
        timestamp = int(time.time() * 1000)
        safe_path = _make_safe_path(relative_path)
        snap_path = os.path.join(self.snapshots_dir, f"{timestamp}_{safe_path}.snap")
        with open(snap_path, "w", encoding="utf-8") as f:
            f.write(content)
        return snap_path

    def save_base(self, relative_path: str, content: str) -> str:
        """保存当前内容作为下次比较的基准，使用完整相对路径命名"""
        safe_path = _make_safe_path(relative_path)
        base_path = os.path.join(self.bases_dir, f"{safe_path}.base")
        with open(base_path, "w", encoding="utf-8") as f:
            f.write(content)
        return base_path

    def get_base(self, relative_path: str) -> Optional[str]:
        """获取上一次记录的基准内容"""
        safe_path = _make_safe_path(relative_path)
        base_path = os.path.join(self.bases_dir, f"{safe_path}.base")
        return self.get_file_content(base_path)

    def delete_base(self, relative_path: str) -> bool:
        """删除基准文件"""
        safe_path = _make_safe_path(relative_path)
        base_path = os.path.join(self.bases_dir, f"{safe_path}.base")
        if os.path.exists(base_path):
            os.remove(base_path)
            return True
        return False


# -------------------------------------------------------------------
# MiniVCS
# -------------------------------------------------------------------


class MiniVCS:
    """MiniVCS 核心控制器"""

    def __init__(self, project_root: str, vcs_root: Optional[str] = None):
        self.project_root = os.path.abspath(project_root)
        # 默认存储在 ~/.openclaw/minivcs/，与项目目录解耦
        if vcs_root is not None:
            self.vcs_root = os.path.abspath(vcs_root)
        else:
            self.vcs_root = os.path.join(os.path.expanduser("~"), ".openclaw", "minivcs")
        self.log_manager = LogManager(self.vcs_root)
        self.diff_engine = DiffEngine()
        self.file_manager = FileManager(self.vcs_root, self.project_root)

    def _get_relative_path(self, absolute_path: str) -> str:
        if absolute_path.startswith(self.project_root + os.sep):
            return absolute_path[len(self.project_root) + 1 :]
        return absolute_path

    # ------------------------------------------------------------------
    # 核心操作
    # ------------------------------------------------------------------

    def record_modify(self, file_path: str) -> Dict[str, Any]:
        """
        记录文件修改（增量 Diff + 修改前快照）。
        每次编辑后调用一次即可，无需"修改前后各调一次"：
        - 首次调用（无 base）：将当前内容保存为基准，本条记录无快照
        - 后续调用（有 base）：diff = base→当前，snapshot = base（即修改前内容），更新 base
        调用后自动返回已到期待清理的记录列表。

        快照链示意（每次编辑后调一次）：
          初始 C0 → record() → base=C0
          编辑C1  → record() → snapshot=C0, base=C1  (R1, 可回滚到C0)
          编辑C2  → record() → snapshot=C1, base=C2  (R2, 可回滚到C1=t1状态)
          编辑C3  → record() → snapshot=C2, base=C3  (R3, 可回滚到C2=t2状态)
        """
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        # 二进制文件：无法 diff，改用完整副本备份（复制为 .bak，不删除原文件）
        if self.file_manager.is_binary_file(abs_path):
            return self._record_binary_backup(abs_path)

        try:
            new_content = self.file_manager.get_file_content(abs_path)
            if new_content is None:
                return {"success": False, "error": "Cannot read file content"}

            relative_path = self._get_relative_path(abs_path)
            prev_base = self.file_manager.get_base(relative_path)
            old_content = prev_base if prev_base is not None else ""

            diff_text = self.diff_engine.generate_diff(old_content, new_content)
            diff_summary = self.diff_engine.parse_diff_summary(diff_text)

            if old_content != "" and diff_summary["added"] == 0 and diff_summary["removed"] == 0:
                due = self.query_due_for_cleanup()
                return {"success": True, "message": "No changes detected", "skipped": True, "due_for_cleanup": due}

            diff_path = self.file_manager.save_diff(relative_path, diff_text)

            # 有基准时，old_content 就是修改前的内容，保存为快照供回滚使用
            snap_path = None
            if old_content:
                snap_path = self.file_manager.save_snapshot(relative_path, old_content)

            # 更新基准为当前内容
            self.file_manager.save_base(relative_path, new_content)

            retention_days = get_retention_days(abs_path)
            important = is_important_file(abs_path)

            record: Dict[str, Any] = {
                "filePath": relative_path,
                "action": "MODIFY",
                "diffFile": diff_path,
                "summary": diff_summary["summary"],
                "linesAdded": diff_summary["added"],
                "linesRemoved": diff_summary["removed"],
                "isImportant": important,
                "retentionDays": retention_days,
            }
            if snap_path:
                record["snapshotFile"] = snap_path

            record_id = self.log_manager.append_record(record)
            due = self.query_due_for_cleanup()

            return {
                "success": True,
                "recordId": record_id,
                "summary": diff_summary["summary"],
                "diffFile": diff_path,
                "snapshotFile": snap_path,
                "canRollback": snap_path is not None,
                "isImportant": important,
                "retentionDays": retention_days,
                "due_for_cleanup": due,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def _record_binary_backup(self, abs_path: str) -> Dict[str, Any]:
        """二进制文件备份：将当前文件完整复制为 .bak，保留原文件，支持后续还原。"""
        try:
            relative_path = self._get_relative_path(abs_path)
            important = is_important_file(abs_path)
            retention_days = get_retention_days(abs_path)

            backup_path = self.file_manager.save_binary_backup(abs_path)
            file_size = os.path.getsize(abs_path)

            record = {
                "filePath": relative_path,
                "action": "BINARY_BACKUP",
                "backupFile": backup_path,
                "summary": f"Binary file backup ({file_size} bytes)",
                "isImportant": important,
                "retentionDays": retention_days,
            }

            record_id = self.log_manager.append_record(record)
            due = self.query_due_for_cleanup()

            return {
                "success": True,
                "recordId": record_id,
                "backupFile": backup_path,
                "summary": record["summary"],
                "canRollback": True,
                "isImportant": important,
                "retentionDays": retention_days,
                "due_for_cleanup": due,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def record_delete(self, file_path: str) -> Dict[str, Any]:
        """
        记录文件删除（文件移入 trash）。
        调用后自动返回已到期待清理的记录列表。
        """
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            return {"success": False, "error": f"File not found: {file_path}"}

        try:
            relative_path = self._get_relative_path(abs_path)
            important = is_important_file(abs_path)
            retention_days = get_retention_days(abs_path)

            trash_path = self.file_manager.save_to_trash(abs_path)

            record = {
                "filePath": relative_path,
                "action": "DELETE",
                "trashFile": trash_path,
                "summary": "File moved to trash",
                "isImportant": important,
                "retentionDays": retention_days,
            }

            record_id = self.log_manager.append_record(record)
            due = self.query_due_for_cleanup()

            return {
                "success": True,
                "recordId": record_id,
                "trashFile": trash_path,
                "message": "File deleted and backed up to trash",
                "isImportant": important,
                "retentionDays": retention_days,
                "due_for_cleanup": due,
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    # ------------------------------------------------------------------
    # 恢复 / 回滚
    # ------------------------------------------------------------------

    def restore_file(self, record_id: str) -> Dict[str, Any]:
        """
        恢复文件：
        - DELETE 记录：从 trash 恢复完整文件
        - MODIFY 记录：从修改前快照回滚到修改前状态
        成功后将记录标记为 RESTORED / ROLLED_BACK。
        """
        record = self.log_manager.get_record_by_id(record_id)
        if not record:
            return {"success": False, "error": "Record not found"}

        action = record.get("action")

        if action == "DELETE":
            trash_file = record.get("trashFile")
            if not trash_file or not os.path.exists(trash_file):
                return {"success": False, "error": "Backup file not found (may have been cleaned up)"}
            # filePath 可能是相对路径或绝对路径
            file_path = record.get("filePath", "")
            target_path = file_path if os.path.isabs(file_path) else os.path.join(self.project_root, file_path)
            success = self.file_manager.restore_from_trash(trash_file, target_path)
            if success:
                # 标记记录为已恢复，防止重复恢复或出现在 trash 列表
                self.log_manager.update_record(
                    record_id,
                    {
                        "action": "RESTORED",
                        "restoredAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "trashFile": None,
                    },
                )
                return {"success": True, "message": f"File restored to: {target_path}"}
            return {"success": False, "error": "Failed to restore file from trash"}

        elif action == "MODIFY":
            snap_file = record.get("snapshotFile")
            if not snap_file or not os.path.exists(snap_file):
                return {
                    "success": False,
                    "error": (
                        "No pre-edit snapshot available for this record. "
                        "Rollback is only possible when record_modify was called "
                        "both before AND after the edit."
                    ),
                }
            content = self.file_manager.get_file_content(snap_file)
            if content is None:
                return {"success": False, "error": "Cannot read snapshot file"}
            file_path = record.get("filePath", "")
            target_path = file_path if os.path.isabs(file_path) else os.path.join(self.project_root, file_path)
            os.makedirs(os.path.dirname(target_path), exist_ok=True)
            with open(target_path, "w", encoding="utf-8") as f:
                f.write(content)
            self.log_manager.update_record(
                record_id,
                {
                    "action": "ROLLED_BACK",
                    "rolledBackAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                },
            )
            return {"success": True, "message": f"File rolled back to pre-edit state: {target_path}"}

        elif action == "BINARY_BACKUP":
            backup_file = record.get("backupFile")
            if not backup_file or not os.path.exists(backup_file):
                return {"success": False, "error": "Backup file not found (may have been cleaned up)"}
            file_path = record.get("filePath", "")
            target_path = file_path if os.path.isabs(file_path) else os.path.join(self.project_root, file_path)
            success = self.file_manager.restore_binary_backup(backup_file, target_path)
            if success:
                self.log_manager.update_record(
                    record_id,
                    {
                        "action": "ROLLED_BACK",
                        "rolledBackAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    },
                )
                return {"success": True, "message": f"Binary file restored to: {target_path}"}
            return {"success": False, "error": "Failed to restore binary backup"}

        elif action in ("RESTORED", "ROLLED_BACK"):
            return {"success": False, "error": f"This record has already been {action.lower()}"}

        return {"success": False, "error": f"Unknown action: {action}"}

    # ------------------------------------------------------------------
    # 到期清理管理
    # ------------------------------------------------------------------

    def query_due_for_cleanup(self) -> List[Dict[str, Any]]:
        """
        扫描整体记录表，从早到晚返回 expireAt <= 当前时间 的记录列表。
        已恢复/回滚的记录不包含在内。
        """
        return self.log_manager.get_due_for_cleanup()

    def extend_record_expiry(self, record_id: str) -> Dict[str, Any]:
        """将指定记录的过期时间延后一个留存周期（retentionDays 天）"""
        record = self.log_manager.get_record_by_id(record_id)
        if not record:
            return {"success": False, "error": "Record not found"}

        retention_days = record.get("retentionDays", RETENTION_NORMAL_DAYS)
        additional_ms = retention_days * 24 * 60 * 60 * 1000
        ok = self.log_manager.extend_record_expiry(record_id, additional_ms)
        if ok:
            updated = self.log_manager.get_record_by_id(record_id)
            return {
                "success": True,
                "recordId": record_id,
                "newExpireAt": updated.get("expireAt"),
                "newExpireAtDatetime": updated.get("expireAtDatetime"),
                "message": f"Expiry extended by {retention_days} days",
            }
        return {"success": False, "error": "Failed to extend expiry"}

    def delete_due_records(self, record_ids: List[str]) -> Dict[str, Any]:
        """批量删除用户已确认可清理的到期记录（日志 + 物理文件）"""
        deleted_records = []
        failed_records = []
        deleted_files: List[str] = []

        for record_id in record_ids:
            result = self.delete_record_by_id(record_id, delete_files=True)
            if result.get("success"):
                deleted_records.append(record_id)
                deleted_files.extend(result.get("deleted_files", []))
            else:
                failed_records.append({"recordId": record_id, "error": result.get("error")})

        return {
            "success": True,
            "deleted_count": len(deleted_records),
            "deleted_records": deleted_records,
            "failed_records": failed_records,
            "deleted_files": deleted_files,
        }

    # ------------------------------------------------------------------
    # 查询 / 历史
    # ------------------------------------------------------------------

    def get_history(self, file_path: Optional[str] = None, limit: int = 10) -> List[Dict[str, Any]]:
        if file_path:
            abs_path = os.path.abspath(file_path)
            relative_path = self._get_relative_path(abs_path)
            history = self.log_manager.get_history_by_file(relative_path)
        else:
            history = self.log_manager.get_all_history()
        return history[:limit]

    def get_file_diff(self, record_id: str) -> Optional[str]:
        record = self.log_manager.get_record_by_id(record_id)
        if not record or record.get("action") != "MODIFY":
            return None
        diff_file = record.get("diffFile")
        if not diff_file or not os.path.exists(diff_file):
            return None
        return self.file_manager.get_file_content(diff_file)

    def query_expired(self, days: int) -> List[Dict[str, Any]]:
        """兼容旧接口：按固定天数查过期记录"""
        return self.log_manager.get_expired_records(days)

    def clean_expired(self, days: int, delete_files: bool = False) -> Dict[str, Any]:
        """兼容旧接口：清理过期记录"""
        expired = self.log_manager.get_expired_records(days)
        deleted_files = []
        if delete_files:
            for record in expired:
                diff_file = record.get("diffFile")
                if diff_file and os.path.exists(diff_file):
                    os.remove(diff_file)
                    deleted_files.append(diff_file)
        result = self.log_manager.clean_expired_records(days)
        result["deleted_files"] = deleted_files
        return result

    def list_trash(self) -> List[Dict[str, Any]]:
        """列出 trash 中尚未恢复的已删除文件"""
        records = self.log_manager.get_all_history()
        return [
            {
                "recordId": r.get("recordId"),
                "filePath": r.get("filePath"),
                "datetime": r.get("datetime"),
                "trashFile": r.get("trashFile"),
                "isImportant": r.get("isImportant", False),
                "retentionDays": r.get("retentionDays", RETENTION_NORMAL_DAYS),
                "expireAtDatetime": r.get("expireAtDatetime"),
            }
            for r in records
            if r.get("action") == "DELETE"
        ]

    def delete_record_by_id(self, record_id: str, delete_files: bool = True) -> Dict[str, Any]:
        """删除指定记录（日志 + 物理文件）"""
        record = self.log_manager.get_record_by_id(record_id)
        if not record:
            return {"success": False, "error": "Record not found"}

        deleted_files = []

        if delete_files:
            # 删除 diff 文件
            diff_file = record.get("diffFile")
            if diff_file and os.path.exists(diff_file):
                os.remove(diff_file)
                deleted_files.append(diff_file)

            # 删除 trash 备份
            trash_file = record.get("trashFile")
            if trash_file and os.path.exists(trash_file):
                os.remove(trash_file)
                deleted_files.append(trash_file)

            # 删除快照文件
            snap_file = record.get("snapshotFile")
            if snap_file and os.path.exists(snap_file):
                os.remove(snap_file)
                deleted_files.append(snap_file)

            # 删除二进制备份文件
            backup_file = record.get("backupFile")
            if backup_file and os.path.exists(backup_file):
                os.remove(backup_file)
                deleted_files.append(backup_file)

            # 仅当该文件没有其他 MODIFY 记录时才删除 base 文件
            file_path = record.get("filePath")
            if file_path and record.get("action") == "MODIFY":
                remaining = [
                    r
                    for r in self.log_manager.get_history_by_file(file_path)
                    if r.get("action") == "MODIFY" and r.get("recordId") != record_id
                ]
                if not remaining:
                    self.file_manager.delete_base(file_path)

        self.log_manager.delete_record(record_id)
        return {
            "success": True,
            "deleted_record": record_id,
            "deleted_files": deleted_files,
            "message": f"Record {record_id} deleted",
        }

    def merge_modify(self, file_path: str, keep_record_id: Optional[str] = None) -> Dict[str, Any]:
        """合并同一文件的多次修改记录，默认保留最新一条"""
        abs_path = os.path.abspath(file_path)
        relative_path = self._get_relative_path(abs_path)

        records = self.log_manager.get_history_by_file(relative_path, descending=True)
        modify_records = [r for r in records if r.get("action") == "MODIFY"]

        if len(modify_records) <= 1:
            return {"success": False, "error": "No need to merge (only one or zero record)"}

        if keep_record_id:
            keep_record = next((r for r in modify_records if r.get("recordId") == keep_record_id), None)
            if not keep_record:
                return {"success": False, "error": "Record not found"}
        else:
            keep_record = modify_records[0]

        deleted_count = 0
        deleted_files = []
        for r in modify_records:
            if r.get("recordId") == keep_record.get("recordId"):
                continue
            if self.log_manager.delete_record(r.get("recordId")):
                deleted_count += 1
            for fkey in ("diffFile", "snapshotFile"):
                f = r.get(fkey)
                if f and os.path.exists(f):
                    os.remove(f)
                    deleted_files.append(f)

        return {
            "success": True,
            "kept_record": keep_record.get("recordId"),
            "deleted_count": deleted_count,
            "deleted_files": deleted_files,
            "message": f"Merged {deleted_count} records, kept latest: {keep_record.get('recordId')}",
        }


# -------------------------------------------------------------------
# CLI 输出辅助
# -------------------------------------------------------------------


def print_records(records: list, show_diff: bool = False, vcs: Optional[MiniVCS] = None):
    if not records:
        print("No records found.")
        return
    for i, record in enumerate(records):
        important_tag = " [IMPORTANT]" if record.get("isImportant") else ""
        action = record.get("action", "")
        rollback_tag = " [rollback available]" if action == "MODIFY" and record.get("snapshotFile") else ""
        print(f"\n[{i + 1}] Record ID: {record.get('recordId')}")
        print(f"    File    : {record.get('filePath')}{important_tag}")
        print(f"    Action  : {action}{rollback_tag}")
        print(f"    Time    : {record.get('datetime')}")
        print(f"    Summary : {record.get('summary')}")
        print(f"    Expires : {record.get('expireAtDatetime', 'N/A')}  (retention {record.get('retentionDays', '?')}d)")
        if show_diff and vcs and action == "MODIFY":
            diff_content = vcs.get_file_diff(record.get("recordId"))
            if diff_content:
                print("\n    Diff Content:")
                print("    " + "-" * 40)
                for line in diff_content.splitlines()[:30]:
                    print(f"    {line}")


def print_due_for_cleanup(due: list):
    if not due:
        return
    print(f"\n{'=' * 50}")
    print(f"  [CLEANUP NOTICE] {len(due)} record(s) have expired and are pending cleanup:")
    for i, r in enumerate(due):
        important_tag = " [IMPORTANT]" if r.get("isImportant") else ""
        print(f"  [{i + 1}] ID={r.get('recordId')}  File={r.get('filePath')}{important_tag}")
        print(f"       Action={r.get('action')}  Created={r.get('datetime')}  Expired={r.get('expireAtDatetime')}")
    print("  Use 'cleanup --confirm' to delete, or 'extend <record_id>' to postpone.")
    print(f"{'=' * 50}")


# -------------------------------------------------------------------
# CLI 入口
# -------------------------------------------------------------------


def main():
    parser = argparse.ArgumentParser(description="MiniVCS - 轻量级文件版本管理系统")
    parser.add_argument(
        "command",
        choices=["record", "delete", "history", "restore", "expired", "trash", "remove", "cleanup", "extend"],
        help="命令",
    )
    parser.add_argument("file", nargs="?", help="文件路径 或 Record ID")
    parser.add_argument("-n", "--limit", type=int, default=10, help="记录数量限制")
    parser.add_argument("-d", "--show-diff", action="store_true", help="显示差异内容")
    parser.add_argument("-c", "--clean", action="store_true", help="清理过期记录（配合 expired 命令）")
    parser.add_argument("--delete-files", action="store_true", help="同时删除物理文件")
    parser.add_argument("--confirm", action="store_true", help="确认执行清理（配合 cleanup 命令）")
    parser.add_argument("--project-root", default=os.getcwd(), help="项目根目录（用于计算相对路径）")
    parser.add_argument("--vcs-root", default=None, help="VCS 数据存储目录（默认 ~/.openclaw/minivcs）")

    args = parser.parse_args()

    try:
        vcs = MiniVCS(args.project_root, vcs_root=args.vcs_root)
    except Exception as e:
        print(f"Error: Failed to initialize MiniVCS: {e}")
        return 1

    if args.command == "record":
        if not args.file:
            print("Error: Please specify a file to record")
            return 1
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            return 1
        result = vcs.record_modify(args.file)
        if result.get("success"):
            if result.get("skipped"):
                print("~ No changes detected, skipped.")
            elif result.get("action") == "BINARY_BACKUP" or result.get("backupFile"):
                print("✓ Binary file backed up! (.bak copy saved)")
                print(f"  Record ID  : {result.get('recordId')}")
                print(f"  Backup     : {result.get('backupFile')}")
                print(f"  Summary    : {result.get('summary')}")
                important_tag = " [IMPORTANT]" if result.get("isImportant") else ""
                print(f"  Retention  : {result.get('retentionDays')} days{important_tag}")
                print(f"  Rollback   : available (use restore {result.get('recordId')})")
            else:
                print("✓ File change recorded!")
                print(f"  Record ID  : {result.get('recordId')}")
                print(f"  Summary    : {result.get('summary')}")
                important_tag = " [IMPORTANT]" if result.get("isImportant") else ""
                print(f"  Retention  : {result.get('retentionDays')} days{important_tag}")
                if result.get("canRollback"):
                    print(f"  Rollback   : available (use restore {result.get('recordId')})")
            print_due_for_cleanup(result.get("due_for_cleanup", []))
        else:
            print(f"✗ Failed: {result.get('error')}")
            return 1

    elif args.command == "delete":
        if not args.file:
            print("Error: Please specify a file to delete")
            return 1
        if not os.path.exists(args.file):
            print(f"Error: File not found: {args.file}")
            return 1
        result = vcs.record_delete(args.file)
        if result.get("success"):
            print("✓ File deleted and backed up!")
            print(f"  Record ID  : {result.get('recordId')}")
            print(f"  Backup     : {result.get('trashFile')}")
            important_tag = " [IMPORTANT]" if result.get("isImportant") else ""
            print(f"  Retention  : {result.get('retentionDays')} days{important_tag}")
            print_due_for_cleanup(result.get("due_for_cleanup", []))
        else:
            print(f"✗ Failed: {result.get('error')}")
            return 1

    elif args.command == "history":
        records = vcs.get_history(args.file, args.limit)
        if args.file:
            print(f"\n=== History for: {args.file} ===")
        else:
            print(f"\n=== All History (latest {args.limit} records) ===")
        print_records(records, args.show_diff, vcs)

    elif args.command == "restore":
        if not args.file:
            print("Error: Please specify a record ID to restore/rollback")
            return 1
        result = vcs.restore_file(args.file)
        if result.get("success"):
            print(f"✓ {result.get('message')}")
        else:
            print(f"✗ Failed: {result.get('error')}")
            return 1

    elif args.command == "expired":
        if not args.file:
            print("Error: Please specify number of days")
            return 1
        try:
            days = int(args.file)
        except ValueError:
            print("Error: Days must be a number")
            return 1
        if args.clean:
            result = vcs.clean_expired(days, args.delete_files)
            print(f"\n=== Cleaned Expired Records (>{days} days) ===")
            print(f"Records deleted: {result.get('deleted_count')}")
            if args.delete_files and result.get("deleted_files"):
                print(f"Diff files deleted: {len(result.get('deleted_files', []))}")
        else:
            records = vcs.query_expired(days)
            print(f"\n=== Expired Records (>{days} days) ===")
            print(f"Total: {len(records)} records")
            print_records(records)

    elif args.command == "trash":
        files = vcs.list_trash()
        print("\n=== Trash Bin ===")
        if not files:
            print("Trash is empty.")
            return 0
        for i, f in enumerate(files):
            important_tag = " [IMPORTANT]" if f.get("isImportant") else ""
            print(f"\n[{i + 1}] {f.get('filePath')}{important_tag}")
            print(f"    Deleted at : {f.get('datetime')}")
            print(f"    Expires at : {f.get('expireAtDatetime', 'N/A')}")
            print(f"    Record ID  : {f.get('recordId')}")

    elif args.command == "remove":
        if not args.file:
            print("Error: Please specify a record ID to remove")
            print("  Use 'history' command to see record IDs")
            return 1
        result = vcs.delete_record_by_id(args.file)
        if result.get("success"):
            print("✓ Record removed successfully!")
            print(f"  {result.get('message')}")
        else:
            print(f"✗ Failed: {result.get('error')}")
            return 1

    elif args.command == "cleanup":
        due = vcs.query_due_for_cleanup()
        if not due:
            print("✓ No records due for cleanup.")
            return 0
        print(f"\n=== Records Due for Cleanup ({len(due)} total, oldest first) ===")
        print_records(due, vcs=vcs)
        if args.confirm:
            record_ids = [r.get("recordId") for r in due]
            result = vcs.delete_due_records(record_ids)
            print(f"\n✓ Cleanup complete: {result.get('deleted_count')} records deleted.")
            if result.get("failed_records"):
                print(f"  Failed: {result.get('failed_records')}")
        else:
            print("\n  To delete these records, run with --confirm")
            print("  To postpone a record, run: extend <record_id>")

    elif args.command == "extend":
        if not args.file:
            print("Error: Please specify a record ID to extend")
            return 1
        result = vcs.extend_record_expiry(args.file)
        if result.get("success"):
            print("✓ Expiry extended!")
            print(f"  Record ID     : {result.get('recordId')}")
            print(f"  New expire at : {result.get('newExpireAtDatetime')}")
            print(f"  {result.get('message')}")
        else:
            print(f"✗ Failed: {result.get('error')}")
            return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
