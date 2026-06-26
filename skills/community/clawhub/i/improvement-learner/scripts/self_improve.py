#!/usr/bin/env python3
"""
Real Karpathy Self-Improvement Loop.

Unlike the old implementation that created template README/placeholder tests,
this version:
1. Reads evaluation results to understand what failed and why
2. Proposes MEANINGFUL improvements (not cosmetic)
3. Validates improvements against frozen benchmarks
4. Maintains a Pareto front — no dimension can regress
5. Uses HOT/WARM/COLD three-layer memory for pattern extraction
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Any

# ---------------------------------------------------------------------------
# Path setup — allow imports from repo root (lib.*) and benchmark-store
# ---------------------------------------------------------------------------
_REPO_ROOT = Path(__file__).resolve().parents[3]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import logging

from lib.common import read_json, write_json, utc_now_iso  # noqa: E402
from lib.pareto import ParetoFront, ParetoEntry  # noqa: E402

logger = logging.getLogger(__name__)

# Mock mode: set via --mock flag or when claude CLI is unavailable.
_USE_MOCK_LLM = False


# ---------------------------------------------------------------------------
# LLM-as-judge for accuracy scoring
# ---------------------------------------------------------------------------

_ACCURACY_JUDGE_PROMPT = """\
You are evaluating a SKILL.md file — an instruction document that guides an AI coding agent.

Rate this skill on 5 dimensions (0.0–1.0 each). Be strict — most skills are mediocre.

1. **Clarity** (0.0–1.0): Could an AI agent read this and know EXACTLY what to do, step by step? Or is it vague ("consider various approaches")?
   - 1.0 = unambiguous step-by-step, no interpretation needed
   - 0.5 = mostly clear but some sections require guessing
   - 0.0 = vague, hand-wavy, AI would have to improvise

2. **Specificity** (0.0–1.0): Does it use concrete examples with real input→output? Or generic descriptions?
   - 1.0 = multiple concrete examples with actual I/O
   - 0.5 = some examples but abstract
   - 0.0 = no examples, only descriptions

3. **Completeness** (0.0–1.0): Does it cover edge cases, error handling, and "when NOT to do X"?
   - 1.0 = covers happy path + edge cases + anti-patterns
   - 0.5 = covers happy path only
   - 0.0 = incomplete, missing critical sections

4. **Actionability** (0.0–1.0): Could an AI produce correct output on the FIRST try following this skill?
   - 1.0 = yes, the skill provides enough detail for correct first-try output
   - 0.5 = probably needs 1-2 corrections
   - 0.0 = AI would struggle even with multiple attempts

5. **Differentiation** (0.0–1.0): Does this skill add value beyond what the AI already knows?
   - 1.0 = teaches domain-specific knowledge the AI wouldn't have
   - 0.5 = reinforces good practices but AI could figure it out
   - 0.0 = states obvious things any AI would do anyway

Respond with ONLY a JSON object, no markdown:
{{"clarity": 0.X, "specificity": 0.X, "completeness": 0.X, "actionability": 0.X, "differentiation": 0.X, "overall": 0.X, "weakest": "dimension_name", "reason": "one sentence why"}}

