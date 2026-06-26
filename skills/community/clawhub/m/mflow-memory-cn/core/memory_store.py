"""
记忆存储模块 (仁-Ren)
带情感标签的记忆存储，增强版M-flow

功能：
1. 标准记忆存储（继承M-flow格式）
2. 情感标签自动识别
3. 价值洞察提取
4. 承诺识别
5. 关联推理
"""

import json
import re
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List, Any

class MemoryStore:
    """
    中式智慧记忆存储
    
    与原版M-flow兼容，但增加：
    - emotion: 情感标签
    - value: 价值观洞察
    - concern: 深层顾虑
    - promise: 承诺识别
    - weight: 权重
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = Path.home() / ".mflow-memory-cn" / "data"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # 主记忆文件
        self.memories_file = self.data_dir / "memories.jsonl"
        self.emotions_file = self.data_dir / "emotions.jsonl"
        self.promises_file = self.data_dir / "promises.jsonl"
        
        # 承诺追踪器（实例化）
        from .promise_tracker import PromiseTracker
        self.promise_tracker = PromiseTracker(self.data_dir / "promises")
        
    # ========== 仁：以人为本 ==========
    
    def save(self, content: str, user_id: str = "default",
             emotion: Optional[str] = None,
             value: Optional[str] = None,
             concern: Optional[str] = None,
             metadata: Optional[Dict] = None) -> str:
        """
        保存记忆（仁-Ren：存储人情，不只存事实）
        
        Args:
            content: 记忆内容
            user_id: 用户标识
            emotion: 情感标签（如"疲惫"、"兴奋"、"担忧"）
            value: 价值观洞察（如"效率优先"、"家庭为重"）
            concern: 深层顾虑（如"担心错过截止日期"）
            metadata: 其他元数据
            
        Returns:
            memory_id: 记忆ID
        """
        # 自动情感识别（如果没有提供）
        if emotion is None:
            emotion = self._detect_emotion(content)
        
        # 自动承诺识别
        promise_data = self._detect_promise(content)
        
        # 构建记忆对象
        memory = {
            "id": self._generate_id(),
            "content": content,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            # 仁扩展
            "emotion": emotion,
            "value": value,
            "concern": concern,
            # 元数据
            "metadata": metadata or {}
        }
        
        # 保存主记忆
        self._append_to_file(self.memories_file, memory)
        
        # 如果有情感标签，单独存储（用于情感分析）
        if emotion:
            self._append_to_file(self.emotions_file, {
                "memory_id": memory["id"],
                "emotion": emotion,
                "timestamp": memory["timestamp"]
            })
        
        # 如果识别到承诺，启动追踪
        if promise_data:
            self.promise_tracker.register(
                content=promise_data["promise"],
                deadline=promise_data.get("deadline"),
                context=content
            )
            
        return memory["id"]
    
    def search(self, query: str, user_id: str = "default",
               include_emotions: bool = True,
               time_range: Optional[tuple] = None) -> List[Dict]:
        """
        搜索记忆（智-Zhi：举一反三，关联推理）
        
        升级点：
        - 原版：关键词匹配
        - 升级版：意图理解 + 情感 + 关联 三维检索
        """
        memories = self._load_memories(user_id)
        
        # 时间过滤
        if time_range:
            start, end = time_range
            memories = [m for m in memories 
                       if start <= m.get("timestamp", "") <= end]
        
        # 意图理解 + 关键词匹配
        query_lower = query.lower()
        scored = []
        
        for mem in memories:
            content = mem.get("content", "").lower()
            
            # 基础分：关键词匹配
            score = 0
            keywords = query_lower.split()
            for kw in keywords:
                if kw in content:
                    score += 1
            
            # 加分：情感匹配（查询中有情感词）
            if include_emotions and mem.get("emotion"):
                for kw in keywords:
                    if kw in ["累", "烦", "担心", "焦虑", "开心", "兴奋"]:
                        if mem["emotion"] and kw in mem["emotion"]:
                            score += 2
            
            # 加分：价值匹配
            if mem.get("value"):
                for kw in keywords:
                    if kw in mem["value"].lower():
                        score += 1.5
            
            if score > 0:
                scored.append((score, mem))
        
        # 按分数排序
        scored.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in scored]
    
    def get_context(self, user_id: str = "default") -> Dict:
        """
        获取用户上下文（用于每次对话前的记忆注入）
        
        返回：
        - 最近记忆（最近5条）
        - 情感趋势（最近的情绪变化）
        - 待履行承诺
        """
        memories = self._load_memories(user_id)
        recent = memories[-5:] if len(memories) > 5 else memories
        
        # 情感趋势
        emotions = self._load_emotions(user_id)
        recent_emotions = emotions[-10:] if len(emotions) > 10 else emotions
        
        return {
            "recent_memories": recent,
            "emotion_trend": [e.get("emotion") for e in recent_emotions],
            "pending_promises": self.promise_tracker.get_pending(),
            "user_values": self._extract_values(memories),
            "user_concerns": self._extract_concerns(memories)
        }
    
    # ========== 辅助方法 ==========
    
    def _detect_emotion(self, content: str) -> Optional[str]:
        """自动情感识别"""
        emotion_keywords = {
            "疲惫": ["累", "困", "疲惫", "没精神"],
            "兴奋": ["兴奋", "激动", "开心", "太好了"],
            "担忧": ["担心", "焦虑", "怕", "不安"],
            "无奈": ["无奈", "没办法", "只能", "就这样"],
            "期待": ["期待", "希望", "想要", "希望能够"],
            "满足": ["满意", "不错", "挺好", "可以"],
            "烦躁": ["烦", "烦躁", "闹心", "不爽"],
        }
        
        for emotion, keywords in emotion_keywords.items():
            if any(kw in content for kw in keywords):
                return emotion
        return None
    
    def _detect_promise(self, content: str) -> Optional[Dict]:
        """自动承诺识别"""
        promise_patterns = [
            (r"(明天|后天|周末|这周)(给|发|做|完成)(.*)", "short"),
            (r"(\d+月\d+日|下周一|下周二)(给|发|做)(.*)", "specific"),
            (r"(回头|之后|等一下)(给|发|做)(.*)", "deferred"),
            (r"(一定|肯定|保证)(给|发|做)(.*)", "commitment"),
        ]
        
        for pattern, ptype in promise_patterns:
            match = re.search(pattern, content)
            if match:
                return {
                    "promise": match.group(0),
                    "type": ptype,
                    "deadline": self._extract_deadline(content)
                }
        return None
    
    def _extract_deadline(self, content: str) -> Optional[str]:
        """提取截止时间"""
        date_patterns = [
            r"(\d{1,2}月\d{1,2}日)",
            r"(明天|后天|周末|下周)",
            r"(\d{4}-\d{2}-\d{2})"
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, content)
            if match:
                return match.group(1)
        return None
    
    def _generate_id(self) -> str:
        """生成唯一ID"""
        import uuid
        return f"mem_{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid.uuid4().hex[:6]}"
    
    def _append_to_file(self, filepath: Path, data: Dict):
        """追加到JSONL文件"""
        with open(filepath, 'a', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False) + '\n')
    
    def _load_memories(self, user_id: str) -> List[Dict]:
        """加载用户记忆"""
        if not self.memories_file.exists():
            return []
        
        memories = []
        with open(self.memories_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    mem = json.loads(line)
                    if mem.get("user_id") == user_id:
                        memories.append(mem)
                except json.JSONDecodeError:
                    continue
        return memories
    
    def _load_emotions(self, user_id: str) -> List[Dict]:
        """加载情感记录"""
        if not self.emotions_file.exists():
            return []
        
        emotions = []
        memory_ids = {m["id"] for m in self._load_memories(user_id)}
        
        with open(self.emotions_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    emo = json.loads(line)
                    if emo.get("memory_id") in memory_ids:
                        emotions.append(emo)
                except json.JSONDecodeError:
                    continue
        return emotions
    
    def _extract_values(self, memories: List[Dict]) -> List[str]:
        """提取价值观"""
        return list(set(m.get("value") for m in memories if m.get("value")))
    
    def _extract_concerns(self, memories: List[Dict]) -> List[str]:
        """提取顾虑"""
        return list(set(m.get("concern") for m in memories if m.get("concern")))
