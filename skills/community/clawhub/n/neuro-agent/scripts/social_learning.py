#!/usr/bin/env python3
"""
scripts/social_learning.py
===========================
Neuro-Agent 社会化学习模块
让 Agent 除了和用户对话，还能主动从互联网上学习真实世界的情景处理案例

核心思路：
- 人类的情商有两个来源：亲身经历 + 观察学习
- 观察学习 = 看别人怎么处理事情，结果如何，然后自己模拟推演
- 这个模块让 Agent 定期主动搜索真实情景案例，沉淀为"社会经验胶囊"

触发方式：Cron 定时触发（每天 1-2 次）
输出：社会经验胶囊 + 情景推演结果
"""

import sys
import json
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Optional, Any
import random

SCRIPT_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(SCRIPT_DIR))

DATA_DIR = Path.home() / ".openclaw" / "workspace" / "neuro_claw"
SOCIAL_LEARNING_DIR = DATA_DIR / "social_learning"
SOCIAL_CAPSULES_FILE = SOCIAL_LEARNING_DIR / "social_capsules.json"
LEARNING_LOG_FILE = SOCIAL_LEARNING_DIR / "learning_log.json"


# ============ 社会经验胶囊结构 ============

class SocialCapsule:
    """
    社会经验胶囊
    
    和普通情绪胶囊的区别：
    - 普通胶囊：来自和用户的互动
    - 社会胶囊：来自网上观察到的真实情景
    
    字段说明：
    - source_url: 来源链接
    - scenario_type: 情景类型（沟通/冲突/安慰/拒绝/道歉/赞美...）
    - situation: 具体情景描述
    - people_behavior: 当事人是怎么处理的
    - outcome: 结果如何（正向/负向/中性）
    - emotion_label: 当事人当时的情绪
    - lessons: 从中学到的教训
    - applicable_scenes: 适用于哪些场景
    - simulation_notes: 如果是我会怎么做
    """

    def __init__(
        self,
        scenario_type: str,
        situation: str,
        people_behavior: str,
        outcome: str,  # positive / negative / neutral
        emotion_label: str,
        lessons: List[str],
        applicable_scenes: List[str],
        source_url: str = "",
        source_title: str = "",
        tags: List[str] = None
    ):
        self.id = f"social_{datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000,9999)}"
        self.timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.scenario_type = scenario_type
        self.situation = situation
        self.people_behavior = people_behavior
        self.outcome = outcome
        self.emotion_label = emotion_label
        self.lessons = lessons
        self.applicable_scenes = applicable_scenes
        self.source_url = source_url
        self.source_title = source_title
        self.tags = tags or []
        self.access_count = 0
        self.last_used = None
        self.simulations: List[Dict] = []

    def to_dict(self) -> Dict:
        return {
            "id": self.id,
            "timestamp": self.timestamp,
            "scenario_type": self.scenario_type,
            "situation": self.situation,
            "people_behavior": self.people_behavior,
            "outcome": self.outcome,
            "emotion_label": self.emotion_label,
            "lessons": self.lessons,
            "applicable_scenes": self.applicable_scenes,
            "source_url": self.source_url,
            "source_title": self.source_title,
            "tags": self.tags,
            "access_count": self.access_count,
            "last_used": self.last_used,
            "simulations": self.simulations
        }

    @classmethod
    def from_dict(cls, data: Dict) -> "SocialCapsule":
        capsule = cls(
            scenario_type=data["scenario_type"],
            situation=data["situation"],
            people_behavior=data["people_behavior"],
            outcome=data["outcome"],
            emotion_label=data["emotion_label"],
            lessons=data["lessons"],
            applicable_scenes=data["applicable_scenes"],
            source_url=data.get("source_url", ""),
            source_title=data.get("source_title", ""),
            tags=data.get("tags", [])
        )
        capsule.id = data.get("id", capsule.id)
        capsule.timestamp = data.get("timestamp", capsule.timestamp)
        capsule.access_count = data.get("access_count", 0)
        capsule.last_used = data.get("last_used")
        capsule.simulations = data.get("simulations", [])
        return capsule


# ============ 学习主题库 ============