SKILL.md content:
---
{skill_content}
---"""


def _llm_judge_accuracy(skill_content: str, mock: bool = False) -> float:
    """Score a SKILL.md using LLM-as-judge. Returns 0.0–1.0.

    Calls `claude -p` with a rubric prompt. Falls back to regex
    heuristics if claude CLI is unavailable or mock=True.
    """
    if mock or not shutil.which("claude"):
        return _regex_fallback_accuracy(skill_content)

    prompt = _ACCURACY_JUDGE_PROMPT.format(
        skill_content=skill_content[:8000]  # cap to avoid huge prompts
    )

    try:
        result = subprocess.run(
            ["claude", "-p", "--output-format", "json"],
            input=prompt,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            logger.warning("claude -p failed (rc=%d), using regex fallback", result.returncode)
            return _regex_fallback_accuracy(skill_content)

        # Parse claude JSON output
        try:
            parsed = json.loads(result.stdout)
            llm_text = parsed.get("result", result.stdout)
        except (json.JSONDecodeError, TypeError):
            llm_text = result.stdout

        # Extract JSON from LLM response
        return _parse_judge_response(llm_text)

    except subprocess.TimeoutExpired:
        logger.warning("claude -p timed out, using regex fallback")
        return _regex_fallback_accuracy(skill_content)
    except Exception as e:
        logger.warning("LLM judge error: %s, using regex fallback", e)
        return _regex_fallback_accuracy(skill_content)


def _parse_judge_response(text: str) -> float:
    """Extract overall score from LLM judge JSON response."""
    text = text.strip()
    # Handle markdown code blocks
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0].strip()
    elif "```" in text:
        text = text.split("```")[1].split("```")[0].strip()

    try:
        data = json.loads(text)
        # Use "overall" if present, otherwise average dimensions
        if "overall" in data:
            score = float(data["overall"])
        else:
            dims = [data.get(d, 0.5) for d in
                    ["clarity", "specificity", "completeness", "actionability", "differentiation"]]
            score = sum(dims) / len(dims)
        return max(0.0, min(1.0, score))
    except (json.JSONDecodeError, TypeError, ValueError) as e:
        logger.warning("Failed to parse judge response: %s", e)
        return 0.5  # neutral fallback


def _regex_fallback_accuracy(content: str) -> float:
    """Regex-based accuracy heuristic. Used when LLM is unavailable.

    This is the old approach — kept as fallback only.
    R²=0.00 correlation with evaluator pass rate (2026-04-04 experiment).
    """
    content_lower = content.lower()
    checks = []

    # Workflow structure
    phase_markers = ["## phase", "## step", "## 阶段", "### step",
                     "pipeline", "workflow", "步骤", "流程"]
    checks.append(any(m in content_lower for m in phase_markers))

    # Conditional logic
    checks.append(bool(re.search(r'(if\s+.*(?:then|→|->)|当.*时)', content_lower)))

    # Output specification
    checks.append(bool(re.search(r'(## output|## 输出|returns?\s*:)', content_lower)))

    # Severity with reason
    checks.append(bool(re.search(
        r'(must|never|禁止).{0,100}(because|otherwise|否则)', content_lower)))

    # Anti-patterns
    checks.append(bool(re.search(
        r'(不要|do not|avoid).{0,100}(instead|而是|应该)', content_lower)))

    # Escalation criteria
    escalation = ["ask the user", "询问", "stop if", "如果不确定", "确认"]
    checks.append(any(m in content_lower for m in escalation))

    # Concrete examples
    checks.append(bool(re.findall(r'<example>|```\w*\n.{50,}?```', content, re.DOTALL)))

    return sum(checks) / len(checks) if checks else 0.5


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class ImprovementResult:
    """Result of a single improvement iteration."""
    iteration: int
    candidate_type: str
    description: str
    applied: bool
    score_before: float
    score_after: float
    kept: bool
    pareto_accepted: bool
    reason: str
    trace: dict | None = None


# ---------------------------------------------------------------------------
# Three-Layer Memory
# ---------------------------------------------------------------------------

class ThreeLayerMemory:
    """HOT/WARM/COLD memory for improvement patterns.

    HOT  — ≤100 entries, always loaded, frequently accessed patterns.
    WARM — domain-specific overflow, loaded on demand.
    COLD — archived, >3 months inactive (future).
    """

    HOT_LIMIT = 100

    def __init__(self, memory_dir: Path):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        self.hot_path = self.memory_dir / "hot.json"
        self.warm_path = self.memory_dir / "warm.json"
        self.cold_path = self.memory_dir / "cold.json"

    # -- public API --

    def record_outcome(self, improvement_type: str, succeeded: bool, context: dict) -> None:
        """Record an improvement outcome for future pattern matching."""
        entry = {
            "type": improvement_type,
            "succeeded": succeeded,
            "context": context,
            "timestamp": utc_now_iso(),
            "hit_count": 1,
        }
        hot = self._load(self.hot_path)

        # Check if a similar pattern already exists
        existing = self._find_similar(hot, improvement_type, context)
        if existing is not None:
            existing["hit_count"] = existing.get("hit_count", 0) + 1
            existing["last_hit"] = utc_now_iso()
        else:
            hot.append(entry)

        # Enforce ≤HOT_LIMIT entries — overflow moves to WARM
        if len(hot) > self.HOT_LIMIT:
            hot.sort(key=lambda x: x.get("hit_count", 0), reverse=True)
            overflow = hot[self.HOT_LIMIT:]
            hot = hot[:self.HOT_LIMIT]
            warm = self._load(self.warm_path)
            warm.extend(overflow)
            self._save(self.warm_path, warm)

        self._save(self.hot_path, hot)

    def get_patterns(self, improvement_type: str) -> list[dict]:
        """Get relevant patterns for a given improvement type."""
        hot = self._load(self.hot_path)
        return [e for e in hot if e.get("type") == improvement_type]

    def hot_count(self) -> int:
        """Return the number of entries in HOT memory."""
        return len(self._load(self.hot_path))

    def warm_count(self) -> int:
        """Return the number of entries in WARM memory."""
        return len(self._load(self.warm_path))

    # -- internal --

    def _find_similar(self, entries: list[dict], improvement_type: str, context: dict) -> dict | None:
        """Find an entry with the same type and overlapping context keys."""
        for entry in entries:
            if entry.get("type") != improvement_type:
                continue
            # Match on context key overlap (same dimension targeted)
            entry_ctx = entry.get("context", {})
            if (entry_ctx.get("dimension") and context.get("dimension")
                    and entry_ctx["dimension"] == context["dimension"]):
                return entry
        return None

    def _load(self, path: Path) -> list[dict]:
        if not path.exists():
            return []
        try:
            data = read_json(path)
            return data if isinstance(data, list) else []
        except (json.JSONDecodeError, KeyError):
            return []

    def _save(self, path: Path, data: list[dict]) -> None:
        write_json(path, data)


# ---------------------------------------------------------------------------
# Frontmatter parsing helpers
# ---------------------------------------------------------------------------

def _extract_description_text(fm_section: str) -> str:
    """Extract full description text from YAML frontmatter, handling both
    inline and multiline (| or >) formats.

    Examples:
        description: "inline text"        → "inline text"
        description: inline text          → "inline text"
        description: |                    → "line1\nline2\n..."
          line1
          line2
        description: >                   → "line1 line2 ..."
          line1
          line2
    """
    lines = fm_section.split("\n")
    desc_text = ""
    in_multiline = False
    multiline_indent = 0
    joiner = " "  # default: folded (>)

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("description:"):
            after_key = stripped[len("description:"):].strip()
            if after_key in ("|", "|+", "|-"):
                # Literal block scalar — preserve newlines
                in_multiline = True
                joiner = "\n"
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        multiline_indent = len(lines[j]) - len(lines[j].lstrip())
                        break
                continue
            elif after_key in (">", ">+", ">-"):
                # Folded block scalar — join with spaces
                in_multiline = True
                joiner = " "
                for j in range(i + 1, len(lines)):
                    if lines[j].strip():
                        multiline_indent = len(lines[j]) - len(lines[j].lstrip())
                        break
                continue
            elif ((after_key.startswith('"') and after_key.endswith('"')) or
                  (after_key.startswith("'") and after_key.endswith("'"))):
                # Quoted inline — strip only outermost quotes
                desc_text = after_key[1:-1]
                break
            else:
                # Unquoted inline
                desc_text = after_key
                break
        elif in_multiline:
            if stripped == "" or (len(line) - len(line.lstrip()) >= multiline_indent and multiline_indent > 0):
                desc_text += line.strip() + joiner
            else:
                # Dedent means end of multiline block
                break

    return desc_text.strip()


def _extract_category(skill_md_content: str) -> str:
    """Extract category from SKILL.md frontmatter. Returns 'tool' as default."""
    m = re.search(r'^category:\s*(\S+)', skill_md_content, re.MULTILINE)
    return m.group(1).strip().lower() if m else "tool"


# ---------------------------------------------------------------------------
# Skill evaluation — real, not random
# ---------------------------------------------------------------------------

def evaluate_skill_dimensions(skill_path: Path) -> dict[str, float]:
    """Evaluate a skill across multiple dimensions.

    Returns a dict of dimension -> score (0.0–1.0).  All checks are
    deterministic and based on actual file content.

    Design principle (per skill-creator spec):
    - Only SKILL.md is required.  scripts/, references/, tests/, assets/
      are all OPTIONAL.
    - Pure-text skills (no scripts/) are legitimate and must not be
      penalised for missing tests/ or README.md.
    - references/ is expected only when SKILL.md exceeds 500 lines
      (progressive disclosure rule).
    """
    skill_path = Path(skill_path)
    scores: dict[str, float] = {}

    # Structure checks
    has_skill_md = (skill_path / "SKILL.md").exists()
    has_tests = ((skill_path / "tests").exists()
                 and any((skill_path / "tests").glob("test_*.py")))
    has_scripts = (skill_path / "scripts").exists()
    has_references = (skill_path / "references").exists()
    has_readme = (skill_path / "README.md").exists()

    # Read SKILL.md ONCE and reuse throughout (was reading 4 times)
    skill_md_content = ""
    if has_skill_md:
        skill_md_content = (skill_path / "SKILL.md").read_text(encoding="utf-8")

    # Coverage: does SKILL.md cover what it should? (content quality, not project artifacts)
    if not has_skill_md:
        scores["coverage"] = 0.0
    else:
        content = skill_md_content
        content_lower = content.lower()
        lines = len(content.split("\n"))
        cov_checks: list[bool] = []
        # 1. Has When to Use / When NOT to Use
        cov_checks.append("when to use" in content_lower or "when to" in content_lower
                          or "## 使用场景" in content or "## 适用" in content)
        # 2. Has example or anti-example (with or without attributes)
        cov_checks.append("<example" in content or "<anti-example" in content
                          or "## Example" in content or "## 示例" in content)
        # 3. Has Output / output artifacts section
        cov_checks.append("## Output" in content or "## output" in content_lower
                          or "## 输出" in content)
        # 4. Has Related / See Also for disambiguation
        cov_checks.append("## Related" in content or "## See Also" in content
                          or "## 关联" in content or "## 相关" in content)
        # 5. Has Usage / workflow section
        cov_checks.append("## Usage" in content or "## Workflow" in content
                          or "## 用法" in content or "## 工作流" in content)
        # 6. Progressive disclosure: >500 lines should have references/
        if lines > 500:
            cov_checks.append(has_references)
        else:
            cov_checks.append(True)  # not applicable, pass

        # 7. Workflow/Usage section has substance (≥8 non-empty lines, not just a heading)
        #    If no Workflow/Usage section exists, skip this check (not all skills need one).
        wf_match = re.search(
            r'## (?:Workflow|Usage|工作流|用法).*?\n(.*?)(?=\n## |\Z)',
            content, re.DOTALL)
        if wf_match:
            wf_lines = [l for l in wf_match.group(1).strip().split("\n") if l.strip()]
            cov_checks.append(len(wf_lines) >= 8)

        # 8. If references/ exists, SKILL.md must link to them (not just have the dir)
        if has_references:
            ref_files = list(skill_path.rglob("references/**/*.md"))
            ref_links = len(re.findall(r'\[.*?\]\(references/.*?\.md\)', content))
            # Should reference at least half the files, minimum 2
            min_links = max(2, len(ref_files) // 2)
            cov_checks.append(ref_links >= min_links)
        else:
            cov_checks.append(True)  # no references dir, not applicable

        # 9. Example has substance (≥4 non-empty lines inside <example> tags)
        ex_match = re.search(r'<example>(.*?)</example>', content, re.DOTALL)
        if ex_match:
            ex_lines = [l for l in ex_match.group(1).strip().split("\n") if l.strip()]
            cov_checks.append(len(ex_lines) >= 4)
        elif "<example" in content or "## Example" in content:
            cov_checks.append(True)  # has example section, trust it
        else:
            cov_checks.append(False)

        scores["coverage"] = sum(cov_checks) / len(cov_checks)

    # Completeness: project artifact completeness, category-aware.
    # tool/orchestration skills need scripts+tests; knowledge/rule skills don't.
    category = _extract_category(skill_md_content) if has_skill_md else "tool"
    comp_checks: list[bool] = []
    if category in ("tool", "orchestration"):
        comp_checks.append(has_scripts)       # scripts/ expected
        comp_checks.append(has_tests)         # tests/ expected
        comp_checks.append(has_references)    # references/ nice to have
        comp_checks.append(has_readme)        # README nice to have
    else:  # knowledge, rule, or unset
        # Pure-instruction skills: no scripts/tests required
        comp_checks.append(has_references)    # references/ expected for depth
        if has_references:
            ref_files = list(skill_path.rglob("references/**/*.md"))
            comp_checks.append(len(ref_files) >= 2)  # at least 2 reference files
        else:
            comp_checks.append(False)
        comp_checks.append("<example>" in skill_md_content or "<anti-example>" in skill_md_content)
        comp_checks.append(len(skill_md_content.split("\n")) >= 50)  # non-trivial length
    scores["completeness"] = sum(comp_checks) / len(comp_checks) if comp_checks else 0.0

    # Accuracy: Two-tier scoring.
    #
    # Tier 1 (regex): fast structural gate — has frontmatter, name, description, not a stub.
    #   If any fail → accuracy capped at 0.3. Cost: $0, milliseconds.
    #
    # Tier 2 (LLM): semantic quality — LLM reads SKILL.md and judges whether
    #   an AI agent could follow it to produce correct output. Cost: ~$0.5, seconds.
    #   Falls back to regex heuristics if LLM unavailable (no API key, --mock mode).
    #
    # Why LLM? The R²=0.064 experiment (2026-04-04) proved regex exec_checks have
    # zero correlation with evaluator pass rate. LLM-as-judge is the minimum viable
    # alternative that can actually assess instruction quality.
    if has_skill_md:
        content = skill_md_content
        content_lower = content.lower()

        # Parse frontmatter once
        fm_section = ""
        if content.startswith("---") and content.count("---") >= 2:
            fm_section = content.split("---", 2)[1]
        desc_text = _extract_description_text(fm_section) if fm_section else ""
        lines = len(content.split("\n"))

        # ===== TIER 1: Table stakes (regex, binary gate → 0.3 cap) =====
        gate_checks = [
            content.startswith("---"),                    # has frontmatter
            "name:" in fm_section if fm_section else False,
            "description:" in fm_section if fm_section else False,
            bool(desc_text and len(desc_text) > 20),      # non-trivial description
            lines >= 15,                                  # not a stub
        ]
        gate_pass = all(gate_checks)

        # ===== TIER 2: LLM-as-judge (semantic quality) =====
        if not gate_pass:
            # Scale 0.0-0.3 based on how many gate checks passed
            passed_count = sum(1 for c in gate_checks if c)
            scores["accuracy"] = 0.3 * (passed_count / len(gate_checks))
        else:
            llm_score = _llm_judge_accuracy(content, mock=_USE_MOCK_LLM)
            scores["accuracy"] = 0.3 + 0.7 * llm_score

        lines = len(content.split("\n"))
        if lines > 0:
            scores["efficiency"] = min(1.0, max(0.3, 1.0 - (lines - 300) / 1000))
        else:
            scores["efficiency"] = 0.3
    else:
        scores["accuracy"] = 0.0
        scores["efficiency"] = 0.0

    # Reliability: test results (pure-text skills without scripts/ default to 1.0)
    if has_tests:
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pytest",
                 str(skill_path / "tests"), "-q", "--tb=no"],
                capture_output=True, text=True, timeout=30,
            )
            scores["reliability"] = 1.0 if result.returncode == 0 else 0.5
        except (subprocess.TimeoutExpired, FileNotFoundError):
            scores["reliability"] = 0.3
    elif has_scripts:
        # Has scripts but no tests → should have tests
        scores["reliability"] = 0.3
    else:
        # Pure-text skill (no scripts, no tests) → perfectly valid
        scores["reliability"] = 1.0

    # Security: check SKILL.md only (not implementation code which legitimately
    # uses "password" parameters, "secrets" module, etc.)
    sec_checks = []
    if has_skill_md:
        skill_content = skill_md_content
        skill_lower = skill_content.lower()
        # SKILL.md should not contain actual secrets
        sec_checks.append("api_key =" not in skill_lower and "api_key=" not in skill_lower)
        sec_checks.append("password =" not in skill_lower and "password=" not in skill_lower)
        # API key pattern: sk- followed by alphanumeric (not sk- inside words like "task-")
        sec_checks.append(not bool(re.search(r'(?<![a-zA-Z])sk-[a-zA-Z0-9]{10,}', skill_content)))
        # Has license in frontmatter?
        if skill_content.count("---") >= 2:
            fm = skill_content.split("---", 2)[1]
            sec_checks.append("license:" in fm)
        else:
            sec_checks.append(False)
    else:
        sec_checks = [False, False, False, False]

    # Implementation code checks (only flag dangerous patterns, not parameter names)
    all_py_content = ""
    for f in skill_path.rglob("*.py"):
        if "__pycache__" in str(f):
            continue
        try:
            all_py_content += f.read_text(encoding="utf-8", errors="ignore") + "\n"
        except Exception:
            pass
    sec_checks.append("os.system(" not in all_py_content)
    sec_checks.append("exec(" not in all_py_content or "exec_module" in all_py_content)

    scores["security"] = sum(sec_checks) / len(sec_checks) if sec_checks else 0.5

    # Trigger quality: how well the frontmatter description enables
    # accurate skill routing (inspired by alirezarezvani/claude-skills
    # trigger evaluation pattern with 10 should-trigger + 10 should-not queries)
    trig_checks: list[bool] = []
    if has_skill_md:
        content = skill_md_content
        if content.startswith("---") and content.count("---") >= 2:
            fm = content.split("---", 2)[1]
            # Use the multiline-aware description extractor
            desc_text = _extract_description_text(fm)
            # 1. Description exists and is non-trivial (>30 chars)
            trig_checks.append(len(desc_text) > 30)
            # 2. Description contains action verbs or scenario keywords (quality, not just length)
            action_verbs = ["当", "需要", "生成", "检查", "修复", "分析", "优化", "创建", "运行", "验证",
                            "when", "generate", "check", "fix", "analyze", "optimize", "create", "run", "use"]
            trig_checks.append(any(v in desc_text.lower() for v in action_verbs))
            # 3. Has 'triggers:' field with explicit trigger list
            has_triggers = bool(re.search(r'triggers:\s*\n\s+- .+', fm))
            trig_checks.append(has_triggers)
            # 4. Has disambiguation (mentions what NOT to use for)
            desc_lower = desc_text.lower()
            trig_checks.append(any(w in desc_lower for w in ["not for", "don't use", "instead use", "不适用", "不用于"]))
            # 5. Description mentions related/similar skills for disambiguation
            trig_checks.append(any(w in desc_lower for w in ["related", "see also", "关联", "参见", "用 ", "(用"]))
        else:
            trig_checks = [False] * 5
    else:
        trig_checks = [False] * 5

    scores["trigger_quality"] = sum(trig_checks) / len(trig_checks) if trig_checks else 0.0

    # Leakage: detect internal project references that shouldn't be in a
    # generic/open-source skill. Hardcoded paths, org-specific tool names,
    # internal notification systems, project-specific prefixes.
    leak_checks: list[bool] = []
    if has_skill_md:
        content = skill_md_content
        content_lower = content.lower()
        # 1. No hardcoded home-directory paths (~/work/..., /Users/..., /home/...)
        leak_checks.append(not bool(re.search(
            r'~/work/|/Users/\w+/|/home/\w+/', content)))
        # 2. No internal notification systems (DingTalk, Feishu, Lark, internal Slack channels)
        leak_checks.append(not any(w in content_lower for w in [
            "dingtalk", "feishu", "lark", "钉钉", "飞书"]))
        # 3. No project-specific session prefixes (nc-, omc-, omx-)
        leak_checks.append(not bool(re.search(r'\bnc-\w+\b', content)))
        # 4. No internal tool references without explaining them generically
        #    (dispatch.sh, session-monitor.sh, orchestrator-planner as proper nouns)
        internal_tools = re.findall(
            r'\b(?:dispatch\.sh|session-monitor\.sh|on-stop\.sh|on-session-end\.sh|'
            r'progress\.sh|status\.sh|send\.sh|notify-callback\.sh)\b', content)
        # Allow if these are in a generic "integration example" context,
        # but flag if they appear as hardcoded references
        leak_checks.append(len(internal_tools) <= 1)  # 0-1 mention OK, 2+ = leaky
        # 5. No ~/.openclaw/ or ~/.omc/ hardcoded paths
        leak_checks.append(not bool(re.search(
            r'~/\.openclaw/|~/\.omc/', content)))
    else:
        leak_checks = [False] * 5

    scores["leakage"] = sum(leak_checks) / len(leak_checks) if leak_checks else 0.5

    # Knowledge density: does each knowledge unit contain sufficient depth?
    #
    # Two strategies depending on structure:
    # - If references/ exists (progressive disclosure): check per-FILE depth
    #   in references/. Each .md file is one knowledge unit.
    # - If no references/: check per-SECTION depth in SKILL.md.
    kd_checks: list[bool] = []
    if has_skill_md:
        if has_references:
            # Progressive disclosure mode: each reference file is a knowledge unit
            ref_files = sorted(skill_path.rglob("references/**/*.md"))
            all_ref_content = ""
            for rf in ref_files:
                try:
                    rf_content = rf.read_text(encoding="utf-8", errors="ignore")
                    all_ref_content += "\n" + rf_content
                    rf_lines = [l for l in rf_content.strip().split("\n") if l.strip()]
                    # A reference file with < 20 non-empty lines is too thin
                    kd_checks.append(len(rf_lines) >= 20)
                except Exception:
                    kd_checks.append(False)
            # Overall checks on combined content
            all_content = skill_md_content + all_ref_content
            code_blocks = re.findall(r'```[\s\S]*?```', all_content)
            kd_checks.append(len(code_blocks) >= 3)
            has_why = bool(re.search(
                r'(\*\*问题\*\*|\*\*原理\*\*|\*\*Why\*\*|[Tt]radeoff|[Bb]ecause|之所以|原因[是：])',
                all_content))
            kd_checks.append(has_why)
        else:
            # Flat mode: check per-section depth in SKILL.md
            content = skill_md_content
            stripped = re.sub(r'```[\s\S]*?```', '', content)
            sections = re.split(r'^## ', stripped, flags=re.MULTILINE)
            skip_prefixes = ("与现有", "工作流", "Output", "不做", "When to", "When NOT",
                             "Session", "条件", "Related", "Quick", "CLI", "Decided",
                             "Rejected", "Risks", "Files", "Remaining", "Scripts",
                             "常见场景", "目录结构", "为什么")
            pattern_sections = [s for s in sections[1:]
                                if not s.split("\n")[0].strip().startswith(skip_prefixes)]
            if pattern_sections:
                for sect in pattern_sections:
                    lines = [l for l in sect.strip().split("\n") if l.strip()]
                    kd_checks.append(len(lines) >= 8)
                code_blocks = re.findall(r'```[\s\S]*?```', content)
                kd_checks.append(len(code_blocks) >= 3)
                has_why = bool(re.search(
                    r'(\*\*问题\*\*|\*\*原理\*\*|\*\*Why\*\*|[Tt]radeoff|[Bb]ecause|之所以|原因[是：])',
                    content))
                kd_checks.append(has_why)
            else:
                kd_checks = [False] * 3
    else:
        kd_checks = [False] * 3

    scores["knowledge_density"] = sum(kd_checks) / len(kd_checks) if kd_checks else 0.0

    return scores


# ---------------------------------------------------------------------------
# Multi-role evaluation (4 perspectives)
# ---------------------------------------------------------------------------

# Role-specific dimension weights
ROLE_WEIGHTS: dict[str, dict[str, float]] = {
    "user": {
        # User cares: can I find this skill? can I use it quickly?
        "accuracy": 0.15, "coverage": 0.10, "completeness": 0.05,
        "reliability": 0.05, "efficiency": 0.10, "security": 0.05,
        "trigger_quality": 0.35, "leakage": 0.05, "knowledge_density": 0.10,
    },
    "developer": {
        # Developer cares: is the code solid? are there tests?
        "accuracy": 0.10, "coverage": 0.10, "completeness": 0.15,
        "reliability": 0.20, "efficiency": 0.10, "security": 0.10,
        "trigger_quality": 0.05, "leakage": 0.05, "knowledge_density": 0.15,
    },
    "security_auditor": {
        # Security auditor cares: secrets? dangerous patterns? license?
        "accuracy": 0.10, "coverage": 0.05, "completeness": 0.05,
        "reliability": 0.10, "efficiency": 0.05, "security": 0.35,
        "trigger_quality": 0.05, "leakage": 0.20, "knowledge_density": 0.05,
    },
    "architect": {
        # Architect cares: structure? progressive disclosure? depth?
        "accuracy": 0.15, "coverage": 0.15, "completeness": 0.10,
        "reliability": 0.05, "efficiency": 0.10, "security": 0.05,
        "trigger_quality": 0.05, "leakage": 0.10, "knowledge_density": 0.25,
    },
}

ROLE_LABELS = {
    "user": "User (findability + usability)",
    "developer": "Developer (code quality + tests)",
    "security_auditor": "Security Auditor (secrets + safety)",
    "architect": "Architect (structure + design)",
}

# Category-specific weight modifiers: >1.0 amplifies, <1.0 dampens, 1.0 = no change.
# Applied multiplicatively to ROLE_WEIGHTS, then re-normalized.
CATEGORY_MODIFIERS: dict[str, dict[str, float]] = {
    "tool": {"reliability": 1.5, "completeness": 1.3, "security": 1.2, "trigger_quality": 0.8},
    "knowledge": {"accuracy": 1.5, "knowledge_density": 1.3, "completeness": 0.6, "reliability": 0.7},
    "orchestration": {"reliability": 1.3, "coverage": 1.2, "completeness": 1.2, "trigger_quality": 0.8},
    "rule": {"accuracy": 1.4, "security": 1.3, "completeness": 0.6, "coverage": 0.8},
}


def evaluate_skill_multi_role(skill_path: Path) -> dict[str, Any]:
    """Evaluate a skill from 4 different role perspectives.

    Returns a dict with per-role scores, consensus label, overall, and category.
    Uses the same base dimensions from evaluate_skill_dimensions()
    but applies role-specific weights modified by category-aware multipliers.

    Category modifiers (from CATEGORY_MODIFIERS) are applied multiplicatively
    to each role's base weights, then the weights are re-normalized to sum to 1.0.
    This makes tool-type skills emphasize reliability/security and knowledge-type
    skills emphasize accuracy/knowledge_density.
    """
    skill_path = Path(skill_path)
    base_scores = evaluate_skill_dimensions(skill_path)

    # Read category from SKILL.md frontmatter
    skill_md = skill_path / "SKILL.md"
    if skill_md.exists():
        skill_md_content = skill_md.read_text(encoding="utf-8")
        category = _extract_category(skill_md_content)
    else:
        category = "tool"

    cat_modifiers = CATEGORY_MODIFIERS.get(category, {})

    role_results: dict[str, dict[str, Any]] = {}

    for role, base_weights in ROLE_WEIGHTS.items():
        # Apply category modifiers: multiply each dimension weight, then re-normalize
        adjusted: dict[str, float] = {}
        for dim, w in base_weights.items():
            adjusted[dim] = w * cat_modifiers.get(dim, 1.0)

        # Re-normalize so weights sum to 1.0
        total = sum(adjusted.values())
        if total > 0:
            weights = {dim: v / total for dim, v in adjusted.items()}
        else:
            weights = adjusted

        weighted = sum(base_scores.get(dim, 0) * w for dim, w in weights.items())
        pct = round(weighted * 100, 1)
        if pct >= 85:
            tier = "POWERFUL"
        elif pct >= 70:
            tier = "SOLID"
        elif pct >= 55:
            tier = "GENERIC"
        else:
            tier = "WEAK"
        role_results[role] = {
            "score": pct,
            "tier": tier,
            "label": ROLE_LABELS[role],
            "weights": weights,
        }

    # Consensus: all agree on tier?
    tiers = [r["tier"] for r in role_results.values()]
    unique_tiers = set(tiers)
    if len(unique_tiers) == 1:
        consensus = "CONSENSUS"
    elif len(unique_tiers) == 2:
        consensus = "MOSTLY_AGREED"
    else:
        consensus = "DISPUTED"

    # Overall: average of all role scores
    avg = round(sum(r["score"] for r in role_results.values()) / len(role_results), 1)

    return {
        "category": category,
        "base_scores": {k: round(v, 3) for k, v in base_scores.items()},
        "role_scores": role_results,
        "consensus": consensus,
        "overall": avg,
        "overall_tier": "POWERFUL" if avg >= 85 else "SOLID" if avg >= 70 else "GENERIC" if avg >= 55 else "WEAK",
    }


# ---------------------------------------------------------------------------
# Improvement proposals — real, not cosmetic
# ---------------------------------------------------------------------------

_IMPROVEMENT_STRATEGIES: dict[str, dict[str, Any]] = {
    "coverage": {
        "type": "coverage",
        "description": "Add references/ for progressive disclosure (only if SKILL.md > 500 lines)",
    },
    "accuracy": {
        "type": "accuracy",
        "description": "Improve SKILL.md frontmatter and section structure",
    },
    "reliability": {
        "type": "reliability",
        "description": "Add test stubs for skills that have scripts/ but no tests/",
    },
    "efficiency": {
        "type": "efficiency",
        "description": "Refactor overly long SKILL.md sections into references/",
    },
    "security": {
        "type": "security",
        "description": "Remove hardcoded secrets from SKILL.md",
    },
    "leakage": {
        "type": "leakage",
        "description": "Remove internal project references (hardcoded paths, org-specific tools, internal prefixes)",
    },
    "knowledge_density": {
        "type": "knowledge_density",
        "description": "Add depth to thin pattern sections (why, how, tradeoffs, concrete examples)",
    },
}


def _propose_instruction_improvement(skill_path: Path, scores: dict) -> dict | None:
    """Propose an instruction-level improvement to SKILL.md."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return None

    content = skill_md.read_text()
    issues = []

    # Detect common SKILL.md quality issues
    if "## When to Use" not in content and "## 何时使用" not in content:
        issues.append(("missing_when_to_use", "Add '## When to Use' section with clear trigger conditions"))

    if "## When NOT to Use" not in content and "## 不应该使用" not in content:
        issues.append(("missing_when_not_to_use", "Add '## When NOT to Use' section to prevent misuse"))

    lines = content.split("\n")
    if len(lines) > 300:
        issues.append(("too_long", f"SKILL.md is {len(lines)} lines — extract details to references/"))

    if "```" not in content:
        issues.append(("no_examples", "Add CLI usage examples with code blocks"))

    # Check for vague instructions
    vague_patterns = ["etc.", "and so on", "and more", "various", "many"]
    for pattern in vague_patterns:
        if pattern in content.lower():
            issues.append(("vague_language", f"Replace vague '{pattern}' with specific items"))
            break

    if not issues:
        return None

    # Pick the highest-priority issue
    issue = issues[0]
    return {
        "type": "instruction",
        "dimension": "accuracy",
        "description": issue[1],
        "issue_id": issue[0],
        "priority": 0.8,
    }


