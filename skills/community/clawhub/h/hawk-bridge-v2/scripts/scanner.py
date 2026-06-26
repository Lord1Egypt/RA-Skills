# Product thinking scanner — depends on core, llm, memory, helpers
import json
import re
from pathlib import Path
from typing import Optional

from .core import *
from .llm import call_llm, get_openclaw_llm_config
from .memory import PersonaAwareMemory
from .helpers import sort_by_priority


@dataclass
class ProductThinkingFinding:
    """A product-level insight about what should evolve, not just what should be cleaned up."""
    description: str
    category: str
    evidence: list[str]
    impact_score: float
    suggested_direction: str
    file_path: str
    risk: RiskLevel = RiskLevel.MEDIUM
    why_now: str = ""


class ProductThinkingScanner:
    """
    v3.5: Scans the codebase from the persona's perspective.
    Asks: "还有什么不足, 有哪些地方可以优化, 使用体验如何？"
    Uses persona context + hawk preferences + learnings history.
    """

    def __init__(self, repos: list[Repository], config: dict,
                 recall_persona: str = "", memory_source: str = "auto") -> None:
        self.repos = repos
        self.config = config
        self.memory = PersonaAwareMemory(
            recall_persona=recall_persona, memory_source=memory_source
        )
        self.master_summary = self.memory.get_context_summary()
        self.hawk_prefs = self.memory.get_preferences()
        self.effective_persona = self.memory.context_persona
        self.learnings = self._load_learnings_context()

    def _load_learnings_context(self) -> str:
        """Build a context string from learnings history using persona's workspace."""
        try:
            learnings_dir = self.memory.workspace / ".learnings"
            approvals_file = learnings_dir / "approvals.json"
            rejections_file = learnings_dir / "rejections.json"
            approvals, rejections = [], []
            if approvals_file.exists():
                try:
                    approvals = json.loads(approvals_file.read_text(encoding="utf-8"))
                except Exception:
                    pass
            if rejections_file.exists():
                try:
                    rejections = json.loads(rejections_file.read_text(encoding="utf-8"))
                except Exception:
                    pass
            if not approvals and not rejections:
                return f"No learnings history yet for {self.effective_persona}."
            p = self.effective_persona
            parts = [f"【{p} 学习历史 / Learnings History】"]
            if rejections:
                parts.append(f"\n{p} 之前拒绝过的改动（共 {len(rejections)} 次）:")
                for r in rejections[-5:]:
                    parts.append(f"  - 拒绝: {r.get('description', '')[:80]} | 原因: {r.get('reason', '未说明')[:60]}")
            if approvals:
                parts.append(f"\n{p} 之前批准过的改动（共 {len(approvals)} 次）:")
                for a in approvals[-5:]:
                    parts.append(f"  - 批准: {a.get('description', '')[:80]}")
            return "\n".join(parts)
        except Exception:
            return f"No learnings history yet for {self.effective_persona}."

    def scan(self) -> list[ProductThinkingFinding]:
        all_findings: list[ProductThinkingFinding] = []
        print(f"[ProductThinkingScanner] Starting scan of {len(self.repos)} repos...")
        for repo in self.repos:
            if not repo.auto_monitor:
                continue
            repo_path = repo.resolve_path()
            if not repo_path.exists():
                continue
            findings = self._scan_key_files(repo)
            all_findings.extend(findings)
            learnings_findings = self._analyze_learnings_patterns(repo)
            all_findings.extend(learnings_findings)
        all_findings.sort(key=lambda f: f.impact_score, reverse=True)
        return all_findings

    def _scan_key_files(self, repo: Repository) -> list[ProductThinkingFinding]:
        findings: list[ProductThinkingFinding] = []
        repo_path = repo.resolve_path()
        priority_files: list[Path] = []
        for fp in [repo_path / "README.md", repo_path / "SOUL.md", repo_path / "AGENTS.md"]:
            if fp.exists():
                priority_files.append(fp)
        skill_dir = repo_path / "skills"
        if skill_dir.exists():
            for sd in skill_dir.glob("*"):
                md = sd / "SKILL.md"
                if md.exists():
                    priority_files.append(md)
        for script in list(repo_path.glob("scripts/*.py")) + list(repo_path.glob("*.py")):
            if script.exists():
                priority_files.append(script)
        for fp in priority_files:
            try:
                content = fp.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            rel = str(fp.relative_to(repo_path))
            if len(content) > 8000:
                content = content[:8000]
            finding = self._analyze_file_for_product_thinking(content, rel, repo)
            if finding:
                findings.append(finding)
        return findings

    def _analyze_file_for_product_thinking(
        self, content: str, file_path: str, repo: Repository
    ) -> Optional[ProductThinkingFinding]:
        config = get_openclaw_llm_config()
        if not config.get("api_key") or not config.get("base_url"):
            return None

        hawk_block = ""
        if self.hawk_prefs.get("disliked"):
            hawk_block += "\n\n主人不喜欢的东西（hawk-bridge 记忆）：\n" + "\n".join(
                f"  - {d}" for d in self.hawk_prefs["disliked"][:3]
            )
        if self.hawk_prefs.get("liked"):
            hawk_block += "\n\n主人喜欢的东西（hawk-bridge 记忆）：\n" + "\n".join(
                f"  - {l}" for l in self.hawk_prefs["liked"][:3]
            )
        if not hawk_block:
            hawk_block = "\n\n（无 hawk-bridge 偏好记忆）"

        system = (
            f"You are the CONTINUOUS IMPROVEMENT PARTNER for persona: {self.effective_persona}.\n\n"
            "IMPORTANT: For EVERY file you analyze, ask from this persona's perspective:\n"
            "\"还有什么不足, 有哪些地方可以优化, 使用体验如何？\"\n\n"
            f"【{self.effective_persona} 上下文】\n"
            f"{self.master_summary}\n"
            f"【{self.effective_persona} 偏好】\n"
            f"{hawk_block}\n"
            "【学习历史】\n"
            f"{self.learnings}\n\n"
            "Answer ONLY with a JSON object with keys: "
            "  insight (answer to the 3 questions above — max 150 chars, honest), "
            "  category (one of: user_complaint | friction_point | unused_feature | competitive_gap | stop_doing | add_feature), "
            "  impact (0.0 to 1.0), "
            "  evidence (array of 1-2 short text snippets that support this), "
            "  suggested_direction (one concrete next step, max 100 chars), "
            "  why_now (why this matters now, max 80 chars). "
            "If nothing significant is broken, return {\"insight\": \"\", \"category\": \"ok\", \"impact\": 0.0, \"evidence\": [], \"suggested_direction\": \"\", \"why_now\": \"\"}. "
            "Be honest. Prefer 'stop doing X' over 'add more features'."
        )
        lang = detect_language_from_path(file_path)
        prompt = (
            "IMPORTANT: Answer with ONLY a JSON object. No explanation.\n\n"
            f"File: {file_path}\n\n"
            f"Content (excerpt):\n```{lang}\n{content[:5000]}\n```\n\n"
            "请回答：还有什么不足, 有哪些地方可以优化, 使用体验如何？"
        )
        result = call_llm(prompt=prompt, system=system, model=config["model"],
                          base_url=config["base_url"], api_key=config["api_key"])
        if not result:
            return None
        try:
            parsed = json.loads(result)
        except json.JSONDecodeError:
            m = re.search(r'\{[^{}]*\}', result, re.DOTALL)
            if not m:
                return None
            try:
                parsed = json.loads(m.group())
            except Exception:
                return None
        insight = parsed.get("insight", "").strip()
        if not insight or parsed.get("category") == "ok" or parsed.get("impact", 0.0) == 0.0:
            return None
        return ProductThinkingFinding(
            description=insight,
            category=parsed.get("category", "user_complaint"),
            evidence=parsed.get("evidence", []),
            impact_score=float(parsed.get("impact", 0.5)),
            suggested_direction=parsed.get("suggested_direction", ""),
            why_now=parsed.get("why_now", ""),
            file_path=file_path,
            risk=RiskLevel.MEDIUM,
        )

    def _analyze_learnings_patterns(self, repo: Repository) -> list[ProductThinkingFinding]:
        findings: list[ProductThinkingFinding] = []
        learnings = load_learnings(persona=self.effective_persona)
        rejections = learnings.get("rejections", [])
        approvals = learnings.get("approvals", [])
        if not rejections:
            return findings
        reason_count: dict[str, int] = {}
        type_count: dict[str, int] = {}
        for r in rejections:
            reason = r.get("reason", "no reason given")[:80]
            desc = r.get("description", "")[:80]
            reason_count[reason] = reason_count.get(reason, 0) + 1
            type_count[desc] = type_count.get(desc, 0) + 1
        for reason, count in reason_count.items():
            if count >= 3:
                findings.append(ProductThinkingFinding(
                    description=(
                        f"STOP: This keeps getting rejected ({count}x) — '{reason}'. "
                        "Auto-evolve keeps trying the same thing. Rules need adjustment."
                    ),
                    category="stop_doing",
                    evidence=[f"Rejected {count} times: {reason}"],
                    impact_score=min(1.0, count * 0.2),
                    suggested_direction="Review full_auto_rules. This pattern keeps failing.",
                    why_now="Same rejection reason 3+ times — fix the rule now.",
                    file_path="auto-evolve config",
                    risk=RiskLevel.HIGH,
                ))
        for desc, count in type_count.items():
            if count >= 3:
                findings.append(ProductThinkingFinding(
                    description=(
                        f"Stop attempting this: '{desc}' — rejected {count} times. "
                        "The system keeps generating changes nobody wants."
                    ),
                    category="unused_feature",
                    evidence=[f"Rejected {count} times: {desc}"],
                    impact_score=min(1.0, count * 0.25),
                    suggested_direction="Add to learnings blocklist.",
                    why_now=f"Rejected {count}x — wastes resources on unwanted changes.",
                    file_path="auto-evolve learnings",
                    risk=RiskLevel.MEDIUM,
                ))
        approval_themes: dict[str, int] = {}
        for a in approvals:
            theme = a.get("description", "")[:50]
            approval_themes[theme] = approval_themes.get(theme, 0) + 1
        for theme, count in approval_themes.items():
            if count >= 5:
                findings.append(ProductThinkingFinding(
                    description=(
                        f"This type of change keeps getting approved ({count}x): '{theme}'. "
                        "Consider doing MORE of this automatically."
                    ),
                    category="add_feature",
                    evidence=[f"Approved {count} times: {theme}"],
                    impact_score=min(1.0, count * 0.15),
                    suggested_direction="Increase auto-execution of this category",
                    why_now=f"Approved {count}x — safe to auto-execute more.",
                    file_path="auto-evolve learnings",
                    risk=RiskLevel.LOW,
                ))
        return findings


