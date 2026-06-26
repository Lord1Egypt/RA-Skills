#!/usr/bin/env python3
"""
Auto-Evolve v3.9 — Four-perspective automated skill scanner.

Features (v3.5):
- PersonaAwareMemory: openclaw SQLite primary + hawkbridge LanceDB supplement
- Cross-persona workspace: recall context from any persona's workspace
- CLI args: --recall-persona, --memory-source (auto|openclaw|hawkbridge|both)
- FourPerspectiveScanner: USER / PRODUCT / PROJECT / TECH four-angle scan
- EffectTracker: true before/after effect tracking per iteration
- CostTracker: LLM call cost tracking with pricing table
- IssueLinker: auto-close GitHub issues related to committed changes
- SmartScheduler: activity-based dynamic scan frequency

Features (v3.0):
- LLM-driven code analysis
- Dependency awareness
- Test comparison
- Cherry-pick rollback
- Multi-language support
- Release management
- Contributor tracking
- Priority scoring

Usage:
    auto-evolve.py scan [--dry-run]
    auto-evolve.py approve [--all | ID...] [--reason TEXT]
    auto-evolve.py confirm                       # confirm pending changes (semi-auto)
    auto-evolve.py reject <id> [--reason TEXT]
    auto-evolve.py repo-add <path> --type TYPE [--monitor]
    auto-evolve.py repo-list
    auto-evolve.py rollback --to VERSION
    auto-evolve.py schedule --every HOURS
    auto-evolve.py schedule --suggest
    auto-evolve.py schedule --auto
    auto-evolve.py schedule --show
    auto-evolve.py schedule --remove
    auto-evolve.py set-mode semi-auto|full-auto
    auto-evolve.py set-rules [--low] [--medium] [--high]
    auto-evolve.py log [--limit N]
    auto-evolve.py learnings
    auto-evolve.py release --version VERSION [--changelog TEXT]
    auto-evolve.py effects [--iteration ID]
    auto-evolve.py costs [--iteration ID]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Optional

# Fix sys.path so we can import from scripts.helpers (for record_learning etc.)
import sys as _sys
_script_dir = str(Path(__file__).parent.parent)
if _script_dir not in _sys.path:
    _sys.path.insert(0, _script_dir)
from scripts.helpers import record_learning, record_iteration_metrics


# ===========================================================
# Persona Detection & Workspace Resolution
# ===========================================================

def detect_persona() -> str:
    """Detect the current persona from environment or working directory."""
    import os
    persona = os.environ.get("OPENCLAW_AGENT_ID", "").strip().lower()
    if persona in ("main", "tseng", "wukong", "bajie", "bailong", "shaseng"):
        return persona
    cwd = os.getcwd()
    for p in ("workspace-tseng", "workspace-wukong", "workspace-bajie", "workspace-bailong", "workspace-shaseng"):
        if p in cwd:
            return p.replace("workspace-", "")
    return "main"

def get_workspace_for_persona(persona: str) -> Path:
    """Return the workspace Path for a given persona."""
    home = Path.home()
    if persona == "main":
        return home / ".openclaw" / "workspace"
    return home / ".openclaw" / f"workspace-{persona}"

# ===========================================================
# Memory: OpenClaw SQLite
# ===========================================================

class OpenClawMemory:
    """Access OpenClaw's SQLite message memory for a persona."""

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace

    def _get_db_path(self) -> Optional[Path]:
        memory_dir = self.workspace / "memory"
        if not memory_dir.exists():
            return None
        for fname in (f"{detect_persona()}.sqlite", "main.sqlite"):
            p = memory_dir / fname
            if p.exists():
                return p
        return None

    def is_available(self) -> bool:
        return self._get_db_path() is not None

    def search(self, query: str, top_k: int = 5) -> list[str]:
        db_path = self._get_db_path()
        if not db_path:
            return []
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content FROM messages WHERE content LIKE ? ORDER BY created_at DESC LIMIT ?",
                (f"%{query}%", top_k),
            )
            results = [row[0] for row in cursor.fetchall() if row[0]]
            conn.close()
            return results
        except Exception:
            return []

    def get_preferences(self, persona: str) -> dict[str, list[str]]:
        memories = self.get_recent(limit=50)
        disliked, liked = [], []
        for m in memories:
            content = (m.get("content") or "")[:200].lower()
            if any(kw in content for kw in ["不要", "别", "拒绝", "不喜欢", "讨厌", "反感"]):
                disliked.append(content)
            elif any(kw in content for kw in ["喜欢", "很好", "继续保持", "需要", "想要", "可以"]):
                liked.append(content)
        return {"liked": liked[:5], "disliked": disliked[:5]}

    def get_recent(self, limit: int = 20) -> list[dict]:
        db_path = self._get_db_path()
        if not db_path:
            return []
        try:
            import sqlite3
            conn = sqlite3.connect(str(db_path))
            cursor = conn.cursor()
            cursor.execute(
                "SELECT content, created_at FROM messages ORDER BY created_at DESC LIMIT ?",
                (limit,),
            )
            results = [
                {"content": row[0], "created_at": row[1]}
                for row in cursor.fetchall() if row[0]
            ]
            conn.close()
            return results
        except Exception:
            return []

# ===========================================================
# Memory: HawkBridge LanceDB
# ===========================================================

class HawkBridgeMemory:
    """Access HawkBridge's LanceDB vector memory for a persona."""

    LANCEDB_CANDIDATES = [
        "skills/hawk-bridge/python/lancedb",
        "skills/hawk-bridge/lancedb",
        "skills/hawk-bridge/python/.lancedb",
        "hawk-bridge/lancedb",
        "hawk-bridge/.lancedb",
    ]

    def __init__(self, workspace: Path) -> None:
        self.workspace = workspace
        self.db_path = self._find_lancedb()

    def _find_lancedb(self) -> Optional[Path]:
        for rel in self.LANCEDB_CANDIDATES:
            p = self.workspace / rel
            if p.exists():
                return p
        return None

    def is_available(self) -> bool:
        return self.db_path is not None

    def search(self, query: str, persona: str, top_k: int = 5) -> list[str]:
        if not self.is_available():
            return []
        try:
            import lancedb
            db = lancedb.connect(str(self.db_path))
            for table_name in ("memories", "memory", "default", "embeddings"):
                try:
                    tbl = db.open_table(table_name)
                    try:
                        results = (
                            tbl.search(query)
                            .where(f"persona = '{persona}'")
                            .limit(top_k)
                            .to_list()
                        )
                    except Exception:
                        results = tbl.search(query).limit(top_k).to_list()
                    texts = [r.get("text", r.get("content", "")) for r in results]
                    return [t for t in texts if t]
                except Exception:
                    continue
            return []
        except Exception:
            return []

    def get_preferences(self, persona: str) -> dict[str, list[str]]:
        disliked_queries = [
            f"{persona} 不要", f"{persona} 拒绝", f"{persona} 不喜欢", "不要 做", "stop doing"
        ]
        liked_queries = [
            f"{persona} 喜欢", f"{persona} 需要", "很好 继续保持", "keep doing"
        ]
        disliked, liked = set(), set()
        for q in disliked_queries:
            for r in self.search(q, persona, top_k=3):
                if r:
                    disliked.add(r[:200])
        for q in liked_queries:
            for r in self.search(q, persona, top_k=3):
                if r:
                    liked.add(r[:200])
        return {"liked": list(liked)[:5], "disliked": list(disliked)[:5]}

# ===========================================================
# Memory: PersonaAware unified interface
# ===========================================================

class MemorySource(Enum):
    AUTO = "auto"
    OPENCLAW = "openclaw"
    HAWKBRIDGE = "hawkbridge"
    BOTH = "both"

class PersonaAwareMemory:
    """Unified memory access with persona-aware workspace and source routing."""

    WORKSPACE_FILES = (
        "SOUL.md", "USER.md", "IDENTITY.md", "MEMORY.md", "AGENTS.md", "TOOLS.md"
    )

    def __init__(self, recall_persona: str = "", memory_source: str = "auto") -> None:
        self.effective_persona = (recall_persona.strip().lower() or detect_persona())
        if self.effective_persona == "master":
            self.effective_persona = "main"
        self.workspace = get_workspace_for_persona(self.effective_persona)
        self.context_persona = self.effective_persona
        self.source = MemorySource(memory_source)
        self.openclaw_mem = OpenClawMemory(self.workspace)
        self.hawkbridge_mem = HawkBridgeMemory(self.workspace)
        self._use_openclaw = self.source in (MemorySource.OPENCLAW, MemorySource.AUTO)
        self._use_hawkbridge = self.source in (MemorySource.HAWKBRIDGE, MemorySource.AUTO)
        # AUTO: openclaw primary, hawkbridge supplement
        if self.source == MemorySource.AUTO:
            self._use_openclaw = True
            self._use_hawkbridge = self.hawkbridge_mem.is_available()

    def load_context_files(self) -> dict[str, str]:
        ctx = {}
        for fname in self.WORKSPACE_FILES:
            fp = self.workspace / fname
            if fp.exists() and fp.is_file():
                try:
                    ctx[fname] = fp.read_text(encoding="utf-8", errors="ignore")
                except OSError:
                    ctx[fname] = ""
            else:
                ctx[fname] = ""
        return ctx

    def get_context_summary(self) -> str:
        ctx = self.load_context_files()
        labels = {
            "SOUL.md": "价值观/风格",
            "USER.md": "偏好/习惯",
            "IDENTITY.md": "项目定位",
            "MEMORY.md": "长期记忆",
            "AGENTS.md": "Agent团队架构",
            "TOOLS.md": "工具配置",
        }
        lines = [f"【{self.context_persona} 上下文】"]
        for fname, label in labels.items():
            content = ctx.get(fname, "")
            if content:
                snippet = content[:250].replace("\n", " ").strip()
                lines.append(f"\n{label}（{fname}）: {snippet}")
            else:
                lines.append(f"\n{label}（{fname}）: 未配置")
        return "\n".join(lines)

    def get_preferences(self) -> dict[str, list[str]]:
        oc_prefs = {"liked": [], "disliked": []}
        hb_prefs = {"liked": [], "disliked": []}
        if self._use_openclaw and self.openclaw_mem.is_available():
            oc_prefs = self.openclaw_mem.get_preferences(self.context_persona)
        elif self._use_hawkbridge and self.hawkbridge_mem.is_available():
            hb_prefs = self.hawkbridge_mem.get_preferences(self.context_persona)
        if self.source == MemorySource.BOTH:
            return {
                "liked": oc_prefs.get("liked", []) + hb_prefs.get("liked", []),
                "disliked": oc_prefs.get("disliked", []) + hb_prefs.get("disliked", []),
            }
        if self._use_openclaw and (oc_prefs.get("liked") or oc_prefs.get("disliked")):
            return oc_prefs
        if hb_prefs.get("liked") or hb_prefs.get("disliked"):
            return hb_prefs
        return {"liked": [], "disliked": []}

    def search(self, query: str, top_k: int = 5) -> list[str]:
        results = []
        if self._use_openclaw and self.openclaw_mem.is_available():
            results.extend(self.openclaw_mem.search(query, top_k))
        if self._use_hawkbridge and self.hawkbridge_mem.is_available():
            results.extend(self.hawkbridge_mem.search(query, self.context_persona, top_k))
        seen = set()
        deduped = []
        for r in results:
            if r not in seen:
                seen.add(r)
                deduped.append(r)
        return deduped[:top_k]

# ===========================================================
# Constants
# ===========================================================

HOME = Path.home()
AUTO_EVOLVE_RC = HOME / ".auto-evolverc.json"
SKILL_DIR = HOME / ".openclaw" / "workspace" / "skills" / "auto-evolve"
ITERATIONS_DIR = SKILL_DIR / ".iterations"
LEARNINGS_DIR = SKILL_DIR / ".learnings"

REPO_TYPES = ("skill", "norms", "project", "closed")

# Multi-language TODO patterns
TODO_PATTERNS = {
    ".py": ["# TODO", "# FIXME", "# XXX", "# HACK", "# NOTE"],
    ".js": ["// TODO", "// FIXME", "// XXX", "// HACK", "/* TODO"],
    ".ts": ["// TODO", "// FIXME", "// XXX", "// HACK", "/* TODO"],
    ".go": ["// TODO", "// FIXME", "// XXX"],
    ".sh": ["# TODO", "# FIXME", "# XXX"],
    ".java": ["// TODO", "// FIXME", "// XXX", "/* TODO"],
    ".md": ["<!-- TODO", "[TODO]", "- [ ]"],
}
LANGUAGE_EXTENSIONS = {
    ".py": "python", ".js": "javascript", ".ts": "typescript", ".go": "go",
    ".sh": "shell", ".bash": "shell", ".zsh": "shell", ".java": "java",
}
RISK_LEVELS = ("low", "medium", "high")
RISK_COLORS = {
    "low": "🟢",
    "medium": "🟡",
    "high": "🔴",
}

# Priority scoring weights
PRIORITY_WEIGHTS = {
    "value": 0.5,
    "risk": 0.3,
    "cost": 0.2,
}

DEFAULT_VALUE_SCORES = {
    "bug_fix": 10,
    "todo_fixme": 7,
    "add_test": 7,
    "optimization": 6,
    "refactor": 5,
    "docs": 4,
    "lint_fix": 4,
    "formatting": 3,
}

DEFAULT_COST_SCORES = {
    "5min": 1,
    "15min": 3,
    "30min": 5,
    "1h": 7,
    "2h": 10,
}


# ===========================================================
# LLM Pricing (v3.2 CostTracker)
# ===========================================================

LLM_PRICING: dict[str, dict[str, float]] = {
    "MiniMax-M2": {"input": 0.1, "output": 0.3},
    "gpt-4": {"input": 30.0, "output": 60.0},
    "gpt-4o": {"input": 2.5, "output": 10.0},
    "gpt-4o-mini": {"input": 0.15, "output": 0.6},
    "claude-3-5-sonnet": {"input": 3.0, "output": 15.0},
    "claude-3-opus": {"input": 15.0, "output": 75.0},
}


# ===========================================================
# Enums
# ===========================================================

class RiskLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class ChangeCategory(Enum):
    AUTO_EXEC = "auto_exec"
    PENDING_APPROVAL = "pending_approval"
    OPTIMIZATION = "optimization"


class OperationMode(Enum):
    SEMI_AUTO = "semi-auto"
    FULL_AUTO = "full-auto"


# ===========================================================
# Data Models
# ===========================================================

@dataclass
class Repository:
    path: str
    type: str
    visibility: str = "public"
    auto_monitor: bool = True
    risk_override: Optional[str] = None
    scan_interval_hours: int = 168  # v3.2 SmartScheduler

    def resolve_path(self) -> Path:
        return Path(self.path).expanduser().resolve()

    def is_closed(self) -> bool:
        return self.visibility == "closed"

    def get_default_risk(self, change_type: str, file_path: str) -> RiskLevel:
        if self.risk_override:
            return RiskLevel(self.risk_override)

        file_lower = file_path.lower()

        if self.visibility == "closed":
            if change_type in ("modified", "added"):
                if any(ext in file_lower for ext in (".py", ".js", ".ts", ".go", ".rs")):
                    return RiskLevel.MEDIUM
            if change_type == "removed":
                return RiskLevel.MEDIUM

        if self.type == "norms":
            if any(ext in file_lower for ext in (".md", ".txt", ".yaml", ".yml", ".json")):
                return RiskLevel.LOW

        if self.type == "project":
            if "test" in file_lower or "_test." in file_lower:
                return RiskLevel.MEDIUM

        return RiskLevel.MEDIUM


@dataclass
class ChangeItem:
    id: int
    description: str
    file_path: str
    change_type: str
    risk: RiskLevel
    category: ChangeCategory
    repo_path: str = ""
    repo_type: str = ""
    optimization_type: Optional[str] = None
    commit_hash: Optional[str] = None
    pr_url: Optional[str] = None
    content_hash: Optional[str] = None
    value_score: int = 5
    risk_score: int = 5
    cost_score: int = 5
    priority: float = 0.0
    llm_suggestion: Optional[str] = None
    llm_risk: Optional[str] = None
    llm_implementation_hint: Optional[str] = None
    affected_files: Optional[list[str]] = None


@dataclass
class OptimizationFinding:
    type: str
    file_path: str
    line: int
    description: str
    suggestion: str
    risk: RiskLevel


@dataclass
class IterationManifest:
    version: str
    date: str
    status: str
    risk_level: str
    items_auto: int = 0
    items_approved: int = 0
    items_rejected: int = 0
    items_optimization: int = 0
    duration_seconds: float = 0.0
    items_pending_approval: list = field(default_factory=list)
    rollback_of: Optional[str] = None
    rollback_reason: Optional[str] = None
    has_alert: bool = False
    metrics_id: Optional[str] = None
    test_coverage_delta: Optional[float] = None
    contributors: Optional[dict] = None
    # v3.2
    total_cost_usd: Optional[float] = None
    llm_calls: int = 0


@dataclass
class LearningEntry:
    id: str
    type: str
    change_id: str
    description: str
    reason: Optional[str]
    date: str
    repo: str
    approved_by: Optional[str] = None


@dataclass
class AlertEntry:
    iteration_id: str
    date: str
    alert_type: str
    message: str
    details: dict


@dataclass
class IterationMetrics:
    iteration_id: str
    date: str
    todos_resolved: int = 0
    lint_errors_fixed: int = 0
    test_coverage_delta: float = 0.0
    files_changed: int = 0
    lines_added: int = 0
    lines_removed: int = 0
    quality_gate_passed: bool = True


# ===========================================================
# v3.2: EffectTracker
# ===========================================================

