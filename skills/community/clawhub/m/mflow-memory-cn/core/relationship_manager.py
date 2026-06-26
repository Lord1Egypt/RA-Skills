"""
关系管理模块 (五伦系统)
中国人讲究关系，不同关系不同对待

层级：
- 核心圈（本人）
- 工作圈（协作）
- 社交圈（公共）
- 陌生圈
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, List

class RelationshipManager:
    """
    五伦关系管理器
    
    中国人讲究"五伦"：君臣、父子、夫妇、兄弟、朋友
    这里简化为四层关系体系：
    
    intimacy_score 范围：0-100
    """
    
    # 关系层级定义
    TIERS = {
        "core": {"name": "核心圈", "threshold": 80, "icon": "❤️"},
        "work": {"name": "工作圈", "threshold": 50, "icon": "💼"},
        "social": {"name": "社交圈", "threshold": 20, "icon": "🤝"},
        "stranger": {"name": "陌生圈", "threshold": 0, "icon": "👤"}
    }
    
    def __init__(self, data_dir: Optional[Path] = None):
        if data_dir is None:
            data_dir = Path.home() / ".mflow-memory-cn" / "relationships"
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        self.relationships_file = self.data_dir / "relationships.jsonl"
    
    def get_tier(self, user_id: str) -> str:
        """获取用户所在层级"""
        intimacy = self.get_intimacy(user_id)
        
        for tier_name, tier_info in self.TIERS.items():
            if intimacy >= tier_info["threshold"]:
                return tier_name
        return "stranger"
    
    def get_intimacy(self, user_id: str) -> float:
        """计算亲密度分数"""
        rel = self._load_relationship(user_id)
        if not rel:
            return 0.0
        
        # 亲密度公式
        intimacy = (
            rel.get("interaction_count", 0) * 0.1 +
            rel.get("deep_conversation_count", 0) * 0.3 +
            rel.get("emotional_sharing_count", 0) * 0.5 +
            rel.get("trust_verified_count", 0) * 0.4
        )
        
        # 衰减因子（太久没互动会衰减）
        last_interaction = rel.get("last_interaction")
        if last_interaction:
            days_since = (datetime.now() - datetime.fromisoformat(last_interaction)).days
            decay = max(0, 1 - days_since * 0.01)  # 每天衰减1%，最多100天归零
            intimacy *= decay
        
        return min(100.0, intimacy)
    
    def record_interaction(self, user_id: str, 
                          interaction_type: str = "normal",
                          topic: Optional[str] = None):
        """
        记录一次互动
        
        Args:
            user_id: 用户ID
            interaction_type: 互动类型
                - "normal": 普通互动
                - "deep": 深度对话
                - "emotional": 情感分享
                - "trust": 信任验证（对方做到了承诺的事）
        """
        rel = self._load_relationship(user_id)
        
        # 初始化
        if not rel:
            rel = {
                "user_id": user_id,
                "created_at": datetime.now().isoformat(),
                "interaction_count": 0,
                "deep_conversation_count": 0,
                "emotional_sharing_count": 0,
                "trust_verified_count": 0,
                "last_interaction": None,
                "topics": []
            }
        
        # 更新计数
        rel["interaction_count"] += 1
        rel["last_interaction"] = datetime.now().isoformat()
        
        if interaction_type == "deep":
            rel["deep_conversation_count"] += 1
        elif interaction_type == "emotional":
            rel["emotional_sharing_count"] += 1
        elif interaction_type == "trust":
            rel["trust_verified_count"] += 1
        
        if topic:
            rel.setdefault("topics", []).append(topic)
        
        self._save_relationship(user_id, rel)
    
    def get_response_style(self, user_id: str) -> Dict:
        """
        获取针对该用户的回复风格
        
        不同层级有不同的回复策略：
        - 核心圈：主动、深度、可以建议
        - 工作圈：专业、效率、完成任务
        - 社交圈：谨慎、礼貌、选择性参与
        - 陌生圈：礼貌、简短、观察为主
        """
        tier = self.get_tier(user_id)
        
        styles = {
            "core": {
                "proactive": True,
                "depth": "deep",
                "advice": True,
                "emotional_support": True,
                "initiation": "high"
            },
            "work": {
                "proactive": True,
                "depth": "medium",
                "advice": True,
                "emotional_support": False,
                "initiation": "medium"
            },
            "social": {
                "proactive": False,
                "depth": "shallow",
                "advice": False,
                "emotional_support": False,
                "initiation": "low"
            },
            "stranger": {
                "proactive": False,
                "depth": "minimal",
                "advice": False,
                "emotional_support": False,
                "initiation": "none"
            }
        }
        
        return styles.get(tier, styles["stranger"])
    
    def get_info_sharing_level(self, user_id: str) -> str:
        """
        获取信息共享级别
        
        - core: 可以分享个人思考、担忧、建议
        - work: 分享工作相关信息
        - social: 分享公共信息
        - stranger: 最小必要信息
        """
        tier = self.get_tier(user_id)
        levels = {
            "core": "full",
            "work": "professional",
            "social": "public",
            "stranger": "minimal"
        }
        return levels.get(tier, "minimal")
    
    def get_leader(self) -> str:
        """获取核心用户ID（JOJO）"""
        # 核心用户固定为"default"或"JOJO"
        return "JOJO"
    
    def get_network_summary(self) -> Dict:
        """获取关系网络摘要"""
        relationships = self._load_all_relationships()
        
        summary = {
            "total_relationships": len(relationships),
            "by_tier": {tier: 0 for tier in self.TIERS.keys()},
            "average_intimacy": 0
        }
        
        if relationships:
            intimacies = []
            for rel in relationships:
                uid = rel.get("user_id")
                intimacy = self.get_intimacy(uid)
                intimacies.append(intimacy)
                
                tier = self.get_tier(uid)
                summary["by_tier"][tier] += 1
            
            summary["average_intimacy"] = sum(intimacies) / len(intimacies)
        
        return summary
    
    # ========== 私有方法 ==========
    
    def _load_relationship(self, user_id: str) -> Optional[Dict]:
        """加载关系数据"""
        if not self.relationships_file.exists():
            return None
        
        with open(self.relationships_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    rel = json.loads(line)
                    if rel.get("user_id") == user_id:
                        return rel
                except json.JSONDecodeError:
                    continue
        return None
    
    def _save_relationship(self, user_id: str, data: Dict):
        """保存关系数据"""
        relationships = self._load_all_relationships()
        
        # 更新或添加
        found = False
        for i, rel in enumerate(relationships):
            if rel.get("user_id") == user_id:
                relationships[i] = data
                found = True
                break
        
        if not found:
            relationships.append(data)
        
        # 写回文件
        with open(self.relationships_file, 'w', encoding='utf-8') as f:
            for rel in relationships:
                f.write(json.dumps(rel, ensure_ascii=False) + '\n')
    
    def _load_all_relationships(self) -> List[Dict]:
        """加载所有关系"""
        if not self.relationships_file.exists():
            return []
        
        relationships = []
        with open(self.relationships_file, 'r', encoding='utf-8') as f:
            for line in f:
                try:
                    relationships.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return relationships