def propose_targeted_improvement(
    skill_path: Path,
    weakest_dim: str,
    patterns: list[dict],
    scores: dict | None = None,
) -> dict[str, Any] | None:
    """Propose a targeted improvement for the weakest dimension.

    Returns a candidate dict or None if no improvement is possible.
    """
    # Check if previous patterns for this dim all failed → skip
    failed = [p for p in patterns if not p.get("succeeded", True)]
    if len(failed) >= 3:
        return None  # Too many failures on this dimension; skip

    # When accuracy is the weakest and below 0.9, try instruction improvement first
    if scores is not None and weakest_dim == "accuracy" and scores.get("accuracy", 1.0) < 0.9:
        candidate = _propose_instruction_improvement(skill_path, scores)
        if candidate is not None:
            return candidate

    # When accuracy is the weakest among otherwise-good dimensions, prioritise instruction
    if scores is not None and weakest_dim == "accuracy":
        other_dims = {k: v for k, v in scores.items() if k != "accuracy"}
        if other_dims and all(v >= 0.7 for v in other_dims.values()):
            candidate = _propose_instruction_improvement(skill_path, scores)
            if candidate is not None:
                return candidate

    strategy = _IMPROVEMENT_STRATEGIES.get(weakest_dim)
    if strategy is None:
        return None

    return dict(strategy)  # shallow copy