class EffectTracker:
    """
    Tracks the actual effects of each iteration by comparing
    code quality metrics before and after changes are applied.
    """

    def __init__(self, iterations_dir: Path = ITERATIONS_DIR) -> None:
        self.iterations_dir = iterations_dir

    def count_todos(self, repo_path: Path) -> int:
        """Count unresolved TODO/FIXME annotations across the repo."""
        count = 0
        for ext, patterns in TODO_PATTERNS.items():
            if ext == ".md":
                continue  # Skip markdown separately
            for code_file in repo_path.rglob(f"*{ext}"):
                if any(s in str(code_file) for s in (".git", "__pycache__", "node_modules", ".iterations")):
                    continue
                try:
                    content = code_file.read_text(encoding="utf-8")
                    for line in content.split("\n"):
                        for pat in patterns:
                            if pat in line:
                                count += 1
                                break
                except (UnicodeDecodeError, OSError):
                    pass
        # Also scan markdown TODO markers
        for md_file in repo_path.rglob("*.md"):
            if ".git" in str(md_file) or ".iterations" in str(md_file):
                continue
            try:
                content = md_file.read_text(encoding="utf-8")
                for line in content.split("\n"):
                    for pat in TODO_PATTERNS[".md"]:
                        if pat in line:
                            count += 1
                            break
            except (UnicodeDecodeError, OSError):
                pass
        return count

    def count_code_lines(self, repo_path: Path) -> int:
        """Count non-blank, non-comment lines of code."""
        total = 0
        for ext in LANGUAGE_EXTENSIONS:
            for code_file in repo_path.rglob(f"*{ext}"):
                if any(s in str(code_file) for s in (".git", "__pycache__", "node_modules", ".iterations")):
                    continue
                try:
                    content = code_file.read_text(encoding="utf-8")
                    for line in content.split("\n"):
                        stripped = line.strip()
                        if stripped and not stripped.startswith("#") and not stripped.startswith("//"):
                            total += 1
                except (UnicodeDecodeError, OSError):
                    pass
        return total

    def count_functions(self, repo_path: Path) -> int:
        """Count function/ method definitions in Python files."""
        count = 0
        for py_file in repo_path.rglob("*.py"):
            if any(s in str(py_file) for s in (".git", "__pycache__", ".iterations")):
                continue
            try:
                content = py_file.read_text(encoding="utf-8")
                count += len(re.findall(r"^(?:async\s+)?def\s+\w+", content, re.MULTILINE))
            except (UnicodeDecodeError, OSError):
                pass
        return count

    def count_duplicate_lines(self, repo_path: Path) -> int:
        """Estimate duplicate code lines (identical lines appearing 3+ times)."""
        line_counts: dict[str, int] = {}
        for ext in LANGUAGE_EXTENSIONS:
            for code_file in repo_path.rglob(f"*{ext}"):
                if any(s in str(code_file) for s in (".git", "__pycache__", ".iterations")):
                    continue
                try:
                    content = code_file.read_text(encoding="utf-8")
                    for line in content.split("\n"):
                        stripped = line.strip()
                        if len(stripped) > 20 and not stripped.startswith("#") and not stripped.startswith("//"):
                            line_counts[stripped] = line_counts.get(stripped, 0) + 1
                except (UnicodeDecodeError, OSError):
                    pass
        return sum(1 for c in line_counts.values() if c >= 3)

    def run_lint(self, repo_path: Path) -> int:
        """Run pylint on Python files and return error count."""
        result = subprocess.run(
            ["python3", "-m", "py_compile"],
            cwd=str(repo_path),
            capture_output=True,
        )
        # Simple syntax check only - pylint may not be installed
        return 0  # Placeholder; real lint count requires pylint

    def snapshot(self, repo_path: Path) -> dict:
        """
        Take a snapshot of current code quality metrics.
        Returns a dict with todos, code_lines, functions, duplicates.
        """
        return {
            "todos": self.count_todos(repo_path),
            "code_lines": self.count_code_lines(repo_path),
            "functions": self.count_functions(repo_path),
            "duplicate_lines": self.count_duplicate_lines(repo_path),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def track_iteration_effect(
        self,
        iteration_id: str,
        before_snapshots: dict[str, dict],
        after_snapshots: dict[str, dict],
        todos_resolved: int = 0,
        lint_errors_fixed: int = 0,
        coverage_delta: float = 0.0,
    ) -> dict:
        """
        Compare before/after snapshots and produce an effect report.
        Stores the result as effect.json in the iteration directory.
        """
        effects: dict[str, dict] = {}

        all_repos = set(before_snapshots.keys()) | set(after_snapshots.keys())

        for repo_key in all_repos:
            before = before_snapshots.get(repo_key, {})
            after = after_snapshots.get(repo_key, {})

            effects[repo_key] = {
                "todos_delta": (after.get("todos", 0) - before.get("todos", 0)),
                "code_lines_delta": (after.get("code_lines", 0) - before.get("code_lines", 0)),
                "functions_delta": (after.get("functions", 0) - before.get("functions", 0)),
                "duplicate_lines_delta": (after.get("duplicate_lines", 0) - before.get("duplicate_lines", 0)),
            }

        # Aggregate deltas across all repos
        total_todos_delta = sum(e["todos_delta"] for e in effects.values())
        total_code_lines_delta = sum(e["code_lines_delta"] for e in effects.values())
        total_functions_delta = sum(e["functions_delta"] for e in effects.values())
        total_duplicate_delta = sum(e["duplicate_lines_delta"] for e in effects.values())

        # Determine verdict
        positive_signals = sum(1 for d in [
            -total_todos_delta,  # Fewer TODOs = good
            coverage_delta,
            -total_duplicate_delta,  # Fewer duplicates = good
            -abs(total_functions_delta),  # Fewer long functions = good
        ] if d > 0)
        negative_signals = sum(1 for d in [
            -total_todos_delta,
            coverage_delta,
            -total_duplicate_delta,
            -abs(total_functions_delta),
        ] if d < 0)

        if positive_signals >= 3:
            verdict = "positive"
        elif negative_signals >= 3:
            verdict = "negative"
        else:
            verdict = "neutral"

        summary_parts = []
        if total_todos_delta != 0:
            summary_parts.append(f"{abs(total_todos_delta)} TODOs {'resolved' if total_todos_delta < 0 else 'added'}")
        if coverage_delta != 0:
            summary_parts.append(f"coverage {coverage_delta:+.1f}%")
        if total_duplicate_delta != 0:
            summary_parts.append(f"{abs(total_duplicate_delta)} duplicate lines {'removed' if total_duplicate_delta < 0 else 'added'}")
        if total_code_lines_delta != 0:
            summary_parts.append(f"{total_code_lines_delta:+,} lines of code")

        summary = ", ".join(summary_parts) if summary_parts else "No significant changes detected"

        effect_report = {
            "iteration_id": iteration_id,
            "date": datetime.now(timezone.utc).isoformat(),
            "effects": effects,
            "summary": summary,
            "verdict": verdict,
            "totals": {
                "todos_resolved": todos_resolved,
                "todos_delta": total_todos_delta,
                "coverage_delta": coverage_delta,
                "lint_errors_delta": -lint_errors_fixed if lint_errors_fixed else 0,
                "duplicate_lines_delta": total_duplicate_delta,
                "function_count_delta": total_functions_delta,
                "code_lines_delta": total_code_lines_delta,
            },
        }

        # Save to iteration directory
        iter_dir = self.iterations_dir / iteration_id
        iter_dir.mkdir(parents=True, exist_ok=True)
        (iter_dir / "effect.json").write_text(json.dumps(effect_report, indent=2))

        return effect_report


# ===========================================================
# v3.2: CostTracker
# ===========================================================

class CostTracker:
    """
    Tracks LLM call costs per iteration using a pricing table.
    Records each call and aggregates costs in catalog.json.
    """

    def __init__(self, iterations_dir: Path = ITERATIONS_DIR) -> None:
        self.iterations_dir = iterations_dir
        self.pricing = LLM_PRICING

    def track_llm_call(
        self,
        prompt_tokens: int,
        completion_tokens: int,
        model: str,
    ) -> dict:
        """
        Record a single LLM call and estimate its cost in USD.
        Saves the call record to the current iteration's llm_calls.jsonl.
        """
        pricing = self.pricing.get(model, {"input": 0.0, "output": 0.0})
        input_cost = (prompt_tokens / 1_000_000) * pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * pricing["output"]
        total_cost = round(input_cost + output_cost, 6)

        record = {
            "date": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "prompt_tokens": prompt_tokens,
            "completion_tokens": completion_tokens,
            "total_tokens": prompt_tokens + completion_tokens,
            "estimated_cost_usd": total_cost,
        }

        # Append to current iteration's calls file (session-scoped)
        if not hasattr(self, "_pending_calls"):
            self._pending_calls: list[dict] = []
        self._pending_calls.append(record)

        return record

    def flush_calls(self, iteration_id: str) -> None:
        """Write accumulated calls to the iteration directory."""
        if not hasattr(self, "_pending_calls") or not self._pending_calls:
            return
        iter_dir = self.iterations_dir / iteration_id
        iter_dir.mkdir(parents=True, exist_ok=True)
        calls_file = iter_dir / "llm_calls.jsonl"
        with calls_file.open("a") as f:
            for call in self._pending_calls:
                f.write(json.dumps(call) + "\n")
        self._pending_calls = []

    def get_iteration_cost(self, iteration_id: str) -> dict:
        """Aggregate all LLM costs for a given iteration."""
        calls = self.load_calls(iteration_id)
        total = sum(c["estimated_cost_usd"] for c in calls)
        total_tokens = sum(c["total_tokens"] for c in calls)
        return {
            "iteration_id": iteration_id,
            "total_calls": len(calls),
            "total_tokens": total_tokens,
            "total_cost_usd": round(total, 6),
        }

    def load_calls(self, iteration_id: str) -> list[dict]:
        """Load all LLM call records for an iteration."""
        calls_file = self.iterations_dir / iteration_id / "llm_calls.jsonl"
        if not calls_file.exists():
            return []
        calls = []
        with calls_file.open() as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        calls.append(json.loads(line))
                    except json.JSONDecodeError:
                        pass
        return calls


# ===========================================================
# v3.2: IssueLinker
# ===========================================================

class IssueLinker:
    """
    Finds and auto-closes GitHub Issues related to committed changes.
    Uses `gh issue list` to find open issues referencing changed files.
    """

    def __init__(self) -> None:
        self._gh_available: Optional[bool] = None

    def _check_gh(self) -> bool:
        """Check if gh CLI is available."""
        if self._gh_available is None:
            self._gh_available = subprocess.run(
                ["which", "gh"], capture_output=True
            ).returncode == 0
        return self._gh_available

    def find_related_issues(self, repo_path: Path, changed_files: list[str]) -> list[dict]:
        """
        Find open issues whose title or body references any of the changed files.
        """
        if not self._check_gh():
            return []

        result = subprocess.run(
            ["gh", "issue", "list", "--state", "open", "--limit", "50", "--json", "number,title,body"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            return []

        try:
            issues = json.loads(result.stdout)
        except json.JSONDecodeError:
            return []

        related = []
        for issue in issues:
            body = issue.get("body", "") or ""
            title = issue.get("title", "") or ""
            combined = title.lower() + " " + body.lower()
            for file_path in changed_files:
                file_lower = file_path.lower()
                # Match file name or path component
                if file_lower in combined or Path(file_lower).name in combined:
                    related.append({
                        "number": issue["number"],
                        "title": issue["title"],
                        "body": body[:200],
                    })
                    break

        return related

    def close_issue(self, repo_path: Path, issue_number: int, comment: str) -> bool:
        """
        Add a comment to an issue explaining it was resolved by auto-evolve,
        then close it with reason 'completed'.
        """
        if not self._check_gh():
            return False

        # Add comment
        subprocess.run(
            [
                "gh", "issue", "comment", str(issue_number),
                "--body", comment,
            ],
            cwd=str(repo_path),
            capture_output=True,
        )

        # Close issue
        result = subprocess.run(
            [
                "gh", "issue", "close", str(issue_number),
                "--reason", "completed",
            ],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def close_related_issues(self, repo_path: Path, changed_files: list[str], iteration_id: str) -> dict:
        """
        Find and close all issues related to changed files.
        Returns a summary dict.
        """
        related = self.find_related_issues(repo_path, changed_files)
        if not related:
            return {"found": 0, "closed": 0, "issues": []}

        closed = []
        for issue in related:
            comment = (
                f"**Resolved by auto-evolve** (iteration `{iteration_id}`)\n\n"
                f"This issue was automatically resolved after the related "
                f"code changes were applied and validated."
            )
            success = self.close_issue(repo_path, issue["number"], comment)
            closed.append({
                "number": issue["number"],
                "title": issue["title"],
                "closed": success,
            })

        return {
            "found": len(related),
            "closed": sum(1 for c in closed if c["closed"]),
            "issues": closed,
        }


# ===========================================================
# v3.2: SmartScheduler
# ===========================================================

class SmartScheduler:
    """
    Dynamically adjusts scan frequency based on project activity.
    Uses git commit frequency over the last 7 days to assess activity level.
    """

    ACTIVITY_THRESHOLDS: dict[str, dict[str, int]] = {
        "very_active": {"commits_per_week": 20, "scan_interval_hours": 24},
        "active": {"commits_per_week": 10, "scan_interval_hours": 72},
        "normal": {"commits_per_week": 3, "scan_interval_hours": 168},
        "idle": {"commits_per_week": 0, "scan_interval_hours": 336},
    }

    def __init__(self, config: Optional[dict] = None) -> None:
        self.config = config or {}

    def assess_activity(self, repo_path: Path) -> str:
        """
        Count commits in the last 7 days and return activity level.
        Returns one of: very_active, active, normal, idle
        """
        result = subprocess.run(
            ["git", "log", "--oneline", "--since", "7 days ago"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
        )
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        commit_count = len([l for l in lines if l])

        if commit_count >= self.ACTIVITY_THRESHOLDS["very_active"]["commits_per_week"]:
            return "very_active"
        elif commit_count >= self.ACTIVITY_THRESHOLDS["active"]["commits_per_week"]:
            return "active"
        elif commit_count >= self.ACTIVITY_THRESHOLDS["normal"]["commits_per_week"]:
            return "normal"
        else:
            return "idle"

    def get_recommended_interval(self, repo_path: Path) -> int:
        """Get the recommended scan interval for a repo based on its activity."""
        activity = self.assess_activity(repo_path)
        return self.ACTIVITY_THRESHOLDS[activity]["scan_interval_hours"]

    def get_activity_stats(self, repo_path: Path) -> dict:
        """Get detailed activity statistics for a repo."""
        result = subprocess.run(
            ["git", "log", "--oneline", "--since", "7 days ago"],
            cwd=str(repo_path),
            capture_output=True,
            text=True,
        )
        lines = result.stdout.strip().split("\n") if result.stdout.strip() else []
        commit_count = len([l for l in lines if l])

        activity = self.assess_activity(repo_path)
        recommended = self.ACTIVITY_THRESHOLDS[activity]["scan_interval_hours"]

        return {
            "commits_last_7_days": commit_count,
            "activity": activity,
            "recommended_interval_hours": recommended,
            "threshold": self.ACTIVITY_THRESHOLDS[activity]["commits_per_week"],
        }

    def suggest_schedule(self) -> dict:
        """
        Generate scheduling suggestions for all configured repositories.
        Returns a dict mapping repo name to suggestion details.
        """
        suggestions = {}
        repositories = self.config.get("repositories", [])

        for repo in repositories:
            repo_path = Path(repo["path"]).expanduser().resolve()
            if not repo_path.exists():
                continue

            stats = self.get_activity_stats(repo_path)
            current_interval = repo.get("scan_interval_hours", 168)

            delta = stats["recommended_interval_hours"] - current_interval
            if delta > 0:
                action = "increase"
            elif delta < 0:
                action = "decrease"
            else:
                action = "maintain"

            suggestions[repo["path"]] = {
                "name": repo_path.name,
                "current_interval_hours": current_interval,
                "recommended_interval_hours": stats["recommended_interval_hours"],
                "activity": stats["activity"],
                "commits_last_7_days": stats["commits_last_7_days"],
                "action": action,
                "change_hours": delta,
            }

        return suggestions

    def apply_schedule(self, updates: dict[str, int]) -> dict:
        """
        Apply interval changes to config and save.
        updates: dict mapping repo path -> new interval hours
        Returns a summary dict.
        """
        from auto_evolve import load_config, save_config
        config = load_config()
        applied = []

        for repo in config.get("repositories", []):
            path = repo["path"]
            if path in updates:
                old = repo.get("scan_interval_hours", 168)
                repo["scan_interval_hours"] = updates[path]
                applied.append({
                    "path": path,
                    "old_interval": old,
                    "new_interval": updates[path],
                })

        save_config(config)
        return {"applied": applied}


# ===========================================================
# LLM Integration
# ===========================================================

def get_openclaw_llm_config() -> dict:
    """
    Read OpenClaw LLM configuration from environment, openclaw CLI, or models.json.
    Priority: env vars > models.json > openclaw config get llm
    """
    api_key = os.environ.get("OPENAI_API_KEY") or os.environ.get("MINIMAX_API_KEY", "")
    base_url = os.environ.get("OPENAI_BASE_URL") or os.environ.get("MINIMAX_BASE_URL", "")
    model = os.environ.get("OPENAI_MODEL") or os.environ.get("MINIMAX_MODEL", "MiniMax-M2")

    # Try openclaw config get llm (may not exist in all versions)
    try:
        result = subprocess.run(
            ["openclaw", "config", "get", "llm"],
            capture_output=True, text=True, timeout=5,
        )
        if result.returncode == 0:
            cfg = json.loads(result.stdout)
            api_key = api_key or cfg.get("api_key", "")
            base_url = base_url or cfg.get("base_url", "")
            model = model or cfg.get("model", "MiniMax-M2")
    except Exception:
        pass

    # Fallback: read from agents/main/agent/models.json
    if not api_key or not base_url:
        models_file = HOME / ".openclaw" / "agents" / "main" / "agent" / "models.json"
        if models_file.exists():
            try:
                data = json.loads(models_file.read_text())
                providers = data.get("providers", {})
                # Try minimax provider first
                minimax = providers.get("minimax", {})
                if not api_key:
                    api_key = minimax.get("apiKey", "")
                if not base_url:
                    base_url = minimax.get("baseUrl", "")
                    if base_url:
                        # The baseUrl is like https://api.minimaxi.com/anthropic
                        # The /v1/messages suffix is added by _call_llm_for_refactor
                        base_url = base_url.rstrip("/")
                # Also try openai provider
                if not api_key:
                    openai = providers.get("openai", {})
                    api_key = openai.get("apiKey", "")
                if not base_url:
                    openai = providers.get("openai", {})
                    obu = openai.get("baseUrl", "")
                    if obu:
                        base_url = obu.rstrip("/") + "/chat/completions"
            except (json.JSONDecodeError, OSError):
                pass

    return {"api_key": api_key, "base_url": base_url, "model": model}


def call_llm(prompt: str, system: str = "", model: str = "", base_url: str = "", api_key: str = "") -> str:
    if not api_key or not base_url:
        return ""
    import urllib.request
    headers = {"Content-Type": "application/json", "Authorization": "Bearer " + api_key}
    messages = ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}]
    body = json.dumps({"model": model or "MiniMax-M2", "messages": messages, "temperature": 0.3, "max_tokens": 16000}).encode("utf-8")
    # Try Anthropic /v1/messages first (MiniMax and other Anthropic-compatible APIs)
    for endpoint_suffix in ["/v1/messages", "/chat/completions"]:
        endpoint = base_url.rstrip("/") + endpoint_suffix
        try:
            req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
            with urllib.request.urlopen(req, timeout=120) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if "anthropic" in endpoint or endpoint_suffix == "/v1/messages":
                    text_blocks = [
                        b.get("text", "") for b in data.get("content", [])
                        if b.get("type") == "text" and b.get("text", "").strip()
                    ]
                    if text_blocks:
                        return max(text_blocks, key=len)
                    thinking_blocks = [
                        b.get("thinking", "") for b in data.get("content", [])
                        if b.get("type") == "thinking" and b.get("thinking", "").strip()
                    ]
                    if thinking_blocks:
                        return "\n".join(thinking_blocks)
                    return ""
                # OpenAI-style response
                return data.get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception:
            continue
    return ""


def analyze_with_llm(code_snippet: str, context: str, repo_path: str = "") -> dict:
    config = get_openclaw_llm_config()
    if not config["api_key"] or not config["base_url"]:
        return {"suggestion": "", "risk_level": "medium", "implementation_hint": "", "available": False}
    lang = detect_language_from_path(repo_path)
    system = (
        "You are a product reviewer. "
        "IMPORTANT: Use EXACTLY this question as your guide for EVERYTHING you output:\n"
        "\"还有什么不足, 有哪些地方可以优化, 使用体验如何？\"\n"
        "Return valid JSON with keys: "
        "  suggestion (answer to '还有什么不足, 有哪些地方可以优化, 使用体验如何？' — max 200 chars, honest and specific), "
        "  risk_level (low/medium/high), "
        "  implementation_hint (one concrete next step to address the issue, max 100 chars), "
        "  category (one of: user_complaint | friction_point | unused_feature | competitive_gap | stop_doing | add_feature). "
        "Only JSON. Be honest. Do not add features if the real issue is removing or fixing something."
    )
    prompt = (
        "IMPORTANT: Answer with ONLY a JSON object. No explanation, no markdown fences.\n\n"
        "Code:\n```" + lang + "\n" + code_snippet[:2000] + "\n```\n\n"
        "Context: " + context + "\n\n"
        "请回答：还有什么不足, 有哪些地方可以优化, 使用体验如何？"
    )
    result = call_llm(prompt=prompt, system=system, model=config["model"], base_url=config["base_url"], api_key=config["api_key"])
    if not result:
        return {"suggestion": "", "risk_level": "medium", "implementation_hint": "", "available": False, "category": "unknown"}
    try:
        parsed = json.loads(result)
        parsed["available"] = True
        if "category" not in parsed:
            parsed["category"] = "user_complaint"
        return parsed
    except json.JSONDecodeError:
        m = re.search(r'\{[^{}]*\}', result, re.DOTALL)
        if m:
            try:
                parsed = json.loads(m.group())
                parsed["available"] = True
                if "category" not in parsed:
                    parsed["category"] = "user_complaint"
                return parsed
            except Exception:
                pass
        return {"suggestion": result.strip()[:200], "risk_level": "medium", "implementation_hint": "", "available": True, "category": "user_complaint"}


# ===========================================================
# LLM-Driven Code Optimization (v3.2)
# Implements true auto-execution of optimization findings.
# ===========================================================

import tempfile
import urllib.request


def _quality_check(file_path: str, code: str) -> tuple[bool, str]:
    """
    Validate that modified code passes syntax check.
    Writes code to a temp file and runs py_compile.
    Returns (passed, error_message).
    """
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=Path(file_path).suffix, delete=False
        ) as f:
            f.write(code)
            tmp_path = f.name
        result = subprocess.run(
            ["python3", "-m", "py_compile", tmp_path],
            capture_output=True,
            text=True,
            timeout=10,
        )
        os.unlink(tmp_path)
        if result.returncode == 0:
            return True, ""
        # Extract meaningful error
        stderr = result.stderr.strip()
        if not stderr and result.stdout:
            stderr = result.stdout.strip()
        return False, stderr[:300]
    except Exception as e:
        return False, str(e)[:200]


def _rollback_optimization(repo: Repository, file_path: str, before_hash: str) -> bool:
    """
    Rollback a file to its pre-modification state using git.
    Returns True if rollback succeeded.
    """
    try:
        subprocess.run(
            ["git", "checkout", before_hash, "--", file_path],
            cwd=str(repo.resolve_path()),
            capture_output=True,
            timeout=10,
        )
        return True
    except Exception:
        return False


def _get_file_snapshot(repo: Repository, file_path: str) -> tuple[str, str]:
    """
    Get current file content and git hash before modification.
    Returns (content, git_hash). Empty string hash means file is not in git.
    """
    full_path = repo.resolve_path() / file_path
    try:
        content = full_path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return "", ""
    try:
        result = subprocess.run(
            ["git", "hash-object", file_path],
            cwd=str(repo.resolve_path()),
            capture_output=True,
            text=True,
            timeout=5,
        )
        git_hash = result.stdout.strip() if result.returncode == 0 else ""
    except Exception:
        git_hash = ""
    return content, git_hash


def _call_llm_for_refactor(
    prompt: str,
    system: str,
    file_ext: str,
    max_retries: int = 2,
) -> str:
    """
    Call LLM to generate code refactor. Returns the refactored code string.
    Falls back to empty string on failure.
    
    Retries on prose/empty responses with a stricter system prompt to improve
    reliability of code generation.
    """
    config = get_openclaw_llm_config()
    import sys as _sys
    if not config.get("api_key") or not config.get("base_url"):
        _sys.stderr.write(f"[DEBUG] LLM config empty: api_key={bool(config.get('api_key'))}, base_url={config.get('base_url')}\n")
        _sys.stderr.flush()
        return ""

    lang_map = {
        ".py": "python", ".js": "javascript", ".ts": "typescript",
        ".go": "go", ".sh": "shell", ".java": "java",
    }
    lang = lang_map.get(file_ext.lower(), "text")

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + config["api_key"],
    }
    messages = (
        ([{"role": "system", "content": system}] if system else [])
        + [{"role": "user", "content": prompt}]
    )

    # Detect API type from base_url
    base_url = config["base_url"].rstrip("/")
    if "anthropic" in base_url or config.get("model", "").lower().startswith("minimax"):
        body = {
            "model": config.get("model", "MiniMax-M2"),
            "messages": messages,
            "max_tokens": 16000,
            "temperature": 0.2,
        }
        endpoint = base_url + "/v1/messages"
    else:
        body = {
            "model": config.get("model", "MiniMax-M2"),
            "messages": messages,
            "max_tokens": 16000,
            "temperature": 0.2,
        }
        endpoint = base_url + "/chat/completions"

    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(body).encode("utf-8"),
                headers=headers,
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=60) as resp:
                data = json.loads(resp.read().decode("utf-8"))
                if "anthropic" in endpoint:
                    text_blocks = [
                        b.get("text", "") for b in data.get("content", [])
                        if b.get("type") == "text" and b.get("text", "").strip()
                    ]
                    if text_blocks:
                        content_text = max(text_blocks, key=len)
                    else:
                        thinking_blocks = [
                            b.get("thinking", "") for b in data.get("content", [])
                            if b.get("type") == "thinking" and b.get("thinking", "").strip()
                        ]
                        content_text = "\n".join(thinking_blocks)
                else:
                    content_text = (
                        data.get("choices", [{}])[0]
                        .get("message", {})
                        .get("content", "")
                    )
                stripped = _strip_code_fences(content_text)
                if stripped:
                    return stripped
                # Retry with stricter system prompt
                if attempt == 0:
                    strict_system = (
                        (system + "\n\n" if system else "")
                        + "CRITICAL: You must output ONLY code. "
                        "Start directly with 'def ' or 'class ' or equivalent. "
                        "Do not write any explanation, introduction, or description."
                    )
                    messages = (
                        [{"role": "system", "content": strict_system}]
                        if strict_system else []
                    ) + [{"role": "user", "content": prompt}]
                    body["messages"] = messages
            if attempt == max_retries - 1:
                return ""
        except urllib.error.HTTPError:
            if attempt == max_retries - 1:
                return ""
        except Exception:
            if attempt == max_retries - 1:
                return ""
    return ""


def _strip_code_fences(text: str) -> str:
    """
    Strip markdown code fences and prose from LLM output.
    
    Handles cases where LLM returns prose like "Here's the refactored code:"
    instead of actual code. Uses statistical detection (code-like line ratio)
    and pattern matching to reliably extract code.
    """
    if not text:
        return ""
    
    lines = text.strip().split("\n")
    
    # Remove leading/trailing fence lines
    while lines and "```" in lines[0]:
        lines = lines[1:]
    while lines and "```" in lines[-1]:
        lines = lines[:-1]
    
    content = "\n".join(lines).strip()
    if not content:
        return ""
    
    # Count code-like vs prose lines
    code_indicators = [
        "def ", "class ", "import ", "from ", "if ", "else:",
        "return ", "for ", "while ", "async ", "@",
        "const ", "let ", "function ", "fn ", "func ",
        "package ", "export ", "module ",
    ]
    
    non_empty_lines = [l for l in lines if l.strip()]
    prose_lines = sum(
        1 for l in non_empty_lines
        if not any(l.strip().startswith(ind) for ind in code_indicators)
    )
    total = len(non_empty_lines)
    
    # If less than 30% of non-empty lines are code-like, it's likely prose
    if total > 5 and (total - prose_lines) / total < 0.3:
        # Try to find the first code-block starting line
        for i, line in enumerate(non_empty_lines):
            stripped = line.strip()
            if any(stripped.startswith(ind) for ind in code_indicators):
                return "\n".join(non_empty_lines[i:]).strip()
        return ""  # No real code found
    
    return content


def _execute_todo_fixme(
    code: str,
    item: dict,
    repo_path: Path,
) -> tuple[str, str]:
    """
    Handle todo_fixme optimization: use LLM to analyze the TODO/FIXME
    and either remove it (if trivial), replace with explanation, or flag for manual review.
    Returns (new_code, result_description).
    """
    file_ext = Path(item["file_path"]).suffix
    lang = {"py": "python", "js": "javascript", "ts": "typescript", "go": "go"}.get(
        file_ext.lstrip("."), "text"
    )
    line_info = f"Line {item['line']}: {item['description']}"

    system = (
        f"You are a code refactoring assistant. You work with {lang} code only.\n"
        "Rules:\n"
        "1. If the TODO/FIXME is trivial (e.g. spelling, formatting, outdated note), remove it.\n"
        "2. If it references an issue that is already resolved, remove it.\n"
        "3. If it is a genuine future task, replace the TODO with a brief inline comment explaining status.\n"
        "4. NEVER fabricate functionality — only clean up existing annotations.\n"
        "5. Return ONLY the complete modified file content. No markdown fences, no explanations.\n"
        "6. Preserve all code exactly; only modify the TODO/FIXME lines.\n"
    )
    prompt = (
        f"File: {item['file_path']}\n"
        f"Issue: {line_info}\n\n"
        f"Original code:\n```{lang}\n{code}\n```\n\n"
        "Apply the cleanup rule and return the complete modified file."
    )

    new_code = _call_llm_for_refactor(prompt, system, file_ext)
    if not new_code:
        return "", "LLM call failed or no API key"
    return new_code, "todo_fixme resolved"


def _execute_duplicate_code(
    code: str,
    item: dict,
    repo_path: Path,
) -> tuple[str, str]:
    """
    Handle duplicate_code optimization: use LLM to detect the repeated pattern
    and refactor by extracting it into a constant or helper function.
    Returns (new_code, result_description).
    """
    file_ext = Path(item["file_path"]).suffix
    lang = {"py": "python", "js": "javascript", "ts": "typescript", "go": "go"}.get(
        file_ext.lstrip("."), "text"
    )
    desc = item.get("description", "")

    system = (
        f"You are an expert code refactorer. You work with {lang} only.\n"
        "CRITICAL: Return ONLY the refactored code. "
        "Do NOT write any explanation, comment, or description before or after the code. "
        "Start directly with the code (no 'here is', 'here's', 'this is', 'i would', etc.). "
        "If you cannot refactor, write 'EMPTY' and nothing else.\n"
        "Task: eliminate duplicate code by extracting repeated patterns into constants or helpers.\n"
        "Rules:\n"
        "1. Find the duplicate pattern described.\n"
        "2. Replace repeated occurrences with a constant or small helper function.\n"
        "3. Preserve all functionality exactly.\n"
        "4. Return ONLY the complete modified file content. No markdown fences, no explanation.\n"
    )
    prompt = (
        f"Language: {lang}\n"
        f"File: {item['file_path']}\n"
        f"Duplicate pattern: {desc}\n\n"
        f"Original code:\n```{lang}\n{code}\n```\n\n"
        "Refactored code (ONLY code, NO explanation):"
    )

    new_code = _call_llm_for_refactor(prompt, system, file_ext)
    if not new_code:
        return "", "LLM call failed or no valid code returned"
    return new_code, "duplicate pattern refactored"


def _execute_long_function(
    code: str,
    item: dict,
    repo_path: Path,
) -> tuple[str, str]:
    """
    Handle long_function optimization: use LLM to split a function >100 lines
    into smaller, focused sub-functions.
    Returns (new_code, result_description).
    """
    file_ext = Path(item["file_path"]).suffix
    lang = {"py": "python", "js": "javascript", "ts": "typescript", "go": "go"}.get(
        file_ext.lstrip("."), "text"
    )
    desc = item.get("description", "")

    system = (
        f"You are a code refactoring assistant. You work with {lang} only.\n"
        "Task: Split an oversized function (>100 lines) into smaller, focused functions.\n"
        "Rules:\n"
        "1. Identify logical sections within the function that can be extracted.\n"
        "2. Create helper functions with clear, descriptive names.\n"
        "3. Preserve the original function signature and all side effects.\n"
        "4. Keep the code readable and maintainable.\n"
        "5. Return ONLY the complete modified file. No markdown fences.\n"
        "6. Do NOT change any logic — only restructure.\n"
    )
    prompt = (
        f"File: {item['file_path']}\n"
        f"Finding: {desc}\n\n"
        f"Current code:\n```{lang}\n{code}\n```\n\n"
        "Split the long function into smaller functions. Return complete file."
    )

    new_code = _call_llm_for_refactor(prompt, system, file_ext)
    if not new_code:
        return "", "LLM call failed or no API key"
    return new_code, "long function refactored"


def _execute_missing_test(
    code: str,
    item: dict,
    repo_path: Path,
) -> tuple[str, str]:
    """
    Handle missing_test optimization: generate a basic test file for an untested module.
    Since we can't write a new file from an optimization finding (no file path given),
    this generates test stubs in a string for manual use or writes to tests/ directory.
    Returns (generated_test_code, result_description).
    """
    desc = item.get("description", "")
    # missing_test often has file_path="." meaning root-level scan
    # Generate test stubs based on the module structure
    file_ext = Path(item.get("file_path", "test.py")).suffix or ".py"
    lang = {"py": "python"}.get(file_ext.lstrip("."), "python")

    system = (
        "You are a testing assistant. Generate pytest-compatible test stubs.\n"
        "Rules:\n"
        "1. Create a test file with imports matching the module structure.\n"
        "2. Add placeholder test functions with pass (one per public function).\n"
        "3. Include basic assert checks where logic is obvious.\n"
        "4. Return ONLY the complete test file content. No markdown fences.\n"
    )
    prompt = (
        f"Finding: {desc}\n\n"
        "Generate a test file for the untested modules. "
        "Use pytest conventions (test_ prefix). Return complete file content."
    )

    new_code = _call_llm_for_refactor(prompt, system, ".py")
    if not new_code:
        return "", "LLM call failed or no API key"
    return new_code, "test stubs generated"


def _execute_outdated_dep(
    code: str,
    item: dict,
    repo_path: Path,
) -> tuple[str, str]:
    """
    Handle outdated_dep optimization: replace pinned version with semver range.
    Returns (new_code, result_description).
    """
    import re as _re

    desc = item.get("description", "")
    # Extract package name from the line
    match = _re.search(r"^([a-zA-Z0-9_-]+)[=<>!]+", desc, _re.MULTILINE)
    if not match:
        return "", "Could not parse package name"

    new_code = _re.sub(
        r"([a-zA-Z0-9_-]+)==[\d.]+",
        r"\1>=1.0.0,<2.0.0",
        code,
    )
    if new_code == code:
        return "", "No change needed or pattern not matched"
    return new_code, "pinned dep converted to semver range"


def execute_optimization(
    item: dict,
    code: str,
    repo: Repository,
) -> tuple[str, str]:
    """
    Main dispatcher for LLM-driven optimization execution.

    Args:
        item: Optimization finding dict with keys: type, file_path, line, description, suggestion, risk
        code: Current file content
        repo: Repository object

    Returns:
        (new_code, result_msg). Empty new_code means execution failed or was skipped.
    """
    opt_type = item.get("type") or item.get("optimization_type", "")

    if opt_type == "todo_fixme":
        return _execute_todo_fixme(code, item, repo.resolve_path())

    elif opt_type == "duplicate_code":
        return _execute_duplicate_code(code, item, repo.resolve_path())

    elif opt_type == "long_function":
        return _execute_long_function(code, item, repo.resolve_path())

    elif opt_type == "missing_test":
        return _execute_missing_test(code, item, repo.resolve_path())

    elif opt_type == "outdated_dep":
        return _execute_outdated_dep(code, item, repo.resolve_path())

    else:
        return "", f"Unknown optimization type: {opt_type}"


@dataclass
class OptimizationResult:
    """Result of executing a single optimization."""
    item_id: int
    file_path: str
    opt_type: str
    success: bool
    new_code: str = ""
    result_msg: str = ""
    before_hash: str = ""
    quality_passed: bool = False
    quality_error: str = ""


def _auto_execute_optimizations(
    all_changes: list[ChangeItem],
    all_opts: list[OptimizationFinding],
    mode: OperationMode,
    rules: dict,
    dry_run: bool,
) -> tuple[list[ChangeItem], dict]:
    """
    Execute optimization findings in full-auto mode using LLM-driven code modification.

    In full-auto mode with rules permitting the risk level, each optimization is:
      1. Loaded from disk
      2. Sent to LLM for refactoring
      3. Validated with py_compile
      4. Written back to disk on success
      5. Git-committed

    Returns (executed_change_items, stats_dict).
    """
    executed: list[ChangeItem] = []
    stats: dict = {
        "total": 0,
        "attempted": 0,
        "succeeded": 0,
        "failed": 0,
        "skipped_llm": 0,
        "quality_failed": 0,
        "by_type": {},
    }

    if mode != OperationMode.FULL_AUTO or dry_run:
        # In dry-run or non-full-auto, just report what would be executed
        executable_opts = [
            c for c in all_changes
            if c.category == ChangeCategory.OPTIMIZATION
            and should_auto_execute(rules, c.risk)
        ]
        stats["total"] = len(executable_opts)
        stats["attempted"] = 0
        if executable_opts:
            print(f"\n⚡ Full-auto would execute {len(executable_opts)} optimization(s):")
            for c in executable_opts[:10]:
                print(f"   [{c.id}] {c.optimization_type}: {c.description[:60]}")
            if len(executable_opts) > 10:
                print(f"   ... and {len(executable_opts) - 10} more")
        return [], stats

    # Full-auto mode: actually execute
    optimization_changes = [
        c for c in all_changes
        if c.category == ChangeCategory.OPTIMIZATION
        and should_auto_execute(rules, c.risk)
    ]
    stats["total"] = len(optimization_changes)

    if not optimization_changes:
        return [], stats

    print(f"\n⚡ Executing {len(optimization_changes)} optimization(s) in full-auto mode:")

    for change_item in optimization_changes:
        opt_type = change_item.optimization_type or "unknown"
        # Track by type
        stats["by_type"][opt_type] = stats["by_type"].get(opt_type, 0) + 1
        stats["attempted"] += 1

        repo = Repository(path=change_item.repo_path, type=change_item.repo_type)
        repo_path = repo.resolve_path()
        file_path = change_item.file_path

        # Skip directories and non-code files
        full_path = repo_path / file_path
        if full_path.is_dir():
            stats["skipped_llm"] += 1
            continue
        ext = Path(file_path).suffix.lower()
        if ext not in LANGUAGE_EXTENSIONS and ext != ".md":
            stats["skipped_llm"] += 1
            continue

        # Load current content
        try:
            code = full_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError) as e:
            print(f"  ❌ [{change_item.id}] {file_path}: cannot read file ({e})")
            stats["failed"] += 1
            continue

        # Snapshot before modification for rollback
        _, before_hash = _get_file_snapshot(repo, file_path)

        # Build finding-style dict for execute_optimization
        finding_dict: dict = {
            "type": opt_type,
            "file_path": file_path,
            "line": 0,
            "description": change_item.description,
            "suggestion": "",
            "risk": change_item.risk.value,
        }

        # Execute LLM-driven optimization
        try:
            new_code, result_msg = execute_optimization(finding_dict, code, repo)
        except Exception as e:
            print(f"  ❌ [{change_item.id}] {file_path}: LLM execution error ({e})")
            stats["failed"] += 1
            continue

        if not new_code:
            print(f"  ⏭️  [{change_item.id}] {file_path}: {result_msg or 'no LLM output'}")
            stats["skipped_llm"] += 1
            record_learning(finding_dict, result_msg or "skipped_llm: no valid code returned", str(repo_path))
            continue

        # Skip if no actual change was made
        if new_code.strip() == code.strip():
            print(f"  ⏭️  [{change_item.id}] {file_path}: no change produced")
            stats["skipped_llm"] += 1
            record_learning(finding_dict, "skipped_llm: no change produced", str(repo_path))
            continue

        # Quality gate: py_compile check
        quality_ok, quality_err = _quality_check(file_path, new_code)
        if not quality_ok:
            print(f"  ❌ [{change_item.id}] {file_path}: quality gate failed — {quality_err[:80]}")
            stats["quality_failed"] += 1
            stats["failed"] += 1
            record_learning(finding_dict, f"quality_failed: {quality_err[:100]}", str(repo_path))
            continue

        # Write the optimized code back
        try:
            full_path.write_text(new_code, encoding="utf-8")
        except OSError as e:
            print(f"  ❌ [{change_item.id}] {file_path}: write failed ({e})")
            # Rollback
            if before_hash:
                _rollback_optimization(repo, file_path, before_hash)
            stats["failed"] += 1
            record_learning(finding_dict, f"write_failed: {e}", str(repo_path))
            continue

        # Git commit (truncate message safely to avoid UTF-8 cutting)
        commit_msg = f"auto: {opt_type} — {change_item.description}"
        commit_msg_bytes = commit_msg.encode("utf-8")[:72].decode("utf-8", errors="ignore")
        try:
            commit_hash = git_commit(repo, commit_msg_bytes)
        except Exception as e:
            print(f"  ❌ [{change_item.id}] {file_path}: git commit failed ({e})")
            # Rollback on commit failure
            if before_hash:
                _rollback_optimization(repo, file_path, before_hash)
            stats["failed"] += 1
            record_learning(finding_dict, f"commit_failed: {e}", str(repo_path))
            continue

        # Success
        change_item.commit_hash = commit_hash
        executed.append(change_item)
        stats["succeeded"] += 1
        print(f"  ✅ [{change_item.id}] {opt_type} {file_path} ({commit_hash[:7]})")
        record_learning(finding_dict, "ok", str(repo_path))

    # Summary
    print(
        f"\n  Optimization execution: {stats['succeeded']}/{stats['attempted']} succeeded "
        f"(skipped_llm={stats['skipped_llm']}, quality_failed={stats['quality_failed']})"
    )
    return executed, stats


