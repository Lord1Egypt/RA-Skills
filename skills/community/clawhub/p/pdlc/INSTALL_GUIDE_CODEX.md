# AI-* Family — Complete Installation Guide for OpenAI Codex

**Applies to:** OpenAI Codex CLI — full workflow support with `AGENTS.md` integration.

> **Why Codex?** Codex CLI is a sandboxed coding agent with full workspace file access. It reads `AGENTS.md` files automatically at every session start, supports on-demand file reading, and writes deliverables to disk. All workflow packages, generators, and governance rule generation work at 100%. Only AI-GCE hook auto-execution is unavailable (Kiro-only).

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
- [AI-GCE Governance on Codex](#ai-gce-governance-on-codex)
- [Session Continuity](#session-continuity)
- [Coexistence with Other Instructions](#coexistence-with-other-instructions)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **OpenAI Codex CLI** | Installed and authenticated (`npm install -g @openai/codex`) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Python, Docker, or any additional runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

The installer places **one always-loaded file** plus the **package home**, both scoped to the AI-* PDLC Family (multiple AIFLC families can coexist in one workspace):

1. **Session orchestrator** — the orchestrator placed in the root `AGENTS.md` that Codex reads automatically at every session start. It is the ONLY always-loaded file. It detects which package you want and `Read`s that package's core on demand — keeping the context window free.
2. **Package home** — every package's core AND rule-details live together in the uniform, agent-neutral home `.aiflc/pdlc/`. Nothing here auto-loads; the orchestrator reads from it on demand.

```
your-workspace/
├── AGENTS.md                      ← The ONLY always-loaded file (orchestrator; routes to cores)
├── .aiflc/
│   └── pdlc/                      ← AI-* PDLC Family home (cores + rule-details + fabric)
│       ├── ai-pilc-rules/core-workflow.md    ← Read on demand by the orchestrator
│       ├── ai-pilc-rule-details/             ← Read on demand by the core
│       │   ├── common/  inception/  assessment/  templates/  ...
│       └── ... one {pkg}-rules/ + {pkg}-rule-details/ per installed package
├── pdlc-ws/                       ← All runtime outputs land here (never workspace root)
└── (your project files)
```

Codex reads `AGENTS.md` at the workspace root on every session start. The family places the compact orchestrator there; when you activate a package (by key or intent), the orchestrator `Read`s `.aiflc/pdlc/ai-{pkg}-rules/core-*.md`, and the core reads its rule-details from `.aiflc/pdlc/ai-{pkg}-rule-details/` as each phase needs them.

> **The AIFLC model:** one orchestrator loads always-on (root `AGENTS.md`); every package core + its rule-details live in the uniform home `.aiflc/pdlc/` and are read on demand; and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Method 1: Automated Installer (Recommended)

The interactive installer handles all file placement automatically.

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive (asks platform, packages, target)
.\installer\install.ps1

# Option B: One-liner for Codex with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Codex
./installer/install.sh --target <your-project-path> --platform codex --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform codex --bundle full
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
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Bundle full -DryRun
```

---

## Method 2: Manual Installation

### Single Package Example (AI-PILC)

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Place the orchestrator as the root AGENTS.md (Codex reads this automatically)
Copy-Item "$Source\session-orchestrator.md" "$Target\AGENTS.md"

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Place the orchestrator as the root AGENTS.md
cp "$SOURCE/session-orchestrator.md" "$TARGET/AGENTS.md"

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
mkdir -p "$TARGET/.aiflc/pdlc"
cp -R "$SOURCE/ai-pilc/ai-pilc-rules" "$TARGET/.aiflc/pdlc/"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details" "$TARGET/.aiflc/pdlc/"
```

### Multi-Package Manual Install

Add more packages by copying their cores + rule-details into the same uniform home. The root `AGENTS.md` orchestrator stays as-is — it routes to whichever cores are present:

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Orchestrator at root (once)
Copy-Item "$Source\session-orchestrator.md" "$Target\AGENTS.md" -Force

# Uniform home
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"

# Install AI-PILC + AI-ADLC + AI-DWG (cores + rule-details) into .aiflc/pdlc/
foreach ($pkg in @("ai-pilc", "ai-adlc", "ai-dwg")) {
    Copy-Item -Recurse "$Source\$pkg\$pkg-rules" "$Target\.aiflc\pdlc\" -Force
    Copy-Item -Recurse "$Source\$pkg\$pkg-rule-details" "$Target\.aiflc\pdlc\" -Force
}
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Orchestrator at root (once)
cp "$SOURCE/session-orchestrator.md" "$TARGET/AGENTS.md"

# Uniform home
mkdir -p "$TARGET/.aiflc/pdlc"

# Install AI-PILC + AI-ADLC + AI-DWG (cores + rule-details) into .aiflc/pdlc/
for pkg in ai-pilc ai-adlc ai-dwg; do
    cp -R "$SOURCE/$pkg/${pkg}-rules" "$TARGET/.aiflc/pdlc/"
    cp -R "$SOURCE/$pkg/${pkg}-rule-details" "$TARGET/.aiflc/pdlc/"
done
```

### File Placement Convention (Codex)

The orchestrator is the only always-loaded file (root `AGENTS.md`). Every package core + its rule-details live in the uniform home `.aiflc/pdlc/`, read on demand.

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

---

## Multi-Package Installation

### Installing All 11 Packages (Full Chain)

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform codex -Bundle full
```

Or manually:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Uniform home for all cores + rule-details
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc" | Out-Null

$packages = @(
    "ai-ilc", "ai-pilc", "ai-ppm", "ai-flo", "ai-adlc",
    "ai-uxd", "ai-polc", "ai-dwg", "ai-gce", "ai-tge", "ai-dfe"
)

# Copy every package core + rule-details into the uniform home
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

# Place the single always-loaded orchestrator at the workspace root
Copy-Item "$Source\session-orchestrator.md" "$Target\AGENTS.md" -Force
Write-Host "Installed session orchestrator (AGENTS.md)" -ForegroundColor Green
```

### Context Window Consideration

Codex loads only the root `AGENTS.md` (the orchestrator) at session start — not the package cores. With 11 packages installed:

- **The orchestrator is compact** — it routes by intent and `Read`s exactly one package core from `.aiflc/pdlc/` when you activate it.
- **Package cores stay dormant** in `.aiflc/pdlc/` until invoked (each is orchestration logic, 1–3 KB), so installing all 11 costs nothing at session start.
- **The AI activates only one package at a time** — the others are dormant until you invoke them.

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
├── AGENTS.md                            ← The ONLY always-loaded file (orchestrator; routes to cores)
├── .aiflc/
│   └── pdlc/                            ← AI-* PDLC Family home (cores + rule-details, on-demand)
│       ├── ai-ilc-rules/core-workflow.md
│       ├── ai-ilc-rule-details/            ← idea lifecycle details
│       ├── ai-pilc-rules/core-workflow.md
│       ├── ai-pilc-rule-details/           ← project initiation details
│       │   ├── common/
│       │   ├── inception/
│       │   ├── assessment/
│       │   ├── justification/
│       │   ├── authorization/
│       │   ├── planning/
│       │   ├── mobilization/
│       │   └── templates/
│       ├── ai-ppm-rules/core-engine.md
│       ├── ai-ppm-rule-details/            ← portfolio management details
│       ├── ai-flo-rules/core-engine.md
│       ├── ai-flo-rule-details/            ← flow routing details
│       ├── ai-adlc-rules/core-workflow.md
│       ├── ai-adlc-rule-details/           ← architecture design details
│       ├── ai-uxd-rules/core-workflow.md
│       ├── ai-uxd-rule-details/            ← UX design details
│       ├── ai-polc-rules/core-workflow.md
│       ├── ai-polc-rule-details/           ← product ownership details
│       ├── ai-dwg-rules/core-generator.md
│       ├── ai-dwg-rule-details/            ← workspace generation details
│       ├── ai-gce-rules/core-generator.md
│       ├── ai-gce-rule-details/            ← governance engine details
│       ├── ai-tge-rules/core-engine.md
│       ├── ai-tge-rule-details/            ← test governance details
│       ├── ai-dfe-rules/core-engine.md
│       └── ai-dfe-rule-details/            ← data fabric details
├── pdlc-ws/                             ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   ├── .ai-family-manifest.json         ← Installer tracking (for uninstall)
│   └── tools/                           ← Family tools (visual tools / extensions)
│       └── extensions/
│           ├── AIFLC-PDLC-Dashboard/    ← HTML dashboard + .vsix (reads ../../data/ via AI-DFE)
│           └── AIFLC-CommandBoard/      ← Trigger palette (HTML + .vsix)
└── (your project files)
```

> **Note:** The `.aiflc/pdlc/` home is dot-prefixed (hidden) and won't clutter your project view in most file explorers.

---

## Verification

After installation, verify everything is working:

### Step 1: Confirm files are in place

```powershell
# Windows
Get-ChildItem "<your-project-path>\AGENTS.md"
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory
```

```bash
# macOS/Linux
ls <your-project-path>/AGENTS.md
ls -d <your-project-path>/.aiflc/pdlc/ai-*-rules/
ls -d <your-project-path>/.aiflc/pdlc/ai-*-rule-details/
```

### Step 2: Start Codex in your workspace

```bash
# Navigate to your project
cd <your-project-path>

# Start Codex CLI
codex
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

**Expected:** Codex should respond with the package's welcome message and begin the structured workflow, asking about depth level and presenting the first stage.

### Step 4: Verify on-demand loading

During a workflow, when Codex transitions to a new phase, it reads the corresponding rule-details file. You'll see file-read operations in Codex's output referencing paths like `.aiflc/pdlc/ai-pilc-rule-details/inception/stage-01-...`.

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell Codex which package to use with the activation phrase
2. **Choose depth:** The package asks if you want Minimal, Standard, or Comprehensive output
3. **Work through stages:** Each package has defined stages. Codex guides you through them sequentially
4. **Approve at gates:** At the end of each stage, Codex presents output and waits for your approval before proceeding
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

Codex will respond with the AI-PILC welcome, ask about depth, then walk you through 6 phases / 16 stages producing professional deliverables at each gate.

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

---

## AI-GCE Governance on Codex

AI-GCE generates all governance files correctly on Codex, but enforcement is advisory rather than automatic:

### What Works (100%)

- Rule generation (`.governance/rules/`) — full mode 1/2/3/4
- Compliance documentation
- Brownfield baseline scanning
- Hook and agent file generation (structurally valid but inert)

### What Doesn't Work (Kiro-only features)

| Feature | Why | Workaround |
|---------|-----|------------|
| Hook auto-execution | No event bus in Codex | Add governance rules to root `AGENTS.md` |
| Agent shortcut triggers | No `.kiro/agents/` runtime | Paste agent prompts manually when needed |
| Automatic compliance logging | Triggered by hooks | Ask Codex to log manually |
| Re-derivation auto-trigger | Requires file-edit events | Say "re-derive governance" manually |

### Best Practice: Maximizing Governance Value

After AI-GCE generates your governance layer, append this to your root `AGENTS.md`:

```markdown
## Governance Rules (Always Enforce)

The following rules from `.governance/rules/` apply to ALL work in this workspace.
Check compliance on every file you create or modify.

- See: .governance/rules/security-rules.md (CRITICAL)
- See: .governance/rules/architecture-rules.md
- See: .governance/rules/naming-conventions.md
- See: .governance/COMPLIANCE_README.md for full rule index
```

Then periodically ask Codex: "Run a compliance check against `.governance/rules/` on recent changes."

This gives you ~70% of Kiro's enforcement value through advisory compliance.

---

## Session Continuity

Each workflow package maintains a **state file** (e.g., `pilc-state.md`) that records:
- Current phase and stage
- Completed stages
- Pending decisions
- Selected depth level
- Key outputs produced

**This means you can close Codex and resume later.** When you start a new session and say "Continue AI-PILC", Codex reads the state file and picks up exactly where you left off.

> **Important:** Don't delete state files unless you want to restart a workflow from scratch.

---

## Coexistence with Other Instructions

AI-* package files coexist peacefully with your existing Codex configuration:

- **Existing `AGENTS.md`**: The installer merges or appends the orchestrator block to your existing file (never overwrites without asking).
- **Existing subdirectory `AGENTS.md` files**: Untouched. Package cores live under `.aiflc/pdlc/`, not in subdirectory `AGENTS.md` files.
- **Other project files**: Never modified. Only AI-* steering files are added.
- **Package isolation**: Each package activates ONLY when you invoke it by name. Dormant packages don't interfere.

### Approval Mode Compatibility

Codex's sandbox and approval modes work transparently with AI-* packages:

| Mode | Compatibility |
|------|--------------|
| `suggest` (default) | ✅ Full — Codex proposes file writes, you approve |
| `auto-edit` | ✅ Full — file writes happen automatically |
| `full-auto` | ✅ Full — entire workflow runs hands-free |

> **Recommendation:** Use `auto-edit` or default `suggest` mode for your first run so you can see what each stage produces before it writes to disk.

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
# Remove all package cores + rule-details from the uniform home
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory | Remove-Item -Recurse -Force
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force

# Remove the manifest (lives under pdlc-ws/)
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue

# Remove installed family tools (extensions)
Remove-Item "<your-project-path>\pdlc-ws\tools\extensions" -Recurse -Force -ErrorAction SilentlyContinue

# Remove runtime outputs if you want a clean slate (this deletes all generated work — back up first)
# Remove-Item "<your-project-path>\pdlc-ws" -Recurse -Force -ErrorAction SilentlyContinue

# Remove or revert root AGENTS.md (if you had a pre-existing one, restore from git)
Remove-Item "<your-project-path>\AGENTS.md" -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Codex doesn't recognize the package | Root `AGENTS.md` missing or not the orchestrator | Verify `AGENTS.md` exists at workspace root and contains the session orchestrator |
| Package core not found | Path mismatch | Verify `.aiflc/pdlc/ai-{pkg}-rules/core-*.md` exists |
| "Can't find rule-details" | Path mismatch | Core resolves `.aiflc/pdlc/ai-{pkg}-rule-details/` first |
| No welcome message | Wrong activation phrase | Use the exact format: "Using AI-PILC, ..." (uppercase package name) |
| State file not created | First interaction only | State is created after the first stage completes, not immediately |
| Chain detection not working | Upstream state file missing | Run packages in order. Verify `pilc-state.md` exists before running AI-ADLC |
| Sandbox blocks file writes | Restrictive sandbox mode | Use `--sandbox workspace-write` or `auto-edit` mode |
| Codex not reading subdirectory AGENTS.md | Version-dependent behavior | Use the concatenated single-file approach instead (see Alternative above) |
| Context window getting large | Too many packages loaded | Remove packages you don't actively need |

---

## Platform Capabilities Summary

| Feature | Codex CLI |
|---------|:---------:|
| Core workflow execution | ✅ |
| On-demand file loading | ✅ |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ✅ All 11 |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ❌ (Kiro only) |
| Agent shortcut triggers | ❌ (Kiro only) |
| Automatic compliance logging | ⚠️ Manual |
| Depth adaptation | ✅ |
| Session continuity | ✅ Cold resume |

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
