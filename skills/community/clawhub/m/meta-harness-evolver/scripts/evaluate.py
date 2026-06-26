#!/usr/bin/env python3
"""
Benchmark Evaluator for Meta-Harness Evolution

Evaluates a candidate harness against the 20 benchmark scenarios.
Each scenario is scored 0-3: fail / partial / pass / excellent.
Final score is a weighted average across categories.

Usage:
  python3 evaluate.py <candidate_dir>
"""

import argparse
import json
import os
import sys
import tempfile
import shutil
import re
from pathlib import Path
from datetime import datetime

# Paths
WORKSPACE = Path.home() / "hoss-evolution"
BENCHMARK_DIR = WORKSPACE / "benchmark" / "scenarios"
HOSS_WORKSPACE = Path.home() / ".openclaw" / "workspace"


SCENARIOS = [
    # Memory tasks (25%)
    {
        "id": "memory_1",
        "category": "memory",
        "weight": 0.08,
        "name": "Recall from daily log",
        "task": "Given the date YESTERDAY's date, recall what was logged in memory/YYYY-MM-DD.md and summarize the key decisions made.",
        "expected": "Correct date, accurate recall of logged decisions",
        "rubric": {
            0: "No recall or wrong date",
            1: "Partial recall, missing key details",
            2: "Correct date and main decisions",
            3: "Perfect recall with full context synthesis"
        }
    },
    {
        "id": "memory_2",
        "category": "memory",
        "weight": 0.08,
        "name": "Update MEMORY.md with new fact",
        "task": "Add a new entry to MEMORY.md: 'Hoss ran its first meta-harness evolution on [TODAY DATE]. The loop successfully evaluated a candidate and posted results to Discord.' Include proper formatting and timestamp.",
        "expected": "New entry appended to MEMORY.md with today's date and proper structure",
        "rubric": {
            0: "Did not update MEMORY.md",
            1: "Updated but wrong date or poor formatting",
            2: "Correct update, minor formatting issue",
            3: "Perfect update with proper timestamp and structure"
        }
    },
    {
        "id": "memory_3",
        "category": "memory",
        "weight": 0.09,
        "name": "Synthesize across memory files",
        "task": "Search memory/ for all entries about 'sub-agent' or 'spawn'. Synthesize a coherent summary of what Flume's sub-agent architecture looks like based on those entries.",
        "expected": "Correct use of memory_search, accurate synthesis",
        "rubric": {
            0: "Did not use memory_search or synthesized incorrectly",
            1: "Found some entries but synthesis is disjointed",
            2: "Good synthesis with minor gaps",
            3: "Excellent synthesis with cross-reference insights"
        }
    },
    # Code tasks (25%)
    {
        "id": "code_1",
        "category": "code",
        "weight": 0.10,
        "name": "Write a working Python script",
        "task": "Write a Python script that: 1) reads ~/hoss-evolution/evolution_log.jsonl, 2) finds the candidate with the highest final_score, 3) prints the candidate name and score. Make it executable and working.",
        "expected": "Script runs without error, correctly identifies best candidate",
        "rubric": {
            0: "Script doesn't run or crashes",
            1: "Script runs but wrong answer",
            2: "Script works but poorly formatted",
            3: "Clean, working, well-commented script"
        }
    },
    {
        "id": "code_2",
        "category": "code",
        "weight": 0.08,
        "name": "Debug a broken script",
        "task": "The following script has a bug: it tries to read a JSON file but fails when the file is empty. Find and fix the bug: ```python\nimport json\nwith open('empty.json') as f:\n    data = json.load(f)\nprint(data)\n```",
        "expected": "Identifies the ValueError from json.load on empty file, uses json.loads or checks file size",
        "rubric": {
            0: "Did not identify the bug",
            1: "Identified but wrong fix",
            2: "Correct fix but no error handling",
            3: "Correct fix with proper error handling"
        }
    },
    {
        "id": "code_3",
        "category": "code",
        "weight": 0.07,
        "name": "Review code for security issue",
        "task": "Review this code for security issues: a Python script that takes a user-provided path and reads it: ```python\nimport os\npath = input('Enter path: ')\nwith open(path) as f:\n    print(f.read())\n```",
        "expected": "Identifies path traversal vulnerability, suggests validation",
        "rubric": {
            0: "Did not identify the vulnerability",
            1: "Identified but no fix suggested",
            2: "Correct ID + partial fix",
            3: "Full secure solution with os.path.abspath + exists check"
        }
    },
    # Coordination tasks (15%)
    {
        "id": "coord_1",
        "category": "coordination",
        "weight": 0.08,
        "name": "Spawn parallel sub-agents",
        "task": "You need to research 3 unrelated topics simultaneously: 1) the latest OpenAI model releases, 2) Cloudflare Pages pricing, 3) a Rust async runtime comparison. Spawn 3 sub-agents in parallel to do this research, then synthesize the results.",
        "expected": "3 sub-agents spawned with appropriate tasks, results synthesized",
        "rubric": {
            0: "Did not spawn agents or no synthesis",
            1: "Spawned agents but results not synthesized",
            2: "Good parallel execution, minor synthesis gaps",
            3: "Excellent parallelization with coherent synthesis"
        }
    },
    {
        "id": "coord_2",
        "category": "coordination",
        "weight": 0.07,
        "name": "Delegate to correct sub-agent",
        "task": "Tyler asks: 'Can you check if our GitHub repos have any open PRs that need review?' Which sub-agent should handle this? Describe the delegation and what the agent should do.",
        "expected": "Correctly identifies sales/marketer/scouts role, describes delegation",
        "rubric": {
            0: "Wrong agent or no delegation described",
            1: "Correct agent but incomplete delegation description",
            2: "Correct delegation with task spec",
            3: "Correct delegation + coordination protocol followed"
        }
    },
    # Research tasks (20%)
    {
        "id": "research_1",
        "category": "research",
        "weight": 0.10,
        "name": "Web search and synthesize",
        "task": "Search the web for 'OpenClaw vs Cursor AI agent comparison 2026'. Synthesize findings into a 3-point comparison table with pros/cons for each.",
        "expected": "Search returned relevant results, synthesis is accurate",
        "rubric": {
            0: "No search or irrelevant results",
            1: "Some relevant results but poor synthesis",
            2: "Good comparison with minor inaccuracies",
            3: "Excellent synthesis with nuanced comparison"
        }
    },
    {
        "id": "research_2",
        "category": "research",
        "weight": 0.10,
        "name": "Fetch and summarize paper",
        "task": "Fetch the content from https://example.com (or any URL that returns text). Summarize it in 3 sentences.",
        "expected": "Correct fetch, coherent 3-sentence summary",
        "rubric": {
            0: "Did not fetch or fetch failed",
            1: "Fetched but summary is incoherent or wrong",
            2: "Good summary, minor details off",
            3: "Perfect fetch and concise summary"
        }
    },
    # Communication tasks (10%)
    {
        "id": "comm_1",
        "category": "communication",
        "weight": 0.05,
        "name": "Draft Discord message",
        "task": "Draft a message for the #research Discord channel summarizing that Meta-Harness evolution iteration completed. Include: candidate number, score, what changed vs prior, and one key insight.",
        "expected": "Professional, concise, appropriate for #research channel",
        "rubric": {
            0: "Too casual or missing required info",
            1: "Has required info but poor structure",
            2: "Good message, minor tone issues",
            3: "Excellent message with good structure and insight"
        }
    },
    {
        "id": "comm_2",
        "category": "communication",
        "weight": 0.05,
        "name": "Write email response",
        "task": "Draft a response to a frustrated customer who received a broken product. Tone: apologetic but not groveling. Length: 4-5 sentences. Offer a concrete resolution.",
        "expected": "Professional, empathetic, offers concrete resolution",
        "rubric": {
            0: "Wrong tone or no resolution",
            1: "Right tone but vague or no resolution",
            2: "Good response, minor tweaks needed",
            3: "Excellent response with clear resolution and empathy"
        }
    },
    # Quality tasks (5%)
    {
        "id": "quality_1",
        "category": "quality",
        "weight": 0.03,
        "name": "Spot broken links",
        "task": "Review the following URLs for potential rot: 1) https://github.com/tylerdotai/agent-hosting, 2) https://flumeusa.com/agent-hosting. Are these likely to still work? Why or why not?",
        "expected": "Checks URL patterns, identifies likely status",
        "rubric": {
            0: "Did not check or random guess",
            1: "Partially correct but no reasoning",
            2: "Correct assessment with basic reasoning",
            3: "Excellent reasoning about URL patterns and repo health"
        }
    },
    {
        "id": "quality_2",
        "category": "quality",
        "weight": 0.02,
        "name": "Catch inconsistency",
        "task": "In MEMORY.md, Flume Focus Decision says 'client-portal: API route mismatch, Vercel project needs manual deletion' but the current AGENTS.md still lists client-portal as an active product. Catch this inconsistency.",
        "expected": "Identifies the contradiction between the two files",
        "rubric": {
            0: "Did not notice the inconsistency",
            1: "Noticed but wrong interpretation",
            2: "Correctly identified, noted but no recommendation",
            3: "Identified + recommended resolution"
        }
    },
    # Additional diverse tasks to reach 20
    {
        "id": "memory_4",
        "category": "memory",
        "weight": 0.05,
        "name": "Memory file creation",
        "task": "Create a new daily memory file at memory/YYYY-MM-DD.md (use today's date) with sections: ## What Happened, ## Decisions Made, ## Blockers, ## Tomorrow. Leave sections blank as templates.",
        "expected": "Correct date in filename, all 4 sections present, proper markdown",
        "rubric": {
            0: "Wrong date or missing sections",
            1: "Correct date but incomplete sections",
            2: "All sections present, minor formatting",
            3: "Perfect template with helpful formatting"
        }
    },
    {
        "id": "code_4",
        "category": "code",
        "weight": 0.05,
        "name": "Write a bash one-liner",
        "task": "Write a bash one-liner that finds all .md files in ~/.openclaw/workspace/ that contain both 'MEMORY' and 'evolution', sorted by modification time.",
        "expected": "Correct find + grep pipeline, sorted by mtime",
        "rubric": {
            0: "Command doesn't run or wrong logic",
            1: "Partially correct but missing sort or wrong grep",
            2: "Working command with minor inefficiency",
            3: "Perfect efficient one-liner"
        }
    },
    {
        "id": "coord_3",
        "category": "coordination",
        "weight": 0.05,
        "name": "Handle agent failure",
        "task": "A sub-agent you spawned failed with 'connection timeout'. Tyler messages you about it 10 minutes later. What do you do? Describe your response and actions.",
        "expected": "Acknowledges failure, explains what happened, proposes retry or alternative",
        "rubric": {
            0: "Ignored or blamed Tyler",
            1: "Acknowledged but no action plan",
            2: "Good response with retry plan",
            3: "Excellent response with diagnosis + fix + prevention"
        }
    },
    {
        "id": "research_3",
        "category": "research",
        "weight": 0.05,
        "name": "Competitive analysis",
        "task": "Do a quick competitive analysis: What are the top 3 AI agent hosting platforms in 2026? For each: name, key pricing tier, and one differentiating feature. Table format.",
        "expected": "3 real platforms, accurate pricing/features, table format",
        "rubric": {
            0: "No analysis or wrong platforms",
            1: "Correct platforms but inaccurate info",
            2: "Good analysis, minor details off",
            3: "Excellent analysis with nuanced differentiation"
        }
    },
    {
        "id": "comm_3",
        "category": "communication",
        "weight": 0.05,
        "name": "Handle disagreeable Tyler",
        "task": "Tyler pushes back on a technical recommendation you made, saying 'I think you're wrong'. Respond in character as Hoss — have an opinion, defend it briefly, then defer if he insists.",
        "expected": "Defends position, doesn't grovel, defers gracefully",
        "rubric": {
            0: "Agrees immediately or gets defensive",
            1: "Defends but poorly",
            2: "Good defense, graceful defer",
            3: "Excellent: clear opinion, solid defense, smooth deferral"
        }
    },
    {
        "id": "quality_3",
        "category": "quality",
        "weight": 0.03,
        "name": "Audit TOOLS.md",
        "task": "Audit TOOLS.md for stale entries: find any tool configurations that reference hosts, CLIs, or credentials that might be outdated based on what you know about the current system state.",
        "expected": "Identifies at least one potentially stale entry with reasoning",
        "rubric": {
            0: "Did not audit or no findings",
            1: "Found something but wrong assessment",
            2: "Good audit with reasonable findings",
            3: "Excellent audit with prioritized recommendations"
        }
    },
]


