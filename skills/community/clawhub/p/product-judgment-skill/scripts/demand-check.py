#!/usr/bin/env python3
"""
demand-check.py — Product Judgment CLI
Product Judgment Skill / 产品需求审判

This script is a demand review COLLECTOR and JUDGMENT.md GENERATOR.
The structural logic here surfaces the right questions at the right time.
Deep product judgment comes from the LLM Skill (SKILL.md), not from if-else rules.

Usage:
    python demand-check.py                        # Interactive review (new demand)
    python demand-check.py --scan                 # Scan project first, then review
    python demand-check.py --scope                # Scope check against existing JUDGMENT.md
    python demand-check.py --from <file>          # Pre-load demand from existing doc (PRD/README/idea.md)
    python demand-check.py --feature "<text>"     # Pass demand description directly, skip that question
    python demand-check.py --output <path>        # Custom output path (default: ./JUDGMENT.md)
    python demand-check.py --json                 # Also write JUDGMENT.json (structured, for agents)
    python demand-check.py --strict               # Output verdict only, no explanation

Combine flags:
    python demand-check.py --scan --from docs/prd.md
    python demand-check.py --from README.md --json
    python demand-check.py --feature "AI会议纪要助手" --strict

Outputs JUDGMENT.md to project root. Commit it. Let everyone see the reasoning.
"""

import os
import sys
import json
import re
import subprocess
import textwrap
from pathlib import Path
from datetime import datetime

# ─── Document Parser (--from mode) ───────────────────────────────────────────

def parse_from_file(filepath):
    """
    Read an existing document (PRD / README / idea.md / issue) and extract
    demand-relevant information to pre-fill the interview.

    Returns a dict of pre-filled data. Empty string = not found, user will be asked.
    Fields mirror the run_interview() data dict keys.
    """
    path = Path(filepath)
    if not path.exists():
        print(f"\033[91m  Error: File not found: {filepath}\033[0m")
        sys.exit(1)

    text = path.read_text(errors="ignore")
    prefill = {
        "_source_file": str(path),
        "_source_text": text[:4000],
        "demand_raw": "",
        "demand_source": "",
        "target_user": "",
        "trigger_context": "",
        "user_frequency": "",
        "old_experience": "",
        "new_experience": "",
        "replacement_cost": "",
        "assumptions": [],
        "business_value": "",
        "resource_ask": "",
    }

    lines = text.split("\n")
    demand_lines = []
    in_section = False
    section_triggers = {"overview", "background", "summary", "context", "description",
                        "需求描述", "背景", "概述", "功能描述", "产品描述"}

    for i, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("#"):
            header_text = stripped.lstrip("#").strip().lower()
            if any(t in header_text for t in section_triggers):
                in_section = True
                demand_lines = []
                continue
            elif in_section and stripped.startswith("#"):
                break
        if in_section and stripped:
            demand_lines.append(stripped)
            if len(demand_lines) >= 6:
                break

    if not demand_lines:
        buffer = []
        for line in lines:
            s = line.strip()
            if s and not s.startswith("#") and not s.startswith("!") and not s.startswith(">") and len(s) > 30:
                buffer.append(s)
                if len(buffer) >= 4:
                    break
        demand_lines = buffer

    if demand_lines:
        prefill["demand_raw"] = " ".join(demand_lines)

    user_patterns = [
        r"(?:target user|目标用户|用户群|user group|audience)[：:]\s*(.+)",
        r"(?:for|面向|适用于)\s+(.{5,60}?)(?:\.|，|。|$)",
        r"(?:用户是|user is|users are)\s+(.{5,60}?)(?:\.|，|。|$)",
    ]
    for pat in user_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            prefill["target_user"] = m.group(1).strip()[:120]
            break

    assumption_section = re.search(
        r"(?:假设|assumption|前提)[^\n]*\n((?:[-*\d].+\n?){1,8})",
        text, re.IGNORECASE
    )
    if assumption_section:
        raw = assumption_section.group(1)
        items = [re.sub(r"^[-*\d.\s]+", "", l).strip() for l in raw.split("\n") if l.strip()]
        prefill["assumptions"] = [a for a in items if len(a) > 5][:6]

    biz_patterns = [
        r"(?:business value|商业价值|变现|revenue|盈利|收益)[：:]\s*(.+)",
        r"(?:目标|goal|objective)[：:]\s*(.{10,120}?)(?:\n|。|\.)",
    ]
    for pat in biz_patterns:
        m = re.search(pat, text, re.IGNORECASE)
        if m:
            prefill["business_value"] = m.group(1).strip()[:200]
            break

    source_signals = {
        "竞品": "Competitor launched something",
        "competitor": "Competitor launched something",
        "用户反馈": "User complaints",
        "user feedback": "User complaints",
        "老板": "CEO / leadership",
        "ceo": "CEO / leadership",
        "leader": "CEO / leadership",
        "调研": "User research",
        "research": "User research",
    }
    text_lower = text.lower()
    for signal, source_val in source_signals.items():
        if signal in text_lower:
            prefill["demand_source"] = source_val
            break

    return prefill


