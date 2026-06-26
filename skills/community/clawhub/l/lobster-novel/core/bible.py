#!/usr/bin/env python3
"""
lobster-novel: novel bible manager
"""
import json, re, logging
from pathlib import Path
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import List, Optional, Dict, Any


# ═══════════════════════════════════════════════════════════════
#  Data models
# ═══════════════════════════════════════════════════════════════

@dataclass
class Character:
    name: str
    role: str                # protagonist, supporting, antagonist
    age: int = 0
    traits: List[str] = field(default_factory=list)
    background: str = ""
    motivation: str = ""
    arc: str = ""            # growth arc description
    relationships: Dict[str, str] = field(default_factory=dict)  # name->type
    current_state: str = ""  # alive, injured, captured, etc.
    notes: str = ""

@dataclass
class WorldRule:
    name: str
    description: str
    category: str = "geography"  # magic, technology, society, geography

@dataclass
class ChapterSpec:
    number: int
    title: str = ""
    summary: str = ""
    pov: str = ""
    scene_beats: List[str] = field(default_factory=list)
    emotional_turn: str = ""
    new_info: List[str] = field(default_factory=list)
    hooks_planted: List[str] = field(default_factory=list)
    hooks_payoff: List[str] = field(default_factory=list)  # which hooks resolved

@dataclass
class Arc:
    number: int
    name: str = ""
    chapters: List[int] = field(default_factory=list)
    core_conflict: str = ""
    climax_chapter: int = 0

@dataclass
class NovelBible:
    title: str = ""
    logline: str = ""
    genre: str = ""
    subgenre: str = ""
    target_length: str = ""  # short, novella, long, web_serial
    tone: str = ""
    theme: str = ""
    pov: str = ""
    style_template: str = ""  # 当前使用的风格模板文件名
    available_style_templates: Dict[str, str] = field(default_factory=dict)  # 可用风格模板列表

    characters: Dict[str, Character] = field(default_factory=dict)
    world_rules: List[WorldRule] = field(default_factory=list)
    arcs: List[Arc] = field(default_factory=list)
    chapters: Dict[int, ChapterSpec] = field(default_factory=dict)

    # continuity
    current_arc: int = 1
    current_chapter: int = 0
    unresolved_hooks: List[Dict] = field(default_factory=list)
    continuity_risks: List[str] = field(default_factory=list)

    created_at: str = ""
    updated_at: str = ""


# ═══════════════════════════════════════════════════════════════
#  Bible manager
# ═══════════════════════════════════════════════════════════════

