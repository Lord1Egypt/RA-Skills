#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
one-novel-skill 世界观/人物/大纲生成器

自动生成小说蓝图：世界观设定 → 人物设计 → 剧情大纲 → 主线支线 → 伏笔埋点。
纯代码编排，LLM 只负责写内容，不负责决策结构。
"""

import json
from pathlib import Path
import re

from .engine_base import EngineBase


class WorldBuilder:
    """小说蓝图生成器"""

    def __init__(self, generator, state, reference):
        self.gen = generator
        self.state = state
        self.ref = reference

    def build(self, genre: str, platform: str, emotion: str = "爽",
              total_chapters: int = 100, reference_keywords: list = None):
        """生成完整小说蓝图，写入 state JSON"""

        print("  [蓝图] 生成大纲/世界观...")
        raw_outline = self.gen.generate("大纲", genre=genre, platform=platform,
            total_words=total_chapters * 2500, chapters=total_chapters,
            emotion=emotion)
        world = raw_outline
        outline = raw_outline

        print("  [蓝图] 生成主角团...")
        # 参考 character-design.md 四维公式：身份+执念+弱点+秘密
        for role_type, archetype in [("主角", "起点最低、成长最大"),
                                      ("配角", "与主角互补或对立"),
                                      ("反派", "动机合理、不降智")]:
            for i in range(1 if role_type == "主角" else 2):
                name_label = f"{role_type}{i+1}" if role_type != "主角" else "主角"
                char_text = self.gen.generate("人物卡", name=name_label,
                    role_type=role_type, world=world[:300])
                for line in char_text.split("\n"):
                    if "姓名" in line or "名字" in line:
                        cname = line.split("：")[-1].split(":")[-1].strip()
                        if cname and len(cname) <= 6:
                            self.state.set_character(cname, {
                                "type": role_type,
                                "archetype": archetype,
                                "card": char_text[:600],
                                "state": "初始",
                                "location": "初始地点",
                            })
                            break

        from .state_accessor import StateAccessor
        sa = StateAccessor(self.state)
        sa.set_meta("outline", outline[:2000])

        # 按卷规划伏笔
        arcs = [
            (1, 30, "开局+金手指"),
            (31, 80, "中期冲突"),
            (81, total_chapters, "高潮+结局"),
        ]
        for start, end, desc in arcs:
            if end <= total_chapters:
                hook_text = self.gen.generate("伏笔规划", written=f"第{start}-{end}章",
                    outline=outline[:1000], pending_hooks=f"{desc}阶段核心伏笔")
                plot = self.state._state.setdefault("plot", {}).setdefault("arcs", [])
                plot.append({
                    "start": start, "end": end, "desc": desc, "plan": hook_text[:500]
                })

        sa.save()
        return {
            "world": world[:500],
            "outline": outline[:500],
            "characters": list(self.state.all_characters().keys()),
            "arcs": len(self.state._state.get("plot", {}).get("arcs", [])),
        }


class Scoring(EngineBase):
    """审核评分系统 — 基于参考数据 quality-check.md 的完整检测清单"""

    engine_name = "scoring"
    engine_tags = ["评分"]

    def analyze(self, text, **kwargs):
        return self.score_text(text, genre=kwargs.get("genre", "general"))

    THRESHOLD = 60
    CHECKLIST_PENALTY = 8
    SHORT_PENALTY_1500 = 15
    SHORT_PENALTY_2000 = 5
    PER_ISSUE_PENALTY = 5
    RED_PENALTY = 30
    YELLOW_PENALTY = 15

    # 来自 quality-check.md 的章节级审查清单
    CHECKLIST = {
        "开篇钩子": lambda t: any(c in t[:300] for c in ['?','！','突然','就在这时','没想到']),
        "开头非天气": lambda t: not any(t[:100].lstrip().startswith(w) for w in [
            '天空','天气','阳光','风雨','下雨','阴天','晴天','多云',
            '雷雨','闪电','刮风','下雪','雾霾','朝霞','晚霞','夕阳',
        ]),
        "主角早出场": lambda t: any(c in t[:500] for c in ['他','她','我','你']),
        "结尾悬念": lambda t: not t[-200:].rstrip().endswith(('。','.')),
        "字数达标": lambda t: 2200 <= len(t) <= 3500,
        "有核心事件": lambda t: len([p for p in t.split('\n') if len(p)>50]) <= 20,
        "局势有变化": lambda t: any(w in t for w in ['发现','知道','决定','突然','原来']),
        "非水字数": lambda t: len(t) > 1500,
    }

    @staticmethod
    def _ensure_detectors_path():
        """确保 detectors/ 在 sys.path 中（防重复插入）"""
        import sys
        from pathlib import Path
        det_dir = str(Path(__file__).parent.parent / "detectors")
        if det_dir not in sys.path:
            sys.path.append(det_dir)

    @staticmethod
    def score_text(text: str, genre: str = "general") -> dict:
        """对文本进行多维度评分，返回分数和判定"""
        Scoring._ensure_detectors_path()
        from run_all_detectors import run_all, extract_cn

        result = run_all(text, genre=genre)
        tc = len(extract_cn(text))

        # 质量基准分
        quality = 100

        # 审查清单评分
        checklist_pass = 0
        checklist_total = len(Scoring.CHECKLIST)
        for name, check_fn in Scoring.CHECKLIST.items():
            if check_fn(text):
                checklist_pass += 1
        quality -= (checklist_total - checklist_pass) * 8
        if tc < 1500:
            quality -= 15
        elif tc < 2000:
            quality -= 5

        # AI检测扣分
        issues_count = result.get("total_issues", 0)
        quality -= issues_count * 5

        # 加权投票直接转分数
        cls = result.get("classification", "")
        if "[RED]" in cls:
            quality -= 30
        elif "[YELLOW]" in cls:
            quality -= 15

        quality = max(0, min(100, quality))

        passed = quality >= Scoring.THRESHOLD

        return {
            "score": quality,
            "passed": passed,
            "issues": issues_count,
            "classification": cls,
            "red_flags": [i for i in result.get("issues", []) if "P0" in i],
        }

    @staticmethod
    def needs_rewrite(score_result: dict) -> bool:
        """判定是否需要重写"""
        if not score_result["passed"]:
            return True
        if score_result.get("red_flags"):
            return True
        if "[YELLOW]" in score_result.get("classification", "") and score_result["score"] < 70:
            return True
        return False

    # === 人物设计四维公式 (源自character-design.md) ===
    @staticmethod
    def character_formula(identity, obsession, weakness, secret):
        """人物四维: 身份标签 + 执念目标 + 致命弱点 + 反差秘密"""
        return {
            "identity": identity,
            "obsession": obsession,
            "weakness": weakness,
            "secret": secret,
            "profile": f"{identity}想{obsession},却{weakness},其实{secret}",
            "score": len(identity) + len(obsession) + len(weakness) + len(secret),
        }

    @staticmethod
    def validate_character_3d(past, present, future):
        """验证角色三维结构: 过去创伤/现在准则/未来弧光"""
        issues = []
        if not past:
            issues.append("缺少过去创伤 - 决定性格的关键经历")
        if not present:
            issues.append("缺少现在准则 - 行为逻辑和底线")
        if not future:
            issues.append("缺少未来弧光 - 成长方向")
        if past and present:
            # 从创伤到准则的推导
            if any(w in past for w in ["背叛", "欺骗", "伤害"]):
                if not any(w in present for w in ["不信任", "冷漠", "孤立"]):
                    issues.append("创伤与准则不匹配: 背叛经历应导出不信任准则")
        return issues

    # === 世界观五维 (源自world-building.md) ===
    @staticmethod
    def validate_world(dimensions):
        """验证世界观五维完整性"""
        required = ["theme", "time_space", "power_system", "society", "economy"]
        result = {k: False for k in required}
        for key in required:
            if key in dimensions and dimensions[key]:
                result[key] = True
        missing = [k for k, v in result.items() if not v]
        return {"complete": len(missing) == 0, "missing": missing,
                "score": int((len(required) - len(missing)) / len(required) * 100)}

    @staticmethod
    def check_world_ecology(geography, economics, politics):
        """检查地理-资源-经济-政治因果链完整性"""
        gaps = []
        if geography and not economics:
            gaps.append("地理定义了资源分布,但缺少经济系统描述")
        if economics and not politics:
            gaps.append("经济形态决定了权力结构,但缺少政治格局描述")
        if geography and not politics:
            gaps.append("环境地理应影响权力格局")
        return gaps or ["因果链完整"]
    # === 命名检查 (源自naming-guide.md 七大铁律) ===
    @staticmethod
    def check_name(name):
        """检查角色/地名是否符合命名七律"""
        issues = []
        if not name:
            return ["名称为空"]
        # 规则1: 字符规范
        if re.search(r"[a-zA-Z0-9]", name):
            issues.append("含字母/数字 - 全中文命名")
        if re.search(r"[\u4e00-\u9fff]", name):
            pass  # 有中文
        else:
            issues.append("无中文字符")
        # 规则2: 易写易认
        rare = re.findall(r"[^\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef]", name)
        if rare:
            issues.append(f"含生僻字{rare} - 建议使用常见字")
        # 规则3: 独特性 (长度)
        cn_chars = len(re.findall(r"[\u4e00-\u9fff]", name))
        if cn_chars <= 1:
            issues.append("过短 - 建议2-3字")
        elif cn_chars > 4:
            issues.append(f"过长({cn_chars}字) - 建议2-3字")
        # 规则5: 谐音检查
        bad_homophones = ["屎", "尿", "屁", "死", "亡", "丧", "悲", "哭"]
        for b in bad_homophones:
            if b in name:
                issues.append(f"含不良谐音'{b}' - 建议更换")
        return issues

    @staticmethod
    def suggest_name(gender="男", role_type="主角", style="仙侠"):
        """建议命名方案"""
        prefixes = {"男": ["萧", "林", "叶", "楚", "江", "顾", "陆", "秦", "苏", "沈"],
                    "女": ["苏", "林", "白", "沈", "顾", "洛", "安", "慕", "温", "姜"]}
        suffixes = {"男": ["辰", "尘", "玄", "渊", "澜", "御", "墨", "寒", "风", "天"],
                    "女": ["雪", "月", "瑶", "溪", "浅", "汐", "薇", "晴", "涵", "晚"]}
        p = prefixes.get(gender, prefixes["男"])
        s = suffixes.get(gender, suffixes["男"])
        style_map = {"仙侠": ["萧", "剑", "灵", "玄"], "都市": ["江", "林", "明", "天"]}
        return {"prefix": p[:3], "suffix": s[:3], "style_hint": style_map.get(style, [])}
    # === 8种原型系统 (源自07-45-master-characters.md, 实现了8/45) ===
    ARCHETYPES = {
        "英雄": {"动机": "证明自我", "恐惧": "示弱"},
        "导师": {"动机": "传递智慧", "恐惧": "见死不救"},
        "守门人": {"动机": "维持秩序", "恐惧": "规则被破"},
        "信使": {"动机": "传递信息", "恐惧": "信息失真"},
        "变形者": {"动机": "适应变化", "恐惧": "身份迷失"},
        "阴影": {"动机": "毁灭对立", "恐惧": "被光明吞噬"},
        "盟友": {"动机": "互助共赢", "恐惧": "被背叛"},
        "捣蛋鬼": {"动机": "打破常规", "恐惧": "无聊重复"},
    }

    @staticmethod
    def assign_archetype(character_name, primary, secondary_1="", secondary_2=""):
        """为角色分配原型"""
        arch = WorldBuilder.ARCHETYPES.get(primary, {})
        s1 = WorldBuilder.ARCHETYPES.get(secondary_1, {})
        s2 = WorldBuilder.ARCHETYPES.get(secondary_2, {})
        return {
            "character": character_name,
            "primary": primary, "primary_motivation": arch.get("动机", ""),
            "secondary": [secondary_1, secondary_2],
            "all_motivations": list(set(filter(None, [arch.get("动机",""), s1.get("动机",""), s2.get("动机","")]))),
            "narrative_function": "主角" if primary == "英雄" else "导师/引导者" if primary == "导师" else "对手" if primary == "阴影" else "配角",
        }

    @staticmethod
    def check_archetype_coverage(chars):
        """检查角色列表中8种原型的覆盖率"""
        if not chars:
            return {"coverage": 0, "missing": list(WorldBuilder.ARCHETYPES.keys())}
        present = set()
        for c in chars:
            if isinstance(c, dict):
                p = c.get("primary", "")
                if p:
                    present.add(p)
                for s in c.get("secondary", []):
                    if s:
                        present.add(s)
        all_types = set(WorldBuilder.ARCHETYPES.keys())
        missing = all_types - present
        return {"coverage": int(len(present) / len(all_types) * 100),
                "present": list(present), "missing": list(missing)}
    # === 魔法体系&科幻设定检查 ===
    @staticmethod
    def check_magic_system(system):
        """桑德森魔法法则检查: 规则清晰度/局限性/代价"""
        if not system:
            return ["无魔法体系定义"]
        issues = []
        rules = system.get("rules", [])
        limits = system.get("limits", [])
        costs = system.get("costs", [])
        if len(rules) < 3:
            issues.append(f"魔法规则仅{len(rules)}条 - 桑德森法则: 规则越清晰越有趣")
        if not limits:
            issues.append("无局限性定义 - 无限能力的魔法会杀死悬念")
        if not costs:
            issues.append("无代价定义 - 强大魔法需对应代价")
        return issues

    @staticmethod
    def check_tech_consistency(tech_system):
        """硬科幻OBL检查: 技术突破点不超过1-2个"""
        if not tech_system:
            return ["无科技体系定义"]
        issues = []
        big_lies = tech_system.get("big_lies", [])
        if len(big_lies) > 2:
            issues.append(f"技术突破点{len(big_lies)}个 > 2 - 硬科幻建议不超过1个技术假设")
        return issues
    # === 轻小说角色属性 (源自01-light-novel-characters.md) ===
    @staticmethod
    def light_novel_archetype(name, primary_attr="", secondary_attr=""):
        """分配轻小说角色属性"""
        attrs = {
            "傲娇": "嘴硬心软, 口是心非但关键时刻可靠",
            "病娇": "极端执着, 为爱偏执到不择手段",
            "冷娇": "表面冷漠但暗地关心, 不善于表达",
            "慵懒": "看似什么都不在乎, 但该出手时绝不犹豫",
            "沉默": "话少但观察力强, 行动先于语言",
            "天然": "纯真直率, 无意中说出关键的话",
            "腹黑": "表面温和但暗中布局, 笑里藏刀",
        }
        p_desc = attrs.get(primary_attr, "")
        s_desc = attrs.get(secondary_attr, "")
        return {
            "character": name,
            "primary_attribute": primary_attr,
            "primary_desc": p_desc,
            "secondary_attribute": secondary_attr,
            "secondary_desc": s_desc,
            "attribute_count": (1 if primary_attr else 0) + (1 if secondary_attr else 0),
        }
    # === 圆形/扁平人物检测 (源自02-aspects-of-the-novel.md 福斯特) ===
    @staticmethod
    def classify_character_roundness(traits, motives):
        """检测角色是圆形(>=3矛盾特质/2深层动机)还是扁平"""
        if not traits and not motives:
            return {"type": "扁平", "score": 0}
        trait_count = len(traits) if isinstance(traits, list) else 0
        motive_count = len(motives) if isinstance(motives, list) else 0
        score = trait_count + motive_count * 2
        return {
            "type": "圆形" if score >= 6 else "扁平",
            "score": score,
            "traits": trait_count, "motives": motive_count,
            "verdict": "圆形人物: 能令人信服地惊讶读者" if score >= 6 else "扁平人物: 适合配角/喜剧",
            "advice": "增加至少1个矛盾特质或1个深层动机" if 3 <= score < 6 else "",
        }
    # === 跨媒体延展性评估 (源自02-cross-media.md) ===
    @staticmethod
    def transmedia_potential(world_depth, char_breadth, has_gaps=True):
        """评估跨媒体延展潜力"""
        score = 0
        if world_depth >= 3:
            score += 3
        if char_breadth >= 5:
            score += 2
        if has_gaps:
            score += 2  # 未填满的时间线
        return {"score": min(10, score), "verdict": "高延展性" if score >= 7 else "中" if score >= 4 else "低"}

    def add_chapters_incremental(self, start_chapter, count, existing_state=None):
        from datetime import datetime
        msg = '增量规划第{}-{}章（基于已有{}章状态）'.format(
            start_chapter, start_chapter + count - 1, len(existing_state or []))
        return {'message': msg, 'start': start_chapter, 'count': count}

    def refine_later_chapters(self, written_so_far, total):
        from datetime import datetime
        horizon = written_so_far
        rstart = horizon + 1
        rend = min(horizon * 2, total)
        if rstart > total or rend <= rstart:
            return []
        return [{'action': 'refine', 'range': '{}-{}'.format(rstart, rend),
                 'count': rend - rstart + 1,
                 'prompt': '当前已写{}章，请细化第{}-{}章的细纲'.format(written_so_far, rstart, rend),
                 'timestamp': datetime.now().isoformat()}]
