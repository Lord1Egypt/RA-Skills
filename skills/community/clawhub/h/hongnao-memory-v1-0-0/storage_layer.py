"""
弘脑记忆系统 - 存储层模块
HongNao Memory OS - Storage Layer

负责记忆的持久化存储，包括：
- SQLite 关系型存储（MemCells/MemScenes 元数据）
- ChromaDB 向量存储（语义检索索引）
- Redis 缓存层（热点记忆缓存）
"""

import sqlite3
import json
import hashlib
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path


# ============================================================================
# 数据模型定义
# ============================================================================

@dataclass
class MemCell:
    """记忆颗粒 - 最小记忆存储单元"""
    id: str
    cell_type: str  # fact/preference/skill/emotion/constraint
    content: str
    tags: List[str]
    importance: float  # 1-10
    created_at: str
    updated_at: str
    access_count: int = 0
    last_accessed: Optional[str] = None
    scene_id: Optional[str] = None  # 所属场景 ID
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemCell':
        return cls(**data)


@dataclass
class MemScene:
    """记忆场景 - 围绕主题/人物/任务形成的记忆集合"""
    id: str
    title: str
    scene_type: str  # project/user/task/relationship
    description: str
    cell_ids: List[str]
    created_at: str
    updated_at: str
    activity_score: float = 0.0  # 活跃度 0-100
    last_accessed: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'MemScene':
        return cls(**data)


# ============================================================================
# SQLite 存储层
# ============================================================================

