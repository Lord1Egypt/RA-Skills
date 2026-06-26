#!/usr/bin/env python3
"""
lobster-novel: LLM-driven Arc Planner (重写版)
=============================================
Replace old template-based arc_planner with SenseNova LLM-driven planning.
Two-phase architecture:
  Phase 1: LLM generates volume-level outline (story beats + level milestones)
  Phase 2: LLM expands each volume into chapter-level plan

DND 5e power reference built-in for level-appropriate encounter/plot guidance.
"""
import json, re, os, logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Tuple
from datetime import datetime
import urllib.request
import urllib.error

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("arc_planner")


# ═══════════════════════════════════════════════════════════════
#  DND 5e Power Reference
# ═══════════════════════════════════════════════════════════════

DND5E_LEVEL_MILESTONES = {
    "tier1":   (1, 4,   "Local heroes: village-level threats, goblins, bandits, starter dungeons"),
    "tier2":   (5, 10,  "Heroes of the realm: city-level threats, giants, dragons, political intrigue"),
    "tier3":   (11, 16, "Masters of the realm: kingdom-level threats, planar incursions, archmages"),
    "tier4":   (17, 20, "Masters of the world: save-the-world quests, demon lords, gods' avatars"),
    "epic":    (21, 30, "Epic legend: lesser deities, planar lords, existential threats"),
    "godlike": (31, 40, "Near-divine: demon princes, archdevils, cosmic balance"),
}

DND5E_CLASS_PROGRESSION = {
    "barbarian": {
        1:  "Rage (2/day), Unarmored Defense",
        2:  "Reckless Attack, Danger Sense",
        3:  "Primal Path (totem/berserker/etc), Rage 3/day",
        5:  "Extra Attack, Fast Movement",
        7:  "Primal Path feature, Feral Instinct",
        9:  "Brutal Critical (1 die), Rage 4/day",
        11: "Relentless Rage",
        14: "Primal Path feature",
        15: "Persistent Rage",
        17: "Brutal Critical (2 dice), Rage 5/day",
        18: "Indomitable Might",
        20: "Primal Champion (STR/CON +4, cap 24)",
    },
    "sorcerer": {
        1:  "Spellcasting, Sorcerous Origin (draconic bloodline)",
        2:  "Font of Magic (sorcery points)",
        3:  "Metamagic (2 options)",
        5:  "Metamagic (3 options)",
        6:  "Sorcerous Origin feature (elemental affinity: fire)",
        7:  "Metamagic (4 options)",
        10: "Sorcerous Origin feature (dragonic wings)",
        11: "Sorcerous Origin feature (dragon breath)",
        14: "Sorcerous Origin feature (dragon resistance)",
        17: "Metamagic (5 options)",
        18: "Sorcerous Origin feature (dragon apotheosis)",
    },
    "bard": {
        1:  "Spellcasting, Bardic Inspiration (d6)",
        2:  "Jack of All Trades, Song of Rest (d6)",
        3:  "Bard College, Expertise (2 skills)",
        5:  "Bardic Inspiration (d8), Font of Inspiration",
        6:  "Countercharm, Bard College feature",
        10: "Bardic Inspiration (d10), Expertise (2 more), Magical Secrets",
        14: "Bardic Inspiration (d12), Magical Secrets",
        18: "Magical Secrets (×2)",
        20: "Superior Inspiration",
    }
}


# ═══════════════════════════════════════════════════════════════
#  Data Models
# ═══════════════════════════════════════════════════════════════

@dataclass
class VolumePlan:
    """One volume (arc) outline."""
    number: int
    title: str
    chapters: int                # 该卷分配章节数
    word_count: int              # 该卷目标字数
    summary: str                 # 卷概要
    main_locations: List[str]    # 主要场景
    level_range: Tuple[int, int] # 主角等级范围 (起始→结束)
    class_growth: List[str]      # 职业等级变化，如 ["barbarian 1→5"]
    key_encounters: List[str]    # 关键战斗/事件
    character_arcs: List[str]    # 角色发展弧线
    climax_type: str             # climax变体: battle/diplomacy/revelation/sacrifice


@dataclass
class ChapterPlan:
    """One chapter's plan."""
    number: int
    title: str
    summary: str                 # ~200字内容概要
    location: str                # 场景地点
    pov: str = ""                # 视角角色
    word_target: int = 4000      # 目标字数
    scenes: int = 3              # 场景数
    dramatic_type: str = ""      # buildup/climax/resolution/twist
    character_focus: List[str] = field(default_factory=list)


