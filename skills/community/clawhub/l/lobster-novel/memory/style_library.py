#!/usr/bin/env python3
"""
lobster-novel: 风格库管理

存储、检索、复用提取的小说风格档案。
支持：
  1) 预设风格模板（开箱即用）
  2) 从文本提取风格并入库
  3) 按流派/特征检索
  4) 设为当前项目激活风格
"""
import json, re
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Tuple
from datetime import datetime


# ── 预设风格模板 ────────────────────────────────────────────
# 开箱即用，不用先找范文
PRESET_STYLES = {
    "修仙爽文": {
        "pov": "third-limited",
        "tense": "past",
        "paragraph_avg_len": 120,
        "sentence_avg_len": 25,
        "dialog_ratio": 0.45,
        "description_ratio": 2.0,
        "vocabulary_level": "simple",
        "tone_adjectives": ["明快", "紧张", "热血"],
        "common_openings": ["就在这时", "突然", "没想到"],
        "favored_phrases": ["突破", "灵气", "丹田", "剑诀", "元神"],
        "sample_sentence": "就在这时，一道剑光划破天际，林风突破到了筑基境。",
        "genre_tags": ["修仙", "玄幻", "爽文"],
    },
    "悬疑推理": {
        "pov": "first",
        "tense": "past",
        "paragraph_avg_len": 200,
        "sentence_avg_len": 32,
        "dialog_ratio": 0.30,
        "description_ratio": 4.0,
        "vocabulary_level": "neutral",
        "tone_adjectives": ["冷峻", "压抑", "紧张"],
        "common_openings": ["那天晚上", "我没想到", "究竟发生了什么"],
        "favored_phrases": ["线索", "不对劲", "奇怪", "调查", "真相"],
        "sample_sentence": "那天晚上的雨水格外冷，我站在空无一人的巷口，闻到一股若有若无的铁锈味。",
        "genre_tags": ["悬疑", "推理", "刑侦"],
    },
    "都市言情": {
        "pov": "third-limited",
        "tense": "present",
        "paragraph_avg_len": 150,
        "sentence_avg_len": 28,
        "dialog_ratio": 0.50,
        "description_ratio": 3.0,
        "vocabulary_level": "neutral",
        "tone_adjectives": ["温暖", "细腻", "温柔"],
        "common_openings": ["她抬起头", "那天阳光很好", "这座城市"],
        "favored_phrases": ["心跳", "眼神", "嘴角", "温柔", "思念"],
        "sample_sentence": "她抬起头，阳光正好落在他侧脸上，心跳漏了一拍。",
        "genre_tags": ["都市", "言情", "现代"],
    },
    "历史架空": {
        "pov": "third-omni",
        "tense": "past",
        "paragraph_avg_len": 180,
        "sentence_avg_len": 35,
        "dialog_ratio": 0.35,
        "description_ratio": 4.5,
        "vocabulary_level": "literary",
        "tone_adjectives": ["沉重", "冷峻", "细腻"],
        "common_openings": ["宣和三年", "自那以后", "天下大势"],
        "favored_phrases": ["之", "其", "乃", "天下", "苍生"],
        "sample_sentence": "宣和三年秋，北方传来急报，铁骑已破三关。",
        "genre_tags": ["历史", "架空", "权谋"],
    },
    "轻小说/沙雕": {
        "pov": "first",
        "tense": "present",
        "paragraph_avg_len": 80,
        "sentence_avg_len": 18,
        "dialog_ratio": 0.60,
        "description_ratio": 1.5,
        "vocabulary_level": "simple",
        "tone_adjectives": ["诙谐", "明快", "轻松"],
        "common_openings": ["事情是这样的", "你别说", "离谱"],
        "favored_phrases": ["不是吧", "离谱", "好家伙", "整活", "摆烂"],
        "sample_sentence": "事情是这样的——我穿越了，但金手指没到账。",
        "genre_tags": ["轻小说", "搞笑", "日常"],
    },
    "克苏鲁/恐怖": {
        "pov": "first",
        "tense": "past",
        "paragraph_avg_len": 250,
        "sentence_avg_len": 38,
        "dialog_ratio": 0.20,
        "description_ratio": 6.0,
        "vocabulary_level": "literary",
        "tone_adjectives": ["压抑", "沉重", "冷峻", "紧张"],
        "common_openings": ["我不该", "那个地方", "一切始于"],
        "favored_phrases": ["不可名状", "深渊", "腐朽", "低语", "疯狂"],
        "sample_sentence": "我不该翻开那本日记的——但一切已经太迟了。",
        "genre_tags": ["恐怖", "克苏鲁", "悬疑"],
    },
    "硬核科幻": {
        "pov": "third-limited",
        "tense": "past",
        "paragraph_avg_len": 220,
        "sentence_avg_len": 36,
        "dialog_ratio": 0.25,
        "description_ratio": 5.0,
        "vocabulary_level": "neutral",
        "tone_adjectives": ["冷峻", "细腻", "沉重"],
        "common_openings": ["公元", "休眠舱打开", "最后的信号"],
        "favored_phrases": ["系统", "信号", "轨道", "坐标", "能源"],
        "sample_sentence": "休眠舱打开的瞬间，显示屏上的日期告诉他——已经过了三百年。",
        "genre_tags": ["科幻", "硬科幻", "未来"],
    },

    # ── 情色武侠（基于9章《江山如此多娇》正文分析）───────────
    "情色武侠": {
        "pov": "third-limited",
        "tense": "past",
        "paragraph_avg_len": 160,
        "sentence_avg_len": 38,
        "dialog_ratio": 0.42,
        "description_ratio": 2.5,
        "vocabulary_level": "literary",
        "tone_adjectives": ["风流", "香艳", "江湖", "潇洒", "旖旎", "淫邪"],
        "common_openings": ["我是个淫贼", "随着一声娇斥", "原来如此", "人生如戏"],
        "favored_phrases": ["江湖", "公子", "美人", "笑道", "玲珑", "姐妹", "萧潇", "武林", "淫贼", "风流", "侠女", "小蝶"],
        "sample_sentence": "我是个淫贼。当然，这已经是过去的事了。淫贼并不是一个可以长久从事的职业，我的大多数同行在出道的三至五年内便光荣殉职了。",
        "genre_tags": ["情色", "武侠", "后宫", "成人"],
        "core_rules": {
            "story_framework": {
                "description": "以武侠世界为框架，情色描写为重要但不唯一的叙事元素",
                "world_building": "必须有完整武侠世界观：门派体系、武功等级、江湖规矩、正邪对立",
                "balance": "武打与情色的交叉推进，约6:4比例"
            },
            "protagonist": {
                "type": "亦正亦邪风流型，魔门/邪派出身但不失正义感",
                "personality": "潇洒不羁、幽默自嘲、重情但不专一、聪明世故",
                "background": "身世坎坷或有特殊体质/天赋（天阳绝脉等），拜师邪派高手",
                "name_style": "单名或双名皆可，忌太白话（如：王动、何同）",
                "examples": "王动（江山如此多娇·主角）、何同（蝶舞大唐春·主角）"
            },
            "female_characters": {
                "types": "多样化：清纯师妹、妖娆侍婢、冷艳女侠、活泼大小姐、神秘女强人，每人独立人格",
                "intro_rule": "每次出场需有外貌描写的惊鸿一瞥，用古风比喻（春水、朝露、玉、花、雪）",
                "relationship": "从排斥到倾心的过程需要充分铺垫，不搞一见就收",
                "count_min": "至少3-5位主要女性角色，每人有独立剧情线和成长弧",
                "example_types": "玲珑双玉（孪生姐妹）、萧潇（贴身侍婢·朝露花雨）、宝亭（商业女强人）、解雨（隐湖仙子）、武舞（将门虎女）"
            },
            "erotic_scenes": {
                "frequency": "每5-8章1次正戏，穿插暧昧调情、眼神勾连",
                "description_style": "用婉约含蓄语言代替直白：七大名器（春水玉壶/比目鱼吻/重峦叠翠/朝露花雨等）、独角龙王等隐喻",
                "rhythm": "调情→障碍→渐入佳境→高潮→事后温情",
                "note": "情色为人物关系服务，不单为写而写；每次需推动人物关系"
            },
            "narrative_style": {
                "tradition": "第三人称有限视角为主，穿插主角内心独白（自嘲/吐槽）",
                "humor": "自嘲和冷幽默贯穿，主角内心戏极其丰富",
                "description": "女性外貌用诗词化比喻（桃颊樱唇/鼻隆眉黛/灿若星河）",
                "language": "半文半白，古风但不晦涩；对话符合人物身份（市井/官场/江湖各有口吻）"
            },
            "plot_structure": {
                "backbone": "一条主线（寻宝/复仇/争霸/查案）+ 多条感情线/势力线",
                "pacing": "武打→智斗→感情→武打的交替节奏，避免连续多章只有情色",
                "twist": "每15-20章有一次重大转折（身份揭露/背叛/势力洗牌）",
                "ending": "开放式偏圆满，不要求1v1；主要感情线需有闭环"
            },
            "world_building_tips": {
                "dynasty": "以真实历史朝代（唐/明/宋）为背景，重要历史事件需考据",
                "martial_arts": "门派需要有特色武学系统和传承谱系",
                "economy": "江湖门派的经济来源要合理（盐商/镖局/田庄/珠宝行）",
                "politics": "江湖与朝廷的关系要微妙，正邪不是非黑即白"
            },
            "forbidden": ["纯肉无剧情", "女主角工具人化（用完就扔）", "过于弱化男性角色", "过于现代的语言风格（网络用语/流行梗）", "低俗直白的性描写", "连续多章无剧情推进", "女性角色全部单一类型"]
        }
    },

    # ── 妖刀记式·暗黑情色武侠（默默猴《妖刀记》1~32卷）──────────
    "妖刀记式-暗黑情色武侠": {
        "pov": "third-limited",
        "tense": "past",
        "paragraph_avg_len": 113,
        "sentence_avg_len": 38,
        "dialog_ratio": 0.18,
        "description_ratio": 1.2,
        "vocabulary_level": "neutral",
        "tone_adjectives": ["诡异", "细腻", "幽暗", "阴郁", "冷峻", "苍茫"],
        "common_openings": ["在不觉云上楼", "每个在华人世界长大的孩子", "数日前于流影城中", "锣鼓声中"],
        "favored_phrases": ["耿照", "慕容", "妖刀", "笑道", "水月停轩", "默默", "埋皇剑冢", "指剑奇宫", "断肠湖", "观海天门"],
        "sample_sentence": "每个在华人世界长大的孩子，心中都有武侠梦。在那里，籍籍无名的少年仗剑驰马，自波澜壮阔的冒险中成长茁壮，得到一些、也失去一些，最后立下不世功勋，成为英雄。",
        "genre_tags": ["情色", "武侠", "暗黑", "成人", "悬疑"],
        "core_rules": {
            "story_framework": {
                "description": "暗黑武侠+情色+悬疑多线叙事，全新架空世界（东胜洲）",
                "world_building": "完整门派体系：水月停轩、指剑奇宫、埋皇剑冢、观海天门等",
                "tone": "阴郁苍茫，宿命感与悬疑色彩贯穿全书"
            },
            "protagonist": {
                "type": "普通出身却卷入巨大阴谋的少年（耿照）",
                "personality": "坚韧、隐忍、在逆境中成长",
                "growth": "从市井少年到江湖高手，伴随巨大代价"
            },
            "narrative_style": {
                "tradition": "多视角第三人称有限，频繁切换POV",
                "prose": "高度文学化，大量环境烘托与心理描写",
                "language": "古典文学笔法，讲究修辞节奏",
                "description": "极尽细腻的氛围营造，兼具古龙式留白与金庸式铺陈"
            },
            "erotic_scenes": {
                "style": "偏向心理和氛围驱动，较少的直白描写",
                "integration": "情色与人物性格/剧情高度融合",
                "principle": "每个女性角色在床戏之外各有面目，坚持情色≠色情"
            },
            "female_characters": {
                "types": "极其丰富多样，各有独立人格动机",
                "depth": "有复杂心理描写，嫉妒、寂寞、患得患失等细腻转变",
                "design": "每个女角有独立「色票」（色彩性格定位）"
            },
            "forbidden": ["脸谱化角色", "空洞情色", "忽略心理描写", "破坏悬疑节奏", "女主角单一类型"]
        }
    },

    # ── 六朝云龙吟式·历史权谋情色武侠（紫狂《六朝云龙吟》第10集）────
    "六朝云龙吟式-历史权谋情色武侠": {
        "pov": "third-limited",
        "tense": "past",
        "paragraph_avg_len": 128,
        "sentence_avg_len": 22,
        "dialog_ratio": 0.30,
        "description_ratio": 1.0,
        "vocabulary_level": "neutral",
        "tone_adjectives": ["华丽", "妩媚", "温柔", "紧张", "香艳", "轻松"],
        "common_openings": ["暮色中的云涛观", "程宗扬随着", "门缝合紧的刹那"],
        "favored_phrases": ["程宗扬", "笑道", "夫人", "小紫", "阮香", "丫头", "刘娥", "香凝", "雁儿", "宗主"],
        "sample_sentence": "暮色中的云涛观肃穆而寂静，观内纤尘不染，显然常有人打扫，但路上没有看到一个人影，也听不到诵经声，安静得仿佛空无一人。",
        "genre_tags": ["情色", "武侠", "历史", "权谋", "成人"],
        "core_rules": {
            "story_framework": {
                "description": "真实历史背景（南北朝/六朝）+情色+权谋+修行",
                "world_building": "法术体系融入历史背景，政治权谋与江湖恩怨交织",
                "balance": "权谋线50%、情色线30%、修行线20%"
            },
            "protagonist": {
                "type": "聪明机敏、善于周旋的市井/底层出身主角（程宗扬）",
                "personality": "滑头却不失原则，好色但不昏头",
                "role": "在多方势力间游走谋利"
            },
            "narrative_style": {
                "tradition": "第三人称有限视角",
                "prose": "明快紧凑，场景转换频繁",
                "language": "半文半白偏白话，节奏快",
                "description": "场景描写细腻，行动描写占主导"
            },
            "historical_setting": {
                "era": "六朝/南北朝",
                "feature": "真实历史框架+架空法术体系",
                "detail": "官制、地理、服饰、饮食需有依据"
            },
            "erotic_scenes": {
                "frequency": "较高，每2-3章1次",
                "style": "较直白但配合情节",
                "principle": "服务于角色关系和权力动态"
            },
            "forbidden": ["忽略历史背景", "主角过于正经", "情色与情节脱节", "权谋线过于简单"]
        }
    },
}


