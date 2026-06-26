---
name: pmo-true-skill
version: 2.2.0
description: "AI-native PMO (Project Management Office) Skill for OpenClaw. Acts as Glue Code — connects to GitHub Issues, Notion, and other tools, then summarizes, alerts, and surfaces cross-project risks. MUST activate when user asks about: portfolio status, project health, weekly report, risk check, new project intake, or cross-project dependencies. Triggers on explicit /pmo commands OR any message containing: 'portfolio', 'all projects', '周报', 'weekly report', 'risk check', 'project status', '项目状态', '风险', 'new project', 'add project', 'stale', 'blocked'. This skill does NOT store project data — it reads from external tools and caches only events + risks locally."
---

# PMO Skill v2.2.0 — Glue Code PMO

## Precise Triggering Conditions

**You MUST invoke this skill when the message matches ANY of:**

```
IF user_message matches regex: /(?:^|\s)(\/pmo|pmo\s+)(list|status|risks|check|sync|weekly|add|remove)/i
IF user_message contains any of: ["portfolio", "all projects", "总览", "项目总览"]
IF user_message contains any of: ["周报", "weekly report", "weekly status", "周度报告"]
IF user_message contains any of: ["risk check", "scan risks", "风险扫描", "check risks"]
IF user_message contains any of: ["project status", "项目状态", "XXX 怎么样了", "how is.*doing"]
IF user_message contains any of: ["new project", "add project", "start tracking", "跟踪新项目"]
IF user_message contains any of: ["stale", "dormant", "blocked", "没有更新", "卡住了"]
IF user_message contains any of: ["cross-project", "dependency", "依赖", "关联项目"]
IF user_message matches regex: /p-?\d{3}/i  # project IDs like p-001
```

**If none of the above match, do NOT activate this skill.**

---

## Intent Classification (Hardcoded If-Else)

```python
def classify_intent(user_message: str, has_attachment: bool = False) -> str:
    """
    Returns one of: intake | remove | query_portfolio | query_project
                | query_risks | weekly_report | detect_risks | sync | unknown
    """
    msg = user_message.strip().lower()

    # === INTENT: intake ===
    if any(kw in msg for kw in ["new project", "add project", "start tracking",
                                  "跟踪新项目", "想跟踪一个", "我要加一个项目"]):
        return "intake"

    # === INTENT: remove ===
    if any(kw in msg for kw in ["remove project", "stop tracking", "delete project",
                                  "删除项目", "不跟踪了", "移除项目"]):
        return "remove"

    # === INTENT: weekly_report ===
    if any(kw in msg for kw in ["weekly", "周报", "周报生成", "weekly report",
                                  "status report", "周度"]):
        return "weekly_report"

    # === INTENT: detect_risks ===
    if any(kw in msg for kw in ["risk check", "scan", "风险扫描", "check risks",
                                  "scan risks", "detect risks", "风险检测"]):
        return "detect_risks"

    # === INTENT: sync ===
    if any(kw in msg for kw in ["sync", "refresh", "更新缓存", "re-sync"]):
        return "sync"

    # === INTENT: query_risks ===
    if any(kw in msg for kw in ["risks", "风险", "problems", "blockers",
                                  "有什么风险", "风险列表"]):
        return "query_risks"

    # === INTENT: query_portfolio ===
    if any(kw in msg for kw in ["portfolio", "all projects", "总览", "项目总览",
                                  "所有项目", "overview", "全局"]):
        return "query_portfolio"

    # === INTENT: query_project ===
    # Must have a project reference + status keyword, but NOT portfolio/risk keywords
    project_keywords = ["status", "怎么样了", "进度", "更新", "health",
                         "最近怎么样", "现在什么情况"]
    if any(pk in msg for pk in project_keywords):
        # Also check for project name/ID presence
        if not any(kw in msg for kw in ["portfolio", "all projects", "总览", "risks"]):
            return "query_project"

    # === INTENT: unknown ===
    return "unknown"


def route_intent(intent: str, user_message: str) -> str:
    """
    Given an intent, return the action to take.
    Each branch is an actual function name to call.
    """
    if intent == "intake":
        return "handle_intake"
    elif intent == "remove":
        return "handle_remove"
    elif intent == "query_portfolio":
        return "handle_portfolio"
    elif intent == "query_project":
        return "handle_project_status"
    elif intent == "query_risks":
        return "handle_risks"
    elif intent == "weekly_report":
        return "handle_weekly_report"
    elif intent == "detect_risks":
        return "handle_risk_detection"
    elif intent == "sync":
        return "handle_sync"
    elif intent == "unknown":
        return "handle_unknown"
    else:
        return "handle_unknown"
```

