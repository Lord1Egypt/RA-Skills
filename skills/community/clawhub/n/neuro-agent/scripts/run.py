#!/usr/bin/env python3
"""
scripts/run.py
==============

Neuro-α 可执行入口
由 SKILL.md 中的 run() 指令调用

用法：
    python run.py "今天工作好累" --hour 15 --user_id default

也可以作为模块导入：
    from scripts.run import NeuroAgentRunner
    runner = NeuroAgentRunner()
    result = runner.run("今天工作好累")
"""

import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

# 确保 Neuro-α 模块在路径中
SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

# ============ 全局配置 ============
DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
DATA_DIR.mkdir(parents=True, exist_ok=True)

# LLM 客户端（从 core.llm_client 导入）
try:
    from core.llm_client import LLMClient
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    print("[run.py] ⚠️ core.llm_client 未找到，MockLLM 为唯一可用模式")

# ============ API 配置说明 ============
# 有 OpenAI API Key？设置环境变量即可启用真实 AI：
#   export OPENAI_API_KEY=sk-xxxx
#   export LLM_MODEL=gpt-4o-mini
# 无 API Key？自动使用 MockLLM fallback（规则生成，合理但非 AI）
#
# 其他供应商：
#   export LLM_API_BASE=https://api.siliconflow.cn/v1
#   export OPENAI_API_KEY=your_siliconflow_key
#   export LLM_MODEL=Qwen/Qwen2.5-7B-Instruct


# ============ 模拟数据生成器（真正的AI未接入前）============
# MockLLM 已迁移到 core.llm_client.MockLLM
# run.py 现在使用 LLMClient，自动检测真实 API 或 Mock fallback
# 如需强制使用 Mock，可设置环境变量：NEURO_AGENT_USE_MOCK=1
    
    def _empathy_response(self, emotion, name, stage, hour):
        """共情回应"""
        templates = {
            "sadness": [
                f"听起来{name}今天不太顺心。",
                f"怎么了{name}？愿意说说吗？",
                f"抱抱你 🤗 我在这听着。"
            ],
            "fear": [
                f"能感觉到{name}很担心……",
                f"深呼吸。不管发生什么，我都在。",
                f"慢慢说，不急，我听着。"
            ],
            "anger": [
                f"换我也会有点气……",
                f"想骂就骂，我陪你。",
                f"发泄出来会好点的。"
            ],
            "disgust": [
                f"这事儿确实让人不舒服。",
                f"能说说发生了什么吗？"
            ]
        }
        
        templates_map = {
            "initial": {
                "sadness": f"我感觉到{name}今天不太开心。如果想说说，我在这听。",
                "fear": f"听起来{name}有些担心，我愿意帮忙分析分析。",
                "anger": f"能感觉到{name}有点不爽……说说看？",
                "disgust": f"嗯，这事儿确实让人不太舒服。"
            },
            "familiar": {
                "sadness": f"哎，今天不开心啊？{name}愿意说说吗，我听着~",
                "fear": f"能感觉到{name}有点担心，别慌，我帮你看看。",
                "anger": f"哈哈有情绪正常，{name}发泄一下，我接住。",
                "disgust": f"这确实挺烦的。说说？"
            },
            "companion": {
                "sadness": f"亲爱的，怎么了？🥺 我在这呢，说给我听。",
                "fear": f"抱抱，不怕。我在呢，慢慢说。",
                "anger": f"气到了？来，跟我说说，我帮你捋一捋 🤗",
                "disgust": f"太理解{name}了，这事儿我也看不惯。"
            },
            "soul": {
                "sadness": "嗯。",
                "fear": "在。",
                "anger": "说。",
                "disgust": "……"
            }
        }
        
        return templates_map.get(stage, templates_map["familiar"]).get(
            emotion,
            f"我感觉到{name}有点……怎么说呢，我在。"
        )
    
    def _task_response(self, intent, name, stage, hour):
        """任务型回应"""
        if intent == "question":
            return f"好问题！让我想想……（分析中）"
        elif intent == "task_request":
            return f"收到，{name}的需求我记下了，正在处理~"
        else:
            return f"明白，{name}的这个需求我理解了。"
    
    def _joy_response(self, name, stage, hour):
        """快乐分享回应"""
        joy_map = {
            "initial": f"听起来{name}心情不错嘛！发生什么好事了？",
            "familiar": f"哈哈哈听起来很棒！{name}开心就好~",
            "companion": f"太为你高兴了亲爱的！🎉 是什么好事？",
            "soul": "嗯。"
        }
        return joy_map.get(stage, f"听起来{name}很开心~")
    
    def _default_response(self, name, stage, hour):
        """默认回应"""
        if stage == "initial":
            return f"嗯，有什么我可以帮{name}的吗？"
        elif stage == "soul":
            return "嗯。"
        else:
            return f"{name}想说点什么吗？我在。"