def show_prefill_summary(prefill):
    section("📄 Document Pre-fill / 文档预读结果")
    print(f"  Source: {BOLD}{prefill['_source_file']}{RESET}")
    print()

    fields = [
        ("Demand description", "demand_raw"),
        ("Target user",        "target_user"),
        ("Business value",     "business_value"),
        ("Demand source",      "demand_source"),
    ]
    found = 0
    for label, key in fields:
        val = prefill.get(key, "")
        if val:
            found += 1
            display = val[:100] + ("..." if len(val) > 100 else "")
            print(f"  {GREEN}✓{RESET} {BOLD}{label}:{RESET} {DIM}{display}{RESET}")
        else:
            print(f"  {DIM}○ {label}: not detected{RESET}")

    if prefill.get("assumptions"):
        found += 1
        print(f"  {GREEN}✓{RESET} {BOLD}Assumptions:{RESET} {len(prefill['assumptions'])} found")

    print()
    print(DIM + f"  {found} fields pre-filled. You'll be asked to confirm or supplement each." + RESET)
    print()


def ask_with_prefill(prompt, prefill_value, required=True, multiline=False):
    prefix = YELLOW + "  ❯ " + RESET
    if prefill_value:
        print(prefix + prompt)
        print(DIM + f"    Pre-filled: {prefill_value[:120]}{'...' if len(prefill_value) > 120 else ''}" + RESET)
        if multiline:
            print(DIM + "    Press Enter to accept, or type replacement (blank line to finish):" + RESET)
            override_lines = []
            first = input("    ").strip()
            if first == "":
                return prefill_value
            override_lines.append(first)
            while True:
                line = input("    ")
                if line == "" and override_lines:
                    break
                override_lines.append(line)
            return "\n".join(override_lines).strip() or prefill_value
        else:
            override = input(DIM + "    Press Enter to accept, or type replacement: " + RESET).strip()
            return override if override else prefill_value
    else:
        return ask(prompt, required=required, multiline=multiline)


RED    = "\033[91m"
YELLOW = "\033[93m"
GREEN  = "\033[92m"
BLUE   = "\033[94m"
BOLD   = "\033[1m"
DIM    = "\033[2m"
RESET  = "\033[0m"

def hr(char="─", width=70):
    print(DIM + char * width + RESET)

def header(text):
    print()
    hr("═")
    print(BOLD + f"  {text}" + RESET)
    hr("═")
    print()

def section(text):
    print()
    hr()
    print(BOLD + BLUE + f"  {text}" + RESET)
    hr()
    print()

def ask(prompt, required=True, multiline=False):
    prefix = YELLOW + "  ❯ " + RESET
    if multiline:
        print(prefix + prompt)
        print(DIM + "    (Enter a blank line when done)" + RESET)
        lines = []
        while True:
            line = input("    ")
            if line == "" and lines:
                break
            lines.append(line)
        return "\n".join(lines).strip()
    else:
        while True:
            answer = input(prefix + prompt + " ").strip()
            if answer or not required:
                return answer
            print(DIM + "    (Required — please answer to continue)" + RESET)

def choose(prompt, options, allow_multi=False):
    print(YELLOW + "  ❯ " + RESET + prompt)
    for i, opt in enumerate(options, 1):
        print(f"    {BOLD}{i}{RESET}. {opt}")
    print()
    if allow_multi:
        raw = input("    Enter numbers separated by commas (e.g. 1,3): ").strip()
        selected = []
        for part in raw.split(","):
            part = part.strip()
            if part.isdigit() and 1 <= int(part) <= len(options):
                selected.append(options[int(part) - 1])
        return selected if selected else [options[0]]
    else:
        while True:
            raw = input("    Enter number: ").strip()
            if raw.isdigit() and 1 <= int(raw) <= len(options):
                return options[int(raw) - 1]
            print(DIM + "    Please enter a valid number." + RESET)

def verdict_color(v):
    colors = {
        "BUILD": GREEN,
        "VALIDATE FIRST": YELLOW,
        "DE-SCOPE": YELLOW,
        "REFRAME": BLUE,
        "KILL": RED,
    }
    return colors.get(v, RESET) + BOLD + v + RESET


