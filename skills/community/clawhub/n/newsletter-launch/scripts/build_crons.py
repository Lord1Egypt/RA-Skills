#!/usr/bin/env python3
"""
build_crons.py — Generates OpenClaw cron job payloads for a new newsletter.

Usage:
    python3 build_crons.py <config_json_file> [--workspace <path>]

    --workspace  Path to the OpenClaw workspace root.
                 Defaults to the grandparent of this script's directory.
                 Override if your workspace is in a non-standard location.

Outputs JSON array of 4 cron definitions to stdout.
The agent reads this and calls the OpenClaw cron API to create each one.

Cron types:
    Research + Quarterly keywords: sessionTarget=isolated, payload.kind=agentTurn
    Write + Evergreen:             sessionTarget=main,     payload.kind=systemEvent
    (main+systemEvent = injected into the user's active session)
    (isolated+agentTurn = runs in a background agent session)

Crons produced:
    1. Research (Tue/Thu/Sat 9AM in user tz)     — isolated/agentTurn
    2. Write + KPI + publish-check spawn (Mon 9AM) — main/systemEvent
    3. Evergreen post (1st of month, 9AM)         — main/systemEvent
    4. Quarterly keyword research                  — isolated/agentTurn

Publish-check is spawned dynamically by the Write cron — not a standing job.

Config fields used:
    slug, name, beehiiv_pub_id, beehiiv_api_key, auto_post,
    publish_day, timezone (default: America/Chicago),
    owner_name (default: "you" — used in alert messages)
"""

import json
import sys
import argparse
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_DEFAULT_WORKSPACE = _SCRIPT_DIR.parent.parent.parent


def get_workspace(args_workspace=None):
    if args_workspace:
        return Path(args_workspace).resolve()
    return _DEFAULT_WORKSPACE


