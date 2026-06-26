"""
弘脑记忆系统 - 用户偏好学习模块
HongNao Memory OS - User Preference Learning Module

功能：
- 从对话中自动识别用户偏好
- 偏好分类和标签化
- 偏好重要性动态调整
- 偏好冲突检测与解决
"""

import re
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
import sys

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent))

from storage_layer import MemCell, MemScene, SQLiteStorage
from vector_store import ChromaVectorStore
from memory_api import HongNaoMemorySystem, MemorySystemConfig


@dataclass
class Preference:
    """用户偏好数据类"""
    id: str
    content: str
    category: str  # 偏好分类
    tags: List[str] = field(default_factory=list)
    importance: float = 5.0  # 重要性 1-10
    confidence: float = 0.0  # 置信度 0-1
    source: str = ""
    created_at: str = ""
    updated_at: str = ""
    access_count: int = 0
    last_accessed: str = ""
    
    def __post_init__(self):
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        if not self.updated_at:
            self.updated_at = self.created_at
    
    def to_dict(self) -> Dict:
        return {
            'id': self.id,
            'content': self.content,
            'category': self.category,
            'tags': self.tags,
            'importance': self.importance,
            'confidence': self.confidence,
            'source': self.source,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'access_count': self.access_count,
            'last_accessed': self.last_accessed,
        }


class PreferencePatterns:
    """偏好识别模式"""
    
    # 偏好表达模式
    PATTERNS = {
        'like': [
            r'我喜欢 (.+)',
            r'我偏好 (.+)',
            r'我更倾向于 (.+)',
            r'我习惯 (.+)',
            r'我通常 (.+)',
            r'我一般 (.+)',
            r'我喜欢(.+)',
            r'我偏好(.+)',
        ],
        'dislike': [
            r'我不喜欢 (.+)',
            r'我讨厌 (.+)',
            r'我反感 (.+)',
            r'我不太喜欢 (.+)',
            r'我避免 (.+)',
            r'我不喜欢(.+)',
            r'我讨厌(.+)',
        ],
        'style': [
            r'我喜欢(.+?) 的风格',
            r'我喜欢(.+?) 方式',
            r'请用 (.+?) 的方式',
            r'用 (.+?) 风格',
        ],
        'habit': [
            r'我每天早上 (.+)',
            r'我通常 (.+?) 时间',
            r'我习惯在 (.+)',
            r'我每天 (.+)',
        ],
    }
    
    # 偏好分类关键词
    CATEGORIES = {
        'communication': ['沟通', '交流', '回复', '说话', '风格', '语气', '简洁', '直接', '详细'],
        'work': ['工作', '开发', '编程', '代码', '工具', '软件', '技术'],
        'learning': ['学习', '阅读', '知识', '技能', '培训'],
        'lifestyle': ['生活', '习惯', '作息', '饮食', '运动', '健康'],
        'information': ['信息', '新闻', '报告', '数据', '资讯'],
        'interaction': ['交互', '界面', '操作', '使用', '体验'],
    }
    
    @classmethod
    def extract_preferences(cls, text: str) -> List[Dict]:
        """从文本中提取偏好"""
        preferences = []
        
        for pattern_type, patterns in cls.PATTERNS.items():
            for pattern in patterns:
                matches = re.finditer(pattern, text, re.IGNORECASE)
                for match in matches:
                    preference_text = match.group(1).strip()
                    if preference_text and len(preference_text) < 100:  # 过滤过长的匹配
                        pref = cls._create_preference(
                            text=preference_text,
                            pattern_type=pattern_type,
                            original_text=text
                        )
                        if pref:
                            preferences.append(pref)
        
        return preferences
    
    @classmethod
    def _create_preference(cls, text: str, pattern_type: str, original_text: str) -> Optional[Dict]:
        """创建偏好对象"""
        # 判断正负向
        is_negative = pattern_type == 'dislike'
        
        # 分类
        category = cls._classify(text)
        
        # 标签
        tags = cls._extract_tags(text)
        
        # 置信度
        confidence = cls._calculate_confidence(text, pattern_type)
        
        content = f"{'不' if is_negative else ''}喜欢{text}"
        
        return {
            'content': content,
            'category': category,
            'tags': tags,
            'confidence': confidence,
            'pattern_type': pattern_type,
        }
    
    @classmethod
    def _classify(cls, text: str) -> str:
        """偏好分类"""
        scores = {}
        for category, keywords in cls.CATEGORIES.items():
            score = sum(1 for kw in keywords if kw in text)
            scores[category] = score
        
        if max(scores.values()) > 0:
            return max(scores, key=scores.get)
        return 'general'  # 默认分类
    
    @classmethod
    def _extract_tags(cls, text: str) -> List[str]:
        """提取标签"""
        # 简单分词作为标签
        tags = []
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', text)
        for word in words:
            if len(word) >= 2 and len(word) <= 10:  # 过滤太短或太长的词
                tags.append(word)
        return tags[:5]  # 最多 5 个标签
    
    @classmethod
    def _calculate_confidence(cls, text: str, pattern_type: str) -> float:
        """计算置信度"""
        confidence = 0.5  # 基础置信度
        
        # 明确表达提高置信度
        if any(kw in text for kw in ['非常', '特别', '极其', '一定']):
            confidence += 0.2
        
        # 具体细节提高置信度
        if len(text) > 10:
            confidence += 0.1
        
        # 重复强调提高置信度
        if pattern_type in ['like', 'dislike']:
            confidence += 0.1
        
        return min(confidence, 1.0)