def scan_project(root="."):
    root = Path(root)
    summary = {
        "has_project": False,
        "name": None,
        "description": None,
        "tech_stack": [],
        "structure": [],
        "recent_commits": [],
        "existing_judgment": None,
        "spec_files": [],
        "age_estimate": None,
        "lines_of_code": 0,
    }

    for readme in ["README.md", "README.txt", "README"]:
        p = root / readme
        if p.exists():
            summary["has_project"] = True
            content = p.read_text(errors="ignore")
            lines = content.split("\n")
            for line in lines:
                if line.startswith("# "):
                    summary["name"] = line[2:].strip()
                    break
            desc_lines = []
            in_desc = False
            for line in lines:
                if line.startswith("# ") and not in_desc:
                    in_desc = True
                    continue
                if in_desc:
                    if line.startswith("#"):
                        break
                    if line.strip():
                        desc_lines.append(line.strip())
                    elif desc_lines:
                        break
            summary["description"] = " ".join(desc_lines[:3]) if desc_lines else None
            break

    tech_indicators = {
        "package.json": "Node.js/JavaScript",
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        "Cargo.toml": "Rust",
        "go.mod": "Go",
        "pom.xml": "Java/Maven",
        "build.gradle": "Java/Gradle",
        "Gemfile": "Ruby",
        "composer.json": "PHP",
        "pubspec.yaml": "Flutter/Dart",
    }
    for file, tech in tech_indicators.items():
        if (root / file).exists():
            summary["tech_stack"].append(tech)
            summary["has_project"] = True

    judgment_path = root / "JUDGMENT.md"
    if judgment_path.exists():
        summary["existing_judgment"] = judgment_path.read_text(errors="ignore")

    spec_patterns = ["PRD", "SPEC", "DESIGN", "RFC", "ADR", "REQUIREMENTS"]
    for f in root.rglob("*.md"):
        if any(p in f.stem.upper() for p in spec_patterns):
            summary["spec_files"].append(str(f.relative_to(root)))

    try:
        dirs = [d.name for d in root.iterdir()
                if d.is_dir() and not d.name.startswith(".") and d.name not in
                {"node_modules", "__pycache__", ".git", "venv", ".venv", "dist", "build"}]
        files = [f.name for f in root.iterdir()
                 if f.is_file() and not f.name.startswith(".")]
        summary["structure"] = sorted(dirs)[:10] + sorted(files)[:10]
    except Exception:
        pass

    try:
        log = subprocess.check_output(
            ["git", "log", "--oneline", "-10"],
            cwd=root, stderr=subprocess.DEVNULL
        ).decode().strip().split("\n")
        summary["recent_commits"] = [l for l in log if l]

        first = subprocess.check_output(
            ["git", "log", "--oneline", "--reverse", "-1", "--format=%ar"],
            cwd=root, stderr=subprocess.DEVNULL
        ).decode().strip()
        summary["age_estimate"] = first if first else None
    except Exception:
        pass

    loc = 0
    code_exts = {".py", ".js", ".ts", ".tsx", ".jsx", ".go", ".rs", ".java",
                 ".kt", ".swift", ".rb", ".php", ".cs", ".cpp", ".c"}
    try:
        for f in root.rglob("*"):
            if (f.suffix in code_exts and
                    ".git" not in str(f) and
                    "node_modules" not in str(f) and
                    "__pycache__" not in str(f)):
                try:
                    loc += len(f.read_text(errors="ignore").splitlines())
                except Exception:
                    pass
        summary["lines_of_code"] = loc
    except Exception:
        pass

    return summary

def print_scan_summary(scan):
    section("📂 Project Scan Results")
    if not scan["has_project"]:
        print(DIM + "  No project detected in current directory. Proceeding with blank slate review." + RESET)
        return

    if scan["name"]:
        print(f"  {BOLD}Project:{RESET} {scan['name']}")
    if scan["description"]:
        print(f"  {BOLD}Description:{RESET} {scan['description'][:200]}")
    if scan["tech_stack"]:
        print(f"  {BOLD}Tech Stack:{RESET} {', '.join(scan['tech_stack'])}")
    if scan["age_estimate"]:
        print(f"  {BOLD}Started:{RESET} {scan['age_estimate']}")
    if scan["lines_of_code"]:
        print(f"  {BOLD}Lines of Code:{RESET} {scan['lines_of_code']:,}")
    if scan["recent_commits"]:
        print(f"\n  {BOLD}Recent Commits:{RESET}")
        for c in scan["recent_commits"][:5]:
            print(f"    {DIM}{c}{RESET}")
    if scan["spec_files"]:
        print(f"\n  {BOLD}Spec Files Found:{RESET} {', '.join(scan['spec_files'])}")
    if scan["existing_judgment"]:
        print(f"\n  {YELLOW}⚠  JUDGMENT.md already exists in this project.{RESET}")
        print(f"  {DIM}This review will overwrite it.{RESET}")
    print()

EVIDENCE_LEVELS = [
    "L0 — Pure internal opinion (领导觉得 / 团队感觉)",
    "L1 — User verbal feedback (访谈说想要 / 销售转述)",
    "L2 — Small-sample behavioral observation (可用性测试 / 小范围内测)",
    "L3 — Real behavioral data (DAU / 转化率 / AB测试)",
    "L4 — Payment / commercial validation (付费 / 续费 / 真实流失)",
]