SOCIAL_LEARNING_TOPICS = [
    # 沟通类
    {
        "scenario_type": "沟通",
        "query": "人际沟通技巧 真实案例 怎么处理",
        "emotion_label": "真诚",
        "tags": ["沟通", "技巧", "人际关系"]
    },
    {
        "scenario_type": "冲突",
        "query": "同事之间发生冲突 怎么处理 结果如何",
        "emotion_label": "愤怒",
        "tags": ["冲突", "职场", "解决"]
    },
    {
        "scenario_type": "安慰",
        "query": "朋友难过怎么安慰 真实经历分享",
        "emotion_label": "共情",
        "tags": ["安慰", "共情", "支持"]
    },
    {
        "scenario_type": "拒绝",
        "query": "如何得体地拒绝别人 真实案例",
        "emotion_label": "为难",
        "tags": ["拒绝", "边界", "沟通"]
    },
    {
        "scenario_type": "道歉",
        "query": "做错事怎么道歉 真诚道歉的例子",
        "emotion_label": "愧疚",
        "tags": ["道歉", "认错", "修复关系"]
    },
    {
        "scenario_type": "赞美",
        "query": "如何真诚地赞美别人 技巧和例子",
        "emotion_label": "欣赏",
        "tags": ["赞美", "人际", "正面"]
    },
    {
        "scenario_type": "倾听",
        "query": "倾听的重要性 倾听的技巧 真实故事",
        "emotion_label": "专注",
        "tags": ["倾听", "沟通", "关注"]
    },
    {
        "scenario_type": "边界",
        "query": "如何设立健康的个人边界 真实经历",
        "emotion_label": "坚定",
        "tags": ["边界", "自我保护", "成长"]
    },
    {
        "scenario_type": "调解",
        "query": "两个人吵架怎么调解 真实案例",
        "emotion_label": "中立",
        "tags": ["调解", "冲突", "和解"]
    },
    {
        "scenario_type": "陪伴",
        "query": "陪伴的重要性 默默陪伴的故事",
        "emotion_label": "温暖",
        "tags": ["陪伴", "支持", "存在"]
    },
]


# ============ 核心类 ============

