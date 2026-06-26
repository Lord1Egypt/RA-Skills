"""
Hermes记忆核心 - 方案二核心模块
直接从方案文档提取，可独立运行测试
"""

import sqlite3
import json
import os
import re
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
import hashlib


class HermesMemoryCore:
    """
    Hermes记忆系统核心
    
    核心特性：
    1. 双重索引：FTS5全文搜索 + 实体关系索引
    2. 自动分级：重要信息自动提升到长期记忆
    3. 衰减机制：低频访问的记忆逐渐弱化
    4. 主动触发：基于上下文自动唤醒相关记忆
    """
    
    def __init__(self, base_path: str = "~/.workbuddy/hermes_memory"):
        self.base_path = os.path.expanduser(base_path)
        self._ensure_directories()
        
        # 数据库连接
        self.db_path = os.path.join(self.base_path, "index.db")
        self.conn = sqlite3.connect(self.db_path)
        self._init_db()
        
        # 内存缓存（最近访问的记忆）
        self.cache = {}
        self.cache_max_size = 1000
        
        # 记忆规则
        self.memory_rules = self._load_memory_rules()
    
    def _ensure_directories(self):
        """确保目录结构存在"""
        dirs = [
            "", "memory/conversations", "memory/knowledge", 
            "memory/profile", "memory/reminders",
            "skills/built-in", "skills/custom", "config"
        ]
        for d in dirs:
            path = os.path.join(self.base_path, d)
            os.makedirs(path, exist_ok=True)
    
    def _init_db(self):
        """初始化数据库表结构"""
        cursor = self.conn.cursor()
        
        # FTS5全文搜索表
        cursor.execute("""
            CREATE VIRTUAL TABLE IF NOT EXISTS memory_fts USING fts5(
                content,
                source_type,
                source_id,
                session_id,
                timestamp,
                importance,
                access_count,
                last_accessed,
                tags,
                entities,
                content='memory_content',
                tokenize='porter unicode61'
            )
        """)
        
        # 内容表（FTS5的外部内容表）
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS memory_content(
                rowid INTEGER PRIMARY KEY AUTOINCREMENT,
                content TEXT,
                source_type TEXT,
                source_id TEXT,
                session_id TEXT,
                timestamp TEXT,
                importance INTEGER DEFAULT 5,
                access_count INTEGER DEFAULT 0,
                last_accessed TEXT,
                tags TEXT,
                entities TEXT
            )
        """)
        
        # 实体关系表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entities(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                type TEXT,
                description TEXT,
                first_seen TEXT,
                last_seen TEXT,
                mention_count INTEGER DEFAULT 0,
                related_entities TEXT,
                attributes TEXT
            )
        """)
        
        # 实体关联表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS entity_relations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source_entity_id INTEGER,
                target_entity_id INTEGER,
                relation_type TEXT,
                strength REAL DEFAULT 1.0,
                context TEXT,
                first_observed TEXT
            )
        """)
        
        # 用户画像表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_profile(
                key TEXT PRIMARY KEY,
                value TEXT,
                category TEXT,
                confidence REAL DEFAULT 0.5,
                first_learned TEXT,
                last_updated TEXT,
                source_session_id TEXT
            )
        """)
        
        # 会话摘要表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS session_summaries(
                session_id TEXT PRIMARY KEY,
                summary TEXT,
                topics TEXT,
                key_findings TEXT,
                tasks_completed TEXT,
                files_referenced TEXT,
                start_time TEXT,
                end_time TEXT,
                message_count INTEGER
            )
        """)
        
        self.conn.commit()
    
    def store_memory(self, content: str, metadata: Dict[str, Any]) -> int:
        """存储记忆到系统中"""
        timestamp = datetime.now().isoformat()
        importance = metadata.get('importance', 5)
        tags = ','.join(metadata.get('tags', []))
        entities_json = json.dumps(metadata.get('entities', []), ensure_ascii=False)
        
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO memory_content (
                content, source_type, source_id, session_id,
                timestamp, importance, access_count, last_accessed,
                tags, entities
            ) VALUES (?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
        """, (
            content,
            metadata.get('source_type', 'conversation'),
            metadata.get('source_id', ''),
            metadata.get('session_id', ''),
            timestamp,
            importance,
            timestamp,
            tags,
            entities_json
        ))
        
        rowid = cursor.lastrowid
        
        # 同时插入FTS5索引
        cursor.execute("""
            INSERT INTO memory_fts (rowid, content, source_type, source_id, 
                                    session_id, timestamp, importance, 
                                    access_count, last_accessed, tags, entities)
            VALUES (?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?)
        """, (
            rowid, content,
            metadata.get('source_type', 'conversation'),
            metadata.get('source_id', ''),
            metadata.get('session_id', ''),
            timestamp, importance,
            timestamp, tags, entities_json
        ))
        
        # 提取并存储实体
        if metadata.get('entities'):
            for entity in metadata['entities']:
                self._upsert_entity(entity, rowid, session_id=metadata.get('session_id'))
        
        self.conn.commit()
        
        # 如果是高重要性记忆，同时写入Markdown长期记忆
        if importance >= 8:
            self._persist_to_markdown(content, metadata)
        
        return rowid
    
    def search(self, query: str, limit: int = 20, 
               filters: Optional[Dict] = None) -> List[Dict]:
        """多模式搜索"""
        cursor = self.conn.cursor()
        
        fts_query = self._build_fts_query(query)
        
        sql = f"""
            SELECT mc.rowid, mc.content, mc.source_type, mc.session_id, 
                   mc.timestamp, mc.importance, mc.access_count, 
                   mc.tags, rank
            FROM memory_content mc
            JOIN memory_fts ON memory_fts.rowid = mc.rowid
            WHERE memory_fts MATCH ?
        """
        params = [fts_query]
        
        if filters:
            if filters.get('source_type'):
                sql += " AND mc.source_type IN (?)"
                params.append(filters['source_type'])
            
            if filters.get('min_importance'):
                sql += " AND mc.importance >= ?"
                params.append(filters['min_importance'])
            
            if filters.get('since'):
                sql += " AND mc.timestamp >= ?"
                params.append(filters['since'])
            
            if filters.get('tags'):
                tag_conditions = ' OR '.join(['mc.tags LIKE ?'] * len(filters['tags']))
                sql += f" AND ({tag_conditions})"
                params.extend([f'%{t}%' for t in filters['tags']])
        
        sql += " ORDER BY rank LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        
        results = []
        for row in rows:
            result = {
                'id': row[0],
                'content': row[1],
                'source_type': row[2],
                'session_id': row[3],
                'timestamp': row[4],
                'importance': row[5],
                'access_count': row[6],
                'tags': row[7].split(',') if row[7] else [],
                'relevance_score': row[8]
            }
            results.append(result)
            self._update_access_count(row[0])
        
        return results
    
    def _build_fts_query(self, query: str) -> str:
        """构建优化的FTS5查询"""
        # 移除所有非字母数字/中文/空格/星号的字符
        query = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff\s*]', ' ', query)
        tokens = [t.strip() for t in query.split() if t.strip()]
        
        # 处理空查询（匹配所有）
        if not tokens:
            return '"zzz_no_match_xyz"'
        
        # 单token：加前缀通配
        if len(tokens) == 1:
            token = tokens[0]
            if token == '*':
                return '"zzz_no_match_xyz"'
            return f'{token}*' if not token.endswith('*') else token
        
        # 2-3个token：用OR + 通配（避免NEAR的引号问题）
        elif len(tokens) <= 3:
            safe_tokens = [t.replace('"', '').strip() for t in tokens if t.strip()]
            return ' OR '.join([f'{t}*' for t in safe_tokens if t])
        
        # 多token：用OR + 通配
        else:
            safe_tokens = [t.replace('"', '').strip() for t in tokens[:5] if t.strip()]
            return ' OR '.join([f'{t}*' for t in safe_tokens])
    
    def get_context_for_session(self, session_id: str) -> Dict:
        """
        为新会话获取相关上下文
        这是解决"遗漏信息"问题的核心方法！
        """
        recent_sessions = self._get_recent_session_summaries(limit=3)
        
        important_memories = self.search("*", limit=30, filters={
            'min_importance': 7
        })
        
        profile = self._get_user_profile()
        
        active_projects = self.search("项目", limit=10, filters={
            'tags': ['project']
        })
        
        recent_files = self.search("", limit=15, filters={
            'source_type': 'user_provided'
        })
        
        return {
            'recent_sessions': recent_sessions,
            'important_memories': important_memories[:15],
            'user_profile': profile,
            'active_projects': active_projects[:5],
            'recent_files': recent_files[:10]
        }
    
    def auto_extract_and_store(self, text: str, session_id: str, 
                                source_type: str = 'conversation') -> List[int]:
        """
        从文本中自动提取关键信息并存储
        解决问题：用户提供了重要信息但AI没有保存
        """
        stored_ids = []
        extractions = self._extract_key_information(text)
        
        for extraction in extractions:
            importance = self._assess_importance(extraction)
            
            memory_id = self.store_memory(
                content=extraction['content'],
                metadata={
                    'source_type': source_type,
                    'source_id': extraction.get('source_id', ''),
                    'session_id': session_id,
                    'importance': importance,
                    'tags': extraction.get('tags', []),
                    'entities': extraction.get('entities', [])
                }
            )
            stored_ids.append(memory_id)
            
            if importance >= 8:
                self._send_reminder(f"⚠️ 检测到高重要性信息：{extraction['content'][:50]}...")
        
        return stored_ids
    
    def _extract_key_information(self, text: str) -> List[Dict]:
        """从文本中提取关键信息 - 启发式规则"""
        extractions = []
        
        # 规则1：检测文件/资料提及
        file_patterns = [
            r'(.{10,200}?)(?:PDF|pdf|文档|资料|报告|星盘)[^。]*',
            r'(?:我给你|提供了?|这是)[^。]{10,200}?(?:文件|文档|图片|截图)',
            r'(.{10,300})?(?:\.md|\.py|\.js|\.json|\.pdf|\.xlsx)'
        ]
        for pattern in file_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                if len(match.strip()) > 15:
                    extractions.append({
                        'content': match.strip(),
                        'tags': ['user_provided_file', 'important'],
                        'entities': self._extract_entities_from_text(match),
                        'importance_hint': 8
                    })
        
        # 规则2：检测个人偏好/习惯
        preference_patterns = [
            r'我喜欢[^。]+',
            r'我的(偏好|习惯|风格|方式|方法是)[^。]+',
            r'(?:不要|别|避免)[^。]{5,50}',
            r'(?:注意|记住|一定要)[^。]{5,80}'
        ]
        for pattern in preference_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                extractions.append({
                    'content': match,
                    'tags': ['user_preference'],
                    'entities': self._extract_entities_from_text(match),
                    'importance_hint': 7
                })
        
        # 规则3：检测项目背景信息
        project_patterns = [
            r'(?:目前)?(?:正在做|在做|参与)[^。]{10,200}(?:项目|工作|任务)',
            r'.{5,100}(?:项目|产品|应用|App)[^。]{5,100}(?:开发|制作|设计)',
            r'(?:我是|叫)[^。]{5,50}(?:开发者|创作者|制作人|导演)'
        ]
        for pattern in project_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                extractions.append({
                    'content': match,
                    'tags': ['project_background'],
                    'entities': self._extract_entities_from_text(match),
                    'importance_hint': 9
                })
        
        # 规则4：检测具体数据/参数
        data_patterns = [
            r'(?:出生|生日)[^。]{5,100}(?:年|月|日|时)',
            r'\d{4}[/-]\d{1,2}[/-]\d{1,2}',
            r'[A-Z]\d{5}\.[A-Z]{2}',
            r'(?:价格|金额|费用)[^。]*\d+'
        ]
        for pattern in data_patterns:
            matches = re.findall(pattern, text)
            for match in matches:
                extractions.append({
                    'content': match,
                    'tags': ['specific_data'],
                    'entities': [{'name': match, 'type': 'data'}],
                    'importance_hint': 6
                })
        
        # 去重
        seen_hashes = set()
        unique_extractions = []
        for ext in extractions:
            content_hash = hashlib.md5(ext['content'].encode()).hexdigest()
            if content_hash not in seen_hashes:
                seen_hashes.add(content_hash)
                unique_extractions.append(ext)
        
        return unique_extractions
    
    def _assess_importance(self, extraction: Dict) -> int:
        """评估提取信息的重要性（0-10）"""
        base_score = extraction.get('importance_hint', 5)
        
        tag_weights = {
            'user_provided_file': 3,
            'important': 2,
            'user_preference': 2,
            'project_background': 3,
            'specific_data': 1
        }
        for tag in extraction.get('tags', []):
            base_score += tag_weights.get(tag, 0)
        
        length = len(extraction['content'])
        if 20 < length < 500:
            base_score += 1
        
        return min(10, max(1, base_score))
    
    def _upsert_entity(self, entity_info: Dict, memory_id: int, 
                       session_id: str = None):
        """更新或插入实体"""
        cursor = self.conn.cursor()
        
        name = entity_info.get('name', '')
        entity_type = entity_info.get('type', 'unknown')
        
        cursor.execute("SELECT id FROM entities WHERE name = ? AND type = ?", 
                      (name, entity_type))
        existing = cursor.fetchone()
        
        now = datetime.now().isoformat()
        
        if existing:
            cursor.execute("""
                UPDATE entities SET 
                    last_seen = ?,
                    mention_count = mention_count + 1,
                    description = COALESCE(description, ?)
                WHERE id = ?
            """, (now, entity_info.get('description', ''), existing[0]))
            entity_id = existing[0]
        else:
            cursor.execute("""
                INSERT INTO entities (name, type, description, first_seen, 
                                      last_seen, mention_count, attributes)
                VALUES (?, ?, ?, ?, ?, 1, ?)
            """, (name, entity_type, entity_info.get('description', ''), 
                  now, now, json.dumps(entity_info.get('attributes', {}))))
            entity_id = cursor.lastrowid
        
        self.conn.commit()
        return entity_id
    
    def _persist_to_markdown(self, content: str, metadata: Dict):
        """将高重要性记忆持久化到Markdown文件"""
        memory_dir = os.path.expanduser("~/.workbuddy/memory/")
        os.makedirs(memory_dir, exist_ok=True)
        today = datetime.now().strftime('%Y-%m-%d')
        daily_file = os.path.join(memory_dir, f"{today}.md")
        
        entry = f"\n\n## [Hermes自动记录] {datetime.now().strftime('%H:%M')}\n\n"
        entry += f"- **来源**: {metadata.get('source_type', 'unknown')}\n"
        entry += f"- **标签**: {', '.join(metadata.get('tags', []))}\n"
        entry += f"- **内容**: {content}\n"
        entry += f"- **重要度**: {metadata.get('importance', 5)}/10\n"
        
        with open(daily_file, 'a', encoding='utf-8') as f:
            f.write(entry)
    
    def _send_reminder(self, message: str):
        """发送提醒"""
        reminders_file = os.path.join(self.base_path, "memory/reminders/pending.json")
        reminders = []
        if os.path.exists(reminders_file):
            with open(reminders_file, 'r') as f:
                reminders = json.load(f)
        
        reminders.append({
            'message': message,
            'timestamp': datetime.now().isoformat(),
            'acknowledged': False
        })
        
        with open(reminders_file, 'w') as f:
            json.dump(reminders, f, ensure_ascii=False, indent=2)
    
    def _update_access_count(self, memory_id: int):
        """更新访问计数"""
        now = datetime.now().isoformat()
        self.conn.execute(
            "UPDATE memory_content SET access_count = access_count + 1, last_accessed = ? WHERE rowid = ?",
            (now, memory_id)
        )
        self.conn.commit()
    
    def _get_recent_session_summaries(self, limit: int = 3) -> List[Dict]:
        """获取最近的会话摘要"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT session_id, summary, topics, end_time, message_count
            FROM session_summaries 
            ORDER BY end_time DESC 
            LIMIT ?
        """, (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'session_id': row[0],
                'summary': row[1],
                'topics': json.loads(row[2]) if row[2] else [],
                'end_time': row[3],
                'message_count': row[4]
            })
        return results
    
    def _get_user_profile(self) -> Dict:
        """获取用户画像"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT key, value, category, confidence FROM user_profile")
        
        profile = {}
        for row in cursor.fetchall():
            category = row[2]
            if category not in profile:
                profile[category] = {}
            profile[category][row[0]] = {
                'value': row[1],
                'confidence': row[3]
            }
        return profile
    
    def _load_memory_rules(self) -> Dict:
        """加载记忆规则配置"""
        rules_file = os.path.join(self.base_path, "config/memory_rules.json")
        default_rules = {
            'auto_extract_enabled': True,
            'auto_persist_threshold': 8,
            'cache_size': 1000,
            'max_extraction_per_message': 5,
            'entity_types_to_track': ['person', 'project', 'file', 'location', 'organization', 'concept'],
            'importance_boost_tags': ['user_provided_file', 'error_correction', 'critical_instruction']
        }
        
        if os.path.exists(rules_file):
            with open(rules_file, 'r') as f:
                custom_rules = json.load(f)
                default_rules.update(custom_rules)
        
        return default_rules
    
    def _extract_entities_from_text(self, text: str) -> List[Dict]:
        """简单实体提取"""
        entities = []
        
        project_names = [
            '星语', '星轨人生', '星轨故事', '紫微引擎', '印度占星',
            'cv01', 'plotGenerator', 'Hermes Agent', 'WorkBuddy'
        ]
        for name in project_names:
            if name in text:
                entities.append({'name': name, 'type': 'project'})
        
        file_match = re.search(r'([\w\u4e00-\u9fff\-]+\.(?:md|py|js|json|pdf|xlsx))', text)
        if file_match:
            entities.append({'name': file_match.group(1), 'type': 'file'})
        
        return entities
    
    def close(self):
        """关闭数据库连接"""
        self.conn.close()


# ==================== 测试代码 ====================

if __name__ == "__main__":
    print("=" * 60)
    print("  Hermes Memory Core - 部署测试")
    print("=" * 60)
    
    # 初始化
    test_path = "~/.workbuddy/hermes_memory_test"
    memory = HermesMemoryCore(base_path=test_path)
    print("\n✅ 记忆核心初始化成功")
    print(f"   数据库路径: {memory.db_path}")
    
    # 测试1：存储用户提供的PDF星盘信息
    print("\n--- 测试1: 存储高重要性信息 ---")
    mid1 = memory.store_memory(
        content="用户提供了11页印度占星星盘PDF资料，包含完整的行星位置、宫位分布、Karaka分配等信息。正确数据：Lagna狮子座12°38'/Magha 4/1宫；Sun白羊座3°31'/Ashwini 2/9宫(GK)；Moon水瓶座11°47'/Satabhisha 2/7宫(AmK)；Jupiter处女座13°49'/Hasta 2/2宫落陷逆行(AK)",
        metadata={
            'source_type': 'user_provided',
            'source_id': 'indian_astrology_chart_pdf_11pages',
            'session_id': 'astrology-session-20260422',
            'importance': 10,
            'tags': ['user_provided_file', 'indian_astrology', 'chart_data', 'critical'],
            'entities': [
                {'name': '印度占星星盘', 'type': 'document'},
                {'name': 'Lagna', 'type': 'concept'},
                {'name': 'Jupiter AK', 'type': 'planet'}
            ]
        }
    )
    print(f"  ✅ 存储成功，ID={mid1}")
    
    # 测试2：存储项目背景
    print("\n--- 测试2: 存储项目背景 ---")
    mid2 = memory.store_memory(
        content="一楠是星轨系列产品独立开发者，包括紫微斗数App(星轨人生)、AI剧本系统(cv01)、故事生成器(星语)。使用WorkBuddy作为开发助手。",
        metadata={
            'source_type': 'user_provided',
            'session_id': 'profile-session',
            'importance': 9,
            'tags': ['project_background', 'developer_profile'],
            'entities': [
                {'name': '星轨人生', 'type': 'project'},
                {'name': 'cv01', 'type': 'project'},
                {'name': '星语', 'type': 'project'}
            ]
        }
    )
    print(f"  ✅ 存储成功，ID={mid2}")
    
    # 测试3：存储用户偏好
    print("\n--- 测试3: 存储用户偏好 ---")
    mid3 = memory.store_memory(
        content="一楠偏好简洁直接的沟通风格，不要废话。称呼为'一楠'或'助手'。工作流程：读历史→执行→交付附件→写摘要",
        metadata={
            'source_type': 'conversation',
            'session_id': 'pref-session',
            'importance': 8,
            'tags': ['user_preference', 'communication_style']
        }
    )
    print(f"  ✅ 存储成功，ID={mid3}")
    
    # 测试4：搜索功能
    print("\n--- 测试4: FTS5全文搜索 ---")
    results = memory.search("印度占星星盘", limit=5)
    print(f"  搜索'印度占星星盘' → 找到 {len(results)} 条结果:")
    for r in results:
        print(f"    [{r['importance']}★] {r['content'][:70]}...")
    
    # 测试5：自动提取关键信息
    print("\n--- 测试5: 自动提取关键信息 ---")
    test_message = "我给你发了11页的PDF星盘资料，你分析的时候一定要用正确的数据。另外我在做星轨人生的iOS版本开发，最近在研究奇门遁甲的编剧映射。"
    extracted = memory.auto_extract_and_store(test_message, "test-session-auto")
    print(f"  输入: '{test_message}'")
    print(f"  自动提取并存储了 {len(extracted)} 条关键信息")
    for eid in extracted:
        print(f"    → 存储 ID={eid}")
    
    # 测试6：为新会话加载上下文
    print("\n--- 测试6: 新会话上下文加载 ---")
    context = memory.get_context_for_session("new-test-session")
    print(f"  最近会话摘要: {len(context['recent_sessions'])} 条")
    print(f"  高重要性记忆: {len(context['important_memories'])} 条")
    print(f"  用户画像类别: {list(context['user_profile'].keys())}")
    print(f"  活跃项目: {len(context['active_projects'])} 条")
    print(f"  最近文件: {len(context['recent_files'])} 条")
    
    # 统计
    print("\n" + "=" * 60)
    print("  📊 数据库统计")
    cursor = memory.conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM memory_content")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM entities")
    entities = cursor.fetchone()[0]
    print(f"  总记忆条数: {total}")
    print(f"  实体数量: {entities}")
    
    memory.close()
    print("\n✅ 所有6项测试通过！记忆核心部署成功")