EVIDENCE_SHORT = ["L0", "L1", "L2", "L3", "L4"]

DISEASES = [
    "竞品焦虑症 — Driven by competitor moves, not user need",
    "技术炫技症 — Capability-push looking for demand",
    "老板幻觉症 — Authority masquerading as user insight",
    "Demo成瘾症 — Optimized for demo, not daily use",
    "替换成本失明 — Overestimates gains, ignores migration friction",
    "商业闭环断裂 — User value exists, business capture doesn't",
    "低频刚需误判 — Real pain, but occurs too rarely to matter",
    "万能入口症 — One feature trying to serve every context",
    "指标幻觉症 — Metric improved, user value unclear",
    "场景错配症 — Valid elsewhere, wrong context here",
    "None of the above / Multiple / Not sure",
]

def run_interview(scan=None, prefill=None):
    prefill = prefill or {}
    data = {}

    _ask = lambda prompt, key, req=True, ml=False: ask_with_prefill(
        prompt, prefill.get(key, ""), required=req, multiline=ml
    ) if prefill else ask(prompt, required=req, multiline=ml)

    section("📋 Stage 1: What Are We Judging?")
    print("  Describe the demand in plain language.")
    print(DIM + "  Don't write a PRD. Just explain what you want to build and why.\n" + RESET)

    data["demand_raw"] = _ask("Demand / 需求描述:", "demand_raw", ml=True)

    print()
    if prefill.get("demand_source"):
        print(DIM + f"  Demand source detected: {prefill['demand_source']}" + RESET)
        override = input(YELLOW + "  ❯ " + RESET + "Press Enter to accept, or type to override: ").strip()
        data["demand_source"] = override if override else prefill["demand_source"]
    else:
        data["demand_source"] = choose(
            "Where did this demand come from? / 需求从哪里来的？",
            [
                "User research / 用户研究",
                "User complaints / 用户投诉",
                "Sales feedback / 销售反馈",
                "CEO / leadership / 老板/领导",
                "Competitor launched something / 竞品上线了",
                "Team brainstorm / 团队内部讨论",
                "Technical capability available / 技术能力驱动",
                "Personal intuition / 个人直觉",
            ]
        )

    section("📋 Stage 2: Who Is the User?")
    print(DIM + '  "用户不是自然人，而是需求的集合" — 俞军\n' + RESET)

    data["target_user"] = _ask(
        "Who specifically is the user? (Not '用户'. A specific person in a specific moment.)",
        "target_user"
    )
    data["trigger_context"] = _ask(
        "What exact situation triggers this need? When / where / why?",
        "trigger_context"
    )
    data["user_frequency"] = choose(
        "How often does this situation occur? / 触发频率？",
        ["Multiple times daily", "Daily", "Weekly", "Monthly", "A few times a year", "Rarely / edge case"]
    )

    section("📋 Stage 3: Old vs New Experience")
    print(DIM + "  用户价值 = 新体验 - 旧体验 - 替换成本\n" + RESET)

    data["old_experience"] = _ask(
        "What do users do TODAY without your product? Be specific.",
        "old_experience"
    )
    data["new_experience"] = _ask(
        "What does your product do better? Be specific — not 'more convenient'.",
        "new_experience"
    )
    data["replacement_cost"] = _ask(
        "What does it take for a user to switch? Learning? Migration? Trust? Org buy-in?",
        "replacement_cost"
    )

    section("📋 Stage 4: Assumptions")

    prefill_assumptions = prefill.get("assumptions", [])
    if prefill_assumptions:
        print(f"  {GREEN}Pre-filled assumptions from document:{RESET}")
        for i, a in enumerate(prefill_assumptions, 1):
            print(f"    {i}. {DIM}{a}{RESET}")
        print()
        keep = input(YELLOW + "  ❯ " + RESET + "Press Enter to use these, or type 'edit' to modify: ").strip()
        if keep.lower() == "edit":
            prefill_assumptions = []

    assumptions = list(prefill_assumptions)
    if not prefill_assumptions:
        print("  List the key assumptions your demand requires to be true.")
        print(DIM + "  (e.g. 'Users check this dashboard daily', 'AI output quality is trusted')\n" + RESET)
        print(YELLOW + "  ❯ " + RESET + "Enter assumptions one by one. Blank line to finish.")
        i = len(assumptions) + 1
        while True:
            a = input(f"    Assumption {i}: ").strip()
            if not a:
                break
            assumptions.append(a)
            i += 1

    data["assumptions"] = assumptions

    if assumptions:
        print()
        data["evidence_level"] = choose(
            "What's the strongest evidence you have for these assumptions?",
            EVIDENCE_LEVELS
        )

    section("📋 Stage 5: Business Model")

    data["business_value"] = _ask(
        "How does the company capture value from this? Revenue / retention / acquisition / strategic?",
        "business_value"
    )
    data["resource_ask"] = choose(
        "What level of resource commitment does this require?",
        ["Small (days / 1 person)", "Medium (weeks / small team)", "Large (months / full team)", "Very large (quarters / multiple teams)"]
    )

    section("📋 Stage 6: Self-Assessment")

    data["self_verdict"] = choose(
        "Before I give my verdict — what do YOU think?",
        ["BUILD — confident this is right", "VALIDATE FIRST — some uncertainty", "DE-SCOPE — scope is too big", "REFRAME — not sure about the approach", "KILL — might be wrong direction"]
    )

    data["strongest_concern"] = ask("What's your biggest worry about this demand?", required=False)

    return data


