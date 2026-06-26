#!/usr/bin/env python3
"""
lobster-novel: writing pipeline coordinator
"""
import json, re, sys
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict

sys.path.insert(0, str(Path(__file__).parent))
from bible import BibleManager, Character, ChapterSpec, Arc
from continuity import ContinuityTracker, ChapterState


class Pipeline:
    """Orchestrates the novel writing pipeline.

    This is a stateless coordinator that:
    1. Reads project state (bible + continuity)
    2. Prepares writing context for the next chapter
    3. Validates generated output
    4. Updates state after writing
    """

    def __init__(self, project_dir: Path):
        self.dir = Path(project_dir)
        self.bible = BibleManager(self.dir)
        self.continuity = ContinuityTracker(self.dir)
        self._item_verifier = None

    @property
    def item_verifier(self):
        """Lazy-init SceneItemVerifier.
        Calls LLM to verify scene item plausibility before writing."""
        if self._item_verifier is None:
            from scene_items import SceneItemVerifier
            self._item_verifier = SceneItemVerifier(self.dir)
        return self._item_verifier

    def verify_scene_items(self, chapter_num: int, chapter_plan: dict):
        """Verify scene item plausibility before writing chapter.
        Returns SceneItemChecklist with verified items + rejected list."""
        return self.item_verifier.verify_chapter(chapter_num, chapter_plan)

    # ── Context Preparation ───────────────────────────────────

    def get_writing_context(self, chapter: Optional[int] = None) -> dict:
        """Prepare the context needed to write the next chapter"""
        b = self.bible.bible
        ch_n = chapter or (b.current_chapter + 1)

        # Bible summary
        bible_summary = (
            f"## {b.title}\n"
            f"Genre: {b.genre}/{b.subgenre}\n"
            f"Tone: {b.tone}  POV: {b.pov}\n"
            f"Theme: {b.theme}\n"
        )

        # Characters overview
        char_lines = []
        for c in b.characters.values():
            char_lines.append(
                f"- {c.name} ({c.role}): {c.current_state or 'alive'} | {c.background[:80]}")
        char_summary = "\n".join(char_lines) if char_lines else "none yet"

        # Plot context
        arcs = b.arcs
        plot_summary = (
            f"Current arc: {b.current_arc}\n"
            f"Total arcs: {len(arcs)}\n"
            f"Chapters written: {b.current_chapter}\n"
        )

        # Continuity context
        cont_summary = self.continuity.get_summary_for(max(ch_n - 1, 0))
        hook_status = self.continuity.get_hook_status()
        overdue_hooks = self.bible.check_hooks()

        # Chapter spec (if exists)
        spec = b.chapters.get(ch_n)

        return {
            "chapter": ch_n,
            "bible_summary": bible_summary,
            "characters": char_summary,
            "plot": plot_summary,
            "continuity": cont_summary or "first chapter",
            "hooks": hook_status,
            "overdue_hooks": overdue_hooks,
            "spec": {
                "title": spec.title if spec else "",
                "summary": spec.summary if spec else "",
                "scenes": spec.scene_beats if spec else [],
                "pov": spec.pov if spec else "",
                "emotional_turn": spec.emotional_turn if spec else "",
            } if spec else {},
        }

    def format_writing_prompt(self, ctx: dict) -> str:
        """Format the context into a writing prompt for the agent"""
        spec = ctx.get("spec", {})
        lines = [
            f"# Chapter {ctx['chapter']} Writing Brief",
            "",
            f"## Novel",
            ctx.get("bible_summary", ""),
            "",
            f"## Characters",
            ctx.get("characters", ""),
            "",
            f"## Plot Context",
            ctx.get("plot", ""),
            "",
            f"## Continuity (last chapters)",
            ctx.get("continuity", "first chapter"),
            "",
        ]
        if ctx.get("hooks"):
            lines += ["## Active Hooks", ctx["hooks"], ""]
        if ctx.get("overdue_hooks"):
            lines += ["## Overdue Hooks (resolve these!)"]
            lines += [f"- {h}" for h in ctx["overdue_hooks"]]
            lines.append("")
        if spec.get("title"):
            lines.append(f"## Chapter Spec")
            if spec.get("title"):
                lines.append(f"Title: {spec['title']}")
            if spec.get("summary"):
                lines.append(f"Summary: {spec['summary']}")
            if spec.get("scenes"):
                lines.append(f"Scenes:")
                lines.extend(f"- {s}" for s in spec["scenes"])
            if spec.get("pov"):
                lines.append(f"POV: {spec['pov']}")
            lines.append("")

        lines += [
            "## Requirements",
            "- Write ~2000-3000 words",
            "- Hook at chapter end",
            "- Advance at least one character arc",
            "- Pay off any overdue hooks if possible",
            "- Keep prose consistent with tone",
            "",
            "## Output:",
            "---",
            "# Chapter X: [Title]",
            "",
            "(chapter text here)",
            "---",
        ]
        return "\n".join(lines)

    # ── Post-Write Processing ─────────────────────────────────

    def process_chapter_output(self, chapter: int, text: str) -> dict:
        """Process generated chapter: validate + update state"""
        word_count = len(text.replace("\n", "").replace(" ", ""))
        # rough word count for Chinese: use character count
        char_count = len([c for c in text if '\u4e00' <= c <= '\u9fff'])

        result = {
            "chapter": chapter,
            "char_count": char_count,
            "total_chars": len(text),
            "word_count_est": word_count,
            "has_title": bool(re.search(r'^#\s+第.*章', text, re.M)),
            "has_hook": self._detect_hook(text),
            "continuity_risks": [],
        }
        return result

    def _detect_hook(self, text: str) -> bool:
        """Heuristic: check if last paragraph feels like a hook"""
        paras = [p for p in text.split("\n\n") if p.strip()]
        if not paras:
            return False
        last = paras[-1].strip()
        hook_indicators = ["?", "!", "突然", "竟然", "究竟", "谁", "什么", "...", "——"]
        return any(indicator in last for indicator in hook_indicators)

    def save_chapter(self, chapter: int, text: str, summary: str,
                     char_changes: dict, new_hooks: list, resolved: list):
        """Save chapter and update continuity"""
        output_dir = self.dir / "chapters"
        output_dir.mkdir(parents=True, exist_ok=True)

        # save chapter text
        out_file = output_dir / f"ch{chapter:03d}.md"
        out_file.write_text(text, encoding="utf-8")

        # update bible
        spec = self.bible.bible.chapters.get(chapter)
        if not spec:
            spec = ChapterSpec(number=chapter)
        self.bible.add_chapter(spec)

        # plant/payoff hooks
        for h_desc in new_hooks:
            self.bible.plant_hook(chapter, h_desc, chapter + 5)
        for h_desc in resolved:
            self.bible.payoff_hook(chapter, h_desc)

        # update characters
        for name, new_state in char_changes.items():
            self.bible.update_character_state(name, new_state)

        # continuity record
        state = ChapterState(
            chapter=chapter,
            summary=summary,
            changed_characters=char_changes,
            new_hooks=new_hooks,
            resolved_hooks=resolved,
        )
        self.continuity.append(state)

        return {
            "chapter": chapter,
            "file": str(out_file),
            "word_count": len(text),
        }

    # ── Review Prep ───────────────────────────────────────────

    def get_review_context(self, chapter: int) -> dict:
        """Prepare context for reviewing a chapter"""
        ch_file = self.dir / "chapters" / f"ch{chapter:03d}.md"
        if not ch_file.exists():
            return {"error": f"chapter {chapter} not found"}

        text = ch_file.read_text(encoding="utf-8")
        ctx = self.get_writing_context(chapter)
        return {
            "chapter": chapter,
            "text": text[:8000],
            "bible_summary": ctx.get("bible_summary", ""),
            "characters": ctx.get("characters", ""),
            "hooks": ctx.get("hooks", ""),
        }

    # ── 6-Stage Workflow ─────────────────────────────────────
    # Inspired by novel-writer-structure:
    #   Write → Self-check → Review → Score → Conflict Check → Polish → Revise

    def run_self_check(self, chapter: int, text: str) -> list:
        """Stage 1: Self-check — author's own quick review (static checks)."""
        from quality_check import QualityChecker
        report = QualityChecker.check_text(text, chapter)
        return report.issues

    def run_review_all(self, chapter: int, text: str) -> dict:
        """Stage 2: Full review — static + scorer + conflict checks."""
        from quality_check import QualityChecker
        from scorer import SixDimScorer
        from conflict_detector import ConflictDetector

        issues = []

        # Static quality
        report = QualityChecker.check_text(text, chapter)
        issues.extend(report.issues)

        # No-LLM check
        detector = ConflictDetector(self.dir)
        conflicts = detector.check_all(chapter, text)
        for c in conflicts:
            issues.append({
                "severity": c.severity,
                "role": "Storyteller",
                "category": c.category,
                "description": c.description,
                "suggestion": c.suggestion,
            })

        return {
            "issues": issues,
            "static_score": report.scores.get("static", 0),
            "conflicts": len(conflicts),
        }

    def run_scoring(self, text: str, bible_context: str = "") -> dict:
        """Stage 3: 6-dimension scoring (novel-evaluator-inspired)."""
        from scorer import SixDimScorer
        result = SixDimScorer.score_all(text, bible_context)
        return {
            "total": result.total,
            "avg": result.avg,
            "dimensions": {k: v.score for k, v in result.dimensions.items()},
        }

    def polish_text(self, text: str, profile: Optional[str] = None) -> str:
        """Stage 4: Polish — basic text-level improvements without LLM.
        Fixes: extra whitespace, inconsistent line breaks, dialog formatting.
        """
        # Strip trailing whitespace per line
        lines = [l.rstrip() for l in text.split("\n")]
        # Normalize multiple blank lines to at most one
        result = []
        blank_count = 0
        for l in lines:
            if not l.strip():
                blank_count += 1
                if blank_count <= 1:
                    result.append("")
            else:
                blank_count = 0
                result.append(l)
        # Fix dialog spacing: remove spaces between quote and text
        cleaned = "\n".join(result)
        cleaned = re.sub(r'"\s+', '"', cleaned)
        cleaned = re.sub(r'\s+"', '"', cleaned)
        cleaned = re.sub(r'[\u201c]\s+', '\u201c', cleaned)
        cleaned = re.sub(r'\s+[\u201d]', '\u201d', cleaned)
        return cleaned.strip()

    def revise_from_issues(self, text: str, issues: list) -> str:
        """Stage 5: Revise — apply simple P0 fixes automatically.
        This is a static revision (not LLM). For complex revisions,
        the user can invoke LLM-assisted revision.
        """
        # Only handle specific P0 patterns automatically
        p0_fixes = {
            r'http[s]?://': '(link removed)',
        }
        for pat, replacement in p0_fixes.items():
            text = re.sub(pat, replacement, text)
        return text

    def full_quality_gate(self, chapter: int, text: str,
                          bible_context: str = "") -> dict:
        """Run all 6 stages and return combined report.
        Stages: Self-check → Review → Score → Conflict Check → Polish → Revise
        """
        issues = self.run_self_check(chapter, text)
        review = self.run_review_all(chapter, text)
        scoring = self.run_scoring(text, bible_context)
        polished = self.polish_text(text)
        revised = self.revise_from_issues(polished, review.get("issues", []))

        p0_count = sum(1 for i in review.get("issues", []) if i.get("severity") == "P0")
        p1_count = sum(1 for i in review.get("issues", []) if i.get("severity") == "P1")

        return {
            "chapter": chapter,
            "original_len": len(text),
            "polished_len": len(polished),
            "revised_len": len(revised),
            "p0_count": p0_count,
            "p1_count": p1_count,
            "static_score": review.get("static_score", 0),
            "scoring": scoring,
            "conflicts": review.get("conflicts", 0),
            "issues": review.get("issues", [])[:10],
            "passed": p0_count == 0,
        }

    # ── Multi-Agent Pipeline ────────────────────────────────────
    # Inspired by 马良写作 7-Agent collaboration:
    #   Planner → Writer → Expander → Reviewer → Reviser → Polish → Audit

    def multi_agent_write(self, chapter_num: int, api_key: str = "",
                          template_name: str = "") -> dict:
        """Multi-stage writing pipeline with internal iteration.
        Stages: Plan → Write → Expand → Review → Revise → Polish
        """
        from chapters import ChapterGenerator
        gen = ChapterGenerator(api_key=api_key)
        if not gen.api_key:
            return {"error": "SENSENOVA_API_KEY not set"}

        from chapters import count_tokens, token_report

        ctx = self.get_writing_context(chapter_num)
        bible_context = ctx.get("bible_summary", "")
        result = {"chapter": chapter_num, "stages": [], "total_tokens": 0}

        # Stage 1: Planner — generate chapter outline/intent
        plan = self._agent_plan(gen, chapter_num, ctx, template_name)
        result["stages"].append({"stage": "plan", "output": plan[:100]})

        # Stage 2: Writer — write full chapter from plan
        text = self._agent_write(gen, chapter_num, ctx, plan)
        result["stages"].append({
            "stage": "write", "chars": len(text),
            "tokens": gen.last_tokens.get("total_tokens", 0),
        })
        result["total_tokens"] += gen.last_tokens.get("total_tokens", 0)

        # Stage 3: Quality check + auto-revise loop (max 2 iterations)
        for attempt in range(2):
            review_result = self.run_review_all(chapter_num, text)
            p0_issues = [i for i in review_result.get("issues", [])
                         if i.get("severity") == "P0"]
            if not p0_issues:
                break
            # Revise via LLM
            text = self._agent_revise(gen, chapter_num, text, p0_issues[:3])
            result["stages"].append({
                "stage": f"revise-{attempt + 1}",
                "p0_fixed": len(p0_issues),
                "tokens": gen.last_tokens.get("total_tokens", 0),
            })
            result["total_tokens"] += gen.last_tokens.get("total_tokens", 0)

        # Stage 4: Polish (static, no API)
        from chinese_typeset import ChineseTypeset
        polished = ChineseTypeset.clean_all(text)
        result["stages"].append({"stage": "polish", "chars": len(polished)})

        result["final_text"] = polished
        return result

    def _agent_plan(self, gen, chapter_num: int, ctx: dict,
                     template_name: str = "") -> str:
        """Stage 1: Planner — generate chapter intent/outline."""
        brief = ctx.get("bible_summary", "")[:500]
        chars = ctx.get("characters", "")[:300]
        hooks = ctx.get("hooks", "")

        template_hint = ""
        if template_name:
            from beat_sheet import get_template
            bs = get_template(template_name)
            if bs:
                beat = bs.get_beat_for_chapter(chapter_num)
                if beat:
                    template_hint = f"\nBeat: {beat.name}\nFunction: {beat.function}\nTone: {beat.emotional_tone}"

        system = "你是一名小说策划师。根据上下文生成章节规划（500字内）：核心冲突、场景顺序、角色动态、章节末钩子。"
        prompt = (
            f"# Chapter {chapter_num} Planning\n\n"
            f"## Novel Context\n{brief}\n\n"
            f"## Characters\n{chars}\n\n"
            f"## Hooks\n{hooks[:200]}\n"
            f"{template_hint}\n\n"
            "Output format:\n"
            "Core Conflict:（一句话）\n"
            "Scenes:（场景列表）\n"
            "Character Arcs:（角色变化）\n"
            "End Hook:（章节末钩子）"
        )
        return gen._call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ], temp=0.5, max_tokens=1024)

    def _agent_write(self, gen, chapter_num: int, ctx: dict,
                      plan: str) -> str:
        """Stage 2: Writer — generate full chapter from plan."""
        bible = ctx.get("bible_summary", "")[:800]
        chars = ctx.get("characters", "")[:400]
        cont = ctx.get("continuity", "")[:400]

        system = "你是一名优秀的中文网文作者。根据章节规划和圣经，创作完整的章节内容。"
        prompt = (
            f"# Chapter {chapter_num}\n\n"
            f"## Bible\n{bible}\n\n"
            f"## Characters\n{chars}\n\n"
            f"## Continuity\n{cont}\n\n"
            f"## Plan\n{plan}\n\n"
            "Requirements:\n"
            "- 2000-3000字\n"
            "- 章节末留钩子\n"
            "- 推进至少一个角色弧\n"
            "- 自然过渡\n\n"
            "Output:\n"
            f"# Chapter {chapter_num}: [Title]\n\n(text)"
        )
        return gen._call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ], temp=0.7, max_tokens=4096)

    def _agent_revise(self, gen, chapter_num: int, text: str,
                       issues: list) -> str:
        """Stage 3+: Reviser — fix specific issues via LLM."""
        if not issues:
            return text
        issue_text = "\n".join(
            f"- [{i.get('severity','P1')}] {i.get('description','')[:80]}"
            for i in issues[:3])

        system = "你是一名小说修订编辑。针对提出的问题修改章节内容。保持原文风格和情节，只改问题区域。"
        prompt = (
            f"## Issues to Fix\n{issue_text}\n\n"
            f"## Chapter Text\n{text[:5000]}\n\n"
            "输出修改后的完整章节文本："
        )
        return gen._call_api([
            {"role": "system", "content": system},
            {"role": "user", "content": prompt},
        ], temp=0.3, max_tokens=4096)

    def quality_summary(self, chapter: int, text: str,
                        bible_context: str = "") -> str:
        """Human-readable quality gate summary."""
        result = self.full_quality_gate(chapter, text, bible_context)
        lines = [
            f"# Chapter {chapter} Quality Gate",
            f"",
            f"## Static Score: {result['static_score']}/100",
            f"## 6-Dim Score: {result['scoring']['avg']}/100",
            f"   Total: {result['scoring']['total']}/600",
            f"",
            f"## Issues",
            f"   P0 (must fix): {result['p0_count']}",
            f"   P1 (recommend): {result['p1_count']}",
            f"   Conflicts: {result['conflicts']}",
            f"",
            f"## Polish",
            f"   Original: {result['original_len']} chars",
            f"   Polished: {result['polished_len']} chars",
            f"   Revised:  {result['revised_len']} chars",
            f"",
        ]
        if result['passed']:
            lines.append("## Result: PASS ✅")
        else:
            lines.append(f"## Result: FAIL ({result['p0_count']} P0 issues) ❌")
            for i in result["issues"][:5]:
                if i.get("severity") == "P0":
                    lines.append(f"  - {i.get('description','')[:60]}")
        return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="lobster-novel pipeline")
    parser.add_argument("--dir", default="./my-novel", help="project dir")
    parser.add_argument("--context", type=int, help="get writing context for chapter")
    parser.add_argument("--prompt", type=int, help="get writing prompt for chapter")
    args = parser.parse_args()

    pipe = Pipeline(Path(args.dir))

    if args.context:
        ctx = pipe.get_writing_context(args.context)
        print(json.dumps(ctx, ensure_ascii=False, indent=2))
    elif args.prompt:
        ctx = pipe.get_writing_context(args.prompt)
        print(pipe.format_writing_prompt(ctx))