# ===========================================================
# Multi-Language Support
# ===========================================================

def detect_language_from_path(path: str) -> str:
    return LANGUAGE_EXTENSIONS.get(Path(path).suffix.lower(), "text")


def detect_repo_languages(repo_path: Path) -> set[str]:
    langs: set[str] = set()
    for ext in LANGUAGE_EXTENSIONS:
        if any(repo_path.rglob("*" + ext)):
            langs.add(ext)
    return langs


def get_todo_patterns_for_file(file_path: str) -> list[str]:
    return TODO_PATTERNS.get(Path(file_path).suffix.lower(), ["# TODO"])


def scan_todos_multilang(repo: Repository) -> list[OptimizationFinding]:
    findings = []
    repo_path = repo.resolve_path()
    for ext in LANGUAGE_EXTENSIONS:
        for file_path in repo_path.rglob("*" + ext):
            if any(s in str(file_path) for s in (".git", "__pycache__", "node_modules", ".iterations")):
                continue
            try:
                content = file_path.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            lang_pats = TODO_PATTERNS.get(ext, ["# TODO"])
            for i, line in enumerate(content.split("\n"), 1):
                for pat in lang_pats:
                    if pat in line:
                        idx = line.find(pat)
                        findings.append(OptimizationFinding(
                            type="todo_fixme",
                            file_path=str(file_path.relative_to(repo_path)),
                            line=i,
                            description="Unresolved: " + line[idx:].strip()[:80],
                            suggestion="Address or document this annotation",
                            risk=RiskLevel.LOW,
                        ))
                        break
    return findings


# ===========================================================
# Dependency Analysis
# ===========================================================

def extract_imports(content: str, file_path: str) -> list[str]:
    ext = Path(file_path).suffix.lower()
    imports: list[str] = []
    if ext == ".py":
        for m in re.finditer(r"^(?:from\s+([\w.]+)\s+import|import\s+([\w.]+))", content, re.MULTILINE):
            imports.append((m.group(1) or m.group(2)).split(".")[0])
    elif ext in (".js", ".ts"):
        for m in re.finditer(r"(?:require\s*\(\s*[\"']([^\"']+)[\"']\s*\)|import\s+.*?\s+from\s+[\"']([^\"']+)[\"'])", content):
            imp = m.group(1) or m.group(2)
            if imp and not imp.startswith("."):
                imports.append(imp.split("/")[0])
    elif ext == ".go":
        for m in re.finditer(r'import\s+"([^"]+)"', content):
            imports.append(m.group(1).split("/")[-1])
    elif ext == ".java":
        for m in re.finditer(r"import\s+([\w.]+);", content):
            imports.append(m.group(1).split(".")[-1])
    return imports


def build_dependency_map(repo_path: Path) -> dict[str, list[str]]:
    dep_map: dict[str, list[str]] = {}
    for ext in LANGUAGE_EXTENSIONS:
        for fp in repo_path.rglob("*" + ext):
            if any(s in str(fp) for s in (".git", "__pycache__", "node_modules")):
                continue
            try:
                dep_map[str(fp.relative_to(repo_path))] = extract_imports(
                    fp.read_text(encoding="utf-8"), str(fp)
                )
            except (UnicodeDecodeError, OSError):
                pass
    return dep_map


def find_dependents(target_file: str, dep_map: dict[str, list[str]]) -> list[str]:
    target_base = Path(target_file).stem
    return [fp for fp, imps in dep_map.items() if target_base in imps]


def analyze_dependencies(repo: Repository, changed_files: list[str]) -> dict[str, list[str]]:
    repo_path = repo.resolve_path()
    dep_map = build_dependency_map(repo_path)
    affected: dict[str, list[str]] = {}
    for changed in changed_files:
        deps = find_dependents(changed, dep_map)
        if deps:
            affected[changed] = deps
    return affected


# ===========================================================
# Test Comparison
# ===========================================================

def run_tests_for_hash(repo: Repository, ref: str) -> dict:
    repo_path = str(repo.resolve_path())
    if subprocess.run(["which", "pytest"], capture_output=True).returncode != 0:
        return {"passed": None, "coverage": None, "duration": 0.0, "error": "pytest not found"}
    subprocess.run(["git", "stash", "-q"], cwd=repo_path)
    try:
        subprocess.run(["git", "checkout", "-q", ref], cwd=repo_path)
        start = time.time()
        r = subprocess.run(["pytest", "--tb=short", "-q"], cwd=repo_path, capture_output=True, text=True, timeout=120)
        dur = time.time() - start
        passed = r.returncode == 0
        cov = None
        cr = Path(repo_path) / "coverage.xml"
        if cr.exists():
            txt = cr.read_text()
            m = re.search(r'line-rate="([0-9.]+)"', txt)
            if m:
                cov = float(m.group(1)) * 100
        return {"passed": passed, "coverage": cov, "duration": dur, "error": None}
    except subprocess.TimeoutExpired:
        return {"passed": False, "coverage": None, "duration": 120.0, "error": "timeout"}
    except Exception as e:
        return {"passed": False, "coverage": None, "duration": 0.0, "error": str(e)}
    finally:
        subprocess.run(["git", "checkout", "-q", "-"], cwd=repo_path)
        subprocess.run(["git", "stash", "pop", "-q"], cwd=repo_path)


def run_test_comparison(repo: Repository, before_hash: str, after_hash: str) -> dict:
    before = run_tests_for_hash(repo, before_hash)
    after = run_tests_for_hash(repo, after_hash)
    delta = None
    if before.get("coverage") is not None and after.get("coverage") is not None:
        delta = round(after["coverage"] - before["coverage"], 2)
    return {
        "before_coverage": before.get("coverage"),
        "after_coverage": after.get("coverage"),
        "delta": delta,
        "before_passed": before.get("passed"),
        "after_passed": after.get("passed"),
        "before_duration": before.get("duration", 0.0),
        "after_duration": after.get("duration", 0.0),
        "tests_passed": after.get("passed", False),
    }


# ===========================================================
# Contributor Tracking
# ===========================================================

def track_contributors(repo: Repository) -> dict:
    r = subprocess.run(
        ["git", "log", "--pretty=format:%H|%s|%ad", "--date=iso"],
        cwd=str(repo.resolve_path()),
        capture_output=True,
        text=True,
        timeout=10,
    )
    total = auto_count = manual_count = 0
    last_manual = None
    for line in r.stdout.strip().split("\n"):
        if not line:
            continue
        total += 1
        parts = line.split("|", 2)
        if len(parts) < 2:
            continue
        msg, date = parts[1], parts[2] if len(parts) > 2 else ""
        if msg.startswith("auto:") or msg.startswith("auto-evolve:"):
            auto_count += 1
        else:
            manual_count += 1
            if date and (last_manual is None or date > last_manual):
                last_manual = date.split()[0]
    return {
        "total_commits": total,
        "auto_commits": auto_count,
        "manual_commits": manual_count,
        "auto_percentage": round((auto_count / total) * 100, 1) if total else 0.0,
        "last_manual_commit": last_manual,
    }


# ===========================================================
# Release Management
# ===========================================================

def create_release(repo: Repository, version: str, changelog: str = "") -> None:
    repo_path = repo.resolve_path()
    tag = "v" + version.lstrip("v")
    subprocess.run(["git", "tag", tag, "-m", "Release " + version.lstrip("v")], cwd=str(repo_path), check=True)
    subprocess.run(["git", "push", "origin", tag], cwd=str(repo_path), check=True)
    r = subprocess.run(["git", "remote", "get-url", "origin"], cwd=str(repo_path), capture_output=True, text=True)
    m = re.search(r"github\.com[/:]([^/]+/[^/]+?)(?:\.git)?$", r.stdout.strip())
    if not m:
        print("Tag " + tag + " created and pushed.")
        return
    slug = m.group(1)
    notes = "# Release " + version.lstrip("v") + "\n\n" + changelog + "\n\n## auto-evolve\nManaged by auto-evolve.\n"
    gr = subprocess.run(
        ["gh", "release", "create", tag, "--title", tag, "--notes", notes, "--repo", slug],
        cwd=str(repo_path),
        capture_output=True,
        text=True,
    )
    if gr.returncode == 0:
        print("Release " + tag + " created: " + gr.stdout.strip())
    else:
        print("Tag " + tag + " created. gh failed: " + gr.stderr.strip())


# ===========================================================
# Priority Calculation
# ===========================================================

def infer_value_score(item: ChangeItem) -> int:
    """Infer value score (1-10) from change type and description."""
    desc_lower = item.description.lower()
    opt_type = (item.optimization_type or "").lower()

    if "bug" in desc_lower or "fix" in desc_lower:
        return DEFAULT_VALUE_SCORES["bug_fix"]
    if opt_type == "todo_fixme":
        return DEFAULT_VALUE_SCORES["todo_fixme"]
    if opt_type == "missing_test":
        return DEFAULT_VALUE_SCORES["add_test"]
    if opt_type == "long_function":
        return DEFAULT_VALUE_SCORES["refactor"]
    if opt_type == "duplicate_code":
        return DEFAULT_VALUE_SCORES["optimization"]
    if opt_type == "outdated_dep":
        return DEFAULT_VALUE_SCORES["optimization"]
    if "test" in desc_lower:
        return DEFAULT_VALUE_SCORES["add_test"]
    if any(kw in desc_lower for kw in ("readme", "changelog", "docs")):
        return DEFAULT_VALUE_SCORES["docs"]
    if "lint" in desc_lower or "format" in desc_lower:
        return DEFAULT_VALUE_SCORES["lint_fix"]
    return 5


def infer_risk_score(risk: RiskLevel) -> int:
    mapping = {RiskLevel.LOW: 2, RiskLevel.MEDIUM: 5, RiskLevel.HIGH: 9}
    return mapping.get(risk, 5)


def infer_cost_score(item: ChangeItem) -> int:
    desc_lower = item.description.lower()
    file_path = item.file_path.lower()
    if any(kw in desc_lower for kw in ("todo", "fixme", "lint", "format", "typo")):
        return 1
    if any(ext in file_path for ext in (".md", ".txt", ".rst")):
        if "readme" in file_path or "changelog" in file_path:
            return 2
        return 1
    if "test" in file_path or "_test." in file_path:
        return 3
    num_files = desc_lower.count(",") + 1
    if num_files <= 2:
        return 4
    elif num_files <= 5:
        return 6
    return 8


def calculate_priority(item: ChangeItem) -> float:
    value = item.value_score
    risk = item.risk_score
    cost = item.cost_score
    if risk * cost == 0:
        return 0.0
    return round((value * PRIORITY_WEIGHTS["value"]) / (risk * cost), 3)


def enrich_change_with_priority(item: ChangeItem) -> ChangeItem:
    item.value_score = infer_value_score(item)
    item.risk_score = infer_risk_score(item.risk)
    item.cost_score = infer_cost_score(item)
    item.priority = calculate_priority(item)
    return item


def sort_by_priority(items: list[ChangeItem]) -> list[ChangeItem]:
    return sorted(items, key=lambda x: x.priority, reverse=True)


def priority_color(p: float) -> str:
    if p >= 0.7:
        return "🟢"
    elif p >= 0.4:
        return "🟡"
    return "🔴"


# ===========================================================
# Config Management
# ===========================================================

def load_config() -> dict:
    if AUTO_EVOLVE_RC.exists():
        return json.loads(AUTO_EVOLVE_RC.read_text())
    return get_default_config()


def save_config(config: dict) -> None:
    AUTO_EVOLVE_RC.parent.mkdir(parents=True, exist_ok=True)
    AUTO_EVOLVE_RC.write_text(json.dumps(config, indent=2))


def get_default_config() -> dict:
    return {
        "mode": "semi-auto",
        "full_auto_rules": {
            "execute_low_risk": True,
            "execute_medium_risk": False,
            "execute_high_risk": False,
        },
        "semi_auto_rules": {
            "notify_on_each_scan": True,
            "require_confirm_before_execute": True,
        },
        "schedule_interval_hours": 168,
        "schedule_cron_id": None,
        "repositories": [
            {
                "path": str(HOME / ".openclaw" / "workspace" / "skills" / "soul-force"),
                "type": "skill",
                "visibility": "public",
                "auto_monitor": True,
            }
        ],
        "notification": {
            "mode": "log",
            "log_file": str(HOME / ".auto-evolve-notifications.log"),
        },
        "git": {
            "remote": "origin",
            "branch": "main",
            "pr_branch_prefix": "auto-evolve",
        },
    }


def config_to_repos(config: dict) -> list[Repository]:
    repos: list[Repository] = []
    for r in config.get("repositories", []):
        repos.append(Repository(
            path=r["path"],
            type=r.get("type", "skill"),
            visibility=r.get("visibility", "public"),
            auto_monitor=r.get("auto_monitor", True),
            risk_override=r.get("risk_override"),
            scan_interval_hours=r.get("scan_interval_hours", 168),
        ))
    return repos


def repos_to_config(repos: list[Repository], config: dict) -> dict:
    config["repositories"] = [
        {
            "path": r.path,
            "type": r.type,
            "visibility": r.visibility,
            "auto_monitor": r.auto_monitor,
            "risk_override": r.risk_override,
            "scan_interval_hours": r.scan_interval_hours,
        }
        for r in repos
    ]
    return config


def get_operation_mode(config: dict) -> OperationMode:
    mode_str = config.get("mode", "semi-auto")
    try:
        return OperationMode(mode_str)
    except ValueError:
        return OperationMode.SEMI_AUTO


def get_full_auto_rules(config: dict) -> dict:
    return config.get("full_auto_rules", {
        "execute_low_risk": True,
        "execute_medium_risk": False,
        "execute_high_risk": False,
    })


def should_auto_execute(rules: dict, risk: RiskLevel) -> bool:
    if risk == RiskLevel.LOW:
        return rules.get("execute_low_risk", True)
    elif risk == RiskLevel.MEDIUM:
        return rules.get("execute_medium_risk", False)
    elif risk == RiskLevel.HIGH:
        return rules.get("execute_high_risk", False)
    return False


# ===========================================================
# Learning History
# ===========================================================

def load_learnings(persona: str = "") -> dict:
    """Load learnings using per-persona path (delegates to helpers)."""
    if not persona:
        persona = detect_persona()
    p_dir = get_workspace_for_persona(persona) / ".learnings"
    approvals, rejections = [], []
    try:
        with open(p_dir / "approvals.json") as f:
            approvals = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    try:
        with open(p_dir / "rejections.json") as f:
            rejections = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    return {"approvals": approvals, "rejections": rejections}


def save_learnings(data: dict, persona: str = "") -> None:
    """Save learnings using per-persona path."""
    if not persona:
        persona = detect_persona()
    p_dir = get_workspace_for_persona(persona) / ".learnings"
    p_dir.mkdir(parents=True, exist_ok=True)
    with open(p_dir / "rejections.json", "w") as f:
        json.dump({"rejections": data.get("rejections", [])}, f, indent=2)
    with open(p_dir / "approvals.json", "w") as f:
        json.dump({"approvals": data.get("approvals", [])}, f, indent=2)