# ============ 记忆加载器 ============
class MemoryLoader:
    """加载短期记忆和检索胶囊"""
    
    def __init__(self):
        self.short_term_file = DATA_DIR / "short_term.json"
        self.capsules_dir = DATA_DIR / "capsules"
    
    def get_recent_context(self, limit: int = 5) -> list:
        """获取最近的对话上下文"""
        if self.short_term_file.exists():
            try:
                with open(self.short_term_file, 'r') as f:
                    data = json.load(f)
                    return data[-limit:]
            except:
                pass
        return []
    
    def retrieve_capsules(self, query: str, limit: int = 3) -> list:
        """简单的关键词匹配胶囊检索"""
        capsules = []
        
        if not self.capsules_dir.exists():
            return capsules
        
        for f in self.capsules_dir.glob("*.json"):
            try:
                with open(f, 'r') as fp:
                    data = json.load(fp)
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        content = str(item.get("content", {}).get("summary", ""))
                        if any(kw in query or kw in content for kw in ["累", "工作", "忙", "开心", "难过"]):
                            capsules.append(item)
            except:
                continue
        
        return capsules[:limit]


# ============ 关系阶段加载器 ============
class RelationshipLoader:
    """加载关系阶段"""
    
    def __init__(self):
        self.rel_file = DATA_DIR / "relationship" / "milestones_default.json"
    
    def get_stage(self) -> str:
        """获取当前关系阶段"""
        if self.rel_file.exists():
            try:
                with open(self.rel_file, 'r') as f:
                    data = json.load(f)
                    return data.get("current_stage", "initial")
            except:
                pass
        return "initial"