---

## Philosophy: Glue Code, Not Data Silo

This Skill does NOT store your project data. Your project data lives in:

- **GitHub Issues** (development tasks)
- **Notion** (planning docs, specs)
- **Linear / Jira** (if you use them)
- **飞书 / Slack** (conversational updates)

This Skill **reads** from those tools, **analyzes** with AI, and **alerts** proactively.

Local storage is minimal — only:
- Event log (append-only, for trend analysis)
- Cross-project risk register (things no single tool captures)
- Project cache (ID + URL + owner only)

---

## Data Architecture

```
memory/PMO/
├── config.yaml              # Tool connections (GitHub tokens, Notion IDs, etc.)
├── projects.yaml            # Project registry (id, name, source_url, owner, tags)
├── events.jsonl             # Append-only event log
├── risks.yaml               # Cross-project risks (things no single tool captures)
└── cache/                   # Temporary cache of external tool data (TTL 5min)
    └── {project-id}.json
```

### config.yaml
```yaml
integrations:
  github:
    enabled: true
    repos:
      - owner: my-org
        repo: erp-system
        token_env: GH_TOKEN
  notion:
    enabled: false
    databases: []
  feishu:
    enabled: true
    space_id: "xxx"

alerts:
  channels:
    telegram: true
    feishu: false
  stale_threshold_days: 7
  dormant_threshold_days: 14
  milestone_reminder_days: 1

review_cycle: weekly
```

### projects.yaml
```yaml
projects:
  - id: p-001
    name: "ERP System"          # Fictional: enterprise resource planning
    source: github
    source_url: "https://github.com/my-org/erp-system/issues"
    owner: alice
    tags: [backend, priority-high]
    methodology: agile
    created_at: "2026-04-01T09:00:00"

  - id: p-002
    name: "E-commerce App"      # Fictional: consumer-facing shopping app
    source: github
    source_url: "https://github.com/my-org/shop-app/issues"
    owner: bob
    tags: [frontend, priority-high]
    methodology: scrum
    created_at: "2026-04-01T09:00:00"

  - id: p-003
    name: "Mobile App iOS"      # Fictional: native iOS shopping companion
    source: notion
    source_url: "https://notion.so/my-org/mobile-ios"
    owner: carol
    tags: [mobile, ios, planning]
    methodology: kanban
    created_at: "2026-04-03T09:00:00"
```

### events.jsonl (Append-only)
```json
{"ts":"2026-04-06T10:00:00","event":"status_check","project_id":"p-001","source":"github","data":{"open_issues":5,"closed_this_week":2}}
{"ts":"2026-04-06T10:00:00","event":"risk_detected","project_id":"p-001","risk_id":"r-001","severity":"high","data":{"reason":"No update in 14 days"}}
{"ts":"2026-04-06T10:00:00","event":"report_generated","type":"weekly","actor":"pmo-skill","data":{"projects_reviewed":3,"risks_flagged":2}}
```

### risks.yaml
```yaml
risks:
  - id: r-001
    title: "Vendor API delay may block ERP Phase 2"    # Fictional
    category: technical
    severity: high
    status: open
    projects: ["p-001", "p-002"]
    owner: alice
    mitigation: "Get vendor API specs by April 15"
    created_at: "2026-04-06T10:00:00"

  - id: r-002
    title: "iOS developer OOO Apr 10-20 — blocks Mobile App iOS"  # Fictional
    category: resource
    severity: medium
    status: open
    projects: ["p-003"]
    owner: carol
    mitigation: "Bring in backup developer by Apr 8"
    created_at: "2026-04-05T10:00:00"
```

---

## Few-Shot Examples: When to Call This Skill

### Example 1 — Portfolio Status Query
```
User: "show me the portfolio overview"
Model: Calls handle_portfolio()
  → Read projects.yaml → Read all cache/*.json → Aggregate
  → Output: table of all projects with health indicators
```