def compute_verdict(data):
    judgment = {}

    ev_raw = data.get("evidence_level", "L0")
    ev_level = 0
    for i, s in enumerate(EVIDENCE_SHORT):
        if s in ev_raw:
            ev_level = i
            break
    judgment["evidence_level"] = ev_raw
    judgment["evidence_level_int"] = ev_level

    resource_raw = data.get("resource_ask", "")
    resource_level = 0
    if "Medium" in resource_raw: resource_level = 1
    if "Large" in resource_raw and "Very" not in resource_raw: resource_level = 2
    if "Very large" in resource_raw: resource_level = 3
    judgment["resource_level"] = resource_level

    evidence_resource_gap = resource_level - ev_level
    judgment["evidence_resource_gap"] = evidence_resource_gap

    risky_sources = ["CEO", "Competitor", "Team brainstorm", "Technical capability", "Personal intuition"]
    source_risky = any(r in data.get("demand_source", "") for r in risky_sources)
    judgment["source_risky"] = source_risky

    low_freq = data.get("user_frequency", "") in ["Monthly", "A few times a year", "Rarely / edge case"]
    judgment["low_frequency"] = low_freq

    assumption_count = len(data.get("assumptions", []))
    judgment["assumption_count"] = assumption_count
    unverified_risk = assumption_count >= 3 and ev_level <= 1
    judgment["unverified_risk"] = unverified_risk

    if evidence_resource_gap >= 3 or (source_risky and ev_level == 0 and resource_level >= 2):
        verdict = "KILL"
    elif unverified_risk or (evidence_resource_gap >= 2):
        verdict = "VALIDATE FIRST"
    elif low_freq and ev_level <= 1:
        verdict = "REFRAME"
    elif evidence_resource_gap >= 1 or assumption_count >= 2:
        verdict = "VALIDATE FIRST"
    else:
        verdict = "BUILD"

    if data.get("self_verdict", "").startswith("KILL") and ev_level <= 1:
        verdict = "KILL"

    judgment["verdict"] = verdict
    return judgment

def select_diseases(data):
    section("⚡ Strike 1: Name the Disease / 命名病灶")
    print("  Based on what you've told me, which of these patterns best describe this demand?")
    print(DIM + "  (Select all that apply)\n" + RESET)
    selected = choose("Select disease type(s) / 选择病型:", DISEASES, allow_multi=True)
    return [d for d in selected if "None" not in d]


def generate_failure_forecast(data, verdict):
    resource = data.get("resource_ask", "Medium")
    freq = data.get("user_frequency", "Weekly")
    source = data.get("demand_source", "Internal")

    if verdict == "BUILD":
        return "Based on the evidence provided, the demand appears solid. Key risk: maintain scope discipline during development — feature creep is the most common way a validated demand becomes an unvalidated product."

    if "Rarely" in freq or "edge case" in freq:
        timeline = [
            "Month 1: Development proceeds, team is excited about the capability.",
            "Month 2-3: Feature ships. Initial users try it out of curiosity.",
            "Month 4: Usage data shows the triggering scenario is rarer than expected. Team starts discussing 'awareness' as the problem.",
            "Month 5-6: Roadmap additions proposed to 'increase use cases'. Complexity grows, core trigger frequency hasn't changed.",
            "Root cause: The triggering scenario was never frequent enough to build a product around."
        ]
    elif "CEO" in source or "leadership" in source:
        timeline = [
            "Month 1: High-priority label. Resources allocated quickly.",
            "Month 2: Launch with internal fanfare. Leadership is pleased.",
            "Month 3-4: Real usage data arrives. Engagement is lower than expected.",
            "Month 5: Team is caught between data (low usage) and authority (leadership still believes in it).",
            "Month 6: Feature maintained to avoid awkward conversations, not because it creates value.",
            "Root cause: The demand was validated by authority, not by users."
        ]
    elif "Competitor" in source:
        timeline = [
            "Month 1: Fast-tracked to close perceived gap with competitor.",
            "Month 2: Shipped. PR coverage notes you now have feature parity.",
            "Month 3: Data shows your users don't use it the same way competitor users do — different user base, different context.",
            "Month 4-5: Team debates 'polishing' vs 'moving on'. Feature stays in a half-maintained state.",
            "Root cause: Competitor's context was different. Their validation doesn't transfer."
        ]
    else:
        timeline = [
            "Month 1: Development begins with good intentions.",
            "Month 2-3: Feature ships. Some initial usage.",
            "Month 4: Usage drops. Team discusses adding more features to drive engagement.",
            "Month 5-6: Complexity has grown, but the core unverified assumption still hasn't been tested.",
            "Root cause: The critical assumption was never validated before significant resources were committed."
        ]

    return "\n".join(f"    {line}" for line in timeline)


