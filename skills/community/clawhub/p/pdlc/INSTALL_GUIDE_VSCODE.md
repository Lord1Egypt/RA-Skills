# AI-* Family — Complete Installation Guide for VS Code (Agent Framework)

**Applies to:** VS Code's built-in AI Agent framework — works with any model provider (Copilot, Claude, Gemini, OpenAI, or custom via API key).

> **What is this?** Since VS Code 1.102+ (2025), the editor has a unified AI customization system that works with multiple AI providers simultaneously. You can use GitHub Copilot, Claude (via Anthropic API), or any other model — the customization layer is the same. This guide targets that unified system using `AGENTS.md`, `.github/instructions/`, and `.github/copilot-instructions.md`.

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [How It Works](#how-it-works)
- [VS Code Instruction System Overview](#vs-code-instruction-system-overview)
- [Method 1: Automated Installer (Recommended)](#method-1-automated-installer-recommended)
- [Method 2: Manual Installation](#method-2-manual-installation)
- [Multi-Package Installation](#multi-package-installation)
- [Package Reference](#package-reference)
- [Resulting Workspace Structure](#resulting-workspace-structure)
- [Verification](#verification)
- [Using the Packages](#using-the-packages)
- [Chain Handoffs Between Packages](#chain-handoffs-between-packages)
- [AI-GCE Governance on VS Code](#ai-gce-governance-on-vs-code)
- [Session Continuity](#session-continuity)
- [Advanced: Using .instructions.md Files](#advanced-using-instructionsmd-files)
- [Coexistence with Other Customizations](#coexistence-with-other-customizations)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **VS Code 1.102+** | With at least one AI provider configured (Copilot, Claude, etc.) |
| **An AI provider** | GitHub Copilot subscription, Anthropic API key, OpenAI key, or other |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

The installer places **one always-loaded file** plus the **package home**, both scoped to the AI-* PDLC Family (multiple AIFLC families can coexist in one workspace):

1. **Session orchestrator** — a single always-on instruction block that VS Code's agent reads automatically at session start (placed in `AGENTS.md` or `.github/copilot-instructions.md`). It is the ONLY always-loaded file. It detects which package you want and `Read`s that package's core on demand — keeping the context window free.
2. **Package home** — every package's core AND rule-details live together in the uniform, agent-neutral home `.aiflc/pdlc/`. Nothing here auto-loads; the orchestrator reads from it on demand.

```
your-workspace/
├── AGENTS.md                              ← The orchestrator block (any AI agent) — OR —
├── .github/
│   └── copilot-instructions.md            ← The orchestrator block (Copilot, also read by others)
├── .aiflc/
│   └── pdlc/                              ← AI-* PDLC Family home (cores + rule-details + fabric)
│       ├── ai-pilc-rules/core-workflow.md    ← Read on demand by the orchestrator
│       ├── ai-pilc-rule-details/             ← Read on demand by the core
│       │   ├── common/  inception/  assessment/  templates/  ...
│       └── ... one {pkg}-rules/ + {pkg}-rule-details/ per installed package
├── pdlc-ws/                               ← All runtime outputs land here (never workspace root)
└── (your project files)
```

> **The AIFLC model:** one orchestrator loads always-on (`AGENTS.md` or `.github/copilot-instructions.md`); every package core + its rule-details live in the uniform home `.aiflc/pdlc/` and are read on demand; and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root. The `.aiflc/pdlc/` layout is identical on every platform.

---

## VS Code Instruction System Overview

VS Code now supports **multiple instruction formats** that all feed into the same AI context. Understanding these helps you choose the right installation approach:

| Format | File | Scope | Best For |
|--------|------|-------|----------|
| **Always-on (Copilot)** | `.github/copilot-instructions.md` | All requests | Single package or merged multi-package |
| **Always-on (Universal)** | `AGENTS.md` | All AI agents | Cross-agent compatibility (Copilot + Claude + others) |
| **Always-on (Claude)** | `CLAUDE.md` | Claude-based agents | If primary agent is Claude |
| **File-scoped** | `.github/instructions/*.instructions.md` | Matches `applyTo` pattern | Per-package isolation with glob control |
| **Custom agents** | `.github/agents/*.agent.md` | On-demand persona | Each package as a named agent |

### Recommended Approach for AI-* Packages

Under the AIFLC model there is only **one** always-loaded file — the session orchestrator. The only choice is which native slot to place it in. Package cores are never per-package instruction files anymore; they are plain copies under `.aiflc/pdlc/`, read on demand.

**Option A — `AGENTS.md` (simplest, broadest compatibility):**
The orchestrator block in a single `AGENTS.md` that any VS Code AI agent reads. Works with Copilot, Claude, and third-party models.

**Option B — `.github/copilot-instructions.md` (Copilot-focused):**
The same orchestrator block in `.github/copilot-instructions.md`. Best if you primarily use GitHub Copilot (this file is also read by other agents).

This guide covers **both options**. Either way, all 11 package cores live in `.aiflc/pdlc/` — the placement of the orchestrator is the only difference.

---

## Method 1: Automated Installer (Recommended)

The interactive installer supports VS Code via the `copilot` platform flag. For the universal `AGENTS.md` approach, use manual installation (Method 2) or the instructions below.

### Using the Installer (Copilot mode)

```powershell
cd "<path-to-AIPDLC>"
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform copilot -Packages "ai-pilc,ai-adlc,ai-dwg"
```

> **Note:** The installer's `copilot` mode creates `.github/copilot-instructions.md`. For the `AGENTS.md` or `.instructions.md` approach, use Method 2 below.

### macOS / Linux

```bash
cd <path-to-AIPDLC>
./installer/install.sh --target <your-project-path> --platform copilot --packages ai-pilc,ai-adlc,ai-dwg
```

---

## Method 2: Manual Installation

### Option A: Orchestrator in AGENTS.md (Universal — Any AI Agent)

This places the session orchestrator in a single `AGENTS.md` that VS Code loads for ALL AI agents (Copilot, Claude, etc.), and copies every package core + rule-details into the uniform home `.aiflc/pdlc/`:

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Place the session orchestrator (the ONLY always-loaded file) in AGENTS.md
Copy-Item "$Source\session-orchestrator.md" "$Target\AGENTS.md"

# Copy every package core + rule-details into the uniform home .aiflc/pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc" | Out-Null
$packages = @("ai-pilc", "ai-adlc", "ai-dwg")   # example subset

foreach ($pkg in $packages) {
    $rulesSource = Join-Path $Source "$pkg\$pkg-rules"
    $detailsSource = Join-Path $Source "$pkg\$pkg-rule-details"
    if (Test-Path $rulesSource) {
        Copy-Item -Recurse $rulesSource "$Target\.aiflc\pdlc\" -Force
        Copy-Item -Recurse $detailsSource "$Target\.aiflc\pdlc\" -Force
        Write-Host "Installed $pkg into .aiflc/pdlc/" -ForegroundColor Green
    }
}
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Place the session orchestrator (the ONLY always-loaded file) in AGENTS.md
cp "$SOURCE/session-orchestrator.md" "$TARGET/AGENTS.md"

# Copy every package core + rule-details into the uniform home .aiflc/pdlc/
mkdir -p "$TARGET/.aiflc/pdlc"
for pkg in ai-pilc ai-adlc ai-dwg; do   # example subset
    cp -R "$SOURCE/$pkg/${pkg}-rules" "$TARGET/.aiflc/pdlc/"
    cp -R "$SOURCE/$pkg/${pkg}-rule-details" "$TARGET/.aiflc/pdlc/"
    echo "Installed $pkg into .aiflc/pdlc/"
done
```

### Option B: Orchestrator in .github/copilot-instructions.md (Copilot-focused)

This places the same orchestrator in `.github/copilot-instructions.md` instead — the cores still land in `.aiflc/pdlc/`:

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Place the session orchestrator in Copilot's slot (the ONLY always-loaded file)
New-Item -ItemType Directory -Force -Path "$Target\.github" | Out-Null
Copy-Item "$Source\session-orchestrator.md" "$Target\.github\copilot-instructions.md"

# Copy every package core + rule-details into the uniform home .aiflc/pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc" | Out-Null
$packages = @(
    "ai-ilc", "ai-pilc", "ai-ppm", "ai-flo", "ai-adlc",
    "ai-uxd", "ai-polc", "ai-dwg", "ai-gce", "ai-tge", "ai-dfe"
)

foreach ($pkg in $packages) {
    $rulesSource = Join-Path $Source "$pkg\$pkg-rules"
    $detailsSource = Join-Path $Source "$pkg\$pkg-rule-details"
    if (Test-Path $rulesSource) {
        Copy-Item -Recurse $rulesSource "$Target\.aiflc\pdlc\" -Force
        Copy-Item -Recurse $detailsSource "$Target\.aiflc\pdlc\" -Force
        Write-Host "Installed $pkg into .aiflc/pdlc/" -ForegroundColor Green
    }
}
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Place the session orchestrator in Copilot's slot (the ONLY always-loaded file)
mkdir -p "$TARGET/.github"
cp "$SOURCE/session-orchestrator.md" "$TARGET/.github/copilot-instructions.md"

# Copy every package core + rule-details into the uniform home .aiflc/pdlc/
mkdir -p "$TARGET/.aiflc/pdlc"
for pkg in ai-ilc ai-pilc ai-ppm ai-flo ai-adlc ai-uxd ai-polc ai-dwg ai-gce ai-tge ai-dfe; do
    cp -R "$SOURCE/$pkg/${pkg}-rules" "$TARGET/.aiflc/pdlc/"
    cp -R "$SOURCE/$pkg/${pkg}-rule-details" "$TARGET/.aiflc/pdlc/"
    echo "Installed $pkg into .aiflc/pdlc/"
done
```

---

## Multi-Package Installation

### Context Window Considerations

VS Code loads only the **session orchestrator** at session start — not the package cores. This means you can install all 11 packages without bloating the always-on context: the orchestrator is a compact router, and each package core is read from `.aiflc/pdlc/` only when you activate it.

- **Only one always-loaded file** regardless of how many packages you install.
- **Package cores load on demand** — the AI activates exactly one at a time.
- **Rule-details load per phase** — the core reads them from `.aiflc/pdlc/ai-{pkg}-rule-details/` as needed.

### Recommended: Install What You Need

| Scenario | Packages | Notes |
|----------|----------|-------|
| 1–3 packages | Any subset | Minimal footprint |
| 4–6 packages | Selective | Still just one always-on file |
| 7–11 packages | Full chain | Fully supported — cores stay dormant in `.aiflc/pdlc/` until invoked |

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

### Option A (orchestrator in AGENTS.md)

```
your-project/
├── AGENTS.md                                ← The ONLY always-loaded file (orchestrator; all agents read it)
├── .aiflc/
│   └── pdlc/                                ← AI-* PDLC Family home (cores + rule-details, on-demand)
│       ├── ai-pilc-rules/core-workflow.md
│       ├── ai-pilc-rule-details/
│       ├── ai-adlc-rules/core-workflow.md
│       ├── ai-adlc-rule-details/
│       ├── ai-dwg-rules/core-generator.md
│       └── ai-dwg-rule-details/
├── pdlc-ws/                                 ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
└── (your project files)
```

### Option B (orchestrator in .github/copilot-instructions.md — full 11-package install)

```
your-project/
├── .github/
│   └── copilot-instructions.md              ← The ONLY always-loaded file (orchestrator)
├── .aiflc/
│   └── pdlc/                                ← AI-* PDLC Family home (cores + rule-details, on-demand)
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
├── pdlc-ws/                                 ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
└── (your project files)
```

---

## Verification

### Step 1: Check instruction loading

1. Open your workspace in VS Code
2. Open the Command Palette (`Ctrl+Shift+P`)
3. Run `Chat: Configure Instructions` or open the **Agent Customizations** editor
4. Confirm your AI-* instruction files appear in the list

### Step 2: Verify with diagnostics

1. Open any Chat view
2. Right-click → **Diagnostics**
3. Check that AI-* instructions appear in the loaded instructions list

### Step 3: Test activation

Start a chat and type:

```
Using AI-PILC, initiate a project from this requirement: [your requirement]
```

**Expected:** The AI responds with the package's welcome message and begins the structured workflow.

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell the AI which package to use with the activation phrase
2. **Choose depth:** Minimal, Standard, or Comprehensive
3. **Work through stages:** The AI guides you sequentially
4. **Approve at gates:** Output presented for approval before proceeding
5. **Get deliverables:** Each stage produces one professional deliverable (written to disk)

### Which AI Model Works Best?

| Model | Works | Notes |
|-------|:-----:|-------|
| Claude (Anthropic) | ✅ | Excellent instruction-following. Best results. |
| GPT-4o / GPT-4.1 | ✅ | Good instruction-following. Works well. |
| Copilot (GPT-based) | ✅ | Good. Use Chat view, not inline suggestions. |
| Gemini | ✅ | Works. May need more explicit prompting for gates. |
| Local models (Ollama, etc.) | ⚠️ | Depends on model size. 70B+ recommended. |

---

## Chain Handoffs Between Packages

Packages detect each other through **state marker files** (e.g., `pilc-state.md`). Run packages sequentially and they find each other's output automatically.

---

## AI-GCE Governance on VS Code

AI-GCE generates all governance files correctly, but auto-enforcement varies by feature:

| Feature | VS Code (Copilot/Claude) | Notes |
|---------|:------------------------:|-------|
| Rule generation | ✅ | `.governance/rules/` created normally |
| VS Code hooks | ✅ | VS Code 1.102+ supports `.github/hooks/` |
| Kiro-style hook execution | ❌ | Kiro's event bus is proprietary |
| Agent file generation | ✅ | `.github/agents/` works in VS Code |
| Compliance logging | ⚠️ Manual | Ask AI to log manually |

### Best Practice: Governance Instructions

After AI-GCE generates governance, create a governance instruction file:

```markdown
<!-- .github/instructions/governance.instructions.md -->
---
name: 'Governance enforcement'
description: 'Checks compliance against workspace governance rules'
applyTo: '**'
---

## Governance Rules (Always Enforce)

Before completing any file modification, verify against:
- .governance/rules/security-rules.md (CRITICAL)
- .governance/rules/architecture-rules.md
- .governance/rules/naming-conventions.md

See .governance/COMPLIANCE_README.md for the full rule index.
```

### VS Code Hooks (New in 1.102+)

VS Code now supports hooks (`.github/hooks/`) that run at specific points in the agent loop. AI-GCE can be adapted to generate VS Code-format hooks for basic enforcement. This is not yet automatic but is on the roadmap (Idea 011: Platform-Portable Governance Adapters).

---

## Session Continuity

State files persist between sessions. Say "Continue AI-PILC" to resume where you left off.

---

## Advanced: Using .instructions.md Files

### File-Scoped Instructions for Package Details

You can create instructions that only activate when working in specific folders:

```markdown
<!-- .github/instructions/pdlc-ai-pilc-details.instructions.md -->
---
name: 'AI-PILC detail loading'
description: 'Loads AI-PILC phase details when working in PILC output folders'
applyTo: '**/pdlc-ws/**'
---

When working in `pdlc-ws/`, reference the AI-PILC templates in `.aiflc/pdlc/ai-pilc-rule-details/templates/` for consistent formatting.
```

### User-Level Instructions (Cross-Project)

Store shared instructions in `~/.copilot/instructions/` to have them available in all workspaces:

```powershell
# Copy the AI-* Family activation guide to user-level
New-Item -ItemType Directory -Force -Path "$HOME\.copilot\instructions"
# Create a brief activator that tells the AI how to handle "Using AI-*" prompts
```

---

## Coexistence with Other Customizations

AI-* packages coexist with all other VS Code AI customizations:

- **Existing `copilot-instructions.md`**: If using Option B and a file already exists, back it up first — the orchestrator replaces it (or merge the orchestrator block into your existing file).
- **Existing `AGENTS.md`**: If using Option A and a file already exists, merge the orchestrator block into it rather than overwriting.
- **Existing `.instructions.md` files**: Untouched. The family no longer adds per-package instruction files — package cores live under `.aiflc/pdlc/`.
- **Custom agents**: AI-* packages don't create `.agent.md` files by default (but you can convert them — see below).
- **Other project files**: Never modified.

### Converting Packages to Custom Agents (Advanced)

VS Code supports `.github/agents/*.agent.md` files that define specialized personas. You could wrap each AI-* package as a custom agent that reads its core from the uniform home:

```markdown
<!-- .github/agents/pdlc-ai-pilc.agent.md -->
---
name: AI-PILC
description: Project Initiation Life Cycle — guides you from raw requirement to a professional Project Initiation Package
instructions:
  - .aiflc/pdlc/ai-pilc-rules/core-workflow.md
tools:
  - read_file
  - write_file
  - list_directory
---

You are the AI-PILC agent. When invoked, follow the core workflow in `.aiflc/pdlc/ai-pilc-rules/core-workflow.md` to guide the user through project initiation.
```

This lets users invoke `@ai-pilc` in chat directly. This is an advanced configuration not yet handled by the installer.

---

## Uninstalling

### Option A (orchestrator in AGENTS.md)

```powershell
Remove-Item "<your-project-path>\AGENTS.md" -ErrorAction SilentlyContinue
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory | Remove-Item -Recurse -Force
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
```

### Option B (orchestrator in .github/copilot-instructions.md)

```powershell
Remove-Item "<your-project-path>\.github\copilot-instructions.md" -ErrorAction SilentlyContinue
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory | Remove-Item -Recurse -Force
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
```

### Via Installer (Copilot mode)

```powershell
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall
```

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Orchestrator not loading | Setting disabled | Ensure `chat.includeApplyingInstructions` is enabled in settings |
| AGENTS.md not recognized | Feature disabled | Enable `chat.useAgentsMdFile` in VS Code settings (Option A) |
| Package core not found | Path mismatch | Verify `.aiflc/pdlc/ai-{pkg}-rules/core-*.md` exists |
| "Can't find rule-details" | Path mismatch | Core resolves `.aiflc/pdlc/ai-{pkg}-rule-details/` first |
| Wrong model being used | Model selection | Check your model selection in Chat view dropdown |
| Orchestrator not applied | Wrong slot | Confirm the orchestrator sits in `AGENTS.md` or `.github/copilot-instructions.md` |
| Instructions applied but not followed | Model limitation | Try a stronger model (Claude or GPT-4o recommended) |
| Nested instructions not found | Monorepo setting | Enable `chat.useCustomizationsInParentRepositories` |

### Diagnostics

Right-click in Chat view → **Diagnostics** to see:
- Which instruction files were loaded
- Which ones applied to the current request
- Any errors in instruction file parsing

---

## Platform Capabilities Summary

| Feature | VS Code (Agent Framework) |
|---------|:-------------------------:|
| Core workflow execution | ✅ |
| On-demand file loading | ✅ |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ✅ All 11 (cores in `.aiflc/pdlc/`) |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ⚠️ Partial (VS Code hooks exist, different format) |
| VS Code native hooks | ✅ (1.102+, `.github/hooks/`) |
| Custom agent wrapping | ✅ (`.github/agents/`) |
| Multi-model support | ✅ (Any provider) |
| Depth adaptation | ✅ |
| Session continuity | ✅ Cold resume |

### Comparison: VS Code Agent Framework vs. Platform-Specific Guides

| If you use... | Use this guide | Or this platform guide |
|---------------|----------------|----------------------|
| VS Code + Copilot | This guide (Option B) | `INSTALL_GUIDE_COPILOT.md` |
| VS Code + Claude (API) | This guide (Option A or B) | `INSTALL_GUIDE_CLAUDE.md` (for Claude Code CLI) |
| VS Code + Cline extension | `INSTALL_GUIDE_CLINE.md` | — |
| VS Code + Any model via API | This guide | — |
| Kiro (VS Code-based) | `INSTALL_GUIDE_KIRO.md` | — |

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
