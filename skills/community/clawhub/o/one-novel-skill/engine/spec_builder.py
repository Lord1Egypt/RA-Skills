#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re, json
from pathlib import Path
from .contracts import SpecBuilderInput, validate_spec_builder_input
from .writing_notes import build_writing_notes

class SpecBuilder:
    """章节规格生成器 — 接受 SpecBuilderInput dataclass 或 dict（向后兼容）"""

    @staticmethod
    def _to_dict(plan, book_dir, novel_state):
        if isinstance(plan, SpecBuilderInput):
            inp = plan
            d = {"chapter": inp.chapter, "ratio": inp.ratio, "core": inp.core,
                 "ending": inp.ending, "suggested_word_count": inp.suggested_word_count,
                 "dopamine_phase": inp.dopamine_phase,
                 "suggested_emotion": inp.suggested_emotion, "platform": inp.platform}
            if book_dir is None and inp.book_dir:
                book_dir = inp.book_dir
            if novel_state is None:
                novel_state = inp.novel_state
            errs = validate_spec_builder_input(inp)
            if errs:
                import logging
                logging.warning(f"spec_builder: SpecBuilderInput validation: {errs}")
            return d, book_dir, novel_state
        return plan, book_dir, novel_state

    @staticmethod
    def build(plan, book_dir=None, novel_state=None):
        plan, book_dir, novel_state = SpecBuilder._to_dict(plan, book_dir, novel_state)
        if not isinstance(plan, dict):
            import logging
            logging.warning(f"plan not dict (type={type(plan).__name__}), use empty")
            plan = {}
        if not plan.get("core") and not plan.get("chapter"):
            import logging
            logging.warning("plan missing chapter and core")
        ch = plan.get("chapter", 1)
        core = plan.get("core", "")
        ending = plan.get("ending", "悬念收尾")
        wc = plan.get("suggested_word_count", 2500)
        dopamine_phase = plan.get("dopamine_phase", "")
        emotion = plan.get("suggested_emotion", "")
        bs = SpecBuilder._guess_before_state(ch, plan, novel_state)
        mh = SpecBuilder._extract_events(core, plan)
        ks = SpecBuilder._generate_scenes(core, ending, ch, dopamine_phase)
        tc = SpecBuilder._tension_curve(ch, plan)
        # 计算 after_state：基于 before_state + 本章变化
        after_state = SpecBuilder._compute_after_state(bs, ch, plan)
        if not core.strip() and not plan.get("core","").strip():
            import logging
            logging.warning(f"ch{ch}: empty core in plan")
        # 生成写作指导
        platform = plan.get("platform", "")
        genre = plan.get("genre", "")
        total = plan.get("total", 0) or plan.get("total_chapters", 0)
        writing_notes = build_writing_notes(
            platform=platform, chapter=ch,
            total_chapters=total, genre=genre,
        )
        spec = {"chapter": ch, "title": SpecBuilder._guess_title(core, ch),
            "summary": core, "word_count": wc,
            "before_state": bs, "after_state": after_state,
            "must_happen": mh,
            "key_scenes": ks, "tension_curve": tc,
            "ending_type": ending,
            "dopamine_phase": dopamine_phase,
            "suggested_emotion": emotion,
            "new_hooks": [], "plot_advances": [],
            "writing_notes": writing_notes,
            # === 章节契约 (Chapter Contract) 参考 ainovel-cli ===
            "contract": {
                "required_beats": [s[:40] for s in ks if s and s != ""] or ["章节推进"],
                "forbidden_moves": ["信息倾倒", "设定堆砌", "角色OOC", "强行降智"],
                "continuity_checks": [
                    "状态变化是否与前一章衔接",
                    "时间线是否矛盾",
                    "伏笔是否在本章有推进",
                ],
                "emotion_target": emotion or "平静→张力",
                "hook_goal": ending,
            }}
        # 标记无效规格：如果 must_happen 无实际内容
        if mh == ["推进"] and not core.strip():
            spec["_valid"] = False
            spec["_invalid_reason"] = "plan 无有效 core 内容"
        else:
            spec["_valid"] = True
        if book_dir:
            d = Path(book_dir) / "规格"
            d.mkdir(parents=True, exist_ok=True)
            p = d / ("第%03d章.json" % ch)
            try:
                tmp_p = p.with_suffix(".json.tmp")
                tmp_p.write_text(json.dumps(spec, ensure_ascii=False, indent=2), encoding="utf-8")
                if p.exists():
                    p.unlink()
                tmp_p.rename(p)
            except (PermissionError, OSError):
                print("[WARN] 无法写入规格文件")
                return {"spec": spec}

            # 仅输出 .json 格式（v1.1 不再写 .yaml 副本）
            return {"spec": spec, "path": str(p)}
        return {"spec": spec}

    @staticmethod
    def _guess_before_state(ch, plan, novel_state=None):
        """从 NovelState 读取真实角色状态，无 state 时使用比例估算"""
        if novel_state:
            chars = novel_state.all_characters()
            if chars:
                return {
                    "characters": [
                        {"name": name, "state": data.get("state", "?"),
                         "location": data.get("location", "?")}
                        for name, data in chars.items()
                    ],
                    "plot_hooks": [h["text"] for h in novel_state.unresolved_hooks()[:3]]
                }
        # fallback: 无 state 时的比例估算
        r = plan.get("ratio", ch / 100)
        if r <= 0.05:
            return {"characters": [{"name": "主角", "state": "初始", "location": "初始"}], "plot_hooks": []}
        if r <= 0.50:
            return {"characters": [{"name": "主角", "state": "成长", "location": "新地带"}], "plot_hooks": ["伏笔"]}
        return {"characters": [{"name": "主角", "state": "蜕变", "location": "决战地"}], "plot_hooks": ["回收"]}

    @staticmethod
    def _extract_events(core, plan=None):
        e = []
        for s, ev in [("平凡", "展示"), ("召唤", "触发"), ("考验", "打击"), ("蜕变", "突破")]:
            if s in core:
                e.append(ev)
        # 如果有 dopamaine phase，从中提取事件意图
        if plan:
            dop = plan.get("dopamine_phase", "")
            if dop and not e:
                dop_map = {
                    "钩子建立期": "悬念建立",
                    "期待积累期": "矛盾积累",
                    "兑现释放期-1": "冲突爆发",
                    "兑现释放期-2": "快乐满足",
                    "新周期起点": "新线索",
                }
                mapped = dop_map.get(dop)
                if mapped:
                    e.append(mapped)
        return e or ["推进"]

    @staticmethod
    def _generate_scenes(core, ending, ch, dopamine_phase=""):
        if ch <= 1:
            return ["开头:悬念切入", "中段:设定展示", "结尾:钩子"]
        if dopamine_phase == "兑现释放期-1" or dopamine_phase == "兑现释放期-2":
            return ["开头:承接上文", "中段:高潮/满足", "结尾:" + ending]
        if dopamine_phase == "期待积累期":
            return ["开头:承上", "中段:压抑/积累", "结尾:悬念"]
        return ["开头:承接", "中段:推进", "结尾:" + ending]

    @staticmethod
    def _tension_curve(ch, plan):
        r = plan.get("ratio", ch / 100)
        if r <= 0.25:
            return [{"p": 0, "v": 2}, {"p": 50, "v": 7}, {"p": 100, "v": 4}]
        if r <= 0.75:
            return [{"p": 0, "v": 3}, {"p": 40, "v": 7}, {"p": 100, "v": 6}]
        return [{"p": 0, "v": 5}, {"p": 40, "v": 9}, {"p": 100, "v": 3}]

    @staticmethod
    def _compute_after_state(before_state, ch, plan):
        """基于 before_state + 本章 progression 计算 after_state

        进度阈值已参数化为类常量 THRESHOLDS，支持按角色类型差异化。
        """
        bs_chars = before_state.get("characters", [])
        after_chars = []
        r = plan.get("ratio", ch / 100)
        # 进度阈值常量（可覆盖子类）
        T_INIT = 0.05
        T_ENTRY = 0.30
        T_DEEPEN = 0.60
        T_CLIMAX = 0.85
        for c in bs_chars:
            old_state = c.get("state", "初始")
            old_loc = c.get("location", "未知")
            # 角色类型影响发展曲线
            role_type = c.get("role_type", "主角")
            # 根据进度推算变化
            if r <= T_INIT:
                new_state = old_state
                new_loc = old_loc
            elif r <= T_ENTRY:
                new_state = old_state if old_state != "初始" else "入局"
                new_loc = "行进中" if old_loc == "初始" else old_loc
            elif r <= T_DEEPEN:
                if role_type == "配角":
                    new_state = "辅助"
                elif role_type == "反派":
                    new_state = "酝酿"
                else:
                    new_state = "深化" if old_state in ("初始","入局") else old_state
                new_loc = "主舞台"
            elif r <= T_CLIMAX:
                if role_type == "配角":
                    new_state = "助力"
                elif role_type == "反派":
                    new_state = "对决"
                else:
                    new_state = "蜕变"
                new_loc = "决战地"
            else:
                new_state = "终局"
                new_loc = "终局之地"
            after_chars.append({"name": c["name"], "new_state": new_state, "new_location": new_loc})
        return {"characters": after_chars}

    @staticmethod
    def _guess_title(core, ch):
        if ": " in core:
            return core.split(": ")[-1][:12]
        return core.strip()[:12] or ("第%d章" % ch)

    @staticmethod
    def generate_plan(plan, book_dir=None, novel_state=None):
        r = SpecBuilder.build(plan, book_dir, novel_state)
        return r.get("path", "")