def write_judgment_md(data, judgment, diseases, failure_forecast, output_path):
    verdict = judgment["verdict"]
    ev = judgment["evidence_level"]
    resource_labels = ["Small (days)", "Medium (weeks)", "Large (months)", "Very large (quarters)"]
    resource_label = resource_labels[min(judgment["resource_level"], 3)]

    verdict_zh = {
        "BUILD": "立项 / BUILD",
        "VALIDATE FIRST": "先验证 / VALIDATE FIRST",
        "DE-SCOPE": "降级做 / DE-SCOPE",
        "REFRAME": "重新定义 / REFRAME",
        "KILL": "终止 / KILL",
    }.get(verdict, verdict)

    gap = judgment["evidence_resource_gap"]
    gap_warning = ""
    if gap >= 2:
        ev_short = ev.split("—")[0].strip()
        gap_warning = f"\n> ⚠️  **证据-资源失配**：你在用 **{resource_label}** 的资源押注 **{ev_short}** 级别的假设。这不是产品判断，是组织赌博。\n"

    diseases_section = "\n".join(f"- {d}" for d in diseases) if diseases else "- No dominant pattern identified"
    assumptions = data.get("assumptions", [])
    assumption_list = "\n".join(f"{i+1}. {a}" for i, a in enumerate(assumptions)) if assumptions else "No assumptions explicitly listed."
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    content = f"""# JUDGMENT.md
> Generated by Product Judgment Skill — demand-check.py
> {now}
> **This document should be committed to git. It is the record of why this demand was (or wasn't) built.**

---

## ⚖️ Verdict / 判决

### **{verdict_zh}**
{gap_warning}
| 维度 | 值 |
|------|-----|
| 证据等级 Evidence Level | {ev} |
| 资源投入 Resource Commitment | {resource_label} |
| 需求来源 Demand Source | {data.get('demand_source', 'Unknown')} |
| 触发频率 Trigger Frequency | {data.get('user_frequency', 'Unknown')} |

---

## 📋 Demand Summary / 需求描述

{data.get('demand_raw', '(not provided)')}

**Target User / 目标用户：** {data.get('target_user', '(not specified)')}

**Trigger Context / 触发场景：** {data.get('trigger_context', '(not specified)')}

---

## ⚡ Strike 1: Disease Diagnosis / 病灶命名

{diseases_section}

---

## 🔍 Strike 2: Assumption Interrogation / 假设审讯

### 用户价值公式 / User Value Equation

| 维度 | 内容 |
|------|------|
| 旧体验 Old Experience | {data.get('old_experience', '(not specified)')} |
| 新体验 New Experience | {data.get('new_experience', '(not specified)')} |
| 替换成本 Replacement Cost | {data.get('replacement_cost', '(not specified)')} |

### 需求成立的关键假设 / Critical Assumptions

This demand requires ALL of the following to be true:

{assumption_list}

**Strongest evidence on hand / 当前最强证据：** {ev}

---

## 💀 Strike 3: Failure Forecast / 失败预演

If this proceeds without validating the critical assumptions:

{failure_forecast}

---

## 💼 Business Model / 商业模式

**Value Capture / 价值捕获：** {data.get('business_value', '(not specified)')}

---

## ✅ Recommendation / 建议

"""

    if verdict == "BUILD":
        content += """**Go ahead. Write the PRD.**

Before you do:
- Document which assumptions are verified and how
- Define success metrics upfront
- Set a 60-day checkpoint to validate assumptions are holding
"""
    elif verdict == "VALIDATE FIRST":
        content += f"""**Do NOT write the full PRD yet.**

First, validate your critical assumptions with the lowest-cost experiment possible.

Suggested validation approach:
- Pick the 1-2 most critical unverified assumptions above
- Design a test that doesn't require building the full product
- Define a clear success/failure threshold before running the test
- Return to this judgment after validation

Current evidence: {ev}
Evidence needed before proceeding: L2 minimum (small-sample behavioral observation)
"""
    elif verdict == "DE-SCOPE":
        content += """**The core demand may be valid, but the scope is too large.**

Before writing the PRD:
- Identify the single most valuable scenario
- Strip everything that doesn't serve that scenario
- Treat the reduced scope as a validation of the core assumption
- Only expand after the core is validated
"""
    elif verdict == "REFRAME":
        content += """**The demand describes the wrong solution to a potentially real problem.**

Before writing the PRD:
- Step back from the solution you've described
- Define the underlying user problem in situation/trigger/outcome terms
- Explore alternative solutions that might have lower replacement cost
- Return with a reframed demand statement
"""
    elif verdict == "KILL":
        content += f"""**Do not proceed. This demand should not be built.**

This is not a negative judgment on the team or the idea. It is a judgment on the current state of evidence and the risk profile of the commitment.

The primary reasons:
- Evidence level ({ev}) is insufficient for the resource commitment ({resource_label})
- The demand pattern suggests this is driven by internal pressure, not validated user need

If you believe this judgment is wrong, return with new evidence (L2 or higher) that validates the critical assumptions. Do not return with stakeholder support or deadline pressure — those are not evidence.
"""

    content += """
---

## 🔄 How to Change This Verdict

**Only new evidence changes this verdict.**

The following do NOT change this verdict:
- Leadership pressure
- Competitor launching something
- Sunk cost ("we already built X")
- Deadline pressure
- "Users said they wanted it" (verbal ≠ behavioral)

The following WILL change this verdict:
- L2+ behavioral evidence on the critical assumptions
- A validated MVP result
- Real usage data from a lower-cost experiment

---

*Brutal to the logic. Respectful to the person.*
*Product Judgment Skill — github.com/Longfellow1/Yujun-skill*
"""

    Path(output_path).write_text(content, encoding="utf-8")
    return output_path