### Example 2 — Weekly Report
```
User: "generate the weekly PMO report"
Model: Calls handle_weekly_report()
  → Read events.jsonl (last 7 days) + projects.yaml + risks.yaml
  → Output: formatted weekly report with activity, blockers, risks, next priorities
```

### Example 3 — New Project Intake
```
User: "我想跟踪一个新项目，叫电商App，是GitHub上的 my-org/shop"
Model: Calls handle_intake()
  → Extract: name="E-commerce App", source=github, repo="my-org/shop"
  → Append to projects.yaml (id: p-004)
  → Append intake event to events.jsonl
  → Output: "Project added. ID: p-004. Generate initial status report?"
```

### Example 4 — Risk Detection
```
User: "run a risk check across all projects"
Model: Calls handle_risk_detection()
  → For each project: check last_update, open issues age, milestone dates
  → Rules: stale=7d, dormant=14d, overdue=milestone past due
  → Compare cross-project dependencies for cascade risk
  → Output: new risks → write to risks.yaml; surface to user
```

### Example 5 — Specific Project Status
```
User: "how is the ERP System doing?"
Model: Calls handle_project_status()
  → Find project by name "ERP System" → id p-001
  → Read cache/p-001.json (or fetch from GitHub if stale)
  → Output: project health, open/closed issues, last update, blockers
```

---

## DO NOT DO X

**Explicit prohibitions — the skill should NEVER do these:**

1. **DO NOT** create local copies of GitHub Issues, Notion entries, or task items. Always read from source; never duplicate data.

2. **DO NOT** become a data-entry tool. If user describes tasks verbally, ask them to update the source system (GitHub/Notion), then re-sync.

3. **DO NOT** store passwords, tokens, or secrets in plain text files. Use environment variables (e.g., `GH_TOKEN` in config.yaml → `token_env`).

4. **DO NOT** generate fake project data or fabricate status updates. If no real data exists, say "No data found for this project — have you pushed any updates to GitHub/Notion?"

5. **DO NOT** send alerts to channels not configured in `config.yaml`. Always check `alerts.channels` before sending.

6. **DO NOT** modify or close GitHub Issues / Notion entries. This skill is read-only for external tools. It only writes to local files (projects.yaml, events.jsonl, risks.yaml).

7. **DO NOT** respond to casual conversation that has nothing to do with project management (e.g., "how was your weekend?"). Return `unknown` intent and respond minimally.

8. **DO NOT** run risk detection on more than 20 projects in a single pass to avoid token/API exhaustion. Batch into groups of 10.

9. **DO NOT** store sensitive project details (customer names, revenue figures, internal politics) in risks.yaml or events.jsonl. Keep entries high-level.

10. **DO NOT** auto-close risks. Risks stay open until a human marks them resolved in the source system and re-syncs.

---

## Behavior Rules

### Auto-actions
1. **Every `/pmo sync`** → Re-read all sources, update cache, detect risks
2. **Every Monday 9:00 AM** → Auto-generate weekly report, send to configured channels
3. **Every `/pmo check`** → Run risk detection, surface stale projects
4. **New risk detected** → Add to risks.yaml + notify via configured channels

### Proactive Alerts (configurable)
```
When:
- Project stale (7+ days no update) → "Hey, {project} hasn't been updated in X days"
- Risk severity >= high → "⚠️ Risk alert: {risk title}"
- Milestone due today → "📅 Milestone due today: {milestone} on {project}"
- Cross-project dependency blocked → "🔗 Dependency chain alert: {A} blocked → {B} blocked"
```

### Data Freshness
- Cache TTL: 5 minutes
- Stale after: 7 days
- Dormant after: 14 days
- Risk scan: on every `/pmo check` or `/pmo sync`

---

## Commands

| Command | Intent | Example |
|---------|--------|---------|
| `/pmo list` | query_portfolio | `/pmo list` |
| `/pmo status {project}` | query_project | `/pmo status erp` |
| `/pmo risks` | query_risks | `/pmo risks` |
| `/pmo check` | detect_risks | `/pmo check` |
| `/pmo sync` | sync | `/pmo sync` |
| `/pmo weekly` | weekly_report | `/pmo weekly` |
| `/pmo add {name}` | intake | `/pmo add "New Project"` |
| `/pmo remove {project}` | remove | `/pmo remove p-001` |

