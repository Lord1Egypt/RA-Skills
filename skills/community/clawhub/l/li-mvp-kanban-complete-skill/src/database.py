"""
看板系统数据库模块
支持 SQLite + sqlite-vec 向量搜索
"""
import sqlite3
import json
import os
from datetime import datetime
from typing import Optional, List, Dict, Any
import hashlib

# 尝试导入 sqlite-vec
try:
    import sqlite_vec
    HAS_VEC = True
except ImportError:
    HAS_VEC = False
    print("警告：sqlite-vec 未安装，向量搜索功能将不可用")
    print("安装：pip install sqlite-vec")

DB_PATH = os.path.join(os.path.dirname(__file__), 'kanban.db')


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(DB_PATH, timeout=30.0, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    
    # 启用 WAL 模式以支持更好的并发
    conn.execute('PRAGMA journal_mode=WAL')
    conn.execute('PRAGMA synchronous=NORMAL')
    
    # 加载向量扩展
    if HAS_VEC:
        sqlite_vec.load(conn)
    
    return conn


def init_db():
    """初始化数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 项目表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            status TEXT DEFAULT 'todo',
            lane TEXT DEFAULT 'feature',
            progress INTEGER DEFAULT 0,
            tasks INTEGER DEFAULT 0,
            completed INTEGER DEFAULT 0,
            assignee TEXT DEFAULT '',
            priority TEXT DEFAULT 'medium',
            description TEXT DEFAULT '',
            tags TEXT DEFAULT '[]',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            name_embedding BLOB,
            description_embedding BLOB
        )
    ''')
    
    # 泳道表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS lanes (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            color TEXT DEFAULT '#667eea',
            icon TEXT DEFAULT '📌',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 变更日志表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS change_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            project_id INTEGER,
            action TEXT NOT NULL,
            old_data TEXT,
            new_data TEXT,
            changed_by TEXT DEFAULT 'system',
            changed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建索引
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_status ON projects(status)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_lane ON projects(lane)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_projects_assignee ON projects(assignee)')
    
    # 插入默认泳道
    default_lanes = [
        ('feature', '功能开发', '#667eea', '🚀'),
        ('security', '安全加固', '#e53e3e', '🔒'),
        ('devops', 'DevOps', '#38a169', '⚙️'),
        ('bugfix', 'Bug 修复', '#dd6b20', '🐛')
    ]
    
    for lane_id, name, color, icon in default_lanes:
        cursor.execute('''
            INSERT OR IGNORE INTO lanes (id, name, color, icon)
            VALUES (?, ?, ?, ?)
        ''', (lane_id, name, color, icon))
    
    conn.commit()
    conn.close()
    print(f"数据库初始化完成：{DB_PATH}")


def generate_embedding(text: str, dimensions: int = 128) -> Optional[bytes]:
    """
    生成文本的固定维度嵌入（生产环境应使用真实 embedding 模型）
    
    Args:
        text: 输入文本
        dimensions: 向量维度（默认 128）
    
    Returns:
        固定长度的二进制向量（struct 打包）
    """
    if not HAS_VEC or not text:
        return None
    
    import struct
    
    # 使用 MD5 哈希（16 bytes）
    hash_bytes = hashlib.md5(text.encode('utf-8')).digest()
    
    # 将 16 bytes 扩展为 128 floats
    embedding = []
    for i in range(dimensions):
        # 循环使用 16 个 bytes
        byte_val = hash_bytes[i % 16]
        # 添加位置扰动确保维度间有差异
        embedding.append(float(byte_val) / 255.0 + (i % 16) * 0.001)
    
    # 使用 struct 打包为二进制（固定长度：128 * 4 = 512 bytes）
    return struct.pack(f'{dimensions}f', *embedding)


# ============ 项目操作 ============

def get_all_projects() -> List[Dict]:
    """获取所有项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects ORDER BY created_at DESC')
    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    # 清理无法序列化的字段
    for p in projects:
        p.pop('name_embedding', None)
        p.pop('description_embedding', None)
    return projects


def get_project(project_id: int) -> Optional[Dict]:
    """获取单个项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM projects WHERE id = ?', (project_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        project = dict(row)
        project.pop('name_embedding', None)
        project.pop('description_embedding', None)
        return project
    return None


def create_project(data: Dict) -> Dict:
    """创建项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    name = data.get('name', 'New Project')
    embedding = generate_embedding(name) if HAS_VEC else None
    desc_embedding = generate_embedding(data.get('description', '')) if HAS_VEC else None
    
    cursor.execute('''
        INSERT INTO projects (name, status, lane, progress, tasks, completed, 
                            assignee, priority, description, tags, name_embedding, description_embedding)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        name,
        data.get('status', 'todo'),
        data.get('lane', 'feature'),
        data.get('progress', 0),
        data.get('tasks', 0),
        data.get('completed', 0),
        data.get('assignee', ''),
        data.get('priority', 'medium'),
        data.get('description', ''),
        json.dumps(data.get('tags', [])),
        embedding,
        desc_embedding
    ))
    
    project_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    # 变更日志暂时禁用（避免 SQLite 锁竞争）
    # log_change(project_id, 'create', None, data)
    
    return get_project(project_id)


def update_project(project_id: int, data: Dict) -> Optional[Dict]:
    """更新项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取旧数据
    old_project = get_project(project_id)
    if not old_project:
        conn.close()
        return None
    
    # 构建更新字段
    updates = []
    values = []
    
    for key in ['name', 'status', 'lane', 'progress', 'tasks', 'completed', 
                'assignee', 'priority', 'description', 'tags']:
        if key in data:
            updates.append(f'{key} = ?')
            values.append(data[key])
    
    # 更新 embedding
    if 'name' in data:
        updates.append('name_embedding = ?')
        values.append(generate_embedding(data['name']))
    
    updates.append('updated_at = CURRENT_TIMESTAMP')
    values.append(project_id)
    
    query = f"UPDATE projects SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    
    conn.commit()
    conn.close()
    
    # 变更日志暂时禁用
    # log_change(project_id, 'update', old_project, data)
    
    return get_project(project_id)


def delete_project(project_id: int) -> Optional[Dict]:
    """删除项目"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    project = get_project(project_id)
    if not project:
        conn.close()
        return None
    
    cursor.execute('DELETE FROM projects WHERE id = ?', (project_id,))
    conn.commit()
    conn.close()
    
    # 变更日志暂时禁用
    # log_change(project_id, 'delete', project, None)
    
    return project


def search_projects_similar(query: str, limit: int = 5) -> List[Dict]:
    """向量搜索相似项目"""
    if not HAS_VEC:
        return []
    
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query_embedding = generate_embedding(query)
    
    # 使用 sqlite-vec 进行向量相似度搜索
    cursor.execute('''
        SELECT *, 
               vec_distance_cosine(name_embedding, ?) as similarity
        FROM projects
        WHERE name_embedding IS NOT NULL
        ORDER BY similarity ASC
        LIMIT ?
    ''', (query_embedding, limit))
    
    projects = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return projects


# ============ 泳道操作 ============

def get_all_lanes() -> List[Dict]:
    """获取所有泳道"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lanes ORDER BY id')
    lanes = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return lanes


def create_lane(data: Dict) -> Dict:
    """创建泳道"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    lane_id = data.get('id', f'lane_{datetime.now().strftime("%Y%m%d%H%M%S")}')
    
    cursor.execute('''
        INSERT OR REPLACE INTO lanes (id, name, color, icon)
        VALUES (?, ?, ?, ?)
    ''', (lane_id, data.get('name', 'New Lane'), 
          data.get('color', '#667eea'), data.get('icon', '📌')))
    
    conn.commit()
    lane = get_lane(lane_id)
    conn.close()
    return lane


def get_lane(lane_id: str) -> Optional[Dict]:
    """获取单个泳道"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM lanes WHERE id = ?', (lane_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def get_lane_by_id(lane_id: str) -> Optional[Dict]:
    """获取单个泳道（别名）"""
    return get_lane(lane_id)


def update_lane_by_id(lane_id: str, data: Dict) -> Optional[Dict]:
    """更新泳道信息"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查泳道是否存在
    cursor.execute('SELECT * FROM lanes WHERE id = ?', (lane_id,))
    if not cursor.fetchone():
        conn.close()
        return None
    
    # 构建更新字段
    updates = []
    values = []
    
    for key in ['name', 'color', 'icon']:
        if key in data:
            updates.append(f'{key} = ?')
            values.append(data[key])
    
    if not updates:
        conn.close()
        return get_lane(lane_id)
    
    values.append(lane_id)
    query = f"UPDATE lanes SET {', '.join(updates)} WHERE id = ?"
    cursor.execute(query, values)
    conn.commit()
    
    lane = get_lane(lane_id)
    conn.close()
    return lane


def delete_lane_by_id(lane_id: str) -> bool:
    """删除泳道"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 检查泳道是否存在
    cursor.execute('SELECT * FROM lanes WHERE id = ?', (lane_id,))
    if not cursor.fetchone():
        conn.close()
        return False
    
    # 检查是否有项目使用该泳道
    cursor.execute('SELECT COUNT(*) FROM projects WHERE lane = ?', (lane_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        raise ValueError(f'泳道 {lane_id} 中仍有项目，无法删除')
    
    cursor.execute('DELETE FROM lanes WHERE id = ?', (lane_id,))
    conn.commit()
    conn.close()
    return True


# ============ 变更日志 ============

def log_change(project_id: int, action: str, old_data: Optional[Dict], 
               new_data: Optional[Dict], changed_by: str = 'system'):
    """记录变更日志（简化版，避免锁竞争）"""
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            INSERT INTO change_log (project_id, action, old_data, new_data, changed_by)
            VALUES (?, ?, ?, ?, ?)
        ''', (project_id, action, 
              json.dumps(old_data) if old_data else None,
              json.dumps(new_data) if new_data else None,
              changed_by))
        
        conn.commit()
        conn.close()
    except Exception as e:
        # 日志记录失败不影响主流程
        print(f"日志记录失败：{e}")


def get_change_log(project_id: Optional[int] = None, limit: int = 50) -> List[Dict]:
    """获取变更日志"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    if project_id:
        cursor.execute('''
            SELECT * FROM change_log 
            WHERE project_id = ? 
            ORDER BY changed_at DESC 
            LIMIT ?
        ''', (project_id, limit))
    else:
        cursor.execute('''
            SELECT * FROM change_log 
            ORDER BY changed_at DESC 
            LIMIT ?
        ''', (limit,))
    
    logs = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return logs


# ============ 统计指标 ============

def get_metrics() -> Dict:
    """获取统计指标"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 基础指标
    cursor.execute('SELECT COUNT(*) as total FROM projects')
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'done'")
    completed = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'in_progress'")
    in_progress = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM projects WHERE status = 'todo'")
    todo = cursor.fetchone()[0]
    
    # 任务指标
    cursor.execute('SELECT SUM(tasks) FROM projects')
    result = cursor.fetchone()[0]
    total_tasks = result or 0
    
    cursor.execute('SELECT SUM(completed) FROM projects')
    result = cursor.fetchone()[0]
    completed_tasks = result or 0
    
    success_rate = round(completed_tasks / max(total_tasks, 1) * 100)
    
    conn.close()
    
    return {
        'total_projects': total,
        'completed': completed,
        'in_progress': in_progress,
        'todo': todo,
        'total_tasks': total_tasks,
        'completed_tasks': completed_tasks,
        'success_rate': success_rate
    }


# 初始化
if __name__ == '__main__':
    init_db()