class UserPreferenceLearner:
    """用户偏好学习器"""
    
    def __init__(self, memory_system: HongNaoMemorySystem):
        self.memory_system = memory_system
        self.preference_file = Path(__file__).parent / "user_preferences.json"
        self.preferences: Dict[str, Preference] = {}
        self._load_preferences()
    
    def _load_preferences(self):
        """加载已保存的偏好"""
        if self.preference_file.exists():
            with open(self.preference_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                for pid, pdata in data.items():
                    self.preferences[pid] = Preference(**pdata)
    
    def _save_preferences(self):
        """保存偏好"""
        data = {pid: pref.to_dict() for pid, pref in self.preferences.items()}
        with open(self.preference_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    def learn_from_conversation(self, 
                                conversation_text: str,
                                source: str = "conversation") -> List[Preference]:
        """
        从对话中学习用户偏好
        
        Args:
            conversation_text: 对话文本
            source: 来源标识
        
        Returns:
            学习到的偏好列表
        """
        # 提取偏好
        extracted = PreferencePatterns.extract_preferences(conversation_text)
        
        new_preferences = []
        for ext in extracted:
            # 创建偏好 ID
            pref_id = self._generate_id(ext['content'])
            
            # 检查是否已存在
            if pref_id in self.preferences:
                # 更新已有偏好
                self._update_preference(pref_id, ext)
            else:
                # 创建新偏好
                pref = self._create_preference(pref_id, ext, source)
                self.preferences[pref_id] = pref
                new_preferences.append(pref)
                
                # 同步到记忆系统
                self._sync_to_memory(pref)
        
        # 保存
        if new_preferences:
            self._save_preferences()
        
        return new_preferences
    
    def _generate_id(self, content: str) -> str:
        """生成偏好 ID"""
        import hashlib
        return hashlib.md5(content.encode('utf-8')).hexdigest()[:12]
    
    def _create_preference(self, 
                          pref_id: str, 
                          ext: Dict, 
                          source: str) -> Preference:
        """创建偏好对象"""
        now = datetime.now().isoformat()
        return Preference(
            id=pref_id,
            content=ext['content'],
            category=ext['category'],
            tags=ext['tags'],
            importance=6.0,
            confidence=ext['confidence'],
            source=source,
            created_at=now,
            updated_at=now
        )
    
    def _update_preference(self, pref_id: str, ext: Dict):
        """更新已有偏好"""
        pref = self.preferences[pref_id]
        pref.access_count += 1
        pref.last_accessed = datetime.now().isoformat()
        # 重复提及提高重要性
        pref.importance = min(pref.importance + 0.5, 10.0)
    
    def _sync_to_memory(self, pref: Preference):
        """同步偏好到记忆系统"""
        content = f"[偏好-{pref.category}] {pref.content}"
        self.memory_system.add_memory(
            content=content,
            cell_type="preference",
            tags=pref.tags + [pref.category],
            importance=pref.importance,
            source=pref.source
        )
    
    def get_preferences_by_category(self, category: str) -> List[Preference]:
        """按分类获取偏好"""
        return [
            pref for pref in self.preferences.values()
            if pref.category == category
        ]
    
    def get_top_preferences(self, limit: int = 10) -> List[Preference]:
        """获取最重要的偏好"""
        sorted_prefs = sorted(
            self.preferences.values(),
            key=lambda p: (p.importance * p.confidence),
            reverse=True
        )
        return sorted_prefs[:limit]
    
    def detect_conflicts(self) -> List[Tuple[Preference, Preference]]:
        """检测冲突偏好"""
        conflicts = []
        prefs_list = list(self.preferences.values())
        
        for i, pref1 in enumerate(prefs_list):
            for pref2 in prefs_list[i+1:]:
                # 检查是否冲突
                if self._is_conflict(pref1, pref2):
                    conflicts.append((pref1, pref2))
        
        return conflicts
    
    def _is_conflict(self, pref1: Preference, pref2: Preference) -> bool:
        """判断两个偏好是否冲突"""
        # 相反表达检测
        opposites = [
            ('喜欢', '不喜欢'),
            ('喜欢', '讨厌'),
            ('偏好', '避免'),
        ]
        
        for opp in opposites:
            if (opp[0] in pref1.content and opp[1] in pref2.content) or \
               (opp[1] in pref1.content and opp[0] in pref2.content):
                # 检查是否针对同一对象
                common_tags = set(pref1.tags) & set(pref2.tags)
                if len(common_tags) >= 1:
                    return True
        
        return False
    
    def export_report(self) -> Dict:
        """导出偏好学习报告"""
        by_category = {}
        for pref in self.preferences.values():
            if pref.category not in by_category:
                by_category[pref.category] = []
            by_category[pref.category].append(pref.to_dict())
        
        conflicts = self.detect_conflicts()
        
        return {
            'total_count': len(self.preferences),
            'by_category': by_category,
            'top_preferences': [p.to_dict() for p in self.get_top_preferences(5)],
            'conflicts': [
                {'pref1': p1.to_dict(), 'pref2': p2.to_dict()}
                for p1, p2 in conflicts
            ],
            'exported_at': datetime.now().isoformat(),
        }


# ============================================================================
# 测试代码
# ============================================================================

if __name__ == "__main__":
    print("🧠 测试用户偏好学习模块...\n")
    
    # 创建记忆系统
    config = MemorySystemConfig()
    memory_system = HongNaoMemorySystem(config)
    
    # 创建偏好学习器
    learner = UserPreferenceLearner(memory_system)
    
    # 测试对话文本
    test_conversations = [
        "我喜欢简洁直接的沟通风格，不喜欢太多废话。",
        "我通常早上 8 点查看新闻和邮件。",
        "我偏好使用 Python 进行开发，不太喜欢 Java。",
        "我喜欢详细的报告，但回复消息要简洁。",
        "我习惯在晚上 10 点前休息。",
        "我非常讨厌冗长的会议。",
    ]
    
    print("📝 从对话中学习偏好:\n")
    for conv in test_conversations:
        print(f"输入：{conv}")
        learned = learner.learn_from_conversation(conv, source="test")
        if learned:
            for pref in learned:
                print(f"  → 学到：[{pref.category}] {pref.content} (置信度：{pref.confidence:.2f})")
        print()
    
    # 导出报告
    print("📊 偏好学习报告:")
    report = learner.export_report()
    print(f"  总偏好数：{report['total_count']}")
    print(f"  分类统计:")
    for category, prefs in report['by_category'].items():
        print(f"    - {category}: {len(prefs)} 条")
    print(f"  冲突检测：{len(report['conflicts'])} 对")
    
    print("\n✅ 用户偏好学习模块测试完成")