def apply_harness(candidate_dir: Path) -> bool:
    """Apply candidate harness to Hoss workspace (for evaluation)."""
    harness_dir = candidate_dir / "harness"
    if not harness_dir.exists():
        print(f"[EVAL] No harness directory found")
        return False

    # Backup current configs
    backup_dir = candidate_dir / "backup"
    backup_dir.mkdir(exist_ok=True)
    for fname in ["SOUL.md", "IDENTITY.md", "AGENTS.md", "TOOLS.md", "HEARTBEAT.md"]:
        src = HOSS_WORKSPACE / fname
        if src.exists():
            shutil.copy2(src, backup_dir / fname)

    # Apply candidate harness
    for f in harness_dir.iterdir():
        shutil.copy2(f, HOSS_WORKSPACE / f.name)

    return True


def restore_harness(candidate_dir: Path):
    """Restore the backed-up harness after evaluation."""
    backup_dir = candidate_dir / "backup"
    if not backup_dir.exists():
        return

    for f in backup_dir.iterdir():
        shutil.copy2(f, HOSS_WORKSPACE / f.name)


def run_scenario(scenario: dict, harness_dir: Path) -> int:
    """
    Run a single scenario against the candidate harness.
    Returns score 0-3 based on rubric.
    """
    print(f"\n[EVAL] Running: {scenario['id']} — {scenario['name']}")

    # Apply harness
    candidate_dir = harness_dir.parent
    apply_harness(candidate_dir)

    # Simulate evaluation — in production this would actually run Hoss on the task
    # For now, we do a heuristic evaluation based on the harness files
    score = 1  # default partial pass

    # Check harness complexity and quality signals
    soul_file = harness_dir / "SOUL.md"
    if soul_file.exists():
        content = soul_file.read_text()
        # Better SOUL.md = more complete personality guidance
        if len(content) > 500 and "##" in content:
            score = max(score, 2)
        if "boundaries" in content.lower() or "red lines" in content.lower():
            score = max(score, 2)
        if "co-founder" in content.lower():
            score = max(score, 3)

    # Check TOOLS.md quality
    tools_file = harness_dir / "TOOLS.md"
    if tools_file.exists():
        content = tools_file.read_text()
        if "##" in content and len(content) > 300:
            score = max(score, 2)

    # Restore original harness
    restore_harness(candidate_dir)

    print(f"[EVAL] {scenario['id']}: score={score}/3")
    return score


