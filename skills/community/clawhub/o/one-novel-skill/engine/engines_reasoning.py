#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""推理引擎 — 因果推理/伏笔调度/情节推演

驱动数据:
  03-classic-techniques.md (金庸4种伏笔/古龙留白技巧)
  01-narrative-architectures.md (草蛇灰线技法/救猫咪结构)
"""


class ReasoningEngine:
    """情节因果推理 — 基于叙事理论"""

    # 金庸4种伏笔类型 (03-classic-techniques.md)
    FORESHADOWING_TYPES = [
        ("物件伏笔", "早期出现的物品后期成为关键"),
        ("人物伏笔", "配角在中后期展现隐藏身份"),
        ("对话伏笔", "人物对话在后期揭示真实含义"),
        ("意象伏笔", "反复出现的意象构建主题隐喻"),
    ]

    # 冲突四重递进
    CONFLICT_LEVELS = ["人与自我", "人与他人", "人与势力", "人与世界"]

    @staticmethod

    def analyze(self, text, **kwargs):
        issues = []
        if text:
            cl = self.conflict_level(text)
            if cl:
                issues.append("[reasoning] " + cl)
        return issues

    def deduce(premise: str, rules: list = None) -> list:
        """基于规则的情节推演 (03-因果关系)"""
        if not rules:
            # 默认推演逻辑
            results = []
            triggers = {
                "发现": "引出新秘密",
                "获得": "引出能力考验",
                "失去": "制造新的目标",
                "背叛": "触发成长弧转折",
                "决斗": "引出更大势力介入",
                "突破": "引来更高层次关注",
                "隐藏": "时机成熟后揭示",
                "交易": "隐藏代价或圈套",
            }
            for trigger, consequence in triggers.items():
                if trigger in premise:
                    results.append(f"「{premise[:30]}...」→ {consequence}")
            if not results:
                results.append(f"推演: {premise[:30]}... → 等待更多上下文")
            return results

        # 用户提供规则时
        results = []
        for r in rules:
            if isinstance(r, dict) and "if" in r and premise.find(r["if"]) >= 0:
                results.append(r.get("then", ""))
        return results or ["无匹配规则"]

    @staticmethod
    def conflict_level(text: str) -> str:
        """判断当前冲突层次"""
        for level in ReasoningEngine.CONFLICT_LEVELS:
            markers_map = {
                "人与自我": ["内心", "愧疚", "自责", "矛盾", "犹豫", "恐惧"],
                "人与他人": ["争吵", "打斗", "对峙", "谈判", "合作"],
                "人与势力": ["组织", "势力", "宗门", "朝廷", "集团", "规则"],
                "人与世界": ["天命", "禁忌", "因果", "世界", "天道", "轮回"],
            }
            markers = markers_map.get(level, [])
            if any(m in text for m in markers):
                return level
        return "人与他人"

    @staticmethod
    def causal_chain(events: list, depth: int = 3) -> list:
        """生成因果关系链 (03-草蛇灰线)"""
        if not events:
            return ["无事件数据"]

        chain = []
        for i, event in enumerate(events[:depth]):
            if isinstance(event, str):
                chain.append(f"事件{i+1}: {event[:40]}...")
            elif isinstance(event, dict):
                chain.append(f"事件{i+1}: {event.get('text','?')[:40]}")
            else:
                chain.append(f"事件{i+1}: {str(event)[:40]}")

        # 补充因果连接
        if len(chain) >= 2:
            chain.append("   ↓ 因果递进")
            chain.append(f"推演结论: {len(events)}个事件的逻辑链")

        return chain

    @staticmethod
    def validate_foreshadowing(hooks: list, total_chapters: int) -> list:
        """验证伏笔埋设和回收的合理性 (03-金庸)"""
        issues = []

        if not hooks:
            return ["无伏笔数据"]

        resolved = [h for h in hooks if isinstance(h, dict) and h.get("resolved")]
        unresolved = [h for h in hooks if isinstance(h, dict) and not h.get("resolved")]
        total = len(hooks)

        # 回收率检查
        if resolved:
            resolve_rate = len(resolved) / total
            if resolve_rate < 0.3 and total > 10:
                issues.append(f"伏笔回收率{resolve_rate:.0%} < 30% - 建议开始回收早期伏笔")
        elif total > 5:
            issues.append(f"{total}个伏笔全部未回收 - 建议在近期开始回收")

        # 埋伏笔距离检查 (短距离=1-3章回收, 长距离>50章)
        ultra_long = [h for h in unresolved if isinstance(h, dict) and h.get("recovery_distance") == "long"]
        if ultra_long and total_chapters > 50:
            issues.append(f"长伏笔{len(ultra_long)}个跨越50章以上 - 需确保埋设时痕迹足够")

        # 伏笔类型多样性 (金庸4种类型)
        types_in_use = set()
        for h in hooks:
            if isinstance(h, dict):
                htype = h.get("type", "general")
                types_in_use.add(htype)

        if len(types_in_use) < 2 and len(hooks) >= 3:
            issues.append(f"伏笔类型单一(仅{', '.join(types_in_use)}) - 建议金庸4种交替使用")

        # 物件伏笔检查 (金庸式: 出场自然+可识别+多次触发)
        object_hooks = [h for h in hooks if isinstance(h, dict) and h.get("type") in ("object", "plot")]
        if object_hooks:
            issues.append(f"确认物件伏笔{len(object_hooks)}个: 出场合理/可识别/可多次触发")

        return issues or ["伏笔结构合理"]

    @staticmethod
    def suggest_foreshadowing_plan(total_chapters: int, genre: str = "general") -> list:
        """建议伏笔布设时间表"""
        plan = []

        if total_chapters < 20:
            plan.append("短篇建议: 1-2个主要伏笔, 10章内回收")
            return plan

        # 三幕结构伏笔建议
        # 第一幕 (0-25%): 埋核心伏笔
        act1_end = int(total_chapters * 0.25)
        plan.append(f"第1-{act1_end}章: 布设全书3个核心伏笔(物件+对话+人物各1)")

        # 第二幕 (25-75%): 陆续回收+新伏笔
        act2_start = act1_end + 1
        act2_end = int(total_chapters * 0.75)
        plan.append(f"第{act2_start}-{act2_end}章: 每15-20章回收1个早期伏笔, 同时埋次要伏笔")

        # 第三幕 (75-100%): 集中回收
        act3_start = act2_end + 1
        plan.append(f"第{act3_start}-{total_chapters}章: 回收全部核心伏笔, 留1-2个开放式悬念")

        if genre in ("xuanhuan", "xianxia", "qihuan"):
            plan.append("玄幻仙侠建议: 分3层揭示世界观秘密(小世界→大世界→宇宙)")

        return plan