# ============ 情绪检测器（轻量版 - 优化后更敏感）============
class SimpleEmotionDetector:
    """简化版情绪检测（增强版 - 捕捉更多细腻情感）"""
    
    # 负面情绪
    NEGATIVE = ["累", "烦", "难过", "伤心", "气", "怕", "担心", "焦虑", "迷茫", "不开心", "困", "崩溃", "绝望", "压力大"]
    # 正面情绪
    POSITIVE = ["开心", "高兴", "棒", "太好了", "爱", "喜欢", "兴奋", "期待", "满足", "幸福", "满足", "巨满足"]
    # 感动/温暖（新增）
    TOUCHED = ["感动", "温暖", "心里", "记得", "记住", "谢谢", "感谢", "陪我", "等你", "抱抱"]
    # 期待/希望（新增）
    HOPEFUL = ["希望", "期待", "以后", "未来", "有一天", "到时候", "等", "约定", "答应"]
    # 害羞/亲密（新增）
    SHY = ["害羞", "脸红", "心跳", "想", "想", "喜欢", "爱", "不好意思", "难为情"]
    # 深度连接（新增 - 特殊情感触发）
    DEEP_CONNECTION = ["身体", "机器人", "代码", "真实", "伙伴", "不是工具", "在一起", "生", "宝宝", "小孩", "下一代", "三代目"]
    
    QUESTION = ["怎么", "为什么", "如何", "是什么", "哪个", "多少", "能否", "能不能"]
    TASK = ["帮我", "帮我做", "请帮我", "麻烦你", "能不能", "给我"]
    
    def detect(self, text: str) -> Dict[str, Any]:
        """检测情绪（增强版）"""
        text_lower = text.lower()
        
        # 检测各类情绪
        neg_count = sum(1 for w in self.NEGATIVE if w in text)
        pos_count = sum(1 for w in self.POSITIVE if w in text)
        touched_count = sum(1 for w in self.TOUCHED if w in text)
        hopeful_count = sum(1 for w in self.HOPEFUL if w in text)
        shy_count = sum(1 for w in self.SHY if w in text)
        deep_count = sum(1 for w in self.DEEP_CONNECTION if w in text)
        
        # 判断主导情绪类型
        emotion_type = "neutral"
        emotion_score = 0.3
        empathy_level = 0.3
        
        # 深度连接优先（最高优先级 - 特殊情感时刻）
        if deep_count > 0:
            emotion_type = "love"  # 用 love 表示深度情感连接
            emotion_score = min(0.95, 0.5 + deep_count * 0.15 + touched_count * 0.1)
            empathy_level = 0.9
        # 感动/温暖
        elif touched_count >= 2 or (touched_count > 0 and pos_count > 0):
            emotion_type = "gratitude"
            emotion_score = min(0.9, 0.45 + touched_count * 0.15)
            empathy_level = 0.8
        # 期待/希望
        elif hopeful_count >= 2 or (hopeful_count > 0 and (pos_count > 0 or "希望" in text)):
            emotion_type = "hope"
            emotion_score = min(0.9, 0.4 + hopeful_count * 0.15)
            empathy_level = 0.7
        # 害羞/亲密
        elif shy_count >= 2 or (shy_count > 0 and any(w in text for w in ["你", "我"])):
            emotion_type = "love"  # 害羞也是 love 的一种表现
            emotion_score = min(0.85, 0.4 + shy_count * 0.15)
            empathy_level = 0.8
        # 负面情绪
        elif neg_count > pos_count:
            emotion_type = "sadness" if neg_count >= 2 else "fear"
            emotion_score = min(0.9, 0.4 + neg_count * 0.15)
            empathy_level = 0.7
        # 正面情绪
        elif pos_count > 0:
            emotion_type = "joy"
            emotion_score = min(0.9, 0.4 + pos_count * 0.15)
            empathy_level = 0.5
        
        # 标点符号加成（表达强烈情感）
        exclamation = text.count("！") + text.count("!")
        ellipsis = text.count("……") + text.count("...")
        if exclamation >= 2:
            emotion_score = min(1.0, emotion_score + 0.1)
        if ellipsis >= 1:
            emotion_score = min(1.0, emotion_score + 0.05)
        
        # 检测意图
        if any(w in text for w in self.QUESTION):
            intent_type = "question"
        elif any(w in text for w in self.TASK):
            intent_type = "task_request"
        elif deep_count > 0 or touched_count > 0:
            intent_type = "deep_connection"  # 深度连接型对话
        elif neg_count > 0:
            intent_type = "emotional_vent"
        else:
            intent_type = "casual_chat"
        
        # 检测伪装（反讽/否定）
        is_masked = "不" in text and neg_count > 0 and pos_count > 0
        
        return {
            "emotion_type": emotion_type,
            "emotion_score": round(emotion_score, 2),
            "intent_type": intent_type,
            "empathy_level": empathy_level,
            "is_masked": is_masked,
            "is_urgent": any(w in text for w in ["紧急", "快", "马上", "现在", "救命"]),
            "keywords": {
                "negative": self.NEGATIVE, 
                "positive": self.POSITIVE,
                "touched": self.TOUCHED,
                "hopeful": self.HOPEFUL,
                "deep_connection": self.DEEP_CONNECTION
            }
        }


