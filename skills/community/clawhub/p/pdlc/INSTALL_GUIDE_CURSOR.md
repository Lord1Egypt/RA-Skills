# AI-* Family — Complete Installation Guide for Cursor

**Applies to:** Cursor IDE — full workflow support with `.cursor/rules/` integration.

> **Why Cursor?** Cursor supports workspace-level rules via `.cursor/rules/` with `.mdc` frontmatter for always-apply behavior. All workflow packages, generators, and governance rule generation work at 100%. Only AI-GCE hook auto-execution is unavailable (Kiro-only).

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
- [AI-GCE Governance on Cursor](#ai-gce-governance-on-cursor)
- [Session Continuity](#session-continuity)
- [Coexistence with Other Rules](#coexistence-with-other-rules)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **Cursor IDE** | Installed ([cursor.com](https://cursor.com)) |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

The installer places **one always-loaded file** plus the **package home**, both scoped to the AI-* PDLC Family (multiple AIFLC families can coexist in one workspace):

1. **Session orchestrator** — a single `.mdc` rule file with `alwaysApply: true` frontmatter in `.cursor/rules/pdlc-session-orchestrator.mdc`. It is the ONLY always-loaded file (and the only `.mdc` the family installs). Cursor loads it every session; it detects which package you want and `Read`s that package's core on demand — keeping the context window free.
2. **Package home** — every package's core AND rule-details live together in the uniform, agent-neutral home `.aiflc/pdlc/`. Nothing here auto-loads; the orchestrator reads from it on demand.

```
your-workspace/
├── .cursor/
│   └── rules/
│       └── pdlc-session-orchestrator.mdc  ← The ONLY always-loaded file (alwaysApply: true; routes to cores)
├── .aiflc/
│   └── pdlc/                              ← AI-* PDLC Family home (cores + rule-details + fabric)
│       ├── ai-pilc-rules/core-workflow.md    ← Read on demand by the orchestrator
│       ├── ai-pilc-rule-details/             ← Read on demand by the core
│       │   ├── common/  inception/  assessment/  templates/  ...
│       └── ... one {pkg}-rules/ + {pkg}-rule-details/ per installed package
├── pdlc-ws/                              ← All runtime outputs land here (never workspace root)
└── (your project files)
```

Cursor loads only `pdlc-session-orchestrator.mdc` (its `alwaysApply: true` frontmatter). When you activate a package (by key or intent), the orchestrator `Read`s `.aiflc/pdlc/ai-{pkg}-rules/core-*.md`, and the core reads its rule-details from `.aiflc/pdlc/ai-{pkg}-rule-details/` as each phase needs them.

> **The AIFLC model:** one orchestrator loads always-on (`.cursor/rules/pdlc-session-orchestrator.mdc`); every package core + its rule-details live in the uniform home `.aiflc/pdlc/` and are read on demand; and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Method 1: Automated Installer (Recommended)

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive
.\installer\install.ps1

# Option B: One-liner for Cursor with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cursor -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cursor -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Cursor
./installer/install.sh --target <your-project-path> --platform cursor --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform cursor --bundle full
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

# Create the session orchestrator .mdc in Cursor's auto-load slot (the ONLY always-loaded file)
New-Item -ItemType Directory -Force -Path "$Target\.cursor\rules"
$frontmatter = @"
---
description: "AI-* PDLC Family session orchestrator"
alwaysApply: true
---

"@
$frontmatter | Out-File -FilePath "$Target\.cursor\rules\pdlc-session-orchestrator.mdc" -Encoding utf8
Get-Content "$Source\session-orchestrator.md" | Add-Content "$Target\.cursor\rules\pdlc-session-orchestrator.mdc"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
mkdir -p "$TARGET/.aiflc/pdlc"
cp -R "$SOURCE/ai-pilc/ai-pilc-rules" "$TARGET/.aiflc/pdlc/"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details" "$TARGET/.aiflc/pdlc/"

# Create the session orchestrator .mdc in Cursor's auto-load slot (the ONLY always-loaded file)
mkdir -p "$TARGET/.cursor/rules"
cat > "$TARGET/.cursor/rules/pdlc-session-orchestrator.mdc" << 'EOF'
---
description: "AI-* PDLC Family session orchestrator"
alwaysApply: true
---

EOF
cat "$SOURCE/session-orchestrator.md" >> "$TARGET/.cursor/rules/pdlc-session-orchestrator.mdc"
```

### File Placement Convention (Cursor)

Cores and rule-details both live in the uniform home `.aiflc/pdlc/` (read on demand). The only always-loaded file is `.cursor/rules/pdlc-session-orchestrator.mdc` — the single `.mdc` with `alwaysApply: true`.

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

> **Important:** The `.mdc` extension and `alwaysApply: true` frontmatter are required for Cursor to auto-load the orchestrator. It is now the ONLY `.mdc` the family installs — package cores are plain `.md` copies under `.aiflc/pdlc/`. The installer handles this for you.

---

## Multi-Package Installation

### Installing All 11 Packages

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform cursor -Bundle full
```

Or manually (PowerShell example for multiple packages):

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Ensure the uniform home and Cursor's rules slot exist
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc" | Out-Null
New-Item -ItemType Directory -Force -Path "$Target\.cursor\rules" | Out-Null

$packages = @(
    "ai-ilc", "ai-pilc", "ai-ppm", "ai-flo", "ai-adlc",
    "ai-uxd", "ai-polc", "ai-dwg", "ai-gce", "ai-tge", "ai-dfe"
)

# Copy every package core + rule-details into the uniform home (plain copies, no per-package .mdc)
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

# Create the single always-loaded orchestrator .mdc (the ONLY .mdc)
$frontmatter = "---`ndescription: `"AI-* PDLC Family session orchestrator`"`nalwaysApply: true`n---`n`n"
$mdcDest = "$Target\.cursor\rules\pdlc-session-orchestrator.mdc"
$frontmatter | Out-File -FilePath $mdcDest -Encoding utf8 -NoNewline
Get-Content "$Source\session-orchestrator.md" -Raw | Add-Content $mdcDest -NoNewline
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

### Common Starting Points

| Scenario | Start With | Then |
|----------|-----------|------|
| New project from scratch | AI-PILC | → AI-POLC → AI-UXD → AI-ADLC → AI-DWG |
| Have requirements, need architecture | AI-ADLC | → AI-DWG |
| Have architecture, need workspace | AI-DWG | → AI-GCE + AI-TGE |
| Idea evaluation (pre-project) | AI-ILC | → AI-PILC if approved |
| Existing project, add compliance | AI-GCE | + AI-TGE |

---

## Resulting Workspace Structure

After a full install:

```
your-project/
├── .cursor/
│   └── rules/
│       └── pdlc-session-orchestrator.mdc  ← The ONLY always-loaded file (alwaysApply: true)
├── .aiflc/
│   └── pdlc/                              ← AI-* PDLC Family home (cores + rule-details, on-demand)
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

1. Open your workspace in Cursor
2. Open Settings → Features → Rules
3. Confirm the AI-* `.mdc` files appear in the rules list with "Always" status
4. Start a new chat and say: "Using AI-PILC, initiate a project"
5. You should see the AI-PILC welcome message

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell the AI which package to use with the activation phrase
2. **Choose depth:** The package asks if you want Minimal, Standard, or Comprehensive output
3. **Work through stages:** Each package has defined stages with sequential guidance
4. **Approve at gates:** The AI presents output and waits for approval before proceeding
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk)

### Depth Levels

| Level | Output Volume | Best For |
|-------|--------------|----------|
| **Minimal** | Key essentials only | Prototypes, small projects, time-pressed |
| **Standard** | Professional baseline | Most projects (recommended default) |
| **Comprehensive** | Enterprise-grade detail | Regulated industries, large teams, audit-heavy |

---

## Chain Handoffs Between Packages

Packages detect each other's output through **state marker files**. When a package completes, it writes a marker (e.g., `pilc-state.md`). The next package detects the marker and enriches its work with that context.

**No manual wiring needed.** Just run packages sequentially.

---

## AI-GCE Governance on Cursor

AI-GCE generates all governance files correctly on Cursor, but enforcement is advisory rather than automatic:

### What Works

- Rule generation (`.governance/rules/`) — full mode 1/2/3/4
- Compliance documentation
- Brownfield baseline scanning
- Hook and agent file generation (structurally valid but inert)

### What Doesn't Work

| Feature | Why | Workaround |
|---------|-----|------------|
| Hook auto-execution | No event bus in Cursor | Add governance rules as `.mdc` files with `alwaysApply: true` |
| Agent shortcut triggers | No agent runtime | Paste agent prompts manually when needed |
| Automatic compliance logging | Triggered by hooks | Ask the AI to log manually |

### Best Practice

After AI-GCE generates governance, create an additional rule file:

```
.cursor/rules/governance-enforce.mdc
```

```markdown
---
description: "Governance rules enforcement (derived from AI-GCE)"
alwaysApply: true
---

## Governance Rules (Always Enforce)

Check compliance on every file you create or modify against:
- .governance/rules/security-rules.md (CRITICAL)
- .governance/rules/architecture-rules.md
- .governance/rules/naming-conventions.md

See .governance/COMPLIANCE_README.md for full rule index.
```

---

## Session Continuity

State files persist between sessions. Say "Continue AI-PILC" to resume where you left off.

---

## Coexistence with Other Rules

- **Existing `.cursor/rules/`**: Untouched. The family adds only one `.mdc` (`pdlc-session-orchestrator.mdc`) alongside yours; all package cores live under `.aiflc/pdlc/`.
- **Existing `.cursorrules`**: Untouched (legacy format, still respected by Cursor).
- **Other project files**: Never modified.

---

## Uninstalling

```powershell
# Via installer
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall

# Manual
Remove-Item "<your-project-path>\.cursor\rules\pdlc-session-orchestrator.mdc" -ErrorAction SilentlyContinue
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory | Remove-Item -Recurse -Force
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Orchestrator not loading | Missing frontmatter | Ensure `.cursor/rules/pdlc-session-orchestrator.mdc` has `alwaysApply: true` in YAML frontmatter |
| Package core not found | Path mismatch | Verify `.aiflc/pdlc/ai-{pkg}-rules/core-*.md` exists |
| "Can't find rule-details" | Path mismatch | Core resolves `.aiflc/pdlc/ai-{pkg}-rule-details/` first |
| No welcome message | Wrong activation phrase | Use "Using AI-PILC, ..." format |
| State file not created | First interaction only | State is created after first stage completes |

---

## Platform Capabilities Summary

| Feature | Cursor |
|---------|:------:|
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