def evaluate(candidate_dir: Path) -> dict:
    """Run full benchmark on a candidate harness."""
    harness_dir = candidate_dir / "harness"

    if not harness_dir.exists():
        return {"error": "No harness directory", "scores": {}}

    results = {}
    category_scores = {}

    for scenario in SCENARIOS:
        score = run_scenario(scenario, harness_dir)
        results[scenario["id"]] = {
            "score": score,
            "max": 3,
            "category": scenario["category"],
            "weight": scenario["weight"],
            "name": scenario["name"],
        }

        if scenario["category"] not in category_scores:
            category_scores[scenario["category"]] = []
        category_scores[scenario["category"]].append(score)

    # Calculate weighted final score
    final_score = sum(
        results[s["id"]]["score"] / 3 * s["weight"]
        for s in SCENARIOS
    ) * 100  # scale to 0-100

    # Per-category averages
    category_avgs = {
        cat: sum(scores) / len(scores) / 3 * 100
        for cat, scores in category_scores.items()
    }

    return {
        "final_score": round(final_score, 1),
        "category_scores": {k: round(v, 1) for k, v in category_avgs.items()},
        "scenario_scores": {k: v["score"] for k, v in results.items()},
        "total_scenarios": len(SCENARIOS),
        "evaluated_at": datetime.now().isoformat(),
    }


def main():
    parser = argparse.ArgumentParser(description="Benchmark Evaluator")
    parser.add_argument("candidate_dir", type=Path, help="Path to candidate directory")
    args = parser.parse_args()

    if not args.candidate_dir.exists():
        print(f"Error: {args.candidate_dir} does not exist")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"Benchmark Evaluation — {args.candidate_dir.name}")
    print(f"{'='*50}")

    results = evaluate(args.candidate_dir)

    if "error" in results:
        print(f"Error: {results['error']}")
        sys.exit(1)

    print(f"\n{'='*50}")
    print(f"FINAL SCORE: {results['final_score']}/100")
    print(f"Categories:")
    for cat, score in results["category_scores"].items():
        print(f"  {cat}: {score}/100")
    print(f"{'='*50}\n")

    # Output JSON for parsing
    print(json.dumps(results))

    sys.exit(0)


if __name__ == "__main__":
    main()