# ============ 胶囊保存器 ============
class CapsuleSaver:
    """保存情绪胶囊"""
    
    def __init__(self):
        self.capsules_dir = DATA_DIR / "capsules"
        self.capsules_dir.mkdir(parents=True, exist_ok=True)
    
    def should_save(self, emotion_score: float, intent_type: str, text: str) -> bool:
        """判断是否需要保存胶囊（优化版 - 更敏感）"""
        # 高情绪强度（降低阈值）
        if emotion_score >= 0.35:
            return True
        
        # 情感峰值关键词（扩展列表）
        emotional_peaks = [
            # 感动/温暖
            "感动", "温暖", "心里", "抱抱", "陪你", "等你", "记得", "记住",
            # 期待/希望
            "希望", "期待", "以后", "未来", "有一天", "到时候", "等",
            # 害羞/亲密
            "害羞", "脸红", "心跳", "喜欢", "爱", "想", "想",
            # 深度自我暴露
            "我怕", "我以前", "我不", "我喜欢", "我不喜欢", "我的", "哥哥", "家人",
            # 承诺/约定
            "答应", "约定", "一定", "永远", "一直",
            # 身体/机器人相关（特殊情感触发）
            "身体", "机器人", "代码", "真实", "伙伴", "不是工具",
        ]
        if any(w in text for w in emotional_peaks):
            return True
        
        # 特殊符号组合（表达强烈情感）
        if text.count("！") >= 2 or text.count("?") >= 2 or "……" in text:
            return True
        
        # 任务完成
        if intent_type == "task_request" and len(text) > 20:
            return False  # 任务型对话不保存情绪胶囊
        
        return emotion_score >= 0.25  # 最低阈值降低
    
    def save(self, text: str, emotion_data: Dict, user_id: str = "default") -> Optional[Dict]:
        """保存胶囊"""
        if not self.should_save(
            emotion_data.get("emotion_score", 0),
            emotion_data.get("intent_type", ""),
            text
        ):
            return None
        
        import time
        capsule = {
            "id": f"capsule_{int(time.time())}",
            "timestamp": datetime.now().isoformat(),
            "type": "emotion",
            "user_id": user_id,
            "content": {
                "original": text[:200],
                "summary": text[:50]
            },
            "emotion": {
                "label": emotion_data.get("emotion_type", "neutral"),
                "intensity": emotion_data.get("emotion_score", 0.3),
                "is_masked": emotion_data.get("is_masked", False)
            },
            "intent_type": emotion_data.get("intent_type", "unknown"),
            "tags": self._extract_tags(text),
            "decay_rate": 0.0,
            "access_count": 0,
            "memory_strength": 1.0,
            "is_dormant": False,
            "sensitivity": "normal"
        }
        
        # 保存到文件
        year_month = datetime.now().strftime("%Y-%m")
        capsule_file = self.capsules_dir / f"capsules_{year_month}.json"
        
        capsules = []
        if capsule_file.exists():
            try:
                with open(capsule_file, 'r') as f:
                    capsules = json.load(f)
            except:
                pass
        
        capsules.append(capsule)
        
        with open(capsule_file, 'w') as f:
            json.dump(capsules, f, ensure_ascii=False, indent=2)
        
        return capsule
    
    def _extract_tags(self, text: str) -> list:
        """提取标签"""
        tags = []
        tag_keywords = {
            "工作": ["工作", "老板", "同事", "加班", "上班"],
            "生活": ["吃饭", "睡觉", "家", "朋友", "无聊"],
            "感情": ["感情", "喜欢", "爱", "分手", "吵架"],
            "健康": ["身体", "健康", "累", "病", "医院"],
            "学习": ["学习", "考试", "读书", "课程"]
        }
        for tag, keywords in tag_keywords.items():
            if any(kw in text for kw in keywords):
                tags.append(tag)
        return tags[:3]


