#!/usr/bin/env python3
"""
scaffold_newsletter.py — Creates all project files for a new newsletter.

Usage:
    python3 scaffold_newsletter.py <config_json_file> [--workspace <path>]

    --workspace  Path to the OpenClaw workspace root.
                 Defaults to the grandparent of this script's directory.
                 Override if your workspace is in a non-standard location.

Outputs (all relative to workspace root):
    - projects/<slug>/                           (project root)
    - projects/<slug>/project.md                 (project memory file)
    - projects/<slug>/issue-log.md
    - projects/<slug>/issue-template.md
    - projects/<slug>/seo-research-brief.md
    - projects/<slug>/writing-style.md           (generated from style wizard answers)
    - projects/<slug>/issue-001-collection.json
    - skills/newsletter-launch/.skill-config/<slug>.json  (persisted config)

After scaffolding, commits all new files to git.
Exit codes: 0 = success, 1 = error
"""

import json
import sys
import os
import subprocess
import argparse
from pathlib import Path
from datetime import datetime

_SCRIPT_DIR = Path(__file__).resolve().parent
_DEFAULT_WORKSPACE = _SCRIPT_DIR.parent.parent.parent


def get_workspace(args_workspace=None):
    if args_workspace:
        return Path(args_workspace).resolve()
    return _DEFAULT_WORKSPACE


def load_config(path):
    with open(path) as f:
        return json.load(f)


def create_project_memory(cfg, slug_dir):
    slug = cfg["slug"]
    name = cfg["name"]
    audience = cfg["audience"]
    monetization = cfg["monetization"]
    publish_day = cfg.get("publish_day", "Tuesday")
    affiliate_tag = cfg.get("affiliate_tag", "")
    beehiiv_pub_id = cfg.get("beehiiv_pub_id", "")
    auto_post = cfg.get("auto_post", False)
    tz = cfg.get("timezone", "America/Chicago")

    affiliate_line = f"- Affiliate tag: {affiliate_tag}" if affiliate_tag else "- Affiliate: not configured"
    autopost_line = (
        "- Auto-publishing: enabled (Beehiiv Scale/Enterprise)"
        if auto_post
        else "- Auto-publishing: manual (free tier) — paste-ready docs generated each issue"
    )

    kw_rows = "\n".join(
        f"| {kw} | Issue / Evergreen | Pending |"
        for kw in cfg.get("seed_keywords", [])
    )

    content = (
        f"# {name} — Project Memory\n"
        f"Last updated: {datetime.now().strftime('%Y-%m-%d')}\n\n"
        f"## Status: PRE-LAUNCH | Strategy: SEO-First\n\n"
        f"## KPIs\n"
        f"| Date | Subscribers | Open Rate | Click Rate | Revenue | Sponsor Pipeline |\n"
        f"|------|-------------|-----------|------------|---------|------------------|\n"
        f"| {datetime.now().strftime('%Y-%m-%d')} | 0 | — | — | $0 | 0 prospects |\n\n"
        f"## Configuration\n"
        f"- Publication: {name}\n"
        f"- Slug: {slug}\n"
        f"- Beehiiv URL: https://{slug}.beehiiv.com\n"
        f"- Beehiiv Publication ID: {beehiiv_pub_id or 'NOT SET — add to config'}\n"
        f"- Publish day: {publish_day}\n"
        f"- Timezone: {tz}\n"
        f"{affiliate_line}\n"
        f"{autopost_line}\n\n"
        f"## Audience\n{audience}\n\n"
        f"## Monetization Strategy\n{monetization}\n\n"
        f"## Current Strategy\n"
        f"SEO-first. Every issue published as a public web post, optimized for search.\n"
        f"One evergreen SEO guide per month. Social paused until subscribers > 200.\n\n"
        f"## Writing Style\n"
        f"See writing-style.md in this project folder.\n\n"
        f"## SEO Skill Stack (mandatory — run in order)\n"
        f"Voice reference: projects/{slug}/writing-style.md\n"
        f"Full workflow: see newsletter-seo-pipeline SKILL.md\n\n"
        f"## Target Keywords\n"
        f"| Keyword | Assigned To | Status |\n"
        f"|---------|-------------|--------|\n"
        f"{kw_rows}\n\n"
        f"## Project Files\n"
        f"- Issue log: projects/{slug}/issue-log.md\n"
        f"- Issue template: projects/{slug}/issue-template.md\n"
        f"- SEO research brief: projects/{slug}/seo-research-brief.md\n"
        f"- Writing style: projects/{slug}/writing-style.md\n"
    )
    path = slug_dir / "project.md"
    path.write_text(content)
    return path