def add_learning(
    learning_type: str,
    change_id: str,
    description: str,
    reason: Optional[str],
    repo: str,
    approved_by: Optional[str] = None,
) -> None:
    data = load_learnings()
    entry: dict = {
        "id": hashlib.sha256(
            f"{change_id}{description}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:12],
        "type": learning_type,
        "change_id": str(change_id),
        "description": description,
        "reason": reason,
        "date": datetime.now(timezone.utc).date().isoformat(),
        "repo": repo,
    }
    if learning_type == "approval" and approved_by:
        entry["approved_by"] = approved_by

    if learning_type == "rejection":
        data["rejections"].insert(0, entry)
    else:
        data["approvals"].insert(0, entry)

    save_learnings(data)


def is_rejected(change_desc: str, repo: str, learnings: dict) -> bool:
    for rej in learnings.get("rejections", []):
        if rej.get("repo") == repo and rej.get("description") == change_desc:
            return True
    return False


# ===========================================================
# Git Operations
# ===========================================================

def git_run(repo: Repository, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(
        ["git"] + list(args),
        cwd=str(repo.resolve_path()),
        capture_output=True,
        text=True,
    )
    if check and result.returncode != 0:
        raise RuntimeError(f"Git command failed: git {' '.join(args)}\n{result.stderr}")
    return result


def git_status(repo: Repository) -> list[dict]:
    result = git_run(repo, "status", "--porcelain")
    if not result.stdout.strip():
        return []

    changes: list[dict] = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        status_code = line[:2]
        file_path = line[3:].strip()
        if status_code == "??":
            change_type = "untracked"
        elif status_code == "DD":
            change_type = "deleted"
        elif "D" in status_code:
            change_type = "removed"
        elif "A" in status_code:
            change_type = "added"
        else:
            change_type = "modified"
        changes.append({"type": change_type, "file": file_path})
    return changes


def git_current_branch(repo: Repository) -> str:
    result = git_run(repo, "branch", "--show-current")
    return result.stdout.strip()


def git_commit(repo: Repository, message: str) -> str:
    git_run(repo, "add", ".")
    # Check if there are staged changes before committing
    status_result = subprocess.run(
        ["git", "diff", "--cached", "--quiet"],
        cwd=str(repo.resolve_path()),
        capture_output=True,
    )
    if status_result.returncode != 0:
        # There are staged changes, commit them
        git_run(repo, "commit", "-m", message)
    else:
        # Nothing to commit, skip
        pass
    hash_result = git_run(repo, "rev-parse", "--short", "HEAD")
    return hash_result.stdout.strip()


def git_push(repo: Repository, remote: str = "origin", branch: Optional[str] = None) -> None:
    branch = branch or git_current_branch(repo)
    git_run(repo, "push", "-u", remote, branch)


def git_create_branch(repo: Repository, branch_name: str) -> None:
    git_run(repo, "checkout", "-b", branch_name)


def git_revert(repo: Repository, ref: str) -> str:
    git_run(repo, "revert", "--no-edit", ref)
    hash_result = git_run(repo, "rev-parse", "--short", "HEAD")
    return hash_result.stdout.strip()


def git_log(repo: Repository, limit: int = 50) -> list[dict]:
    result = git_run(repo, "log", "--pretty=format:%H|%s|%ad", "--date=iso", f"-n{limit}")
    commits: list[dict] = []
    for line in result.stdout.strip().split("\n"):
        if not line:
            continue
        parts = line.split("|", 2)
        if len(parts) == 3:
            commits.append({"hash": parts[0], "message": parts[1], "date": parts[2]})
    return commits


def git_diff(repo: Repository, ref: Optional[str] = None) -> str:
    if ref:
        result = git_run(repo, "diff", "--stat", ref)
    else:
        result = git_run(repo, "diff", "--stat")
    return result.stdout


def compute_file_hash(repo: Repository, file_path: str) -> Optional[str]:
    try:
        full_path = repo.resolve_path() / file_path
        if full_path.exists():
            h = hashlib.sha256()
            h.update(full_path.read_bytes())
            return h.hexdigest()[:12]
    except OSError:
        pass
    return None


def git_diff_lines_added_removed(repo: Repository) -> tuple[int, int]:
    try:
        result = git_run(repo, "diff", "--numstat", "HEAD")
        lines_added = 0
        lines_removed = 0
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            parts = line.split("\t")
            if len(parts) >= 2:
                try:
                    added = int(parts[0]) if parts[0] != "-" else 0
                    removed = int(parts[1]) if parts[1] != "-" else 0
                    lines_added += added
                    lines_removed += removed
                except ValueError:
                    pass
        return lines_added, lines_removed
    except Exception:
        return 0, 0


def get_conflict_files(repo_path: Path) -> list[str]:
    result = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=U"],
        cwd=str(repo_path),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return []
    return [f for f in result.stdout.strip().split("\n") if f]


def resolve_conflicts_simple(repo_path: Path, conflict_files: list[str]) -> None:
    for f in conflict_files:
        subprocess.run(["git", "checkout", "--theirs", f], cwd=str(repo_path), capture_output=True)
        subprocess.run(["git", "add", f], cwd=str(repo_path), capture_output=True)


def handle_pr_conflict(repo: Repository, branch: str) -> str:
    try:
        subprocess.run(
            ["git", "fetch", "origin", "main"],
            cwd=str(repo.resolve_path()),
            capture_output=True,
            text=True,
        )
        result = subprocess.run(
            ["git", "rebase", "origin/main"],
            cwd=str(repo.resolve_path()),
            capture_output=True,
            text=True,
        )
        if result.returncode == 0:
            return "clean"

        conflict_files = get_conflict_files(repo.resolve_path())
        if len(conflict_files) <= 2:
            resolve_conflicts_simple(repo.resolve_path(), conflict_files)
            cont_result = subprocess.run(
                ["git", "rebase", "--continue"],
                cwd=str(repo.resolve_path()),
                capture_output=True,
                text=True,
            )
            if cont_result.returncode == 0:
                return "auto_resolved"

        return "manual_required"
    except Exception:
        return "manual_required"


# ===========================================================
# Risk Classification
# ===========================================================

def classify_change(repo: Repository, change_type: str, file_path: str) -> RiskLevel:
    default_risk = repo.get_default_risk(change_type, file_path)
    file_lower = file_path.lower()

    high_risk_patterns = ["remove", "delete", "deprecate", "break", "rename", "migrate", "architect", "security"]
    if any(p in file_lower for p in high_risk_patterns):
        return RiskLevel.HIGH

    low_risk_patterns = ["readme", "skill.md", "changelog", ".gitignore", "license", "comments", "typo", "format", "lint", "refactor", "rename"]
    if change_type == "removed":
        if any(p in file_lower for p in ["__init__", "config", "core"]):
            return RiskLevel.HIGH
        return default_risk

    if any(p in file_lower for p in low_risk_patterns):
        return RiskLevel.LOW

    return default_risk


# ===========================================================
# Optimization Scanner
# ===========================================================

ANNOTATION_PATTERN = re.compile(r"(\b(TODO|FIXME|XXX|HACK|NOTE)\b.*?)$", re.IGNORECASE | re.MULTILINE)
PINNED_VERSION = re.compile(r"==\d+\.\d+\.\d+")


def scan_optimizations(repo: Repository) -> list[OptimizationFinding]:
    findings = []
    repo_path = repo.resolve_path()
    findings.extend(scan_todos_multilang(repo))
    for py_file in repo_path.rglob("*.py"):
        rel_path = py_file.relative_to(repo_path)
        findings.extend(_scan_python_file(py_file, rel_path))
    for ext in ("*.js", "*.ts", "*.go"):
        for code_file in repo_path.rglob(ext):
            rel_path = code_file.relative_to(repo_path)
            findings.extend(_scan_code_file(code_file, rel_path))
    findings.extend(_scan_test_coverage(repo_path, repo_path))
    findings.extend(_scan_dependencies(repo_path))
    return findings


def _scan_python_file(py_file: Path, rel_path: Path) -> list[OptimizationFinding]:
    findings = []
    try:
        content = py_file.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return findings
    findings.extend(_scan_annotations(py_file, rel_path, content=content))
    findings.extend(_scan_duplicate_code(content, rel_path))
    findings.extend(_scan_long_functions(content, rel_path))
    return findings


def _scan_annotations(file_path: Path, rel_path: Path, content: Optional[str] = None) -> list[OptimizationFinding]:
    findings = []
    if content is None:
        try:
            content = file_path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            return findings
    for i, line in enumerate(content.split("\n"), 1):
        if ANNOTATION_PATTERN.search(line):
            findings.append(OptimizationFinding(
                type="todo_fixme",
                file_path=str(rel_path),
                line=i,
                description=f"Unresolved annotation: {line.strip()}",
                suggestion="Address or document this TODO/FIXME/XXX",
                risk=RiskLevel.LOW,
            ))
    return findings


def _scan_code_file(code_file: Path, rel_path: Path) -> list[OptimizationFinding]:
    findings = []
    try:
        content = code_file.read_text(encoding="utf-8")
    except Exception:
        return findings
    lines = content.split("\n")
    open_braces = 0
    func_start = 0
    in_func = False
    func_name = ""
    for i, line in enumerate(lines):
        stripped = line.strip()
        if re.match(r"(?:export\s+)?(?:async\s+)?function\s+\w+", stripped):
            m = re.search(r"function\s+(\w+)", stripped)
            func_name = m.group(1) if m else "anon"
            func_start = i
            in_func = True
            open_braces = 0
        elif re.match(r"(?:export\s+)?(?:const|let|var)\s+\w+\s*=\s*(?:async\s+)?\(", stripped):
            m = re.search(r"(?:const|let|var)\s+(\w+)", stripped)
            func_name = m.group(1) if m else "anon"
            func_start = i
            in_func = True
            open_braces = 0
        elif re.match(r"func\s+\w+", stripped):
            m = re.search(r"func\s+(\w+)", stripped)
            func_name = m.group(1) if m else "anon"
            func_start = i
            in_func = True
            open_braces = 0
        if in_func:
            open_braces += stripped.count("{") - stripped.count("}")
            if open_braces <= 0 and "{" in stripped:
                func_lines = i - func_start + 1
                if func_lines > 100:
                    findings.append(OptimizationFinding(
                        type="long_function",
                        file_path=str(rel_path),
                        line=func_start + 1,
                        description=f"Function [{func_name}] is {func_lines} lines (>100)",
                        suggestion="Split into smaller functions",
                        risk=RiskLevel.MEDIUM,
                    ))
                in_func = False
    return findings


def _scan_duplicate_code(content: str, rel_path: Path) -> list[OptimizationFinding]:
    findings = []
    strings = re.findall(r'"""{1,}[\s\S]*?"{3}|"{1,2}[^"]{30,200}"{1,2}', content)
    string_counts: dict[str, list[int]] = {}
    for s in strings:
        key = s[:50]
        string_counts.setdefault(key, []).append(len(s))
    for key, counts in string_counts.items():
        if len(counts) >= 3:
            findings.append(OptimizationFinding(
                type="duplicate_code",
                file_path=str(rel_path),
                line=0,
                description=f"Duplicate string pattern detected ({len(counts)} occurrences)",
                suggestion="Extract repeated string into a constant or variable",
                risk=RiskLevel.LOW,
            ))
            break
    return findings


def _scan_long_functions(content: str, rel_path: Path) -> list[OptimizationFinding]:
    findings = []
    lines = content.split("\n")
    in_function = False
    func_start = 0
    func_indent = 0
    prev_func_name = ""

    for i, line in enumerate(lines):
        stripped = line.lstrip()
        indent = len(line) - len(stripped)
        func_match = re.match(r"(?:async )?def (\w+)\s*\(", stripped)
        if func_match:
            if in_function:
                func_lines = i - func_start - 1
                if func_lines > 100:
                    findings.append(OptimizationFinding(
                        type="long_function",
                        file_path=str(rel_path),
                        line=func_start + 1,
                        description=f"Function '{prev_func_name}' is {func_lines} lines (>100)",
                        suggestion="Split into smaller, focused functions",
                        risk=RiskLevel.MEDIUM,
                    ))
            in_function = True
            func_start = i
            func_indent = indent
            prev_func_name = func_match.group(1)
        elif in_function:
            if stripped and indent <= func_indent:
                func_lines = i - func_start - 1
                if func_lines > 100:
                    findings.append(OptimizationFinding(
                        type="long_function",
                        file_path=str(rel_path),
                        line=func_start + 1,
                        description=f"Function '{prev_func_name}' is {func_lines} lines (>100)",
                        suggestion="Split into smaller, focused functions",
                        risk=RiskLevel.MEDIUM,
                    ))
                in_function = False
    return findings


def _scan_test_coverage(repo_path: Path, scan_root: Path) -> list[OptimizationFinding]:
    findings = []
    tests_dir = scan_root / "tests"
    if not tests_dir.exists():
        return findings
    main_modules: set[Path] = set()
    for py_file in scan_root.rglob("*.py"):
        rel = py_file.relative_to(scan_root)
        if rel.parts[0] in ("tests", ".git", ".iterations", "__pycache__"):
            continue
        if rel.name == "__init__.py" or rel.name.startswith("_"):
            continue
        main_modules.add(rel.parent / rel.stem)
    test_modules: set[Path] = set()
    if tests_dir.exists():
        for test_file in tests_dir.rglob("test_*.py"):
            rel = test_file.relative_to(tests_dir)
            test_modules.add(rel.parent / rel.stem)
    untested = []
    for mod in sorted(main_modules):
        test_path = tests_dir / ("test_" + mod.name + ".py")
        if not test_path.exists():
            untested.append(str(mod))
    if untested:
        findings.append(OptimizationFinding(
            type="missing_test",
            file_path=".",
            line=0,
            description=f"{len(untested)} modules lack test coverage: {', '.join(untested[:5])}",
            suggestion="Add tests for the untested modules",
            risk=RiskLevel.MEDIUM,
        ))
    return findings


def _scan_dependencies(repo_path: Path) -> list[OptimizationFinding]:
    findings = []
    req_file = repo_path / "requirements.txt"
    if req_file.exists():
        try:
            content = req_file.read_text(encoding="utf-8")
            for i, line in enumerate(content.split("\n"), 1):
                line = line.strip()
                if not line or line.startswith("#") or line.startswith("-"):
                    continue
                if PINNED_VERSION.search(line):
                    findings.append(OptimizationFinding(
                        type="outdated_dep",
                        file_path="requirements.txt",
                        line=i,
                        description=f"Pinned version: {line}",
                        suggestion="Use semver range (e.g., >=1.0.0,<2.0.0)",
                        risk=RiskLevel.LOW,
                    ))
        except (UnicodeDecodeError, OSError):
            pass
    return findings


# ===========================================================
# Iteration Management
# ===========================================================

def generate_iteration_id() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%d-%H%M%S")


def ensure_iterations_dir() -> Path:
    ITERATIONS_DIR.mkdir(parents=True, exist_ok=True)
    return ITERATIONS_DIR


def load_iteration(version: str) -> dict:
    manifest_file = ITERATIONS_DIR / version / "manifest.json"
    if not manifest_file.exists():
        raise FileNotFoundError(f"Iteration {version} not found")
    return json.loads(manifest_file.read_text())


def save_iteration(
    iteration_id: str,
    manifest: IterationManifest,
    plan_lines: list[str],
    pending_items: list[dict],
    report_lines: list[str],
    alert: Optional[AlertEntry] = None,
) -> None:
    iter_dir = ensure_iterations_dir() / iteration_id
    iter_dir.mkdir(parents=True, exist_ok=True)

    manifest_dict = asdict(manifest)
    manifest_dict["items_pending_approval"] = pending_items
    manifest_dict["has_alert"] = alert is not None

    (iter_dir / "manifest.json").write_text(json.dumps(manifest_dict, indent=2))
    (iter_dir / "plan.md").write_text("\n".join(plan_lines))
    (iter_dir / "pending-review.json").write_text(json.dumps(pending_items, indent=2))
    (iter_dir / "report.md").write_text("\n".join(report_lines))

    if alert:
        alert_data = {
            "iteration_id": alert.iteration_id,
            "date": alert.date,
            "alert_type": alert.alert_type,
            "message": alert.message,
            "details": alert.details,
        }
        (iter_dir / "alert.json").write_text(json.dumps(alert_data, indent=2))


def save_metrics(metrics: IterationMetrics) -> None:
    iter_dir = ensure_iterations_dir() / metrics.iteration_id
    iter_dir.mkdir(parents=True, exist_ok=True)
    (iter_dir / "metrics.json").write_text(json.dumps(asdict(metrics), indent=2))


def update_catalog(manifest: IterationManifest) -> None:
    catalog_file = ITERATIONS_DIR / "catalog.json"
    if catalog_file.exists():
        catalog = json.loads(catalog_file.read_text())
    else:
        catalog = {"iterations": []}

    catalog["iterations"] = [
        i for i in catalog.get("iterations", [])
        if i.get("version") != manifest.version
    ]

    catalog_entry = {
        "version": manifest.version,
        "date": manifest.date,
        "status": manifest.status,
        "risk_level": manifest.risk_level,
        "items_auto": manifest.items_auto,
        "items_approved": manifest.items_approved,
        "items_rejected": manifest.items_rejected,
        "items_optimization": manifest.items_optimization,
        "rollback_of": manifest.rollback_of,
        "has_alert": manifest.has_alert,
        "metrics_id": manifest.metrics_id,
        "test_coverage_delta": manifest.test_coverage_delta,
        "contributors": manifest.contributors,
        "total_cost_usd": manifest.total_cost_usd,
        "llm_calls": manifest.llm_calls,
    }

    catalog["iterations"].insert(0, catalog_entry)
    catalog_file.parent.mkdir(parents=True, exist_ok=True)
    catalog_file.write_text(json.dumps(catalog, indent=2))


def load_catalog() -> dict:
    catalog_file = ITERATIONS_DIR / "catalog.json"
    if catalog_file.exists():
        return json.loads(catalog_file.read_text())
    return {"iterations": []}


# ===========================================================
# Quality Gates
# ===========================================================

def check_syntax(file_path: str) -> bool:
    result = subprocess.run(
        ["python3", "-m", "py_compile", file_path],
        capture_output=True,
    )
    return result.returncode == 0


def run_quality_gates(repo: Repository) -> dict:
    results: dict = {
        "passed": True,
        "syntax_ok": True,
        "syntax_errors": [],
        "lint_errors_fixed": 0,
    }
    for py_file in repo.resolve_path().rglob("*.py"):
        if not check_syntax(str(py_file)):
            results["syntax_ok"] = False
            results["syntax_errors"].append(str(py_file))
            results["passed"] = False
    return results


# ===========================================================
# Iteration Helpers (DRY: shared patterns across commands)
# ===========================================================

def _find_target_iteration(
    catalog: dict,
    iteration_id: Optional[str],
    status_filter: Optional[str] = None,
) -> tuple[Optional[dict], str]:
    """
    DRY helper: find a target iteration by ID or latest matching status.
    Returns (target_iter, iteration_id) or (None, iteration_id) on error.
    """
    if not catalog.get("iterations"):
        print("No iterations found.")
        return None, ""

    if iteration_id:
        target_iter = next(
            (i for i in catalog["iterations"] if i["version"] == iteration_id),
            None,
        )
        if not target_iter:
            print(f"Iteration {iteration_id} not found.")
            return None, ""
    else:
        if status_filter:
            target_iter = next(
                (i for i in catalog["iterations"] if i.get("status") == status_filter),
                None,
            )
            if not target_iter:
                print(f"No {status_filter} iteration found.")
                return None, ""
        else:
            return None, ""

    return target_iter, target_iter["version"]


def _load_iteration_pending(iteration_id: str) -> tuple[Optional[dict], list[dict]]:
    """DRY helper: load iteration manifest and extract pending items."""
    try:
        manifest_data = load_iteration(iteration_id)
        pending_items = manifest_data.get("items_pending_approval", [])
        return manifest_data, pending_items
    except FileNotFoundError:
        print(f"Iteration {iteration_id} manifest not found.")
        return None, []


def _finalize_iteration_status(
    iteration_id: str,
    manifest_data: dict,
    catalog: dict,
    status: str,
    **extra_fields: Any,
) -> None:
    """DRY helper: update manifest + catalog and persist both."""
    manifest_data.update({"status": status, **extra_fields})
    (ITERATIONS_DIR / iteration_id / "manifest.json").write_text(
        json.dumps(manifest_data, indent=2)
    )
    for i, cat_iter in enumerate(catalog["iterations"]):
        if cat_iter["version"] == iteration_id:
            catalog["iterations"][i].update({"status": status, **extra_fields})
            break
    (ITERATIONS_DIR / "catalog.json").write_text(json.dumps(catalog, indent=2))


# ===========================================================
# Closed-Repo Sanitization
# ===========================================================

def sanitize_pending_item(item: dict, repo: Repository) -> dict:
    if not repo.is_closed():
        return item
    sanitized = dict(item)
    if "file_path" in sanitized:
        fp = sanitized["file_path"]
        try:
            full_path = repo.resolve_path() / fp
            if full_path.exists():
                h = hashlib.sha256()
                h.update(full_path.read_bytes())
                sanitized["file_path_hash"] = h.hexdigest()[:12]
        except OSError:
            pass
        sanitized["file_path"] = "[REDACTED]"
    sanitized["description"] = "[CLOSED REPO] Change requires manual review"
    sanitized["content_redacted"] = True
    return sanitized


def sanitize_change_for_log(change: ChangeItem, repo: Repository) -> str:
    if not repo.is_closed():
        return f"{change.change_type}: {change.file_path}"
    return f"{change.change_type}: [FILE REDACTED for closed repo]"


# ===========================================================
# Execution Preview
# ===========================================================

def print_execution_preview(
    changes: list[ChangeItem],
    auto_exec: list[ChangeItem],
    mode: OperationMode,
    rules: dict,
) -> None:
    if mode == OperationMode.SEMI_AUTO:
        print("\n⚠️  Semi-Auto Mode: About to execute auto-changes:")
    else:
        print("\n⚠️  Full-Auto Mode: About to execute changes:")

    print(f"  Total: {len(auto_exec)} change(s)")
    sorted_exec = sort_by_priority(auto_exec)

    for i, c in enumerate(sorted_exec, 1):
        color = priority_color(c.priority)
        opt_badge = " [opt]" if c.category == ChangeCategory.OPTIMIZATION else ""
        risk_label = c.risk.value.upper()
        print(f"  [{i}] {color} P={c.priority:.2f} {risk_label}: {c.description[:60]}{opt_badge}")
    print()


# ===========================================================
# PR Batch Merging
# ===========================================================

def should_merge_prs(changes: list[dict]) -> bool:
    if len(changes) < 3:
        return False
    types = set(c.get("type", "") for c in changes)
    files = set(c.get("file", "") for c in changes)
    return len(types) <= 2 and len(files) <= 5


def group_similar_changes(changes: list[dict]) -> list[list[dict]]:
    if not should_merge_prs(changes):
        return [[c] for c in changes]
    by_type: dict[str, list[dict]] = {}
    for c in changes:
        t = c.get("type", "unknown")
        by_type.setdefault(t, []).append(c)
    groups: list[list[dict]] = []
    for t, type_changes in by_type.items():
        by_file: dict[str, list[dict]] = {}
        for c in type_changes:
            files_key = ",".join(sorted(c.get("file", "").split("/")[:2]))
            by_file.setdefault(files_key, []).append(c)
        for file_key, file_changes in by_file.items():
            if len(file_changes) >= 2:
                groups.append(file_changes)
            else:
                groups.extend([[c] for c in file_changes])
    return groups


def build_merged_pr_body(groups: list[list[dict]]) -> str:
    lines = ["## auto-evolve: Batch improvement", "", "### Changes", ""]
    for group in groups:
        if len(group) == 1:
            c = group[0]
            lines.append(f"- {c.get('description', c.get('change_type', 'unknown'))}")
        else:
            lines.append(f"- {len(group)} changes of type: {group[0].get('type', 'unknown')}")
            for c in group:
                lines.append(f"  - {c.get('description', c.get('file_path', 'unknown'))}")
    lines.extend(["", "### Approval", "", "This PR was auto-generated and merged for efficiency.", "Run `auto-evolve.py log` to review all changes."])
    return "\n".join(lines)


# ===========================================================
# LLM Analysis on Changes
# ===========================================================

def run_llm_analysis_on_changes(
    changes: list[ChangeItem],
    repo: Repository,
    cost_tracker: Optional[CostTracker] = None,
) -> list[ChangeItem]:
    """Run LLM analysis on pending high-priority changes. Tracks costs if CostTracker provided."""
    config = get_openclaw_llm_config()
    if not config["api_key"] or not config["base_url"]:
        return changes

    pending = [c for c in changes if c.category == ChangeCategory.PENDING_APPROVAL]
    top = sort_by_priority(pending)[:5]
    analyzed: set[int] = set()

    for item in top:
        if item.id in analyzed:
            continue
        fp = repo.resolve_path() / item.file_path
        if not fp.exists() or not fp.is_file():
            continue
        try:
            content = fp.read_text(encoding="utf-8")
        except Exception:
            continue

        ctx = f"File: {item.file_path}\nChange type: {item.change_type}\nRisk: {item.risk.value}\nCategory: {item.category.value}"
        result = analyze_with_llm(content, ctx, item.file_path)

        # v3.2: Track LLM call cost
        if cost_tracker:
            prompt_tokens = len(ctx + content[:2000]) // 4  # rough estimate
            completion_tokens = len(result.get("suggestion", "")) // 4
            cost_tracker.track_llm_call(prompt_tokens, completion_tokens, config["model"])

        if result.get("available"):
            item.llm_suggestion = result.get("suggestion", "")
            item.llm_risk = result.get("risk_level", item.risk.value)
            item.llm_implementation_hint = result.get("implementation_hint", "")
            if item.llm_risk in RISK_LEVELS:
                item.risk = RiskLevel(item.llm_risk)
                enrich_change_with_priority(item)
            analyzed.add(item.id)
            if item.llm_suggestion:
                print("  [LLM] " + item.llm_suggestion[:80])

    return changes


# ============================================================
# v3.3: Product Thinking Scanner
# Changes the question from "is the code clean?" to
# "what is broken from a USER perspective?"
# ============================================================

PRODUCT_CATEGORIES = (
    "user_complaint",
    "friction_point",
    "unused_feature",
    "competitive_gap",
    "stop_doing",
    "add_feature",
)


@dataclass
@dataclass
class PerspectiveFinding:
    """
    A finding from one of the four perspectives of the auto-evolve scan.

    Attributes:
        perspective: USER | PRODUCT | PROJECT | TECH
        description: what was found (in Chinese, human-readable)
        category: nature of the finding
        evidence: supporting snippets from code/docs
        impact_score: 0.0-1.0, how much this hurts users or the project
        suggested_direction: concrete next step in Chinese
        file_path: relevant file or '' if project-wide
        risk: risk level
        why_now: why this matters right now
    """
    description: str
    perspective: str          # USER | PRODUCT | PROJECT | TECH
    category: str             # nature of finding
    evidence: list[str]
    impact_score: float
    suggested_direction: str
    file_path: str
    risk: RiskLevel = RiskLevel.MEDIUM
    why_now: str = ""


# ===========================================================
# File Analysis Cache (v3.5)
# ===========================================================

class FileAnalysisCache:
    """
    LRU cache for file analysis results with 10-minute TTL.
    Key = (file_path, content_hash), Value = parsed JSON result.
    Persists to disk so it survives across process runs.
    """

    CACHE_FILE = Path.home() / ".openclaw" / "workspace" / ".file_analysis_cache.json"
    TTL_MS = 30 * 60 * 1000  # 30 minutes in milliseconds

    def __init__(self) -> None:
        self._memory: dict[str, dict] = {}  # key -> {result, timestamp_ms}
        self._load()

    def _load(self) -> None:
        """Load cache from disk, pruning expired entries."""
        if not self.CACHE_FILE.exists():
            return
        try:
            data = json.loads(self.CACHE_FILE.read_text(encoding="utf-8"))
            now_ms = int(time.time() * 1000)
            for key, entry in data.items():
                if now_ms - entry.get("_ts", 0) < self.TTL_MS:
                    self._memory[key] = entry
            self._save()
        except (json.JSONDecodeError, OSError):
            self._memory = {}

    def _save(self) -> None:
        """Persist memory to disk."""
        try:
            self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
            self.CACHE_FILE.write_text(
                json.dumps(self._memory, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError:
            pass

    def _make_key(self, file_path: str, content: str) -> str:
        """Build a cache key from file path and content hash."""
        h = hashlib.sha256(content.encode("utf-8")).hexdigest()[:16]
        return f"{file_path}@{h}"

    def get(self, file_path: str, content: str) -> Optional[dict]:
        """Return cached result if fresh, else None."""
        key = self._make_key(file_path, content)
        entry = self._memory.get(key)
        if entry is None:
            return None
        now_ms = int(time.time() * 1000)
        if now_ms - entry.get("_ts", 0) > self.TTL_MS:
            del self._memory[key]
            self._save()
            return None
        return entry.get("result")

    def set(self, file_path: str, content: str, result: dict) -> None:
        """Store result in cache with current timestamp."""
        key = self._make_key(file_path, content)
        self._memory[key] = {"result": result, "_ts": int(time.time() * 1000)}
        self._save()


# ===========================================================
# FourPerspectiveScanner (v3.9)
# Asks: "这个项目还有什么可以改进的？" from four distinct angles:
#   👤 USER    — Is it easy/best to use?
#   📦 PRODUCT — Does it actually solve what it claims?
#   🏗 PROJECT — Is it运作得好 (learnings, schedule, config)?
#   ⚙️ TECH   — Is the code healthy?
# ===========================================================

# Perspective labels and display info
PERSPECTIVE_META = {
    "USER":    {"icon": "👤", "label": "用户视角", "stars": 5},
    "PRODUCT": {"icon": "📦", "label": "产品视角", "stars": 4},
    "PROJECT": {"icon": "🏗", "label": "项目视角", "stars": 3},
    "TECH":    {"icon": "⚙️", "label": "技术视角", "stars": 2},
}


class FourPerspectiveScanner:
    """
    Runs four scanners concurrently (conceptually), one per perspective.

    Each perspective asks a different question and produces findings
    tagged with its perspective label.  Findings are later grouped
    and displayed by perspective in the report.
    """

    BATCH_SIZE = 5
    DOC_BATCH_SIZE = 3

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
        self._cache = FileAnalysisCache()
        # Load project-standard reference docs (评判标准)
        self._project_standard_docs = self._load_project_standard_docs()

    # ---- project-standard integration ---------------------------------------

    # Map each perspective to its reference doc
    PERSPECTIVE_REF_DOCS = {
        "USER":    "references/user/user-perspective.md",
        "PRODUCT": "references/product-requirements.md",
        "PROJECT": "references/project-inspection.md",
        "TECH":    "references/code-standards.md",
    }

    # Numeric weights per project type (4 perspectives)
    # Values: USER, PRODUCT, PROJECT, TECH
    PERSPECTIVE_WEIGHTS: dict[str, tuple[float, float, float, float]] = {
        "前端应用":    (0.35, 0.25, 0.15, 0.25),
        "后端服务":    (0.25, 0.20, 0.20, 0.35),
        "智能体/AI": (0.25, 0.30, 0.20, 0.25),
        "基础设施":    (0.15, 0.20, 0.25, 0.40),
        "内容与文档": (0.30, 0.35, 0.20, 0.15),
        "通用项目":    (0.25, 0.25, 0.25, 0.25),
    }

    # Priority order for each project type (which perspectives to check first)
    PERSPECTIVE_PRIORITY: dict[str, list[str]] = {
        "前端应用":    ["USER", "PRODUCT", "TECH", "PROJECT"],
        "后端服务":    ["TECH", "USER", "PRODUCT", "PROJECT"],
        "智能体/AI": ["PRODUCT", "USER", "TECH", "PROJECT"],
        "基础设施":    ["TECH", "PROJECT", "PRODUCT", "USER"],
        "内容与文档": ["PRODUCT", "USER", "PROJECT", "TECH"],
        "通用项目":    ["USER", "PRODUCT", "PROJECT", "TECH"],
    }

    # Built-in default reference docs (used when project-standard is not installed)
    # v4.1: These ensure auto-evolve works standalone without project-standard
    DEFAULT_REF_DOCS = {
        "USER": """## User Perspective — Built-in Default Standards

### 1. CLI / Interaction Design
- Flag names are intuitive (--dry-run not --simulate-mode)
- Reasonable defaults (don't require all flags to run)
- --help is clear, explains usage not just lists flags
- Subcommand structure is logical (git clone not git --clone)
- No unnecessary interactive prompts

### 2. Learning Curve
- README has "Quick Start" — up in 3 steps
- Has example input/output
- No dependency黑洞 (no circular install requirements)
- Error messages suggest fixes

### 3. Error Messages
- Error explains WHAT went wrong, not just "Error occurred"
- Has fix suggestions ("You may need to: ...")
- Distinguishes: config error vs runtime error vs data error
- Log levels are clear (ERROR/WARNING/INFO)

### 4. Fault Tolerance
- Operations are atomic — no half-baked state on failure
- Has backup/rollback mechanism
- Failures give clear error + recovery guide
- Idempotent: running twice has no side effects

### 5. Workflow Efficiency
- Core operations complete in <=3 steps
- Config files preferred over repeated flag passing
- Supports pipeline/chain for automation
- Has batch mode""",

        "PRODUCT": """## Product Perspective — Built-in Default Standards

### README Promises vs Reality
- README claims features — verify they are actually implemented
- "Done" markers in docs reflect actual status
- Pain points documented in README are actively worked on

### Feature Completeness
- Claimed features are complete, not half-baked
- API contract matches documentation
- Breaking changes are documented

### Docs Consistency
- Documentation says the same thing as the code
- No "TODO: document this" left in final docs
- Examples in docs are runnable

### Missing Features
- Essential features for the stated use case are present
- Common user workflows are all supported""",

        "PROJECT": """## Project Perspective — Built-in Default Standards

### Learnings Loop
- Learnings from previous inspections are tracked
- Same mistakes are not repeated
- Feedback from rejections influences future behavior

### Inspection Rhythm
- Regular inspection schedule exists (not "scan when we remember")
- auto-evolve schedule is configured and running

### Config Rationality
- No over-engineering (too many config options)
- No under-engineering (missing essential configs)
- Configuration is documented

### Dependency Health
- Dependencies are not outdated (check for old versions)
- No known security vulnerabilities in deps
- No unnecessary dependencies (bloat)

### Git Practices
- Commit messages are meaningful
- No giant PRs (break up large changes)
- Version tags exist for releases""",

        "TECH": """## Tech Perspective — Built-in Default Standards

### Code Quality
- No duplicate code blocks (DRY principle)
- Functions are short (<=50 lines)
- No magic numbers or hardcoded strings
- Naming is consistent and descriptive

### Security
- No hardcoded passwords/tokens/secrets in code
- No SQL/NoSQL injection risks (use parameterized queries)
- Authentication/authorization is properly implemented
- Input validation on all user inputs

### Performance
- No N+1 queries (lazy loading where appropriate)
- No large loops that block the event loop
- Async/await used for I/O-bound operations
- Large data sets are paginated

### Error Handling
- No bare except: clauses
- Errors are not silently swallowed
- Errors propagate correctly through call stack
- All exceptions have meaningful messages

### Testing
- Core logic has unit tests
- Tests are not just happy-path
- Test files are co-located with source files""",
    }

    def _load_project_standard_docs(self) -> dict[str, str]:
        """Load project-standard reference docs from the skills directory.

        Falls back to built-in DEFAULT_REF_DOCS if project-standard is not installed.
        """
        # Find project-standard skill directory
        skill_dirs = [
            Path.home() / ".openclaw" / "workspace" / "skills" / "project-standard",
            Path.home() / ".openclaw" / "skills" / "project-standard",
        ]
        ps_dir = None
        for d in skill_dirs:
            if d.exists():
                ps_dir = d
                break

        docs = {}
        if ps_dir is None:
            print("[FourPerspectiveScanner] project-standard not found, using built-in default standards")
            return self.DEFAULT_REF_DOCS.copy()

        print(f"[FourPerspectiveScanner] Loading project-standard from {ps_dir}")
        for perspective, rel_path in self.PERSPECTIVE_REF_DOCS.items():
            file_path = ps_dir / rel_path
            if file_path.exists():
                try:
                    docs[perspective] = file_path.read_text(encoding="utf-8")
                    print(f"  [OK] {perspective} → {rel_path}")
                except OSError as e:
                    print(f"  [FAIL] {perspective} {rel_path}: {e}")
                    docs[perspective] = self.DEFAULT_REF_DOCS.get(perspective, "")
            else:
                print(f"  [SKIP] {perspective} {rel_path} (not found) — using built-in default")
                docs[perspective] = self.DEFAULT_REF_DOCS.get(perspective, "")
        return docs

    def _detect_project_type(self, repo_path: Path) -> tuple[str, str]:
        """
        Detect project type using project-standard's v2.0 two-level classification.
        Level 1: Business form (determines inspection weights)
        Level 2: Tech stack (determines specific check items)
        Returns (level1_type, perspective_weights).
        Falls back to '通用项目' if project-standard unavailable.
        """
        # Scan for key files to determine business form
        has_skill = (repo_path / "SKILL.md").exists()
        has_meta = (repo_path / "_meta.json").exists() or (repo_path / "skill.json").exists()
        has_skill_json = (repo_path / "agent.json").exists()

        # Frontend indicators
        has_index = (repo_path / "index.html").exists()
        has_pages = (repo_path / "pages").exists() or (repo_path / "src" / "pages").exists()
        has_templates = (repo_path / "templates").exists()
        has_static = (repo_path / "static").exists()
        has_frontend = (repo_path / "frontend").exists()
        has_mobile = any((repo_path / d).exists() for d in ["ios", "android", "flutter", "react-native", "src-tauri"])
        has_desktop = any((repo_path / d).exists() for d in ["electron", "tauri", "windows", "macos"])
        has_plugin = (repo_path / "manifest.json").exists() or (repo_path / ".vsix").exists()
        has_weapp = any((repo_path / d).exists() for d in ["miniprogram", "wechat", "alipay"])

        # Backend indicators
        has_api = any((repo_path / d).exists() for d in ["routes", "controllers", "api", "grpc"])
        has_openapi = (repo_path / "openapi.yaml").exists() or (repo_path / "openapi.yml").exists()
        has_proto = any(repo_path.rglob("*.proto"))
        has_microservice = any((repo_path / d).exists() for d in ["service", "registry", "consul"])
        has_cli = (repo_path / "main.py").exists() or (repo_path / "main.go").exists()
        has_cli_indicator = (repo_path / "cli.py").exists() or (repo_path / "__main__.py").exists()
        has_console_scripts = (repo_path / "setup.py").exists() or (repo_path / "pyproject.toml").exists()
        has_middleware = any((repo_path / d).exists() for d in ["middleware", "broker", "queue"])
        has_docker = (repo_path / "Dockerfile").exists() or (repo_path / "docker-compose.yml").exists()
        has_ci = any((repo_path / f).exists() for f in [".gitlab-ci.yml", "Jenkinsfile", ".github/workflows"])

        # AI/ML indicators
        has_llm = any((repo_path / d).exists() for d in ["llm", "model", "inference", "prompt"])
        has_features = (repo_path / "features").exists() or (repo_path / "models").exists()
        has_notebooks = (repo_path / "notebooks").exists()
        has_dvc = (repo_path / "dvc.yaml").exists()
        has_etl = any((repo_path / d).exists() for d in ["etl", "pipeline", "airflow", "dbt"])

        # Infrastructure indicators
        has_firmware = any((repo_path / d).exists() for d in ["firmware", "arduino", "platformio", "embedded"])
        has_solidity = any((repo_path / d).exists() for d in ["contracts", "solidity", "hardhat"])

        # Content/Docs indicators
        has_docs = any((repo_path / d).exists() for d in ["docs", "documentation"])
        has_vitepress = (repo_path / ".vitepress").exists()
        has_mkdocs = (repo_path / "mkdocs.yml").exists()
        has_docusaurus = (repo_path / "docusaurus").exists()
        has_posts = (repo_path / "_posts").exists()
        has_swagger = (repo_path / "swagger").exists() or (repo_path / "postman").exists()

        # Python library indicator
        has_pyproject = (repo_path / "pyproject.toml").exists()
        has_setup = (repo_path / "setup.py").exists()
        has_src_import = (repo_path / "src").exists() or any(
            (repo_path / "src").exists() for _ in [1]
        )

        # === Level 1 Business Form Detection ===
        # Order matters: more specific first
        if (has_skill or has_meta or has_skill_json) and ("skill" in str(repo_path).lower() or "agent" in str(repo_path).lower()):
            return ("智能体/AI", "用户 25% / 产品 30% / 项目 20% / 技术 25%")
        elif has_llm or has_features or has_notebooks or has_dvc or has_etl:
            if has_features or has_notebooks or has_dvc:
                return ("智能体/AI", "用户 25% / 产品 30% / 项目 20% / 技术 25%")
            elif has_etl:
                return ("基础设施", "用户 15% / 产品 20% / 项目 25% / 技术 40%")
            else:
                return ("智能体/AI", "用户 25% / 产品 30% / 项目 20% / 技术 25%")
        elif has_firmware or has_solidity:
            return ("基础设施", "用户 15% / 产品 20% / 项目 25% / 技术 40%")
        elif has_mobile or has_desktop or has_weapp or has_plugin:
            return ("前端应用", "用户 35% / 产品 25% / 项目 15% / 技术 25%")
        elif has_index or has_pages or has_templates or has_static or has_frontend:
            return ("前端应用", "用户 35% / 产品 25% / 项目 15% / 技术 25%")
        elif has_api or has_openapi or has_proto or has_microservice:
            return ("后端服务", "用户 25% / 产品 20% / 项目 20% / 技术 35%")
        elif has_cli or has_cli_indicator or (has_console_scripts and has_cli):
            return ("后端服务", "用户 25% / 产品 20% / 项目 20% / 技术 35%")
        elif has_middleware or has_docker or has_ci:
            return ("后端服务", "用户 25% / 产品 20% / 项目 20% / 技术 35%")
        elif has_vitepress or has_mkdocs or has_docusaurus or has_docs:
            return ("内容与文档", "用户 30% / 产品 35% / 项目 20% / 技术 15%")
        elif has_posts or has_swagger:
            return ("内容与文档", "用户 30% / 产品 35% / 项目 20% / 技术 15%")
        elif has_pyproject and (has_setup or has_src_import):
            return ("后端服务", "用户 25% / 产品 20% / 项目 20% / 技术 35%")
        else:
            return ("通用项目", "用户 25% / 产品 25% / 项目 25% / 技术 25%")

    def _load_learnings_context(self) -> str:
        """Build a context string from learnings history, using current persona's workspace.

        v4.0: richer format includes perspective, scenario, and pattern analysis.
        """
        try:
            learnings_dir = self.memory.workspace / ".learnings"
            approvals_file = learnings_dir / "approvals.json"
            rejections_file = learnings_dir / "rejections.json"
            approvals = []
            rejections = []
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
            parts = [f"【{p} 学习历史 / Learnings History v4.0】"]

            # Pattern analysis: count rejection reasons
            if rejections:
                reason_count: dict[str, int] = {}
                for r in rejections:
                    reason = r.get("reason", "no reason")[:60]
                    reason_count[reason] = reason_count.get(reason, 0) + 1

                parts.append(f"\n{p} 之前拒绝过的改动（共 {len(rejections)} 次）:")
                # Show pattern first (why rejections happen)
                if len(reason_count) > 0:
                    top_reasons = sorted(reason_count.items(), key=lambda x: -x[1])[:3]
                    parts.append("  常见拒绝原因（TOP3）:")
                    for reason, count in top_reasons:
                        parts.append(f"    - [{count}x] {reason}")
                # Recent rejections
                for r in rejections[-3:]:
                    scenario = r.get("scenario", "")
                    persp = r.get("perspective", "")
                    desc = r.get("description", "")[:70]
                    reason = r.get("reason", "")[:50]
                    parts.append(f"  - 拒绝[{persp}]: {desc} | 因: {reason} | 场景: {scenario or '(未记录)'}")
            if approvals:
                parts.append(f"\n{p} 之前批准过的改动（共 {len(approvals)} 次）:")
                for a in approvals[-5:]:
                    persp = a.get("perspective", "")
                    desc = a.get("description", "")[:80]
                    direction = a.get("suggested_direction", "")[:50]
                    parts.append(f"  - 批准[{persp}]: {desc} | 方向: {direction or '(未记录)'}")
            return "\n".join(parts)
        except Exception:
            return f"No learnings history yet for {self.effective_persona}."

    # ---- P1: Scan History Persistence ----------------------------------------

    def _scan_history_file(self, repo_path: Path) -> Path:
        """Path to scan history JSON for a repo."""
        ae_dir = repo_path / ".auto-evolve"
        ae_dir.mkdir(exist_ok=True)
        return ae_dir / "scan-history.json"

    def _load_scan_history(self, repo_path: Path) -> dict[str, list[dict]]:
        """Load previous scan findings grouped by perspective.

        Returns:
            { "USER": [{description, category, impact_score}, ...], ... }
        """
        history_file = self._scan_history_file(repo_path)
        if not history_file.exists():
            return {}
        try:
            data = json.loads(history_file.read_text(encoding="utf-8"))
            # data is { repo_path: [scan_round1, scan_round2, ...] }
            # Each scan_round is {perspective: [findings]}
            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, list) and len(v) > 0:
                        # Return the most recent scan round
                        return v[0] if isinstance(v[0], dict) else {}
                    elif isinstance(v, dict):
                        return v
            return {}
        except Exception:
            return {}

    def _save_scan_history(self, repo_path: Path, findings: list["PerspectiveFinding"]) -> None:
        """Save current scan findings to history for trend analysis.

        v4.3: Stores multiple scan rounds (last 10) for trend tracking.
        Structure: { repo_path: [latest_round, prev_round, ...] }
        """
        history_file = self._scan_history_file(repo_path)
        try:
            # Group findings by perspective
            by_perspective: dict[str, list[dict]] = {}
            for f in findings:
                persp = f.perspective
                if persp not in by_perspective:
                    by_perspective[persp] = []
                by_perspective[persp].append({
                    "description": f.description.replace("[NEW] ", ""),
                    "category": f.category,
                    "impact_score": f.impact_score,
                    "file_path": f.file_path,
                    "timestamp": __import__("datetime").datetime.now().isoformat(),
                })

            new_round = by_perspective
            key = str(repo_path.resolve())

            # Load existing history
            existing: dict[str, list] = {}
            if history_file.exists():
                try:
                    existing = json.loads(history_file.read_text(encoding="utf-8"))
                except Exception:
                    existing = {}

            # Prepend new round, keep last 10
            if key in existing and isinstance(existing[key], list):
                existing[key] = [new_round] + existing[key]
                existing[key] = existing[key][:10]
            else:
                existing[key] = [new_round]

            history_file.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")
        except Exception as e:
            print(f"  [WARN] Could not save scan history: {e}")

    def _is_new_finding(self, finding: "PerspectiveFinding", prev_findings: list[dict]) -> bool:
        """Check if a finding is NEW (not in previous scan) or still open."""
        if not prev_findings:
            return True
        # Strip [NEW] prefix for comparison
        desc = finding.description.replace("[NEW] ", "")
        for prev in prev_findings:
            prev_desc = prev.get("description", "").replace("[NEW] ", "")
            if prev_desc == desc and finding.category == prev.get("category"):
                return False
        return True

    # ---- P2: GitHub Integration ---------------------------------------------

    def post_github_comment(self, repo_path: Path, findings: list["PerspectiveFinding"],
                             github_event: str = "scan") -> bool:
        """Post scan results as a GitHub PR comment or create an issue.

        Uses GITHUB_TOKEN env var for API authentication.
        """
        import os, urllib.request, urllib.parse

        token = os.environ.get("GITHUB_TOKEN", "")
        if not token:
            print("[GitHub] GITHUB_TOKEN not set, skipping comment")
            return False

        # Try to detect GitHub context from git remote
        remote_url = self._get_github_remote(repo_path)
        if not remote_url:
            print("[GitHub] Could not detect GitHub remote, skipping")
            return False

        owner, repo = remote_url

        # Format findings as GitHub markdown (with trend if repo_path available)
        body = self._format_github_comment(findings, github_event, repo_path=repo_path)

        # Determine if this is a PR comment or issue
        pr_number = os.environ.get("PR_NUMBER", "")
        issue_number = os.environ.get("ISSUE_NUMBER", "")

        # v4.4: Check for existing auto-evolve issue, update it instead of creating new
        existing_issue = self._find_auto_evolve_issue(token, owner, repo)
        if existing_issue:
            self._update_issue(token, owner, repo, existing_issue["number"], body)
            print(f"[GitHub] Updated existing issue #{existing_issue['number']}")
            ok = True
        else:
            ok = self._create_issue(token, owner, repo, body)
        # Also post PR comment if this is from a PR
        if pr_number:
            self._post_pr_comment(token, owner, repo, pr_number, body)
        return ok

    def _get_github_remote(self, repo_path: Path) -> tuple[str, str] | None:
        """Get (owner, repo) from git remote URL."""
        try:
            result = __import__("subprocess").run(
                ["git", "remote", "get-url", "origin"],
                cwd=str(repo_path), capture_output=True, text=True, timeout=10
            )
            url = result.stdout.strip()
            # git@github.com:owner/repo.git or https://github.com/owner/repo.git
            if "github.com" in url:
                if url.startswith("git@"):
                    parts = url.split(":")[1].rstrip(".git").split("/")
                else:
                    parts = url.split("github.com/")[1].rstrip(".git").split("/")
                if len(parts) >= 2:
                    return parts[0], parts[1]
        except Exception:
            pass
        return None

    def _format_github_comment(self, findings: list["PerspectiveFinding"],
                                event: str,
                                repo_path: Path = None) -> str:
        """Format findings as GitHub-flavored markdown with trend summary.

        v4.4: Shows all four perspectives even on All Clear.
        """
        lines = [
            f"## 🔍 Auto-Evolve Scan Results (`{event}`)",
            "",
        ]

        # Trend summary
        if repo_path:
            trend = self._get_scan_trend(repo_path)
            if trend:
                lines.append(trend)
                lines.append("")

        emoji_map = {"USER": "👤", "PRODUCT": "📦", "PROJECT": "🏗", "TECH": "⚙️"}
        label_map = {
            "USER": "User Perspective",
            "PRODUCT": "Product Perspective",
            "PROJECT": "Project Perspective",
            "TECH": "Tech Perspective",
        }
        all_perspectives = ["USER", "PRODUCT", "PROJECT", "TECH"]

        if not findings:
            lines.append("✅ **All Clear** — No issues found.")
            lines.append("")
            # Show all four perspectives were checked
            for persp in all_perspectives:
                lines.append(f"{emoji_map.get(persp, "📋")} {label_map.get(persp, persp)}: 0 findings")
            lines.append("")
            lines.append("_This project passed the auto-evolve inspection._")
            lines.append("---")
            lines.append("_Auto-evolved by [auto-evolve](https://github.com/relunctance/auto-evolve)_")
            return "\n".join(lines)

        # Group findings by perspective
        by_perspective: dict[str, list["PerspectiveFinding"]] = {}
        for f in findings:
            by_perspective.setdefault(f.perspective, []).append(f)

        lines.append(f"Found **{len(findings)}** finding(s) across {len(by_perspective)} perspective(s):")
        lines.append("")

        for persp in all_perspectives:
            persp_findings = by_perspective.get(persp, [])
            count = len(persp_findings)
            lines.append(f"### {emoji_map.get(persp, "📋")} {label_map.get(persp, persp)} ({count} findings)")
            for f in persp_findings:
                is_new = "[NEW]" in f.description
                marker = "🆕 " if is_new else "  "
                lines.append(f"{marker}**[{f.impact_score:.0%}]** {f.description}")
                if f.file_path:
                    lines.append(f"   - File: `{f.file_path}`")
                if f.suggested_direction:
                    lines.append(f"   - Fix: {f.suggested_direction}")
                lines.append("")

        lines.append("---")
        lines.append("_Auto-evolved by [auto-evolve](https://github.com/relunctance/auto-evolve)_")
        return "\n".join(lines)

    def _get_scan_trend(self, repo_path: Path) -> str:
        """Build trend summary from scan history. v4.3."""
        history_file = self._scan_history_file(repo_path)
        if not history_file.exists():
            return ""

        try:
            data = json.loads(history_file.read_text(encoding="utf-8"))
            if isinstance(data, dict):
                for v in data.values():
                    if isinstance(v, dict) and len(v) >= 2:
                        # We have at least 2 scans — build trend
                        all_scans = []
                        for persp, findings in v.items():
                            if isinstance(findings, list) and len(findings) > 0:
                                all_scans.append({
                                    "perspective": persp,
                                    "count": len(findings),
                                    "findings": findings,
                                })

                        if len(all_scans) < 2:
                            return ""

                        latest = all_scans[0]
                        prev = all_scans[1] if len(all_scans) > 1 else None

                        if prev:
                            delta = latest["count"] - prev["count"]
                            delta_str = f"{delta:+d}" if delta != 0 else "0"
                            emoji = "📈" if delta > 0 else ("📉" if delta < 0 else "➡️")
                            trend_line = (
                                f"{emoji} **Trend**: {prev['count']} → **{latest['count']}** findings "
                                f"({delta_str}) since last scan"
                            )
                            return trend_line
        except Exception:
            pass
        return ""

    def _post_pr_comment(self, token: str, owner: str, repo: str,
                         pr_number: str, body: str) -> bool:
        """Post a comment on a GitHub PR."""
        import urllib.request, json

        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
        data = json.dumps({"body": body}).encode()
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "auto-evolve/4.2")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status in (200, 201):
                    print(f"[GitHub] Posted comment on PR #{pr_number}")
                    return True
        except Exception as e:
            print(f"[GitHub] Failed to post PR comment: {e}")
        return False

    def _create_issue(self, token: str, owner: str, repo: str,
                       body: str, title: str = "Auto-Evolve Scan Results") -> bool:
        """Create a GitHub issue with scan results."""
        import urllib.request, json

        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        data = json.dumps({"title": title, "body": body, "labels": ["auto-evolve"]}).encode()
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "auto-evolve/4.2")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status in (200, 201):
                    result = json.loads(resp.read())
                    print(f"[GitHub] Created issue #{result.get('number', '?')}")
                    return True
        except Exception as e:
            print(f"[GitHub] Failed to create issue: {e}")
        return False

    def _create_issue_comment(self, token: str, owner: str, repo: str,
                               issue_number: str, body: str) -> bool:
        """Post a comment on an existing GitHub issue."""
        import urllib.request, json

        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}/comments"
        data = json.dumps({"body": body}).encode()
        req = urllib.request.Request(url, data=data, method="POST")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "auto-evolve/4.2")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                if resp.status in (200, 201):
                    print(f"[GitHub] Posted comment on issue #{issue_number}")
                    return True
        except Exception as e:
            print(f"[GitHub] Failed to post issue comment: {e}")
        return False

    def _find_auto_evolve_issue(self, token: str, owner: str, repo: str) -> dict | None:
        """Find the most recent open auto-evolve issue for this repo. v4.4."""
        import urllib.request, json

        url = f"https://api.github.com/repos/{owner}/{repo}/issues"
        url += "?state=open&labels=auto-evolve&per_page=10&sort=created&direction=desc"
        req = urllib.request.Request(url)
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                issues = json.loads(resp.read())
                for issue in issues:
                    if "Auto-Evolve Scan" in issue.get("title", ""):
                        return issue
        except Exception:
            pass
        return None

    def _update_issue(self, token: str, owner: str, repo: str,
                       issue_number: int, body: str) -> bool:
        """Update an existing GitHub issue with new scan results. v4.4."""
        import urllib.request, json

        url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
        data = json.dumps({"body": body}).encode()
        req = urllib.request.Request(url, data=data, method="PATCH")
        req.add_header("Authorization", f"Bearer {token}")
        req.add_header("Accept", "application/vnd.github+json")
        req.add_header("X-GitHub-Api-Version", "2022-11-28")
        req.add_header("User-Agent", "auto-evolve/4.4")
        try:
            with urllib.request.urlopen(req, timeout=15) as resp:
                return resp.status in (200, 201)
        except Exception as e:
            print(f"[GitHub] Failed to update issue #{issue_number}: {e}")
            return False

    def scan(self) -> list[PerspectiveFinding]:
        """
        Run all four perspective scanners and merge their findings.

        Workflow:
          1. Detect project type (via project-standard/project-types.md)
          2. Scan from 4 perspectives in priority order (project-type-dependent)
          3. Each perspective uses project-standard's reference docs + weights
        """
        all_findings: list[PerspectiveFinding] = []
        print(f"[FourPerspectiveScanner] Starting 4-perspective scan of {len(self.repos)} repos...")
        for repo in self.repos:
            if not repo.auto_monitor:
                continue
            repo_path = repo.resolve_path()
            if not repo_path.exists():
                continue

            # Step 1: Detect project type
            project_type, weights_str = self._detect_project_type(repo_path)
            numeric_weights = self.PERSPECTIVE_WEIGHTS.get(project_type, (0.25, 0.25, 0.25, 0.25))
            priority_order = self.PERSPECTIVE_PRIORITY.get(project_type, ["USER", "PRODUCT", "PROJECT", "TECH"])
            weight_map = dict(zip(["USER", "PRODUCT", "PROJECT", "TECH"], numeric_weights))

            print(f"\n  [TYPE] {project_type}")
            print(f"  [WEIGHTS] " + " / ".join(f"{p}={weight_map[p]*100:.0f}%" for p in priority_order))

            # Load scan history for this repo (P1: persistence)
            scan_history = self._load_scan_history(repo_path)

            # Step 2: Scan in priority order
            print(f"\n  Scanning {repo_path.name} in order: {' → '.join(priority_order)}")
            for perspective in priority_order:
                meta = PERSPECTIVE_META[perspective]
                weight = weight_map[perspective]
                print(f"    [{perspective}] {meta['icon']} {meta['label']} (weight={weight:.0%})...")
                findings = self._scan_by_perspective(
                    repo, perspective, project_type,
                    weight=weight,
                    prev_findings=scan_history.get(perspective, [])
                )
                if findings:
                    print(f"      → Found {len(findings)} finding(s)")
                    # Mark which are new vs still open
                    for f in findings:
                        is_new = self._is_new_finding(f, scan_history.get(perspective, []))
                        if is_new:
                            f.description = f"[NEW] {f.description}"
                all_findings.extend(findings)

            # Save updated scan history
            self._save_scan_history(repo_path, all_findings)

        all_findings.sort(key=lambda f: f.impact_score, reverse=True)
        return all_findings

    def _scan_by_perspective(self, repo: Repository, perspective: str,
                              project_type: str = "通用项目",
                              weight: float = 0.25,
                              prev_findings: list = None) -> list[PerspectiveFinding]:
        """Dispatch to the right perspective scanner, passing project type + weight."""
        if perspective == "USER":
            return self._scan_user(repo, project_type, weight)
        elif perspective == "PRODUCT":
            return self._scan_product(repo, project_type, weight)
        elif perspective == "PROJECT":
            return self._scan_project(repo, project_type, weight)
        elif perspective == "TECH":
            return self._scan_tech(repo, project_type, weight)
        return []

    def _scan_user(self, repo: Repository, project_type: str = "通用项目",
                   weight: float = 0.25) -> list[PerspectiveFinding]:
        """
        👤 用户视角: Is it easy and pleasant to use?
        Uses project-standard's user/user-perspective.md as evaluation criteria.
        v4.2: Weight-aware scanning + prior findings context.
        """
        config = get_openclaw_llm_config()
        if not config.get("api_key") or not config.get("base_url"):
            return []
        repo_path = repo.resolve_path()
        context = self._gather_context(repo)
        ref_doc = self._project_standard_docs.get("USER", "")

        # Build weight-aware focus instruction
        if weight >= 0.30:
            focus = "此项目用户视角权重较高，请格外仔细检查用户体验问题，优先发现 CLI/交互/上手门槛问题。"
        elif weight >= 0.20:
            focus = "此项目用户视角权重中等，按标准检查即可。"
        else:
            focus = "此项目用户视角权重较低，可以简略检查，重点放在其他高权重视角。"

        prompt = (
            f"你收到了这条飞书消息：\n"
            f"\"你觉得 {repo_path.name} 这个工具好用吗？有什么用户体验不好的地方？\"\n\n"
            f"【项目类型】{project_type} | 用户视角权重: {weight:.0%}\n"
            f"【重点提示】{focus}\n"
            f"【你的身份】\n{self.effective_persona}\n"
            f"【上下文】\n{self.master_summary[:500]}\n"
            f"【用户偏好】\n"
            f"  喜欢: {', '.join(self.hawk_prefs.get('liked', [])[:3]) or '(无)'}\n"
            f"  不喜欢: {', '.join(self.hawk_prefs.get('disliked', [])[:3]) or '(无)'}\n\n"
            f"【评判标准 - 用户视角】\n"
            f"{ref_doc[:3000] if ref_doc else '(无可用标准，使用内置检查项)'}\n\n"
            f"从用户视角分析，重点关注：\n"
            f"  1. CLI 设计是否直观（参数名、默认值、help文案）\n"
            f"  2. 错误提示是否说人话\n"
            f"  3. 新人上手门槛（文档够吗？）\n"
            f"  4. 容错性（某一步失败了会怎样？）\n"
            f"  5. 操作流程度（完成一件事要几步？）\n\n"
            f"返回 JSON 数组，每个元素：\n"
            f"  insight: (string, 中文) 你发现了什么用户体验问题\n"
            f"  category: (string) cli_design | error_message | learning_curve | fault_tolerance | workflow\n"
            f"  impact: (float 0.0-1.0) 对用户体验的影响程度\n"
            f"  evidence: (array) 支持你观点的代码/文档片段（1-2条，每条<80字）\n"
            f"  suggested_fix: (string, 中文) 具体改进建议\n"
            f"  why_now: (string, 中文) 为什么现在重要\n"
            f"  repo_path: (string) 相关文件或空字符串\n\n"
            f"如果没有发现任何用户体验问题，返回空数组 []。\n"
            f"Context:\n{context[:6000]}"
        )
        result = call_llm(prompt=prompt, system="你是一个资深用户体验专家。回复中文。",
                          model=config["model"], base_url=config["base_url"], api_key=config["api_key"])
        return self._parse_llm_findings(result, "USER")

    def _scan_product(self, repo: Repository, project_type: str = "通用项目",
                      weight: float = 0.25) -> list[PerspectiveFinding]:
        """
        📦 产品视角: Does it actually solve what it claims to solve?
        Uses project-standard's product-requirements.md as evaluation criteria.
        v4.2: Weight-aware scanning.
        """
        config = get_openclaw_llm_config()
        if not config.get("api_key") or not config.get("base_url"):
            return []
        repo_path = repo.resolve_path()
        context = self._gather_context(repo)
        ref_doc = self._project_standard_docs.get("PRODUCT", "")

        if weight >= 0.30:
            focus = "此项目产品视角权重最高，请仔细核查 README/SKILL.md 承诺是否兑现。"
        elif weight >= 0.20:
            focus = "此项目产品视角权重中等，按标准检查即可。"
        else:
            focus = "此项目产品视角权重较低，可以简略检查。"

        prompt = (
            f"你收到了这条飞书消息：\n"
            f"\"你觉得 {repo_path.name} 还有什么可以优化的地方？有什么不足？\"\n\n"
            f"【项目类型】{project_type} | 产品视角权重: {weight:.0%}\n"
            f"【重点提示】{focus}\n"
            f"【你的身份】\n{self.effective_persona}\n"
            f"【上下文】\n{self.master_summary[:500]}\n\n"
            f"【评判标准 - 产品视角】\n"
            f"{ref_doc[:3000] if ref_doc else '(无可用标准，使用内置检查项)'}\n\n"
            f"你要分析：这个项目声称解决什么问题？它真的解决了吗？\n\n"
            f"关注：\n"
            f"  1. README/SKILL.md 里 ❌ 标记的痛点，哪些还没解决？\n"
            f"  2. 声称的功能，是完整实现还是半成品？\n"
            f"  3. 文档和代码说的是同一件事吗？\n"
            f"  4. 有什么应该有的功能却缺失了？\n\n"
            f"返回 JSON 数组，每个元素：\n"
            f"  insight: (string, 中文) 发现了什么产品级问题\n"
            f"  category: (string) pain_point_unresolved | partial_solution | missing_feature | wrong_approach\n"
            f"  pain_point: (string) 你参考的原始文档中记录的痛点\n"
            f"  impact: (float 0.0-1.0) 对产品价值的影响\n"
            f"  evidence: (array) 支持观点的文档/代码片段（1-2条）\n"
            f"  suggested_fix: (string, 中文) 具体改进建议\n"
            f"  why_now: (string, 中文) 为什么现在重要\n"
            f"  repo_path: (string) 相关文件或空字符串\n\n"
            f"如果没有发现任何产品级问题，返回空数组 []。\n"
            f"Context:\n{context[:6000]}"
        )
        result = call_llm(prompt=prompt, system="你是一个严格的产品评审专家。回复中文。",
                          model=config["model"], base_url=config["base_url"], api_key=config["api_key"])
        return self._parse_llm_findings(result, "PRODUCT")

    def _scan_project(self, repo: Repository, project_type: str = "通用项目",
                     weight: float = 0.25) -> list[PerspectiveFinding]:
        """
        🏗 项目视角: Is the project运作得好？
        Uses project-standard's project-inspection.md as evaluation criteria.
        v4.2: Weight-aware scanning.
        """
        config = get_openclaw_llm_config()
        if not config.get("api_key") or not config.get("base_url"):
            return []
        repo_path = repo.resolve_path()
        learnings = self.learnings
        iterations_dir = repo_path / ".iterations"
        ref_doc = self._project_standard_docs.get("PROJECT", "")

        if weight >= 0.25:
            focus = "此项目项目视角权重较高，请仔细检查运作健康度、巡检节奏和依赖管理。"
        else:
            focus = "此项目项目视角权重较低，可以简略检查。"

        learnings_status = "无" if "No learnings" in learnings else f"有 {learnings.count(chr(10))} 条记录"
        iteration_count = len(list(iterations_dir.glob("*"))) if iterations_dir.exists() else 0

        prompt = (
            f"你收到了这条飞书消息：\n"
            f"\"你觉得 {repo_path.name} 这个项目在运作方式上有什么问题？\"\n\n"
            f"【项目类型】{project_type} | 项目视角权重: {weight:.0%}\n"
            f"【重点提示】{focus}\n"
            f"【你的身份】\n{self.effective_persona}\n"
            f"【上下文】\n{self.master_summary[:400]}\n"
            f"【项目状态】\n"
            f"  learnings历史: {learnings_status}\n"
            f"  巡检迭代次数: {iteration_count}\n\n"
            f"【评判标准 - 项目视角】\n"
            f"{ref_doc[:3000] if ref_doc else '(无可用标准，使用内置检查项)'}\n\n"
            f"从项目运作视角分析，关注：\n"
            f"  1. learnings有没有形成闭环（上一次发现的问题追踪了吗？）\n"
            f"  2. 巡检是否有稳定的节奏（还是想起来才扫一次？）\n"
            f"  3. 配置是否合理（有没有过度配置或缺失必要配置？）\n"
            f"  4. 依赖管理是否健康（依赖是否过多、过旧？）\n\n"
            f"返回 JSON 数组，每个元素：\n"
            f"  insight: (string, 中文) 发现了什么项目运作问题\n"
            f"  category: (string) learnings_gap | scan_rhythm | config_issue | dependency_issue\n"
            f"  impact: (float 0.0-1.0) 对项目长期健康的影响\n"
            f"  evidence: (array) 支持观点的证据（1-2条）\n"
            f"  suggested_fix: (string, 中文) 具体改进建议\n"
            f"  why_now: (string, 中文) 为什么现在重要\n"
            f"  repo_path: (string) 相关文件或空字符串\n\n"
            f"如果没有发现任何项目运作问题，返回空数组 []。\n"
            f"Learnings历史:\n{learnings[:1000]}"
        )
        result = call_llm(prompt=prompt, system="你是一个项目管理和工程效率专家。回复中文。",
                          model=config["model"], base_url=config["base_url"], api_key=config["api_key"])
        return self._parse_llm_findings(result, "PROJECT")

    def _parse_llm_findings(self, raw_result: str, perspective: str) -> list[PerspectiveFinding]:
        """Parse raw LLM output into a list of PerspectiveFinding."""
        if not raw_result:
            return []
        try:
            parsed = json.loads(raw_result)
        except json.JSONDecodeError:
            m = re.search(r'\[[\s\S]*\]', raw_result)
            if m:
                try:
                    parsed = json.loads(m.group())
                except Exception:
                    return []
            else:
                return []
        if not isinstance(parsed, list):
            return []
        findings: list[PerspectiveFinding] = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            insight = item.get("insight", "").strip()
            if not insight:
                continue
            findings.append(PerspectiveFinding(
                description=insight,
                perspective=perspective,
                category=item.get("category", "unknown"),
                evidence=[str(e)[:80] for e in item.get("evidence", [])[:2]],
                impact_score=float(item.get("impact", 0.5)),
                suggested_direction=str(item.get("suggested_fix", item.get("suggested_direction", "")))[:150],
                file_path=str(item.get("repo_path", "")),
                risk=RiskLevel.MEDIUM,
                why_now=str(item.get("why_now", ""))[:80],
            ))
        return findings

    def _scan_tech(self, repo: Repository, project_type: str = "通用项目",
                  weight: float = 0.25) -> list[PerspectiveFinding]:
        """
        ⚙️ 技术视角: Is the code healthy?
        Uses project-standard's code-standards.md as evaluation criteria.

        v4.2: LLM-driven scan + project-type-aware checks (security + performance) + weight-aware.
        """
        config = get_openclaw_llm_config()
        repo_path = repo.resolve_path()

        # Load project-standard TECH reference doc
        ref_doc = self._project_standard_docs.get("TECH", "")

        # 1. Run existing optimization scanner (TODO/FIXME/duplicates)
        findings = scan_optimizations(repo)
        risk_to_impact = {"low": 0.3, "medium": 0.5, "high": 0.7, "critical": 0.9}
        result: list[PerspectiveFinding] = []
        for f in findings:
            result.append(PerspectiveFinding(
                description=f.description,
                perspective="TECH",
                category=f.type,
                evidence=[f"{f.file_path}:{f.line}" if f.file_path else ""],
                impact_score=risk_to_impact.get(f.risk.value, 0.5),
                suggested_direction="优化代码质量",
                file_path=f.file_path or "",
                risk=f.risk,
                why_now="技术债务积累",
            ))

        # 2. LLM-driven security + performance scan (v4.0 enhancement)
        if config.get("api_key") and config.get("base_url"):
            tech_findings = self._scan_tech_llm(repo, project_type, ref_doc)
            result.extend(tech_findings)

        return result

    def _scan_tech_llm(self, repo: Repository, project_type: str,
                        ref_doc: str) -> list[PerspectiveFinding]:
        """LLM-driven security and performance checks, tailored by project_type."""
        config = get_openclaw_llm_config()
        repo_path = repo.resolve_path()
        context = self._gather_context(repo)

        tech_focus_map = {
            "前端应用": "前端性能(首屏/加载优化)、XSS/CSRF、依赖安全",
            "后端服务": "API安全(注入/鉴权)、N+1查询、内存泄漏",
            "智能体/AI": "Prompt注入、数据泄露、模型信息暴露、API Key硬编码",
            "基础设施": "资源泄漏、OTA安全、内存溢出、错误处理缺失",
            "内容与文档": "静态资源安全、链接有效性、构建产物安全",
        }
        tech_focus = tech_focus_map.get(project_type, "通用代码质量、安全漏洞、性能问题")

        prompt_parts = [
            "你收到了这条消息：",
            f"你觉得 {repo_path.name} 这个项目在技术层面有什么问题？",
            "",
            f"[项目类型] {project_type}，技术检查重点：{tech_focus}",
            f"[你的身份] {self.effective_persona}",
            f"[上下文] {self.master_summary[:400]}",
            "",
            "[评判标准 - 技术视角]",
            "参考 project-standard 的技术标准：",
            ref_doc[:2500] if ref_doc else "(无可用标准，使用内置检查项)",
            "",
            "重点检查（根据项目类型）：",
            "  " + tech_focus,
            "",
            "通用检查项：",
            "  1. 安全漏洞：硬编码密码/Token/Secret、SQL/NoSQL注入风险、XSS",
            "  2. 性能问题：N+1查询，大循环，内存泄漏，同步阻塞",
            "  3. 代码质量：重复代码，长函数(>100行)，硬编码magic number",
            "  4. 异常处理：裸except，吞掉异常，错误传播缺失",
            "",
            "返回 JSON 数组，每个元素：",
            "  insight: (string, 中文) 发现了什么技术问题",
            "  category: (string) security | performance | code_quality | error_handling",
            "  impact: (float 0.0-1.0) 对系统稳定性/安全的影响",
            "  evidence: (array) 支持观点的代码片段（1-2条，每条<100字）",
            "  suggested_fix: (string, 中文) 具体修复建议",
            "  why_now: (string, 中文) 为什么现在重要",
            "  repo_path: (string) 相关文件",
            "",
            "如果没有发现任何技术问题，返回空数组 []。",
            "Context: " + context[:5000],
        ]
        prompt = "\n".join(prompt_parts)

        result_raw = call_llm(
            prompt=prompt,
            system="你是一个资深技术评审专家，专注于代码安全、性能和架构质量。回复中文。",
            model=config["model"],
            base_url=config["base_url"],
            api_key=config["api_key"],
        )
        return self._parse_llm_findings(result_raw, "TECH")


    def _gather_context(self, repo: Repository) -> str:
        """Gather all available context for holistic analysis."""
        repo_path = repo.resolve_path()
        parts = []

        # README content (first 4000 chars)
        for fname in ["README.md", "README.zh-CN.md"]:
            fp = repo_path / fname
            if fp.exists():
                try:
                    content = fp.read_text(encoding="utf-8")[:4000]
                    parts.append(f"\n\n=== {fname} (excerpt) ===\n{content}")
                    break
                except Exception:
                    pass

        # SKILL.md (first 2000 chars)
        sk = repo_path / "SKILL.md"
        if sk.exists():
            try:
                parts.append(f"\n\n=== SKILL.md (excerpt) ===\n{sk.read_text(encoding='utf-8')[:2000]}")
            except Exception:
                pass

        # Main script (first 200 lines)
        main_scripts = list(repo_path.glob("scripts/*.py"))
        if main_scripts:
            main_script = sorted(main_scripts, key=lambda p: p.stat().st_size, reverse=True)[0]
            try:
                lines = main_script.read_text(encoding="utf-8").splitlines()[:200]
                parts.append(f"\n\n=== Main script: {main_script.name} (first 200 lines) ===\n" + "\n".join(lines))
            except Exception:
                pass

        # Learnings (last 5 approvals + rejections)
        learnings = self.learnings
        if learnings and learnings != f"No learnings history yet for {self.effective_persona}.":
            parts.append(f"\n\n=== Learnings history ===\n{learnings[:1000]}")

        # Hawk-bridge preferences
        if self.hawk_prefs.get("disliked") or self.hawk_prefs.get("liked"):
            liked = ", ".join(self.hawk_prefs.get("liked", [])[:3])
            disliked = ", ".join(self.hawk_prefs.get("disliked", [])[:3])
            parts.append(f"\n\n=== Owner preferences (hawk-bridge) ===\nLiked: {liked or '(none)'}\nDisliked: {disliked or '(none)'}")

        return "\n".join(parts)

    def _holistic_review(self, repo: Repository) -> list[PerspectiveFinding]:
        """
        Single LLM call that mirrors how a human would think when asked:
        'What can be improved in this project?'
        
        Asks the LLM to think from the owner's perspective, forming real opinions
        rather than running a checklist. Output is human-readable, not a code report.
        """
        config = get_openclaw_llm_config()
        if not config.get("api_key") or not config.get("base_url"):
            return []

        repo_path = repo.resolve_path()
        context = self._gather_context(repo)

        system = (
            f"You are a sharp, experienced developer who just received a Feishu message "
            f"from the owner of this project. The message says:\n\n"
            f"\"你觉得 {repo_path.name} 还有什么可以优化的地方？有什么不足？\"\n\n"
            f"You are {self.effective_persona}. You use this project. "
            f"You have opinions. You are NOT a static analyzer.\n\n"
            f"【Context about you】\n{self.master_summary[:800]}\n\n"
            f"【What you like/dislike】\n"
            f"  Liked: {', '.join(self.hawk_prefs.get('liked', [])[:3]) or '(none)'}\n"
            f"  Disliked: {', '.join(self.hawk_prefs.get('disliked', [])[:3]) or '(none)'}\n\n"
            f"【Your learnings from past reviews】\n{self.learnings[:600]}\n\n"
            "Answer the owner's Feishu message directly. Form a real opinion.\n"
            "Think about:\n"
            "  - What does this project CLAIM to do? Is it actually doing it well?\n"
            "  - What would frustrate you as a user of this project?\n"
            "  - What's awkward, counterintuitive, or missing?\n"
            "  - What have you seen in similar projects that is better?\n"
            "  - What looks like it was half-implemented or copy-pasted?\n\n"
            "IMPORTANT: Your response must be a JSON array. Each item is ONE finding.\n"
            "Be specific. 'The code could be cleaner' is NOT a finding. "
            "'The repeated SoulForgeConfig initialization (15x) suggests no shared setup function' IS.\n\n"
            "Return a JSON array with one object per finding:\n"
            "  finding_id: short unique string\n"
            "  insight: (Chinese, 50-200 chars) what you genuinely think is wrong or missing\n"
            "  category: one of: product_gap | structural_code | user_friction | missing_feature | partial_implementation\n"
            "  impact: (0.0-1.0) how much this hurts the project or its users\n"
            "  evidence: (array of 1-3 short text snippets from the code/docs that support this)\n"
            "  suggested_fix: (Chinese, 50-150 chars) what you would do to fix it\n"
            "  why_now: (Chinese, 50 chars) why this matters right now\n"
            "  repo_path: (string) relative path to the relevant file, or '' if project-wide\n\n"
            "If you genuinely have nothing meaningful to say, return [] (empty array).\n"
            "Do NOT list duplicate_code or long_function findings — those are handled separately.\n"
            "Do NOT repeat pain points already documented in the files.\n"
            "Think like a user, not a linter."
        )

        prompt = (
            f"You received this Feishu message:\n"
            f"\"你觉得 {repo_path.name} 还有什么可以优化的地方？有什么不足？\"\n\n"
            f"Here is the project context:\n{context}\n\n"
            "Reply as if you are a developer who uses this project daily. "
            "Be honest, specific, and helpful. Return ONLY a JSON array."
        )

        result = call_llm(
            prompt=prompt,
            system=system,
            model=config["model"],
            base_url=config["base_url"],
            api_key=config["api_key"],
        )

        if not result:
            print(f"  [Holistic] LLM returned empty — skipping")
            return []

        try:
            parsed = json.loads(result)
        except json.JSONDecodeError:
            m = re.search(r'\[[\s\S]*\]', result)
            if m:
                try:
                    parsed = json.loads(m.group())
                except Exception:
                    print(f"  [Holistic] Could not parse LLM response as JSON")
                    return []
            else:
                print(f"  [Holistic] Could not parse LLM response as JSON")
                return []

        if not isinstance(parsed, list):
            print(f"  [Holistic] LLM returned non-array: {type(parsed)}")
            return []

        findings: list[PerspectiveFinding] = []
        for item in parsed:
            if not isinstance(item, dict):
                continue
            insight = item.get("insight", "").strip()
            if not insight:
                continue
            finding = PerspectiveFinding(
                description=insight,
                category=item.get("category", "product_gap"),
                evidence=item.get("evidence", [])[:3],
                impact_score=float(item.get("impact", 0.5)),
                suggested_direction=item.get("suggested_fix", ""),
                file_path=item.get("repo_path", ""),
                risk=RiskLevel.MEDIUM,
                why_now=item.get("why_now", ""),
            )
            findings.append(finding)

        print(f"  [Holistic] Found {len(findings)} human-level insights")
        return findings

    def _scan_product_docs(self, repo: Repository) -> list[PerspectiveFinding]:
        """
        Phase 1: Read README.md, README.zh-CN.md, SKILL.md and extract documented
        pain points. Ask LLM which of these pain points are still unresolved.
        """
        findings: list[PerspectiveFinding] = []
        repo_path = repo.resolve_path()

        doc_files = []
        for fname in ["README.md", "README.zh-CN.md", "SKILL.md"]:
            fp = repo_path / fname
            if fp.exists():
                try:
                    content = fp.read_text(encoding="utf-8")
                except (UnicodeDecodeError, OSError):
                    continue
                if len(content) > 8000:
                    content = content[:8000]
                doc_files.append((str(fp.relative_to(repo_path)), content))

        if not doc_files:
            print(f"  [Phase 1] No doc files found — skipping product doc scan")
            return findings

        print(f"  [Phase 1] Found {len(doc_files)} doc file(s): {[f[0] for f in doc_files]}")

        # Check cache for each doc file
        uncached: list[tuple[str, str]] = []
        for rel_path, content in doc_files:
            cached = self._cache.get(rel_path, content)
            if cached:
                parsed_list = cached.get("results", [])
                for item in parsed_list:
                    finding = self._parse_finding(item, rel_path)
                    if finding:
                        findings.append(finding)
                        print(f"    [cache hit] {rel_path}")
            else:
                uncached.append((rel_path, content))

        if not uncached:
            return findings

        # Batch uncached doc files
        total_batches = (len(uncached) + self.DOC_BATCH_SIZE - 1) // self.DOC_BATCH_SIZE
        print(f"  [Phase 1] {len(uncached)} doc files uncached — batching into {total_batches} LLM call(s)")
        for batch_idx in range(total_batches):
            batch = uncached[batch_idx * self.DOC_BATCH_SIZE:(batch_idx + 1) * self.DOC_BATCH_SIZE]
            results = self._batch_analyze_product_docs(batch, repo)
            for rel_path, content in batch:
                result = results.get(rel_path, {})
                self._cache.set(rel_path, content, result)
                # result is a dict with "results": list[parsed_items]
                for item in result.get("results", []):
                    finding = self._parse_finding(item, rel_path)
                    if finding:
                        findings.append(finding)

        return findings

    def _batch_analyze_product_docs(
        self, batch: list[tuple[str, str]], repo: Repository
    ) -> dict[str, dict]:
        """
        Analyze a batch of product doc files (README/SKILL.md).
        Extract documented pain points, then ask LLM which ones are STILL broken.
        Returns dict: file_path -> {results: [list of findings]}
        """
        config = get_openclaw_llm_config()
        if not config.get("api_key") or not config.get("base_url"):
            return {}

        hawk_block = ""
        if self.hawk_prefs.get("disliked"):
            hawk_block += "\n\n主人不喜欢的东西：\n" + "\n".join(
                f"  - {d}" for d in self.hawk_prefs["disliked"][:3]
            )
        if self.hawk_prefs.get("liked"):
            hawk_block += "\n\n主人喜欢的东西：\n" + "\n".join(
                f"  - {l}" for l in self.hawk_prefs["liked"][:3]
            )

        # Build doc sections with pain point extraction context
        doc_sections: list[str] = []
        for rel_path, content in batch:
            doc_sections.append(
                f"--- FILE: {rel_path} ---\n{content[:6000]}"
            )
        docs_block = "\n\n".join(doc_sections)

        system = (
            f"You are a product reviewer for the OpenClaw ecosystem.\n\n"
            f"【Persona: {self.effective_persona}】\n"
            f"【Context】\n{self.master_summary}\n"
            f"【Preferences】\n{hawk_block or '(无偏好记忆)'}\n\n"
            "You are analyzing a project that CLAIMS to solve certain problems.\n"
            "Your job: Look at the documented pain points in the files below, then identify\n"
            "which of those claimed problems are STILL BROKEN or only partially solved.\n\n"
            "Look specifically for:\n"
            "  - Pain points labeled ❌ in the documentation\n"
            "  - 'Core Problem' sections describing what's broken\n"
            "  - 'Pain Points' tables listing unsolved issues\n"
            "  - 'Before vs After' examples where 'After' is still weak\n"
            "  - Features that claim to solve X but evidence shows X is still happening\n\n"
            "Answer with a JSON array. Each element must have:\n"
            "  file_path: (string) the source file\n"
            "  insight: (string, Chinese) what's still broken, specific and honest\n"
            "  category: one of: pain_point_unresolved | partial_solution | wrong_approach | missing_feature\n"
            "  pain_point: (string) the ORIGINAL documented pain point you're referencing\n"
            "  impact: (float 0.0-1.0) how much this still hurts users\n"
            "  evidence: (array) 1-2 short text snippets from the doc or your reasoning\n"
            "  suggested_direction: (string, Chinese) one concrete next step\n"
            "  why_now: (string) why this matters right now\n\n"
            "If all documented pain points appear genuinely solved, return [] (empty array).\n"
            "Be specific. 'It works' is not a finding. 'The pain point is still present because X' is."
        )

        prompt = (
            "IMPORTANT: Answer with ONLY a JSON array. No fences, no explanation outside JSON.\n\n"
            f"{docs_block}\n\n"
            "Identify which documented pain points are STILL BROKEN. "
            "Return a JSON array, one element per finding."
        )

        result = call_llm(
            prompt=prompt,
            system=system,
            model=config["model"],
            base_url=config["base_url"],
            api_key=config["api_key"],
        )

        if not result:
            return {}

        output: dict[str, dict] = {}
        for rel_path, content in batch:
            output[rel_path] = {"results": []}

        try:
            parsed = json.loads(result)
        except json.JSONDecodeError:
            m = re.search(r'\[[\s\S]*\]', result)
            if m:
                try:
                    parsed = json.loads(m.group())
                except Exception:
                    return output
            else:
                return output

        if not isinstance(parsed, list):
            return output

        # Map findings back to their source files
        for item in parsed:
            if not isinstance(item, dict):
                continue
            fp = item.get("file_path", "")
            if fp in output:
                output[fp]["results"].append(item)
            else:
                # Assign to first file if file_path not matched
                first_key = next(iter(output), None)
                if first_key:
                    output[first_key]["results"].append(item)

        return output

    def _scan_code_files(self, repo: Repository) -> list[PerspectiveFinding]:
        """
        Phase 2: Scan code files for implementation quality.
        NOTE: README/SKILL.md/SOUL.md/AGENTS.md are handled by _scan_product_docs.
        """
        findings: list[PerspectiveFinding] = []
        repo_path = repo.resolve_path()

        # Only code files — docs handled by _scan_product_docs
        skip_names = {
            "README.md", "README.zh-CN.md", "SKILL.md",
            "SOUL.md", "AGENTS.md", "MEMORY.md", "TOOLS.md",
            "USER.md", "IDENTITY.md", "HEARTBEAT.md",
            "BOOTSTRAP.md",
        }

        priority_files: list[tuple[Path, str, str]] = []
        for script in list(repo_path.glob("scripts/*.py")) + list(repo_path.glob("*.py")):
            if script.name in skip_names:
                continue
            if script.exists():
                priority_files.append((script, str(script.relative_to(repo_path)), ""))

        # 2. Load content and partition into cached vs. needs-analysis
        uncached: list[tuple[str, str, str]] = []  # (rel_path, content, cache_key)
        for fp, rel, _ in priority_files:
            try:
                content = fp.read_text(encoding="utf-8")
            except (UnicodeDecodeError, OSError):
                continue
            if len(content) > 8000:
                content = content[:8000]
            cached = self._cache.get(rel, content)
            if cached:
                finding = self._parse_finding(cached, rel)
                if finding:
                    findings.append(finding)
                    print(f"  [cache hit] {rel}")
            else:
                uncached.append((rel, content, rel))  # rel = cache key

        if not uncached:
            return findings

        # 3. Batch uncached files (BATCH_SIZE per LLM call)
        total_batches = (len(uncached) + self.BATCH_SIZE - 1) // self.BATCH_SIZE
        print(f"  [cache miss] {len(uncached)} files — batching into {total_batches} LLM call(s)")
        for batch_idx in range(total_batches):
            batch = uncached[batch_idx * self.BATCH_SIZE:(batch_idx + 1) * self.BATCH_SIZE]
            results = self._batch_analyze(batch, repo)
            for rel, content, _ in batch:
                result = results.get(rel)
                if result:
                    self._cache.set(rel, content, result)
                    finding = self._parse_finding(result, rel)
                    if finding:
                        findings.append(finding)

        return findings

    def _batch_analyze(
        self, batch: list[tuple[str, str, str]], repo: Repository
    ) -> dict[str, dict]:
        """
        Send a batch of up to BATCH_SIZE files to LLM in a single call.
        Returns a dict mapping file_path -> parsed JSON result.
        """
        config = get_openclaw_llm_config()
        if not config.get("api_key") or not config.get("base_url"):
            return {}

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

        # Build per-file sections for the prompt
        file_sections: list[str] = []
        for rel_path, content, _ in batch:
            lang = detect_language_from_path(rel_path)
            file_sections.append(
                f"--- FILE: {rel_path} ---\n```{lang}\n{content[:4000]}\n```"
            )
        files_block = "\n\n".join(file_sections)

        system = (
            f"You are the CONTINUOUS IMPROVEMENT PARTNER for persona: {self.effective_persona}.\n\n"
            "IMPORTANT: Answer the SAME question for EACH file listed below.\n"
            "Question: \"还有什么不足, 有哪些地方可以优化, 使用体验如何？\"\n\n"
            f"【{self.effective_persona} 上下文】\n"
            f"{self.master_summary}\n"
            f"【{self.effective_persona} 偏好】\n"
            f"{hawk_block}\n"
            "【学习历史】\n"
            f"{self.learnings}\n\n"
            "Answer with ONLY a JSON array. No markdown fences, no explanation.\n"
            "Each element must have keys: "
            "  file_path (string, match the name exactly), "
            "  insight (max 150 chars, honest, in Chinese), "
            "  category (one of: user_complaint | friction_point | unused_feature | competitive_gap | stop_doing | add_feature | ok), "
            "  impact (0.0 to 1.0), "
            "  evidence (array of 1-2 short text snippets, each max 80 chars), "
            "  suggested_direction (max 100 chars), "
            "  why_now (max 80 chars). "
            "If a file is fine, use category 'ok' and impact 0.0 with empty insight."
        )

        prompt = (
            "IMPORTANT: Answer with ONLY a JSON array. No fences, no text outside the array.\n\n"
            f"{files_block}\n\n"
            "Return a JSON array with one entry per file, in the same order."
        )

        result = call_llm(
            prompt=prompt,
            system=system,
            model=config["model"],
            base_url=config["base_url"],
            api_key=config["api_key"],
        )

        if not result:
            return {}

        output: dict[str, dict] = {}
        # Try parsing as a JSON array
        try:
            parsed = json.loads(result)
        except json.JSONDecodeError:
            # Try to extract array from mixed output
            m = re.search(r'\[[\s\S]*\]', result)
            if m:
                try:
                    parsed = json.loads(m.group())
                except Exception:
                    return {}
            else:
                return {}

        if not isinstance(parsed, list):
            return {}

        for item in parsed:
            if not isinstance(item, dict):
                continue
            fp = item.get("file_path", "")
            if fp:
                output[fp] = item

        return output

    def _parse_finding(self, parsed: dict, file_path: str, perspective: str = "PRODUCT") -> Optional[PerspectiveFinding]:
        """Parse a cached or LLM-parsed dict into a PerspectiveFinding."""
        insight = parsed.get("insight", "").strip()
        category = parsed.get("category", "")
        impact = float(parsed.get("impact", 0.0))
        if not insight or category == "ok" or impact == 0.0:
            return None
        return PerspectiveFinding(
            description=insight,
            perspective=perspective,
            category=category,
            evidence=parsed.get("evidence", []),
            impact_score=impact,
            suggested_direction=parsed.get("suggested_direction", ""),
            why_now=parsed.get("why_now", ""),
            file_path=file_path,
            risk=RiskLevel.MEDIUM,
        )

    def _analyze_learnings_patterns(self, repo: Repository) -> list[PerspectiveFinding]:
        findings: list[PerspectiveFinding] = []
        learnings = load_learnings()
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
                findings.append(PerspectiveFinding(
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
                findings.append(PerspectiveFinding(
                    description=(
                        f"Stop attempting this: '{desc}' — rejected {count} times. "
                        "The system keeps generating changes nobody wants."
                    ),
                    category="unused_feature",
                    evidence=[f"Rejected {count} times: {desc}"],
                    impact_score=min(1.0, count * 0.25),
                    suggested_direction=f"Add to learnings blocklist.",
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
                findings.append(PerspectiveFinding(
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


def print_product_findings(findings: list[PerspectiveFinding]) -> None:
    """Display findings grouped by perspective with icons and impact bars."""
    if not findings:
        print(f"\n🎯 Product Evolution Insights: none (all clear — or LLM returned empty)")
        return

    # Group by perspective
    by_perspective: dict[str, list[PerspectiveFinding]] = {}
    for f in findings:
        by_perspective.setdefault(f.perspective, []).append(f)

    print(f"\n🎯 Four-Perspective Insights ({len(findings)} total):")
    print("=" * 62)

    # Icons per category
    category_icons = {
        # USER
        "cli_design": "🎨",
        "error_message": "📛",
        "learning_curve": "📉",
        "fault_tolerance": "🛡",
        "workflow": "🔗",
        # PRODUCT
        "pain_point_unresolved": "🚨",
        "partial_solution": "⚠️",
        "missing_feature": "❌",
        "wrong_approach": "🔄",
        # PROJECT
        "learnings_gap": "🔁",
        "scan_rhythm": "⏰",
        "config_issue": "⚙️",
        "dependency_issue": "📦",
        # TECH
        "duplicate_code": "📋",
        "long_function": "📏",
        "missing_test": "🧪",
        "dead_code": "💀",
    }

    # Display order: USER > PRODUCT > PROJECT > TECH
    for perspective in ["USER", "PRODUCT", "PROJECT", "TECH"]:
        items = by_perspective.get(perspective, [])
        if not items:
            continue
        meta = PERSPECTIVE_META[perspective]
        stars = "⭐" * meta["stars"]
        print(f"\n{'━' * 62}")
        print(f"{meta['icon']} {meta['label']} {stars}")
        print(f"{'━' * 62}")

        for i, f in enumerate(items[:10], 1):
            icon = category_icons.get(f.category, "❓")
            impact_bar = "█" * int(f.impact_score * 10) + "░" * (10 - int(f.impact_score * 10))
            risk_label = f.risk.value.upper()
            print(f"\n  {i}. {icon} {risk_label} [{f.category}]")
            print(f"     {f.description}")
            if f.evidence:
                print(f"     Evidence: {' | '.join(str(e)[:60] for e in f.evidence[:2])}")
            print(f"     Impact: {impact_bar} {f.impact_score:.1f}")
            if f.suggested_direction:
                print(f"     → {f.suggested_direction}")
            if f.why_now:
                print(f"     ⏱ {f.why_now}")
            if f.file_path:
                print(f"     📄 {f.file_path}")

        if len(items) > 10:
            print(f"\n  ... and {len(items) - 10} more in {meta['label']}")

    print(f"\n{'=' * 62}")
    print(f"📌 行动优先级：用户 > 产品 > 项目 > 技术")


# ===========================================================
# Main Scan Logic
# ===========================================================

def run_scan(
    repo: Repository,
    dry_run: bool = False,
    learnings: Optional[dict] = None,
    before_snapshots: Optional[dict[str, dict]] = None,
    cost_tracker: Optional[CostTracker] = None,
) -> tuple[list[ChangeItem], list[OptimizationFinding], list[str], dict[str, dict]]:
    """
    Run a full scan on a repository.
    Returns: (changes, optimizations, plan_lines, after_snapshots)
    """
    changes: list[ChangeItem] = []
    opts: list[OptimizationFinding] = []
    plan_lines: list[str] = []
    change_id = 1
    learnings = learnings or {"rejections": [], "approvals": []}

    # Take before snapshot for effect tracking
    if before_snapshots is not None:
        effect_tracker = EffectTracker()
        before_snapshots[repo.path] = effect_tracker.snapshot(repo.resolve_path())

    # 1. Git changes
    git_changes = git_status(repo)
    changed_files = [gc["file"] for gc in git_changes]

    # Dependency analysis
    dep_affected: dict[str, list[str]] = {}
    if changed_files:
        dep_affected = analyze_dependencies(repo, changed_files)
        for changed, deps in dep_affected.items():
            print("  [!] Dependency Alert: Changing: " + changed)
            for dep in deps:
                print("     May affect: " + dep)

    for gc in git_changes:
        if is_rejected(gc["file"], repo.path, learnings):
            continue
        risk = classify_change(repo, gc["type"], gc["file"])
        category = ChangeCategory.AUTO_EXEC if risk == RiskLevel.LOW else ChangeCategory.PENDING_APPROVAL
        item = ChangeItem(
            id=change_id,
            description=f"{gc['type']}: {gc['file']}",
            file_path=gc["file"],
            change_type=gc["type"],
            risk=risk,
            category=category,
            repo_path=repo.path,
            repo_type=repo.type,
        )
        if gc["file"] in dep_affected:
            item.affected_files = dep_affected[gc["file"]]
        enrich_change_with_priority(item)
        changes.append(item)
        change_id += 1

    # 2. Proactive optimizations
    opts = scan_optimizations(repo)
    for o in opts:
        if is_rejected(o.description, repo.path, learnings):
            continue
        item = ChangeItem(
            id=change_id,
            description=f"[opt] {o.type}: {o.description}",
            file_path=o.file_path,
            change_type="optimization",
            risk=o.risk,
            category=ChangeCategory.OPTIMIZATION,
            repo_path=repo.path,
            repo_type=repo.type,
            optimization_type=o.type,
        )
        enrich_change_with_priority(item)
        changes.append(item)
        change_id += 1

    # Take after snapshot
    after_snapshots: dict[str, dict] = {}
    if before_snapshots is not None:
        effect_tracker = EffectTracker()
        after_snapshots[repo.path] = effect_tracker.snapshot(repo.resolve_path())

    return changes, opts, plan_lines, after_snapshots


# ===========================================================
# Metrics Generation
# ===========================================================

def generate_metrics(
    iteration_id: str,
    todos_resolved: int,
    lint_errors_fixed: int,
    files_changed: int,
    lines_added: int,
    lines_removed: int,
    quality_gate_passed: bool,
) -> IterationMetrics:
    return IterationMetrics(
        iteration_id=iteration_id,
        date=datetime.now(timezone.utc).isoformat(),
        todos_resolved=todos_resolved,
        lint_errors_fixed=lint_errors_fixed,
        test_coverage_delta=0.0,
        files_changed=files_changed,
        lines_added=lines_added,
        lines_removed=lines_removed,
        quality_gate_passed=quality_gate_passed,
    )


def compute_todos_resolved(changes: list[ChangeItem]) -> int:
    return sum(1 for c in changes if c.optimization_type == "todo_fixme" or "todo" in c.description.lower())


# ===========================================================
# Cron Integration
# ===========================================================

def setup_cron(interval_hours: int) -> bool:
    result = subprocess.run(["which", "openclaw"], capture_output=True)
    if result.returncode != 0:
        return False

    cmd = [
        "openclaw", "cron", "add",
        "--name", "auto-evolve-scan",
        "--every", f"{interval_hours}h",
        "--message", "exec python3 ~/.openclaw/workspace/skills/auto-evolve/scripts/auto-evolve.py scan",
    ]
    add_result = subprocess.run(cmd, capture_output=True, text=True)
    if add_result.returncode == 0:
        cron_id_match = re.search(r"cron[_-]?id[:\s]+([\w-]+)", add_result.stdout + add_result.stderr)
        cron_id = cron_id_match.group(1) if cron_id_match else None
        config = load_config()
        config["schedule_cron_id"] = cron_id
        save_config(config)
        return True
    return False


def remove_cron() -> bool:
    result = subprocess.run(["which", "openclaw"], capture_output=True)
    if result.returncode != 0:
        return False
    config = load_config()
    cron_id = config.get("schedule_cron_id")
    cmd = ["openclaw", "cron", "remove"]
    if cron_id:
        cmd.append(cron_id)
    else:
        cmd.append("auto-evolve-scan")
    rem_result = subprocess.run(cmd, capture_output=True, text=True)
    if rem_result.returncode == 0:
        config["schedule_cron_id"] = None
        save_config(config)
        return True
    return False


# ===========================================================
# Pending Review
# ===========================================================

def load_pending_review(iteration_id: str) -> list[dict]:
    try:
        return json.loads((ITERATIONS_DIR / iteration_id / "pending-review.json").read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_pending_review(iteration_id: str, items: list[dict]) -> None:
    (ITERATIONS_DIR / iteration_id / "pending-review.json").write_text(json.dumps(items, indent=2))


# ===========================================================
# Commands
# ===========================================================

# ===========================================================
# cmd_scan helpers (reduce function length)
# ===========================================================

def _scan_repos(
    config: dict,
    args,
    learnings: dict,
    before_snapshots: dict[str, dict],
    cost_tracker: CostTracker,
    iteration_id: str,
) -> tuple[list[ChangeItem], list[OptimizationFinding], dict[str, dict], list[Repository], Optional[AlertEntry], dict]:
    """
    Scan all configured repositories.
    Returns (all_changes, all_opts, after_snapshots, repos, alert, qg).
    """
    repos = config_to_repos(config)
    all_changes: list[ChangeItem] = []
    all_opts: list[OptimizationFinding] = []
    after_snapshots: dict[str, dict] = {}
    alert: Optional[AlertEntry] = None
    qg_result: dict = {}

    for repo in repos:
        if not repo.auto_monitor:
            print(f"\n⏭️  Skipping {repo.path} (auto_monitor=false)")
            continue
        if not repo.resolve_path().exists():
            print(f"\n⚠️  Repository not found: {repo.path}")
            continue

        print(f"\n📦 Scanning: {repo.path} ({repo.type})")

        qg_result = run_quality_gates(repo)
        if not qg_result["passed"]:
            print(f"  ⚠️  Quality gate failed: {len(qg_result['syntax_errors'])} syntax error(s)")
            alert = AlertEntry(
                iteration_id=iteration_id,
                date=datetime.now(timezone.utc).isoformat(),
                alert_type="quality_gate_failed",
                message="Syntax errors detected in repository",
                details={"errors": qg_result["syntax_errors"]},
            )
        else:
            print(f"  ✅ Quality gates passed")

        changes, opts, _, after_snaps = run_scan(
            repo,
            dry_run=args.dry_run,
            learnings=learnings,
            before_snapshots=before_snapshots,
            cost_tracker=cost_tracker,
        )
        all_changes.extend(changes)
        all_opts.extend(opts)
        after_snapshots.update(after_snaps)

    return all_changes, all_opts, after_snapshots, repos, alert, qg_result


def _auto_execute_changes(
    auto_exec: list[ChangeItem],
    rules: dict,
    pending_sorted: list[ChangeItem],
    mode: OperationMode,
    dry_run: bool,
) -> tuple[list[ChangeItem], set[str], int, str, list[ChangeItem]]:
    """
    Execute auto-approved low-risk changes in full-auto mode.
    Returns (auto_executed, repos_affected, todos_resolved, iteration_status, remaining_pending).
    """
    auto_executed: list[ChangeItem] = []
    repos_affected: set[str] = set()
    todos_resolved = 0
    remaining_pending: list[ChangeItem] = []
    iteration_status = "dry-run" if dry_run else mode.value

    if mode == OperationMode.FULL_AUTO and not dry_run:
        for change in auto_exec:
            if should_auto_execute(rules, change.risk):
                try:
                    repo_obj = Repository(path=change.repo_path, type=change.repo_type)
                    commit_hash = git_commit(repo_obj, f"auto: {change.description}")
                    change.commit_hash = commit_hash
                    auto_executed.append(change)
                    repos_affected.add(change.repo_path)
                    if change.optimization_type == "todo_fixme":
                        todos_resolved += 1
                    log_desc = sanitize_change_for_log(change, repo_obj)
                    print(f"  ✅ {log_desc} ({commit_hash})")
                    change_dict = {
                        "description": change.description,
                        "type": change.optimization_type or change.category.value,
                        "file_path": change.file_path,
                    }
                    record_learning(change_dict, "ok", change.repo_path)
                except Exception as e:
                    print(f"  ❌ {change.file_path}: {e}")
        remaining_pending = pending_sorted
        iteration_status = "full-auto-completed"

    elif mode == OperationMode.SEMI_AUTO and not dry_run:
        remaining_pending = auto_exec + pending_sorted
        iteration_status = "pending-approval"
        if auto_exec:
            print(f"\n📋 {len(auto_exec)} auto-changes held for confirmation (semi-auto mode)")
            print(f"   Run `auto-evolve.py confirm` after reviewing pending items")
    else:
        remaining_pending = auto_exec + pending_sorted

    return auto_executed, repos_affected, todos_resolved, iteration_status, remaining_pending


def _build_pending_items(pending_sorted: list[ChangeItem]) -> tuple[list[dict], list[str]]:
    """Convert sorted pending ChangeItems to dicts and plan_lines."""
    pending_items: list[dict] = []
    for c in pending_sorted:
        repo_obj = Repository(path=c.repo_path, type=c.repo_type)
        item: dict = {
            "id": c.id,
            "description": c.description,
            "file_path": c.file_path,
            "risk": c.risk.value,
            "category": c.category.value,
            "repo_path": c.repo_path,
            "optimization_type": c.optimization_type,
            "priority": c.priority,
            "value_score": c.value_score,
            "risk_score": c.risk_score,
            "cost_score": c.cost_score,
        }
        if repo_obj.is_closed():
            item = sanitize_pending_item(item, repo_obj)
        pending_items.append(item)
    return pending_items, []


def _display_remaining_pending(
    remaining_pending: list[ChangeItem],
    plan_lines: list[str],
) -> None:
    """Print remaining pending items grouped by repository, and extend plan_lines."""
    if not remaining_pending:
        return
    by_repo = _group_by_repo(remaining_pending)
    total_counter = 1
    print(f"\n📋 Pending Items ({len(remaining_pending)} across {len(by_repo)} repo(s)):")
    for repo_path, items in by_repo.items():
        repo_name = Path(repo_path).name
        print(f"\n  📦 {repo_name} ({len(items)} items)")
        for c in items:
            risk_icon = RISK_COLORS.get(c.risk.value, "⚪")
            opt_badge = " [opt]" if c.category == ChangeCategory.OPTIMIZATION else ""
            print(f"    [{total_counter}] {risk_icon} P={c.priority:.2f} {c.description[:55]}{opt_badge}")
            total_counter += 1
    plan_lines.extend(["## Pending Items ({})".format(len(remaining_pending)), ""])
    for c in remaining_pending:
        plan_lines.append(
            f"- [{c.id}] **{c.risk.value.upper()}** P={c.priority:.2f} "
            f"[{Path(c.repo_path).name}] {c.description}"
        )


def _push_repos(repos_affected: set[str]) -> None:
    """Push all affected repos to remote."""
    for rp in repos_affected:
        repo_obj = Repository(path=rp, type="skill")
        try:
            git_push(repo_obj)
            print(f"  📤 Pushed to remote")
        except Exception as e:
            print(f"  ⚠️  Push failed: {e}")


def _build_pending_items_with_plan(
    pending_sorted: list[ChangeItem],
    plan_lines: list[str],
) -> tuple[list[dict], list[str]]:
    """Convert pending ChangeItems to dicts and append to plan_lines."""
    pending_items: list[dict] = []
    for c in pending_sorted:
        repo_obj = Repository(path=c.repo_path, type=c.repo_type)
        item: dict = {
            "id": c.id,
            "description": c.description,
            "file_path": c.file_path,
            "risk": c.risk.value,
            "category": c.category.value,
            "repo_path": c.repo_path,
            "optimization_type": c.optimization_type,
            "priority": c.priority,
            "value_score": c.value_score,
            "risk_score": c.risk_score,
            "cost_score": c.cost_score,
        }
        if repo_obj.is_closed():
            item = sanitize_pending_item(item, repo_obj)
        pending_items.append(item)
    return pending_items, plan_lines


def _compute_diff_stats(repos_affected: set[str]) -> tuple[int, int, int]:
    """Compute lines added/removed and files changed across repos."""
    lines_added_total = lines_removed_total = files_changed_total = 0
    for rp in repos_affected:
        repo_obj = Repository(path=rp, type="skill")
        la, lr = git_diff_lines_added_removed(repo_obj)
        lines_added_total += la
        lines_removed_total += lr
        files_changed_total += len(git_status(repo_obj))
    return lines_added_total, lines_removed_total, files_changed_total


def _post_scan_cleanup(
    cost_tracker: CostTracker,
    iteration_id: str,
    effect_tracker: EffectTracker,
    before_snapshots: dict[str, dict],
    after_snapshots: dict[str, dict],
    auto_executed: list[ChangeItem],
    remaining_pending: list[ChangeItem],
    todos_resolved: int,
    qg: dict,
    repos_affected: set[str],
) -> dict:
    """Flush LLM costs, compute effects, link issues. Returns cost_summary."""
    cost_tracker.flush_calls(iteration_id)
    cost_summary = cost_tracker.get_iteration_cost(iteration_id)

    if before_snapshots and after_snapshots and (auto_executed or remaining_pending):
        effect_report = effect_tracker.track_iteration_effect(
            iteration_id=iteration_id,
            before_snapshots=before_snapshots,
            after_snapshots=after_snapshots,
            todos_resolved=todos_resolved,
            lint_errors_fixed=qg.get("lint_errors_fixed", 0),
            coverage_delta=0.0,
        )
        verdict_icon = {"positive": "✅", "neutral": "➖", "negative": "❌"}.get(effect_report["verdict"], "➖")
        print(f"\n  {verdict_icon} Effect: {effect_report['summary']}")

    if auto_executed:
        issue_linker = IssueLinker()
        for rp in repos_affected:
            repo_path = Path(rp)
            repo_changed = [g["file"] for g in git_status(Repository(path=rp, type="skill"))]
            if repo_changed:
                close_result = issue_linker.close_related_issues(repo_path, repo_changed, iteration_id)
                if close_result["found"] > 0:
                    print(f"\n  🔗 IssueLinker: found {close_result['found']} related issue(s), closed {close_result['closed']}")

    return cost_summary


def _group_by_repo(items: list[ChangeItem]) -> dict[str, list[ChangeItem]]:
    """Group ChangeItems by repo path, preserving order within each group."""
    groups: dict[str, list[ChangeItem]] = {}
    for c in items:
        groups.setdefault(c.repo_path, []).append(c)
    return groups


def _print_scan_summary(
    all_changes: list[ChangeItem],
    all_opts: list[OptimizationFinding],
    auto_exec: list[ChangeItem],
    pending_sorted: list[ChangeItem],
    mode: OperationMode,
    dry_run: bool,
    rules: dict,
) -> None:
    """Print scan result summary and priority queue, grouped by repository."""
    print(f"\n📊 Scan Results:")
    print(f"  Changes detected: {len(all_changes) - len(all_opts)}")
    print(f"  Optimizations found: {len(all_opts)}")
    print(f"  Auto-executable:     {len(auto_exec)}")
    print(f"  Pending review:      {len(pending_sorted)}")

    if pending_sorted:
        print(f"\n📊 Priority Queue (by repo):")
        by_repo = _group_by_repo(pending_sorted)
        item_counter = 1
        for repo_path, items in by_repo.items():
            repo_name = Path(repo_path).name
            print(f"\n  📦 {repo_name}")
            for c in items[:10]:
                color = priority_color(c.priority)
                risk_label = c.risk.value.upper()
                opt_badge = " [opt]" if c.category == ChangeCategory.OPTIMIZATION else ""
                print(f"    [{item_counter}] {color} P={c.priority:.2f} {risk_label}: {c.description[:50]}{opt_badge}")
                item_counter += 1
            if len(items) > 10:
                print(f"    ... and {len(items) - 10} more in {repo_name}")
        extra = len(pending_sorted) - item_counter + 1
        if extra > 0:
            print(f"  (total {len(pending_sorted)} items across {len(by_repo)} repos)")

    if auto_exec and not dry_run:
        print_execution_preview(all_changes, auto_exec, mode, rules)


def _build_plan_and_report(
    iteration_id: str,
    mode: OperationMode,
    dry_run: bool,
    repos: list[Repository],
    duration: float,
    all_changes: list[ChangeItem],
    all_opts: list[OptimizationFinding],
    pending_sorted: list[ChangeItem],
) -> tuple[list[str], list[str], list[dict]]:
    """Build plan_lines, report_lines, and pending_items from scan results."""
    plan_lines = [
        f"# Iteration Plan — {iteration_id}",
        "",
        f"**Date:** {datetime.now(timezone.utc).isoformat()}",
        f"**Mode:** {mode.value}",
        f"**Repositories:** {len(repos)}",
        f"**Duration:** {duration:.1f}s",
        "",
        "## Changes",
        "",
    ]
    report_lines = [
        f"# Iteration Report — {iteration_id}",
        "",
        f"**Date:** {datetime.now(timezone.utc).isoformat()}",
        f"**Mode:** {mode.value}",
        f"**Status:** {'dry-run' if dry_run else mode.value}",
        "",
        "## Summary",
        "",
        f"- Changes detected: {len(all_changes) - len(all_opts)}",
        f"- Optimizations found: {len(all_opts)}",
        f"- Pending review: {len(pending_sorted)}",
        "",
    ]
    pending_items, plan_lines = _build_pending_items_with_plan(pending_sorted, plan_lines)
    return plan_lines, report_lines, pending_items


def _track_contributors(repos_affected: set[str]) -> dict:
    """Collect contributor stats for all affected repos."""
    contributors: dict = {}
    for rp in repos_affected:
        repo_obj = Repository(path=rp, type="skill")
        contributors[rp] = track_contributors(repo_obj)
    return contributors


def _build_scan_manifest(
    iteration_id: str,
    iteration_status: str,
    duration: float,
    num_auto: int,
    num_opts: int,
    pending_items: list[dict],
    alert: Optional[AlertEntry],
    contributors: dict,
    cost_summary: dict,
) -> IterationManifest:
    """Build and return the IterationManifest for a scan iteration."""
    return IterationManifest(
        version=iteration_id,
        date=datetime.now(timezone.utc).isoformat(),
        status=iteration_status,
        risk_level="mixed",
        items_auto=num_auto,
        items_approved=0,
        items_rejected=0,
        items_optimization=num_opts,
        duration_seconds=round(duration, 1),
        items_pending_approval=pending_items,
        has_alert=alert is not None,
        metrics_id=iteration_id,
        test_coverage_delta=None,
        contributors=contributors,
        total_cost_usd=cost_summary.get("total_cost_usd"),
        llm_calls=cost_summary.get("total_calls", 0),
    )


def _print_contributors(contributors: dict) -> None:
    """Print contributor stats."""
    for rp, contrib in contributors.items():
        rn = Path(rp).name
        print(f"   [C] {rn}: {contrib['auto_commits']} auto / "
              f"{contrib['manual_commits']} manual ({contrib['auto_percentage']}% auto)")


def _print_iteration_summary(
    iteration_id: str,
    pending_items: list[dict],
    metrics,
    cost_summary: dict,
    mode: OperationMode,
    auto_exec: list[ChangeItem],
    dry_run: bool,
    opt_executed: Optional[list[ChangeItem]] = None,
    opt_stats: Optional[dict] = None,
) -> None:
    """Print final iteration summary."""
    print(f"\n📁 Iteration {iteration_id} saved to .iterations/{iteration_id}/")
    print(f"   pending-review.json: {len(pending_items)} items")
    print(f"   metrics.json: todos={metrics.todos_resolved}, files={metrics.files_changed}, "
          f"+{metrics.lines_added}/-{metrics.lines_removed}")
    if opt_executed:
        print(f"   ⚡ Optimizations executed: {len(opt_executed)} "
              f"(via LLM auto-fix, v3.2)")
        if opt_stats:
            by_type = opt_stats.get("by_type", {})
            for ot, cnt in by_type.items():
                print(f"      - {ot}: {cnt}")
    if cost_summary.get("total_calls", 0) > 0:
        print(f"   💰 LLM cost: ${cost_summary['total_cost_usd']:.6f} "
              f"({cost_summary['total_calls']} calls)")

    if mode == OperationMode.SEMI_AUTO and auto_exec and not dry_run:
        print(f"\n   Confirm with: auto-evolve.py confirm")

    if dry_run:
        print("\n⚠️  Dry-run mode — no changes committed")


def cmd_scan(args) -> int:
    """Scan all configured repositories and produce an iteration."""
    config = load_config()
    dry_run = args.dry_run
    mode = get_operation_mode(config)
    rules = get_full_auto_rules(config)
    learnings = load_learnings()

    # Filter to a single repo if --repo is specified
    if getattr(args, 'repo', '').strip():
        target = args.repo.strip()
        original = list(config.get("repositories", []))
        config["repositories"] = [
            r for r in original
            if str(Path(r["path"]).resolve()) == str(Path(target).resolve())
        ]
        if not config["repositories"]:
            print(f"❌ Repository not found in config: {target}")
            print(f"   Configured repos: {[r['path'] for r in original]}")
            return 1
        print(f"🎯 Targeting single repo: {target}")

    print("🔍 Auto-Evolve v3.9 Scanner")
    print(f"   Mode: {mode.value}")
    print("=" * 50)

    start_time = time.time()
    iteration_id = generate_iteration_id()

    # Trackers
    effect_tracker = EffectTracker()
    cost_tracker = CostTracker()
    before_snapshots: dict[str, dict] = {}

    # Scan repos
    all_changes, all_opts, after_snapshots, repos, alert, qg = _scan_repos(
        config, args, learnings, before_snapshots, cost_tracker, iteration_id,
    )
    duration = time.time() - start_time

    # Categorize changes
    auto_exec = [c for c in all_changes if c.category == ChangeCategory.AUTO_EXEC and c.risk == RiskLevel.LOW]
    pending = [c for c in all_changes if c.category in (ChangeCategory.PENDING_APPROVAL, ChangeCategory.OPTIMIZATION)]
    pending_sorted = sort_by_priority(pending)

    # Print scan summary and priority queue
    _print_scan_summary(all_changes, all_opts, auto_exec, pending_sorted, mode, dry_run, rules)

    # v3.3: Product Thinking Scanner — ask the RIGHT questions
    print("\n" + "=" * 50)
    product_scanner = FourPerspectiveScanner(
        repos, config,
        recall_persona=getattr(args, 'recall_persona', '') or '',
        memory_source=getattr(args, 'memory_source', 'auto') or 'auto',
    )
    product_findings = product_scanner.scan()
    print_product_findings(product_findings)

    # v4.2: GitHub integration — post results as PR comment or issue
    github_event = getattr(args, 'github_event', '') or ""
    if github_event and product_findings:
        for repo in repos:
            repo_path = repo.resolve_path()
            product_scanner.post_github_comment(repo_path, product_findings, github_event)

    # Build plan and report lines
    plan_lines, report_lines, pending_items = _build_plan_and_report(
        iteration_id, mode, dry_run, repos, duration,
        all_changes, all_opts, pending_sorted,
    )

    # Auto-execute changes
    (auto_executed, repos_affected, todos_resolved, iteration_status, remaining_pending) = \
        _auto_execute_changes(auto_exec, rules, pending_sorted, mode, dry_run)

    # Auto-execute LLM-driven optimizations (v3.2)
    (opt_executed, opt_stats) = _auto_execute_optimizations(
        all_changes, all_opts, mode, rules, dry_run,
    )

    # Merge optimization repos into repos_affected
    for item in opt_executed:
        repos_affected.add(item.repo_path)

    # Update todos_resolved with optimization todos
    todos_resolved += sum(
        1 for item in opt_executed if item.optimization_type == "todo_fixme"
    )

    # Diff stats
    lines_added_total, lines_removed_total, files_changed_total = _compute_diff_stats(repos_affected)

    # Pending items display
    _display_remaining_pending(remaining_pending, plan_lines)

    # Push auto-executed (both git changes and LLM optimizations)
    if (auto_executed or opt_executed) and not dry_run:
        _push_repos(repos_affected)

    # Post-scan: costs, effects, issue linking
    cost_summary = _post_scan_cleanup(
        cost_tracker, iteration_id, effect_tracker,
        before_snapshots, after_snapshots,
        auto_executed, remaining_pending,
        todos_resolved, qg, repos_affected,
    )

    # Metrics and contributors
    quality_passed = alert is None
    metrics = generate_metrics(
        iteration_id=iteration_id,
        todos_resolved=todos_resolved,
        lint_errors_fixed=qg.get("lint_errors_fixed", 0),
        files_changed=files_changed_total,
        lines_added=lines_added_total,
        lines_removed=lines_removed_total,
        quality_gate_passed=quality_passed,
    )
    save_metrics(metrics)
    
    # Record metrics to per-persona learnings (for trend tracking)
    try:
        from scripts.helpers import record_iteration_metrics
        record_iteration_metrics(
            iteration_id=iteration_id,
            todo_count=todos_resolved + len(pending_items),  # approximate
            todo_resolved=todos_resolved,
            auto_executed=total_auto,
            llm_cost_usd=cost_summary.get("total_cost_usd", 0.0),
        )
    except Exception:
        pass  # Non-critical
    
    contributors = _track_contributors(repos_affected)

    # Build manifest and save
    total_auto = len(auto_executed) + len(opt_executed)
    manifest = _build_scan_manifest(
        iteration_id, iteration_status, duration,
        total_auto, len(all_opts),
        pending_items, alert, contributors, cost_summary,
    )
    _print_contributors(contributors)
    save_iteration(iteration_id, manifest, plan_lines, pending_items, report_lines, alert)
    update_catalog(manifest)

    # Final summary
    _print_iteration_summary(
        iteration_id, pending_items, metrics, cost_summary,
        mode, auto_exec, dry_run, opt_executed, opt_stats,
    )
    return 0


def cmd_confirm(args) -> int:
    """Confirm pending changes from a semi-auto scan iteration."""
    catalog = load_catalog()
    target_iter, iteration_id = _find_target_iteration(
        catalog, args.iteration_id, status_filter="pending-approval",
    )
    if not iteration_id:
        return 1

    manifest_data, pending_items = _load_iteration_pending(iteration_id)
    if manifest_data is None:
        return 1
    if not pending_items:
        print(f"No pending items in iteration {iteration_id}.")
        return 0

    print(f"Confirming {len(pending_items)} pending items from {iteration_id}...")

    repos_affected: set[str] = set(p.get("repo_path", "") for p in pending_items)
    confirmed_count = 0

    for rp in repos_affected:
        repo_obj = Repository(path=rp, type="skill")
        if not repo_obj.resolve_path().exists():
            continue
        repo_items = [p for p in pending_items if p.get("repo_path") == rp]
        for p in repo_items:
            try:
                commit_hash = git_commit(repo_obj, f"auto-evolve: {p['description']}")
                print(f"  ✅ [{p['id']}] {p['description'][:60]} ({commit_hash})")
                confirmed_count += 1
                add_learning(
                    learning_type="approval",
                    change_id=str(p["id"]),
                    description=p["description"],
                    reason=None,
                    repo=rp,
                    approved_by="user",
                )
            except Exception as e:
                print(f"  ❌ [{p['id']}] {p['description'][:60]}: {e}")

    # v3.2: Issue linking after confirm
    if confirmed_count > 0:
        issue_linker = IssueLinker()
        for rp in repos_affected:
            repo_path = Path(rp)
            repo_changed = [g["file"] for g in git_status(Repository(path=rp, type="skill"))]
            if repo_changed:
                close_result = issue_linker.close_related_issues(repo_path, repo_changed, iteration_id)
                if close_result["found"] > 0:
                    print(f"\n  🔗 IssueLinker: closed {close_result['closed']} of {close_result['found']} related issue(s)")

    for rp in repos_affected:
        repo_obj = Repository(path=rp, type="skill")
        try:
            git_push(repo_obj)
        except Exception as e:
            print(f"  ⚠️  Push failed for {rp}: {e}")

    _finalize_iteration_status(
        iteration_id, manifest_data, catalog,
        "completed", items_approved=confirmed_count,
    )
    print(f"\n✅ Confirmed and executed {confirmed_count} items")
    return 0


def cmd_reject(args) -> int:
    """Reject a specific pending change and record it in learnings."""
    catalog = load_catalog()
    target_iter, iteration_id = _find_target_iteration(
        catalog, args.iteration_id, status_filter="pending-approval",
    )
    if not iteration_id:
        return 1

    manifest_data, pending_items = _load_iteration_pending(iteration_id)
    if manifest_data is None:
        return 1

    item = next((p for p in pending_items if p.get("id") == args.id), None)
    if not item:
        print(f"Item {args.id} not found in pending items.")
        return 1

    add_learning(
        learning_type="rejection",
        change_id=str(args.id),
        description=item["description"],
        reason=args.reason,
        repo=item.get("repo_path", ""),
    )

    remaining = [p for p in pending_items if p.get("id") != args.id]
    save_pending_review(iteration_id, remaining)

    manifest_data["items_pending_approval"] = remaining
    manifest_data["items_rejected"] = manifest_data.get("items_rejected", 0) + 1
    (ITERATIONS_DIR / iteration_id / "manifest.json").write_text(
        json.dumps(manifest_data, indent=2),
    )

    print(f"❌ Rejected item {args.id}: {item['description'][:60]}")
    if args.reason:
        print(f"   Reason: {args.reason}")
    print(f"   Recorded in .learnings/rejections.json")

    return 0


def cmd_approve(args) -> int:
    """Approve and execute pending changes (supports --all, --ids, or interactive)."""
    catalog = load_catalog()
    target_iter, iteration_id = _find_target_iteration(
        catalog, args.iteration_id,
        status_filter="pending-approval",
    )
    if not iteration_id:
        # Fallback: also check full-auto-completed
        catalog = load_catalog()
        target_iter, iteration_id = _find_target_iteration(
            catalog, args.iteration_id,
            status_filter="full-auto-completed",
        )
        if not iteration_id:
            return 1

    manifest_data, pending_items = _load_iteration_pending(iteration_id)
    if manifest_data is None:
        return 1
    if not pending_items:
        print(f"No pending items in iteration {iteration_id}.")
        return 0

    # Resolve which IDs to approve
    approved_ids = _resolve_approved_ids(args, pending_items)
    if approved_ids is None:
        return 0  # Interactive listing was shown

    # Batch merge check for high-risk
    changes_for_pr = [p for p in pending_items if p["id"] in approved_ids and p.get("risk") == "high"]
    if len(changes_for_pr) >= 3 and should_merge_prs(changes_for_pr):
        print(f"\n📦 Batch-merging {len(changes_for_pr)} high-risk changes into single PR...")
        groups = group_similar_changes(changes_for_pr)
        print(f"   Created {len(groups)} change group(s)")

    # Execute approvals
    approved_count, repos_affected = _execute_approved_items(
        pending_items, approved_ids, iteration_id, args,
    )

    # Push
    if approved_count > 0:
        _push_repos(repos_affected)

    _finalize_iteration_status(
        iteration_id, manifest_data, catalog,
        "completed", items_approved=approved_count,
    )
    print(f"\n✅ Approved and executed {approved_count} items")
    return 0


def _resolve_approved_ids(
    args,
    pending_items: list[dict],
) -> Optional[list[int]]:
    """Resolve which item IDs to approve. Returns None if displaying interactive list."""
    if args.all:
        approved_ids = [p["id"] for p in pending_items]
        reason = getattr(args, "reason", None)
        print(f"✅ Approving all {len(approved_ids)} pending items...")
        if reason:
            print(f"   Reason: {reason}")
        return approved_ids

    ids_str = getattr(args, "ids", None)
    if ids_str:
        try:
            return [int(x.strip()) for x in str(ids_str).split(",") if x.strip()]
        except ValueError:
            print("Invalid IDs. Use: approve 1,2,3")
            return None

    # Interactive listing
    iteration_id = getattr(args, "iteration_id", None)
    print(f"Iteration: {iteration_id}")
    print(f"Pending items ({len(pending_items)}):")
    for p in pending_items:
        risk_icon = RISK_COLORS.get(p.get("risk", "medium"), "⚪")
        pri = p.get("priority", 0)
        llm_b = " [LLM]" if p.get("llm_suggestion") else ""
        dep_b = ""
        if p.get("affected_files"):
            dep_b = f" [!]{len(p['affected_files'])}deps"
        print(f"  [{p['id']}] {risk_icon} P={pri:.2f} {p.get('risk', '?').upper()} "
              f"{p.get('description', '')[:55]}{llm_b}{dep_b}")
    print("\nRun: auto-evolve.py approve --all [--reason 'your reason']")
    print("Or:  auto-evolve.py approve 1,3 [--reason 'your reason']")
    return None


def _execute_approved_items(
    pending_items: list[dict],
    approved_ids: list[int],
    iteration_id: str,
    args,
) -> tuple[int, set[str]]:
    """Execute approved items. Returns (approved_count, repos_affected)."""
    approved_count = 0
    repos_affected: set[str] = set()
    issue_linker = IssueLinker()
    approval_reason = getattr(args, "reason", None)

    for p in pending_items:
        if p["id"] not in approved_ids:
            continue

        repo_obj = Repository(path=p["repo_path"], type=p.get("repo_type", "skill"))
        if not repo_obj.resolve_path().exists():
            print(f"  ⚠️  Repo not found: {repo_obj.path}")
            continue

        if p.get("risk") == "high":
            _approve_high_risk(p, repo_obj, issue_linker, iteration_id)
            approved_count += 1
            repos_affected.add(p["repo_path"])
        else:
            try:
                commit_hash = git_commit(repo_obj, f"auto-evolve: {p['description']}")
                print(f"  ✅ [{p['id']}] {p['description'][:60]} ({commit_hash})")
                approved_count += 1
                repos_affected.add(p["repo_path"])
                add_learning(
                    learning_type="approval",
                    change_id=str(p["id"]),
                    description=p["description"],
                    reason=approval_reason,
                    repo=repo_obj.path,
                    approved_by="user",
                )
                repo_changed = [p.get("file_path", "")]
                close_result = issue_linker.close_related_issues(
                    repo_obj.resolve_path(), repo_changed, iteration_id,
                )
                if close_result["found"] > 0:
                    print(f"  🔗 IssueLinker: closed {close_result['closed']} of {close_result['found']} related issue(s)")
            except Exception as e:
                print(f"  ❌ [{p['id']}] {p['description'][:60]}: {e}")

    return approved_count, repos_affected


def _approve_high_risk(
    p: dict,
    repo_obj: Repository,
    issue_linker: IssueLinker,
    iteration_id: str,
) -> None:
    """Handle approval of a high-risk item (branch + PR)."""
    print(f"\n🔴 High-risk: {p['description'][:60]}")
    print(f"  Creating branch and PR...")
    branch = create_branch_for_change(repo_obj, p["description"][:50])
    conflict_result = handle_pr_conflict(repo_obj, branch)
    try:
        commit_hash = git_commit(repo_obj, f"auto-evolve: {p['description']}")
        pr_body = f"## auto-evolve: {p['description']}\n\n### Changes\n\n- {p['description']}"
        pr_url = create_pr(
            repo_obj, branch,
            p["description"],
            [ChangeItem(
                id=p["id"],
                description=p["description"],
                file_path=p["file_path"],
                change_type="approved",
                risk=RiskLevel.HIGH,
                category=ChangeCategory.PENDING_APPROVAL,
                repo_path=repo_obj.path,
            )],
            extra_body=pr_body,
        )
        print(f"  ✅ Branch: {branch}")
        print(f"  ✅ Commit: {commit_hash}")
        if conflict_result == "auto_resolved":
            print(f"  🔧 Conflicts auto-resolved during rebase")
        elif conflict_result == "manual_required":
            print(f"  ⚠️  Conflicts require manual resolution")
        print(f"  🔗 {pr_url}")
    except Exception as e:
        print(f"  ❌ Failed: {e}")


def create_branch_for_change(repo: Repository, change_desc: str) -> str:
    sanitized = re.sub(r"[^a-zA-Z0-9_-]", "-", change_desc.lower())[:50]
    branch_name = f"auto-evolve/{sanitized}"
    git_create_branch(repo, branch_name)
    return branch_name


def create_pr(repo: Repository, branch_name: str, description: str, changes: list[ChangeItem], extra_body: Optional[str] = None) -> str:
    result = git_run(repo, "remote", "get-url", "origin", check=False)
    remote_url = result.stdout.strip()
    match = re.search(r"github\.com[/:]([^/]+/[^/]+?)(?:\.git)?$", remote_url)
    if not match:
        return f"Branch created: {branch_name} (PR creation requires gh CLI and GitHub remote)"
    repo_slug = match.group(1)

    pr_body_lines = [
        f"## auto-evolve: {description}",
        "",
        "### Changes",
        "",
    ]
    for c in changes:
        pr_body_lines.append(f"- **{c.risk.value}** {c.description} (`{c.file_path}`)")
    if extra_body:
        pr_body_lines.extend(["", extra_body])
    pr_body_lines.extend([
        "",
        "### Approval",
        "",
        "This PR requires explicit approval. Run:",
        "```",
        "auto-evolve.py approve",
        "```",
    ])
    pr_body = "\n".join(pr_body_lines)

    result = subprocess.run(
        [
            "gh", "pr", "create",
            "--repo", repo_slug,
            "--title", f"[auto-evolve] {description}",
            "--body", pr_body,
            "--base", "main",
            "--head", branch_name,
        ],
        cwd=str(repo.resolve_path()),
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        return f"Branch {branch_name} created. PR creation failed: {result.stderr.strip()}"
    return result.stdout.strip()


def cmd_repo_add(args) -> int:
    config = load_config()
    repos = config_to_repos(config)
    repo_path = Path(args.path).expanduser().resolve()
    if not repo_path.exists():
        print(f"❌ Repository not found: {repo_path}")
        return 1
    repo_type = args.type or "skill"
    if repo_type not in REPO_TYPES:
        print(f"Invalid type. Must be one of: {', '.join(REPO_TYPES)}")
        return 1
    for r in repos:
        if Path(r.path).resolve() == repo_path:
            print(f"Repository already monitored: {repo_path}")
            return 0
    new_repo = Repository(
        path=str(repo_path),
        type=repo_type,
        visibility="public",
        auto_monitor=True,
    )
    repos.append(new_repo)
    config = repos_to_config(repos, config)
    save_config(config)
    print(f"✅ Added repository: {repo_path}")
    print(f"   Type: {repo_type}")
    print(f"   Auto-monitor: True")
    return 0


def cmd_repo_list(args) -> int:
    config = load_config()
    repos = config_to_repos(config)
    if not repos:
        print("No repositories configured.")
        print("Run: auto-evolve.py repo-add <path> --type <type>")
        return 0
    print("📦 Configured Repositories:")
    print("=" * 50)
    for i, r in enumerate(repos, 1):
        exists = "✅" if r.resolve_path().exists() else "❌"
        mon = "🟢" if r.auto_monitor else "⏭️"
        vis = "🔒" if r.is_closed() else "🌐"
        print(f"{i}. {exists} {mon} {vis} {r.path}")
        print(f"   Type: {r.type} | Visibility: {r.visibility}")
        print(f"   Auto-monitor: {r.auto_monitor} | Scan interval: {r.scan_interval_hours}h")
        if r.risk_override:
            print(f"   Risk override: {r.risk_override}")
        if r.resolve_path().exists():
            det = detect_repo_languages(r.resolve_path())
            if det:
                print(f"   Languages: {', '.join(sorted(det))}")
        print()
    return 0


def cmd_rollback(args) -> int:
    version = args.to
    item_id = getattr(args, "item", None)
    reason = args.reason or "User-initiated rollback"

    catalog = load_catalog()
    iteration_ids = [i["version"] for i in catalog["iterations"]]

    if version not in iteration_ids:
        print(f"❌ Version {version} not found.")
        print("Available versions:")
        for vid in iteration_ids:
            print(f"  - {vid}")
        return 1

    iter_data = load_iteration(version)
    rollback_iter_id = generate_iteration_id()

    print(f"⚠️  Rolling back iteration {version}")
    if item_id is not None:
        print(f"   Cherry-pick mode: only item #{item_id}")
    print(f"   Reason: {reason}")

    items = iter_data.get("items_pending_approval", [])
    repos_affected: dict[str, list] = {}
    for item in items:
        rp = item.get("repo_path", "")
        repos_affected.setdefault(rp, []).append(item)

    reverted = 0
    for repo_path_str, repo_items in repos_affected.items():
        repo_obj = Repository(path=repo_path_str, type="skill")
        if not repo_obj.resolve_path().exists():
            print(f"  ⚠️  Repo not found: {repo_path_str}")
            continue

        items_to_revert = repo_items
        if item_id is not None:
            items_to_revert = [i for i in repo_items if i.get("id") == item_id]
            if not items_to_revert:
                print(f"  Item {item_id} not found in {repo_path_str}")
                continue

        try:
            commits = git_log(repo_obj, limit=len(repo_items) + 1)
            for commit in commits[: len(items_to_revert)]:
                try:
                    git_revert(repo_obj, commit["hash"])
                    print(f"  ✅ Reverted: {commit['message'][:60]}")
                    reverted += 1
                except Exception as e:
                    print(f"  ⚠️  Could not revert {commit['hash']}: {e}")
        except Exception as e:
            print(f"  ❌ Git error for {repo_path_str}: {e}")

    manifest = IterationManifest(
        version=rollback_iter_id,
        date=datetime.now(timezone.utc).isoformat(),
        status="rolled-back",
        risk_level="medium",
        items_auto=0,
        items_approved=0,
        items_rejected=reverted,
        duration_seconds=0.0,
        rollback_of=version,
        rollback_reason=reason,
    )

    report_lines = [
        f"# Rollback Report — {rollback_iter_id}",
        "",
        f"**Rolled back:** {version}",
        f"**Reason:** {reason}",
        f"**Reverted items:** {reverted}",
        "",
    ]

    save_iteration(rollback_iter_id, manifest, [], [], report_lines)
    update_catalog(manifest)

    print(f"\n✅ Rollback complete: {rollback_iter_id}")
    print(f"   Reverted: {reverted} items from {version}")
    if item_id is not None:
        print(f"   (cherry-pick: only item #{item_id})")
    return 0


def cmd_release(args) -> int:
    version = args.version
    changelog = args.changelog or ""
    config = load_config()
    repos = config_to_repos(config)
    if not repos:
        print("No repositories configured.")
        return 1
    if len(repos) > 1:
        print("Multiple repos -- creating release for first repo.")
    repo = repos[0]
    if not repo.resolve_path().exists():
        print("Repository not found: " + repo.path)
        return 1
    print("Creating release v" + version.lstrip("v") + " for " + repo.path + "...")
    try:
        create_release(repo, version, changelog)
        print("Release v" + version.lstrip("v") + " created successfully")
    except Exception as e:
        print("Release failed: " + str(e))
        return 1
    return 0


def cmd_schedule(args) -> int:
    """
    v3.2: Schedule management with smart scheduling.
    --suggest: Show activity-based scheduling recommendations
    --auto: Apply recommendations to config
    --every: Set interval (creates cron)
    --show: Show current schedule
    --remove: Remove cron job
    """
    config = load_config()

    if args.remove:
        removed = remove_cron()
        if removed:
            print("✅ Cron job removed via openclaw CLI.")
        else:
            print("# Remove auto-evolve cron job manually:")
            print("openclaw cron remove auto-evolve-scan")
            print()
            print("Or manually delete the cron in your OpenClaw config.")
        return 0

    if args.show:
        interval = config.get("schedule_interval_hours", 168)
        cron_id = config.get("schedule_cron_id")
        print("# Auto-Evolve Schedule Configuration")
        print("#")
        if cron_id:
            print(f"# Cron ID: {cron_id}")
        print(f"# Current interval: every {interval} hour(s)")
        print()
        print("# To change interval, run:")
        print(f"#   auto-evolve.py schedule --every {interval}")
        return 0

    if args.suggest:
        return _schedule_suggest(config)

    if args.auto:
        return _schedule_auto(config)

    if args.every:
        interval = args.every
        if interval < 1:
            print("❌ Interval must be at least 1 hour.")
            return 1
        config["schedule_interval_hours"] = interval
        save_config(config)
        print(f"✅ Schedule interval set to {interval} hour(s)")
        cron_created = setup_cron(interval)
        if cron_created:
            print(f"✅ Cron job created via openclaw CLI (ID: {config.get('schedule_cron_id', 'unknown')})")
        else:
            print()
            print("⚠️  openclaw CLI not available — create cron manually:")
            print(f"  openclaw cron add --name auto-evolve-scan \\")
            print(f"    --every {interval}h \\")
            print(f"    --message 'exec python3 {SKILL_DIR}/scripts/auto-evolve.py scan'")
        return 0

    # No subcommand
    print("auto-evolve.py schedule --every HOURS   Set scan interval (creates cron)")
    print("auto-evolve.py schedule --suggest        Smart scheduling recommendations (v3.2)")
    print("auto-evolve.py schedule --auto           Apply recommended intervals (v3.2)")
    print("auto-evolve.py schedule --show            Show current schedule")
    print("auto-evolve.py schedule --remove          Remove cron job")
    return 0


def _schedule_suggest(config: dict) -> int:
    """Show smart scheduling recommendations."""
    scheduler = SmartScheduler(config)
    suggestions = scheduler.suggest_schedule()
    if not suggestions:
        print("No repositories configured.")
        return 0
    print("📊 Smart Schedule Suggestions")
    print("=" * 60)
    activity_icons = {"very_active": "🔥", "active": "⚡", "normal": "📅", "idle": "💤"}
    for path, sug in suggestions.items():
        icon = activity_icons.get(sug["activity"], "📦")
        action_icon = {"increase": "⬆️", "decrease": "⬇️", "maintain": "➡️"}.get(sug["action"], "➡️")
        print(f"\n{icon} {sug['name']} ({path})")
        print(f"   Activity: {sug['activity']} ({sug['commits_last_7_days']} commits/7d)")
        print(f"   Current interval:  {sug['current_interval_hours']}h")
        print(f"   Recommended:       {sug['recommended_interval_hours']}h {action_icon}")
        if sug["change_hours"] != 0:
            print(f"   → Change by {abs(sug['change_hours'])}h ({sug['action']})")
    print("\n💡 Apply with: auto-evolve.py schedule --auto")
    return 0


def _schedule_auto(config: dict) -> int:
    """Auto-apply scheduling recommendations."""
    scheduler = SmartScheduler(config)
    suggestions = scheduler.suggest_schedule()
    if not suggestions:
        print("No repositories configured.")
        return 0
    updates: dict[str, int] = {}
    for path, sug in suggestions.items():
        if sug["action"] != "maintain":
            updates[path] = sug["recommended_interval_hours"]
    if not updates:
        print("✅ All repositories already at recommended intervals.")
        return 0
    result = scheduler.apply_schedule(updates)
    print("✅ Applied schedule changes:")
    for a in result["applied"]:
        print(f"   {a['path']}: {a['old_interval']}h → {a['new_interval']}h")
    return 0


def cmd_set_mode(args) -> int:
    mode = args.mode
    if mode not in ("semi-auto", "full-auto"):
        print(f"❌ Invalid mode. Must be 'semi-auto' or 'full-auto'.")
        return 1
    config = load_config()
    old_mode = config.get("mode", "semi-auto")
    config["mode"] = mode
    save_config(config)
    mode_desc = {
        "semi-auto": "semi-auto (confirm before execution)",
        "full-auto": "full-auto (execute per rules)",
    }
    print(f"✅ Mode changed: {old_mode} → {mode}")
    print(f"   {mode_desc.get(mode, mode)}")
    return 0


def cmd_set_rules(args) -> int:
    config = load_config()
    rules = config.get("full_auto_rules", {})
    rules["execute_low_risk"] = (
        args.low if args.low is not None else rules.get("execute_low_risk", True)
    )
    rules["execute_medium_risk"] = (
        args.medium if args.medium is not None else rules.get("execute_medium_risk", False)
    )
    rules["execute_high_risk"] = (
        args.high if args.high is not None else rules.get("execute_high_risk", False)
    )
    config["full_auto_rules"] = rules
    save_config(config)
    print("✅ Full-auto rules updated:")
    print(f"   execute_low_risk:    {rules['execute_low_risk']}")
    print(f"   execute_medium_risk: {rules['execute_medium_risk']}")
    print(f"   execute_high_risk:   {rules['execute_high_risk']}")
    return 0


def cmd_learnings(args) -> int:
    """Show learning history with optional summary statistics. v4.3."""
    data = load_learnings()
    rejections = data.get("rejections", [])
    approvals = data.get("approvals", [])

    # v4.3: --summary shows statistics
    if getattr(args, "summary", False):
        print("📊 Learnings Summary")
        print("=" * 50)
        print(f"  Total rejections: {len(rejections)}")
        print(f"  Total approvals: {len(approvals)}")
        if rejections:
            print(f"  Rejection rate: {len(rejections)/(len(rejections)+len(approvals))*100:.1f}%")
        if len(rejections) > 0:
            print("\n  Top rejection reasons:")
            reason_count: dict = {}
            for r in rejections:
                reason = r.get("reason", "(no reason)")[:60]
                reason_count[reason] = reason_count.get(reason, 0) + 1
            top = sorted(reason_count.items(), key=lambda x: -x[1])[:5]
            for reason, count in top:
                print(f"    [{count}x] {reason}")
        if len(rejections) > 0:
            print(f"\n  Most rejected repo:")
            repo_count: dict = {}
            for r in rejections:
                repo = r.get("repo", "unknown")
                repo_count[repo] = repo_count.get(repo, 0) + 1
            most_rejected = sorted(repo_count.items(), key=lambda x: -x[1])[0]
            print(f"    {most_rejected[0].split('/')[-1]}: {most_rejected[1]} rejections")
        if len(approvals) > 0:
            print(f"\n  Most approved repo:")
            repo_count = {}
            for a in approvals:
                repo = a.get("repo", "unknown")
                repo_count[repo] = repo_count.get(repo, 0) + 1
            most_approved = sorted(repo_count.items(), key=lambda x: -x[1])[0]
            print(f"    {most_approved[0].split('/')[-1]}: {most_approved[1]} approvals")
        return 0

    if args.type == "rejections" or args.type is None:
        rejections = data.get("rejections", [])
        print(f"📕 Rejections ({len(rejections)} total):")
        print("=" * 60)
        if not rejections:
            print("  (none)")
        for r in rejections[: args.limit or 20]:
            ts = r.get("timestamp", "")
            date_str = ts[:10] if ts else "?"
            repo_name = r.get("repo", "?").split("/")[-1] or "?"
            desc = r.get("description", "")
            scenario = r.get("scenario", "")
            suggested = r.get("suggested_direction", "")
            impact = r.get("impact_score", 0)
            print(f"  [{date_str}] {repo_name}")
            print(f"    {desc}")
            if scenario:
                print(f"    Scenario: {scenario}")
            if suggested:
                print(f"    → Fix: {suggested[:80]}")
            if impact:
                print(f"    Impact: {impact:.0%}")
            print()

    if args.type == "approvals" or args.type is None:
        approvals = data.get("approvals", [])
        print(f"📗 Approvals ({len(approvals)} total):")
        print("=" * 60)
        if not approvals:
            print("  (none)")
        for a in approvals[: args.limit or 20]:
            ts = a.get("timestamp", "")
            date_str = ts[:10] if ts else "?"
            repo_name = a.get("repo", "?").split("/")[-1] or "?"
            desc = a.get("description", "")
            scenario = a.get("scenario", "")
            impact = a.get("impact_score", 0)
            print(f"  [{date_str}] {repo_name}")
            print(f"    {desc}")
            if scenario:
                print(f"    Scenario: {scenario}")
            if impact:
                print(f"    Impact: {impact:.0%}")
            print()

    if args.type not in ("rejections", "approvals", None):
        print(f"❌ Unknown type: {args.type}. Use --type rejections or --type approvals.")
        return 1
    return 0


def cmd_trends(args) -> int:
    """Show scan trends for repositories. v4.3."""
    import json

    config = load_config()
    repos = [Repository(**r) for r in config.get("repositories", [])]
    target = args.repo.strip() if args.repo else ""

    if args.all:
        targets = repos
    elif target:
        targets = [r for r in repos if target in str(r.path)]
        if not targets:
            print(f"❌ Repo not found: {target}")
            return 1
    else:
        print("Usage: auto-evolve trends --repo <path> OR --all")
        return 1

    print("📈 Scan Trends")
    print("=" * 60)
    for repo in targets:
        repo_path = repo.resolve_path()
        history_file = repo_path / ".auto-evolve" / "scan-history.json"
        print(f"\n📁 {repo_path.name}")
        print(f"   Path: {repo_path}")

        if not history_file.exists():
            print("   Status: No scan history (run `auto-evolve scan` first)")
            continue

        try:
            data = json.loads(history_file.read_text(encoding="utf-8"))
            # data structure: { repo_path: [scan_round1, scan_round2, ...] }
            scans = None
            for v in data.values():
                if isinstance(v, list) and len(v) > 0:
                    scans = v
                    break
            if not scans or len(scans) < 2:
                print(f"   Status: Need at least 2 scans for trend (have {len(scans) if scans else 0})")
                continue

            # Count total findings per scan round
            counts = []
            for scan in scans[:5]:
                total = sum(len(f) for f in scan.values() if isinstance(f, list))
                counts.append(total)

            counts_display = list(reversed(counts))
            print(f"   Recent scans: {' → '.join(str(c) for c in counts_display)}")

            if len(counts) >= 2:
                delta = counts[0] - counts[1]
                if delta > 0:
                    print(f"   Trend: 📈 +{delta} findings since last scan")
                elif delta < 0:
                    print(f"   Trend: 📉 {delta} findings (improved)")
                else:
                    print(f"   Trend: ➡️  No change")
        except Exception as e:
            print(f"   Error reading history: {e}")

    return 0



def cmd_log(args) -> int:
    catalog = load_catalog()
    if not catalog["iterations"]:
        print("No iterations recorded yet.")
        return 0
    print("📚 Iteration Log")
    print("=" * 50)
    limit = args.limit or 10
    for iteration in catalog["iterations"][:limit]:
        status_icon = {
            "completed": "✅",
            "pending-approval": "⏳",
            "full-auto-completed": "⚡",
            "dry-run": "⚡",
            "rolled-back": "🔄",
        }.get(iteration["status"], "❓")

        alert_flag = " 🚨" if iteration.get("has_alert") else ""
        cost_str = ""
        if iteration.get("total_cost_usd"):
            cost_str = f" 💰${iteration['total_cost_usd']:.4f}"
        llm_str = f" 🤖{iteration.get('llm_calls', 0)}calls" if iteration.get("llm_calls", 0) > 0 else ""

        print(f"\n{status_icon} {iteration['version']}{alert_flag}{cost_str}{llm_str}")
        print(f"   Date: {iteration['date']}")
        print(f"   Status: {iteration['status']}")
        print(f"   Risk: {iteration.get('risk_level', 'unknown')}")
        if iteration.get("items_auto"):
            print(f"   Auto: {iteration['items_auto']}")
        if iteration.get("items_approved"):
            print(f"   Approved: {iteration['items_approved']}")
        if iteration.get("items_rejected"):
            print(f"   Rejected: {iteration['items_rejected']}")
        if iteration.get("rollback_of"):
            print(f"   Rolled back: {iteration['rollback_of']}")
        if iteration.get("has_alert"):
            print(f"   🚨 Alert: quality gate failed")
    return 0


# ===========================================================
# v3.2: effects command
# ===========================================================

def cmd_effects(args) -> int:
    """Show effect tracking reports for iterations."""
    iteration_id = args.iteration_id

    catalog = load_catalog()
    if not catalog["iterations"]:
        print("No iterations found.")
        return 0

    if iteration_id:
        target_iter = next((i for i in catalog["iterations"] if i["version"] == iteration_id), None)
        if not target_iter:
            print(f"Iteration {iteration_id} not found.")
            return 1
        iteration_ids = [iteration_id]
    else:
        iteration_ids = [i["version"] for i in catalog["iterations"][: args.limit or 5]]

    for iid in iteration_ids:
        effect_file = ITERATIONS_DIR / iid / "effect.json"
        if not effect_file.exists():
            continue
        effect = json.loads(effect_file.read_text())
        verdict_icon = {"positive": "✅", "neutral": "➖", "negative": "❌"}.get(effect["verdict"], "➖")
        print(f"\n{verdict_icon} Iteration {iid} — {effect['verdict'].upper()}")
        print(f"   Date: {effect['date']}")
        print(f"   Summary: {effect['summary']}")
        totals = effect.get("totals", {})
        if totals.get("todos_resolved"):
            print(f"   TODOs resolved: {totals['todos_resolved']}")
        if totals.get("coverage_delta"):
            print(f"   Coverage delta: {totals['coverage_delta']:+.1f}%")
        if totals.get("duplicate_lines_delta"):
            print(f"   Duplicate lines: {totals['duplicate_lines_delta']:+,}")
        if totals.get("code_lines_delta"):
            print(f"   Code lines: {totals['code_lines_delta']:+,}")

    if not iteration_ids:
        print("No effect reports found. Run a scan first.")
    return 0


# ===========================================================
# v3.2: costs command
# ===========================================================

def cmd_costs(args) -> int:
    """Show LLM cost tracking for iterations."""
    iteration_id = args.iteration_id

    catalog = load_catalog()
    if not catalog["iterations"]:
        print("No iterations found.")
        return 0

    if iteration_id:
        target_iter = next((i for i in catalog["iterations"] if i["version"] == iteration_id), None)
        if not target_iter:
            print(f"Iteration {iteration_id} not found.")
            return 1
        iteration_ids = [iteration_id]
    else:
        iteration_ids = [i["version"] for i in catalog["iterations"][: args.limit or 5]]

    cost_tracker = CostTracker()
    total_all = 0.0
    total_calls = 0

    for iid in iteration_ids:
        cost_summary = cost_tracker.get_iteration_cost(iid)
        if cost_summary["total_calls"] == 0:
            continue
        total_all += cost_summary["total_cost_usd"]
        total_calls += cost_summary["total_calls"]
        print(f"\n💰 Iteration {iid}")
        print(f"   Calls: {cost_summary['total_calls']}")
        print(f"   Tokens: {cost_summary['total_tokens']:,}")
        print(f"   Cost: ${cost_summary['total_cost_usd']:.6f}")

        # Show per-model breakdown
        calls = cost_tracker.load_calls(iid)
        by_model: dict[str, dict] = {}
        for call in calls:
            model = call["model"]
            by_model.setdefault(model, {"calls": 0, "tokens": 0, "cost": 0.0})
            by_model[model]["calls"] += 1
            by_model[model]["tokens"] += call["total_tokens"]
            by_model[model]["cost"] += call["estimated_cost_usd"]
        for model, stats in by_model.items():
            print(f"   [{model}] {stats['calls']} calls, {stats['tokens']:,} tokens, ${stats['cost']:.6f}")

    if total_calls == 0:
        print("No LLM costs recorded. Run a scan with LLM analysis.")
    else:
        print(f"\n💰 TOTAL: {total_calls} calls, ${total_all:.6f}")
    return 0


# ===========================================================
# CLI Entry Point
# ===========================================================

def _build_argument_parser() -> argparse.ArgumentParser:
    """Build and return the root argument parser with all subcommands."""
    parser = argparse.ArgumentParser(
        description="Auto-Evolve v3.5 — LLM-driven automated skill iteration manager",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scan
    scan_p = subparsers.add_parser("scan", help="Scan and evolve skills")
    scan_p.add_argument("--dry-run", action="store_true", help="Preview only, no commits")
    scan_p.add_argument(
        "--recall-persona", type=str, default="",
        help="Persona to recall context from (main|tseng|wukong|bajie|bailong|shaseng, default: auto-detect)"
    )
    scan_p.add_argument(
        "--memory-source", type=str,
        choices=["auto", "openclaw", "hawkbridge", "both"],
        default="auto",
        help="Memory source: auto (openclaw primary+hawkbridge supplement), openclaw, hawkbridge, or both"
    )
    scan_p.add_argument(
        "--repo", type=str, default="",
        help="Scan only the specified repository path (default: all configured repos)"
    )
    scan_p.add_argument(
        "--github-event", type=str, default="",
        help="GitHub event type (pr_review, push, manual). When set, results are posted to GitHub."
    )

    # confirm
    confirm_p = subparsers.add_parser("confirm", help="Confirm pending changes (semi-auto mode)")
    confirm_p.add_argument("--iteration", dest="iteration_id", type=str, help="Iteration ID")

    # reject
    reject_p = subparsers.add_parser("reject", help="Reject a pending change")
    reject_p.add_argument("id", type=int, help="Item ID to reject")
    reject_p.add_argument("--reason", type=str, help="Rejection reason")
    reject_p.add_argument("--iteration", dest="iteration_id", type=str, help="Iteration ID")

    # approve
    approve_p = subparsers.add_parser("approve", help="Approve pending changes")
    approve_p.add_argument("--all", action="store_true", help="Approve all pending items")
    approve_p.add_argument("--ids", type=str, help="Comma-separated IDs (e.g. 1,2,3)")
    approve_p.add_argument("ids", nargs="?", type=str, help="IDs to approve (positional)")
    approve_p.add_argument("--iteration", dest="iteration_id", type=str, help="Iteration ID")
    approve_p.add_argument("--reason", type=str, help="Reason for approval (recorded in learnings)")

    # repo-add
    repo_add_p = subparsers.add_parser("repo-add", help="Add a repository to monitor")
    repo_add_p.add_argument("path", type=str, help="Repository path")
    repo_add_p.add_argument("--type", type=str, choices=REPO_TYPES, help="Repository type")
    repo_add_p.add_argument("--monitor", action="store_true", default=True, help="Enable auto-monitor")

    # repo-list
    subparsers.add_parser("repo-list", help="List configured repositories")

    # trends (v4.3)
    trends_p = subparsers.add_parser("trends", help="Show scan trends for repositories (v4.3)")
    trends_p.add_argument("--repo", type=str, default="", help="Specific repo path to show trends for")
    trends_p.add_argument("--all", action="store_true", help="Show trends for all monitored repos")

    # rollback
    rollback_p = subparsers.add_parser("rollback", help="Rollback to a previous iteration")
    rollback_p.add_argument("--to", required=True, dest="to", type=str, help="Target version")
    rollback_p.add_argument("--reason", type=str, help="Rollback reason")
    rollback_p.add_argument("--item", type=int, dest="item", help="Cherry-pick: only rollback specific item ID")

    # release
    release_p = subparsers.add_parser("release", help="Create a GitHub release")
    release_p.add_argument("--version", required=True, dest="version", type=str, help="Version tag (e.g. 2.3.0)")
    release_p.add_argument("--changelog", type=str, default="", help="Changelog / release notes")

    # schedule (v3.2)
    schedule_p = subparsers.add_parser("schedule", help="Schedule management (cron setup)")
    schedule_p.add_argument("--every", type=int, help="Set scan interval in hours")
    schedule_p.add_argument("--suggest", action="store_true", help="Smart scheduling recommendations (v3.2)")
    schedule_p.add_argument("--auto", action="store_true", help="Apply recommended intervals (v3.2)")
    schedule_p.add_argument("--show", action="store_true", help="Show current schedule")
    schedule_p.add_argument("--remove", action="store_true", help="Remove cron job")

    # set-mode
    set_mode_p = subparsers.add_parser("set-mode", help="Set operation mode")
    set_mode_p.add_argument("mode", type=str, choices=["semi-auto", "full-auto"], help="Mode")

    # set-rules
    set_rules_p = subparsers.add_parser("set-rules", help="Set full-auto execution rules")
    set_rules_p.add_argument("--low", type=lambda x: x.lower() == "true", help="Execute low-risk (true/false)")
    set_rules_p.add_argument("--medium", type=lambda x: x.lower() == "true", help="Execute medium-risk (true/false)")
    set_rules_p.add_argument("--high", type=lambda x: x.lower() == "true", help="Execute high-risk (true/false)")

    # learnings
    learnings_p = subparsers.add_parser("learnings", help="Show learning history")
    learnings_p.add_argument("--type", type=str, choices=["rejections", "approvals"], help="Filter by type")
    learnings_p.add_argument("--limit", type=int, default=20, help="Limit entries")
    learnings_p.add_argument("--summary", action="store_true", help="Show summary statistics (v4.3)")

    # log
    log_p = subparsers.add_parser("log", help="Show iteration log")
    log_p.add_argument("--limit", type=int, default=10, help="Limit entries")

    # effects (v3.2)
    effects_p = subparsers.add_parser("effects", help="Show effect tracking reports (v3.2)")
    effects_p.add_argument("--iteration", dest="iteration_id", type=str, help="Specific iteration ID")
    effects_p.add_argument("--limit", type=int, default=5, help="Limit iterations shown")

    # costs (v3.2)
    costs_p = subparsers.add_parser("costs", help="Show LLM cost tracking (v3.2)")
    costs_p.add_argument("--iteration", dest="iteration_id", type=str, help="Specific iteration ID")
    costs_p.add_argument("--limit", type=int, default=5, help="Limit iterations shown")

    return parser


def main() -> int:
    parser = _build_argument_parser()
    args = parser.parse_args()

    commands: dict[str, callable] = {
        "scan": cmd_scan,
        "confirm": cmd_confirm,
        "reject": cmd_reject,
        "approve": cmd_approve,
        "repo-add": cmd_repo_add,
        "repo-list": cmd_repo_list,
        "rollback": cmd_rollback,
        "release": cmd_release,
        "schedule": cmd_schedule,
        "set-mode": cmd_set_mode,
        "set-rules": cmd_set_rules,
        "learnings": cmd_learnings,
        "trends": cmd_trends,
        "log": cmd_log,
        "effects": cmd_effects,
        "costs": cmd_costs,
    }

    return commands[args.command](args)


if __name__ == "__main__":
    sys.exit(main())