---

## Core Prompt Handlers

### handle_portfolio()
Reads: `projects.yaml` + `cache/*.json` + `risks.yaml`
Outputs: Portfolio overview table with health indicators per project.

### handle_weekly_report()
Reads: `events.jsonl` (last 7 days) + `projects.yaml` + `risks.yaml`
Outputs: Formatted weekly report.

### handle_risk_detection()
Reads: `projects.yaml` + `cache/*` + `events.jsonl`
Rules: stale=7d, dormant=14d, overdue milestone, cascade risk from dependencies.
Outputs: New risks → write to `risks.yaml`; display to user.

### handle_project_status(project_name)
Reads: `projects.yaml` (find by name/ID) + `cache/{id}.json` (or fetch from source)
Outputs: Single project status with issues and blockers.

### handle_intake(project_info)
Writes: Append to `projects.yaml`; append event to `events.jsonl`.
Outputs: Project ID, initial confirmation, optional status report.

### handle_remove(project_id)
Updates: Mark archived in `projects.yaml`; append removal event to `events.jsonl`.
Does NOT delete historical events.

### handle_sync()
Reads: Re-read all integrations (GitHub, Notion), update all cache files.
Outputs: Sync summary (N projects updated, M events logged).

### handle_unknown()
If intent is unknown: ask one clarifying question, do NOT assume.
Do NOT invoke full PMO logic for unrelated messages.

---

## Glue Code: External Integrations

### GitHub Integration

**Script:** `scripts/github_fetch.py`

The official GitHub integration uses `github_fetch.py` to read issues from repos configured in `config.yaml`.

**Usage:**
```bash
python scripts/github_fetch.py --owner my-org --repo my-project --token-env GH_TOKEN
```

**Output format (JSON):**
```json
{
  "project_name": "my-org/my-project",
  "owner": "my-org",
  "repo": "my-project",
  "open_count": 5,
  "closed_count": 12,
  "total_count": 17,
  "progress_pct": 70.6,
  "last_updated": "2026-04-05T14:30:00Z",
  "fetched_at": "2026-04-06T10:00:00Z",
  "issues": [
    {
      "id": 42,
      "title": "Fix authentication bug",
      "state": "open",
      "labels": ["bug", "priority-high"],
      "url": "https://github.com/my-org/my-project/issues/42",
      "created_at": "2026-04-01T09:00:00Z",
      "updated_at": "2026-04-05T14:30:00Z",
      "assignees": ["alice"]
    }
  ]
}
```

**In skill handlers**, call it like:
```python
import subprocess, json

def fetch_github_issues(owner: str, repo: str, token_env: str = "GH_TOKEN") -> dict:
    result = subprocess.run(
        ["python", "scripts/github_fetch.py",
         "--owner", owner, "--repo", repo,
         "--token-env", token_env],
        capture_output=True, text=True, cwd="/home/nekai/.openclaw/workspace/skills/pmo-true-skill"
    )
    return json.loads(result.stdout)
```

**Constraints:**
- Token comes from environment variable (`GH_TOKEN` by default) — never hardcoded
- Pull requests are excluded (only actual issues are fetched)
- Each call reads up to 100 open + 100 closed issues per repo
- Cache result in `memory/PMO/cache/{owner}-{repo}.json` with 5-min TTL

### Notion Integration (future)
```python
def fetch_notion_database(database_id: str, token: str) -> dict:
    """
    Reads from Notion Database API.
    Returns: {entries, last_updated, status_distribution}
    """
```

---

## Version History

- **v2.2.0** — GitHub integration via `scripts/github_fetch.py`, updated config.yaml template with real integration examples, enhanced docs for GitHub glue code.
- **v2.1.0** — Gemini顾问 review: added precise triggering conditions, hardcoded If-Else intent classification pseudocode, 5 few-shot examples, explicit DO NOT DO X section (10 rules). All examples fictional.
- **v2.0.0** — Complete rewrite. Glue Code philosophy. Minimal local storage. External integrations. Fictional examples only.
- **v1.1.0** — Full data model with YAML/JSONL local storage (now deprecated)
- **v1.0.1** — Initial skeleton