def build_crons(cfg, workspace=None):
    if workspace is None:
        workspace = str(_DEFAULT_WORKSPACE)

    slug = cfg["slug"]
    name = cfg["name"]
    pub_id = cfg.get("beehiiv_pub_id", "")
    api_key = cfg.get("beehiiv_api_key", "")
    auto_post = cfg.get("auto_post", False)
    publish_day = cfg.get("publish_day", "Tuesday")
    tz = cfg.get("timezone", "America/Chicago")
    owner = cfg.get("owner_name", "you")

    project_file = f"{workspace}/projects/{slug}.md"
    issue_log = f"{workspace}/projects/{slug}/issue-log.md"
    issue_template = f"{workspace}/projects/{slug}/issue-template.md"
    seo_brief = f"{workspace}/projects/{slug}/seo-research-brief.md"
    scripts = f"{workspace}/skills/newsletter-seo-pipeline/scripts"

    # ── Auto-post step (injected into write cron if Scale/Enterprise) ─────────
    if auto_post and pub_id and api_key:
        autopost_step = f"""
STEP 7 (AUTO-POST): Publish to Beehiiv via API.
Build the post payload:
{{
  "title": "<issue title>",
  "subtitle": "<one-sentence hook>",
  "content_html": "<full article as HTML — convert markdown to HTML first>",
  "slug": "<URL slug from article header>",
  "meta_default_title": "<meta title from article header>",
  "meta_default_description": "<meta description from article header>",
  "audience": "both",
  "status": "confirmed",
  "schedule_for": "<publish date ISO8601>"
}}
Run:
curl -s -X POST "https://api.beehiiv.com/v2/publications/{pub_id}/posts" \\
  -H "Authorization: Bearer {api_key}" \\
  -H "Content-Type: application/json" \\
  -d '<payload>'
If successful: log post ID to issue-log.md, update status to 'published'.
If failed: alert {owner} with full error and fallback to paste doc."""
        alert_step = "STEP 8"
        publish_note = "Auto-published to Beehiiv"
    else:
        autopost_step = ""
        alert_step = "STEP 7"
        publish_note = f"Paste doc ready — publish to beehiiv on {publish_day} (email + web)"

    crons = [
        # ── 1. Research cron ────────────────────────────────────────────────
        {
            "name": f"{name} — Weekly Research Pass",
            "schedule": {"kind": "cron", "expr": "0 9 * * 2,4,6", "tz": tz},
            "sessionTarget": "isolated",
            "delivery": {"mode": "none"},
            "failureAlert": {"after": 1, "channel": "telegram", "mode": "announce"},
            "payload": {
                "kind": "agentTurn",
                "timeoutSeconds": 300,
                "message": f"""NEWSLETTER RESEARCH PASS — {name}

STEP 1: Read {issue_log}. Determine next issue number N (last + 1).

STEP 2: Check for collection file at {workspace}/projects/{slug}/issue-{{N}}-collection.json.
If not found, create it:
{{"issue": N, "status": "collecting", "target_publish": "<next {publish_day}>", "sections": {{"News & Trends": [], "Business Ops": [], "Quick Win": [], "Tools & Resources": []}}}}

STEP 3: Read {issue_log} topic bank. Note topics covered in last 8 issues (freshness exclusion list).

STEP 4: Run 3-4 web searches relevant to the newsletter audience (read {project_file} for audience context).

STEP 5: For each item found, apply ALL FOUR gates:
- Gate 1: Backed by a real named source?
- Gate 2: Directly actionable for the audience?
- Gate 3: Not already in this collection?
- Gate 4: Not covering the same ground as the last 8 issues?
Only add items passing all four gates.

STEP 6: Add passing items to collection JSON: title, url, key_stat, relevance, source, gate_verified: true.

STEP 7: Count total items. Log to memory/YYYY-MM-DD.md: items added, total count, issue number.

Only alert {owner} if something urgent or time-sensitive. Otherwise complete silently."""
            }
        },

        # ── 2. Write cron (Monday) — includes KPI pull + dynamic publish-check ─
        {
            "name": f"{name} — Weekly Issue Write",
            "schedule": {"kind": "cron", "expr": "0 9 * * 1", "tz": tz},
            "sessionTarget": "main",
            "payload": {
                "kind": "systemEvent",
                "text": f"""NEWSLETTER ISSUE WRITE — {name}

STEP 1: Read {issue_template} — follow it exactly.
STEP 2: Read {issue_log}. Next issue = last + 1 (call it N).
STEP 3: Read collection file at {workspace}/projects/{slug}/issue-{{N}}-collection.json.

STEP 4 — MINIMUM GATE: Count total items. If fewer than 6: STOP.
Alert {owner}: '{name} Issue #[N] only has [X] items — minimum 6 needed. Research cron fires Tue/Thu/Sat. Reply "run research pass" to trigger manually.'

STEP 5: Run newsletter-seo-pipeline skill (mandatory — no skipping):
  5a. serp-analysis on primary keyword
  5b. seo-content-engine for outline
  5c. article-writing skill
  5d. python3 {scripts}/score_ai_patterns.py <draft_file>
      Score < 8: run de-ai-ify, re-score until >= 8
  5e. QVP quality gates (see newsletter-seo-pipeline SKILL.md Step 5)
  5f. python3 {scripts}/validate_seo.py <draft_file> "<keyword>"
      Fix all ISSUES before continuing
  5g. markdown-formatter
  5h. python3 {scripts}/build_paste_doc.py <draft_file> <YYYY-MM-DD>
{autopost_step}

STEP 6: Write final article to {workspace}/projects/{slug}/issue-{{N}}-FINAL.md
Update {issue_log}: add row for issue N, status: draft.

KPI PULL: Fetch latest Beehiiv stats (subscriber count, last post open/click rate).
Run: curl -s "https://api.beehiiv.com/v2/publications/{pub_id}/subscriptions?limit=1&status=active" -H "Authorization: Bearer {api_key}"
Append a KPI row to the KPIs table in {project_file}.

SPAWN PUBLISH-CHECK: Create a one-shot cron job (kind: at, {publish_day} noon {tz}) with this payload:
"Check whether {name} Issue #[N] has been published to Beehiiv.
Run: curl -s 'https://api.beehiiv.com/v2/publications/{pub_id}/posts?limit=5&status=confirmed' -H 'Authorization: Bearer {api_key}'
If issue N found: update {issue_log} status to published.
If not found: alert {owner}: '{name} Issue #[N] not published yet — paste doc at projects/{slug}/issue-[N]-FINAL-PASTE.md'
sessionTarget: main, deleteAfterRun: true."

{alert_step}: Alert {owner}:
'{name} Issue #[N] is ready.
File: projects/{slug}/issue-{{N}}-FINAL.md
Paste doc: projects/{slug}/issue-{{N}}-FINAL-PASTE.md

AI score: [X]/10 | SEO validated | QVP passed

{publish_note}'"""
            }
        },

        # ── 3. Evergreen post (monthly) ──────────────────────────────────────
        {
            "name": f"{name} — Monthly Evergreen Post",
            "schedule": {"kind": "cron", "expr": "0 9 1 * *", "tz": tz},
            "sessionTarget": "main",
            "payload": {
                "kind": "systemEvent",
                "text": f"""NEWSLETTER EVERGREEN POST — {name}

STEP 1: Read {seo_brief}. Find first keyword with Status: Pending or Future with no matching seo-post file in projects/{slug}/.
If none: alert {owner} — 'No evergreen keywords remaining for {name}. Quarterly research cron will replenish, or trigger manually.' Then STOP.

STEP 2: Read {issue_template} for voice and quality standards.

STEP 3: Run newsletter-seo-pipeline skill (mandatory — no skipping):
  3a. serp-analysis on target keyword
  3b. seo-content-engine (target 1,200-1,800 words)
  3c. article-writing skill
  3d. python3 {scripts}/score_ai_patterns.py <draft_file> (must be >= 8/10)
  3e. QVP quality gates (see newsletter-seo-pipeline SKILL.md Step 5)
  3f. python3 {scripts}/validate_seo.py <draft_file> "<keyword>"
  3g. markdown-formatter
  3h. python3 {scripts}/build_paste_doc.py <draft_file> <YYYY-MM-DD>

STEP 4: Write to {workspace}/projects/{slug}/seo-post-[N]-FINAL.md
Update keyword Status to 'Written' in {seo_brief}.
If < 3 pending keywords remain: also alert {owner} — 'Only [N] evergreen keywords left for {name}.'

STEP 5: Alert {owner}:
'{name} Evergreen Post #[N] ready.
File: projects/{slug}/seo-post-[N]-FINAL.md
Paste doc: projects/{slug}/seo-post-[N]-FINAL-PASTE.md

AI score: [X]/10 | SEO validated | QVP passed

Publish as web-only post in beehiiv (no email send).'"""
            }
        },

        # ── 4. Quarterly keyword research ────────────────────────────────────
        {
            "name": f"{name} — Quarterly Keyword Research",
            "schedule": {"kind": "cron", "expr": "0 9 1 1,4,7,10 *", "tz": tz},
            "sessionTarget": "isolated",
            "delivery": {"mode": "none"},
            "failureAlert": {"after": 1, "channel": "telegram", "mode": "announce"},
            "payload": {
                "kind": "agentTurn",
                "timeoutSeconds": 300,
                "message": f"""NEWSLETTER QUARTERLY KEYWORD RESEARCH — {name}

STEP 1: Read {seo_brief}. Count Tier 1 and Tier 2 keywords with Status: Pending or Future.

STEP 2: Read {project_file} for audience context. Run serp-analysis + web research to find 10 new high-intent, low-competition long-tail keywords (3+ words, directly actionable for the audience, not already in the list).

STEP 3: Add 10 new keywords to {seo_brief} under a new 'Tier 2 — [Quarter] [Year]' section.

STEP 4: If total pending count < 3 after adding: alert {owner} — '{name} keyword list still critically low. Manual research needed.'

STEP 5: Log to memory/YYYY-MM-DD.md: quarterly keyword research complete, N new keywords added.

Complete silently unless count is critically low."""
            }
        }
    ]

    return crons


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate cron definitions for a newsletter")
    parser.add_argument("config", help="Path to config JSON file")
    parser.add_argument(
        "--workspace", default=None,
        help="Path to OpenClaw workspace root (auto-detected from script location if omitted)"
    )
    args = parser.parse_args()

    workspace = str(get_workspace(args.workspace))

    with open(args.config) as f:
        cfg = json.load(f)

    crons = build_crons(cfg, workspace)
    print(json.dumps(crons, indent=2))