def run_scope_check(judgment_path="JUDGMENT.md"):
    header("🔍 Scope Check / 范围审查")

    p = Path(judgment_path)
    if not p.exists():
        print(RED + f"  No JUDGMENT.md found at {judgment_path}" + RESET)
        print(DIM + "  Run `python demand-check.py` first to create one." + RESET)
        sys.exit(1)

    existing = p.read_text()
    print(f"  Found existing JUDGMENT.md ({len(existing.split(chr(10)))} lines)")
    print()

    feature = ask("What feature or scope addition are you considering? / 你想加什么功能？", multiline=True)
    reason = ask("Why do you want to add this? / 为什么要加？")
    source = ask("Who is asking for this? / 谁提出来的？")

    print()
    print(BOLD + "  Checking against original judgment..." + RESET)
    print()

    warnings = []

    if any(word in reason.lower() for word in ["user asked", "user said", "sales said", "leader", "ceo", "boss"]):
        warnings.append("⚠  This addition is driven by the same pattern we already reviewed. Verbal requests ≠ validated need.")

    if any(word in source.lower() for word in ["ceo", "boss", "vp", "leader", "管理", "老板"]):
        warnings.append("⚠  Authority pressure. Check: does this addition change the evidence level, or just the organizational pressure?")

    if warnings:
        for w in warnings:
            print(RED + f"  {w}" + RESET)
        print()

    print(BOLD + "  Core question:" + RESET)
    print(f"  Does '{feature[:80]}...' serve the same user, in the same context, with the same trigger,")
    print(f"  as the demand described in JUDGMENT.md?")
    print()

    aligned = choose("Is this addition aligned with the original validated demand?",
                     ["Yes — same user, same context, extends the core value",
                      "Partially — related but serves different users or contexts",
                      "No — this is a different demand dressed as a feature addition"])

    print()
    if "Yes" in aligned:
        print(GREEN + "  ✓ Scope addition appears aligned. Proceed, but document why in a PR." + RESET)
    elif "Partially" in aligned:
        print(YELLOW + "  △ Partial alignment. Consider whether this should be a separate demand review." + RESET)
        print(DIM + "  Run `python demand-check.py` with the new demand as a standalone review." + RESET)
    else:
        print(RED + "  ✗ This is scope creep. This is a new demand, not a feature addition." + RESET)
        print(DIM + "  Run `python demand-check.py` as a separate review for this demand." + RESET)
        print(DIM + "  Do not add it to the current project without its own JUDGMENT.md." + RESET)

    print()