def create_writing_style(cfg, slug_dir):
    name = cfg["name"]
    style_reader = cfg.get("style_reader", "Busy professionals who read on mobile")
    style_tone = cfg.get("style_tone", "Direct and practical")
    style_vocab = cfg.get("style_vocab", "")

    # Parse vocab into use/avoid lists
    # Supports: "word1, word2 - never word3, word4" or "word1, word2 -- never use word3"
    vocab_use = []
    vocab_avoid = []
    if style_vocab:
        normalized = style_vocab.replace(" — ", " - ").replace(" -- ", " - ")
        # Split on ' - never' or 'never use' boundary
        import re
        parts = re.split(r'\s*-\s*never(?:\s+use)?\s*', normalized, maxsplit=1, flags=re.IGNORECASE)
        if len(parts) == 2:
            vocab_use = [v.strip() for v in parts[0].split(",") if v.strip()]
            vocab_avoid = [v.strip() for v in parts[1].split(",") if v.strip()]
        else:
            vocab_use = [v.strip() for v in style_vocab.split(",") if v.strip()]

    use_block = "\n".join(f"- {v}" for v in vocab_use) if vocab_use else "- (add audience-specific terms here)"
    avoid_block = "\n".join(f"- {v}" for v in vocab_avoid) if vocab_avoid else "- generic AI buzzwords (leverage, synergy, robust, seamless)\n- passive voice\n- vague qualifiers (significantly, dramatically, very)"

    content = (
        f"# Writing Style Guide — {name}\n\n"
        f"## Reader Profile\n"
        f"{style_reader}\n\n"
        f"## Tone\n"
        f"{style_tone}\n\n"
        f"Core tone rules:\n"
        f"- Lead with the business impact, dollar figure, or risk — never bury the lede\n"
        f"- Active voice always — rewrite every passive sentence\n"
        f"- Address the reader directly as 'you'\n"
        f"- One clear, actionable takeaway per section\n"
        f"- Numbers beat adjectives: '4 hours/week' not 'dramatically reduces time'\n\n"
        f"## Language Rules\n\n"
        f"**Use (audience vocabulary):**\n"
        f"{use_block}\n\n"
        f"**Never use:**\n"
        f"{avoid_block}\n\n"
        f"## Structure\n"
        f"- Short paragraphs: 2-3 sentences max — readers skim on mobile\n"
        f"- Hook in the first paragraph: open with a problem, number, or provocative fact\n"
        f"- H2s = one clear topic each, targeting a keyword variant where possible\n"
        f"- No filler transitions: remove 'moreover', 'furthermore', 'additionally'\n"
        f"- End every section with the practical implication, not a summary\n"
        f"- Single CTA at close — one action, not three options\n\n"
        f"## The Skim Test\n"
        f"A reader should be able to skim in 90 seconds and still know:\n"
        f"1. What the problem or opportunity is\n"
        f"2. What to do about it\n"
        f"3. What it's worth to them\n"
        f"If they can't — it's too dense. Cut or rewrite.\n"
    )
    path = slug_dir / "writing-style.md"
    path.write_text(content)
    return path


def create_issue_log(cfg, slug_dir):
    content = (
        f"# Issue Log — {cfg['name']}\n\n"
        f"| # | Keyword | File | Status | Published |\n"
        f"|---|---------|------|--------|----------|\n"
    )
    path = slug_dir / "issue-log.md"
    path.write_text(content)
    return path


def create_issue_template(cfg, slug_dir):
    name = cfg["name"]
    slug = cfg["slug"]
    publish_day = cfg.get("publish_day", "Tuesday")

    content = (
        f"# Issue Template — {name}\n\n"
        f"## Voice\n"
        f"See projects/{slug}/writing-style.md for the full style guide.\n\n"
        f"## Mandatory Skill Stack (run in order — no skipping)\n"
        f"See newsletter-seo-pipeline SKILL.md for full instructions.\n"
        f"Voice reference to pass to article-writing skill: projects/{slug}/writing-style.md\n\n"
        f"## Article Header Block (required at top of every output file)\n"
        f"Meta Title: <50-60 chars, includes primary keyword>\n"
        f"Meta Description: <150-160 chars, includes keyword + value prop>\n"
        f"URL Slug: <keyword-rich-hyphenated-slug>\n"
        f"Primary Keyword: <exact keyword phrase>\n\n"
        f"## Publish Checklist\n"
        f"- [ ] Article header block complete\n"
        f"- [ ] AI score >= 8/10\n"
        f"- [ ] All QVP gates passed\n"
        f"- [ ] SEO validation: no blocking issues\n"
        f"- [ ] Paste doc generated (-PASTE.md)\n"
        f"- [ ] Published on {publish_day} to BOTH email and web\n\n"
        f"## Issue Structure\n"
        f"1. Hook paragraph (problem + dollar figure or stat)\n"
        f"2. Section 1 (H2) — core news/insight\n"
        f"3. Section 2 (H2) — what it means for the reader\n"
        f"4. Section 3 (H2) — what to do about it\n"
        f"5. Quick Win (H2) — one actionable tip\n"
        f"6. CTA — subscribe link or affiliate recommendation\n"
    )
    path = slug_dir / "issue-template.md"
    path.write_text(content)
    return path


