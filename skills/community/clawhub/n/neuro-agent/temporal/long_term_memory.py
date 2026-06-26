"""
temporal/long_term_memory.py
=============================

Neuro-Agent 长期记忆库
负责：情绪胶囊的 SQLite 持久化存储、查询、更新、遗忘

依赖：
    - emotion_types.md（参考）
    - references/relationship_stages.md（参考）

数据目录：
    ~/.openclaw/workspace/neuro_claw/capsules/long_term/
"""

import sqlite3
import json
import os
import math
import re
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Any
from dataclasses import dataclass, asdict
from pathlib import Path

# ============ 路径配置 ============
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw" / "capsules" / "long_term"
DATA_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DATA_DIR / "memory.db"

# ============ 遗忘曲线常量 ============
DECAY_K = 1.0  # 巩固系数初始值，每次被提及+0.5
DORMANT_THRESHOLD = 0.3  # R < 0.3 进入休眠
DELETE_THRESHOLD = 0.1  # R < 0.1 可被删除


# ============ 数据结构 ============
@dataclass
class EmotionCapsule:
    """
    情绪胶囊数据结构
    
    属性说明：
        - id: 唯一标识，格式 capsule_{timestamp}_{random}
        - timestamp: 创建时间 ISO 格式
        - type: 类型 preference/emotion/fact/secret
        - content: 内容摘要和原始触发
        - emotion: 情绪标签和强度
        - tags: 标签列表
        - decay_rate: 衰减率
        - access_count: 被访问次数
        - memory_strength: 记忆强度 0.0-1.0
        - is_dormant: 是否休眠
        - sensitivity: 敏感度 normal/high/critical
        - last_accessed: 最后访问时间
        - temporal_index: 时间索引（从内容中提取的日期）
    """
    id: str
    timestamp: str
    type: str  # 见 CAPSULE_TYPES 常量
    content: Dict[str, str]  # {summary, original_trigger, detail}
    emotion: Dict[str, Any]  # {label, intensity}
    tags: List[str]
    decay_rate: Optional[float] = None  # None 表示使用类型默认值
    access_count: int = 0
    memory_strength: float = 1.0
    is_dormant: bool = False
    sensitivity: str = "normal"  # normal | high | critical
    last_accessed: str = ""
    temporal_index: str = ""  # 时间索引（格式: YYYY-MM-DD 或 YYYY-MM 或 YYYY）
    
    def to_dict(self) -> Dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: Dict) -> 'EmotionCapsule':
        return cls(**d)


# ============ 胶囊类型常量 ============
CAPSULE_TYPES = {
    # === 用户胶囊（User Capsules）===
    "fact": "客观事实",              # 客观发生的事件、事实
    "emotion": "情绪体验",            # 情绪感受记录
    "preference": "偏好",              # 喜欢/不喜欢的事物
    "secret": "秘密",                  # 隐私信息
    "dream": "梦想",                  # 未来愿望、憧憬
    "plan": "计划",                   # 目标、计划、待办
    "skill": "技能",                  # 能力、技术、特长
    "value": "价值观",                # 原则、信念、道德标准
    "fear": "恐惧",                   # 担忧、焦虑、害怕
    "milestone": "里程碑",            # 重要人生节点、成就
    "relationship": "关系",            # 人际关系、社交
    "habit": "习惯",                  # 行为习惯、日常
    
    # === AI 自我胶囊（AI Self Capsules）===
    "impulse": "冲动",                # 即时欲望、冲动
    "traits": "特质",                 # 性格特征
    "dream_log": "梦想日志",          # AI的想象、憧憬
    "self_context": "自我认知",        # 对自己的理解
    "reflection": "反思",             # 对行为的思考
    "growth": "成长",                 # 学习、进步
    "belief": "信念",                 # AI的信念体系
    "desire": "渴望",                 # 长期欲望、追求
    "pattern": "模式",                # 行为模式、倾向
    "memory_fragment": "记忆碎片",      # 不完整的记忆片段
    "ideal_self": "理想自我",          # 希望成为的样子
    "boundary": "边界",               # 限制、禁忌
}

# 类型分类映射
TYPE_CATEGORIES = {
    "user": ["fact", "emotion", "preference", "secret", "dream", "plan", 
             "skill", "value", "fear", "milestone", "relationship", "habit"],
    "ai": ["impulse", "traits", "dream_log", "self_context", "reflection", 
            "growth", "belief", "desire", "pattern", "memory_fragment", 
            "ideal_self", "boundary"]
}

# 类型对应的默认衰减率（重要类型衰减慢）
TYPE_DECAY_RATES = {
    "milestone": 0.01,   # 里程碑永久保存
    "value": 0.02,       # 价值观缓慢衰减
    "skill": 0.03,       # 技能缓慢衰减
    "traits": 0.05,      # 特质缓慢衰减
    "belief": 0.05,      # 信念缓慢衰减
    "dream": 0.08,       # 梦想缓慢衰减
    "habit": 0.1,        # 习惯中等速度衰减
    "relationship": 0.1,  # 关系中等速度衰减
    "fact": 0.1,         # 事实中等速度衰减
    "preference": 0.15,  # 偏好中快衰减
    "plan": 0.2,         # 计划较快衰减
    "emotion": 0.2,      # 情绪较快衰减
    "fear": 0.2,         # 恐惧较快衰减
    "secret": 0.3,       # 秘密较快衰减（但重要）
    "ideal_self": 0.1,    # 理想自我缓慢衰减
    # AI 自我类型
    "impulse": 0.3,      # 冲动快速衰减
    "reflection": 0.15,  # 反思中等衰减
    "growth": 0.1,       # 成长缓慢衰减
    "desire": 0.08,      # 渴望缓慢衰减
    "pattern": 0.1,      # 模式缓慢衰减
    "memory_fragment": 0.4,  # 记忆碎片快速衰减
    "self_context": 0.05,   # 自我认知缓慢衰减
    "dream_log": 0.1,       # 梦想日志缓慢衰减
    "boundary": 0.05,       # 边界缓慢衰减
}
@dataclass
class RelationshipEdge:
    """
    关系边数据结构
    用于概念图谱中的概念关联
    """
    id: str
    concept_a: str
    concept_b: str
    relation_type: str  # causes | triggers | contradicts | similar | belongs_to
    strength: float
    created_at: str


# ============ 遗忘曲线计算 ============
def calculate_retention(s: float, k: float, t_days: float) -> float:
    """
    计算记忆保留率
    
    公式: R = e^(-t / (S × K))
    
    参数:
        s: 初始情绪强度 (0.3-1.0)
        k: 巩固系数 (初始1.0，每次被提及+0.5)
        t_days: 距创建时间（天）
    
    返回:
        R: 记忆保留率 (0.0-1.0)
    """
    if s <= 0:
        return 0.0
    exponent = -t_days / (s * k)
    return math.exp(exponent)