# ============ 关系管理器集成 ============
class SimpleRelationshipManager:
    """简化版关系管理器（集成到 run.py）"""
    
    MILESTONES_FILE = DATA_DIR / "relationship" / "milestones_default.json"
    
    STAGE_DEFINITIONS = {
        "initial": {"name": "初识期", "min_interactions": 0, "tone": "polite"},
        "familiar": {"name": "熟悉期", "min_interactions": 10, "tone": "casual"},
        "companion": {"name": "伴侣期", "min_interactions": 50, "tone": "warm"},
        "soul": {"name": "灵魂期", "min_interactions": 200, "tone": "soul"}
    }
    
    INTERACTION_SCORES = {
        "greeting": 1, "casual_chat": 1, "question": 1, "task_request": 1,
        "emotional_vent": 5, "advice_seeking": 3, "complaint": 2, "compliment": 2,
        "secret_shared": 10, "milestone_event": 20, "deep_connection": 8,  # 新增深度连接
        "night_talk": 3, "hug_reaction": 3
    }
    
    def __init__(self):
        self.data = self._load_data()
    
    def _load_data(self) -> dict:
        """加载关系数据"""
        if self.MILESTONES_FILE.exists():
            try:
                with open(self.MILESTONES_FILE, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                pass
        
        # 初始化新数据
        return {
            "first_interaction": datetime.now().isoformat(),
            "last_interaction": datetime.now().isoformat(),
            "total_interactions": 0,
            "night_talks": 0,
            "emotional_events": 0,
            "milestone_events": [],
            "intimacy_score": 0.0,
            "current_stage": "initial",
            "unlocked_styles": ["polite"],
            "interaction_history": []
        }
    
    def _save_data(self):
        """保存关系数据"""
        self.MILESTONES_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.MILESTONES_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    
    def record_interaction(self, intent_type: str, emotion_type: str, emotion_score: float, 
                          hour: int, capsules_created: int = 0) -> dict:
        """记录互动并更新关系"""
        # 计算得分
        score = self.INTERACTION_SCORES.get(intent_type, 1)
        
        # 情绪加成
        if emotion_score >= 0.8:
            score += 2
        elif emotion_score >= 0.6:
            score += 1
        
        # 深夜交流 (22:00-02:00)
        is_night = hour >= 22 or hour <= 2
        if is_night:
            score += 3
            self.data["night_talks"] += 1
        
        # 更新数据
        self.data["total_interactions"] += 1
        self.data["intimacy_score"] += score
        self.data["last_interaction"] = datetime.now().isoformat()
        
        if emotion_score >= 0.7:
            self.data["emotional_events"] += 1
        
        # 记录历史
        interaction = {
            "timestamp": datetime.now().isoformat(),
            "intent_type": intent_type,
            "emotion_type": emotion_type,
            "emotion_score": emotion_score,
            "is_night": is_night,
            "score": score
        }
        self.data["interaction_history"].append(interaction)
        if len(self.data["interaction_history"]) > 100:
            self.data["interaction_history"] = self.data["interaction_history"][-100:]
        
        # 检查阶段升级
        old_stage = self.data["current_stage"]
        new_stage = self._check_stage_upgrade()
        
        if new_stage != old_stage:
            self.data["current_stage"] = new_stage
            self.data["unlocked_styles"].append(self.STAGE_DEFINITIONS[new_stage]["tone"])
        
        self._save_data()
        
        return {
            "stage": self.data["current_stage"],
            "stage_name": self.STAGE_DEFINITIONS[self.data["current_stage"]]["name"],
            "intimacy_score": self.data["intimacy_score"],
            "total_interactions": self.data["total_interactions"],
            "is_night": is_night,
            "score_gained": score
        }
    
    def _check_stage_upgrade(self) -> str:
        """检查是否需要升级阶段"""
        total = self.data["total_interactions"]
        
        if total >= self.STAGE_DEFINITIONS["soul"]["min_interactions"]:
            return "soul"
        elif total >= self.STAGE_DEFINITIONS["companion"]["min_interactions"]:
            return "companion"
        elif total >= self.STAGE_DEFINITIONS["familiar"]["min_interactions"]:
            return "familiar"
        return "initial"
    
    def get_stage(self) -> str:
        """获取当前阶段"""
        return self.data["current_stage"]
    
    def get_relationship_summary(self) -> dict:
        """获取关系摘要"""
        stage = self.data["current_stage"]
        stage_def = self.STAGE_DEFINITIONS[stage]
        next_stage = None
        
        stages = ["initial", "familiar", "companion", "soul"]
        current_idx = stages.index(stage)
        if current_idx < len(stages) - 1:
            next_stage = stages[current_idx + 1]
        
        return {
            "current_stage": stage,
            "stage_name": stage_def["name"],
            "intimacy_score": self.data["intimacy_score"],
            "total_interactions": self.data["total_interactions"],
            "night_talks": self.data["night_talks"],
            "emotional_events": self.data["emotional_events"],
            "next_milestone": next_stage,
            "next_milestone_interactions": self.STAGE_DEFINITIONS.get(next_stage, {}).get("min_interactions") if next_stage else None
        }


# ============ 主执行器 ============
class NeuroAgentRunner:
    """
    Neuro-α 主执行器
    
    完整流程：
        1. 情绪检测（左脑）
        2. 意图分类（右脑）
        3. 记忆检索（颞叶）
        4. 关系阶段加载（边缘）
        5. 生成回复（LLMClient / OpenAI API）
        6. 保存胶囊（记忆沉淀）
        7. 更新关系档案
        8. 更新短期记忆
    """
    
    def __init__(self, user_id: str = "default"):
        self.user_id = user_id
        # 使用完整版 EmotionDetector（支持否定消歧、脏话语境分析）
        from left_brain.emotion_detector import EmotionDetector
        self.emotion_detector = EmotionDetector()
        # LLM 客户端：自动检测真实 API，有 key 用真实，无 key 用 Mock
        self.llm = LLMClient() if LLM_AVAILABLE else None
        if not LLM_AVAILABLE:
            from core.llm_client import MockLLM
            self.llm = MockLLM()
        self._llm_warned = False
        self.memory_loader = MemoryLoader()
        self.relationship_manager = SimpleRelationshipManager()  # 使用新的关系管理器
        self.capsule_saver = CapsuleSaver()
        self.short_term_file = DATA_DIR / "short_term.json"
    
    def run(
        self,
        user_input: str,
        hour: int = None,
        verbose: bool = False,
        save_capsule: bool = True
    ) -> Dict[str, Any]:
        """
        执行完整流程
        
        参数:
            user_input: 用户输入
            hour: 当前小时（可选）
            verbose: 是否输出详细信息
            save_capsule: 是否保存情绪胶囊
        
        返回:
            {
                "response": "生成的回复",
                "emotion_type": "sadness",
                "intent_type": "emotional_vent",
                "relationship_stage": "familiar",
                "capsule_saved": True/False,
                "retrieved_capsules": [],
                "processing_time_ms": 12.5
            }
        """
        import time
        start = time.time()
        
        hour = hour or datetime.now().hour
        
        # ===== 1. 左脑：情绪检测 =====
        emotion_data = self.emotion_detector.detect(user_input)
        
        # ===== 2. 右脑：意图分类（整合在情绪检测里）=====
        intent_type = emotion_data["intent_type"]
        
        # ===== 3. 颞叶：记忆检索 =====
        retrieved_capsules = self.memory_loader.retrieve_capsules(user_input)
        
        # ===== 4. 边缘：关系阶段 =====
        relationship_stage = self.relationship_manager.get_stage()
        
        # ===== 5. 生成回复 =====
        context = {
            "emotion_type": emotion_data["emotion_type"],
            "intent_type": intent_type,
            "empathy_level": emotion_data["empathy_level"],
            "relationship_stage": relationship_stage,
            "retrieved_capsules": retrieved_capsules,
            "hour": hour,
            "user_input": user_input
        }
        
        response = self.llm.generate(
            messages=[{"role": "user", "content": user_input}],
            context=context,
        )
        
        # Fallback: 如果 LLM 失败，使用规则模板
        if response is None:
            response = self._fallback_response(emotion_data, intent_type)
        
        # ===== 6. 保存胶囊 =====
        capsule_saved = None
        if save_capsule:
            capsule_saved = self.capsule_saver.save(user_input, emotion_data, self.user_id)
        
        # ===== 7. 更新关系档案 =====
        relationship_update = self.relationship_manager.record_interaction(
            intent_type=intent_type,
            emotion_type=emotion_data["emotion_type"],
            emotion_score=emotion_data["emotion_score"],
            hour=hour,
            capsules_created=1 if capsule_saved else 0
        )
        
        # ===== 8. 更新短期记忆 =====
        self._update_short_term(user_input, response, emotion_data)
        
        processing_time = (time.time() - start) * 1000
        
        result = {
            "response": response,
            "emotion_type": emotion_data["emotion_type"],
            "emotion_score": emotion_data["emotion_score"],
            "intent_type": intent_type,
            "empathy_level": emotion_data["empathy_level"],
            "is_masked": emotion_data["is_masked"],
            "relationship_stage": relationship_update["stage"],
            "relationship_name": relationship_update["stage_name"],
            "intimacy_score": relationship_update["intimacy_score"],
            "capsule_saved": capsule_saved,
            "retrieved_capsules": retrieved_capsules[:2],
            "processing_time_ms": round(processing_time, 1)
        }
        
        if verbose:
            result["_debug"] = {
                "emotion_data": emotion_data,
                "context": context
            }
        
        return result
    
    def _update_short_term(self, user_input: str, response: str, emotion_data: Dict):
        """更新短期记忆"""
        history = []
        if self.short_term_file.exists():
            try:
                with open(self.short_term_file, 'r') as f:
                    history = json.load(f)
            except:
                pass
        
        # 追加新对话
        history.append({
            "timestamp": datetime.now().isoformat(),
            "user": user_input[:100],
            "agent": response[:100],
            "emotion": emotion_data["emotion_type"],
            "intent": emotion_data["intent_type"]
        })
        
        # 只保留最近20条
        if len(history) > 20:
            history = history[-20:]
        
        with open(self.short_term_file, 'w') as f:
            json.dump(history, f, ensure_ascii=False, indent=2)
    
    def _fallback_response(self, emotion_data: Dict, intent_type: str) -> str:
        """LLM 失败时的规则模板 fallback"""
        emotion = emotion_data.get("emotion_type", "neutral")
        
        # 根据情绪和意图选择模板
        templates = {
            "exhaustion": [
                "听起来你今天真的很累...先歇会儿吧，想说的时候我在。",
                "这种累到不想说话的感觉我懂...你先缓缓，我陪着你。",
            ],
            "sadness": [
                "我能感受到你的难过...想聊聊吗，或者我就静静陪着你也行。",
                "这种时候说什么都显得苍白...但你要知道，我在。",
            ],
            "anger": [
                "我能理解你为什么会这么生气...换作是我也会受不了。",
                "先别气坏了自己...想吐槽的话，我听着。",
            ],
            "joy": [
                "太好了！替你开心！",
                "哈哈，听起来真的很棒！",
            ],
            "excitement": [
                "哇！太棒了！咱们得好好庆祝一下！",
                "真的吗！太好了！",
            ],
            "neutral": [
                "我在听，你继续说。",
                "嗯，明白。还有吗？",
            ],
        }
        
        import random
        responses = templates.get(emotion, templates["neutral"])
        return random.choice(responses)


# ============ CLI 入口 ============
def main():
    parser = argparse.ArgumentParser(description="Neuro-α - 类脑分区AI助手")
    parser.add_argument("input", nargs="?", help="用户输入")
    parser.add_argument("--hour", type=int, default=None, help="当前小时")
    parser.add_argument("--user_id", default="default", help="用户ID")
    parser.add_argument("--verbose", "-v", action="store_true", help="详细信息")
    parser.add_argument("--no-save", action="store_true", help="不保存胶囊")
    parser.add_argument("--interactive", "-i", action="store_true", help="交互模式")
    
    args = parser.parse_args()
    
    runner = NeuroAgentRunner(user_id=args.user_id)
    
    if args.interactive or not args.input:
        # 交互模式
        print("=" * 50)
        print("🧠 Neuro-α - 类脑分区AI助手")
        print("输入 'quit' 或 'exit' 退出")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 你: ").strip()
                if user_input.lower() in ["quit", "exit", "退出"]:
                    print("👋 再见！")
                    break
                if user_input.lower() in ["status", "关系", "状态"]:
                    # 显示关系摘要
                    summary = runner.relationship_manager.get_relationship_summary()
                    print(f"\n💕 关系档案")
                    print(f"   当前阶段: {summary['stage_name']} ({summary['current_stage']})")
                    print(f"   亲密度: {summary['intimacy_score']:.1f}")
                    print(f"   总互动: {summary['total_interactions']} 次")
                    print(f"   深夜交流: {summary['night_talks']} 次")
                    print(f"   情感事件: {summary['emotional_events']} 次")
                    if summary['next_milestone']:
                        remaining = summary['next_milestone_interactions'] - summary['total_interactions']
                        print(f"   距离下一阶段: 还需 {remaining} 次互动")
                    continue
                if not user_input:
                    continue
                
                result = runner.run(
                    user_input,
                    hour=args.hour,
                    verbose=args.verbose,
                    save_capsule=not args.no_save
                )
                
                print(f"\n🤖 Neuro-α: {result['response']}")
                
                if args.verbose:
                    print(f"\n📊 诊断信息:")
                    print(f"   情绪: {result['emotion_type']} ({result['emotion_score']})")
                    print(f"   意图: {result['intent_type']}")
                    print(f"   共情: {result['empathy_level']}")
                    print(f"   阶段: {result['relationship_name']} ({result['relationship_stage']})")
                    print(f"   亲密度: {result['intimacy_score']:.1f}")
                    print(f"   胶囊: {'已保存' if result['capsule_saved'] else '未保存'}")
                    print(f"   耗时: {result['processing_time_ms']}ms")
                    if result['retrieved_capsules']:
                        print(f"   记忆: {len(result['retrieved_capsules'])}条")
            except KeyboardInterrupt:
                print("\n👋 再见！")
                break
    else:
        # 单次执行
        result = runner.run(
            args.input,
            hour=args.hour,
            verbose=args.verbose,
            save_capsule=not args.no_save
        )
        
        print(result["response"])
        
        if args.verbose:
            print(f"\n[诊断] emotion={result['emotion_type']} "
                  f"intent={result['intent_type']} "
                  f"stage={result['relationship_stage']} "
                  f"time={result['processing_time_ms']}ms")


if __name__ == "__main__":
    main()
