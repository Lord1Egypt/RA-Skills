# AI-* Family — Complete Installation Guide for Cline

**Applies to:** Cline (VS Code extension) — full workflow support with `.clinerules/` integration.

> **Why Cline?** Cline reads workspace rules from `.clinerules/` and has full file system access. All workflow packages, generators, and governance rule generation work at 100%. Only AI-GCE hook auto-execution is unavailable (Kiro-only).

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
- [AI-GCE Governance on Cline](#ai-gce-governance-on-cline)
- [Session Continuity](#session-continuity)
- [Coexistence with Other Rules](#coexistence-with-other-rules)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Cline** | VS Code extension installed ([marketplace](https://marketplace.visualstudio.com/items?itemName=saoudrizwan.claude-dev)) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

The installer places **one always-loaded file** plus the **package home**, both scoped to the AI-* PDLC Family (multiple AIFLC families can coexist in one workspace):

1. **Session orchestrator** — a single Markdown file Cline reads automatically at session start (placed in `.clinerules/pdlc-session-orchestrator.md`). It is the ONLY always-loaded file. It detects which package you want and `Read`s that package's core on demand — keeping the context window free.
2. **Package home** — every package's core AND rule-details live together in the uniform, agent-neutral home `.aiflc/pdlc/`. Nothing here auto-loads; the orchestrator reads from it on demand.

```
your-workspace/
├── .clinerules/
│   └── pdlc-session-orchestrator.md   ← The ONLY always-loaded file (routes to cores)
├── .aiflc/
│   └── pdlc/                          ← AI-* PDLC Family home (cores + rule-details + fabric)
│       ├── ai-pilc-rules/core-workflow.md    ← Read on demand by the orchestrator
│       ├── ai-pilc-rule-details/             ← Read on demand by the core
│       │   ├── common/  inception/  assessment/  templates/  ...
│       └── ... one {pkg}-rules/ + {pkg}-rule-details/ per installed package
├── pdlc-ws/                           ← All runtime outputs land here (never workspace root)
└── (your project files)
```

Cline reads all Markdown files in `.clinerules/` at session start — the family places exactly one there: `pdlc-session-orchestrator.md`. When you activate a package (by key or intent), the orchestrator `Read`s `.aiflc/pdlc/ai-{pkg}-rules/core-*.md`, and the core reads its rule-details from `.aiflc/pdlc/ai-{pkg}-rule-details/` as each phase needs them.

> **The AIFLC model:** one orchestrator loads always-on (`.clinerules/pdlc-session-orchestrator.md`); every package core + its rule-details live in the uniform home `.aiflc/pdlc/` and are read on demand; and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Method 1: Automated Installer (Recommended)

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive
.\installer\install.ps1

# Option B: One-liner for Cline with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cline -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cline -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Cline
./installer/install.sh --target <your-project-path> --platform cline --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform cline --bundle full
```

### Preset Bundles

| Bundle | Command Flag | Packages | Best For |
|--------|-------------|----------|----------|
| **Greenfield Full** | `-Bundle full` | AI-ILC + AI-PILC + AI-PPM + AI-FLO + AI-POLC + AI-UXD + AI-ADLC + AI-DWG + AI-GCE + AI-TGE + AI-DFE | New project, complete family |
| **Greenfield Minimal** | `-Bundle minimal` | AI-PILC + AI-ADLC + AI-DWG | Quick start, architecture focus |
| **Architecture Focus** | `-Bundle arch` | AI-ADLC + AI-DWG + AI-GCE | Architecture → workspace → governance |
| **Governance Only** | `-Bundle governance` | AI-GCE + AI-TGE | Existing project, add compliance |
| **Portfolio** | `-Bundle portfolio` | AI-ILC + AI-PILC + AI-PPM + AI-FLO | Multi-project management |

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

# Copy the session orchestrator into Cline's auto-load slot (the ONLY always-loaded file)
New-Item -ItemType Directory -Force -Path "$Target\.clinerules"
Copy-Item "$Source\session-orchestrator.md" "$Target\.clinerules\pdlc-session-orchestrator.md"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
mkdir -p "$TARGET/.aiflc/pdlc"
cp -R "$SOURCE/ai-pilc/ai-pilc-rules" "$TARGET/.aiflc/pdlc/"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details" "$TARGET/.aiflc/pdlc/"

# Copy the session orchestrator into Cline's auto-load slot (the ONLY always-loaded file)
mkdir -p "$TARGET/.clinerules"
cp "$SOURCE/session-orchestrator.md" "$TARGET/.clinerules/pdlc-session-orchestrator.md"
```

### File Placement Convention (Cline)

Cores and rule-details both live in the uniform home `.aiflc/pdlc/` (read on demand). The only always-loaded file is `.clinerules/pdlc-session-orchestrator.md`.

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

### Installing All 11 Packages

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cline -Bundle full
```

Or manually:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Ensure the uniform home and Cline's rules slot exist
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc" | Out-Null
New-Item -ItemType Directory -Force -Path "$Target\.clinerules" | Out-Null

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

# Copy the single always-loaded orchestrator into Cline's slot
Copy-Item "$Source\session-orchestrator.md" "$Target\.clinerules\pdlc-session-orchestrator.md" -Force
Write-Host "Installed session orchestrator" -ForegroundColor Green
```

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

---

## Resulting Workspace Structure

After a full install:

```
your-project/
├── .clinerules/
│   └── pdlc-session-orchestrator.md     ← The ONLY always-loaded file (routes to cores)
├── .aiflc/
│   └── pdlc/                            ← AI-* PDLC Family home (cores + rule-details, on-demand)
│       ├── ai-ilc-rules/core-workflow.md
│       ├── ai-ilc-rule-details/
│       ├── ai-pilc-rules/core-workflow.md
│       ├── ai-pilc-rule-details/
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
├── pdlc-ws/                             ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   └── .ai-family-manifest.json         ← Installer tracking
└── (your project files)
```

---

## Verification

1. Open your workspace in VS Code with Cline extension active
2. Start a new Cline chat
3. Type: "Using AI-PILC, initiate a project"
4. **Expected:** The AI responds with the package's welcome message and begins the structured workflow

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell the AI which package to use with the activation phrase
2. **Choose depth:** Minimal, Standard, or Comprehensive
3. **Work through stages:** The AI guides you sequentially
4. **Approve at gates:** Output presented for approval before proceeding
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk)

---

## Chain Handoffs Between Packages

Packages detect each other through **state marker files** (e.g., `pilc-state.md`). Run packages sequentially and they find each other's output automatically.

---

## AI-GCE Governance on Cline

AI-GCE generates all governance files correctly, but enforcement is advisory:

| Feature | Status | Workaround |
|---------|--------|------------|
| Rule generation | ✅ Works | — |
| Hook auto-execution | ❌ | Add a governance rule file in `.clinerules/` |
| Agent triggers | ❌ | Paste agent prompts manually |
| Compliance logging | ⚠️ Manual | Ask the AI to log checks |

### Best Practice

After AI-GCE generates governance, add a summary file:

```bash
cp .governance/COMPLIANCE_README.md .clinerules/governance-rules.md
```

This ensures Cline always has the governance context loaded.

---

## Session Continuity

State files persist between sessions. Say "Continue AI-PILC" to resume where you left off.

---

## Coexistence with Other Rules

- **Existing `.clinerules/`**: Untouched. The family adds only one file (`pdlc-session-orchestrator.md`) alongside yours; package cores live under `.aiflc/pdlc/`.
- **Other project files**: Never modified.

---

## Uninstalling

```powershell
# Via installer
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall

# Manual
Remove-Item "<your-project-path>\.clinerules\pdlc-session-orchestrator.md" -ErrorAction SilentlyContinue
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory | Remove-Item -Recurse -Force
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Orchestrator not loading | Cline not reading `.clinerules/` | Verify `.clinerules/pdlc-session-orchestrator.md` exists and is `.md` |
| Package core not found | Path mismatch | Verify `.aiflc/pdlc/ai-{pkg}-rules/core-*.md` exists |
| "Can't find rule-details" | Path mismatch | Core resolves `.aiflc/pdlc/ai-{pkg}-rule-details/` first |
| No welcome message | Wrong activation phrase | Use "Using AI-PILC, ..." format |
| State file not created | First interaction only | State is created after first stage completes |

---

## Platform Capabilities Summary

| Feature | Cline |
|---------|:-----:|
| Core workflow execution | ✅ |
| On-demand file loading | ✅ |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ✅ All 11 |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ❌ (Kiro only) |
| Depth adaptation | ✅ |
| Session continuity | ✅ Cold resume |

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