@dataclass
class FullNovelPlan:
    """Complete multi-volume novel plan."""
    title: str
    logline: str
    total_volumes: int
    total_chapters: int
    total_words: int
    volumes: List[VolumePlan] = field(default_factory=list)
    chapter_plans: Dict[int, List[ChapterPlan]] = field(default_factory=dict)
    final_character_sheet: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_text(self) -> str:
        lines = [
            f"# {self.title}",
            f"Logline: {self.logline}",
            f"{self.total_volumes} Volumes | {self.total_chapters} Chapters | ~{self.total_words:,} words",
            "",
        ]
        for vol in self.volumes:
            lines.extend([
                f"## 卷{vol.number}: {vol.title} ({vol.chapters}章, ~{vol.word_count:,}字)",
                f"  场景: {' / '.join(vol.main_locations[:4])}",
                f"  等级: {vol.level_range[0]}→{vol.level_range[1]}级",
                f"  职业成长: {'; '.join(vol.class_growth)}",
                f"  {vol.summary}",
                "",
            ])
            for ch in self.chapter_plans.get(vol.number, []):
                lines.append(f"  Ch{ch.number:03d}: {ch.title}")
                lines.append(f"       {ch.summary[:100]}")
                lines.append(f"       [{ch.location}]  {'/'.join(ch.character_focus[:3])}")
                lines.append("")
        return "\n".join(lines)

    def save(self, path: Path):
        path.write_text(json.dumps(
            {"text": self.to_text(), "structured": asdict(self)},
            ensure_ascii=False, indent=2), encoding="utf-8")


# ═══════════════════════════════════════════════════════════════
#  DeepSeek API Wrapper
# ═══════════════════════════════════════════════════════════════

class SenseNovaClient:
    """Lightweight DeepSeek chat API client (switched from SenseNova)."""
    API_URL = "https://api.deepseek.com/v1/chat/completions"
    MODEL = "deepseek-chat"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("DEEPSEEK_API_KEY", "")
        if not self.api_key:
            logger.warning("DEEPSEEK_API_KEY not set, LLM calls will fail")

    def chat(self, messages: list, temp: float = 0.7, max_tokens: int = 8192,
             retries: int = 3) -> str:
        """Call DeepSeek chat API with retry logic."""
        payload = json.dumps({
            "model": self.MODEL,
            "messages": messages,
            "temperature": temp,
            "max_tokens": max_tokens,
        }).encode("utf-8")

        for attempt in range(retries):
            try:
                req = urllib.request.Request(
                    self.API_URL, data=payload,
                    headers={
                        "Content-Type": "application/json",
                        "Authorization": f"Bearer {self.api_key}",
                    })
                with urllib.request.urlopen(req, timeout=180) as resp:
                    data = json.loads(resp.read().decode("utf-8"))
                if "choices" in data and data["choices"]:
                    return data["choices"][0]["message"]["content"]
                else:
                    raise ValueError(f"Unexpected API response: {data}")
            except Exception as e:
                logger.warning(f"DeepSeek call failed (attempt {attempt+1}/{retries}): {e}")
                if attempt < retries - 1:
                    import time
                    time.sleep(2 ** attempt)
        raise RuntimeError(f"DeepSeek API failed after {retries} retries")

    def extract_json(self, text: str) -> dict:
        """Try to extract JSON from LLM response text.
        Handles common LLM JSON errors: trailing commas, missing commas,
        single quotes, markdown fences, extra text."""
        raw = text
        # 1. Remove markdown code fences
        text = re.sub(r'```(?:json)?\s*\n?', '', text)
        text = re.sub(r'\n?```\s*', '', text)

        # 2. Find first { to last }
        start = text.find('{')
        end = text.rfind('}')
        if start == -1 or end == -1 or end <= start:
            raise ValueError(f"Cannot find JSON boundaries in response:\n{text[:500]}")
        text = text[start:end+1]

        # 3. Try parsing directly
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            logger.debug(f"Direct JSON parse failed: {e}, attempting repair...")

        # 4. Auto-fix common LLM JSON errors
        fixes = [
            # trailing commas in objects
            (r',\s*}', '}'),
            # trailing commas in arrays
            (r',\s*\]', ']'),
            # single quotes instead of double
            (r"'", '"'),
            # unquoted keys (like {key: value} instead of {"key": value})
            (r'([{,]) (\w+) :', r'\1 "\2" :'),
            # Python None/True/False
            ('None', 'null'),
            ('True', 'true'),
            ('False', 'false'),
        ]

        for pattern, replacement in fixes:
            try:
                fixed = re.sub(pattern, replacement, text)
                return json.loads(fixed)
            except json.JSONDecodeError:
                continue

        # 5. Try `json5`-like: strip comments, trailing commas manually
        # Strip // style comments
        text_no_comments = re.sub(r'//.*', '', text)
        try:
            return json.loads(text_no_comments)
        except json.JSONDecodeError:
            pass

        # Save for debug
        debug_path = Path("/tmp/arc_planner_parse_error.json")
        debug_path.write_text(raw[:10000], encoding="utf-8")
        raise ValueError(f"Cannot parse JSON after all fixes. Saved to {debug_path}")


