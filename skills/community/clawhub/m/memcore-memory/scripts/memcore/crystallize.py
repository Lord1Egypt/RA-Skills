"""
Skill Crystallization: 高价值模式自动结晶为 Skill 建议。

对标 MemOS Skill: 当 L2 pattern 的频率/置信度超过阈值时，
自动生成 Skill 创建/更新建议。
"""

import json
import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Optional


@dataclass
class CrystallizationSuggestion:
    """一条 Skill 结晶建议"""
    pattern_id: int
    pattern_name: str
    skill_name: str                    # 建议的 skill 名称
    action: str                        # 建议动作: create / update / merge
    reason: str                        # 原因
    template_content: str              # 建议的 SKILL.md 内容模板
    confidence: float                  # 结晶置信度
    existing_skill_path: str = ""      # 已有 skill 路径（update/merge 时）
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())


class SkillCrystallizer:
    """从 L2 patterns 自动生成 Skill 创建/更新建议"""

    CRYSTALLIZE_THRESHOLD = 3          # 模式至少出现3次
    CONFIDENCE_THRESHOLD = 0.7         # 置信度至少0.7

    def __init__(
        self,
        pattern_db: str = None,
        workspace_root: str = None,
    ):
        if pattern_db is None:
            pattern_db = Path.home() / ".openclaw" / "pattern_index.db"
        self.pattern_db_path = Path(pattern_db)

        if workspace_root is None:
            workspace_root = Path.home() / ".openclaw" / "workspace"
        self.workspace_root = Path(workspace_root)

    def scan_candidates(self) -> list[CrystallizationSuggestion]:
        """扫描所有 patterns，生成结晶建议"""
        patterns = self._get_eligible_patterns()
        if not patterns:
            return []

        suggestions = []
        existing_skills = self._list_existing_skills()

        for p in patterns:
            # 检查是否已有对应 skill
            matched_skill = self._match_existing_skill(p, existing_skills)

            if matched_skill:
                suggestion = self._suggest_update(p, matched_skill)
            else:
                suggestion = self._suggest_create(p)

            if suggestion and suggestion.confidence >= self.CONFIDENCE_THRESHOLD:
                suggestions.append(suggestion)

        suggestions.sort(key=lambda s: -s.confidence)
        return suggestions

    def _get_eligible_patterns(self) -> list[dict]:
        """获取达到结晶阈值的 patterns"""
        if not self.pattern_db_path.exists():
            return []

        with sqlite3.connect(str(self.pattern_db_path)) as conn:
            conn.row_factory = sqlite3.Row
            rows = conn.execute(
                """SELECT * FROM patterns 
                   WHERE frequency >= ? 
                   AND confidence >= ? 
                   AND crystallized = 0 
                   ORDER BY frequency DESC""",
                (self.CRYSTALLIZE_THRESHOLD, self.CONFIDENCE_THRESHOLD)
            ).fetchall()
            return [dict(r) for r in rows]

    def _list_existing_skills(self) -> dict[str, dict]:
        """列出已有 skills"""
        skills = {}
        skills_dir = self.workspace_root / "skills"
        if not skills_dir.exists():
            return skills

        for skill_dir in skills_dir.iterdir():
            if not skill_dir.is_dir():
                continue
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                continue

            try:
                content = skill_md.read_text(encoding="utf-8")
            except Exception:
                continue

            # 解析 frontmatter
            name = skill_dir.name
            description = ""
            for line in content.split("\n"):
                if line.startswith("description:"):
                    description = line.replace("description:", "").strip().strip('"')
                    break

            skills[name] = {
                "path": str(skill_dir),
                "description": description,
                "content": content,
            }

        return skills

    def _match_existing_skill(self, pattern: dict, skills: dict) -> Optional[dict]:
        """匹配 pattern 到已有 skill（按标签/名称重叠度）"""
        pattern_tags = set(json.loads(pattern.get("tags", "[]")))
        pattern_name = pattern.get("name", "").lower()

        for skill_name, skill_info in skills.items():
            skill_text = f"{skill_name} {skill_info['description']}".lower()

            # 标签匹配
            for tag in pattern_tags:
                if tag.lower() in skill_text:
                    return skill_info

            # 名称关键词匹配
            for word in pattern_name.split():
                if len(word) > 2 and word in skill_text:
                    return skill_info

        return None

    def _suggest_create(self, pattern: dict) -> Optional[CrystallizationSuggestion]:
        """建议创建新 skill"""
        name = pattern.get("name", "")
        desc = pattern.get("description", "")
        solution = pattern.get("solution_template", "")
        tags = json.loads(pattern.get("tags", "[]"))
        freq = pattern.get("frequency", 0)

        # 生成 skill 名称
        skill_slug = self._name_to_slug(name)
        skill_title = name.replace("[", "(").replace("]", ")")

        # 生成模板内容
        template = self._generate_skill_template(
            skill_title=skill_title,
            description=desc,
            solution=solution,
            tags=tags,
            frequency=freq,
        )

        return CrystallizationSuggestion(
            pattern_id=pattern["id"],
            pattern_name=name,
            skill_name=skill_slug,
            action="create",
            reason=f"模式出现 {freq} 次，置信度 {pattern.get('confidence', 0):.0%}，尚无对应 Skill",
            template_content=template,
            confidence=pattern.get("confidence", 0.7),
        )

    def _suggest_update(self, pattern: dict, skill: dict) -> Optional[CrystallizationSuggestion]:
        """建议更新已有 skill"""
        solution = pattern.get("solution_template", "")
        freq = pattern.get("frequency", 0)

        # 检查已有 skill 是否已包含此 pattern 的解决方案
        if solution and solution[:100] in skill.get("content", ""):
            return None  # 已包含，无需更新

        return CrystallizationSuggestion(
            pattern_id=pattern["id"],
            pattern_name=pattern.get("name", ""),
            skill_name=Path(skill["path"]).name,
            action="update",
            reason=f"模式出现 {freq} 次，已有 Skill 缺少此模式，建议补充",
            template_content=self._generate_update_patch(solution, skill),
            confidence=pattern.get("confidence", 0.7) * 0.8,
            existing_skill_path=skill["path"],
        )

    # --------- Template Generation ---------

    def _generate_skill_template(
        self,
        skill_title: str,
        description: str,
        solution: str,
        tags: list[str],
        frequency: int,
    ) -> str:
        """生成 SKILL.md 模板"""
        tag_line = ", ".join(tags) if tags else "auto-generated"
        return f"""---
name: {skill_title}
description: "{description}"
version: 0.1.0
tags: [{tag_line}]
auto_crystallized: true
source_pattern_frequency: {frequency}
created_at: {datetime.now().isoformat()}
---

# {skill_title}

## 来源
自动从 {frequency} 次重复模式中结晶生成。

## 模式描述
{description}

## 解决方案
{solution or '（待填充）'}

## 使用场景
- 当遇到以下情况时触发此 Skill：
{chr(10).join(f'  - {tag}' for tag in tags) if tags else '  - （从模式标签推导）'}

## 注意事项
- 此 Skill 由 MemCore 自动生成，请根据实际使用情况完善
- 可通过反馈机制继续优化此 Skill
"""

    def _generate_update_patch(self, solution: str, skill: dict) -> str:
        """生成 skill 更新补丁"""
        return f"""## 自动建议补充 (MemCore)

以下内容建议追加到此 Skill 中:

### 新发现的解决方案
{solution}

### 建议添加的注意事项
- 此模式最近频繁出现，建议提升优先级
"""

    @staticmethod
    def _name_to_slug(name: str) -> str:
        """模式名称 → skill slug"""
        import re
        slug = name.lower()
        slug = re.sub(r'[\[\]]', '', slug)
        slug = re.sub(r'[^a-z0-9\u4e00-\u9fff]+', '-', slug)
        slug = slug.strip('-')
        return slug[:50]


# --------- Feedback-Triggered Check ---------

def check_crystallization_on_feedback(
    trace_id: int,
    trace_db: str = None,
) -> list[CrystallizationSuggestion]:
    """当某个 trace 收到反馈后，检查其所属 patterns 是否达到结晶阈值"""
    if trace_db is None:
        trace_db = Path.home() / ".openclaw" / "trace_index.db"

    # 读 trace 的 tags
    with sqlite3.connect(str(Path(trace_db))) as conn:
        conn.row_factory = sqlite3.Row
        row = conn.execute("SELECT * FROM traces WHERE id = ?", (trace_id,)).fetchone()
        if not row:
            return []

    # 重新运行模式归纳 + 结晶扫描
    from .pattern import PatternInducer
    inducer = PatternInducer(trace_db)
    inducer.induce()

    crystallizer = SkillCrystallizer()
    return crystallizer.scan_candidates()
