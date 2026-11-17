# AI-* Family — Complete Installation Guide for Kiro

**Applies to:** Kiro IDE (VS Code-based) — the primary platform with full feature support including hooks, agents, and auto-enforcement.

> **Why Kiro?** Kiro is the only platform that supports ALL AI-* Family features at 100%, including AI-GCE hook auto-execution, agent shortcut triggers, automatic compliance logging, and event-driven governance. Every other platform gets the workflow logic but misses the real-time enforcement layer.

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
- [AI-GCE Governance on Kiro](#ai-gce-governance-on-kiro)
- [Session Continuity](#session-continuity)
- [Coexistence with Other Steering](#coexistence-with-other-steering)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Kiro IDE** | Installed ([kiro.dev](https://kiro.dev)) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

The installer places **one always-loaded file** plus the **package home**, both scoped to the AI-* PDLC Family (multiple AIFLC families can coexist in one workspace):

1. **Session orchestrator** — a single steering file Kiro reads automatically at session start (placed in `.kiro/steering/session-orchestrator.md`). It is the ONLY always-loaded file. It detects which package you want and `Read`s that package's core on demand — keeping the context window free.
2. **Package home** — every package's core AND rule-details live together in the uniform, agent-neutral home `.aiflc/pdlc/`. Nothing here auto-loads; the orchestrator reads from it on demand.

```
your-workspace/
├── .kiro/
│   └── steering/
│       └── session-orchestrator.md       ← The ONLY always-loaded file (routes to cores)
├── .aiflc/
│   └── pdlc/                              ← AI-* PDLC Family home (cores + rule-details + fabric)
│       ├── ai-pilc-rules/core-workflow.md    ← Read on demand by the orchestrator
│       ├── ai-pilc-rule-details/             ← Read on demand by the core
│       │   ├── common/  inception/  assessment/  templates/  ...
│       └── ... one {pkg}-rules/ + {pkg}-rule-details/ per installed package
├── pdlc-ws/                              ← All runtime outputs land here (never workspace root)
└── (your project files)
```

Kiro auto-loads only `session-orchestrator.md` from `.kiro/steering/`. When you activate a package (by key or intent), the orchestrator `Read`s `.aiflc/pdlc/ai-{pkg}-rules/core-*.md`, and the core reads its rule-details from `.aiflc/pdlc/ai-{pkg}-rule-details/` as each phase needs them.

> **The AIFLC model:** one orchestrator loads always-on (`.kiro/steering/`); every package core + its rule-details live in the uniform home `.aiflc/pdlc/` and are read on demand; and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Method 1: Automated Installer (Recommended)

The interactive installer handles all file placement automatically.

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive (asks platform, packages, target)
.\installer\install.ps1

# Option B: One-liner for Kiro with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform kiro -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform kiro -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Kiro
./installer/install.sh --target <your-project-path> --platform kiro --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform kiro --bundle full
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
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform kiro -Bundle full -DryRun
```

---

## Method 2: Manual Installation

### Single Package Example (AI-PILC)

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"

# Copy the session orchestrator into Kiro's auto-load slot (the ONLY always-loaded file)
New-Item -ItemType Directory -Force -Path "$Target\.kiro\steering"
Copy-Item "$Source\session-orchestrator.md" "$Target\.kiro\steering\session-orchestrator.md"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
mkdir -p "$TARGET/.aiflc/pdlc"
cp -R "$SOURCE/ai-pilc/ai-pilc-rules" "$TARGET/.aiflc/pdlc/"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details" "$TARGET/.aiflc/pdlc/"

# Copy the session orchestrator into Kiro's auto-load slot (the ONLY always-loaded file)
mkdir -p "$TARGET/.kiro/steering"
cp "$SOURCE/session-orchestrator.md" "$TARGET/.kiro/steering/session-orchestrator.md"
```

### File Placement Convention

Cores and rule-details both live in the uniform home `.aiflc/pdlc/` (read on demand). The only always-loaded file is `.kiro/steering/session-orchestrator.md`.

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
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform kiro -Bundle full
```

Or manually:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Ensure base directories exist
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc" | Out-Null
New-Item -ItemType Directory -Force -Path "$Target\.kiro\steering" | Out-Null

# The single always-loaded orchestrator (in Kiro's auto-load slot)
Copy-Item "$Source\session-orchestrator.md" "$Target\.kiro\steering\session-orchestrator.md" -Force

$packages = @(
    "ai-ilc", "ai-pilc", "ai-ppm", "ai-flo", "ai-adlc",
    "ai-uxd", "ai-polc", "ai-dwg", "ai-gce", "ai-tge", "ai-dfe"
)

foreach ($pkg in $packages) {
    $rulesSource = Join-Path $Source "$pkg\$pkg-rules"
    $detailsSource = Join-Path $Source "$pkg\$pkg-rule-details"

    # Core + rule-details both go into the uniform home .aiflc/pdlc/ (read on demand)
    if (Test-Path $rulesSource) {
        Copy-Item -Recurse $rulesSource "$Target\.aiflc\pdlc\" -Force
        Write-Host "Core installed: $pkg" -ForegroundColor Green
    }
    if (Test-Path $detailsSource) {
        Copy-Item -Recurse $detailsSource "$Target\.aiflc\pdlc\" -Force
        Write-Host "Details installed: $pkg" -ForegroundColor Green
    }
}
```

### Context Window Consideration

Kiro auto-loads only `session-orchestrator.md` from `.kiro/steering/` — a single small file — no matter how many packages you install. Package cores live in `.aiflc/pdlc/` and are read on demand, so they cost zero context until activated:

- **Install as many packages as you like** — only the orchestrator is always in context; the 11 cores never all load at once.
- **The AI activates only one package at a time** — the orchestrator `Read`s that package's core when you invoke it; the others stay on disk, dormant.
- **Heavy detail is deferred** — rule-details load per phase, only when the active workflow needs them.

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
├── .kiro/
│   ├── steering/
│   │   └── session-orchestrator.md      ← The ONLY always-loaded file (routes to cores)
│   └── hooks/                           ← Generated by AI-GCE (auto-executed on Kiro)
├── .aiflc/
│   └── pdlc/                            ← AI-* PDLC Family home (cores + rule-details, read on demand)
│       ├── ai-ilc-rules/core-workflow.md
│       ├── ai-ilc-rule-details/
│       ├── ai-pilc-rules/core-workflow.md
│       ├── ai-pilc-rule-details/
│       │   ├── common/  inception/  assessment/  justification/
│       │   ├── authorization/  planning/  mobilization/  templates/
│       ├── ai-ppm-rules/core-engine.md         · ai-ppm-rule-details/
│       ├── ai-flo-rules/core-engine.md         · ai-flo-rule-details/
│       ├── ai-adlc-rules/core-workflow.md      · ai-adlc-rule-details/
│       ├── ai-uxd-rules/core-workflow.md       · ai-uxd-rule-details/
│       ├── ai-polc-rules/core-workflow.md      · ai-polc-rule-details/
│       ├── ai-dwg-rules/core-generator.md      · ai-dwg-rule-details/
│       ├── ai-gce-rules/core-generator.md      · ai-gce-rule-details/
│       ├── ai-tge-rules/core-engine.md         · ai-tge-rule-details/
│       ├── ai-dfe-rules/core-engine.md         · ai-dfe-rule-details/
│       └── FAMILY_BINDINGS.md · GATE_PROTOCOL.md · FAMILY_INTERFACE.md · TRIGGER_KEYS_REFERENCE.md  (fabric)
├── pdlc-ws/                             ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   ├── .ai-family-manifest.json         ← Installer tracking (for uninstall)
│   └── tools/                           ← Family tools (visual tools / extensions)
│       └── extensions/
│           ├── AIFLC-PDLC-Dashboard/    ← HTML dashboard + .vsix (reads ../../data/ via AI-DFE)
│           └── AIFLC-CommandBoard/      ← Trigger palette (HTML + .vsix)
└── (your project files)
```

---

## Verification

### Step 1: Open the Steering Files panel

1. Open your workspace in Kiro IDE
2. Open the **Steering Files** panel (sidebar)
3. Confirm each installed package's core file appears under **Workspace** as always-active

### Step 2: Test activation

Start a new chat and type:

```
Using AI-PILC, initiate a project from this requirement: [paste your requirement]
```

**Expected:** Kiro should respond with the package's welcome message and begin the structured workflow, asking about depth level and presenting the first stage.

### Step 3: Verify on-demand loading

During a workflow, when the AI transitions to a new phase, it reads the corresponding rule-details file automatically. You can confirm this in the conversation — the AI mentions loading phase-specific instructions.

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell the AI which package to use with the activation phrase
2. **Choose depth:** The package asks if you want Minimal, Standard, or Comprehensive output
3. **Work through stages:** Each package has defined stages. The AI guides you sequentially
4. **Approve at gates:** At the end of each stage, the AI presents output and waits for your approval
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk as a file)

### Depth Levels

| Level | Output Volume | Best For |
|-------|--------------|----------|
| **Minimal** | Key essentials only | Prototypes, small projects, time-pressed |
| **Standard** | Professional baseline | Most projects (recommended default) |
| **Comprehensive** | Enterprise-grade detail | Regulated industries, large teams, audit-heavy |

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

## AI-GCE Governance on Kiro

Kiro is the **full-featured** platform for AI-GCE. Everything works natively:

| Feature | Status |
|---------|--------|
| Rule generation (`.governance/rules/`) | ✅ Native |
| Hook generation (`.kiro/hooks/`) | ✅ Native |
| **Hook auto-execution on file save** | ✅ Native |
| Agent generation (`.kiro/agents/`) | ✅ Native |
| **Agent shortcut triggers** | ✅ Native |
| Automatic compliance logging (JSONL) | ✅ Native |
| Tier auto-progression | ✅ Native |
| Re-derivation auto-trigger | ✅ Native |
| Brownfield baseline | ✅ Native |

### How It Works on Kiro

1. Run AI-GCE to generate the governance layer
2. Hooks are placed in `.kiro/hooks/` — Kiro reads them automatically
3. On every file save/create, relevant hooks fire and enforce rules
4. Agents in `.kiro/agents/` respond to shortcut triggers (e.g., `SDC__`)
5. Compliance is logged automatically to `.governance/compliance-log/`
6. Tiers activate progressively based on compliance state

**No extra setup needed beyond running AI-GCE.** The generated files are immediately active.

---

## Session Continuity

Each workflow package maintains a **state file** (e.g., `pilc-state.md`) that records:
- Current phase and stage
- Completed stages
- Pending decisions
- Selected depth level
- Key outputs produced

**This means you can close Kiro and resume later.** When you start a new session and say "Continue AI-PILC", the AI reads the state file and picks up exactly where you left off.

> **Important:** Don't delete state files unless you want to restart a workflow from scratch.

---

## Coexistence with Other Steering

AI-* package files coexist peacefully with your existing Kiro configuration:

- **Existing steering files**: Untouched. The installer adds only `session-orchestrator.md` to `.kiro/steering/`; all package cores + details go under `.aiflc/pdlc/`.
- **Existing hooks**: Untouched. AI-GCE adds hooks in `.kiro/hooks/` without modifying yours.
- **Other project files**: Never modified. Only AI-* steering files are added.
- **Package isolation**: Each package activates ONLY when you invoke it by name.

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

### Manual Removal

```powershell
# Remove the package home (cores + rule-details)
Remove-Item "<your-project-path>\.aiflc\pdlc" -Recurse -Force -ErrorAction SilentlyContinue

# Remove the session orchestrator
Remove-Item "<your-project-path>\.kiro\steering\session-orchestrator.md" -ErrorAction SilentlyContinue

# Remove the manifest (lives under pdlc-ws/)
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue

# Remove runtime outputs if you want a clean slate (this deletes all generated work — back up first)
# Remove-Item "<your-project-path>\pdlc-ws" -Recurse -Force -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Orchestrator not loading | Wrong location | Verify `.kiro/steering/session-orchestrator.md` exists (must sit directly in `.kiro/steering/`, not a subfolder) |
| Package core not found | Path mismatch | Verify `.aiflc/pdlc/ai-{pkg}-rules/core-*.md` exists |
| "Can't find rule-details" | Path mismatch | Core resolves `.aiflc/pdlc/ai-{pkg}-rule-details/` first |
| No welcome message | Wrong activation phrase | Use the exact format: "Using AI-PILC, ..." (uppercase package name) |
| Hooks not firing | AI-GCE not run yet | Run "Using AI-GCE, set up governance" to generate hooks |
| State file not created | First interaction only | State is created after the first stage completes |
| Chain detection not working | Upstream state file missing | Run packages in order |

---

## Platform Capabilities Summary

| Feature | Kiro |
|---------|:----:|
| Core workflow execution | ✅ |
| On-demand file loading | ✅ |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ✅ All 11 |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ✅ Native |
| Agent shortcut triggers | ✅ Native |
| Automatic compliance logging | ✅ Native |
| Depth adaptation | ✅ |
| Session continuity | ✅ Cold resume |

**Kiro is the only platform with 100% feature coverage.** All other platforms lack hook execution and agent triggers.

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
