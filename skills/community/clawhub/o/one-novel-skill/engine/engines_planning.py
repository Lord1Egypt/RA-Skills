#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""决策规划引擎 — 叙事架构/章节规划/伏笔时间表/多巴胺周期

驱动数据:
  01-narrative-architectures.md (英雄之旅12阶/救猫咪15拍/多幕结构)
  04-reader-psychology.md (多巴胺周期3-5章/期待-满足循环)
  06-platform-algorithms.md (番茄/起点推荐算法参数)
"""


class PlanningEngine:
    """创作规划与调度 — 基于叙事理论"""

    # 英雄之旅12阶段
    HERO_JOURNEY = [
        ("平凡世界", 0.00, 0.05, "展示日常状态与渴望"),
        ("冒险召唤", 0.05, 0.08, "打破平衡的事件"),
        ("拒绝召唤", 0.08, 0.10, "犹豫与风险评估"),
        ("遇见导师", 0.10, 0.15, "获得指导/装备"),
        ("跨越门槛", 0.15, 0.20, "不可逆的决定"),
        ("考验盟友敌人", 0.20, 0.35, "发育期/小爽点"),
        ("深入巢穴", 0.35, 0.45, "接近核心危险"),
        ("严峻考验", 0.45, 0.55, "类死亡体验/低谷"),
        ("获得奖励", 0.55, 0.65, "回报/传承"),
        ("回归之路", 0.65, 0.75, "逃亡/准备决战"),
        ("复活蜕变", 0.75, 0.90, "终极蜕变"),
        ("携宝归来", 0.90, 1.00, "改变世界"),
    ]

    # 救猫咪15拍
    SAVE_THE_CAT = [
        ("开场画面", 0.00, 0.02, "前300字,冲突/异常/悬念"),
        ("主题呈现", 0.02, 0.05, "核心矛盾暗线"),
        ("铺垫", 0.05, 0.10, "初始困境展示"),
        ("催化剂", 0.10, 0.15, "打破平静/第1章结尾"),
        ("争论", 0.15, 0.18, "主角犹豫"),
        ("第二幕开启", 0.18, 0.25, "进入新世界"),
        ("副线", 0.25, 0.30, "感情/兄弟情"),
        ("玩闹与游戏", 0.30, 0.40, "金手指展示/第一次打脸"),
        ("中点", 0.40, 0.50, "伪胜利或伪失败"),
        ("坏人逼近", 0.50, 0.60, "反派反扑"),
        ("一无所有", 0.60, 0.70, "最大低谷"),
        ("灵魂黑夜", 0.70, 0.75, "深刻自我质疑"),
        ("第三幕开启", 0.75, 0.85, "最终方案"),
        ("高潮", 0.85, 0.95, "大决战"),
        ("结局", 0.95, 1.00, "收尾+埋伏笔"),
    ]

    # 多巴胺周期 — 基于04-reader-psychology.md
    DOPAMINE_CYCLE = [
        ("钩子建立期", "抛出小悬念/建立目标, 多巴胺开始分泌"),
        ("期待积累期", "努力但遇困难, 期待值上升, '差一步就能实现'"),
        ("兑现释放期-1", "障碍突破, 多巴胺达峰值释放"),
        ("兑现释放期-2", "满足感+植入新期待, 读者进入下一周期"),
        ("新周期起点", "新钩子已下好, 读者在愉悦中继续"),
    ]

    @staticmethod
    def chapter_plan(ch: int, total: int, hooks: list = None, platform: str = "") -> dict:
        """基于叙事阶段+平台差异化生成章节规划

        platform 影响建议字数、钩子强度和节奏。
        """
        if total <= 0:
            return {"chapter": ch, "core": "", "characters": [], "events": [], "hook_ops": [], "ending": ""}

        ratio = ch / total
        plan = {
            "chapter": ch,
            "ratio": round(ratio, 3),
            "core": "",
            "characters": [],
            "events": [],
            "hook_ops": [],
            "ending": "",
            "dopamine_phase": "",
            "suggested_emotion": "",
            "platform": platform,
        }

        # 平台差异化：字数/节奏/钩子
        _PLATFORM_WORD_MAP = {
            "番茄": 2500, "起点": 3000, "七猫": 2800, "飞卢": 2000,
        }
        plan["suggested_word_count"] = _PLATFORM_WORD_MAP.get(platform, 2500)

        # 平台特有标记
        _PLATFORM_MARKS = {
            "番茄": {"must_have_hook": True, "golden_finger_early": True},
            "飞卢": {"must_have_hook": True, "system_appear_early": True},
            "起点": {"quality_focus": True},
            "七猫": {"emotion_focus": True},
        }
        marks = _PLATFORM_MARKS.get(platform, {})
        plan.update(marks)

        # 从英雄之旅匹配当前阶段
        current_stage = None
        for name, start, end, desc in PlanningEngine.HERO_JOURNEY:
            if start <= ratio < end:
                current_stage = (name, desc)
                break
        if ratio >= 0.99:
            current_stage = ("携宝归来", "改变世界")

        if current_stage:
            plan["core"] = f"{current_stage[0]}: {current_stage[1]}"
            
            # 基于阶段推荐核心动作
            stage_map = {
                "平凡世界": "展示缺陷与渴望",
                "冒险召唤": "制造突破平衡的事件",
                "拒绝召唤": "理性分析+被逼入绝境",
                "遇见导师": "传授核心知识/金手指出现",
                "跨越门槛": "做出不可逆决定,展示主角特质",
                "考验盟友敌人": "结识伙伴+识别对手,小爽点交替",
                "深入巢穴": "推进主线,密集体信息爆发",
                "严峻考验": "给主角最大打击,信念动摇",
                "获得奖励": "核心传承/关键道具/突破",
                "回归之路": "逃亡/准备/各方追杀",
                "复活蜕变": "终极决斗,精神蜕变",
                "携宝归来": "收尾,暗示更大世界",
            }
            for key, val in stage_map.items():
                if key in current_stage[0]:
                    plan["core"] = f"{key}: {val}"
                    break

        # 多巴胺周期定位 (3-5章周期)
        cycle_pos = (ch - 1) % 5
        cycle_phases = ["钩子建立期", "期待积累期", "兑现释放期-1", "兑现释放期-2", "新周期起点"]
        plan["dopamine_phase"] = cycle_phases[cycle_pos] if cycle_pos < 5 else ""

        # 建议情感基调
        emotion_by_phase = {
            "钩子建立期": "平静→好奇",
            "期待积累期": "紧张→期待",
            "兑现释放期-1": "兴奋→满足",
            "兑现释放期-2": "满足→新期待",
            "新周期起点": "愉悦→好奇",
        }
        plan["suggested_emotion"] = emotion_by_phase.get(plan["dopamine_phase"], "")

        # 伏笔操作
        if hooks:
            unresolved = [h for h in hooks if not h.get("resolved")]
            # 在"获得奖励"和"复活蜕变"阶段优先回收长伏笔
            if current_stage and current_stage[0] in ("获得奖励", "复活蜕变"):
                long_hooks = [h for h in unresolved if h.get("recovery_distance") == "long"]
                if long_hooks:
                    plan["hook_ops"].append(f"回收长伏笔: {long_hooks[0].get('text','?')}")
            # 中期阶段埋新伏笔
            if current_stage and current_stage[0] in ("考验盟友敌人", "深入巢穴"):
                plan["hook_ops"].append("建议埋设2-3个新伏笔(中期回收)")

        # 结尾类型建议
        if current_stage:
            ending_map = {
                "平凡世界": "新消息打断宁静",
                "冒险召唤": "真相揭露",
                "拒绝召唤": "被迫接受",
                "跨越门槛": "不可逆行动",
                "考验盟友敌人": "小高潮兑现",
                "深入巢穴": "更大谜团浮出",
                "严峻考验": "最坏结果",
                "获得奖励": "新的威胁",
                "回归之路": "危机逼近",
                "复活蜕变": "终极对决",
                "携宝归来": "余韵+续作钩子",
            }
            for key, ending in ending_map.items():
                if key in current_stage[0]:
                    plan["ending"] = ending
                    break

        # 默认钩子要求（平台差异化已在前置代码中处理）
        plan["must_have_hook"] = True
        
        return plan

    @staticmethod
    def plan_next(state):
        """基于当前状态规划下一章"""
        if not state:
            return {}
        progress = state.get("progress", {})
        written = progress.get("written", 0)
        total = progress.get("total_planned", 100)
        hooks = state.get("plot", {}).get("hooks", [])
        return PlanningEngine.chapter_plan(written + 1, total, hooks)

    @staticmethod
    def decide_arc(progress):
        """基于进度决定当前弧线阶段"""
        total = progress if isinstance(progress, (int, float)) else progress.get("total_planned", 100)
        current = progress if isinstance(progress, (int, float)) else progress.get("written", 0)
        if total <= 0:
            return ""
        ratio = current / total
        if ratio <= 0.05:
            return "开局弧"
        elif ratio <= 0.25:
            return "早期发展弧"
        elif ratio <= 0.50:
            return "中期冲突弧"
        elif ratio <= 0.75:
            return "深化弧"
        else:
            return "高潮结局弧"

    @staticmethod
    def optimize_route(goal, constraints):
        """优化创作路线 (placeholder for advanced planning)"""
        return [goal]

    @staticmethod
    def validate_plan_structure(chapters: int, hook_count: int) -> list:
        """验证全书结构合理性"""
        issues = []
        if chapters > 200 and hook_count < chapters * 0.05:
            issues.append(f"长篇小说({chapters}章)伏笔密度不足: {hook_count}个(建议 {chapters*0.05:.0f}+)")
        if chapters < 50 and hook_count > chapters * 0.2:
            issues.append(f"短篇伏笔过密: {hook_count}个在{chapters}章内")
        return issues

    @staticmethod
    def get_dopamine_calendar(chapters: int) -> list:
        """生成全书多巴胺周期时间表"""
        calendar = []
        for ch in range(1, chapters + 1):
            plan = PlanningEngine.chapter_plan(ch, chapters)
            calendar.append({
                "chapter": ch,
                "phase": plan["dopamine_phase"],
                "emotion": plan["suggested_emotion"],
            })
        return calendar
    # === 大纲四问 (源自outline-planning.md) ===
    @staticmethod
    def outline_4_questions(theme="", mainline="", tone="", ending=""):
        """大纲规划四要素: 主题/主线/基调/结局"""
        qs = {"主题": theme, "主线": mainline, "基调": tone, "结局": ending}
        missing = [k for k, v in qs.items() if not v]
        return {
            "questions": qs,
            "complete": len(missing) == 0,
            "missing": missing,
            "logline": f"{mainline[:30]}... — {theme[:20]}" if mainline and theme else "请补全大纲四问",
        }

    @staticmethod
    def validate_logline(logline):
        """验证一句话梗概完整性: 主角+目标+障碍+独特设定"""
        elements = ["主角", "目标", "障碍", "独特"]
        found = [e for e in elements if e in logline]
        missing = [e for e in elements if e not in found]
        return {"score": int(len(found) / len(elements) * 100),
                "found": found, "missing": missing}

    @staticmethod
    def suggest_three_act(chapters):
        """三幕结构建议 (outline-planning.md: 15-20/65-70/15-20)"""
        if chapters < 10:
            return {"verdict": "短篇"}
        act1_end = int(chapters * 0.18)
        act2_mid = int(chapters * 0.50)
        act3_start = int(chapters * 0.82)
        return {
            "act1": {"range": f"1-{act1_end}", "task": "建立世界/引入主角/激励事件"},
            "act2a": {"range": f"{act1_end+1}-{act2_mid}", "task": "发展/中点转折"},
            "act2b": {"range": f"{act2_mid+1}-{act3_start}", "task": "深化/黎明前黑暗"},
            "act3": {"range": f"{act3_start+1}-{chapters}", "task": "高潮/伏笔回收/结局"},
            "warning": "建议前50章完成第一幕" if act1_end > 50 else "",
        }
    # === 章节计算 & 上下文层级 (源自detailed-outline-guide + context-management) ===
    @staticmethod
    def estimate_chapters(total_words, avg_per_chapter=2850):
        """章节数估算: 总字数/2850"""
        estimated = max(4, round(total_words / avg_per_chapter))
        return {"total_words": total_words, "avg_per_chapter": avg_per_chapter,
                "estimated_chapters": estimated, "min_volumes": max(4, round(estimated / 12))}

    @staticmethod
    def chapter_distribution(chapters):
        """三幕分布: 开端18%/发展65%/高潮17%"""
        if chapters < 10:
            return {"act1": max(2, int(chapters*0.18)), "act2": max(3, int(chapters*0.65)),
                    "act3": max(2, chapters - max(2, int(chapters*0.18)) - max(3, int(chapters*0.65)))}
        return {"act1": int(chapters*0.18), "act2": int(chapters*0.65),
                "act3": max(2, chapters - int(chapters*0.18) - int(chapters*0.65))}

    @staticmethod
    def context_hierarchy(state):
        """上下文四级层次 (context-management.md)"""
        if not state:
            return {"level0": [], "level1": [], "level2": [], "level3": []}
        meta = state.get("meta", {})
        progress = state.get("progress", {})
        written = progress.get("written", 0)
        return {
            "level0_global": ["iron_rules", "world_setting", "style_anchor"],
            "level1_volume": {"current_vol": meta.get("current_volume", 1), "summary": f"{written}章已完成"},
            "level2_near": {"recent_chapters": max(3, min(5, written)), "summary": "近章上下文"},
            "level3_current": {"chapter": written + 1, "spec": "当前章纲"},
        }
    # === 普罗普31种叙事功能 (源自01-narrative-morphology.md) ===
    PROPP_FUNCTIONS = [
        "禁止", "违禁", "刺探", "透露", "欺诈", "共谋", "加害", "缺失",
        "调解", "反抗", "出发", "考验", "反应", "获取", "指引", "对决",
        "标记", "战胜", "消除", "归来", "追捕", "解救", "到达", "要求",
        "任务", "解决", "认出", "揭露", "变形", "惩罚", "婚礼",
    ]

    @staticmethod
    def check_propp_coverage(events):
        """普罗普功能覆盖率检查"""
        if not events:
            return {"coverage": 0, "missing": PlanningEngine.PROPP_FUNCTIONS}
        found = []
        for e in events:
            for f in PlanningEngine.PROPP_FUNCTIONS:
                if f in e and f not in found:
                    found.append(f)
        core = ["加害", "对决", "战胜", "归来", "揭露"]
        missing_core = [f for f in core if f not in found]
        late_found = [f for f in found if found.index(f) < len(found) / 2]
        return {
            "coverage": int(len(found) / len(PlanningEngine.PROPP_FUNCTIONS) * 100),
            "found": len(found),
            "total": len(PlanningEngine.PROPP_FUNCTIONS),
            "missing_core": missing_core,
            "warning": "缺失核心功能: " + ", ".join(missing_core) if missing_core else "",
        }
    # === 短篇/中篇/闪小说参数 (源自short-form/novella/flash) ===
    @staticmethod
    def classify_form(word_count):
        """按字数分类创作形式"""
        if word_count < 1000:
            return {"form": "闪小说", "max_chars": 5, "rule": "50字内必须出现冲突, 一句双重功能"}
        if word_count < 15000:
            return {"form": "短篇", "max_chars": 15, "rule": "单主线, 结尾反转"}
        if word_count <= 40000:
            return {"form": "中篇", "max_chars": 40, "rule": "3-5核心角色, 1主线+1副线"}
        return {"form": "长篇", "rule": "多卷展开, 8种原型覆盖"}

    @staticmethod
    def short_form_advice(form):
        """短篇形式写作建议"""
        advice = {
            "闪小说": "第一句建立场景+角色+冲突. 每个词双重功能. 结尾反转.",
            "短篇": "前300字冲突. 单主线. 核心角色<=5. 字字精准.",
            "中篇": "黄金长度2-3万字. 3-5核心人物. 单主线+至多1副线. 事件密度递进.",
        }
        return advice.get(form, "")
    # === 短篇结构 (源自01-short-story-structure.md) ===
    @staticmethod
    def short_story_check(word_count, character_count, has_one_moment=True):
        """短篇结构检查: 一个瞬间/有限人物/五段式"""
        if word_count > 15000:
            return {"form": "非短篇"}
        issues = []
        if character_count > 5:
            issues.append(f"角色数{character_count}>5 - 短篇核心角色应<=5")
        if not has_one_moment:
            issues.append("短篇应聚焦'一个瞬间' - 角色生命中的一个关键时刻")
        return {"form": "短篇", "issues": issues, "verdict": "合格" if not issues else "需优化"}
    # === 章纲生成 (源自chapter-outline + chapter-plan-guide) ===
    @staticmethod
    def generate_chapter_spec(ch, core_event="", characters=None, hooks=None,
                              emotion_range="平静→紧张→悬念", ending_type="钩子"):
        """生成单章规格"""
        return {
            "chapter": ch, "title": "",
            "core": core_event, "characters": characters or ["主角"],
            "key_events": ["事件1", "事件2"],
            "hooks": hooks or [],
            "emotion": emotion_range,
            "ending": ending_type,
            "word_target": "2200-3500字",
        }

    # === 大纲审查框架 (源自outline-review + setting-outline-review) ===
    @classmethod
    def outline_review(cls, has_clear_sell_point=True, has_satisfaction_points=True,
                       causal_chain_complete=True, char_consistency_ok=True,
                       language_quality_ok=True):
        """大纲六维审查"""
        dims = {
            "核心卖点": has_clear_sell_point,
            "爽点分布": has_satisfaction_points,
            "因果闭环": causal_chain_complete,
            "角色一致": char_consistency_ok,
            "语言质量": language_quality_ok,
        }
        passed = sum(1 for v in dims.values() if v)
        return {
            "dimensions": dims,
            "score": int(passed / len(dims) * 100),
            "verdict": "大纲完善" if passed >= 4 else "需修订",
            "critical": [k for k, v in dims.items() if not v and k in ("核心卖点", "因果闭环")],
        }