class SQLiteStorage:
    """SQLite 关系型存储"""
    
    def __init__(self, db_path: str = "hongnao_memory.db"):
        self.db_path = Path(db_path)
        self.conn: Optional[sqlite3.Connection] = None
        self._init_db()
    
    def _init_db(self):
        """初始化数据库表结构"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        
        # MemCells 表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mem_cells (
                id TEXT PRIMARY KEY,
                cell_type TEXT NOT NULL,
                content TEXT NOT NULL,
                tags TEXT,  -- JSON 数组
                importance REAL NOT NULL,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                scene_id TEXT,
                metadata TEXT,  -- JSON 对象
                FOREIGN KEY (scene_id) REFERENCES mem_scenes(id)
            )
        ''')
        
        # MemScenes 表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mem_scenes (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                scene_type TEXT NOT NULL,
                description TEXT,
                cell_ids TEXT,  -- JSON 数组
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                activity_score REAL DEFAULT 0.0,
                last_accessed TEXT,
                metadata TEXT  -- JSON 对象
            )
        ''')
        
        # 索引
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cells_type ON mem_cells(cell_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cells_importance ON mem_cells(importance)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_cells_scene ON mem_cells(scene_id)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scenes_type ON mem_scenes(scene_type)')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_scenes_activity ON mem_scenes(activity_score)')
        
        self.conn.commit()
    
    # -------------------- MemCells 操作 --------------------
    
    def create_cell(self, cell: MemCell) -> bool:
        """创建记忆颗粒"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO mem_cells 
                (id, cell_type, content, tags, importance, created_at, updated_at, 
                 access_count, last_accessed, scene_id, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                cell.id, cell.cell_type, cell.content,
                json.dumps(cell.tags), cell.importance,
                cell.created_at, cell.updated_at,
                cell.access_count, cell.last_accessed,
                cell.scene_id, json.dumps(cell.metadata)
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_cell(self, cell_id: str) -> Optional[MemCell]:
        """获取记忆颗粒"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM mem_cells WHERE id = ?', (cell_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_cell(row)
        return None
    
    def update_cell(self, cell: MemCell) -> bool:
        """更新记忆颗粒"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE mem_cells 
            SET content=?, tags=?, importance=?, updated_at=?,
                access_count=?, last_accessed=?, scene_id=?, metadata=?
            WHERE id=?
        ''', (
            cell.content, json.dumps(cell.tags), cell.importance,
            cell.updated_at, cell.access_count, cell.last_accessed,
            cell.scene_id, json.dumps(cell.metadata), cell.id
        ))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_cell(self, cell_id: str) -> bool:
        """删除记忆颗粒"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM mem_cells WHERE id = ?', (cell_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def list_cells(self, 
                   cell_type: Optional[str] = None,
                   scene_id: Optional[str] = None,
                   min_importance: Optional[float] = None,
                   limit: int = 100,
                   offset: int = 0) -> List[MemCell]:
        """查询记忆颗粒列表"""
        cursor = self.conn.cursor()
        
        query = 'SELECT * FROM mem_cells WHERE 1=1'
        params = []
        
        if cell_type:
            query += ' AND cell_type = ?'
            params.append(cell_type)
        
        if scene_id:
            query += ' AND scene_id = ?'
            params.append(scene_id)
        
        if min_importance is not None:
            query += ' AND importance >= ?'
            params.append(min_importance)
        
        query += ' ORDER BY importance DESC, updated_at DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        return [self._row_to_cell(row) for row in cursor.fetchall()]
    
    def _row_to_cell(self, row: sqlite3.Row) -> MemCell:
        """将数据库行转换为 MemCell 对象"""
        return MemCell(
            id=row['id'],
            cell_type=row['cell_type'],
            content=row['content'],
            tags=json.loads(row['tags']) if row['tags'] else [],
            importance=row['importance'],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            access_count=row['access_count'],
            last_accessed=row['last_accessed'],
            scene_id=row['scene_id'],
            metadata=json.loads(row['metadata']) if row['metadata'] else {}
        )
    
    # -------------------- MemScenes 操作 --------------------
    
    def create_scene(self, scene: MemScene) -> bool:
        """创建记忆场景"""
        cursor = self.conn.cursor()
        try:
            cursor.execute('''
                INSERT INTO mem_scenes 
                (id, title, scene_type, description, cell_ids, created_at, updated_at,
                 activity_score, last_accessed, metadata)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                scene.id, scene.title, scene.scene_type, scene.description,
                json.dumps(scene.cell_ids), scene.created_at, scene.updated_at,
                scene.activity_score, scene.last_accessed, json.dumps(scene.metadata)
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_scene(self, scene_id: str) -> Optional[MemScene]:
        """获取记忆场景"""
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM mem_scenes WHERE id = ?', (scene_id,))
        row = cursor.fetchone()
        if row:
            return self._row_to_scene(row)
        return None
    
    def update_scene(self, scene: MemScene) -> bool:
        """更新记忆场景"""
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE mem_scenes 
            SET title=?, scene_type=?, description=?, cell_ids=?, updated_at=?,
                activity_score=?, last_accessed=?, metadata=?
            WHERE id=?
        ''', (
            scene.title, scene.scene_type, scene.description,
            json.dumps(scene.cell_ids), scene.updated_at,
            scene.activity_score, scene.last_accessed,
            json.dumps(scene.metadata), scene.id
        ))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def delete_scene(self, scene_id: str) -> bool:
        """删除记忆场景"""
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM mem_scenes WHERE id = ?', (scene_id,))
        self.conn.commit()
        return cursor.rowcount > 0
    
    def list_scenes(self,
                    scene_type: Optional[str] = None,
                    min_activity: Optional[float] = None,
                    limit: int = 100,
                    offset: int = 0) -> List[MemScene]:
        """查询记忆场景列表"""
        cursor = self.conn.cursor()
        
        query = 'SELECT * FROM mem_scenes WHERE 1=1'
        params = []
        
        if scene_type:
            query += ' AND scene_type = ?'
            params.append(scene_type)
        
        if min_activity is not None:
            query += ' AND activity_score >= ?'
            params.append(min_activity)
        
        query += ' ORDER BY activity_score DESC, updated_at DESC LIMIT ? OFFSET ?'
        params.extend([limit, offset])
        
        cursor.execute(query, params)
        return [self._row_to_scene(row) for row in cursor.fetchall()]
    
    def _row_to_scene(self, row: sqlite3.Row) -> MemScene:
        """将数据库行转换为 MemScene 对象"""
        return MemScene(
            id=row['id'],
            title=row['title'],
            scene_type=row['scene_type'],
            description=row['description'],
            cell_ids=json.loads(row['cell_ids']) if row['cell_ids'] else [],
            created_at=row['created_at'],
            updated_at=row['updated_at'],
            activity_score=row['activity_score'],
            last_accessed=row['last_accessed'],
            metadata=json.loads(row['metadata']) if row['metadata'] else {}
        )
    
    # -------------------- 统计与工具 --------------------
    
    def get_stats(self) -> Dict:
        """获取存储统计信息"""
        cursor = self.conn.cursor()
        
        cursor.execute('SELECT COUNT(*) FROM mem_cells')
        cell_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM mem_scenes')
        scene_count = cursor.fetchone()[0]
        
        cursor.execute('SELECT cell_type, COUNT(*) FROM mem_cells GROUP BY cell_type')
        cells_by_type = {row[0]: row[1] for row in cursor.fetchall()}
        
        return {
            'total_cells': cell_count,
            'total_scenes': scene_count,
            'cells_by_type': cells_by_type,
            'db_path': str(self.db_path)
        }
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()
            self.conn = None


# ============================================================================
# 使用示例
# ============================================================================

if __name__ == "__main__":
    # 测试存储层
    storage = SQLiteStorage("test_hongnao.db")
    
    # 创建测试记忆场景
    scene = MemScene(
        id="scene_001",
        title="弘脑记忆系统项目",
        scene_type="project",
        description="燧弘华创 AI 平台长期记忆系统开发项目",
        cell_ids=[],
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        activity_score=80.0
    )
    storage.create_scene(scene)
    
    # 创建测试记忆颗粒
    cell = MemCell(
        id="cell_001",
        cell_type="fact",
        content="燧弘华创采用 1+N+X 架构",
        tags=["燧弘", "架构", "项目背景"],
        importance=8.5,
        created_at=datetime.now().isoformat(),
        updated_at=datetime.now().isoformat(),
        scene_id="scene_001"
    )
    storage.create_cell(cell)
    
    # 查询统计
    stats = storage.get_stats()
    print(f"存储统计：{json.dumps(stats, ensure_ascii=False, indent=2)}")
    
    # 查询记忆
    cells = storage.list_cells(limit=10)
    print(f"\n记忆颗粒列表：{len(cells)} 条")
    for cell in cells:
        print(f"  - [{cell.cell_type}] {cell.content[:50]}...")
    
    storage.close()
    print("\n✅ 存储层测试完成")
