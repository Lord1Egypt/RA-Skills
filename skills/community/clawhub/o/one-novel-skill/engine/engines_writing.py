#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
写作引擎 — 反AI本能六法则驱动

驱动数据来源: references/de-ai/anti-ai-instinct.md (身体法则/记忆痕迹/痒的法则/拉不说推/反平衡/反完美)

注意: 本引擎只保留 detectors/run_all_detectors.py 未覆盖的专有检测。
      P0 身体法则 / 告情检测 由 d1_banned 覆盖，主语分布由 d6 覆盖。
"""

import re

from .engine_base import EngineBase


class WritingEngine(EngineBase):
    """写作质量引擎 — 检查并修正AI写作缺陷

    专有检测（detectors 未覆盖）：
    - check_standard_actions: 标准答案式动作描写
    - check_ending:           章末旧答案检测  
    - check_direct_evaluation: 直接评价结构
    - check_memory_trace:     下意识反应无来源
    - check_vocabulary_temperature: 语体光谱单
    - check_style_anchor:     风格锚定（段落/动词/形容词/修辞）
    """

    engine_name = "writing"
    engine_tags = ["写作质量"]

    def analyze(self, text, **kwargs):
        issues = []
        for method in [self.check_polish, self.check_memory_trace]:
            try:
                r = method(text)
                if r: issues.extend(r if isinstance(r, list) else [str(r)])
            except Exception:
                pass
        return issues

    # 反AI本能六法则检测表（供参考）
    RULES = {
        "body_law": {
            "name": "身体法则",
            "level": "P0",
            "forbidden": ["感到", "觉得", "认为", "知道"],
            "desc": "禁止用抽象词告知情绪，须用非标准身体动作展示"
        },
        "memory_trace": {
            "name": "记忆痕迹",
            "level": "P0",
            "desc": "每个角色至少2个过去痕迹，下意识反应必须有来源"
        },
        "itch_law": {
            "name": "痒的法则",
            "level": "P0",
            "desc": "章末必须是新问题而非旧答案；好消息后跟坏代价"
        },
        "show_not_tell": {
            "name": "拉不说推",
            "level": "P0",
            "desc": "禁止直接评价/直接告诉情绪，用三样具体细节替代一个结论"
        },
        "anti_balance": {
            "name": "反平衡",
            "level": "P1",
            "desc": "高潮段落字数x3，低潮段落字数/3；禁止连续3段同一情感色调"
        },
        "anti_perfect": {
            "name": "反完美",
            "level": "P2",
            "desc": "对话不准说完所有信息；允许答非所问；允许无明显功能的描写"
        },
    }

    # ---- WritingEngine 专有检测（detectors 未覆盖） ----

    @staticmethod
    def check_standard_actions(text: str) -> list:
        """检查标准答案式的动作描写"""
        standard = ["攥紧了拳头", "低下了头", "咽了口口水", "握紧了拳头",
                     "咬了咬牙", "深吸一口气", "叹了口气"]
        issues = []
        for action in standard:
            count = len(re.findall(re.escape(action), text))
            if count > 0:
                issues.append(f"标准动作: '{action}'x{count} — 建议替换为非标准身体表现")
        return issues

    @staticmethod
    def check_ending(text: str) -> list:
        """检查章末是否为旧答案（违反痒的法则）"""
        endings = ["他终于明白了", "她终于懂了", "就这样结束了",
                    "一切归于平静", "总算", "终于告一段落"]
        last_200 = text[-200:]
        issues = []
        for e in endings:
            if e in last_200:
                issues.append(f"痒的法则: 章末以旧答案'{e}'结尾 — 应改为新问题")
        return issues

    @staticmethod
    def check_direct_evaluation(text: str) -> list:
        """检查拉不说推：直接评价/告知"""
        patterns = [
            (r"他是\w+的", "直接评价'他是XX的'"),
            (r"\w+是\w+的", "直接评价结构"),
            (r"显得很\w+", "显得很XX — 用动作替代"),
            (r"看起来很\w+", "看起来XX — 用动作替代"),
        ]
        issues = []
        for pat, hint in patterns:
            if re.search(pat, text):
                issues.append(f"拉不说推: {hint}")
                break
        return issues

    @staticmethod
    def check_memory_trace(text):
        """记忆痕迹检查 (反AI本能规则2): 角色反应需有来源"""
        issues = []
        triggers = ['习惯性', '下意识', '条件反射', '本能地']
        for t in triggers:
            pos = 0
            count = 0
            while True:
                pos = text.find(t, pos)
                if pos == -1:
                    break
                after = text[pos+len(t):pos+len(t)+40]
                has_source = any(w in after for w in ['因为', '以前', '曾经', '一直', '多年', '从小', '过去', '戒了', '练了', '学了'])
                if not has_source:
                    count += 1
                pos += len(t)
            if count > 0:
                issues.append(f'{t}出现{count}次无来源说明 - 反AI本能规则2要求每处必须有记忆来源')
        return issues

    @staticmethod
    def check_vocabulary_temperature(text):
        """词汇温度计检测: 检查语体光谱变化 (Layer 2, Module 2)"""
        formal = ['因此', '然而', '此外', '综上所述', '显而易见', '不得低于', '须']
        informal = ['靠', '啧', '得了', '得嘞', '拉倒', '哥', '姐', '牛逼', '贼']
        formal_count = sum(text.count(w) for w in formal)
        informal_count = sum(text.count(w) for w in informal)
        issues = []
        total = formal_count + informal_count
        if total > 0:
            temp_ratio = formal_count / total
            if temp_ratio > 0.8 and formal_count > 5:
                issues.append(f'语体温度偏冷(正式语{formal_count}/{total}) - 建议穿插口语化表达')
            elif temp_ratio < 0.2 and informal_count > 5:
                issues.append(f'语体温度偏热(口语词{informal_count}/{total}) - 建议适度正式')
        paras = [p for p in text.split('\n') if len(p) > 30]
        if len(paras) >= 3:
            scores = []
            for p in paras[:10]:
                fi = sum(p.count(w) for w in formal)
                ii = sum(p.count(w) for w in informal)
                scores.append(fi - ii)
            if scores and max(scores) - min(scores) < 2:
                issues.append(f'全篇语体温度变化过小(波动{max(scores)-min(scores)}) - 建议不同场景切换语体')
        return issues

    def compose(self, style, context):
        return ''

    # ---- 统一检查入口 ----

    def check_polish(self, text):
        """检查文本中常见的AI写作缺陷（仅检测，不修改）

        调用顺序：先 detectors 的通用检测，再加 WritingEngine 专有项。
        避免与 run_all_detectors 重复。
        """
        fixes = []
        # WritingEngine 专有检测
        fixes.extend(self.check_standard_actions(text))
        fixes.extend(self.check_ending(text))
        fixes.extend(self.check_direct_evaluation(text))
        fixes.extend(self.check_memory_trace(text))
        fixes.extend(self.check_vocabulary_temperature(text))
        return fixes

    # ====== 以下为写作技法增强检测（detectors 未覆盖，保留） ======

    @staticmethod
    def check_style_anchor(text):
        """风格锚定: 段落/动词/形容词/修辞密度"""
        issues = []
        if not text:
            return []
        paras = text.split(chr(10))
        long_paras = sum(1 for p in paras if len(p) > 150)
        if paras and long_paras / len(paras) > 0.3:
            issues.append(f"段落过长比例{int(long_paras/len(paras)*100)}% - 建议不超过3行")
        weak_verbs = len(re.findall(r"[慢慢|轻轻|缓缓|静静|用力|狠狠]+地", text))
        if weak_verbs > 3:
            issues.append(f"弱动词结构{weak_verbs}处 - 建议替换为强动词")
        common_adj = ["很", "非常", "极其", "十分", "相当", "特别"]
        adj_count = sum(text.count(w) for w in common_adj)
        if adj_count > 5:
            issues.append(f"程度副词{adj_count}次 - 建议用动词+名词替代")
        rhetoric = ["仿佛", "宛如", "犹如", "如同", "好像", "似乎"]
        rhetoric_count = sum(text.count(w) for w in rhetoric)
        if rhetoric_count > 3:
            issues.append(f"比喻/拟似词{rhetoric_count}次 - 修辞密度偏高")
        return issues

    @staticmethod
    def check_verb_variety(text):
        """动词替换建议: 检测基本动词的使用"""
        issues = []
        basic_verbs = {
            "说": ["吼", "嘀咕", "低语", "质问", "嘟囔", "嗫嚅"],
            "走": ["冲", "溜", "踱", "跨", "疾行", "踉跄"],
            "看": ["盯", "瞥", "瞪", "凝视", "打量", "瞟"],
            "想": ["琢磨", "盘算", "寻思", "掂量", "斟酌"],
            "吃": ["啃", "吞", "咽", "撕咬", "品尝"],
        }
        counts = {}
        for verb, alternatives in basic_verbs.items():
            cnt = len(re.findall(verb + r"(?:了|着|过)?[,，。！？\s\n)]", text))
            if cnt > 3:
                counts[verb] = {"count": cnt, "alternatives": alternatives[:3]}
        if counts:
            for v, info in counts.items():
                alts = "/".join(info["alternatives"])
                issues.append(f"{v}使用{info['count']}次 - 建议交替使用: {alts}")
        return issues

    @staticmethod
    def check_scene_word_reuse(text):
        """场景高频词替换检测 (writing-craft.md)"""
        issue_map = {
            "安静": ["落针可闻", "死寂", "连呼吸都放轻了"],
            "高兴": ["嘴角压不住", "脚步轻快", "眉飞色舞"],
            "紧张": ["手心冒汗", "心跳撞得胸腔疼", "呼吸急促"],
        }
        issues = []
        for weak_word, replacements in issue_map.items():
            cnt = text.count(weak_word)
            if cnt > 2:
                issues.append(f"'{weak_word}'出现{cnt}次 - 建议交替: {'/'.join(replacements)}")
        return issues

    @staticmethod
    def check_ai_space_rules(text):
        """AI去痕规则1-2: 英文空格/破折号"""
        issues = []
        spaced = len(re.findall(r"[a-zA-Z0-9] [a-zA-Z0-9]", text))  # 英数间有空格
        if spaced > 5:
            issues.append(f"英文/数字两侧空格{spaced}处 - AI去痕规则1要求删除")
        dash_count = text.count("——")
        if dash_count > 0:
            issues.append(f"破折号{dash_count}处 - AI去痕规则2禁止, 替换为逗号或省略号")
        ai_conn = ["随着", "因此", "此外", "综上所述", "由此可见"]
        acount = sum(text.count(w) for w in ai_conn)
        if acount > 2:
            issues.append(f"AI连接词{acount}处 - 如'随着/因此/综上所述'建议删除或替换")
        return issues

    @staticmethod
    def check_adverb_density(text):
        """检测每千字副词使用频率"""
        flag_count = sum(1 for w in ["很", "非常", "极其", "十分", "相当", "特别", "格外", "愈发", "越来越"] if w in text)
        cn_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        per_1000 = round(flag_count / max(cn_chars / 1000, 1), 1)
        issues = []
        if per_1000 > 8:
            issues.append(f"副词密度{per_1000}/千字 > 8 - 斯蒂芬·金: 副词不是朋友, 用强动词替代")
        return issues

    @staticmethod
    def estimate_draft_reduction(text, target_pct=10):
        """估算第二稿可删减字数 (编辑模式)"""
        if not text:
            return {"original": 0, "target_reduction": 0}
        total = len(text)
        target_remove = int(total * target_pct / 100)
        redundancies = ["其实", "就是", "可以说", "某种程度", "某种意义上"]
        redundant_count = sum(text.count(w) for w in redundancies)
        return {
            "original_chars": total,
            "target_removal": target_remove,
            "redundant_markers": redundant_count,
            "advice": f"建议删除约{target_remove}字(10%), 其中冗余标记{redundant_count}处" if redundant_count > 0 else "文本简洁",
        }

    @staticmethod
    def check_information_exposure(text):
        """每章暴露的设定/底牌信息不应超过信息池的15%"""
        if not text:
            return {"verdict": "无文本"}
        reveal_markers = ["原来", "真相", "秘密", "其实是", "实际上是", "终于知道"]
        reveal_count = sum(text.count(w) for w in reveal_markers)
        cn_chars = len(re.findall(r"[\u4e00-\u9fff]", text))
        density = round(reveal_count / max(cn_chars / 1000, 1), 1)
        return {
            "reveals": reveal_count,
            "density_per_1000": density,
            "verdict": "信息暴露适中" if density < 5 else "信息暴露过多(>5/千字) - 建议藏",
            "advice": "大纲藏着, 设定藏着, 底牌藏着, 实力藏着 - 千幻冰云" if density > 5 else "",
        }

    @staticmethod
    def check_originality(text, known_sources=None):
        """快速原创性评估: 检测复制/洗稿特征"""
        issues = []
        if not text:
            return []
        template_starts = ["在如今这个", "随着时代的", "在这样一个", "众所周知"]
        for t in template_starts:
            if text[:20].startswith(t):
                issues.append(f"模板式开头'{t}' - 建议删除, 直接进入主题")
                break
        ai_words = ["值得注意的是", "值得一提的是", "综上所述", "由此可见", "不可否认"]
        ai_count = sum(text.count(w) for w in ai_words)
        if ai_count > 2:
            issues.append(f"AI连接词{ai_count}处 - 原创性扣分")
        return issues

    @staticmethod
    def check_libraries(project_dir):
        """检查六大库是否建立"""
        from pathlib import Path
        libs = {"创作资料库": "research/background.md",
                "写作技能库": "skills/", "审查校验库": "checklist/",
                "AI去痕库": "de-ai/", "写作要求库": "requirements/",
                "铁律库": "iron-rules.md"}
        results = {}
        d = Path(project_dir)
        for name, path in libs.items():
            p = d / path
            if name == "写作技能库":
                results[name] = p.exists() and any(p.glob("*.md"))
            elif name == "AI去痕库":
                results[name] = p.exists() and any(p.glob("*.md"))
            else:
                results[name] = p.exists()
        return {"libs": results, "ready": all(results.values()),
                "missing": [k for k, v in results.items() if not v]}
