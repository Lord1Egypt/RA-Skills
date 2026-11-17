# AI-* Family — Complete Installation Guide for Claude

**Applies to:** Claude Code (CLI agent) — the recommended Claude platform for AIFLC packages.

> **Why Claude Code specifically?** The AI-* Family packages need workspace file access to function fully (reading rule-detail files on demand, writing deliverables, persisting state between sessions). Claude Code is the only Claude product that provides this. See the [claude.ai section](#claudeai-web--projects--limited) at the end for the web-based alternative and its limitations.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [How It Works](#how-it-works)
- [Method 1: Automated Installer (Recommended)](#method-1-automated-installer-recommended)
- [Method 2: Manual Installation](#method-2-manual-installation)
- [Multi-Package Installation](#multi-package-installation)
- [Package Reference](#package-reference)
- [Resulting Workspace Structure](#resulting-workspace-structure)
- [Verification](#verification)
- [Using the Packages](#using-the-packages)
- [Chain Handoffs Between Packages](#chain-handoffs-between-packages)
- [AI-GCE Governance on Claude Code](#ai-gce-governance-on-claude-code)
- [Session Continuity](#session-continuity)
- [claude.ai (Web / Projects) — Limited](#claudeai-web--projects--limited)
- [Coexistence with Other Rules](#coexistence-with-other-rules)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Claude Code** | Installed and authenticated ([claude.ai/download](https://claude.ai/download)) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

The installer places **one always-loaded file** plus the **package home**, both scoped to the AI-* PDLC Family (multiple AIFLC families can coexist in one workspace):

1. **Session orchestrator** — deployed as `CLAUDE_PDLC_ORCHESTRATOR.md` at the workspace root and wired into a real root `CLAUDE.md` via an `@import`. This is the single always-loaded entry point. It detects which package you want and `Read`s that package's core on demand from `.aiflc/pdlc/`.
2. **Package home** — every package's core AND rule-details live together in the uniform, agent-neutral home `.aiflc/pdlc/`. Nothing here auto-loads; the orchestrator reads from it on demand. Package cores are **not** root files anymore.

```
your-workspace/
├── CLAUDE.md                      ← Auto-loaded; imports @CLAUDE_PDLC_ORCHESTRATOR.md
├── CLAUDE_PDLC_ORCHESTRATOR.md    ← Always-on router (loaded via the import above)
├── .aiflc/
│   └── pdlc/                      ← AI-* PDLC Family home (cores + rule-details + fabric)
│       ├── ai-pilc-rules/core-workflow.md    ← Read on demand when you activate AI-PILC
│       ├── ai-pilc-rule-details/             ← Read on demand by the core
│       │   ├── common/  inception/  assessment/  templates/  ...
│       └── ... one {pkg}-rules/ + {pkg}-rule-details/ per installed package
├── pdlc-ws/                       ← All runtime outputs land here (never workspace root)
└── (your project files)
```

Claude Code auto-loads **only** `CLAUDE.md` (plus `CLAUDE.local.md`, `.claude/CLAUDE.md`, and `.claude/rules/*.md`) — there is no `CLAUDE*.md` filename wildcard. The installer creates a root `CLAUDE.md` that imports the orchestrator (`@CLAUDE_PDLC_ORCHESTRATOR.md`); the orchestrator then `Read`s each package core from `.aiflc/pdlc/` on demand. That is how the packages inject their expertise into Claude's context without you needing to paste anything. (The installer also generates `.claude/commands/pdlc/*.md` slash commands so you can invoke a package as, e.g., `/pdlc:pilc`, plus destination shortcuts like `/pdlc:dat` and `/pdlc:fhc`.)

> **The AIFLC model:** `CLAUDE.md` (auto) → imports the orchestrator (always-on router) → `Read`s one package core + its rule-details from the uniform home `.aiflc/pdlc/` on demand. Everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Method 1: Automated Installer (Recommended)

The interactive installer handles all file placement automatically.

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive (asks platform, packages, target)
.\installer\install.ps1

# Option B: One-liner for Claude Code with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Claude Code
./installer/install.sh --target <your-project-path> --platform claude-code --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform claude-code --bundle full
```

### Preset Bundles

| Bundle | Command Flag | Packages | Best For |
|--------|-------------|----------|----------|
| **Greenfield Full** | `-Bundle full` | AI-ILC + AI-PILC + AI-PPM + AI-FLO + AI-POLC + AI-UXD + AI-ADLC + AI-DWG + AI-GCE + AI-TGE + AI-DFE | New project, complete family |
| **Greenfield Minimal** | `-Bundle minimal` | AI-PILC + AI-ADLC + AI-DWG | Quick start, architecture focus |
| **Architecture Focus** | `-Bundle arch` | AI-ADLC + AI-DWG + AI-GCE | Architecture → workspace → governance |
| **Governance Only** | `-Bundle governance` | AI-GCE + AI-TGE | Existing project, add compliance |
| **Portfolio** | `-Bundle portfolio` | AI-ILC + AI-PILC + AI-PPM + AI-FLO | Multi-project management |

### Dry Run (Preview Without Installing)

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Bundle full -DryRun
```

This shows exactly what files would be copied and where, without modifying anything.

---

## Method 2: Manual Installation

If you prefer to install manually or need to understand what goes where.

### Single Package Example (AI-PILC)

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

# Place the orchestrator at the root and wire it into CLAUDE.md via an @import
Copy-Item "$Source\session-orchestrator.claude.md" "$Target\CLAUDE_PDLC_ORCHESTRATOR.md"
if (-not (Test-Path "$Target\CLAUDE.md")) { New-Item -ItemType File -Path "$Target\CLAUDE.md" | Out-Null }
Add-Content "$Target\CLAUDE.md" "`n@CLAUDE_PDLC_ORCHESTRATOR.md`n"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
mkdir -p "$TARGET/.aiflc/pdlc"
cp -R "$SOURCE/ai-pilc/ai-pilc-rules" "$TARGET/.aiflc/pdlc/"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details" "$TARGET/.aiflc/pdlc/"

# Place the orchestrator at the root and wire it into CLAUDE.md via an @import
cp "$SOURCE/session-orchestrator.claude.md" "$TARGET/CLAUDE_PDLC_ORCHESTRATOR.md"
printf '\n@CLAUDE_PDLC_ORCHESTRATOR.md\n' >> "$TARGET/CLAUDE.md"
```

### File Placement Convention (Claude Code)

The orchestrator is the only always-loaded file (root `CLAUDE_PDLC_ORCHESTRATOR.md`, imported by `CLAUDE.md`). Every package core + its rule-details live in the uniform home `.aiflc/pdlc/`, read on demand.

| Package | Core (read on demand) | Details (read on demand) |
|---------|-----------------------|--------------------------|
| AI-ILC | `.aiflc/pdlc/ai-ilc-rules/core-workflow.md` | `.aiflc/pdlc/ai-ilc-rule-details/` |
| AI-PILC | `.aiflc/pdlc/ai-pilc-rules/core-workflow.md` | `.aiflc/pdlc/ai-pilc-rule-details/` |
| AI-ADLC | `.aiflc/pdlc/ai-adlc-rules/core-workflow.md` | `.aiflc/pdlc/ai-adlc-rule-details/` |
| AI-UXD | `.aiflc/pdlc/ai-uxd-rules/core-workflow.md` | `.aiflc/pdlc/ai-uxd-rule-details/` |
| AI-POLC | `.aiflc/pdlc/ai-polc-rules/core-workflow.md` | `.aiflc/pdlc/ai-polc-rule-details/` |
| AI-DWG | `.aiflc/pdlc/ai-dwg-rules/core-generator.md` | `.aiflc/pdlc/ai-dwg-rule-details/` |
| AI-GCE | `.aiflc/pdlc/ai-gce-rules/core-generator.md` | `.aiflc/pdlc/ai-gce-rule-details/` |
| AI-TGE | `.aiflc/pdlc/ai-tge-rules/core-engine.md` | `.aiflc/pdlc/ai-tge-rule-details/` |
| AI-PPM | `.aiflc/pdlc/ai-ppm-rules/core-engine.md` | `.aiflc/pdlc/ai-ppm-rule-details/` |
| AI-FLO | `.aiflc/pdlc/ai-flo-rules/core-engine.md` | `.aiflc/pdlc/ai-flo-rule-details/` |
| AI-DFE | `.aiflc/pdlc/ai-dfe-rules/core-engine.md` | `.aiflc/pdlc/ai-dfe-rule-details/` |

> **Why the orchestrator + `.aiflc/pdlc/` split?** Claude Code auto-loads only `CLAUDE.md` — it does **not** read files by a `CLAUDE*.md` wildcard. So the family puts a single always-on router at the root (imported by `CLAUDE.md`) and keeps every package core out of the auto-load path, in the uniform home `.aiflc/pdlc/`, where the orchestrator `Read`s them on demand (the Claude analog of Kiro's `inclusion: manual`). This keeps the always-on context tiny and lets multiple packages (and multiple AIFLC families) coexist without conflicts.

### Alternative: Using `.claude/rules/` Directory

Claude Code also supports a `.claude/rules/` directory where each rule file is loaded on every session (unless `paths:`-scoped). If you deliberately want a small always-on subset, you can place a copy of a package core there — but the cores themselves still live in `.aiflc/pdlc/`:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Copy the package cores + rule-details into the uniform home (as usual)
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

# OPTIONAL: pin one core as always-on by copying it into .claude/rules/pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.claude\rules\pdlc"
Copy-Item "$Source\ai-pilc\ai-pilc-rules\core-workflow.md" "$Target\.claude\rules\pdlc\ai-pilc.md"
```

Use this only when you want a specific core loaded every session; files in `.claude/rules/` load on **every** session unless you `paths:`-scope them, so pinning all 11 cores there would defeat the lightweight on-demand design. The recommended path is the root `CLAUDE.md` + orchestrator (cores `Read` from `.aiflc/pdlc/` on demand).

---

## Multi-Package Installation

### Installing All 11 Packages (Full Chain)

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform claude-code -Bundle full
```

Or manually:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Ensure the uniform home exists
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc" | Out-Null

$packages = @(
    "ai-ilc", "ai-pilc", "ai-ppm", "ai-flo", "ai-adlc",
    "ai-uxd", "ai-polc", "ai-dwg", "ai-gce", "ai-tge", "ai-dfe"
)

# Copy every package core + rule-details into the uniform home (plain copies, no CLAUDE_PDLC_AI_* root files)
foreach ($pkg in $packages) {
    $rulesSource = Join-Path $Source "$pkg\$pkg-rules"
    $detailsSource = Join-Path $Source "$pkg\$pkg-rule-details"

    if (Test-Path $rulesSource) {
        Copy-Item -Recurse $rulesSource "$Target\.aiflc\pdlc\" -Force
        Copy-Item -Recurse $detailsSource "$Target\.aiflc\pdlc\" -Force
        Write-Host "Installed $pkg into .aiflc/pdlc/" -ForegroundColor Green
    } else {
        Write-Host "Skipped $pkg - source not found" -ForegroundColor Yellow
    }
}

# Place the orchestrator at the root and wire it into CLAUDE.md
Copy-Item "$Source\session-orchestrator.claude.md" "$Target\CLAUDE_PDLC_ORCHESTRATOR.md" -Force
if (-not (Test-Path "$Target\CLAUDE.md")) { New-Item -ItemType File -Path "$Target\CLAUDE.md" | Out-Null }
if (-not (Select-String -Path "$Target\CLAUDE.md" -Pattern 'CLAUDE_PDLC_ORCHESTRATOR' -Quiet)) {
    Add-Content "$Target\CLAUDE.md" "`n@CLAUDE_PDLC_ORCHESTRATOR.md`n"
}
Write-Host "Installed session orchestrator" -ForegroundColor Green
```

### Context Window Consideration

Only the orchestrator loads at session start — not the package cores. With 11 packages installed, the always-on footprint is just the single router file:

- **The orchestrator is compact** — it routes by intent and `Read`s exactly one package core from `.aiflc/pdlc/` when you activate it.
- **Package cores stay dormant** in `.aiflc/pdlc/` until invoked (each is orchestration logic, 1–3 KB), so installing all 11 costs nothing at session start.
- **The AI activates only one package at a time** — the others remain unread until you need them.

---

## Package Reference

| # | Package | What It Does | Activation Phrase |
|---|---------|-------------|-------------------|
| 1 | **AI-ILC** | Evaluates raw ideas → Approved Idea Brief | "Using AI-ILC, evaluate this idea" |
| 2 | **AI-PILC** | Raw requirement → Project Initiation Package | "Using AI-PILC, initiate a project" |
| 3 | **AI-PPM** | Portfolio governance across multiple projects | "Using AI-PPM, manage my portfolio" |
| 4 | **AI-FLO** | Routes handoffs between packages | "Using AI-FLO, route this output" |
| 5 | **AI-ADLC** | Requirements → Architecture Package | "Using AI-ADLC, design the architecture" |
| 6 | **AI-UXD** | PIP/AP → UX Design Package (personas, flows) | "Using AI-UXD, design the user experience" |
| 7 | **AI-POLC** | PIP/AP → Product Backlog Package | "Using AI-POLC, build the product backlog" |
| 8 | **AI-DWG** | Architecture → Ready-to-code workspace | "Using AI-DWG, generate the workspace" |
| 9 | **AI-GCE** | Workspace → Compliance enforcement layer | "Using AI-GCE, set up governance" |
| 10 | **AI-TGE** | Workspace → Test strategy & coverage tracking | "Using AI-TGE, establish test governance" |
| 11 | **AI-DFE** | Gather, shape, and distribute structured data | "Using AI-DFE, gather data" |

### Common Starting Points

| Scenario | Start With | Then |
|----------|-----------|------|
| New project from scratch | AI-PILC | → AI-POLC → AI-UXD → AI-ADLC → AI-DWG |
| Have requirements, need architecture | AI-ADLC | → AI-DWG |
| Have architecture, need workspace | AI-DWG | → AI-GCE + AI-TGE |
| Idea evaluation (pre-project) | AI-ILC | → AI-PILC if approved |
| Existing project, add compliance | AI-GCE | + AI-TGE |
| Need UX design alongside architecture | AI-UXD | (runs parallel to AI-ADLC) |
| Need a product backlog | AI-POLC | (runs parallel to AI-ADLC) |

---

## Resulting Workspace Structure

After a full install (`-Bundle full`), your workspace looks like this:

```
your-project/
├── CLAUDE.md                        ← Auto-loaded; imports @CLAUDE_PDLC_ORCHESTRATOR.md
├── CLAUDE_PDLC_ORCHESTRATOR.md      ← The ONLY always-loaded family file (routes to cores)
├── .claude/
│   └── commands/
│       └── pdlc/                    ← Generated slash commands (/pdlc:pilc, /pdlc:adlc, /pdlc:dat, ...)
├── .aiflc/
│   └── pdlc/                        ← AI-* PDLC Family home (cores + rule-details, on-demand)
│       ├── ai-ilc-rules/core-workflow.md
│       ├── ai-ilc-rule-details/        ← idea lifecycle details
│       ├── ai-pilc-rules/core-workflow.md
│       ├── ai-pilc-rule-details/       ← project initiation details
│       │   ├── common/
│       │   ├── inception/
│       │   ├── assessment/
│       │   ├── justification/
│       │   ├── authorization/
│       │   ├── planning/
│       │   ├── mobilization/
│       │   └── templates/
│       ├── ai-ppm-rules/core-engine.md
│       ├── ai-ppm-rule-details/
│       ├── ai-flo-rules/core-engine.md
│       ├── ai-flo-rule-details/
│       ├── ai-adlc-rules/core-workflow.md
│       ├── ai-adlc-rule-details/
│       ├── ai-uxd-rules/core-workflow.md
│       ├── ai-uxd-rule-details/
│       ├── ai-polc-rules/core-workflow.md
│       ├── ai-polc-rule-details/
│       ├── ai-dwg-rules/core-generator.md
│       ├── ai-dwg-rule-details/
│       ├── ai-gce-rules/core-generator.md
│       ├── ai-gce-rule-details/
│       ├── ai-tge-rules/core-engine.md
│       ├── ai-tge-rule-details/
│       ├── ai-dfe-rules/core-engine.md
│       └── ai-dfe-rule-details/
├── pdlc-ws/                         ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   ├── .ai-family-manifest.json     ← Installer tracking (for uninstall)
│   └── tools/                       ← Family tools (visual tools / extensions)
│       └── extensions/
│           ├── AIFLC-PDLC-Dashboard/ ← HTML dashboard + .vsix (reads ../../data/ via AI-DFE)
│           └── AIFLC-CommandBoard/   ← Trigger palette (HTML + .vsix)
└── (your project files)
```

> **Note:** The `.aiflc/pdlc/` home is dot-prefixed (hidden) and won't clutter your project view in most file explorers.

---

## Verification

After installation, verify everything is working:

### Step 1: Confirm files are in place

```powershell
# Windows
Get-ChildItem "<your-project-path>\CLAUDE_PDLC_ORCHESTRATOR.md"
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory
```

```bash
# macOS/Linux
ls <your-project-path>/CLAUDE_PDLC_ORCHESTRATOR.md
ls -d <your-project-path>/.aiflc/pdlc/ai-*-rules/
ls -d <your-project-path>/.aiflc/pdlc/ai-*-rule-details/
```

### Step 2: Start Claude Code in your workspace

```bash
# Navigate to your project
cd <your-project-path>

# Start Claude Code
claude
```

### Step 3: Test activation

Type one of these prompts:

```
Using AI-PILC, initiate a project from this requirement: [paste your requirement]
```

```
Using AI-ADLC, design the architecture for this system: [describe your system]
```

```
Using AI-ILC, evaluate this idea: [describe your idea]
```

**Expected:** Claude should respond with the package's welcome message and begin the structured workflow, asking about depth level and presenting the first stage.

### Step 4: Verify on-demand loading

During a workflow, when Claude transitions to a new phase, it should read the corresponding rule-details file automatically. You'll see file-read tool calls in Claude Code's output referencing paths like `.aiflc/pdlc/ai-pilc-rule-details/inception/stage-01-...`.

If Claude says it can't find rule details, check the folder paths match what the core workflow expects (see [Troubleshooting](#troubleshooting)).

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell Claude which package to use with the activation phrase
2. **Choose depth:** The package asks if you want Minimal, Standard, or Comprehensive output
3. **Work through stages:** Each package has defined stages. Claude guides you through them sequentially
4. **Approve at gates:** At the end of each stage, Claude presents output and waits for your approval before proceeding
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk as a file)

### Depth Levels

| Level | Output Volume | Best For |
|-------|--------------|----------|
| **Minimal** | Key essentials only | Prototypes, small projects, time-pressed |
| **Standard** | Professional baseline | Most projects (recommended default) |
| **Comprehensive** | Enterprise-grade detail | Regulated industries, large teams, audit-heavy |

### Example: Running AI-PILC

```
You: Using AI-PILC, initiate a project from this requirement:

We need a customer portal that allows clients to submit and track support
tickets, view their account status, and download invoices. It should
integrate with our existing Salesforce CRM and support SSO via Azure AD.
Target launch is Q1 2027 with a budget around $400K.
```

Claude will respond with the AI-PILC welcome, ask about depth, then walk you through 6 phases / 16 stages:
1. **Inception** — Source analysis, project definition, stakeholder identification
2. **Assessment** — Feasibility, risk analysis, resource assessment
3. **Justification** — Business case development
4. **Authorization** — Governance approval
5. **Planning** — Detailed planning across multiple dimensions
6. **Mobilization** — Team formation, kickoff

Each stage produces a deliverable file in your workspace.

---

## Chain Handoffs Between Packages

Packages detect each other's output through **state marker files**. When a package completes, it writes a marker (e.g., `pilc-state.md`). When the next package starts, it looks for upstream markers and enriches its work with that context.

### Example Chain: PILC → POLC → UXD → ADLC → DWG

```
1. Run AI-PILC → produces Project Initiation Package (PIP) + pilc-state.md
2. Run AI-POLC → detects pilc-state.md, reads PIP as input → produces Product Backlog Package (PBP) + polc-state.md
3. Run AI-UXD → detects pilc-state.md + polc-state.md → produces UX Design Package (UXP) + uxd-state.md
4. Run AI-ADLC → detects pilc-state.md + polc-state.md + uxd-state.md → produces Architecture Package (AP) + adlc-state.md
5. Run AI-DWG → detects adlc-state.md (+ polc-state.md, uxd-state.md) → generates ready-to-code workspace
```

**No manual wiring needed.** Just run packages sequentially and they find each other's output automatically.

### Packages That Run in Parallel

In the project layer, three packages can run simultaneously:
- **AI-ADLC** (architecture)
- **AI-UXD** (UX design)
- **AI-POLC** (product backlog)

All three accept PIP as input and produce independent outputs that AI-DWG combines.

---

## AI-GCE Governance on Claude Code

AI-GCE (Governance & Compliance Engine) is the one package with reduced capability on Claude Code vs. Kiro:

### What Works (100%)

- Rule generation (`.governance/rules/`) — full mode 1/2/3/4
- Compliance documentation
- Brownfield baseline scanning
- Hook and agent file generation (structurally valid)

### What Doesn't Work (Kiro-only features)

| Feature | Why | Workaround |
|---------|-----|------------|
| Hook auto-execution | No event bus in Claude Code | Append critical rules to CLAUDE.md |
| Agent shortcut triggers | No `.kiro/agents/` runtime | Paste agent prompts manually |
| Automatic compliance logging | Triggered by hooks | Ask Claude to log manually |
| Re-derivation auto-trigger | Requires file-edit events | Say "re-derive governance" manually |

### Best Practice: Maximizing Governance Value

After AI-GCE generates your governance layer, add this section to your root `CLAUDE.md` (create one if it doesn't exist):

```markdown
## Governance Rules (Always Enforce)

The following rules from `.governance/rules/` apply to ALL work in this workspace.
Check compliance on every file you create or modify.

- See: .governance/rules/security-rules.md (CRITICAL)
- See: .governance/rules/architecture-rules.md
- See: .governance/rules/naming-conventions.md
- See: .governance/COMPLIANCE_README.md for full rule index
```

Then periodically ask Claude: "Run a compliance check against `.governance/rules/` on recent changes."

This gives you ~70% of Kiro's enforcement value through advisory compliance.

---

## Session Continuity

Each workflow package maintains a **state file** (e.g., `pilc-state.md`) that records:
- Current phase and stage
- Completed stages
- Pending decisions
- Selected depth level
- Key outputs produced

**This means you can close Claude Code and resume later.** When you start a new session and say "Continue AI-PILC", Claude reads the state file and picks up exactly where you left off.

> **Important:** Don't delete state files unless you want to restart a workflow from scratch.

---

## claude.ai (Web / Projects) — Limited

If you only have access to claude.ai (the web chat), here's what works and what doesn't:

### Setup via Claude Projects

1. Go to [claude.ai](https://claude.ai) → Create a new **Project**
2. Upload `core-workflow.md` (from any package) as **Project Knowledge**
3. Upload the contents of the matching `*-rule-details/` folder as additional knowledge files
4. Set custom instructions: "Follow core-workflow.md as your primary orchestration"

### Limitations

| Feature | Status | Notes |
|---------|--------|-------|
| Core workflow logic | ✅ Works | If uploaded as project knowledge |
| Depth adaptation | ✅ Works | — |
| On-demand file loading | ❌ No | Must pre-upload all detail files |
| Template output | ⚠️ Chat only | Cannot write files to disk |
| State persistence | ❌ No | Cannot resume across sessions |
| Chain detection | ❌ No | No filesystem |
| AI-DWG workspace generation | ❌ No | Needs to create 30+ files |
| AI-GCE governance | ❌ No | Needs filesystem |
| Multi-package coexistence | ⚠️ Awkward | One project per package works best |

### When to Use claude.ai

- Quick exploration of a single workflow (AI-PILC or AI-ILC) in conversation mode
- Getting professional advice without needing file output
- Trying out a package before committing to Claude Code installation

### When to Use Claude Code Instead

- Any real project work (you need the file outputs)
- Multi-package workflows (chain handoffs require state files)
- AI-DWG, AI-GCE, AI-TGE (require filesystem)
- Any scenario where you want to resume across sessions

---

## Coexistence with Other Rules

AI-* package files coexist peacefully with your existing Claude configuration:

- **Existing `CLAUDE.md`**: Preserved. If you already have one, the installer only **appends** a marker-guarded import block (`@CLAUDE_PDLC_ORCHESTRATOR.md`); your content is untouched and uninstall strips just that block. If you have none, the installer creates a minimal `CLAUDE.md` and uninstall removes it.
- **Existing `.claude/rules/`**: Untouched. The installer uses a root `CLAUDE.md` import + on-demand `Read` by default.
- **Other project files**: Never modified. Only AI-* steering files (and the `CLAUDE.md` import block) are added.
- **Package isolation**: Each package is `Read` ONLY when you invoke it by name. Dormant packages are not loaded and consume no context.

### If You Want Everything In CLAUDE.md Instead

Some users prefer to inline the orchestrator directly into `CLAUDE.md` rather than using an `@import`. You can concatenate it:

```powershell
# Inline the orchestrator into CLAUDE.md (instead of the @import)
$header = "# AI-* PDLC Family Steering`n`nThis workspace uses AIFLC packages.`n`n---`n"
$header | Out-File "<your-project-path>\CLAUDE.md" -Encoding utf8
Get-Content "<your-project-path>\CLAUDE_PDLC_ORCHESTRATOR.md" | Add-Content "<your-project-path>\CLAUDE.md"
```

> **Trade-off:** Inlining is marginally simpler, but the `@import` keeps `CLAUDE.md` clean and lets you update the orchestrator without touching your own instructions. Either way, package cores stay in `.aiflc/pdlc/` and are read on demand — never inlined into `CLAUDE.md`.

---

## Uninstalling

### Via Installer

```powershell
# Windows
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall
```

```bash
# macOS/Linux
./installer/install.sh --target <your-project-path> --uninstall
```

The installer reads `.ai-family-manifest.json` and removes exactly what it installed.

### Manual Removal

```powershell
# Remove the root orchestrator and strip its @import from CLAUDE.md
Remove-Item "<your-project-path>\CLAUDE_PDLC_ORCHESTRATOR.md" -ErrorAction SilentlyContinue
# (If you kept your own CLAUDE.md, delete the line "@CLAUDE_PDLC_ORCHESTRATOR.md" from it)

# Remove the generated slash commands
Remove-Item "<your-project-path>\.claude\commands\pdlc" -Recurse -Force -ErrorAction SilentlyContinue

# Remove all package cores + rule-details from the uniform home
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory | Remove-Item -Recurse -Force
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force

# Remove the manifest (lives under pdlc-ws/)
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue

# Remove installed family tools (extensions)
Remove-Item "<your-project-path>\pdlc-ws\tools\extensions" -Recurse -Force -ErrorAction SilentlyContinue

# Remove runtime outputs if you want a clean slate (this deletes all generated work — back up first)
# Remove-Item "<your-project-path>\pdlc-ws" -Recurse -Force -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Claude doesn't recognize the package | Orchestrator not loaded | Verify root `CLAUDE.md` exists and contains `@CLAUDE_PDLC_ORCHESTRATOR.md` (outside any code fence). Run `/memory` to confirm both `CLAUDE.md` and the orchestrator are loaded. Then activate a package (e.g. `_PILC_`) so the orchestrator `Read`s `.aiflc/pdlc/ai-pilc-rules/core-workflow.md`. |
| "Can't find rule-details" | Path mismatch | The core workflow checks `.aiflc/pdlc/{pkg}-rule-details/` first. Ensure `.aiflc/pdlc/ai-{pkg}-rule-details/` exists. |
| No welcome message | Wrong activation phrase | Use the exact format: "Using AI-PILC, ..." (uppercase package name) |
| State file not created | First interaction only | State is created after the first stage completes, not immediately |
| Chain detection not working | Upstream state file missing | Run packages in order. If AI-ADLC can't find PILC output, verify `pilc-state.md` exists |
| Context window getting large | — | Only the orchestrator loads at session start, so this is rare. If it happens, ensure package cores are under `.aiflc/pdlc/` and not pinned in `.claude/rules/` |
| Claude Code not reading files | Working directory wrong | Ensure you launched `claude` from your project root (where `CLAUDE.md` and `.aiflc/pdlc/` are) |
| Installer "source not found" | Package folder missing | Verify `ai-{package}/` exists in your AIPDLC clone |

### Getting Help

If something doesn't work:
1. Run the installer with `-DryRun` to see expected file paths
2. Check that your AIPDLC clone contains the `ai-{package}/` folders
3. Verify Claude Code version is current (`claude --version`)

---

## Platform Capabilities Summary

| Feature | Claude Code | claude.ai (Projects) |
|---------|:-----------:|:--------------------:|
| Core workflow execution | ✅ Full | ✅ If uploaded |
| On-demand file loading | ✅ Automatic | ❌ Manual pre-upload |
| Deliverable file output | ✅ Writes to disk | ⚠️ Chat output only |
| State persistence | ✅ Across sessions | ❌ Single session |
| Chain marker detection | ✅ Automatic | ❌ Not possible |
| Multi-package install | ✅ All 11 | ⚠️ One per project |
| AI-DWG workspace gen | ✅ Full (30+ files) | ❌ Not possible |
| AI-GCE rule generation | ✅ Full | ❌ Not possible |
| AI-GCE hook enforcement | ❌ (Kiro only) | ❌ |
| Depth adaptation | ✅ | ✅ |
| Session continuity | ✅ Cold resume | ❌ |

**Bottom line:** Use **Claude Code** for real project work. Use **claude.ai** only for quick exploration or when Claude Code isn't available.

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