def create_seo_brief(cfg, slug_dir):
    name = cfg["name"]
    keywords = cfg.get("seed_keywords", [])
    kw_rows = "\n".join(f"| {kw} | Evergreen post | Pending |" for kw in keywords)

    content = (
        f"# SEO Research Brief — {name}\n\n"
        f"## Target Keywords\n\n"
        f"### Tier 1 — Write Now\n"
        f"| Keyword | Assigned To | Status |\n"
        f"|---------|-------------|--------|\n"
        f"{kw_rows}\n\n"
        f"### Tier 2 — Next Quarter\n"
        f"*(Replenished by quarterly keyword research cron)*\n\n"
        f"## Keyword Selection Criteria\n"
        f"- Long-tail (3+ words)\n"
        f"- Informational or transactional intent\n"
        f"- Directly actionable for the target audience\n"
        f"- Low-to-medium competition\n"
    )
    path = slug_dir / "seo-research-brief.md"
    path.write_text(content)
    return path


def create_collection(cfg, slug_dir):
    content = {
        "issue": 1,
        "status": "collecting",
        "target_publish": "",
        "sections": {
            "News & Trends": [],
            "Business Ops": [],
            "Quick Win": [],
            "Tools & Resources": []
        }
    }
    path = slug_dir / "issue-001-collection.json"
    path.write_text(json.dumps(content, indent=2))
    return path


def persist_config(cfg, workspace):
    config_dir = workspace / "skills" / "newsletter-launch" / ".skill-config"
    config_dir.mkdir(parents=True, exist_ok=True)
    path = config_dir / f"{cfg['slug']}.json"
    path.write_text(json.dumps(cfg, indent=2))
    return path


def git_commit(workspace, slug, name):
    """Commit all new project files to git."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--is-inside-work-tree"],
            cwd=str(workspace), capture_output=True, text=True
        )
        if result.returncode != 0:
            return None, "workspace is not a git repo — skipping commit"

        subprocess.run(
            ["git", "add", f"projects/{slug}/", f"skills/newsletter-launch/.skill-config/{slug}.json"],
            cwd=str(workspace), check=True, capture_output=True
        )
        commit_result = subprocess.run(
            ["git", "commit", "-m", f"feat: launch newsletter '{name}' — scaffold project files and config"],
            cwd=str(workspace), capture_output=True, text=True
        )
        if commit_result.returncode == 0:
            short_sha = commit_result.stdout.strip().split("\n")[0]
            return short_sha, None
        else:
            return None, commit_result.stderr.strip()
    except Exception as e:
        return None, str(e)


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new newsletter project")
    parser.add_argument("config", help="Path to config JSON file")
    parser.add_argument(
        "--workspace", default=None,
        help="Path to OpenClaw workspace root (auto-detected from script location if omitted)"
    )
    args = parser.parse_args()

    workspace = get_workspace(args.workspace)
    cfg = load_config(args.config)
    slug = cfg["slug"]
    name = cfg["name"]

    slug_dir = workspace / "projects" / slug
    slug_dir.mkdir(parents=True, exist_ok=True)

    created = []
    created.append(create_project_memory(cfg, slug_dir))
    created.append(create_writing_style(cfg, slug_dir))
    created.append(create_issue_log(cfg, slug_dir))
    created.append(create_issue_template(cfg, slug_dir))
    created.append(create_seo_brief(cfg, slug_dir))
    created.append(create_collection(cfg, slug_dir))
    created.append(persist_config(cfg, workspace))

    print(f"\nNewsletter '{name}' scaffolded successfully.\n")
    print("Files created:")
    for p in created:
        try:
            print(f"  {p.relative_to(workspace)}")
        except ValueError:
            print(f"  {p}")

    # Git commit
    sha, err = git_commit(workspace, slug, name)
    if sha:
        print(f"\nCommitted to git: {sha}")
    elif err:
        print(f"\nGit commit skipped: {err}")
    print()


if __name__ == "__main__":
    main()