class SocialLearner:
    """
    社会化学习器
    
    工作流程：
    1. 选择一个学习主题（从主题库轮询）
    2. 联网搜索相关真实案例
    3. 解析内容，提取情景 + 行为 + 结果
    4. 生成社会经验胶囊
    5. 记录学习日志
    
    使用方式：
        learner = SocialLearner()
        result = learner.learn()  # 执行一次学习
        capsules = learner.get_recent_capsules(count=5)  # 获取最近的胶囊
        suggestions = learner.get_simulation_for_context("用户很生气")  # 根据场景找参考
    """

    def __init__(self):
        self._ensure_data_dir()
        self.learning_log = self._load_learning_log()
        self.capsules = self._load_capsules()
        self.last_topic_index = self.learning_log.get("last_topic_index", -1)

    def _ensure_data_dir(self):
        """确保数据目录存在"""
        SOCIAL_LEARNING_DIR.mkdir(parents=True, exist_ok=True)

    def _load_learning_log(self) -> Dict:
        """加载学习日志"""
        if LEARNING_LOG_FILE.exists():
            try:
                with open(LEARNING_LOG_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                pass
        return {
            "last_topic_index": -1,
            "total_learning_cycles": 0,
            "total_capsules_created": 0,
            "last_learning_date": None,
            "learning_history": []
        }

    def _save_learning_log(self):
        """保存学习日志"""
        with open(LEARNING_LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(self.learning_log, f, ensure_ascii=False, indent=2)

    def _load_capsules(self) -> List[SocialCapsule]:
        """加载已有的社会胶囊"""
        if SOCIAL_CAPSULES_FILE.exists():
            try:
                with open(SOCIAL_CAPSULES_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return [SocialCapsule.from_dict(d) for d in data]
            except Exception:
                pass
        return []

    def _save_capsules(self):
        """保存社会胶囊"""
        with open(SOCIAL_CAPSULES_FILE, "w", encoding="utf-8") as f:
            json.dump([c.to_dict() for c in self.capsules], f, ensure_ascii=False, indent=2)

    def _select_next_topic(self) -> Dict:
        """选择下一个学习主题（轮询）"""
        self.last_topic_index = (self.last_topic_index + 1) % len(SOCIAL_LEARNING_TOPICS)
        return SOCIAL_LEARNING_TOPICS[self.last_topic_index]

    def _search_web(self, query: str) -> List[Dict]:
        """
        联网搜索真实案例
        
        返回格式：
        [{
            "title": "...",
            "url": "...",
            "snippet": "...",
            "source": "搜索来源"
        }]
        
        注意：这个函数依赖外部的 web_search 实现
        如果没有联网能力，返回模拟数据（仅测试用）
        """
        try:
            # 尝试导入 OpenClaw 的 web_search（如果可用）
            from openclaw_core import web_search
            results = web_search(query=query, limit=5)
            return results
        except ImportError:
            pass

        # 尝试用 curl 调用网络搜索
        try:
            import urllib.parse
            encoded_query = urllib.parse.quote(query)
            # 这里可以接入任意的搜索 API
            # 例如：Google Search API, DuckDuckGo API 等
            # 为了保持技能独立性，这里返回空列表
            # 实际使用时可接入 SerpAPI / DuckDuckGo 等
            return []
        except Exception:
            return []

    def _search_with_fallback(self, query: str) -> List[Dict]:
        """
        带 fallback 的搜索
        如果联网失败，返回预设的情景案例库（仅作为兜底）
        """
        results = self._search_web(query)
        if not results:
            # 使用内置的情景案例库作为兜底
            return self._get_fallback_scenarios()
        return results

    def _get_fallback_scenarios(self) -> List[Dict]:
        """
        内置的情景案例库（兜底用）
        这些是典型的人类社交情景案例
        """
        return [
            {
                "title": "朋友向你倾诉烦恼，你这样回应",
                "url": "fallback://built_in",
                "snippet": "不要急着给建议，先说'我理解你的感受'，让对方感受到被倾听。很多时候人们不需要解决方案，只需要被理解。",
                "source": "内置经验库"
            },
            {
                "title": "被当众质疑时，高情商的人这样回应",
                "url": "fallback://built_in",
                "snippet": "保持冷静，不急于反驳，先感谢对方的质疑，然后用'这个角度我没想过，能否详细说说？'来延续对话，既化解了尴尬，又显示了开放心态。",
                "source": "内置经验库"
            },
            {
                "title": "如何得体地拒绝别人的请求",
                "url": "fallback://built_in",
                "snippet": "用'yes-and'的方式：先说'我很想帮你（yes）'，然后说'但是现在情况不允许（and）'，最后给一个替代方案。避免直接说'不'，而是用事实和限制代替拒绝。",
                "source": "内置经验库"
            },
            {
                "title": "两个人吵架冷战，后道歉的人真的输了吗",
                "url": "fallback://built_in",
                "snippet": "先道歉不是认输，而是代表你更在乎这段关系。道歉的正确方式是：描述事实+表达感受+说明原因+提出改进，而不是说'对不起你别生气了'。",
                "source": "内置经验库"
            },
            {
                "title": "怎么夸人才能夸到心坎里",
                "url": "fallback://built_in",
                "snippet": "夸奖要具体不要泛泛：不说'你真棒'，而是说'你刚才处理那个客户投诉的方式真的很专业，我学到了'。具体的赞美让人感受到你是真的注意到了对方的努力。",
                "source": "内置经验库"
            },
        ]

    def _generate_capsule_from_result(self, topic: Dict, search_result: Dict) -> SocialCapsule:
        """
        从搜索结果生成社会经验胶囊
        
        这里用 LLM 来做情景理解和教训提取
        如果没有 LLM，用规则模板做兜底
        """
        snippet = search_result.get("snippet", "")
        title = search_result.get("title", "")

        # 尝试用 LLM 分析（如果有）
        try:
            capsule = self._generate_capsule_with_llm(topic, search_result)
            if capsule:
                return capsule
        except Exception:
            pass

        # Fallback：用规则模板
        return self._generate_capsule_with_template(topic, search_result)

    def _generate_capsule_with_llm(self, topic: Dict, search_result: Dict) -> Optional[SocialCapsule]:
        """用 LLM 生成更精准的胶囊"""
        try:
            from core.llm_client import get_llm_client
            client = get_llm_client()

            prompt = f"""分析以下真实情景案例，提取关键信息：

情景标题：{search_result.get('title', '')}
情景描述：{search_result.get('snippet', '')}

请提取：
1. 具体的情景（situation）：发生了什么
2. 当事人行为（people_behavior）：他们是怎么处理的
3. 结果如何（outcome）：positive / negative / neutral
4. 适用的场景（applicable_scenes）：这种情况通常在什么场景出现
5. 学到的教训（lessons）：从中学到了什么（1-2条）

请用 JSON 格式返回：
{{
  "situation": "...",
  "people_behavior": "...",
  "outcome": "positive/negative/neutral",
  "applicable_scenes": ["场景1", "场景2"],
  "lessons": ["教训1", "教训2"]
}}
"""
            response = client.generate(prompt)
            # 解析 LLM 输出...
            # （实际实现需要根据 client 返回格式来定）
            return None
        except Exception:
            return None

    def _generate_capsule_with_template(self, topic: Dict, search_result: Dict) -> SocialCapsule:
        """用规则模板生成胶囊（兜底）"""
        snippet = search_result.get("snippet", "")
        title = search_result.get("title", "")
        scenario_type = topic.get("scenario_type", "沟通")

        # 根据情景类型预设教训模板
        lesson_templates = {
            "沟通": ["先倾听再表达", "用'我'开头的句式而非'你'"],
            "冲突": ["先冷静再沟通", "对事不对人"],
            "安慰": ["先共情再给建议", "不要轻易说'我懂'"],
            "拒绝": ["用替代方案代替直接拒绝", "态度坚定但语气温和"],
            "道歉": ["描述事实+表达感受+说明原因", "道歉后要用行动证明"],
            "赞美": ["具体地赞美而非泛泛", "赞美努力而非天赋"],
            "倾听": ["不打断对方", "用复述确认理解"],
            "边界": ["明确表达自己的底线", "学会说不"],
            "调解": ["保持中立", "引导双方说出感受"],
            "陪伴": ["有时候默默在场就是最好的支持", "不需要说很多话"],
        }

        lessons = lesson_templates.get(scenario_type, ["具体情况具体分析"])

        # 判断结果：正向还是负向（heuristic）
        outcome = "positive" if any(kw in snippet for kw in ["成功", "好", "有效", "改善", "解决"]) else \
                  "negative" if any(kw in snippet for kw in ["失败", "糟糕", "恶化", "破裂"]) else "neutral"

        return SocialCapsule(
            scenario_type=scenario_type,
            situation=f"标题：{title}。内容：{snippet[:200]}",
            people_behavior="从搜索结果中提取的行为描述",
            outcome=outcome,
            emotion_label=topic.get("emotion_label", "真诚"),
            lessons=lessons,
            applicable_scenes=[
                f"用户表达{scenario_type}相关情绪时",
                f"需要处理{scenario_type}相关情境时"
            ],
            source_url=search_result.get("url", ""),
            source_title=title,
            tags=topic.get("tags", [])
        )

    def learn(self) -> Dict:
        """
        执行一次社会化学习
        
        流程：
        1. 选择主题
        2. 搜索真实案例
        3. 生成胶囊
        4. 记录日志
        
        返回学习结果摘要
        """
        topic = self._select_next_topic()
        query = topic.get("query", "")
        scenario_type = topic.get("scenario_type", "未知")

        search_results = self._search_with_fallback(query)

        capsules_created = []

        if search_results:
            # 取第一个最相关的案例来生成胶囊
            for result in search_results[:1]:
                capsule = self._generate_capsule_from_result(topic, result)
                self.capsules.append(capsule)
                capsules_created.append(capsule.to_dict())
        else:
            # 没有搜索结果时，用内置案例
            for result in self._get_fallback_scenarios()[:1]:
                capsule = self._generate_capsule_from_result(topic, result)
                self.capsules.append(capsule)
                capsules_created.append(capsule.to_dict())

        # 更新日志
        self.learning_log["total_learning_cycles"] += 1
        self.learning_log["last_topic_index"] = self.last_topic_index
        self.learning_log["last_learning_date"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.learning_log["total_capsules_created"] = len(self.capsules)
        self.learning_log["learning_history"].append({
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "topic": scenario_type,
            "query": query,
            "results_found": len(search_results),
            "capsules_created": len(capsules_created)
        })

        # 只保留最近 100 个胶囊
        if len(self.capsules) > 100:
            self.capsules = self.capsules[-100:]

        self._save_learning_log()
        self._save_capsules()

        return {
            "status": "ok",
            "topic": scenario_type,
            "query": query,
            "search_results_count": len(search_results),
            "capsules_created": len(capsules_created),
            "total_capsules": len(self.capsules),
            "sample_capsule": capsules_created[0] if capsules_created else None
        }

    def get_recent_capsules(self, count: int = 5) -> List[Dict]:
        """获取最近的社会胶囊"""
        recent = self.capsules[-count:] if self.capsules else []
        return [c.to_dict() for c in recent]

    def get_capsules_by_scenario(self, scenario_type: str) -> List[Dict]:
        """根据情景类型查找胶囊"""
        filtered = [c for c in self.capsules if c.scenario_type == scenario_type]
        return [c.to_dict() for c in filtered]

    def get_simulation_for_context(self, user_situation: str) -> Dict:
        """
        根据用户当前情景，推荐相关的社会经验
        
        这是"沙盘推演"功能：
        用户遇到了某个情况 → 查找类似情景的案例 → 
        推演"如果是我，会怎么做" → 给前额叶提供参考
        """
        # 用关键词匹配最相关的胶囊
        user_words = set(user_situation.lower())

        best_match = None
        best_score = 0

        for capsule in reversed(self.capsules):
            capsule_words = set(
                " ".join(capsule.lessons + capsule.applicable_scenes + [capsule.scenario_type]).lower()
            )
            score = len(user_words & capsule_words)
            if score > best_score:
                best_score = score
                best_match = capsule

        if best_match:
            best_match.access_count += 1
            best_match.last_used = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            self._save_capsules()

            return {
                "has_match": True,
                "scenario_type": best_match.scenario_type,
                "situation": best_match.situation,
                "people_behavior": best_match.people_behavior,
                "outcome": best_match.outcome,
                "lessons": best_match.lessons,
                "applicable_scenes": best_match.applicable_scenes,
                "simulation_note": f"如果是我面对'{user_situation[:30]}...'这种情况，"
                                    f"可以参考'{best_match.scenario_type}'的处理方式："
                                    f"{best_match.lessons[0] if best_match.lessons else '具体问题具体分析'}"
            }

        return {
            "has_match": False,
            "simulation_note": "目前没有相关的社会经验参考，需要更多学习。"
        }

    def add_simulation(self, capsule_id: str, simulation_note: str):
        """为胶囊添加推演记录"""
        for capsule in self.capsules:
            if capsule.id == capsule_id:
                capsule.simulations.append({
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "note": simulation_note
                })
                self._save_capsules()
                return True
        return False

    def get_learning_stats(self) -> Dict:
        """获取学习统计"""
        if not self.capsules:
            return {
                "total_capsules": 0,
                "by_scenario_type": {},
                "total_simulations": 0,
                "last_learning_date": self.learning_log.get("last_learning_date")
            }

        by_type = {}
        for c in self.capsules:
            by_type[c.scenario_type] = by_type.get(c.scenario_type, 0) + 1

        total_simulations = sum(len(c.simulations) for c in self.capsules)

        return {
            "total_capsules": len(self.capsules),
            "by_scenario_type": by_type,
            "total_simulations": total_simulations,
            "last_learning_date": self.learning_log.get("last_learning_date"),
            "total_learning_cycles": self.learning_log.get("total_learning_cycles", 0)
        }


# ============ 主入口 ============

def run_learning_cycle():
    """
    执行一次社会化学习
    
    由 cron 定时触发
    """
    print(f"[social_learning] 🤖 社会化学习开始...", flush=True)

    try:
        learner = SocialLearner()
        result = learner.learn()

        print(f"[social_learning] ✅ 学习完成", flush=True)
        print(f"   主题: {result['topic']}", flush=True)
        print(f"   搜索到案例: {result['search_results_count']} 条", flush=True)
        print(f"   生成胶囊: {result['capsules_created']} 个", flush=True)
        print(f"   累计胶囊总数: {result['total_capsules']}", flush=True)

        stats = learner.get_learning_stats()
        print(f"[social_learning] 📊 学习统计: {json.dumps(stats, ensure_ascii=False, indent=2)}", flush=True)

        return result

    except Exception as e:
        print(f"[social_learning] ❌ 学习失败: {e}", flush=True)
        return {"status": "error", "error": str(e)}


# ============ 测试 ============

if __name__ == "__main__":
    print("=== Neuro-Agent 社会化学习模块测试 ===\n")

    # 测试学习
    print("【执行一次社会化学习】")
    result = run_learning_cycle()
    print()

    # 测试获取最近胶囊
    learner = SocialLearner()
    print("【最近的社会胶囊】")
    recent = learner.get_recent_capsules(count=3)
    for capsule in recent:
        print(f"  [{capsule['scenario_type']}] {capsule['situation'][:50]}...")
        print(f"    教训: {capsule['lessons']}")
    print()

    # 测试沙盘推演
    print("【沙盘推演测试】")
    test_situations = [
        "用户在工作上被老板批评了",
        "用户的朋友最近失恋了",
        "用户不知道怎么拒绝别人的请求"
    ]
    for situation in test_situations:
        sim = learner.get_simulation_for_context(situation)
        print(f"  情景: {situation}")
        print(f"  推演: {sim.get('simulation_note', 'N/A')}")
        print()

    # 测试统计
    print("【学习统计】")
    stats = learner.get_learning_stats()
    print(json.dumps(stats, ensure_ascii=False, indent=2))