class BibleManager:
    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.bible_file = self.dir / "bible.json"
        self.templates_dir = self.dir / "templates"
        self.bible = self._load()

    def _find_style_kit_dir(self) -> Optional[Path]:
        """查找 writing-style-kit/templates 目录"""
        # 方案 1: lobster-novel 在 skills/ 下
        candidate = self.dir.parent / "writing-style-kit" / "templates"
        if candidate.exists():
            return candidate
        # 方案 2: lobster-novel 在 skills/lobster-novel 下
        candidate = self.dir.parent.parent / "writing-style-kit" / "templates"
        if candidate.exists():
            return candidate
        return None

    def load_style_template(self, template_name: str = None) -> Optional[str]:
        """加载风格模板内容"""
        if template_name is None:
            template_name = self.bible.style_template
        if not template_name:
            return None
        # 优先从本地 templates 目录查找
        template_path = self.templates_dir / template_name
        if template_path.exists():
            try:
                return template_path.read_text(encoding="utf-8")
            except Exception as e:
                logging.warning(f"读取风格模板失败 {template_path}: {e}")
                return None
        # 从 writing-style-kit 查找
        style_kit_dir = self._find_style_kit_dir()
        if style_kit_dir:
            template_path = style_kit_dir / template_name
            if template_path.exists():
                try:
                    return template_path.read_text(encoding="utf-8")
                except Exception as e:
                    logging.warning(f"读取风格模板失败 {template_path}: {e}")
                    return None
        logging.warning(f"风格模板未找到：{template_name}")
        return None

    def list_style_templates(self) -> Dict[str, str]:
        """列出所有可用风格模板（优先级：本地 > bible.json > 风格库）"""
        templates: Dict[str, str] = {}
        # 1. writing-style-kit（优先级最低）
        style_kit_dir = self._find_style_kit_dir()
        if style_kit_dir:
            for f in style_kit_dir.glob("*.md"):
                if f.name not in templates:
                    templates[f.name] = f"风格库：{f.name}"
        # 2. bible.json 配置（优先级中等）
        for name, desc in self.bible.available_style_templates.items():
            if name not in templates:
                templates[name] = desc
        # 3. 本地 templates 目录（优先级最高）
        if self.templates_dir.exists():
            for f in self.templates_dir.glob("*.md"):
                templates[f.name] = f"本地模板：{f.name}"
        return templates

    def set_style_template(self, template_name: str):
        """设置当前使用的风格模板（先验证存在）"""
        if self.load_style_template(template_name) is None:
            logging.warning(f"风格模板不存在，无法设置：{template_name}")
            return
        self.bible.style_template = template_name
        self.save()

    def _load(self) -> NovelBible:
        if self.bible_file.exists():
            try:
                data = json.loads(self.bible_file.read_text(encoding="utf-8"))
                return self._dict_to_bible(data)
            except Exception as e:
                logging.warning(f"bible load failed: {e}, returning fresh bible")
        return NovelBible(created_at=datetime.now().isoformat(),
                          updated_at=datetime.now().isoformat())

    def _dict_to_bible(self, d: dict) -> NovelBible:
        b = NovelBible(**{k: v for k, v in d.items()
                          if k not in ("characters", "world_rules", "arcs", "chapters")})
        b.characters = {k: Character(**v) for k, v in d.get("characters", {}).items()}
        b.world_rules = [WorldRule(**r) for r in d.get("world_rules", [])]
        b.arcs = [Arc(**a) for a in d.get("arcs", [])]
        b.chapters = {int(k): ChapterSpec(**v)
                      for k, v in d.get("chapters", {}).items()}
        b.unresolved_hooks = d.get("unresolved_hooks", [])
        b.continuity_risks = d.get("continuity_risks", [])
        if not b.created_at:
            b.created_at = datetime.now().isoformat()
        if not b.updated_at:
            b.updated_at = datetime.now().isoformat()
        return b

    def save(self):
        self.bible.updated_at = datetime.now().isoformat()
        d = asdict(self.bible)
        self.bible_file.write_text(
            json.dumps(d, ensure_ascii=False, indent=2),
            encoding="utf-8")

    # metadata
    def set_meta(self, **kwargs):
        for k, v in kwargs.items():
            if hasattr(self.bible, k):
                setattr(self.bible, k, v)

    # characters
    def add_character(self, char: Character):
        self.bible.characters[char.name] = char
        self.save()

    def get_character(self, name: str) -> Optional[Character]:
        return self.bible.characters.get(name)

    def update_character_state(self, name: str, state: str):
        c = self.bible.characters.get(name)
        if c:
            c.current_state = state
            self.save()

    # world
    def add_rule(self, rule: WorldRule):
        self.bible.world_rules.append(rule)
        self.save()

    # arcs
    def add_arc(self, arc: Arc):
        self.bible.arcs.append(arc)
        self.save()

    # chapters
    def add_chapter(self, spec: ChapterSpec):
        self.bible.chapters[spec.number] = spec
        self.bible.current_chapter = spec.number
        self.save()

    def get_chapter(self, n: int) -> Optional[ChapterSpec]:
        return self.bible.chapters.get(n)

    # hooks
    def plant_hook(self, chapter: int, description: str, expected_payoff: int):
        self.bible.unresolved_hooks.append({
            "planted_at": chapter,
            "description": description,
            "expected_payoff": expected_payoff,
            "status": "unresolved",
        })
        self.save()

    def payoff_hook(self, chapter: int, description: str):
        for h in self.bible.unresolved_hooks:
            if h["description"] == description and h["status"] == "unresolved":
                h["status"] = "resolved"
                h["resolved_at"] = chapter
        self.save()

    def check_hooks(self) -> List[str]:
        """Check for hooks overdue by 3+ chapters"""
        warnings = []
        for h in self.bible.unresolved_hooks:
            if h["status"] != "unresolved":
                continue
            due = h["expected_payoff"]
            overdue = self.bible.current_chapter - due
            if overdue >= 3:
                warnings.append(
                    f"hook overdue: '{h['description']}' "
                    f"(planted ch{h['planted_at']}, due ch{due}, "
                    f"past by {overdue} ch)")
        return warnings

    # continuity
    def add_continuity_risk(self, risk: str):
        self.bible.continuity_risks.append(risk)
        self.save()

    # ------------------------------------------------------------------
    # Contract-compatible methods  (used by SeedContract.from_bible)
    # ------------------------------------------------------------------

    def get_world_settings(self) -> dict[str, Any]:
        """Return world settings as a dict of rule_name → rule_detail."""
        return {
            r.name: {"description": r.description, "category": r.category}
            for r in self.bible.world_rules
        }

    def get_characters(self) -> dict[str, dict[str, Any]]:
        """Return characters as dict of id → character dict."""
        return {
            name: asdict(char) for name, char in self.bible.characters.items()
        }

    def get_plot_arcs(self) -> list[dict[str, Any]]:
        """Return plot arcs as list of dicts."""
        return [asdict(arc) for arc in self.bible.arcs]

    def get_rules(self) -> list[str]:
        """Return world rule descriptions as a flat string list."""
        return [r.description for r in self.bible.world_rules]

    def get_style_guidelines(self) -> list[str]:
        """Return style guidelines parsed from the active style template."""
        content = self.load_style_template()
        if content:
            lines = [
                l.strip() for l in content.split("\n")
                if l.strip() and not l.strip().startswith("#")
            ]
            return lines[:20]
        return [f"tone: {self.bible.tone}"] if self.bible.tone else []

    # ------------------------------------------------------------------
    # Convenience properties (so SeedContract.from_bible works with BibleManager)
    # ------------------------------------------------------------------

    @property
    def title(self) -> str:
        return self.bible.title

    @property
    def genre(self) -> str:
        return self.bible.genre

    @property
    def style_template(self) -> str:
        return self.bible.style_template

    # ------------------------------------------------------------------
    # Contract-compatible methods  (used by SeedContract.from_bible)
    # ------------------------------------------------------------------

    def get_summary(self) -> str:
        b = self.bible
        lines = [
            f"## {b.title or '(untitled)'}",
            f"Genre: {b.genre} / {b.subgenre}",
            f"Tone: {b.tone}  |  POV: {b.pov}",
            f"Progress: ch{b.current_chapter} / {len(b.chapters)} chapters written",
            f"Characters: {len(b.characters)}",
            f"Arcs: {len(b.arcs)}",
            f"Unresolved hooks: {sum(1 for h in b.unresolved_hooks if h['status']=='unresolved')}",
            f"Continuity risks: {len(b.continuity_risks)}",
        ]
        return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
#  CLI
# ═══════════════════════════════════════════════════════════════

def cli():
    import argparse
    parser = argparse.ArgumentParser(description="lobster-novel bible")
    parser.add_argument("--dir", default="./my-novel", help="project directory")
    parser.add_argument("--init", action="store_true", help="init new project")
    parser.add_argument("--status", action="store_true", help="show project status")
    parser.add_argument("--title", help="set novel title")
    args = parser.parse_args()

    mgr = BibleManager(Path(args.dir))

    if args.init:
        mgr.set_meta(title=args.title or "Untitled")
        print(f"init project: {args.dir}")
    elif args.status:
        print(mgr.get_summary())

if __name__ == "__main__":
    cli()