# ═══════════════════════════════════════════════════════════════
#  DND 5e-aware Arc Planner
# ═══════════════════════════════════════════════════════════════

class DnDArcPlanner:
    """
    LLM-driven arc planner with DND 5e power reference.
    2-phase pipeline:
      Phase 1: Plan volumes (given Bible + final character build)
      Phase 2: Plan chapters per volume (volume-level plan → chapter list)
    """

    def __init__(self, project_dir: Path, llm: Optional[SenseNovaClient] = None):
        self.dir = Path(project_dir)
        self.llm = llm or SenseNovaClient()
        # Load bible
        from bible import BibleManager
        self.bible = BibleManager(project_dir)
        self._dnd_context = self._build_dnd_context()

    # ─── DND 5e context builder ───────────────────────────────

    def _world_locations_text(self) -> str:
        """Extract world location descriptions from bible.json dynamically."""
        try:
            bible_path = self.dir / "bible.json"
            if bible_path.exists():
                b = json.loads(bible_path.read_text(encoding="utf-8"))
                world_rules = b.get("world_rules", [])
                parts = []
                for r in world_rules:
                    name = r.get("name", "")
                    desc = r.get("description", "")
                    if not any(kw in name for kw in ["DND","职业","规则"]):
                        short = desc[:150].replace("\n", " ")
                        parts.append(f"- {name}: {short}")
                if parts:
                    return "\n".join(parts)
        except Exception as e:
            logger.warning(f"Failed to load bible locations: {e}")
        # Fallback locations (self-built Terran world)
        return (
            "- 灰港镇: 帝国北疆渔港小镇，主角故乡，有破浪者酒馆\n"
            "- 铁冠城: 北疆矿业重镇，有竞技场和佣兵公会\n"
            "- 辉光城: 帝国首都，七塔法师协会所在地\n"
            "- 北境冰原: 极北苦寒荒野，蛮族领地\n"
            "- 龙骨群岛: 古龙陨落之地，龙裔部落守护\n"
            "- 深渊裂隙: 西南炼狱山脉的恶魔通道"
        )

    def _build_dnd_context(self) -> str:
        """Build a DND 5e system reference string for the LLM prompt."""
        lines = [
            "## DND 5e 力量体系参考",
            "",
            "### Tier 等级分段",
        ]
        for tier, (lo, hi, desc) in DND5E_LEVEL_MILESTONES.items():
            lines.append(f"- {tier} ({lo}-{hi}): {desc}")
        lines += [
            "",
            "### 职业成长关键节点 (野蛮人 Barbarian)",
            "(包含作者设定的史诗级扩展至29级)",
        ]
        for lvl, feat in DND5E_CLASS_PROGRESSION["barbarian"].items():
            lines.append(f"- 野蛮人 {lvl}: {feat}")
        lines += [
            "- 野蛮人 21-25: 史诗狂怒 (Epic Rage) 每日可用 ∞, 狂怒+8伤害",
            "- 野蛮人 26-29: 远古狂龙 (Primal Dragon) 形态: 狂化后进入半龙形态",
            "",
            "### 职业成长关键节点 (术士 Sorcerer - 红龙血统)",
        ]
        for lvl, feat in DND5E_CLASS_PROGRESSION["sorcerer"].items():
            lines.append(f"- 术士 {lvl}: {feat}")
        lines += [
            "",
            "### 职业成长关键节点 (吟游诗人 Bard)",
        ]
        for lvl, feat in DND5E_CLASS_PROGRESSION["bard"].items():
            lines.append(f"- 诗人 {lvl}: {feat}")
        lines += [
            "",
            "### 场景等级参考 (CR与角色等级对应)",
            "- CR 0-4 = 等级1-4 (地精/狗头人/骷髅/强盗)",
            "- CR 5-10 = 等级5-10 (食人魔/巨魔/吸血鬼/年轻巨龙)",
            "- CR 11-16 = 等级11-16 (成年巨龙/恶魔/大魔鬼/巫妖)",
            "- CR 17-24 = 等级17-20 (远古巨龙/恶魔领主/神灵化身)",
            "- CR 25-30 = 史诗级 (恶魔王子/大魔鬼公爵/次级神)",
            "- CR 30+ = 半神级/万界级 (魅魔之主美坎修特 ≈ CR 35+)",
            "",
            "### 重要地点 (自建泰伦大陆)",
            "(以下地点来自圣经设定, 勿使用被遗忘的国度的地名)",
            f"{self._world_locations_text()}",
            "- 无底深渊: 无尽层数, 恶魔的巢穴, 第六十六层翡翠宫",
            "- 九层地狱: 魔鬼的国度, 严酷法律与契约",
            "- 星界: 银色虚空, 漂浮着神明遗迹与龙族宝库",
        ]
        return "\n".join(lines)

    def _build_bible_context(self) -> str:
        """Extract bible info into a prompt-friendly string."""
        b = self.bible.bible
        lines = [
            "## 小说设定",
            f"书名: {b.title or '(未命名)'}",
            f"Logline: {b.logline or '(无)'}",
            f"风格: {b.genre} / {b.subgenre or '(无子类)'}",
            f"基调: {b.tone or '(未设定)'}",
            f"主题: {b.theme or '(未设定)'}",
            f"视角: {b.pov or '第三人称有限'}",
            f"目标长度: {b.target_length or '(未设定)'}",
            "",
            "### 角色列表",
        ]
        for name, char in b.characters.items():
            lines.append(f"- {name} ({char.role}): {char.background}")
            if char.traits:
                lines.append(f"  特质: {', '.join(char.traits)}")
            if char.motivation:
                lines.append(f"  动机: {char.motivation}")
            if char.current_state:
                lines.append(f"  状态: {char.current_state}")

        lines += ["", "### 世界规则"]
        for rule in b.world_rules:
            lines.append(f"- {rule.name} ({rule.category}): {rule.description}")

        if b.arcs:
            lines += ["", "### 已有章/卷"]
            for a in b.arcs:
                lines.append(f"- 卷{a.number}: {a.name} ({len(a.chapters)}章)")

        return "\n".join(lines)

    # ─── Helper utilities ───────────────────────────────────────

    def _default_locations(self) -> List[str]:
        """Get default world locations from bible.json if available."""
        try:
            b = self.bible.bible
            rules = b.get("world_rules", [])
            names = [r["name"] for r in rules if "DND" not in r["name"]
                     and "规则" not in r["name"] and "设定" not in r["name"]]
            if len(names) >= 4:
                return names[:6]
        except Exception:
            pass
        return ["泰伦大陆主位面", "无底深渊", "九层地狱", "星界"]

    def _calc_word_target(self, chapter_num: int, total_chapters: int) -> int:
        """Vary word target by chapter position to avoid uniform length."""
        frac = chapter_num / total_chapters
        if frac > 0.85:  # Climax section
            return 5500
        elif frac > 0.70:  # Pre-climax build-up
            return 4500
        elif chapter_num == 1:  # Opening chapter
            return 5000
        elif chapter_num % 7 == 0:  # Twist/reveal chapters need more space
            return 4500
        elif chapter_num % 5 == 0:  # Minor climax
            return 5000
        elif chapter_num % 3 == 0:
            return 3500
        else:
            return 4000

    # ─── Phase 1: Volume-level planning ───────────────────────

    def plan_volumes(self,
                     total_volumes: int = 7,
                     total_chapters: int = 476,
                     total_words: int = 2000000,
                     final_build: str = "1级吟游诗人/10级红龙术士/29级野蛮人",
                     final_enemy: str = "魅魔之主美坎修特 (Malcanthet)",
                     locations: List[str] = None,
                     ) -> List[VolumePlan]:
        """Phase 1: Use LLM to plan volume-level outline."""
        if locations is None:
            locations = self._default_locations()

        system_prompt = (
            "你是DND 5e资深跑团主持人兼奇幻小说架构师。"
            "你的任务是根据小说设定，规划一部DND世界观长篇奇幻小说的卷级大纲。"
            "要求:\n"
            "1. 规划主角等级成长的合理节奏——每卷主角应提升特定等级, 最终达到指定面板\n"
            "2. 职业等级增长要符合DND 5e规则: 术士级数决定法术位, 野蛮人级数决定狂怒次数\n"
            "3. 核心场景(主位面/深渊/地狱/星界)合理分配到各卷\n"
            "4. 最终BOSS(魅魔之主美坎修特)应在卷6-7才正面出场, 前期通过梦境/低语埋伏笔\n"
            "5. 按照传统西幻「小人物卷入大时代→成长冒险→面对威胁→巅峰决战」的结构\n"
        )

        user_prompt = f"""请根据以下小说设定, 规划{total_volumes}卷的大纲。

{self._build_bible_context()}

{self._dnd_context}

最终要求:
- 总章节: {total_chapters}章 (每章约{total_words//total_chapters}字)
- 总字数: {total_words:,}字
- 最终角色面板: {final_build}
- 最终敌人: {final_enemy}
- 覆盖场景: {', '.join(locations)}
- 字数分配: 每卷字数应与重要性匹配, 高潮卷可更多, 过渡卷可精炼
- 不允许所有卷字数完全相同

请输出JSON格式, 结构如下:
{{
  "volumes": [
    {{
      "number": 1,
      "title": "卷名",
      "chapters": 章节数,
      "summary": "卷概要(300字)",
      "main_locations": ["地点1", "地点2"],
      "level_start": 起始等级,
      "level_end": 结束等级,
      "class_growth": ["职业 起始级→结束级"],
      "key_encounters": ["关键事件1", "关键事件2"],
      "character_arcs": ["角色弧线描述"],
      "climax_type": "高潮类型(battle/diplomacy/revelation/sacrifice)"
    }}
  ]
}}

注意:
- 卷1主角应是低等级(1-4级), 蛮子/诗人为主, 后期才觉醒术士血脉
- 术士等级提升集中在中卷(3-4卷), 对应DND术士强势期(火球术/龙翼)
- 野蛮人最终达到29级(含史诗扩展), 意味着最终2卷主角以蛮子为主体
- 每卷章节数要合理, 卷1-5章节数应多于卷6-7(高潮卷更精炼)
- 吟游诗人1级意味着主角只会最基本的吟唱/鼓舞/基础魔法
"""

        logger.info("Phase 1: LLM volume planning...")
        msg = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        response_text = self.llm.chat(msg, temp=0.6, max_tokens=8192)
        try:
            data = self.llm.extract_json(response_text)
        except ValueError as e:
            logger.error(f"LLM JSON parse failed, saving raw response for debug. {e}")
            debug_path = self.dir / "plans" / "phase1_raw_response.md"
            debug_path.parent.mkdir(parents=True, exist_ok=True)
            debug_path.write_text(response_text, encoding="utf-8")
            raise

        volumes = []
        for v in data.get("volumes", []):
            # Validate required fields
            if "level_start" not in v:
                # Try alternative keys
                lr = v.get("level_range", [1, 4])
                v["level_start"] = lr[0] if isinstance(lr, list) else 1
                v["level_end"] = lr[1] if isinstance(lr, list) else 4
            volumes.append(VolumePlan(
                number=v["number"],
                title=v["title"],
                chapters=v.get("chapters", total_chapters // total_volumes),
                word_count=v.get("chapters", total_chapters // total_volumes) * (total_words // total_chapters),
                summary=v.get("summary", ""),
                main_locations=v.get("main_locations", []),
                level_range=(v.get("level_start", 1), v.get("level_end", 4)),
                class_growth=v.get("class_growth", []),
                key_encounters=v.get("key_encounters", []),
                character_arcs=v.get("character_arcs", []),
                climax_type=v.get("climax_type", "battle"),
            ))

        logger.info(f"Phase 1 complete: {len(volumes)} volumes planned")
        return volumes

    # ─── Phase 2: Chapter-level planning per volume (batched) ──

    def plan_chapters_for_volume(self, volume: VolumePlan,
                                  batch_size: int = 10) -> List[ChapterPlan]:
        """
        Phase 2: Expand a VolumePlan into individual chapter plans via LLM.
        Uses batched requests (batch_size=10) to avoid LLM response truncation.
        """
        import time
        total = volume.chapters
        all_chapters: List[ChapterPlan] = []

        system_prompt = (
            "你是DND 5e奇幻小说大纲策划师。"
            "你的任务是根据一卷大纲, 将这一卷展开为详细的章节计划。"
            "每一章都要有: 标题(有文采的短标题, 5字以内)、内容概要(100-150字)、地点、主角等级区间、戏剧张力类型。"
            "确保章节之间有悬念钩子连接, 每3-5章设置一个小高潮。"
            "注意: 使用小说圣经中的地点名称, 不要使用被遗忘的国度的地名(绝冬城/深水城/博德之门)。"
            "字数分配要有差异: 铺垫章3000-3500字, 普通章4000-4500字, 高潮章5000-6000字。"
        )

        # Volume metadata block (used in every batch)
        vol_meta = (
            f"卷{volume.number}: {volume.title}\n"
            f"概要: {volume.summary}\n"
            f"主要场景: {' / '.join(volume.main_locations)}\n"
            f"等级范围: {volume.level_range[0]}→{volume.level_range[1]}级\n"
            f"职业成长: {'; '.join(volume.class_growth)}\n"
            f"关键战斗/事件: {'; '.join(volume.key_encounters)}\n"
            f"高潮类型: {volume.climax_type}\n"
        )

        num_batches = (total + batch_size - 1) // batch_size
        logger.info(f"Phase 2: Planning volume {volume.number} ({total} chapters, "
                    f"{num_batches} batches of up to {batch_size})...")

        for batch_idx in range(num_batches):
            start_ch = batch_idx * batch_size + 1
            end_ch = min(start_ch + batch_size - 1, total)
            batch_chapters = end_ch - start_ch + 1

            logger.info(f"  Batch {batch_idx+1}/{num_batches}: chapters {start_ch}–{end_ch} "
                        f"({batch_chapters} chapters)")

            # Build context from previous batch's last few chapters
            prev_context = ""
            if all_chapters:
                context_chs = all_chapters[-3:]  # last 3 for continuity
                prev_lines = []
                for cp in context_chs:
                    prev_lines.append(
                        f"  第{cp.number}章「{cp.title}」: {cp.summary[:80]}")
                prev_context = "已完成的上一批章节:\n" + "\n".join(prev_lines) + "\n\n"

            user_prompt = (
                f"请展开下列卷大纲中 **第{start_ch}章至第{end_ch}章** 的详细章节计划。\n\n"
                f"{vol_meta}\n"
                f"{prev_context}"
                f"当前批次范围: 第{start_ch}章 ~ 第{end_ch}章 (共{batch_chapters}章)\n"
                f"在卷中的位置: 第{start_ch}/{total}章之后\n\n"
                f"输出JSON格式:\n"
                f"{{\n"
                f"  \"chapters\": [\n"
                f"    {{\n"
                f"      \"number\": 1,\n"
                f"      \"title\": \"章节标题(5字以内)\",\n"
                f"      \"summary\": \"内容概要(100-150字)\",\n"
                f"      \"location\": \"场景地点\",\n"
                f"      \"scenes\": 3,\n"
                f"      \"dramatic_type\": \"buildup/climax/resolution/twist/reveal\",\n"
                f"      \"character_focus\": [\"角色1\", \"角色2\"]\n"
                f"    }}\n"
                f"  ]\n"
                f"}}\n\n"
                f"要求:\n"
                f"- 本批第1章要有力开场并衔接上一批结尾\n"
                f"- 章节间要有悬念钩子连接\n"
                f"- 如果本批包含卷最后一章(climax章), 需对应卷高潮\n"
                f"- 如果卷内等级跨越较大, 中间章节需要体现等级提升的关键时刻\n"
            )

            msg = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ]

            response_text = self.llm.chat(msg, temp=0.5, max_tokens=8192)

            try:
                data = self.llm.extract_json(response_text)
            except ValueError as e:
                logger.error(f"Phase 2 batch {batch_idx+1} JSON parse failed: {e}")
                # fallback: generate simple plans for this batch
                for i in range(start_ch, end_ch + 1):
                    all_chapters.append(ChapterPlan(
                        number=i,
                        title=f"第{i}章",
                        summary=f"{volume.title} 第{i}章",
                        location=volume.main_locations[0] if volume.main_locations else "未知",
                        word_target=self._calc_word_target(i, total),
                        scenes=4 if i == total else 3,
                        dramatic_type="resolution" if i == total else "buildup",
                    ))
                continue

            for ch in data.get("chapters", []):
                ch_num = ch.get("number", start_ch + len(all_chapters))
                all_chapters.append(ChapterPlan(
                    number=ch_num,
                    title=ch.get("title", f"第{ch_num}章"),
                    summary=ch.get("summary", ""),
                    location=ch.get("location",
                                    volume.main_locations[0] if volume.main_locations else "未知"),
                    word_target=ch.get("word_target",
                                       self._calc_word_target(ch_num, total)),
                    scenes=ch.get("scenes", 3),
                    dramatic_type=ch.get("dramatic_type", "buildup"),
                    character_focus=ch.get("character_focus", []),
                ))

            # Brief cooldown between batches
            time.sleep(1)

        logger.info(f"Volume {volume.number} Phase 2 complete: "
                    f"{len(all_chapters)}/{total} chapters planned")
        return all_chapters

    def _fallback_chapters(self, volume: VolumePlan) -> List[ChapterPlan]:
        """Fallback: generate a simple numbered chapter list if LLM fails.
        Uses bible locations and varied word targets."""
        logger.warning(f"Using fallback chapter plan for volume {volume.number}")
        default_loc = volume.main_locations[0] if volume.main_locations else "灰港镇"
        chapters = []
        for i in range(1, volume.chapters + 1):
            wt = self._calc_word_target(i, volume.chapters)
            if i == 1:
                dt = "buildup"
            elif i == volume.chapters:
                dt = "resolution"
            elif i % 7 == 0:
                dt = "twist"
            elif i % 5 == 0:
                dt = "climax"
            elif i % 3 == 0:
                dt = "reveal"
            else:
                dt = "buildup"
            chapters.append(ChapterPlan(
                number=i,
                title=f"第{i}章",
                summary=f"{volume.title} 第{i}章",
                location=default_loc,
                word_target=wt,
                scenes=4 if dt == "climax" else 3,
                dramatic_type=dt,
            ))
        return chapters

    # ─── Full Pipeline ─────────────────────────────────────────

    def _checkpoint_file(self) -> Path:
        return self.dir / "plans" / ".plan_checkpoint.json"

    def _load_checkpoint(self) -> set:
        """Load completed volume numbers from checkpoint."""
        ckpt = self._checkpoint_file()
        if ckpt.exists():
            try:
                data = json.loads(ckpt.read_text(encoding="utf-8"))
                return set(data.get("completed_volumes", []))
            except Exception:
                return set()
        return set()

    def _save_checkpoint(self, completed: set):
        ckpt = self._checkpoint_file()
        ckpt.parent.mkdir(parents=True, exist_ok=True)
        ckpt.write_text(json.dumps({
            "completed_volumes": sorted(list(completed)),
            "updated_at": datetime.now().isoformat(),
        }, ensure_ascii=False, indent=2), encoding="utf-8")

    def full_plan(self,
                  total_volumes: int = 7,
                  total_chapters: int = 476,
                  total_words: int = 2000000,
                  final_build: str = "1级吟游诗人/10级红龙术士/29级野蛮人",
                  final_enemy: str = "魅魔之主美坎修特",
                  locations: List[str] = None,
                  resume: bool = False,
                  ) -> FullNovelPlan:
        """
        Run full 2-phase planning pipeline with checkpoint resume support.

        Phase 1: Volume-level outline (LLM → phase1_volumes.json)
        Phase 2: Chapter-level plans per volume, SERIALLY (one per LLM call)
                with checkpoint resume. Each volume saved to volume_XX_plan.json.
        """

        b = self.bible.bible
        plans_dir = self.dir / "plans"
        plans_dir.mkdir(parents=True, exist_ok=True)

        # ════════════════════════════════════════════════
        #  Phase 1: Volume-level outline
        # ════════════════════════════════════════════════

        # Check if Phase 1 already done (for resume)
        phase1_path = plans_dir / "phase1_volumes.json"
        if resume and phase1_path.exists():
            logger.info("Resume mode: loading existing Phase 1 result")
            phase1_data = json.loads(phase1_path.read_text(encoding="utf-8"))
            vol_plans = []
            for v in phase1_data["volumes"]:
                vol_plans.append(VolumePlan(
                    number=v["number"],
                    title=v["title"],
                    chapters=v["chapters"],
                    word_count=v["word_count"],
                    summary=v.get("summary", ""),
                    main_locations=v.get("main_locations", []),
                    level_range=tuple(v.get("level_range", [1, 4])),
                    class_growth=v.get("class_growth", []),
                    key_encounters=v.get("key_encounters", []),
                    character_arcs=v.get("character_arcs", []),
                    climax_type=v.get("climax_type", "battle"),
                ))
        else:
            vol_plans = self.plan_volumes(
                total_volumes=total_volumes,
                total_chapters=total_chapters,
                total_words=total_words,
                final_build=final_build,
                final_enemy=final_enemy,
                locations=locations,
            )
            # Save Phase 1
            phase1_data = {
                "volumes": [asdict(v) for v in vol_plans],
                "generated_at": datetime.now().isoformat(),
            }
            phase1_path.write_text(
                json.dumps(phase1_data, ensure_ascii=False, indent=2), encoding="utf-8")
            logger.info(f"Phase 1 complete: {len(vol_plans)} volumes")

        # ════════════════════════════════════════════════
        #  Phase 2: Serial chapter-level plans
        #  with checkpoint resume
        # ════════════════════════════════════════════════

        all_chapter_plans: Dict[int, List[ChapterPlan]] = {}
        completed = self._load_checkpoint() if resume else set()

        if completed:
            logger.info(f"Resume: {len(completed)} volumes already completed: {sorted(completed)}")
            # Load completed volumes from saved files
            for vn in sorted(completed):
                vol_file = plans_dir / f"volume_{vn:02d}_plan.json"
                if vol_file.exists():
                    data = json.loads(vol_file.read_text(encoding="utf-8"))
                    loaded_chapters = []
                    for c in data["chapters"]:
                        loaded_chapters.append(ChapterPlan(
                            number=c["number"],
                            title=c["title"],
                            summary=c["summary"],
                            location=c.get("location", "未知"),
                            word_target=c.get("word_target", 4000),
                            scenes=c.get("scenes", 3),
                            dramatic_type=c.get("dramatic_type", "buildup"),
                            character_focus=c.get("character_focus", []),
                        ))
                    all_chapter_plans[vn] = loaded_chapters
                    logger.info(f"  Loaded volume {vn}: {len(loaded_chapters)} chapters from cache")

        for vol in vol_plans:
            vol_num = vol.number

            # Skip if already completed
            if vol_num in completed and vol_num in all_chapter_plans:
                continue

            logger.info(f"Phase 2: Planning volume {vol_num} ({vol.chapters} chapters)...")
            try:
                ch_plans = self.plan_chapters_for_volume(vol)
            except Exception as e:
                logger.error(f"Phase 2 failed for vol {vol_num}: {e}, using fallback")
                ch_plans = self._fallback_chapters(vol)

            all_chapter_plans[vol_num] = ch_plans

            # Save immediately — serial execution, each volume saved on completion
            vol_data = {
                "volume": asdict(vol),
                "chapters": [asdict(c) for c in ch_plans],
                "generated_at": datetime.now().isoformat(),
            }
            (plans_dir / f"volume_{vol_num:02d}_plan.json").write_text(
                json.dumps(vol_data, ensure_ascii=False, indent=2), encoding="utf-8")

            # Update checkpoint after each volume
            completed.add(vol_num)
            self._save_checkpoint(completed)

            logger.info(f"Volume {vol_num}: {len(ch_plans)} chapters planned, checkpoint saved")

        # Build final result
        plan = FullNovelPlan(
            title=b.title or "Untitled",
            logline=b.logline or "",
            total_volumes=len(vol_plans),
            total_chapters=total_chapters,
            total_words=total_words,
            volumes=vol_plans,
            chapter_plans=all_chapter_plans,
            final_character_sheet=final_build,
        )

        # Save full plan
        full_path = plans_dir / "full_novel_plan.json"
        plan.save(full_path)
        text_path = plans_dir / "full_novel_outline.md"
        text_path.write_text(plan.to_text(), encoding="utf-8")

        logger.info(f"Full plan saved: {full_path} / {text_path}")
        return plan


# ═══════════════════════════════════════════════════════════════
#  CLI (for testing from command line)
# ═══════════════════════════════════════════════════════════════

def main():
    import argparse
    parser = argparse.ArgumentParser(description="DND 5e LLM-driven arc planner")
    parser.add_argument("--dir", default="./my-novel", help="project directory")
    parser.add_argument("--volumes", type=int, default=7, help="number of volumes")
    parser.add_argument("--chapters", type=int, default=476, help="total chapters")
    parser.add_argument("--words", type=int, default=2000000, help="total word count")
    parser.add_argument("--build", default="1级吟游诗人/10级红龙术士/29级野蛮人")
    parser.add_argument("--enemy", default="魅魔之主美坎修特")
    parser.add_argument("--locations", nargs="+",
                        default=["泰伦大陆主位面", "无底深渊", "九层地狱", "星界"])
    args = parser.parse_args()

    planner = DnDArcPlanner(Path(args.dir))
    plan = planner.full_plan(
        total_volumes=args.volumes,
        total_chapters=args.chapters,
        total_words=args.words,
        final_build=args.build,
        final_enemy=args.enemy,
        locations=args.locations,
    )
    print(f"\n{'='*60}")
    print(f"大纲生成完成!")
    print(f"输出路径: {args.dir}/plans/full_novel_outline.md")
    print(f"共 {args.volumes}卷 | {args.chapters}章 | ~{args.words:,}字")
    for v in plan.volumes:
        print(f"  卷{v.number}: {v.title} ({v.chapters}章, 等级{v.level_range[0]}→{v.level_range[1]})")
    print(f"\n详细大纲已完整写入:\n  {args.dir}/plans/full_novel_outline.md")
    print("=" * 60)


if __name__ == "__main__":
    main()
