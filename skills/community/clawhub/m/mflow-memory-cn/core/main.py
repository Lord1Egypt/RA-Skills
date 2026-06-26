"""
mflow-memory-cn 中式智慧记忆引擎
主入口 — 整合所有模块，对外提供统一接口
"""

from datetime import datetime
from typing import Optional, Dict, List

from .memory_store import MemoryStore
from .promise_tracker import PromiseTracker
from .relationship_manager import RelationshipManager
from .timing_sensor import TimingSensor, TimeSlot, EmotionalState
from .wisdom_engine import WisdomEngine

class ChineseMemoryEngine:
    """
    中式智慧记忆引擎主类
    
    整合五大模块：
    - MemoryStore: 记忆存储（仁）
    - PromiseTracker: 承诺追踪（义）
    - RelationshipManager: 关系管理（五伦）
    - TimingSensor: 时机感知（礼）
    - WisdomEngine: 智慧推理（智）
    """
    
    def __init__(self, data_dir: Optional[str] = None):
        """初始化所有子模块"""
        self.memory = MemoryStore(data_dir)
        self.promise = PromiseTracker()
        self.relationship = RelationshipManager()
        self.timing = TimingSensor()
        self.wisdom = WisdomEngine()
        
        # 默认用户
        self.current_user = "JOJO"
    
    # ========== 记忆操作 ==========
    
    def remember(self, content: str,
                emotion: Optional[str] = None,
                value: Optional[str] = None,
                concern: Optional[str] = None,
                user_id: Optional[str] = None) -> str:
        """
        存储记忆（仁-Ren）
        
        自动：
        1. 识别情感
        2. 检测承诺
        3. 判断是否值得记住
        """
        uid = user_id or self.current_user
        
        # 时机感知：判断是否该存储
        should_store = True  # 默认存储，除非是纯闲聊
        
        # 记录互动
        self.relationship.record_interaction(uid, "normal")
        
        # 存储记忆
        memory_id = self.memory.save(
            content=content,
            user_id=uid,
            emotion=emotion,
            value=value,
            concern=concern
        )
        
        return memory_id
    
    def recall(self, query: str,
              user_id: Optional[str] = None) -> List[Dict]:
        """
        检索记忆（智-Zhi）
        
        升级版检索：
        1. 意图理解
        2. 关联推理
        3. 时机适配
        """
        uid = user_id or self.current_user
        
        # 基础搜索
        results = self.memory.search(query, uid)
        
        # 关联推理：举一反三
        inferred_prefs = self.wisdom.infer_preference(uid, query)
        
        return {
            "results": results,
            "inferred_preferences": inferred_prefs,
            "context": self.get_context(uid)
        }
    
    def get_context(self, user_id: Optional[str] = None) -> Dict:
        """获取用户上下文（用于注入对话）"""
        uid = user_id or self.current_user
        
        return self.memory.get_context(uid)
    
    # ========== 承诺操作 ==========
    
    def register_promise(self, content: str,
                       deadline: Optional[str] = None,
                       user_id: Optional[str] = None) -> str:
        """注册承诺（义-Yi）"""
        uid = user_id or self.current_user
        
        return self.promise.register(content, deadline, uid)
    
    def check_promises(self) -> Dict:
        """
        检查承诺状态
        
        返回：
        - pending: 待履行
        - overdue: 逾期
        - near_deadline: 临近截止
        """
        return {
            "pending": self.promise.get_pending(),
            "overdue": self.promise.get_overdue(),
            "near_deadline": self.promise.get_near_deadline(24),
            "stats": self.promise.get_stats(),
            "trust_score": self.promise.get_trust_score()
        }
    
    def fulfill_promise(self, promise_id: str):
        """标记承诺已履行"""
        self.promise.fulfill(promise_id)
        
        # 信任验证+1
        self.relationship.record_interaction(self.current_user, "trust")
    
    def get_reminders(self) -> List[str]:
        """获取待发送的提醒"""
        return self.promise.get_reminders()
    
    # ========== 关系操作 ==========
    
    def get_user_tier(self, user_id: Optional[str] = None) -> str:
        """获取用户关系层级"""
        uid = user_id or self.current_user
        tier = self.relationship.get_tier(uid)
        return self.relationship.TIERS[tier]["name"]
    
    def get_response_guide(self, user_id: Optional[str] = None) -> Dict:
        """
        获取回复指南
        
        基于关系层级和时机，返回合适的回复策略
        """
        uid = user_id or self.current_user
        
        # 获取关系风格
        rel_style = self.relationship.get_response_style(uid)
        
        # 获取时机风格
        time_style = self.timing.get_response_style()
        
        # 综合判断
        return {
            "tier": self.get_user_tier(uid),
            "intimacy": self.relationship.get_intimacy(uid),
            "should_be_proactive": rel_style["proactive"],
            "depth": rel_style["depth"],
            "can_advise": rel_style["advice"],
            "emotional_support": rel_style.get("emotional_support", False),
            "current_time_slot": self.timing.get_time_slot().value,
            "recommended_style": time_style["style"]
        }
    
    # ========== 时机操作 ==========
    
    def should_i_act(self, action_type: str,
                    is_user_initiated: bool = False) -> tuple[bool, str]:
        """
        判断是否该行动
        
        Args:
            action_type: 动作类型
            is_user_initiated: 是否用户主动
        """
        return self.timing.should_act(action_type, is_user_initiated)
    
    def get_timing_analysis(self) -> Dict:
        """获取完整时机分析"""
        return self.timing.analyze_context()
    
    # ========== 智慧操作 ==========
    
    def learn_from_feedback(self,
                          was_accepted: bool,
                          context: str,
                          action: str,
                          outcome: str):
        """
        从反馈中学习
        
        当用户接受或拒绝一个建议时调用
        """
        uid = self.current_user
        
        if was_accepted:
            self.wisdom.record_experience(uid, "success", context, action, outcome)
            self.relationship.record_interaction(uid, "trust")
        else:
            self.wisdom.record_experience(uid, "failure", context, action, outcome)
            self.wisdom.learn_rejection_pattern(uid, action, context)
    
    def predict_user_response(self, proposed_action: str) -> tuple[bool, str]:
        """
        预测用户反应
        
        基于历史拒绝模式
        """
        return self.wisdom.predict_rejection(self.current_user, proposed_action)
    
    def get_wisdom_report(self, user_id: Optional[str] = None) -> Dict:
        """获取智慧报告"""
        uid = user_id or self.current_user
        return self.wisdom.get_wisdom_summary(uid)
    
    # ========== 综合分析 ==========
    
    def analyze_before_response(self, user_message: str) -> Dict:
        """
        响应前综合分析
        
        在回复用户之前调用，返回完整的分析结果
        """
        # 1. 获取时机
        timing = self.timing.analyze_context()
        
        # 2. 获取用户关系
        rel_guide = self.get_response_guide()
        
        # 3. 检查承诺
        promise_status = self.check_promises()
        
        # 4. 尝试检索相关记忆
        recall = self.recall(user_message)
        
        # 5. 预测用户反应
        predicted_rejection = self.predict_user_response(user_message)
        
        return {
            "timing": timing,
            "relationship": rel_guide,
            "promises": promise_status,
            "relevant_memories": recall["results"][:3],
            "inferred_preferences": recall["inferred_preferences"],
            "rejection_risk": predicted_rejection,
            "recommendation": self._generate_response_recommendation(
                timing, rel_guide, promise_status, predicted_rejection
            )
        }
    
    def _generate_response_recommendation(self, timing, rel_guide, promises, rejection) -> str:
        """生成回复建议"""
        parts = []
        
        # 时机建议
        parts.append(f"[时机] {timing['recommendation']}")
        
        # 承诺提醒
        if promises["overdue"]:
            parts.append(f"[承诺] 有{len(promises['overdue'])}个逾期承诺需处理")
        elif promises["near_deadline"]:
            parts.append(f"[承诺] 有{len(promises['near_deadline'])}个承诺临近截止")
        
        # 拒绝风险
        if rejection[0]:
            parts.append(f"[注意] {rejection[1]}")
        
        return " | ".join(parts)
    
    # ========== 工具函数 ==========
    
    def get_full_report(self) -> Dict:
        """获取完整报告（用于定期总结）"""
        return {
            "engine": "mflow-memory-cn v1.0",
            "timestamp": datetime.now().isoformat(),
            "current_user": self.current_user,
            "relationship": {
                "tier": self.get_user_tier(),
                "intimacy": self.relationship.get_intimacy(self.current_user),
                "total_interactions": self.relationship._load_relationship(self.current_user).get("interaction_count", 0) if self.relationship._load_relationship(self.current_user) else 0
            },
            "promises": self.check_promises(),
            "wisdom": self.get_wisdom_report(),
            "timing": self.get_timing_analysis()
        }


# 便捷函数
def create_engine(data_dir: Optional[str] = None) -> ChineseMemoryEngine:
    """创建引擎实例"""
    return ChineseMemoryEngine(data_dir)