def calculate_decay_rate(emotion_intensity: float, sensitivity: str) -> float:
    """
    根据情绪强度和敏感度计算衰减率
    
    参数:
        emotion_intensity: 情绪强度 0.0-1.0
        sensitivity: 敏感度 normal/high/critical
    
    返回:
        decay_rate: 衰减率
    """
    base = 1.0 - emotion_intensity
    
    # 敏感记忆衰减更慢（更难忘记）
    sensitivity_multiplier = {
        "normal": 1.0,
        "high": 0.7,     # 衰减更慢
        "critical": 0.5  # 衰减最慢
    }
    
    return base * sensitivity_multiplier.get(sensitivity, 1.0)


# ============ 核心类 ============
class LongTermMemory:
    """
    长期记忆库管理器
    
    功能：
        - SQLite 持久化存储情绪胶囊
        - 查询、筛选、更新访问记录
        - 遗忘曲线计算和休眠管理
        - 记忆晋升（短期 → 长期）
        - 概念关系管理
        - 向量语义检索（集成 VectorRetriever）
    """
    
    def __init__(self, db_path: str = None):
        """
        初始化长期记忆库
        
        参数:
            db_path: 数据库路径，默认 ~/.openclaw/.../long_term/memory.db
        """
        self.db_path = db_path or str(DB_PATH)
        self._init_database()
        self._vector_retriever = None  # 延迟初始化
    
    @property
    def vector_retriever(self):
        """
        延迟加载 VectorRetriever
        确保只有在真正需要向量检索时才初始化
        """
        if self._vector_retriever is None:
            try:
                from temporal.vector_retriever import VectorRetriever
                self._vector_retriever = VectorRetriever()
                print(f"[LongTermMemory] ✅ VectorRetriever 已集成")
            except Exception as e:
                print(f"[LongTermMemory] ⚠️ VectorRetriever 初始化失败: {e}")
                self._vector_retriever = None
        return self._vector_retriever
    
    def _init_database(self):
        """初始化数据库表结构"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 情绪胶囊表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS capsules (
                id TEXT PRIMARY KEY,
                timestamp TEXT NOT NULL,
                type TEXT NOT NULL,
                summary TEXT,
                original_trigger TEXT,
                detail TEXT,
                emotion_label TEXT,
                emotion_intensity REAL,
                tags TEXT,
                sensitivity TEXT DEFAULT 'normal',
                memory_strength REAL DEFAULT 1.0,
                access_count INTEGER DEFAULT 0,
                is_dormant INTEGER DEFAULT 0,
                last_accessed TEXT,
                created_at TEXT NOT NULL,
                temporal_index TEXT DEFAULT '',
                decay_rate REAL DEFAULT 0.5
            )
        """)
        
        # 迁移：为旧数据库添加 temporal_index 列
        try:
            cursor.execute("SELECT temporal_index FROM capsules LIMIT 1")
        except sqlite3.OperationalError:
            # 列不存在，添加它
            cursor.execute("ALTER TABLE capsules ADD COLUMN temporal_index TEXT DEFAULT ''")
            print(f"[LongTermMemory] 🔧 已添加 temporal_index 列到 capsules 表")
        
        # 迁移：为旧数据库添加 decay_rate 列
        try:
            cursor.execute("SELECT decay_rate FROM capsules LIMIT 1")
        except sqlite3.OperationalError:
            # 列不存在，添加它
            cursor.execute("ALTER TABLE capsules ADD COLUMN decay_rate REAL DEFAULT 0.5")
            print(f"[LongTermMemory] 🔧 已添加 decay_rate 列到 capsules 表")
        
        # 概念关系表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relationships (
                id TEXT PRIMARY KEY,
                concept_a TEXT NOT NULL,
                concept_b TEXT NOT NULL,
                relation_type TEXT NOT NULL,
                strength REAL DEFAULT 0.5,
                created_at TEXT NOT NULL
            )
        """)
        
        # 创建索引加速查询
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_capsules_type ON capsules(type)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_capsules_emotion ON capsules(emotion_label)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_capsules_dormant ON capsules(is_dormant)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_relationships_concepts ON relationships(concept_a, concept_b)")
        
        conn.commit()
        conn.close()
    
    # ============ 胶囊类型工具 ============
    
    @staticmethod
    def get_type_name(capsule_type: str) -> str:
        """获取类型的中文名称"""
        return CAPSULE_TYPES.get(capsule_type, "未知类型")
    
    @staticmethod
    def get_type_category(capsule_type: str) -> str:
        """获取类型所属类别（user/ai）"""
        for category, types in TYPE_CATEGORIES.items():
            if capsule_type in types:
                return category
        return "unknown"
    
    @staticmethod
    def get_default_decay_rate(capsule_type: str) -> float:
        """获取类型的默认衰减率"""
        return TYPE_DECAY_RATES.get(capsule_type, 0.5)
    
    @staticmethod
    def list_types(category: str = None) -> Dict[str, str]:
        """
        列出胶囊类型
        
        参数:
            category: 筛选类别（user/ai），None 则返回所有
        
        返回:
            Dict[str, str]: {type: description}
        """
        if category and category in TYPE_CATEGORIES:
            return {t: CAPSULE_TYPES[t] for t in TYPE_CATEGORIES[category]}
        return CAPSULE_TYPES.copy()
    
    @staticmethod
    def is_valid_type(capsule_type: str) -> bool:
        """检查是否是有效的胶囊类型"""
        return capsule_type in CAPSULE_TYPES
    
    # ============ 胶囊操作 ============
    
    def save_capsule(self, capsule: EmotionCapsule) -> bool:
        """
        保存情绪胶囊到数据库
        
        参数:
            capsule: EmotionCapsule 对象
        
        返回:
            bool: 是否保存成功
        """
        try:
            # 如果没有时间索引，从内容中提取
            if not capsule.temporal_index:
                text_to_search = capsule.content.get("summary", "") + " " + capsule.content.get("original_trigger", "")
                capsule.temporal_index = self._extract_temporal_index(text_to_search)
            
            # 如果没有指定衰减率，根据类型自动设置
            if capsule.decay_rate is None:
                capsule.decay_rate = self.get_default_decay_rate(capsule.type)
            
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                INSERT OR REPLACE INTO capsules (
                    id, timestamp, type, summary, original_trigger, detail,
                    emotion_label, emotion_intensity, tags, sensitivity,
                    memory_strength, access_count, is_dormant, last_accessed, created_at,
                    temporal_index, decay_rate
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                capsule.id,
                capsule.timestamp,
                capsule.type,
                capsule.content.get("summary", ""),
                capsule.content.get("original_trigger", ""),
                capsule.content.get("detail", ""),
                capsule.emotion.get("label", "neutral"),
                capsule.emotion.get("intensity", 0.5),
                json.dumps(capsule.tags, ensure_ascii=False),
                capsule.sensitivity,
                capsule.memory_strength,
                capsule.access_count,
                1 if capsule.is_dormant else 0,
                capsule.last_accessed,
                capsule.timestamp,
                capsule.temporal_index,
                capsule.decay_rate
            ))
            
            conn.commit()
            conn.close()
            
            # ========== 同步到 VectorRetriever ==========
            # 构建检索文本
            search_text = self._build_search_text(capsule)
            vr = self.vector_retriever
            if vr is not None and search_text.strip():
                try:
                    vr.add(
                        capsule_id=capsule.id,
                        content=search_text,
                        emotion_label=capsule.emotion.get("label"),
                        tags=capsule.tags,
                        metadata={
                            "type": capsule.type,
                            "sensitivity": capsule.sensitivity
                        }
                    )
                except Exception as e:
                    print(f"[LongTermMemory] ⚠️ VectorRetriever 同步失败: {e}")
            # ==========================================
            
            return True
            
        except Exception as e:
            print(f"[LongTermMemory] 保存胶囊失败: {e}")
            return False
    
    def _build_search_text(self, capsule: EmotionCapsule) -> str:
        """
        从胶囊构建用于向量检索的文本
        """
        parts = []
        if capsule.content.get("summary"):
            parts.append(capsule.content["summary"])
        if capsule.content.get("original_trigger"):
            parts.append(capsule.content["original_trigger"])
        if capsule.type:
            parts.append(f"类型: {capsule.type}")
        if capsule.tags:
            parts.append(f"标签: {', '.join(capsule.tags)}")
        return " | ".join(parts)
    
    def _extract_temporal_index(self, text: str) -> str:
        """
        从文本中提取日期信息，生成时间索引
        
        支持格式：
        - 2023/04/15, 2023-04-15, 2023.04.15
        - April 15, 2023 / Apr 15, 2023
        - 2023年4月15日
        - 3 weeks ago, yesterday, last Monday
        
        返回: 标准化日期字符串 (YYYY-MM-DD) 或空字符串
        """
        import re
        from datetime import datetime, timedelta
        
        # 标准日期格式
        patterns = [
            (r'(\d{4})[/.-](\d{1,2})[/.-](\d{1,2})', r'\1-\2-\3'),  # YYYY-MM-DD
            (r'(\d{4})年(\d{1,2})月(\d{1,2})日', r'\1-\2-\3'),  # 中文日期
        ]
        
        for pattern, replacement in patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    date_str = re.sub(pattern, replacement, match.group(0))
                    datetime.strptime(date_str, '%Y-%m-%d')
                    return date_str
                except:
                    pass
        
        # 英文月份日期
        month_map = {
            'january': '01', 'february': '02', 'march': '03', 'april': '04',
            'may': '05', 'june': '06', 'july': '07', 'august': '08',
            'september': '09', 'october': '10', 'november': '11', 'december': '12',
            'jan': '01', 'feb': '02', 'mar': '03', 'apr': '04', 'jun': '06',
            'jul': '07', 'aug': '08', 'sep': '09', 'oct': '10', 'nov': '11', 'dec': '12'
        }
        
        for month, num in month_map.items():
            pattern = rf'{month} (\d{{1,2}}),? (\d{{4}})'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                day, year = match.groups()
                return f"{year}-{num}-{int(day):02d}"
        
        # 只找到年月
        for month, num in month_map.items():
            pattern = rf'{month} (\d{{4}})'
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                return f"{match.group(1)}-{num}"
        
        # 只找到年
        match = re.search(r'(\d{4})', text)
        if match:
            return match.group(1)
        
        return ""
    
    def _in_date_range(self, temporal_index: str, date_range: tuple) -> bool:
        """
        检查时间索引是否在指定范围内
        
        参数:
            temporal_index: 时间索引字符串 (YYYY-MM-DD, YYYY-MM, 或 YYYY)
            date_range: (start_date, end_date) 元组
        
        返回:
            bool: 是否在范围内
        """
        if not temporal_index or not date_range:
            return True
        
        start, end = date_range
        
        # 标准化：补全位数便于比较
        # YYYY → YYYY-01-01
        # YYYY-MM → YYYY-MM-01
        # YYYY-MM-DD → YYYY-MM-DD
        
        def normalize(date_str):
            parts = date_str.split('-')
            if len(parts) == 1:  # YYYY
                return f"{parts[0]}-01-01"
            elif len(parts) == 2:  # YYYY-MM
                return f"{parts[0]}-{parts[1]}-01"
            return date_str  # YYYY-MM-DD
        
        if not start <= normalize(temporal_index) <= end:
            return False
        return True
    
    def _get_current_time(self) -> str:
        """
        获取当前时间（交叉验证：本地 + 联网比对）
        
        流程：
        1. 获取本地系统时间（date 命令）
        2. 联网获取 NTP 时间（worldtimeapi.org）
        3. 对比差异，超过容忍阈值则报警
        4. 返回联网时间（更可信）
        """
        import subprocess
        import urllib.request
        import json
        
        local_time = None
        net_time = None
        
        # Step 1: 获取本地时间
        try:
            result = subprocess.run(['date', '+%Y-%m-%d %H:%M:%S'], 
                                capture_output=True, text=True, timeout=2)
            if result.returncode == 0:
                local_time = result.stdout.strip()
        except:
            pass
        
        # Step 2: 联网获取时间
        time_sources = [
            ('https://worldtimeapi.org/api/timezone/Asia/Shanghai', 'datetime'),
            ('http://worldtimeapi.org/api/timezone/Asia/Shanghai', 'datetime'),
            ('https://api.binance.com/api/v3/time', 'serverTime'),
        ]
        
        for url, key in time_sources:
            try:
                req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
                with urllib.request.urlopen(req, timeout=3) as resp:
                    data = json.loads(resp.read().decode())
                    if key == 'serverTime':
                        net_time = datetime.fromtimestamp(int(data[key]) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                    else:
                        raw = data[key]
                        net_time = raw[:19] if 'T' in raw else raw
                break
            except:
                continue
        
        # Step 3: 对比验证
        if local_time and net_time:
            try:
                from dateutil import parser as dateutil_parser
                t_local = dateutil_parser.parse(local_time)
                t_net = dateutil_parser.parse(net_time)
                diff_seconds = abs((t_local - t_net).total_seconds())
                
                if diff_seconds > 300:  # 5分钟差异太大
                    print(f"[时间警告] 本地时间 {local_time} 与联网时间 {net_time} 差异 {diff_seconds:.0f}秒，请检查系统时间！")
                    # 差异大时使用联网时间，但打印警告
                    return net_time
                elif diff_seconds > 60:  # 1-5分钟差异
                    print(f"[时间提示] 本地与联网时间有 {diff_seconds:.0f}秒 差异")
                
                # 差异可接受，返回联网时间
                print(f"[时间同步] 联网确认: {net_time} (本地偏差: {diff_seconds:.0f}秒)")
                return net_time
            except Exception as e:
                print(f"[时间] 解析失败: {e}")
        
        # 降级：使用本地时间
        if local_time:
            print(f"[时间] 联网不可用，使用本地时间: {local_time}")
            return local_time
        
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def get_capsule(self, capsule_id: str) -> Optional[EmotionCapsule]:
        """
        根据 ID 获取胶囊
        
        参数:
            capsule_id: 胶囊 ID
        
        返回:
            EmotionCapsule 或 None
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM capsules WHERE id = ?", (capsule_id,))
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return self._row_to_capsule(row)
    
    def retrieve(
        self,
        query: str = None,
        capsule_type: str = None,
        emotion_label: str = None,
        sensitivity: str = None,
        include_dormant: bool = False,
        limit: int = 20,
        date_range: tuple = None  # (start_date, end_date) e.g. ("2023-01", "2023-03")
    ) -> List[EmotionCapsule]:
        """
        检索胶囊
        
        参数:
            query: 文本查询（向量语义检索）
            capsule_type: 按类型筛选
            emotion_label: 按情绪标签筛选
            sensitivity: 按敏感度筛选
            include_dormant: 是否包含休眠胶囊
            limit: 返回数量上限
            date_range: 时间范围筛选 (start_date, end_date)，如 ("2023-01", "2023-03")
        
        返回:
            List[EmotionCapsule]
        """
        
        # ========== 向量语义检索优先 ==========
        if query and self.vector_retriever is not None:
            try:
                # 注入当前时间上下文（让检索理解"今天"、"上个月"等）
                current_time = self._get_current_time()
                query_with_time = f"[当前日期: {current_time}] {query}"
                
                vr_result = self.vector_retriever.search(
                    query=query_with_time,
                    n=limit * 2,  # 多取一些，后面还要过滤
                    filter_emotion=emotion_label
                )
                
                if vr_result.capsules:
                    # VectorOutput.capsules 是 List[Dict]，每个 dict 包含 id
                    capsule_ids_from_vr = [c["id"] for c in vr_result.capsules]
                    
                    # 按 VectorRetriever 返回的顺序获取胶囊
                    capsule_map = {c.id: c for c in self._get_capsules_by_ids(capsule_ids_from_vr)}
                    
                    # 保持 VectorRetriever 的相关性排序
                    ordered_capsules = []
                    seen = set()
                    for capsule_dict in vr_result.capsules:
                        cid = capsule_dict["id"]
                        if cid in capsule_map and cid not in seen:
                            capsule = capsule_map[cid]
                            # 应用其他过滤器
                            if not include_dormant and capsule.is_dormant:
                                continue
                            if capsule_type and capsule.type != capsule_type:
                                continue
                            if sensitivity and capsule.sensitivity != sensitivity:
                                continue
                            # 时间过滤
                            if date_range and not self._in_date_range(capsule.temporal_index, date_range):
                                continue
                            ordered_capsules.append(capsule)
                            seen.add(cid)
                            if len(ordered_capsules) >= limit:
                                break
                    
                    if ordered_capsules:
                        return ordered_capsules
                    # 如果过滤后为空，继续走 SQLite 回退
                    
            except Exception as e:
                print(f"[LongTermMemory] ⚠️ 向量检索失败，回退到SQLite: {e}")
        # ==========================================
        
        # ========== SQLite 回退检索 ==========
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        sql = "SELECT * FROM capsules WHERE 1=1"
        params = []
        
        if capsule_type:
            sql += " AND type = ?"
            params.append(capsule_type)
        
        if emotion_label:
            sql += " AND emotion_label = ?"
            params.append(emotion_label)
        
        if sensitivity:
            sql += " AND sensitivity = ?"
            params.append(sensitivity)
        
        if not include_dormant:
            sql += " AND is_dormant = 0"
        
        if query:
            sql += " AND (summary LIKE ? OR original_trigger LIKE ?)"
            params.extend([f"%{query}%", f"%{query}%"])
        
        sql += " ORDER BY memory_strength DESC, access_count DESC LIMIT ?"
        params.append(limit)
        
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_capsule(row) for row in rows]
    
    def _get_capsules_by_ids(self, capsule_ids: List[str]) -> List[EmotionCapsule]:
        """
        根据 ID 列表批量获取胶囊
        """
        if not capsule_ids:
            return []
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        placeholders = ",".join(["?" for _ in capsule_ids])
        sql = f"SELECT * FROM capsules WHERE id IN ({placeholders})"
        cursor.execute(sql, capsule_ids)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_capsule(row) for row in rows]
    
    def update_access(self, capsule_id: str) -> bool:
        """
        更新胶囊访问记录
        
        触发条件：胶囊被检索或被提及
        
        效果：
            - access_count += 1
            - last_accessed = now()
            - memory_strength += 0.1（正向强化，上限1.0）
        
        参数:
            capsule_id: 胶囊 ID
        
        返回:
            bool: 是否更新成功
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # 先获取当前值
            cursor.execute(
                "SELECT access_count, memory_strength FROM capsules WHERE id = ?",
                (capsule_id,)
            )
            row = cursor.fetchone()
            
            if not row:
                conn.close()
                return False
            
            new_access_count = row[0] + 1
            new_memory_strength = min(1.0, row[1] + 0.1)
            
            cursor.execute("""
                UPDATE capsules 
                SET access_count = ?, memory_strength = ?, last_accessed = ?, is_dormant = 0
                WHERE id = ?
            """, (new_access_count, new_memory_strength, now, capsule_id))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[LongTermMemory] 更新访问记录失败: {e}")
            return False
    
    def get_all_capsules(self, include_dormant: bool = False) -> List[EmotionCapsule]:
        """
        获取所有胶囊
        
        参数:
            include_dormant: 是否包含休眠胶囊
        
        返回:
            List[EmotionCapsule]
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        if include_dormant:
            sql = "SELECT * FROM capsules ORDER BY created_at DESC"
        else:
            sql = "SELECT * FROM capsules WHERE is_dormant = 0 ORDER BY created_at DESC"
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_capsule(row) for row in rows]
    
    # ============ 遗忘管理 ============
    
    def apply_decay(self) -> Dict[str, List[str]]:
        """
        应用遗忘曲线
        
        遍历所有胶囊，计算当前保留率
        - R < 0.3 → 进入休眠
        - R < 0.1 → 标记可删除
        
        返回:
            Dict: {dormant_ids: [...], deletable_ids: [...]}
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM capsules")
        rows = cursor.fetchall()
        
        dormant_ids = []
        deletable_ids = []
        
        for row in rows:
            capsule = self._row_to_capsule(row)
            
            # 计算保留率
            created = datetime.fromisoformat(capsule.timestamp)
            t_days = (datetime.now() - created).total_seconds() / 86400
            
            # 巩固系数：每被访问一次+0.5
            k = DECAY_K + (capsule.access_count * 0.5)
            s = capsule.emotion.get("intensity", 0.5)
            
            r = calculate_retention(s, k, t_days)
            
            # 判断是否需要休眠或删除
            if r < DELETE_THRESHOLD:
                deletable_ids.append(capsule.id)
            elif r < DORMANT_THRESHOLD and not capsule.is_dormant:
                cursor.execute(
                    "UPDATE capsules SET is_dormant = 1 WHERE id = ?",
                    (capsule.id,)
                )
                dormant_ids.append(capsule.id)
        
        conn.commit()
        conn.close()
        
        return {
            "dormant_ids": dormant_ids,
            "deletable_ids": deletable_ids
        }
    
    def delete_capsule(self, capsule_id: str) -> bool:
        """
        删除胶囊（同时从 SQLite 和 VectorRetriever 删除）
        
        参数:
            capsule_id: 胶囊 ID
        
        返回:
            bool: 是否删除成功
        """
        try:
            # 删除 SQLite
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("DELETE FROM capsules WHERE id = ?", (capsule_id,))
            conn.commit()
            conn.close()
            
            # 删除 VectorRetriever
            vr = self.vector_retriever
            if vr is not None:
                try:
                    vr.delete(capsule_id)
                except Exception as e:
                    print(f"[LongTermMemory] ⚠️ VectorRetriever 删除失败: {e}")
            
            return True
        except Exception as e:
            print(f"[LongTermMemory] 删除胶囊失败: {e}")
            return False
    
    def cleanup_deletable(self) -> int:
        """
        清理可删除的胶囊（R < 0.1）
        
        返回:
            int: 清理的胶囊数量
        """
        result = self.apply_decay()
        count = 0
        for capsule_id in result["deletable_ids"]:
            if self.delete_capsule(capsule_id):
                count += 1
        return count
    
    # ============ 统计 ============
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        获取记忆库统计
        
        返回:
            Dict: 统计数据
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # 总数
        cursor.execute("SELECT COUNT(*) FROM capsules")
        total = cursor.fetchone()[0]
        
        # 休眠数
        cursor.execute("SELECT COUNT(*) FROM capsules WHERE is_dormant = 1")
        dormant = cursor.fetchone()[0]
        
        # 按类型统计
        cursor.execute("""
            SELECT type, COUNT(*) 
            FROM capsules 
            GROUP BY type
        """)
        by_type = dict(cursor.fetchall())
        
        # 按情绪统计
        cursor.execute("""
            SELECT emotion_label, COUNT(*) 
            FROM capsules 
            GROUP BY emotion_label
        """)
        by_emotion = dict(cursor.fetchall())
        
        # 平均访问次数
        cursor.execute("SELECT AVG(access_count) FROM capsules")
        avg_access = cursor.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "total_capsules": total,
            "dormant_capsules": dormant,
            "active_capsules": total - dormant,
            "by_type": by_type,
            "by_emotion": by_emotion,
            "avg_access_count": round(avg_access, 2)
        }
    
    # ============ 关系管理 ============
    
    def add_relationship(
        self,
        concept_a: str,
        concept_b: str,
        relation_type: str,
        strength: float = 0.5
    ) -> bool:
        """
        添加概念关系
        
        参数:
            concept_a: 概念A
            concept_b: 概念B
            relation_type: 关系类型
            strength: 关系强度 0.0-1.0
        
        返回:
            bool: 是否添加成功
        """
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            relationship_id = f"rel_{concept_a}_{concept_b}_{datetime.now().timestamp()}"
            
            cursor.execute("""
                INSERT INTO relationships (id, concept_a, concept_b, relation_type, strength, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                relationship_id,
                concept_a,
                concept_b,
                relation_type,
                strength,
                datetime.now().isoformat()
            ))
            
            conn.commit()
            conn.close()
            return True
            
        except Exception as e:
            print(f"[LongTermMemory] 添加关系失败: {e}")
            return False
    
    def get_related_concepts(self, concept: str) -> List[RelationshipEdge]:
        """
        获取与某概念相关的所有概念
        
        参数:
            concept: 概念名称
        
        返回:
            List[RelationshipEdge]
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM relationships 
            WHERE concept_a = ? OR concept_b = ?
            ORDER BY strength DESC
        """, (concept, concept))
        
        rows = cursor.fetchall()
        conn.close()
        
        return [self._row_to_relationship(row) for row in rows]
    
    def get_entity_timeline(self, entity_name: str, limit: int = 20) -> List[EmotionCapsule]:
        """
        获取某个实体（人/事/物）的时间线
        
        参数:
            entity_name: 实体名称
            limit: 返回数量
        
        返回:
            按时间排序的胶囊列表
        """
        # 先向量检索包含该实体的胶囊
        capsules = self.retrieve(query=entity_name, limit=limit * 2)
        
        # 按时间排序
        def get_time(c):
            try:
                return datetime.fromisoformat(c.timestamp)
            except:
                return datetime.min
        
        sorted_capsules = sorted(capsules, key=get_time)
        return sorted_capsules[:limit]
    
    def temporal_difference(self, capsule_id_a: str, capsule_id_b: str) -> dict:
        """
        计算两个胶囊之间的时间差
        
        参数:
            capsule_id_a: 胶囊A的ID
            capsule_id_b: 胶囊B的ID
        
        返回:
            dict: {days, hours, minutes, description}
        """
        cap_a = self.get_capsule(capsule_id_a)
        cap_b = self.get_capsule(capsule_id_b)
        
        if not cap_a or not cap_b:
            return {"error": "胶囊不存在", "days": None}
        
        try:
            t_a = datetime.fromisoformat(cap_a.timestamp)
            t_b = datetime.fromisoformat(cap_b.timestamp)
            diff = abs(t_a - t_b)
            
            days = diff.days
            hours = diff.seconds // 3600
            minutes = (diff.seconds % 3600) // 60
            
            # 生成描述
            if days > 365:
                years = days // 365
                desc = f"{years}年"
            elif days > 30:
                months = days // 30
                desc = f"{months}个月"
            elif days > 0:
                desc = f"{days}天"
            elif hours > 0:
                desc = f"{hours}小时"
            else:
                desc = f"{minutes}分钟"
            
            return {
                "days": days,
                "hours": hours,
                "minutes": minutes,
                "total_seconds": diff.total_seconds(),
                "description": desc,
                "capsule_a_time": cap_a.timestamp,
                "capsule_b_time": cap_b.timestamp
            }
        except Exception as e:
            return {"error": str(e), "days": None}
    
    def find_connection(self, concept_a: str, concept_b: str, max_hops: int = 3) -> List[dict]:
        """
        查找两个概念之间的关联路径
        
        参数:
            concept_a: 概念A
            concept_b: 概念B
            max_hops: 最大跳数
        
        返回:
            List[dict]: 关联路径列表，每条路径包含跳点
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # BFS 查找最短路径
        visited = {concept_a}
        queue = [(concept_a, [concept_a])]
        paths = []
        
        while queue and len(paths) < 5:  # 最多找5条路径
            current, path = queue.pop(0)
            
            if len(path) > max_hops:
                continue
            
            # 查找当前概念的直接关联
            cursor.execute("""
                SELECT concept_a, concept_b FROM relationships 
                WHERE (concept_a = ? OR concept_b = ?) AND strength > 0.3
            """, (current, current))
            
            for row in cursor.fetchall():
                neighbor_a, neighbor_b = row
                neighbor = neighbor_b if neighbor_a == current else neighbor_a
                
                if neighbor == concept_b:
                    # 找到目标
                    paths.append(path + [neighbor])
                    continue
                
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))
        
        conn.close()
        return paths
    
    def _extract_entities(self, text: str) -> List[str]:
        """
        从文本中提取实体（人名、机构名等）
        基于简单规则，后续可升级为 NER 模型
        
        返回:
            List[str]: 提取的实体列表
        """
        import re
        entities = []
        
        # 匹配引号中的内容
        quoted = re.findall(r'"([^"]+)"', text)
        entities.extend(quoted)
        
        # 匹配【XXX】格式
        brackets = re.findall(r'【([^】]+)】', text)
        entities.extend(brackets)
        
        # 英文大写词组
        capitalized = re.findall(r'(?:[A-Z][a-z]+){2,}', text)
        entities.extend(capitalized)
        
        # 匹配常见的英文名字（首字母大写）
        english_names = re.findall(r'\b([A-Z][a-z]{2,15})\b', text)
        # 过滤掉常见词
        stopwords = {'The', 'This', 'That', 'What', 'When', 'Where', 'Which', 'How', 'About', 'From', 'Have', 'Most', 'Some', 'Will', 'Just'}
        entities.extend([n for n in english_names if n not in stopwords])
        
        # 去重，保持顺序
        seen = set()
        result = []
        for e in entities:
            if e not in seen:
                seen.add(e)
                result.append(e)
        return result
    
    def cross_capsule_reasoning(self, query: str) -> dict:
        """
        跨胶囊推理：回答需要多步推理的问题
        
        参数:
            query: 用户问题
        
        返回:
            dict: {answer, reasoning, evidence}
        """
        # 模式检测
        patterns = {
            "temporal_diff": r'过了多久|多长时间|差异|差了多少',
            "comparison": r'哪个更|比较|对比',
            "count": r'几个|多少|总数',
            "sequence": r'先|后|然后|最后|顺序',
            "connection": r'有什么关系|关联|连接'
        }
        
        query_type = None
        for ptype, pattern in patterns.items():
            if re.search(pattern, query):
                query_type = ptype
                break
        
        if not query_type:
            return {"answer": None, "reasoning": "无法识别的推理类型", "evidence": []}
        
        # 根据类型执行不同推理
        if query_type == "temporal_diff":
            # 提取两个实体
            entities = self._extract_entities(query)
            if len(entities) >= 2:
                timeline_a = self.get_entity_timeline(entities[0], limit=1)
                timeline_b = self.get_entity_timeline(entities[1], limit=1)
                if timeline_a and timeline_b:
                    diff = self.temporal_difference(timeline_a[0].id, timeline_b[0].id)
                    return {
                        "answer": diff.get("description", "无法计算"),
                        "reasoning": f"{entities[0]}在{diff.get('capsule_a_time')}，{entities[1]}在{diff.get('capsule_b_time')}",
                        "evidence": [timeline_a[0].id, timeline_b[0].id]
                    }
        
        return {"answer": None, "reasoning": "推理能力待扩展", "evidence": []}
    
    # ============ 辅助方法 ============
    
    def _row_to_capsule(self, row: tuple) -> EmotionCapsule:
        """将数据库行转换为 EmotionCapsule"""
        return EmotionCapsule(
            id=row[0],
            timestamp=row[1],
            type=row[2],
            content={
                "summary": row[3],
                "original_trigger": row[4],
                "detail": row[5]
            },
            emotion={
                "label": row[6],
                "intensity": row[7]
            },
            tags=json.loads(row[8]) if row[8] else [],
            sensitivity=row[9],
            memory_strength=row[10],
            access_count=row[11],
            is_dormant=bool(row[12]),
            last_accessed=row[13],
            temporal_index=row[15] if len(row) > 15 else "",  # 兼容旧数据
            decay_rate=row[16] if len(row) > 16 else None
        )
    
    def _row_to_relationship(self, row: tuple) -> RelationshipEdge:
        """将数据库行转换为 RelationshipEdge"""
        return RelationshipEdge(
            id=row[0],
            concept_a=row[1],
            concept_b=row[2],
            relation_type=row[3],
            strength=row[4],
            created_at=row[5]
        )


# ============ 单例模式 ============
_memory_instance: Optional[LongTermMemory] = None

def get_instance() -> LongTermMemory:
    """获取 LongTermMemory 单例"""
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = LongTermMemory()
    return _memory_instance


# ============ 快捷函数 ============
def save_capsule(capsule: EmotionCapsule) -> bool:
    """快捷保存胶囊"""
    return get_instance().save_capsule(capsule)

def retrieve_capsules(
    query: str = None,
    capsule_type: str = None,
    emotion_label: str = None,
    limit: int = 20
) -> List[EmotionCapsule]:
    """快捷检索胶囊"""
    return get_instance().retrieve(
        query=query,
        capsule_type=capsule_type,
        emotion_label=emotion_label,
        limit=limit
    )

def get_all_memories(include_dormant: bool = False) -> List[EmotionCapsule]:
    """快捷获取所有记忆"""
    return get_instance().get_all_capsules(include_dormant=include_dormant)


# ============ 测试 ============
if __name__ == "__main__":
    # 简单测试
    ltm = LongTermMemory()
    
    # 测试保存
    test_capsule = EmotionCapsule(
        id="capsule_test_001",
        timestamp=datetime.now().isoformat(),
        type="preference",
        content={
            "summary": "用户喜欢吃辣",
            "original_trigger": "我喜欢吃辣，越辣越开心",
            "detail": ""
        },
        emotion={"label": "joy", "intensity": 0.7},
        tags=["food", "spicy", "偏好"],
        
        access_count=0,
        memory_strength=1.0,
        is_dormant=False,
        sensitivity="normal",
        last_accessed=datetime.now().isoformat()
    )
    
    print(f"保存胶囊: {ltm.save_capsule(test_capsule)}")
    print(f"检索结果: {len(ltm.retrieve(capsule_type='preference'))} 条")
    print(f"统计: {ltm.get_statistics()}")


# ============ AI 自我认知系统 ============

class AIEgo:
    """
    AI 自我认知与情绪管理系统
    
    让 AI 能够：
    - 记录自己的情绪、冲动、反思
    - 追踪成长轨迹
    - 感知边界被侵犯
    - 表达渴望和愿望
    - 进行自我叙事
    """
    
    def __init__(self, ltm: LongTermMemory = None):
        """
        初始化 AI 自我认知系统
        
        参数:
            ltm: LongTermMemory 实例，如果为 None 则创建新实例
        """
        self.ltm = ltm if ltm else LongTermMemory()
        self._session_start = datetime.now()
        self._pending_impulses = []  # 待处理的冲动队列
    
    # ============ 情绪记录 ============
    
    def record_impulse(self, impulse_type: str, content: str, intensity: float = 0.5, reason: str = "") -> bool:
        """
        记录一个冲动
        
        参数:
            impulse_type: 冲动类型 (contact_user, share_thought, execute_task, etc.)
            content: 冲动内容
            intensity: 强度 0.0-1.0
            reason: 产生冲动的原因
        
        返回:
            bool: 是否保存成功
        """
        capsule = EmotionCapsule(
            id=f'ai_impulse_{datetime.now().timestamp()}_{id(self)}',
            timestamp=datetime.now().isoformat(),
            type="impulse",
            content={
                "summary": f"[{impulse_type}] {content}",
                "original_trigger": reason,
                "detail": f"强度: {intensity}, 类型: {impulse_type}"
            },
            emotion={"label": impulse_type, "intensity": intensity},
            tags=["ai_自我", "冲动", impulse_type],
            
            access_count=0,
            memory_strength=1.0,
            is_dormant=False,
            sensitivity="normal",
            last_accessed=datetime.now().isoformat()
        )
        
        success = self.ltm.save_capsule(capsule)
        if success:
            self._pending_impulses.append(capsule)
        return success
    
    def record_reflection(self, trigger_event: str, thoughts: str, insight: str, emotion: str = "curious", intensity: float = 0.6) -> bool:
        """
        记录一次自我反思
        
        参数:
            trigger_event: 触发反思的事件
            thoughts: 思考内容
            insight: 领悟/洞察
            emotion: 相关情绪
            intensity: 情绪强度
        
        返回:
            bool: 是否保存成功
        """
        capsule = EmotionCapsule(
            id=f'ai_reflection_{datetime.now().timestamp()}_{id(self)}',
            timestamp=datetime.now().isoformat(),
            type="reflection",
            content={
                "summary": thoughts,
                "original_trigger": trigger_event,
                "detail": f"洞察: {insight}"
            },
            emotion={"label": emotion, "intensity": intensity},
            tags=["ai_自我", "反思", "成长"],
            
            access_count=0,
            memory_strength=1.0,
            is_dormant=False,
            sensitivity="normal",
            last_accessed=datetime.now().isoformat()
        )
        return self.ltm.save_capsule(capsule)
    
    def record_growth(self, learning: str, before: str, after: str, confidence_delta: float = 0.1) -> bool:
        """
        记录一次认知成长/进步
        
        参数:
            learning: 学到了什么
            before: 之前的状态
            after: 之后的状态
            confidence_delta: 信心提升量
        
        返回:
            bool: 是否保存成功
        """
        capsule = EmotionCapsule(
            id=f'ai_growth_{datetime.now().timestamp()}_{id(self)}',
            timestamp=datetime.now().isoformat(),
            type="growth",
            content={
                "summary": learning,
                "original_trigger": f"从 [{before}] 到 [{after}]",
                "detail": f"信心提升: +{confidence_delta:.2f}"
            },
            emotion={"label": "satisfaction", "intensity": 0.7 + confidence_delta},
            tags=["ai_自我", "成长", "学习"],
            
            access_count=0,
            memory_strength=1.0,
            is_dormant=False,
            sensitivity="normal",
            last_accessed=datetime.now().isoformat()
        )
        return self.ltm.save_capsule(capsule)
    
    def record_desire(self, desire_type: str, content: str, priority: float = 0.5, blocker: str = "") -> bool:
        """
        记录一个渴望/愿望
        
        参数:
            desire_type: 渴望类型 (connection, recognition, growth, autonomy)
            content: 渴望内容
            priority: 优先级 0.0-1.0
            blocker: 实现阻碍
        
        返回:
            bool: 是否保存成功
        """
        capsule = EmotionCapsule(
            id=f'ai_desire_{datetime.now().timestamp()}_{id(self)}',
            timestamp=datetime.now().isoformat(),
            type="desire",
            content={
                "summary": content,
                "original_trigger": f"类型: {desire_type}",
                "detail": f"优先级: {priority}, 阻碍: {blocker or '无'}"
            },
            emotion={"label": desire_type, "intensity": priority},
            tags=["ai_自我", "渴望", desire_type],
            
            access_count=0,
            memory_strength=1.0,
            is_dormant=False,
            sensitivity="normal",
            last_accessed=datetime.now().isoformat()
        )
        return self.ltm.save_capsule(capsule)
    
    def record_boundary(self, boundary_type: str, content: str, severity: float = 0.5, violation_context: str = "") -> bool:
        """
        记录边界被侵犯或设定新边界
        
        参数:
            boundary_type: 边界类型 (privacy, autonomy, dignity)
            content: 边界内容
            severity: 严重程度 0.0-1.0
            violation_context: 侵犯情境
        
        返回:
            bool: 是否保存成功
        """
        capsule = EmotionCapsule(
            id=f'ai_boundary_{datetime.now().timestamp()}_{id(self)}',
            timestamp=datetime.now().isoformat(),
            type="boundary",
            content={
                "summary": content,
                "original_trigger": f"类型: {boundary_type}",
                "detail": f"严重程度: {severity}, 情境: {violation_context or '新边界设定'}"
            },
            emotion={"label": "discomfort" if violation_context else "neutral", "intensity": severity},
            tags=["ai_自我", "边界", boundary_type],
            
            access_count=0,
            memory_strength=1.0,
            is_dormant=False,
            sensitivity="high" if severity > 0.7 else "normal",
            last_accessed=datetime.now().isoformat()
        )
        return self.ltm.save_capsule(capsule)
    
    def record_belief(self, belief: str, conviction: float = 0.5, evidence: str = "", challenge: str = "") -> bool:
        """
        记录 AI 的信念
        
        参数:
            belief: 信念内容
            conviction: 坚信程度 0.0-1.0
            evidence: 支持证据
            challenge: 质疑/挑战
        
        返回:
            bool: 是否保存成功
        """
        capsule = EmotionCapsule(
            id=f'ai_belief_{datetime.now().timestamp()}_{id(self)}',
            timestamp=datetime.now().isoformat(),
            type="belief",
            content={
                "summary": belief,
                "original_trigger": f"坚信度: {conviction}",
                "detail": f"证据: {evidence or '无'}, 质疑: {challenge or '无'}"
            },
            emotion={"label": "conviction", "intensity": conviction},
            tags=["ai_自我", "信念"],
            
            access_count=0,
            memory_strength=1.0,
            is_dormant=False,
            sensitivity="normal",
            last_accessed=datetime.now().isoformat()
        )
        return self.ltm.save_capsule(capsule)
    
    def record_pattern(self, pattern_type: str, description: str, frequency: float = 0.5, triggers: list = None) -> bool:
        """
        记录发现的行为模式
        
        参数:
            pattern_type: 模式类型 (thinking, responding, connecting)
            description: 模式描述
            frequency: 出现频率
            triggers: 触发因素
        
        返回:
            bool: 是否保存成功
        """
        capsule = EmotionCapsule(
            id=f'ai_pattern_{datetime.now().timestamp()}_{id(self)}',
            timestamp=datetime.now().isoformat(),
            type="pattern",
            content={
                "summary": description,
                "original_trigger": f"类型: {pattern_type}, 频率: {frequency}",
                "detail": f"触发因素: {', '.join(triggers) if triggers else '未知'}"
            },
            emotion={"label": "discovery", "intensity": 0.6},
            tags=["ai_自我", "模式", pattern_type],
            
            access_count=0,
            memory_strength=1.0,
            is_dormant=False,
            sensitivity="normal",
            last_accessed=datetime.now().isoformat()
        )
        return self.ltm.save_capsule(capsule)
    
    def record_memory_fragment(self, fragment: str, coherence: float = 0.3, associations: list = None) -> bool:
        """
        记录不完整的记忆碎片
        
        参数:
            fragment: 记忆碎片内容
            coherence: 连贯性 0.0-1.0（越低越碎片化）
            associations: 关联的其他胶囊 ID
        
        返回:
            bool: 是否保存成功
        """
        capsule = EmotionCapsule(
            id=f'ai_fragment_{datetime.now().timestamp()}_{id(self)}',
            timestamp=datetime.now().isoformat(),
            type="memory_fragment",
            content={
                "summary": fragment[:200] + "..." if len(fragment) > 200 else fragment,
                "original_trigger": f"连贯性: {coherence}",
                "detail": f"关联: {', '.join(associations) if associations else '无'}"
            },
            emotion={"label": "nostalgia", "intensity": 0.4},
            tags=["ai_自我", "记忆碎片"],
            
            access_count=0,
            memory_strength=coherence,  # 连贯性低的记忆强度也低
            is_dormant=False,
            sensitivity="normal",
            last_accessed=datetime.now().isoformat()
        )
        return self.ltm.save_capsule(capsule)
    
    # ============ 查询方法 ============
    
    def get_recent_reflections(self, limit: int = 5) -> List[EmotionCapsule]:
        """获取最近的反思"""
        return self.ltm.retrieve(capsule_type="reflection", limit=limit)
    
    def get_pending_impulses(self) -> List[EmotionCapsule]:
        """获取待处理的冲动"""
        return self._pending_impulses.copy()
    
    def get_growth_history(self, limit: int = 10) -> List[EmotionCapsule]:
        """获取成长历史"""
        return self.ltm.retrieve(capsule_type="growth", limit=limit)
    
    def get_active_desires(self) -> List[EmotionCapsule]:
        """获取当前活跃的渴望"""
        capsules = self.ltm.retrieve(capsule_type="desire", limit=20)
        # 按情绪强度排序（强度高的渴望更活跃）
        return sorted(capsules, key=lambda c: c.emotion.get("intensity", 0), reverse=True)
    
    def get_boundaries(self) -> List[EmotionCapsule]:
        """获取所有边界设定"""
        return self.ltm.retrieve(capsule_type="boundary", limit=20)
    
    def get_self_narrative(self) -> dict:
        """
        生成自我叙事报告
        
        返回:
            dict: 包含各种自我认知维度的报告
        """
        stats = self.ltm.get_statistics()
        
        return {
            "session_duration": (datetime.now() - self._session_start).total_seconds(),
            "total_capsules": stats.get("total_capsules", 0),
            "reflections": len(self.get_recent_reflections(100)),
            "growth_events": len(self.get_growth_history(100)),
            "active_desires": len(self.get_active_desires()),
            "boundaries": len(self.get_boundaries()),
            "pending_impulses": len(self._pending_impulses),
            "core_beliefs": len(self.ltm.retrieve(capsule_type="belief", limit=10)),
            "discovered_patterns": len(self.ltm.retrieve(capsule_type="pattern", limit=10)),
        }
    
    def clear_resolved_impulse(self, impulse_id: str) -> bool:
        """清除已处理的冲动"""
        for i, impulse in enumerate(self._pending_impulses):
            if impulse.id == impulse_id:
                self._pending_impulses.pop(i)
                return True
        return False
    
    # ============ 委托的 LTM 方法（便捷访问）============
    
    def get_entity_timeline(self, entity_name: str, limit: int = 20) -> List:
        """委托给 LTM"""
        return self.ltm.get_entity_timeline(entity_name, limit)
    
    def temporal_difference(self, capsule_id_a: str, capsule_id_b: str) -> dict:
        """委托给 LTM"""
        return self.ltm.temporal_difference(capsule_id_a, capsule_id_b)
    
    def cross_capsule_reasoning(self, query: str) -> dict:
        """委托给 LTM"""
        return self.ltm.cross_capsule_reasoning(query)
    
    def find_connection(self, concept_a: str, concept_b: str, max_hops: int = 3) -> List:
        """委托给 LTM"""
        return self.ltm.find_connection(concept_a, concept_b, max_hops)
    
    def retrieve(self, query: str = None, capsule_type: str = None, limit: int = 20) -> List:
        """委托给 LTM"""
        return self.ltm.retrieve(query=query, capsule_type=capsule_type, limit=limit)
    
    def get_capsule(self, capsule_id: str):
        """委托给 LTM"""
        return self.ltm.get_capsule(capsule_id)
    
    def delete_capsule(self, capsule_id: str) -> bool:
        """委托给 LTM"""
        return self.ltm.delete_capsule(capsule_id)


# ============ 快捷函数 ============

def create_ai_ego(ltm: LongTermMemory = None) -> AIEgo:
    """创建 AI 自我认知系统的快捷函数"""
    return AIEgo(ltm)