def print_product_findings(findings: list[ProductThinkingFinding]) -> None:
    """Print product-level findings in a readable format."""
    if not findings:
        print(f"\n🎯 Product Evolution Insights: none (all clear — or LLM returned empty)")
        return
    print(f"\n🎯 Product Evolution Insights (from {len(findings)} finding(s)):")
    print("=" * 60)
    icons = {
        "user_complaint": "😤",
        "friction_point": "🛑",
        "unused_feature": "💤",
        "competitive_gap": "📊",
        "stop_doing": "🚫",
        "add_feature": "✨",
    }
    for i, f in enumerate(findings[:10], 1):
        icon = icons.get(f.category, "❓")
        impact_bar = "█" * int(f.impact_score * 10) + "░" * (10 - int(f.impact_score * 10))
        print(f"\n  {i}. {icon} [{f.category.replace('_', ' ').upper()}]")
        print(f"     {f.description}")
        if f.evidence:
            print(f"     Evidence: {' | '.join(str(e)[:60] for e in f.evidence[:2])}")
        print(f"     Impact: {impact_bar} {f.impact_score:.1f}")
        if f.suggested_direction:
            print(f"     → {f.suggested_direction}")
        if f.why_now:
            print(f"     ⏱ {f.why_now}")
        print(f"     File: {f.file_path}")
    if len(findings) > 10:
        print(f"\n  ... and {len(findings) - 10} more insights")
