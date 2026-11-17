#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""故事发展引擎 - 成长弧/节奏验证/事件密度

驱动数据:
  04-reader-psychology.md (阅读疲劳曲线/预期管理/损失厌恶)
  09-editor-perspective.md (14道审查关卡/节奏审查)
  01-narrative-architectures.md (英雄之旅/救猫咪/多幕结构)
"""


class DevelopmentEngine:
    """角色成长弧与叙事节奏"""

    # 成长弧五阶段 - 源自英雄之旅
    GROWTH_STAGES = [
        ("起点", "能力未觉醒, 欲望萌芽"),
        ("成长", "小胜利积累, 技能学习"),
        ("考验", "核心冲突, 信念动摇"),
        ("蜕变", "突破限制, 获得新能力"),
        ("终局", "完全成熟, 改变世界"),
    ]

    # 冲突等级 - 源自09-editor-perspective
    CONFLICT_LEVELS = [
        ("日常冲突", 0.50, "小摩擦、小矛盾"),
        ("中度冲突", 0.35, "重要对决、突破、危机"),
        ("极限冲突", 0.15, "生死之战、大高潮"),
    ]

    # 阅读疲劳周期 - 源自04-reader-psychology
    FATIGUE_MODEL = {
        "注意力上升": {"start": 0, "duration_ms": 180000},
        "注意力高峰": {"start": 180000, "duration_ms": 420000},
        "注意力下降": {"start": 600000, "duration_ms": 300000},
        "疲劳临界": {"start": 900000, "duration_ms": 300000},
    }


    def analyze(self, text, **kwargs):
        """故事发展分析 — 事件密度/段落节奏"""
        issues = []
        chapter = kwargs.get("ch", 0)

        # 1. 粗略节奏评估
        if text and chapter > 0:
            paras = [p for p in text.split('\n') if p.strip()]
            if len(paras) < 5:
                issues.append("[发展] 段落过少，建议丰富叙事结构")
            avg_para = sum(len(p) for p in paras) / max(len(paras), 1) if paras else 0
            if avg_para > 250:
                issues.append(f"[发展] 平均段落{avg_para:.0f}字偏长，建议拆分")

        return issues

    @staticmethod
    def growth_arc(stages: list = None) -> list:
        """生成默认或自定义成长弧"""
        if not stages:
            return list(DevelopmentEngine.GROWTH_STAGES)
        # 验证阶段顺序合理性
        expected = [s[0] for s in DevelopmentEngine.GROWTH_STAGES]
        actual = [s if isinstance(s, str) else s[0] for s in stages]
        # 检查是否有跨越重要阶段
        missing = [e for e in expected if e not in actual]
        if missing:
            stages.append(("注意", f"缺失阶段: {', '.join(missing)}"))
        return stages

    @staticmethod
    def validate_pacing(chapters: int, events: list = None) -> list:
        """基于09-editor-perspective的14关节奏审查"""
        issues = []

        if chapters <= 0:
            return ["章节数为0"]

        # 事件密度检查 (09-编辑视角: 第三关节奏与结构)
        if events:
            event_density = len(events) / chapters
            if event_density < 0.05:
                issues.append(f"事件密度{event_density:.3f}/章 < 0.05 建议每5-10章至少1个关键事件")
            elif event_density > 0.5:
                issues.append(f"事件密度{event_density:.3f}/章 > 0.5 可能过度密集")
        else:
            issues.append("无关键事件 - 剧情可能推进不足")
            issues.append("建议加入" + ", ".join([
                "30章内引入反派", "50章内揭示世界观核心", "80章内主角质变"
            ]))

        # 结构完整性检查 (09-编辑视角: 三幕/四幕/五幕)
        if chapters >= 50:
            # 三幕结构要求前10章完成导入
            if chapters >= 80:
                first_act_ratio = 50 / chapters
                if first_act_ratio > 0.35:
                    issues.append(f"第一幕({50}章)占{first_act_ratio:.0%}过长, 建议压缩至30%以内")
                third_act_ratio = 30 / chapters
                if third_act_ratio < 0.10:
                    issues.append(f"第三幕({chapters-50-30}章后)过短")

        # 冲突层次分布 (04-读者心理: 疲劳曲线)
        if chapters >= 30:
            expected_extreme = max(1, int(chapters * 0.15))
            issues.append(f"建议极限冲突约{expected_extreme}次(全书{chapters}章の15%)")

        return issues or ["节奏验证通过"]

    @staticmethod
    def validate_growth_arc(character_states: list, total_chapters: int) -> list:
        """验证单个角色的成长弧完整性"""
        issues = []
        if not character_states:
            return ["无角色状态数据"]

        # 检查是否有初始状态
        first = character_states[0] if isinstance(character_states[0], dict) else {}
        last = character_states[-1] if isinstance(character_states[-1], dict) else {}

        if not first.get("state") and not first.get("name"):
            issues.append("缺少角色初始状态")

        # 检查是否有变化
        if first.get("state") == last.get("state"):
            issues.append("角色状态全程未变 - 可能缺乏成长弧")

        # 检查是否有低谷 (英雄之旅第8阶段)
        has_low_point = any(
            isinstance(s, dict) and "失败" in str(s.get("state", ""))
            for s in character_states
        )
        if not has_low_point and total_chapters > 50:
            issues.append("长篇建议有至少1次角色低谷(类死亡体验)")

        return issues

    @staticmethod
    def suggest_tension_curve(total_chapters: int, genre: str = "general") -> list:
        """基于阅读疲劳曲线推荐张力分布"""
        curve = []
        for ch in range(1, total_chapters + 1):
            ratio = ch / total_chapters
            # 开局快速上升
            if ratio <= 0.05:
                tension = 0.3 + ratio * 10  # 0.3 -> 0.8
            elif ratio <= 0.15:
                tension = 0.6 + (ratio - 0.05) * 2  # 0.6 -> 0.8
            elif ratio <= 0.35:
                tension = 0.4 + (ratio - 0.15) * 2  # 起伏
            elif ratio <= 0.50:
                tension = 0.3 + (ratio - 0.35) * 4  # 中期推高
            elif ratio <= 0.70:
                tension = max(0.4, 0.9 - (ratio - 0.50) * 2)  # 波动
            elif ratio <= 0.85:
                tension = 0.5 + (ratio - 0.70) * 2  # 后期攀升
            else:
                tension = 0.8 + (ratio - 0.85) * 2  # 高潮

            tension = max(0.1, min(1.0, tension))
            curve.append({"chapter": ch, "ratio": round(ratio, 3), "tension": round(tension, 2)})

        return curve



    # === 节奏检查: 章节节奏/钩子/冲突密度 (源自pacing-guide.md + reader-engagement.md) ===

    @staticmethod
    def check_chapter_rhythm(text):
        result = {"opening_hook": False, "ending_hook": False, "issues": []}
        if not text or len(text) < 200:
            result["verdict"] = "文本过短"
            return result
        first100 = text[:100]
        last200 = text[-200:]
        hook_words = ["?", "!", "?", "!", "突然", "发现", "原来"]
        result["opening_hook"] = any(w in first100 for w in hook_words)
        result["ending_hook"] = any(w in last200 for w in hook_words)
        if not result["opening_hook"]:
            result["issues"].append("开头缺少冲突/悬念 - 首段3句内应建立")
        if not result["ending_hook"]:
            result["issues"].append("结尾缺少钩子")
        result["verdict"] = "合格" if len(result["issues"]) <= 1 else "需优化"
        return result

    @staticmethod
    def check_micro_conflict(text):
        issues = []
        markers = ["？", "！", "?", "!", "但是", "却", "然而", "矛盾", "争论", "不满", "尴尬", "犹豫", "突然"]
        paras = [p for p in text.split("\n") if len(p) > 20]
        conflict_paras = 0
        for p in paras[:20]:
            if any(w in p for w in markers):
                conflict_paras += 1
        if paras and conflict_paras / len(paras[:20]) < 0.15:
            issues.append("微冲突密度过低 - 日常章节必须有微冲突")
        return issues

    @staticmethod
    def suggest_pacing(chapter, total):
        if total <= 0:
            return {"phase": "未知", "pace": "未知", "suggestion": "请设置总章节数"}
        ratio = chapter / total
        if ratio <= 0.05:
            return {"phase": "开局", "pace": "快", "suggestion": "密集爽点"}
        elif ratio <= 0.25:
            return {"phase": "早期", "pace": "中快", "suggestion": "加深设定"}
        elif ratio <= 0.75:
            return {"phase": "中期", "pace": "中慢", "suggestion": "穿插大小高潮"}
        else:
            return {"phase": "收尾", "pace": "快", "suggestion": "加速冲向终局"}
    # === 断章位置检测 (源自08-tracking-rate-guide.md) ===
    @staticmethod
    def check_chapter_ending_position(text):
        """断章位置: 高潮前/高潮中/高潮后"""
        if not text:
            return {"position": "unknown"}
        ending = text[-200:]
        # 高潮前: 悬念/疑问/未知
        if any(w in ending for w in ["?", "?", "难道", "究竟"]):
            return {"position": "高潮前", "verdict": "最佳断章 - 追读率+40%"}
        # 高潮中: 正在发生
        if any(w in ending for w in ["就在", "这时", "突然", "--", "--"]):
            return {"position": "高潮中", "verdict": "有效断章"}
        # 高潮后: 已结束
        if any(w in ending for w in ["结束了", "终于", "成功了", "完了"]):
            return {"position": "高潮后", "verdict": "低效断章 - 读者已满足, 翻页动力弱"}
        return {"position": "平淡结尾", "verdict": "建议高潮前断章"}

    # === 世界观金字塔法则 (源自13-world-building-guide.md) ===
    @staticmethod
    def check_world_pyramid(shown=10, known=30, foundation=60):
        """世界观金字塔: 展示10%/知道30%/掌握60%"""
        total = shown + known + foundation
        if total == 0:
            return {"verdict": "无世界观数据"}
        issues = []
        if shown / total > 0.2:
            issues.append(f"展示比例{shown}% > 20% - 过多设定暴露在正文中")
        if foundation / total < 0.5:
            issues.append(f"底层{foundation}% < 50% - 世界观逻辑支撑不足")
        return {"shown": shown, "known": known, "foundation": foundation,
                "issues": issues, "verdict": "金字塔合理" if not issues else "需调整"}