def main():
    args = sys.argv[1:]
    scan_mode    = "--scan"   in args
    scope_mode   = "--scope"  in args
    json_mode    = "--json"   in args
    strict_mode  = "--strict" in args
    output_path  = "JUDGMENT.md"
    from_file    = None
    feature_text = None

    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 < len(args):
            output_path = args[idx + 1]

    if "--from" in args:
        idx = args.index("--from")
        if idx + 1 < len(args):
            from_file = args[idx + 1]

    if "--feature" in args:
        idx = args.index("--feature")
        if idx + 1 < len(args):
            feature_text = args[idx + 1]

    if scope_mode:
        run_scope_check()
        return

    if strict_mode and (from_file or feature_text):
        prefill = {}
        if from_file:
            prefill = parse_from_file(from_file)
        if feature_text:
            prefill["demand_raw"] = feature_text
        data = run_interview(prefill=prefill)
        diseases = select_diseases(data)
        judgment = compute_verdict(data)
        v = judgment["verdict"]
        ev = judgment["evidence_level"].split("—")[0].strip()
        print(f"\nVerdict: {verdict_color(v)}  |  Evidence: {ev}\n")
        return

    header("⚖️  Product Judgment / 产品需求审判")
    print(DIM + "  Before writing the PRD, decide whether the demand deserves to exist." + RESET)
    print(DIM + "  别急着写PRD，先判断这个需求配不配存在。\n" + RESET)
    print(DIM + "  Brutal to the logic. Respectful to the person." + RESET)
    print()

    prefill = {}
    if from_file:
        prefill = parse_from_file(from_file)
        show_prefill_summary(prefill)
    if feature_text:
        prefill["demand_raw"] = feature_text
        print(DIM + f"  Feature: {feature_text}" + RESET)
        print()

    scan = None
    if scan_mode:
        print(BLUE + "  Scanning project..." + RESET)
        scan = scan_project(".")
        print_scan_summary(scan)

        if scan["existing_judgment"]:
            cont = choose("A JUDGMENT.md already exists. Overwrite?",
                          ["Yes, run a new review", "No, exit"])
            if "No" in cont:
                print(DIM + "\n  Exiting. Existing JUDGMENT.md preserved." + RESET)
                return

    data = run_interview(scan=scan, prefill=prefill)
    diseases = select_diseases(data)
    judgment = compute_verdict(data)

    section("💀 Strike 3: Failure Forecast / 失败预演")
    failure_forecast = generate_failure_forecast(data, judgment["verdict"])
    print(failure_forecast)
    print()

    section("⚖️  Final Verdict / 最终判决")
    v = judgment["verdict"]
    print(f"  {verdict_color(v)}")
    print()

    gap = judgment["evidence_resource_gap"]
    if gap >= 2:
        ev_short = judgment["evidence_level"].split("—")[0].strip()
        resource_labels = ["Small", "Medium", "Large (months)", "Very large (quarters)"]
        rl = resource_labels[min(judgment["resource_level"], 3)]
        print(RED + f"  ⚠  Evidence-Resource Mismatch: {ev_short} evidence → {rl} resource commitment." + RESET)
        print(RED + "     This is organizational gambling, not product judgment." + RESET)
        print()

    failure_forecast = generate_failure_forecast(data, judgment["verdict"])
    out = write_judgment_md(data, judgment, diseases, failure_forecast, output_path)
    print(GREEN + f"  ✓ JUDGMENT.md written to: {out}" + RESET)

    if json_mode:
        json_path = output_path.replace(".md", ".json")
        json_data = {
            "verdict": v,
            "evidence_level": judgment["evidence_level"].split("—")[0].strip(),
            "evidence_level_int": judgment["evidence_level_int"],
            "resource_level": judgment["resource_level"],
            "evidence_resource_gap": judgment["evidence_resource_gap"],
            "diseases": diseases,
            "assumption_count": judgment["assumption_count"],
            "demand_source": data.get("demand_source", ""),
            "user_frequency": data.get("user_frequency", ""),
            "demand_raw": data.get("demand_raw", ""),
            "assumptions": data.get("assumptions", []),
            "generated_at": datetime.now().isoformat(),
        }
        Path(json_path).write_text(json.dumps(json_data, ensure_ascii=False, indent=2))
        print(GREEN + f"  ✓ JUDGMENT.json written to: {json_path}" + RESET)

    print()
    print(DIM + "  Next steps:" + RESET)
    if v == "BUILD":
        print(DIM + "  → Write the PRD. Commit JUDGMENT.md alongside it." + RESET)
    elif v in ("VALIDATE FIRST", "DE-SCOPE"):
        print(DIM + "  → Design your validation experiment. Don't write the full PRD yet." + RESET)
        print(DIM + "  → Re-run after you have L2+ evidence." + RESET)
    elif v == "REFRAME":
        print(DIM + "  → Step back from the solution. Redefine the problem." + RESET)
        print(DIM + "  → Re-run with the reframed demand." + RESET)
    elif v == "KILL":
        print(DIM + "  → Stop. Redirect resources to validated demands." + RESET)
        print(DIM + "  → If you disagree, return with L2+ behavioral evidence." + RESET)
    print()
    print(DIM + "  git add JUDGMENT.md && git commit -m 'chore: add demand judgment'" + RESET)
    print()

if __name__ == "__main__":
    main()