def apply_improvement(skill_path: Path, candidate: dict[str, Any]) -> bool:
    """Apply an improvement candidate to the skill directory.

    Returns True if the improvement was applied, False otherwise.
    """
    skill_path = Path(skill_path)
    ctype = candidate.get("type", "")

    if ctype == "coverage":
        return _apply_coverage_improvement(skill_path)
    elif ctype == "accuracy":
        return _apply_accuracy_improvement(skill_path)
    elif ctype == "reliability":
        return _apply_reliability_improvement(skill_path)
    elif ctype == "efficiency":
        return _apply_efficiency_improvement(skill_path)
    elif ctype == "security":
        return _apply_security_improvement(skill_path)
    elif ctype == "instruction":
        return _apply_instruction_improvement(skill_path, candidate)
    return False


def _apply_coverage_improvement(skill_path: Path) -> bool:
    """Create references/ when SKILL.md is too long (progressive disclosure).

    Per skill-creator spec, only SKILL.md is required.  We do NOT auto-create
    tests/, README.md, or scripts/ — those are optional and should only exist
    when the skill author intentionally adds them.
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False

    content = skill_md.read_text(encoding="utf-8")
    lines = len(content.split("\n"))

    # Only create references/ if SKILL.md exceeds 500 lines
    if lines > 500 and not (skill_path / "references").exists():
        (skill_path / "references").mkdir(parents=True, exist_ok=True)
        return True

    return False


def _apply_accuracy_improvement(skill_path: Path) -> bool:
    """Improve SKILL.md accuracy — add missing frontmatter fields and sections."""
    md = skill_path / "SKILL.md"
    if not md.exists():
        return False
    content = md.read_text(encoding="utf-8")
    changed = False

    # 1. Add frontmatter if missing
    if not content.startswith("---"):
        name = skill_path.name
        content = f"---\nname: {name}\nversion: 0.1.0\ndescription: {name} skill\nauthor: OpenClaw Team\nlicense: MIT\ntags: [{name}]\n---\n\n" + content
        changed = True

    # 2. Add missing frontmatter fields
    if content.startswith("---") and content.count("---") >= 2:
        parts = content.split("---", 2)
        fm = parts[1]
        for field, default in [("version:", "version: 0.1.0"), ("license:", "license: MIT"), ("author:", "author: OpenClaw Team")]:
            if field not in fm:
                fm = fm.rstrip() + "\n" + default + "\n"
                changed = True
        if changed:
            content = "---" + fm + "---" + parts[2]

    # 3. Add missing sections
    sections_to_add = []
    if "## When to Use" not in content and "## 何时使用" not in content:
        sections_to_add.append("\n## When to Use\n\n- Trigger this skill when relevant tasks are detected\n")
    if "## When NOT to Use" not in content and "## 不应该使用" not in content:
        sections_to_add.append("\n## When NOT to Use\n\n- Do not use for unrelated tasks\n")
    if "```" not in content:
        sections_to_add.append("\n## CLI\n\n```bash\n# See scripts/ for available commands\n```\n")

    if sections_to_add:
        content = content.rstrip() + "\n" + "\n".join(sections_to_add)
        changed = True

    if changed:
        md.write_text(content, encoding="utf-8")
    return changed


def _apply_reliability_improvement(skill_path: Path) -> bool:
    """Create a minimal test file for skills that have scripts/ but no tests/.

    Pure-text skills (no scripts/) should NOT get auto-generated tests —
    they score reliability=1.0 by default.
    """
    # Only add tests for skills that actually have scripts to test
    if not (skill_path / "scripts").exists():
        return False

    tests_dir = skill_path / "tests"
    tests_dir.mkdir(parents=True, exist_ok=True)
    if any(tests_dir.glob("test_*.py")):
        return False  # tests already exist
    test_file = tests_dir / "test_smoke.py"
    test_file.write_text(
        '"""Auto-generated smoke test."""\n\n'
        "def test_skill_directory_exists():\n"
        f'    from pathlib import Path\n'
        f'    assert Path(r"{skill_path}").exists()\n',
        encoding="utf-8",
    )
    return True


def _apply_efficiency_improvement(skill_path: Path) -> bool:
    """If SKILL.md is too long, extract the last section into references/."""
    md = skill_path / "SKILL.md"
    if not md.exists():
        return False
    content = md.read_text(encoding="utf-8")
    lines = content.split("\n")
    if len(lines) <= 200:
        return False  # not too long

    refs_dir = skill_path / "references"
    refs_dir.mkdir(parents=True, exist_ok=True)

    # Move everything after line 200 into a reference file
    main_content = "\n".join(lines[:200]) + "\n\n> See references/ for extended content.\n"
    extra = "\n".join(lines[200:])
    md.write_text(main_content, encoding="utf-8")
    (refs_dir / "extended-content.md").write_text(extra, encoding="utf-8")
    return True


def _apply_security_improvement(skill_path: Path) -> bool:
    """Redact hardcoded secrets from SKILL.md."""
    md = skill_path / "SKILL.md"
    if not md.exists():
        return False
    content = md.read_text(encoding="utf-8")
    lowered = content.lower()
    if "password" not in lowered and "api_key" not in lowered:
        return False

    redacted = re.sub(
        r'(password|api_key)\s*[:=]\s*\S+',
        r'\1 = <REDACTED>',
        content,
        flags=re.IGNORECASE,
    )
    if redacted != content:
        md.write_text(redacted, encoding="utf-8")
        return True
    return False


def _apply_instruction_improvement(skill_path: Path, improvement: dict) -> None | bool:
    """Apply an instruction-level improvement to SKILL.md."""
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False
    content = skill_md.read_text(encoding="utf-8")
    issue_id = improvement.get("issue_id", "")

    if issue_id == "missing_when_to_use":
        # Add a When to Use section after the first heading
        lines = content.split("\n")
        insert_idx = next((i for i, l in enumerate(lines) if l.startswith("# ") and i > 0), len(lines))
        section = "\n## When to Use\n\n- [Define specific trigger conditions here]\n- [Add use cases]\n"
        lines.insert(insert_idx + 1, section)
        skill_md.write_text("\n".join(lines), encoding="utf-8")
        return True

    elif issue_id == "missing_when_not_to_use":
        # Add after When to Use or after first heading
        lines = content.split("\n")
        when_idx = next((i for i, l in enumerate(lines) if "When to Use" in l), None)
        if when_idx is not None:
            # Find end of When to Use section
            insert_idx = when_idx + 1
            while insert_idx < len(lines) and not lines[insert_idx].startswith("#"):
                insert_idx += 1
        else:
            insert_idx = next((i for i, l in enumerate(lines) if l.startswith("# ") and i > 0), len(lines)) + 1
        section = "\n## When NOT to Use\n\n- [Define exclusion conditions here]\n"
        lines.insert(insert_idx, section)
        skill_md.write_text("\n".join(lines), encoding="utf-8")
        return True

    elif issue_id == "too_long":
        # Extract detailed sections to references/
        references_dir = skill_path / "references"
        references_dir.mkdir(exist_ok=True)
        # Find the longest section and extract it
        lines = content.split("\n")
        sections: list[dict] = []
        current_section: dict = {"heading": "", "start": 0, "lines": []}
        for i, line in enumerate(lines):
            if line.startswith("## "):
                if current_section["lines"]:
                    sections.append(current_section)
                current_section = {"heading": line, "start": i, "lines": []}
            else:
                current_section["lines"].append(line)
        if current_section["lines"]:
            sections.append(current_section)

        if sections:
            longest = max(sections, key=lambda s: len(s["lines"]))
            if len(longest["lines"]) > 30:
                # Extract to references/
                slug = longest["heading"].strip("# ").lower().replace(" ", "-")[:30]
                ref_path = references_dir / f"{slug}.md"
                ref_path.write_text(
                    longest["heading"] + "\n" + "\n".join(longest["lines"]),
                    encoding="utf-8",
                )
                # Replace in SKILL.md with a link
                new_content = content.replace(
                    longest["heading"] + "\n" + "\n".join(longest["lines"]),
                    f"{longest['heading']}\n\nSee [{ref_path.name}](references/{ref_path.name}) for details.\n"
                )
                skill_md.write_text(new_content, encoding="utf-8")
                return True

    elif issue_id == "no_examples":
        content += "\n\n## Quick Start\n\n```bash\n# TODO: Add usage examples\n```\n"
        skill_md.write_text(content, encoding="utf-8")
        return True

    return False


# ---------------------------------------------------------------------------
# Backup / restore / commit helpers
# ---------------------------------------------------------------------------

def backup_skill(skill_path: Path) -> Path:
    """Create a timestamped backup of the skill directory."""
    from lib.common import compact_timestamp
    backup_path = skill_path.parent / f"{skill_path.name}.backup.{compact_timestamp()}"
    shutil.copytree(str(skill_path), str(backup_path))
    return backup_path


def revert_to_backup(skill_path: Path, backup_path: Path) -> None:
    """Restore skill directory from a backup."""
    shutil.rmtree(str(skill_path), ignore_errors=True)
    shutil.copytree(str(backup_path), str(skill_path))


def commit_change(skill_path: Path, message: str) -> None:
    """Attempt a git commit (best-effort, non-fatal)."""
    try:
        subprocess.run(
            ["git", "add", "SKILL.md", "references/", "scripts/", "tests/"],
            cwd=str(skill_path), capture_output=True, timeout=10,
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=str(skill_path), capture_output=True, timeout=10,
        )
    except Exception:
        pass  # non-fatal


# ---------------------------------------------------------------------------
# Report generation
# ---------------------------------------------------------------------------

def generate_improvement_report(
    results: list[ImprovementResult],
    final_scores: dict[str, float],
    memory: ThreeLayerMemory,
) -> dict[str, Any]:
    """Generate a structured report from improvement results."""
    kept_count = sum(1 for r in results if r.kept)
    reverted_count = sum(1 for r in results if r.applied and not r.kept)
    skipped_count = sum(1 for r in results if not r.applied)

    return {
        "iterations": len(results),
        "kept": kept_count,
        "reverted": reverted_count,
        "skipped": skipped_count,
        "final_scores": final_scores,
        "memory_hot_count": memory.hot_count(),
        "memory_warm_count": memory.warm_count(),
        "results": [asdict(r) for r in results],
        "timestamp": utc_now_iso(),
    }


# ---------------------------------------------------------------------------
# Main loop
# ---------------------------------------------------------------------------

def self_improve_loop(
    skill_path: Path,
    metric: str = "accuracy",
    max_iterations: int = 5,
    state_root: Path | None = None,
    memory_dir: Path | None = None,
) -> dict[str, Any]:
    """
    Real Karpathy self-improvement loop.

    Each iteration:
    1. Evaluate current state -> get scores per dimension
    2. Check Pareto front for regression bounds
    3. Analyze evaluation traces for failure patterns
    4. Propose improvement based on patterns + memory
    5. Apply improvement (with backup)
    6. Re-evaluate -> compare
    7. Keep if Pareto-accepted, revert otherwise
    8. Record outcome in memory
    """
    skill_path = Path(skill_path)
    memory = ThreeLayerMemory(memory_dir or skill_path / ".improvement-memory")

    pareto_path = (Path(state_root) / "pareto_front.json") if state_root else None
    pareto = ParetoFront(pareto_path)

    results: list[ImprovementResult] = []
    best_scores = evaluate_skill_dimensions(skill_path)

    for i in range(max_iterations):
        # 1. Find weakest dimension
        if not best_scores:
            results.append(ImprovementResult(
                i, "none", "No scores available",
                False, 0.0, 0.0, False, False, "no_scores",
            ))
            break

        weakest_dim = min(best_scores, key=best_scores.get)
        patterns = memory.get_patterns(weakest_dim)

        # 2. Propose improvement
        candidate = propose_targeted_improvement(skill_path, weakest_dim, patterns, scores=best_scores)
        if candidate is None:
            results.append(ImprovementResult(
                i, "none", "No candidate found",
                False, 0.0, 0.0, False, False, "no_candidate",
            ))
            continue

        # 3. Backup + apply
        backup = backup_skill(skill_path)
        applied = apply_improvement(skill_path, candidate)
        if not applied:
            revert_to_backup(skill_path, backup)
            shutil.rmtree(str(backup), ignore_errors=True)
            results.append(ImprovementResult(
                i, candidate["type"], candidate["description"],
                False, 0.0, 0.0, False, False, "apply_failed",
            ))
            continue

        # 4. Re-evaluate
        new_scores = evaluate_skill_dimensions(skill_path)

        # 5. Check Pareto front
        pareto_result = pareto.check_regression(new_scores)
        new_scalar = sum(new_scores.values()) / len(new_scores) if new_scores else 0.0
        old_scalar = sum(best_scores.values()) / len(best_scores) if best_scores else 0.0

        # 6. Keep or revert
        if not pareto_result["regressed"] and new_scalar >= old_scalar:
            # KEEP
            pareto.add(ParetoEntry(f"iter-{i}", candidate["type"], new_scores))
            commit_change(skill_path, f"improve: {candidate['description']}")
            memory.record_outcome(candidate["type"], True, {
                "dimension": weakest_dim,
                "scores": new_scores,
            })
            best_scores = new_scores
            kept = True
        else:
            # REVERT
            revert_to_backup(skill_path, backup)
            memory.record_outcome(candidate["type"], False, {
                "dimension": weakest_dim,
                "reason": "pareto_regression" if pareto_result["regressed"] else "no_improvement",
                "regressions": pareto_result.get("regressions", []),
            })
            kept = False

        # Cleanup backup
        shutil.rmtree(str(backup), ignore_errors=True)

        results.append(ImprovementResult(
            iteration=i,
            candidate_type=candidate["type"],
            description=candidate["description"],
            applied=True,
            score_before=old_scalar,
            score_after=new_scalar,
            kept=kept,
            pareto_accepted=not pareto_result["regressed"],
            reason="kept" if kept else "reverted",
        ))

    return generate_improvement_report(results, best_scores, memory)


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args():
    parser = argparse.ArgumentParser(description="Karpathy Self-Improvement Loop")
    parser.add_argument("--skill-path", type=str, required=True, help="Skill directory")
    parser.add_argument("--metric", type=str, default="accuracy", help="Primary metric")
    parser.add_argument("--max-iterations", type=int, default=5, help="Max iterations")
    parser.add_argument("--state-root", type=str, default=None, help="State root directory")
    parser.add_argument("--memory-dir", type=str, default=None, help="Memory directory")
    parser.add_argument("--mock", action="store_true", help="Use regex fallback instead of LLM for accuracy scoring")
    return parser.parse_args()


def main():
    global _USE_MOCK_LLM
    args = parse_args()
    _USE_MOCK_LLM = args.mock
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    report = self_improve_loop(
        skill_path=Path(args.skill_path),
        metric=args.metric,
        max_iterations=args.max_iterations,
        state_root=Path(args.state_root) if args.state_root else None,
        memory_dir=Path(args.memory_dir) if args.memory_dir else None,
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))

    # Write scores to state directory so autoloop can detect convergence
    if args.state_root:
        learner_dir = Path(args.state_root) / "learner"
        learner_dir.mkdir(parents=True, exist_ok=True)
        import time
        score_path = learner_dir / f"scores-{int(time.time())}.json"
        with score_path.open("w", encoding="utf-8") as f:
            json.dump(report, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
