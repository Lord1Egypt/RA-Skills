#!/usr/bin/env python3
"""
Prompt Library Manager — Store, search, version, and reuse prompt templates.

Usage:
    python3 prompt-library.py add --name "email-summarizer" --category productivity --template "..."
    python3 prompt-library.py search "email"
    python3 prompt-library.py list [--category CAT] [--format text|json|markdown]
    python3 prompt-library.py use "email-summarizer" --var input="text here"
    python3 prompt-library.py update --name "email-summarizer" --template "new template"
    python3 prompt-library.py delete --name "email-summarizer"
    python3 prompt-library.py export --format json [--output prompts.json]
    python3 prompt-library.py import --file prompts.json
    python3 prompt-library.py stats

Built by GetAgentIQ — https://getagentiq.ai
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path

DEFAULT_WORKSPACE = os.path.expanduser("~/.openclaw/workspace")
LIBRARY_FILE = "memory/prompt-library.json"

# ═══════════════════════════════════════════════════════════════════════
# Built-in Starter Prompts
# ═══════════════════════════════════════════════════════════════════════

STARTER_PROMPTS = [
    {
        "name": "email-summarizer",
        "category": "productivity",
        "description": "Summarize email threads with decisions and action items",
        "template": "Summarize the following email thread. Highlight:\n1. Key decisions made\n2. Action items (with owners if mentioned)\n3. Deadlines or dates\n4. Open questions\n\nEmail thread:\n{input}",
        "tags": ["email", "summary", "productivity"],
    },
    {
        "name": "code-reviewer",
        "category": "coding",
        "description": "Review code for bugs, improvements, and best practices",
        "template": "Review the following {language} code. Check for:\n1. Bugs or logic errors\n2. Security vulnerabilities\n3. Performance issues\n4. Code style and readability\n5. Suggestions for improvement\n\nCode:\n```{language}\n{code}\n```",
        "tags": ["code", "review", "quality"],
    },
    {
        "name": "meeting-notes",
        "category": "productivity",
        "description": "Structure meeting transcripts into organized notes",
        "template": "Convert this meeting transcript into structured notes:\n\n**Meeting:** {title}\n**Date:** {date}\n\nTranscript:\n{transcript}\n\nOutput format:\n- Attendees\n- Key Discussion Points\n- Decisions Made\n- Action Items (owner + deadline)\n- Next Steps",
        "tags": ["meeting", "notes", "summary"],
    },
    {
        "name": "bug-report",
        "category": "coding",
        "description": "Generate structured bug reports from descriptions",
        "template": "Create a structured bug report from this description:\n\n{description}\n\nFormat:\n- **Title:** (concise summary)\n- **Severity:** (critical/high/medium/low)\n- **Steps to Reproduce:**\n- **Expected Behavior:**\n- **Actual Behavior:**\n- **Environment:**\n- **Possible Root Cause:**\n- **Suggested Fix:**",
        "tags": ["bug", "report", "coding"],
    },
    {
        "name": "content-writer",
        "category": "writing",
        "description": "Write blog posts from outlines",
        "template": "Write a {length}-word blog post about: {topic}\n\nTone: {tone}\nAudience: {audience}\n\nOutline:\n{outline}\n\nRequirements:\n- Engaging hook in the first paragraph\n- Use headers and subheaders\n- Include actionable takeaways\n- End with a strong conclusion and CTA",
        "tags": ["blog", "writing", "content"],
    },
    {
        "name": "data-analyst",
        "category": "analysis",
        "description": "Analyze datasets and find patterns",
        "template": "Analyze the following data and provide insights:\n\nData:\n{data}\n\nQuestions to answer:\n1. What are the key trends?\n2. Are there any anomalies or outliers?\n3. What patterns emerge?\n4. What recommendations would you make based on this data?\n\nProvide your analysis with specific numbers and percentages.",
        "tags": ["data", "analysis", "insights"],
    },
    {
        "name": "task-breakdown",
        "category": "productivity",
        "description": "Break complex tasks into manageable subtasks",
        "template": "Break down this task into actionable subtasks:\n\nTask: {task}\nDeadline: {deadline}\nResources: {resources}\n\nFor each subtask provide:\n- Description\n- Estimated time\n- Dependencies\n- Priority (high/medium/low)\n\nOrder by recommended execution sequence.",
        "tags": ["planning", "tasks", "project"],
    },
    {
        "name": "explain-concept",
        "category": "education",
        "description": "Explain technical concepts at adjustable complexity levels",
        "template": "Explain {concept} at a {level} level.\n\nInclude:\n- Simple definition\n- How it works (with analogy)\n- Real-world example\n- Common misconceptions\n- When/why it matters\n\nLevel guide: beginner=no jargon, intermediate=some technical terms, expert=full depth",
        "tags": ["explain", "education", "technical"],
    },
    {
        "name": "decision-matrix",
        "category": "analysis",
        "description": "Compare options with weighted pros and cons",
        "template": "Create a decision matrix for choosing between these options:\n\nOptions: {options}\nCriteria: {criteria}\n\nFor each option:\n1. Score each criterion (1-10)\n2. List pros and cons\n3. Risk assessment\n4. Overall recommendation with reasoning\n\nContext: {context}",
        "tags": ["decision", "comparison", "analysis"],
    },
    {
        "name": "daily-standup",
        "category": "productivity",
        "description": "Generate standup update from recent work",
        "template": "Generate a daily standup update based on:\n\nYesterday's work:\n{yesterday}\n\nToday's plan:\n{today}\n\nFormat:\n🔵 **Done Yesterday:**\n- (bullet points)\n\n🟢 **Doing Today:**\n- (bullet points)\n\n🔴 **Blockers:**\n- {blockers}",
        "tags": ["standup", "daily", "update"],
    },
]


# ═══════════════════════════════════════════════════════════════════════
# Library Management
# ═══════════════════════════════════════════════════════════════════════

def get_library_path(workspace):
    ws = Path(workspace or DEFAULT_WORKSPACE).expanduser().resolve()
    return ws / LIBRARY_FILE


def load_library(lib_path):
    """Load prompt library from disk."""
    if lib_path.exists():
        try:
            with open(lib_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return []
    return []


def save_library(lib_path, prompts):
    """Save prompt library to disk."""
    lib_path.parent.mkdir(parents=True, exist_ok=True)
    with open(lib_path, "w") as f:
        json.dump(prompts, f, indent=2)


def init_library(lib_path):
    """Initialize library with starter prompts if empty."""
    prompts = load_library(lib_path)
    if not prompts:
        now = datetime.utcnow().isoformat() + "Z"
        for sp in STARTER_PROMPTS:
            sp["version"] = 1
            sp["created"] = now
            sp["updated"] = now
            sp["use_count"] = 0
            sp["model"] = None
        save_library(lib_path, STARTER_PROMPTS)
        return STARTER_PROMPTS
    return prompts


# ═══════════════════════════════════════════════════════════════════════
# Commands
# ═══════════════════════════════════════════════════════════════════════

def cmd_add(lib_path, name, category, template, description=None, tags=None, model=None, from_file=None):
    """Add a new prompt template."""
    prompts = init_library(lib_path)

    # Check for duplicate
    if any(p["name"] == name for p in prompts):
        print(f"  ❌ Prompt '{name}' already exists. Use 'update' to modify.")
        return

    if from_file:
        try:
            template = Path(from_file).read_text()
        except FileNotFoundError:
            print(f"  ❌ File not found: {from_file}")
            return
        except OSError as e:
            print(f"  ❌ Cannot read file: {e}")
            return
        except UnicodeDecodeError as e:
            print(f"  ❌ Cannot decode file: {e}")
            return

    now = datetime.utcnow().isoformat() + "Z"
    prompt = {
        "name": name,
        "category": category or "general",
        "description": description or f"Prompt template: {name}",
        "template": template,
        "tags": tags.split(",") if tags else [],
        "model": model,
        "version": 1,
        "created": now,
        "updated": now,
        "use_count": 0,
    }
    prompts.append(prompt)
    save_library(lib_path, prompts)
    print(f"  ✅ Added prompt: {name} (category: {prompt['category']})")


def cmd_search(lib_path, query, category=None, tag=None, fmt="text"):
    """Search prompts by keyword."""
    prompts = init_library(lib_path)
    query_lower = query.lower()

    results = []
    for p in prompts:
        # Filter by category/tag first
        if category and p.get("category") != category:
            continue
        if tag and tag not in p.get("tags", []):
            continue

        # Search across fields
        searchable = f"{p['name']} {p.get('description', '')} {' '.join(p.get('tags', []))} {p.get('template', '')}"
        if query_lower in searchable.lower():
            results.append(p)

    if fmt == "json":
        print(json.dumps(results, indent=2))
    else:
        print(f"\n  🔍 Search: '{query}' — {len(results)} result(s)\n")
        for p in results:
            tags_str = ", ".join(p.get("tags", [])) if p.get("tags") else "none"
            print(f"  📝 {p['name']} [{p.get('category', 'general')}]")
            print(f"     {p.get('description', 'No description')}")
            print(f"     Tags: {tags_str}  |  Uses: {p.get('use_count', 0)}  |  v{p.get('version', 1)}")
            print()

    return results


def cmd_list(lib_path, category=None, fmt="text", compact=False):
    """List all prompts."""
    prompts = init_library(lib_path)

    if category:
        prompts = [p for p in prompts if p.get("category") == category]

    if fmt == "json":
        print(json.dumps(prompts, indent=2))
        return

    print(f"\n  📚 Prompt Library — {len(prompts)} prompt(s)\n")

    if compact:
        for p in prompts:
            print(f"  • {p['name']} [{p.get('category', 'general')}]")
    else:
        # Group by category
        categories = {}
        for p in prompts:
            cat = p.get("category", "general")
            categories.setdefault(cat, []).append(p)

        for cat, cat_prompts in sorted(categories.items()):
            print(f"  📂 {cat.upper()} ({len(cat_prompts)})")
            for p in cat_prompts:
                uses = p.get("use_count", 0)
                print(f"     • {p['name']:30s} v{p.get('version', 1)}  ({uses} uses)")
            print()


def cmd_use(lib_path, name, variables=None, fmt="text"):
    """Fill and output a prompt template."""
    prompts = init_library(lib_path)

    prompt = next((p for p in prompts if p["name"] == name), None)
    if not prompt:
        print(f"  ❌ Prompt '{name}' not found. Use 'list' to see available prompts.")
        return

    template = prompt["template"]

    # Fill variables
    if variables:
        for kv in variables:
            if "=" in kv:
                key, value = kv.split("=", 1)
                template = template.replace(f"{{{key}}}", value)

    # Find unfilled variables
    unfilled = re.findall(r'\{(\w+)\}', template)
    if unfilled:
        print(f"  ⚠️  Unfilled variables: {', '.join(unfilled)}")
        print(f"     Use --var {unfilled[0]}=\"value\" to fill them\n")

    # Increment use count
    prompt["use_count"] = prompt.get("use_count", 0) + 1
    save_library(lib_path, prompts)

    if fmt == "json":
        print(json.dumps({"name": name, "filled": template, "unfilled": unfilled}, indent=2))
    else:
        print(f"\n{'─' * 60}")
        print(f"  📝 {name} (v{prompt.get('version', 1)})")
        print(f"{'─' * 60}")
        print(template)
        print(f"{'─' * 60}\n")


def cmd_update(lib_path, name, template=None, tags=None, description=None):
    """Update an existing prompt."""
    prompts = init_library(lib_path)

    prompt = next((p for p in prompts if p["name"] == name), None)
    if not prompt:
        print(f"  ❌ Prompt '{name}' not found.")
        return

    if template:
        prompt["template"] = template
    if tags:
        prompt["tags"] = tags.split(",")
    if description:
        prompt["description"] = description

    prompt["version"] = prompt.get("version", 1) + 1
    prompt["updated"] = datetime.utcnow().isoformat() + "Z"

    save_library(lib_path, prompts)
    print(f"  ✅ Updated prompt: {name} → v{prompt['version']}")


def cmd_delete(lib_path, name, confirm=False):
    """Delete a prompt."""
    prompts = init_library(lib_path)
    original_count = len(prompts)
    prompts = [p for p in prompts if p["name"] != name]

    if len(prompts) == original_count:
        print(f"  ❌ Prompt '{name}' not found.")
        return

    save_library(lib_path, prompts)
    print(f"  🗑️  Deleted prompt: {name}")


def cmd_export(lib_path, fmt="json", output=None, category=None):
    """Export prompt library."""
    prompts = init_library(lib_path)

    if category:
        prompts = [p for p in prompts if p.get("category") == category]

    if fmt == "json":
        content = json.dumps(prompts, indent=2)
    elif fmt == "markdown":
        lines = ["# Prompt Library Export\n"]
        for p in prompts:
            lines.append(f"## {p['name']}\n")
            lines.append(f"**Category:** {p.get('category', 'general')}")
            lines.append(f"**Tags:** {', '.join(p.get('tags', []))}")
            lines.append(f"**Description:** {p.get('description', '')}\n")
            lines.append(f"```\n{p['template']}\n```\n")
        content = "\n".join(lines)
    else:
        content = json.dumps(prompts, indent=2)

    if output:
        with open(output, "w") as f:
            f.write(content)
        print(f"  📤 Exported {len(prompts)} prompts to {output}")
    else:
        print(content)


def cmd_import_prompts(lib_path, file_path, overwrite=False):
    """Import prompts from file."""
    prompts = init_library(lib_path)
    existing_names = {p["name"] for p in prompts}

    try:
        with open(file_path) as f:
            imported = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON in {file_path}: {e}")
        sys.exit(1)
    except OSError as e:
        print(f"ERROR: Could not read file {file_path}: {e}")
        sys.exit(1)

    added = 0
    updated = 0
    for ip in imported:
        if ip["name"] in existing_names:
            if overwrite:
                prompts = [p for p in prompts if p["name"] != ip["name"]]
                prompts.append(ip)
                updated += 1
            else:
                continue  # Skip existing
        else:
            prompts.append(ip)
            added += 1

    save_library(lib_path, prompts)
    print(f"  📥 Import complete: {added} added, {updated} updated, {len(prompts)} total")


def cmd_stats(lib_path):
    """Show library statistics."""
    prompts = init_library(lib_path)

    categories = {}
    total_uses = 0
    for p in prompts:
        cat = p.get("category", "general")
        categories[cat] = categories.get(cat, 0) + 1
        total_uses += p.get("use_count", 0)

    # Most used
    sorted_prompts = sorted(prompts, key=lambda x: x.get("use_count", 0), reverse=True)

    print(f"\n  📊 Prompt Library Stats\n")
    print(f"  Total prompts: {len(prompts)}")
    print(f"  Total uses: {total_uses}")
    print(f"  Categories: {len(categories)}")

    print(f"\n  📂 By Category:")
    for cat, count in sorted(categories.items()):
        print(f"     {cat}: {count}")

    print(f"\n  🏆 Most Used:")
    for p in sorted_prompts[:5]:
        print(f"     {p['name']}: {p.get('use_count', 0)} uses")
    print()


# ═══════════════════════════════════════════════════════════════════════
# Main CLI
# ═══════════════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="Prompt Library Manager")
    parser.add_argument("command", choices=["add", "search", "list", "use", "update", "delete",
                                            "export", "import", "stats"])
    parser.add_argument("query", nargs="?", default=None, help="Search query or prompt name")
    parser.add_argument("--workspace", default=None)
    parser.add_argument("--name", default=None, help="Prompt name")
    parser.add_argument("--category", default=None, help="Category")
    parser.add_argument("--template", default=None, help="Template text")
    parser.add_argument("--description", default=None, help="Description")
    parser.add_argument("--tags", default=None, help="Comma-separated tags")
    parser.add_argument("--model", default=None, help="Recommended model")
    parser.add_argument("--from-file", default=None, help="Load template from file")
    parser.add_argument("--var", action="append", default=[], help="Variable: key=value")
    parser.add_argument("--format", choices=["text", "json", "markdown"], default="text")
    parser.add_argument("--compact", action="store_true")
    parser.add_argument("--output", default=None, help="Output file")
    parser.add_argument("--file", default=None, help="Import file")
    parser.add_argument("--overwrite", action="store_true")
    parser.add_argument("--confirm", action="store_true")
    parser.add_argument("--tag", default=None, help="Filter by tag")

    args = parser.parse_args()
    lib_path = get_library_path(args.workspace)

    if args.command == "add":
        name = args.name or args.query
        if not name:
            print("  ❌ --name required")
            sys.exit(1)
        if not args.template and not args.from_file:
            print("  ❌ --template or --from-file required")
            sys.exit(1)
        cmd_add(lib_path, name, args.category, args.template, args.description, args.tags, args.model, args.from_file)
    elif args.command == "search":
        query = args.query
        if not query:
            print("  ❌ Search query required")
            sys.exit(1)
        cmd_search(lib_path, query, category=args.category, tag=args.tag, fmt=args.format)
    elif args.command == "list":
        cmd_list(lib_path, category=args.category, fmt=args.format, compact=args.compact)
    elif args.command == "use":
        name = args.name or args.query
        if not name:
            print("  ❌ Prompt name required")
            sys.exit(1)
        cmd_use(lib_path, name, variables=args.var, fmt=args.format)
    elif args.command == "update":
        name = args.name or args.query
        if not name:
            print("  ❌ --name required")
            sys.exit(1)
        cmd_update(lib_path, name, template=args.template, tags=args.tags, description=args.description)
    elif args.command == "delete":
        name = args.name or args.query
        if not name:
            print("  ❌ --name required")
            sys.exit(1)
        cmd_delete(lib_path, name, confirm=args.confirm)
    elif args.command == "export":
        cmd_export(lib_path, fmt=args.format, output=args.output, category=args.category)
    elif args.command == "import":
        if not args.file:
            print("  ❌ --file required")
            sys.exit(1)
        cmd_import_prompts(lib_path, args.file, overwrite=args.overwrite)
    elif args.command == "stats":
        cmd_stats(lib_path)


if __name__ == "__main__":
    main()