@dataclass
class StyleEntry:
    """风格库中的一条记录"""
    name: str                          # 风格名称
    profile: dict = field(default_factory=dict)   # StyleProfile 字段
    source: str = "extracted"          # extracted / preset / manual
    genre_tags: List[str] = field(default_factory=list)  # 流派标签
    created_at: str = ""
    updated_at: str = ""
    notes: str = ""
    usage_count: int = 0               # 被选用次数


class StyleLibrary:
    """风格库管理器"""

    FILE = "style_library.json"
    ACTIVE_FILE = "active_style.txt"

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir) / "continuity"
        self.dir.mkdir(parents=True, exist_ok=True)
        self.file = self.dir / self.FILE
        self.active_file = self.dir / self.ACTIVE_FILE
        self.styles: Dict[str, StyleEntry] = self._load()

    def _load(self) -> Dict[str, StyleEntry]:
        if not self.file.exists():
            return self._init_presets()
        try:
            data = json.loads(self.file.read_text(encoding="utf-8"))
            if not data:
                return self._init_presets()
            return {k: StyleEntry(**v) for k, v in data.items()}
        except Exception:
            # 文件损坏时回退到预设模板
            return self._init_presets()

    @staticmethod
    def _init_presets() -> Dict[str, StyleEntry]:
        """初始化预设风格模板"""
        entries = {}
        now = datetime.now().isoformat()
        for name, profile in PRESET_STYLES.items():
            p = dict(profile)  # 浅拷贝，不污染原始PRESET_STYLES
            tags = p.pop("genre_tags", [])
            entries[name] = StyleEntry(
                name=name,
                profile=p,
                source="preset",
                genre_tags=tags,
                created_at=now,
                updated_at=now,
            )
        return entries

    def save(self):
        self.file.write_text(
            json.dumps({k: asdict(v) for k, v in self.styles.items()},
                       ensure_ascii=False, indent=2),
            encoding="utf-8")

    # ── CRUD ─────────────────────────────────────────────────

    def register(self, name: str, profile: dict,
                 source: str = "extracted",
                 genre_tags: List[str] = None,
                 notes: str = "") -> StyleEntry:
        """注册一个新风格"""
        now = datetime.now().isoformat()
        entry = StyleEntry(
            name=name,
            profile=profile,
            source=source,
            genre_tags=genre_tags or [],
            created_at=now if name not in self.styles else self.styles[name].created_at,
            updated_at=now,
            notes=notes,
        )
        self.styles[name] = entry
        self.save()
        return entry

    def get(self, name: str) -> Optional[StyleEntry]:
        return self.styles.get(name)

    def delete(self, name: str) -> bool:
        if name in self.styles:
            # 不允许删除预设模板
            if self.styles[name].source == "preset":
                return False
            del self.styles[name]
            self.save()
            return True
        return False

    def list_names(self, genre: str = None) -> List[Tuple[str, str, int]]:
        """列出风格名列表: (name, source, tags_count)"""
        results = []
        for name, entry in self.styles.items():
            if genre and genre not in entry.genre_tags:
                continue
            results.append((name, entry.source, len(entry.genre_tags)))
        return results

    def find_by_genre(self, genre: str) -> List[StyleEntry]:
        """按流派搜索风格"""
        return [e for e in self.styles.values() if genre in e.genre_tags]

    def find_similar(self, target: dict) -> List[Tuple[str, float]]:
        """找相似风格（基于profile字段匹配度）"""
        scores = []
        for name, entry in self.styles.items():
            score = 0.0
            p = entry.profile
            # 词汇级别匹配
            if p.get("vocabulary_level") == target.get("vocabulary_level"):
                score += 20
            # POV匹配
            if p.get("pov") == target.get("pov"):
                score += 15
            # 段落长度相似
            para_diff = abs(p.get("paragraph_avg_len", 0) - target.get("paragraph_avg_len", 0))
            if para_diff < 50:
                score += max(0, 20 - para_diff * 0.4)
            # 对话比例相似
            dialog_diff = abs(p.get("dialog_ratio", 0) - target.get("dialog_ratio", 0))
            if dialog_diff < 0.2:
                score += max(0, 15 - dialog_diff * 75)
            # 语态匹配
            if p.get("tense") == target.get("tense"):
                score += 10
            # 情感形容匹配
            shared_tones = set(p.get("tone_adjectives", [])) & set(target.get("tone_adjectives", []))
            score += len(shared_tones) * 5
            scores.append((name, round(min(score, 100))))
        scores.sort(key=lambda x: -x[1])
        return scores

    def record_usage(self, name: str):
        """记录一次选用"""
        entry = self.styles.get(name)
        if entry:
            entry.usage_count += 1
            self.save()

    # ── 激活管理 ──────────────────────────────────────────────

    def set_active(self, name: str) -> bool:
        """设为当前项目激活风格"""
        if name not in self.styles:
            return False
        self.active_file.write_text(name, encoding="utf-8")
        self.record_usage(name)
        return True

    def get_active(self) -> Optional[StyleEntry]:
        """获取当前激活风格"""
        if not self.active_file.exists():
            return None
        name = self.active_file.read_text(encoding="utf-8").strip()
        return self.styles.get(name)

    def get_active_name(self) -> str:
        """获取当前激活风格名"""
        if not self.active_file.exists():
            return "未设置"
        return self.active_file.read_text(encoding="utf-8").strip()

    # ── 写入注入 ──────────────────────────────────────────────

    def get_prompt_injection(self, name: str = None) -> str:
        """获取风格提示词注入块"""
        entry = self.styles.get(name) if name else self.get_active()
        if not entry:
            return ""

        p = entry.profile
        parts = [f"## 写作风格指南: {entry.name}\n"]
        if entry.genre_tags:
            parts.append(f"流派: {'/'.join(entry.genre_tags)}")

        pov_cn = {"first": "第一人称", "second": "第二人称",
                  "third-limited": "第三人称有限", "third-omni": "第三人称全知"}
        parts.append(f"视角: {pov_cn.get(p.get('pov', ''), p.get('pov', ''))}")

        tense_cn = {"past": "过去时", "present": "现在时"}
        parts.append(f"时态: {tense_cn.get(p.get('tense', ''), p.get('tense', ''))}")

        vocab_cn = {"simple": "通俗", "neutral": "适中", "literary": "文雅"}
        parts.append(f"词汇水准: {vocab_cn.get(p.get('vocabulary_level', ''), p.get('vocabulary_level', ''))}")

        if p.get("paragraph_avg_len"):
            parts.append(f"段落长度参考: ~{p['paragraph_avg_len']}字/段")
        if p.get("dialog_ratio"):
            parts.append(f"对话占比参考: ~{p['dialog_ratio']:.0%}")
        if p.get("tone_adjectives"):
            parts.append(f"氛围: {'、'.join(p['tone_adjectives'][:5])}")
        if p.get("favored_phrases"):
            parts.append(f"常用词汇: {'、'.join(p['favored_phrases'][:6])}")
        if p.get("sample_sentence"):
            parts.append(f"\n风格参考:\n> {p['sample_sentence'][:120]}")

        if p.get("core_rules"):
            cr = p["core_rules"]
            parts.append("")
            parts.append("--- 风格核心规则 ---")
            if isinstance(cr, dict):
                for section, rules in cr.items():
                    if isinstance(rules, dict):
                        # 转换中文section名
                        section_names = {
                            "story_framework": "故事框架",
                            "protagonist": "主角人设",
                            "female_characters": "女性角色",
                            "erotic_scenes": "情色场景",
                            "narrative_style": "叙事风格",
                            "plot_structure": "情节结构",
                            "forbidden": "禁止事项",
                        }
                        cn_section = section_names.get(section, section)
                        parts.append(f"【{cn_section}】")
                        for k, v in rules.items():
                            if isinstance(v, str):
                                parts.append(f"  {v}")
                            else:
                                parts.append(f"  {k}: {v}")
                    elif isinstance(rules, list):
                        parts.append(f"【禁止事项】")
                        for item in rules:
                            parts.append(f"  ❌ {item}")
                    elif isinstance(rules, str):
                        parts.append(f"  {rules}")
            parts.append("")

        return "\n".join(parts)

    # ── 显示 ──────────────────────────────────────────────────

    def summary(self) -> str:
        """风格库摘要"""
        total = len(self.styles)
        presets = sum(1 for e in self.styles.values() if e.source == "preset")
        customs = total - presets
        active = self.get_active_name()

        lines = [
            f"📖 风格库: {total}个风格",
            f"  预设模板: {presets} / 自定义: {customs}",
            f"  当前激活: {active}",
        ]

        # 按流派分类
        genres = {}
        for entry in self.styles.values():
            for tag in entry.genre_tags:
                genres[tag] = genres.get(tag, 0) + 1
        if genres:
            lines.append(f"  流派分布: {'、'.join(f'{g}({c})' for g, c in sorted(genres.items(), key=lambda x: -x[1]))}")

        # 最近添加
        custom_styles = [e for e in self.styles.values() if e.source != "preset"]
        if custom_styles:
            custom_styles.sort(key=lambda e: e.updated_at, reverse=True)
            lines.append(f"  最近添加: {custom_styles[0].name}")

        return "\n".join(lines)

    def dump(self, detail: bool = False) -> str:
        """全部风格可读输出"""
        lines = [f"风格库共{len(self.styles)}个风格\n"]
        for name, entry in sorted(self.styles.items()):
            icon = "⭐" if entry.source == "preset" else "📝"
            active = "◀ 激活中" if name == self.get_active_name() else ""
            lines.append(f"  {icon} {name} {active}")
            if entry.genre_tags:
                lines.append(f"     流派: {'、'.join(entry.genre_tags)}")
            if entry.notes:
                lines.append(f"     备注: {entry.notes}")
            lines.append(f"     来源: {entry.source} | 选用{entry.usage_count}次")
            if detail:
                p = entry.profile
                lines.append(
                    f"     人称:{p.get('pov','?')} 段落:{p.get('paragraph_avg_len','?')}字 "
                    f"对话:{p.get('dialog_ratio',0):.0%} 词汇:{p.get('vocabulary_level','?')}"
                )
            lines.append("")
        return "\n".join(lines)
