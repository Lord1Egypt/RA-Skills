"""
记忆版本控制模块

支持记忆版本记录、回滚和比较
"""

import sqlite3
import json
import time
from typing import Dict, List, Optional, Tuple
from pathlib import Path
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class MemoryVersion:
    """记忆版本"""
    version_id: int
    memory_id: int
    version_number: int
    content: str
    metadata: Dict
    changed_at: str
    changed_by: str
    change_reason: str


@dataclass
class VersionDiff:
    """版本差异"""
    old_version: int
    new_version: int
    content_changed: bool
    metadata_changed: bool
    changes: List[str]


class VersionController:
    """版本控制器"""

    def __init__(self, db_path: Optional[str] = None):
        """
        初始化版本控制器

        Args:
            db_path: SQLite 数据库路径
        """
        if db_path is None:
            db_path = str(Path.home() / ".openclaw" / "memory" / "main.sqlite")

        self.db_path = db_path
        self._init_tables()

    def _init_tables(self):
        """初始化版本表"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 创建版本表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_versions (
                version_id INTEGER PRIMARY KEY AUTOINCREMENT,
                memory_id INTEGER NOT NULL,
                version_number INTEGER NOT NULL,
                content TEXT NOT NULL,
                metadata TEXT NOT NULL,
                changed_at TEXT NOT NULL,
                changed_by TEXT NOT NULL,
                change_reason TEXT,
                FOREIGN KEY (memory_id) REFERENCES memories(id)
            )
        """)

        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_versions_memory_id
            ON memory_versions(memory_id)
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_versions_number
            ON memory_versions(memory_id, version_number)
        """)

        conn.commit()
        conn.close()

    def create_version(
        self,
        memory_id: int,
        content: str,
        metadata: Dict,
        changed_by: str = "system",
        change_reason: str = ""
    ) -> int:
        """
        创建新版本

        Args:
            memory_id: 记忆 ID
            content: 记忆内容
            metadata: 元数据
            changed_by: 修改人
            change_reason: 修改原因

        Returns:
            int: 新版本号
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # 获取当前最大版本号
        cursor.execute("""
            SELECT COALESCE(MAX(version_number), 0)
            FROM memory_versions
            WHERE memory_id = ?
        """, (memory_id,))

        current_version = cursor.fetchone()[0]
        new_version = current_version + 1

        # 插入新版本
        cursor.execute("""
            INSERT INTO memory_versions
            (memory_id, version_number, content, metadata, changed_at, changed_by, change_reason)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            memory_id,
            new_version,
            content,
            json.dumps(metadata, ensure_ascii=False),
            datetime.now().isoformat(),
            changed_by,
            change_reason
        ))

        version_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return new_version

    def get_version(self, memory_id: int, version_number: int) -> Optional[MemoryVersion]:
        """
        获取指定版本

        Args:
            memory_id: 记忆 ID
            version_number: 版本号

        Returns:
            MemoryVersion: 版本信息，不存在则返回 None
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT version_id, memory_id, version_number, content, metadata,
                   changed_at, changed_by, change_reason
            FROM memory_versions
            WHERE memory_id = ? AND version_number = ?
        """, (memory_id, version_number))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return MemoryVersion(
            version_id=row['version_id'],
            memory_id=row['memory_id'],
            version_number=row['version_number'],
            content=row['content'],
            metadata=json.loads(row['metadata']),
            changed_at=row['changed_at'],
            changed_by=row['changed_by'],
            change_reason=row['change_reason']
        )

    def get_all_versions(self, memory_id: int) -> List[MemoryVersion]:
        """
        获取所有版本

        Args:
            memory_id: 记忆 ID

        Returns:
            List[MemoryVersion]: 版本列表
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT version_id, memory_id, version_number, content, metadata,
                   changed_at, changed_by, change_reason
            FROM memory_versions
            WHERE memory_id = ?
            ORDER BY version_number ASC
        """, (memory_id,))

        rows = cursor.fetchall()
        conn.close()

        return [
            MemoryVersion(
                version_id=row['version_id'],
                memory_id=row['memory_id'],
                version_number=row['version_number'],
                content=row['content'],
                metadata=json.loads(row['metadata']),
                changed_at=row['changed_at'],
                changed_by=row['changed_by'],
                change_reason=row['change_reason']
            )
            for row in rows
        ]

    def get_latest_version(self, memory_id: int) -> Optional[MemoryVersion]:
        """
        获取最新版本

        Args:
            memory_id: 记忆 ID

        Returns:
            MemoryVersion: 最新版本信息
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("""
            SELECT version_id, memory_id, version_number, content, metadata,
                   changed_at, changed_by, change_reason
            FROM memory_versions
            WHERE memory_id = ?
            ORDER BY version_number DESC
            LIMIT 1
        """, (memory_id,))

        row = cursor.fetchone()
        conn.close()

        if row is None:
            return None

        return MemoryVersion(
            version_id=row['version_id'],
            memory_id=row['memory_id'],
            version_number=row['version_number'],
            content=row['content'],
            metadata=json.loads(row['metadata']),
            changed_at=row['changed_at'],
            changed_by=row['changed_by'],
            change_reason=row['change_reason']
        )

    def compare_versions(
        self,
        memory_id: int,
        version1: int,
        version2: int
    ) -> Optional[VersionDiff]:
        """
        比较两个版本

        Args:
            memory_id: 记忆 ID
            version1: 版本号 1
            version2: 版本号 2

        Returns:
            VersionDiff: 版本差异
        """
        v1 = self.get_version(memory_id, version1)
        v2 = self.get_version(memory_id, version2)

        if v1 is None or v2 is None:
            return None

        content_changed = v1.content != v2.content
        metadata_changed = v1.metadata != v2.metadata

        changes = []

        if content_changed:
            changes.append(f"内容已修改")
            changes.append(f"  旧：{v1.content[:100]}...")
            changes.append(f"  新：{v2.content[:100]}...")

        if metadata_changed:
            changes.append("元数据已修改")
            for key in set(v1.metadata.keys()) | set(v2.metadata.keys()):
                if v1.metadata.get(key) != v2.metadata.get(key):
                    changes.append(f"  {key}: {v1.metadata.get(key)} → {v2.metadata.get(key)}")

        return VersionDiff(
            old_version=version1,
            new_version=version2,
            content_changed=content_changed,
            metadata_changed=metadata_changed,
            changes=changes
        )

    def rollback_to_version(
        self,
        memory_id: int,
        target_version: int,
        changed_by: str = "system",
        change_reason: str = "版本回滚"
    ) -> bool:
        """
        回滚到指定版本

        Args:
            memory_id: 记忆 ID
            target_version: 目标版本号
            changed_by: 修改人
            change_reason: 修改原因

        Returns:
            bool: 是否成功
        """
        target = self.get_version(memory_id, target_version)

        if target is None:
            return False

        # 创建新版本（回滚版本）
        new_version = self.create_version(
            memory_id=memory_id,
            content=target.content,
            metadata=target.metadata,
            changed_by=changed_by,
            change_reason=f"{change_reason} (回滚到 v{target_version})"
        )

        return True


if __name__ == "__main__":
    # 测试版本控制功能
    print("=== 版本控制测试 ===\n")

    controller = VersionController()

    # 创建测试版本
    memory_id = 1

    print("创建版本...")
    v1 = controller.create_version(
        memory_id=memory_id,
        content="初始版本内容",
        metadata={"type": "TEST"},
        changed_by="test_user",
        change_reason="初始创建"
    )
    print(f"  创建版本 v{v1}")

    v2 = controller.create_version(
        memory_id=memory_id,
        content="修改后的内容",
        metadata={"type": "TEST", "updated": True},
        changed_by="test_user",
        change_reason="内容更新"
    )
    print(f"  创建版本 v{v2}")

    # 获取所有版本
    print("\n获取所有版本...")
    versions = controller.get_all_versions(memory_id)
    for version in versions:
        print(f"  v{version.version_number}: {version.content[:30]}... ({version.changed_at})")

    # 比较版本
    print("\n比较版本 v1 和 v2...")
    diff = controller.compare_versions(memory_id, 1, 2)
    if diff:
        print(f"  内容变更：{diff.content_changed}")
        print(f"  元数据变更：{diff.metadata_changed}")
        for change in diff.changes:
            print(f"  {change}")

    # 回滚
    print("\n回滚到 v1...")
    success = controller.rollback_to_version(memory_id, 1, "test_user", "测试回滚")
    print(f"  回滚{'成功' if success else '失败'}")

    # 获取最新版本
    print("\n获取最新版本...")
    latest = controller.get_latest_version(memory_id)
    if latest:
        print(f"  v{latest.version_number}: {latest.content[:30]}...")
        print(f"  原因：{latest.change_reason}")

    print("\n=== 测试完成 ===")
