# Loop Polish

> A TRAE Skill for fully automated iterative code polishing of full-stack projects.

**Start project → Full integration verification → Browser automation → Scoring → Auto-fix → Loop until perfect → Generate report.**

*"Not perfect, don't ship."*

---

## What is Loop Polish?

Loop Polish is a TRAE Skill that automates the entire quality assurance cycle for full-stack projects. Instead of manually testing, fixing, re-testing, and repeating, you just say:

```
Run loop polish on my project
```

The Skill will:

1. **Start** your project (backend + frontend), handling cleanup and port conflicts
2. **Verify** every API endpoint, every frontend page, and database state consistency
3. **Score** all features across 5 dimensions (completeness, correctness, UX, error handling, performance)
4. **Auto-fix** discovered issues (with safe Git branching, precise rollback, and human confirmation for high-risk changes)
5. **Regress** intelligently — only re-test what changed
6. **Loop** until the target score is reached (or max rounds/timeout)
7. **Generate** a detailed quality report with score trends, fix diffs, and recommendations

---

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/$(your-username)/loop-polish.git
cd loop-polish
```

**Linux/macOS:**
```bash
./install.sh /path/to/your-project
```

**Windows (PowerShell):**
```powershell
.\install.ps1 -TargetPath C:\path\to\your-project
```

**Manual install:**
Copy `SKILL.md` to your project:
```
mkdir -p your-project/.trae/skills/loop-polish
cp SKILL.md your-project/.trae/skills/loop-polish/
```

### 2. (Optional) Configure

Create a `.loop-polish.json` in your project root, or just use the defaults:

```json
{
  "mode": "full",
  "max_rounds": 10,
  "target_score": 100,
  "scope": "all",
  "auto_fix": { "enabled": true, "strategy": "conservative", "max_per_round": 3 },
  "browser": { "headless": true },
  "report": { "format": "markdown", "output_dir": "./polish-reports/" },
  "timeout_minutes": 120
}
```

### 3. Run

In TRAE, just say:

```
# Full polish
Run loop polish on my project

# Quick scan (no fix, just score)
Loop polish preflight: API only

# Custom
Loop polish: 5 rounds, 95 target score, aggressive strategy, HTML report

# Specific modules
Run loop polish on user module and order module, target 100
```

---

## Two Modes

| Mode | What it does | Use case |
|------|-------------|----------|
| **Full** | Full cycle: verify → score → fix → regress → loop until perfect | Pre-release QA, delivery gate |
| **Preflight** | Verify → score → stop (no fix, no loop) | Quick quality check, CI gate, first assessment |

---

## Three Fix Strategies

| Strategy | What it fixes | Risk |
|----------|--------------|------|
| `conservative` | Only compile errors, null pointers, type mismatches, simple logic errors. Max 3 per round, single-file. | **Low** |
| `moderate` | Plus data consistency issues, state synchronization. Max 5 per round, ≤ 2 files. | **Medium** |
| `aggressive` | Plus UX issues, performance problems. Cross-module allowed. Max 10 per round. | **High** |

All fixes happen in isolated Git branches (`loop-polish/round-{timestamp}`). Your main branch is never touched.

---

## Supported Frameworks

| Layer | Frameworks |
|-------|-----------|
| Backend | Spring Boot (Java), Express/Koa (Node.js), Flask/Django (Python), Go |
| Frontend | Vue 3, React, Angular |

---

## What Gets Verified

### Backend API
- Every endpoint (GET/POST/PUT/DELETE) scanned from source code
- Normal, boundary, missing-field, and permission tests
- Auto auth token acquisition
- Path parameter dependency chains (POST → get ID → GET/PUT/DELETE)
- Failure diagnostics (backend logs, full response, request details)

### Frontend Browser
- Auto route discovery (Vue Router / React Router)
- Form scanning from source (avoids blind clicking)
- Page load, form interaction, list operations, modals, navigation
- Screenshots + console errors + network logs on failure

### Database State
- Direct database verification after every write operation
- Confirms records are actually written/updated/deleted
- Supports MySQL, PostgreSQL, SQLite

---

## Scoring System

| Dimension | Weight | What it measures |
|-----------|--------|-----------------|
| Functional Completeness | 40% | Can features be used normally? |
| Data Correctness | 25% | Is data correct end-to-end? |
| UX | 15% | Are interactions smooth? |
| Error Handling | 10% | Are errors handled gracefully? |
| Performance | 10% | Are pages/APIs fast enough? |

---

## Prerequisites

- Project is buildable and runnable
- `npx playwright install chromium` (auto-installed on first run if missing)
- Database is connectable with initial data

---

## Safety Guarantees

- **Isolated Git branch** — all fixes on a separate branch, never on main
- **Precise rollback** — failed fixes are restored to original code, not just `git checkout`
- **High-risk confirmation** — Schema changes, auth logic changes, and large deletions require human approval
- **Auto stash/pop** — uncommitted changes are stashed before starting and restored on completion
- **Interrupt recovery** — auto-saves state to `.loop-polish-state.json`, resumes from breakpoint

> **Important safety notes:**
> - Port cleanup may terminate processes on 8080/3000/5000/5173 — only if confirmed as project-owned
> - Database verification reads credentials from config files — set `db_verify: false` to skip
> - All diagnostic data (auth tokens, cookies, passwords) is redacted before saving to reports 
> - All operations are designed for **dev/staging environments only**, NOT production
> - Preflight mode is strictly read-only — no data writes, no code changes

---

## Full Documentation

See [SKILL.md](./SKILL.md) for the complete AI execution instructions, including step-by-step tool calls, scoring formulas, fix decision trees, and interrupt recovery details.

---

## License

MIT