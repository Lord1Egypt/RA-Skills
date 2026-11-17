# AI-* Family — Complete Installation Guide for GitHub Copilot

**Applies to:** GitHub Copilot (VS Code / JetBrains) — partial support with workspace-level instructions.

> **⚠️ Partial Support:** GitHub Copilot supports workspace-level instructions via `.github/copilot-instructions.md`, but has limitations: only one instructions file is supported per workspace, and on-demand file reading behavior varies. Under the AIFLC model that single file carries only the compact orchestrator (package cores live in `.aiflc/pdlc/`, read on demand), so the full chain installs cleanly — the main caveat is that on-demand reading is less consistent than on Kiro/Claude Code/Cursor.

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
- [AI-GCE Governance on Copilot](#ai-gce-governance-on-copilot)
- [Limitations and Workarounds](#limitations-and-workarounds)
- [Uninstalling](#uninstalling)
- [Troubleshooting](#troubleshooting)
- [Platform Capabilities Summary](#platform-capabilities-summary)

---

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **GitHub Copilot** | Active subscription + VS Code/JetBrains extension installed |
| **A workspace folder** | Any project directory where you want AI-assisted delivery |
| **PowerShell 5.1+** (Windows) or **Bash** (macOS/Linux) | For the automated installer |
| **The AIFLC package source** | Clone the [AIPDLC repository](https://github.com/mbmd/AIPDLC) |

> You do NOT need: Node.js, Python, Docker, or any runtime. Packages are pure Markdown — no compilation, no dependencies.

---

## How It Works

The installer places **one always-loaded file** plus the **package home**, both scoped to the AI-* PDLC Family (multiple AIFLC families can coexist in one workspace):

1. **Session orchestrator** — the orchestrator block placed in `.github/copilot-instructions.md` (the single file Copilot reads automatically). It is the ONLY always-loaded file. It detects which package you want and `Read`s that package's core on demand — keeping the context window free.
2. **Package home** — every package's core AND rule-details live together in the uniform, agent-neutral home `.aiflc/pdlc/`. Nothing here auto-loads; the orchestrator reads from it on demand.

```
your-workspace/
├── .github/
│   └── copilot-instructions.md                 ← The ONLY always-loaded file (orchestrator block)
├── .aiflc/
│   └── pdlc/                                    ← AI-* PDLC Family home (cores + rule-details + fabric)
│       ├── ai-pilc-rules/core-workflow.md          ← Read on demand by the orchestrator
│       ├── ai-pilc-rule-details/                   ← Read on demand by the core
│       │   ├── common/  inception/  assessment/  templates/  ...
│       └── ... one {pkg}-rules/ + {pkg}-rule-details/ per installed package
├── pdlc-ws/                                      ← All runtime outputs land here (never workspace root)
└── (your project files)
```

> **Note:** GitHub Copilot only reads `.github/copilot-instructions.md` (singular). Under the AIFLC model this is a non-issue: that single file carries only the compact **orchestrator**, and every package core lives separately in `.aiflc/pdlc/`, read on demand. You no longer merge package cores into the instructions file — so the old single-file size constraint is largely lifted.

> **The AIFLC model:** one orchestrator loads always-on (`.github/copilot-instructions.md`); every package core + its rule-details live in the uniform home `.aiflc/pdlc/` and are read on demand; and everything the packages *produce* — projects, portfolio, ideas, generated workspaces — is written under `pdlc-ws/`, never scattered at your workspace root. The `.aiflc/pdlc/` layout is identical on every platform.

---

## Method 1: Automated Installer (Recommended)

### Windows (PowerShell)

```powershell
# Navigate to the AIFLC package source
cd "<path-to-AIPDLC>"

# Option A: Fully interactive
.\installer\install.ps1

# Option B: One-liner for Copilot with specific packages
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform copilot -Packages "ai-pilc,ai-adlc,ai-dwg"

# Option C: Install a preset bundle
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Platform copilot -Bundle full
```

### macOS / Linux (Bash)

```bash
# Navigate to the AIFLC package source
cd <path-to-AIPDLC>

# Option A: Fully interactive
./installer/install.sh

# Option B: One-liner for Copilot
./installer/install.sh --target <your-project-path> --platform copilot --packages ai-pilc,ai-adlc,ai-dwg

# Option C: Install a preset bundle
./installer/install.sh --target <your-project-path> --platform copilot --bundle full
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

### Single Package (Simple Case)

**Windows (PowerShell):**

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Place the orchestrator block in Copilot's slot (the ONLY always-loaded file)
New-Item -ItemType Directory -Force -Path "$Target\.github"
Copy-Item "$Source\session-orchestrator.md" "$Target\.github\copilot-instructions.md"

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
New-Item -ItemType Directory -Force -Path "$Target\.aiflc\pdlc"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rules" "$Target\.aiflc\pdlc\"
Copy-Item -Recurse "$Source\ai-pilc\ai-pilc-rule-details" "$Target\.aiflc\pdlc\"
```

**macOS / Linux:**

```bash
SOURCE=<path-to-AIPDLC>
TARGET=<your-project-path>

# Place the orchestrator block in Copilot's slot (the ONLY always-loaded file)
mkdir -p "$TARGET/.github"
cp "$SOURCE/session-orchestrator.md" "$TARGET/.github/copilot-instructions.md"

# Copy the package core + rule-details into the uniform home .aiflc/pdlc/
mkdir -p "$TARGET/.aiflc/pdlc"
cp -R "$SOURCE/ai-pilc/ai-pilc-rules" "$TARGET/.aiflc/pdlc/"
cp -R "$SOURCE/ai-pilc/ai-pilc-rule-details" "$TARGET/.aiflc/pdlc/"
```

---

## Multi-Package Installation

### One Orchestrator, Many Cores

GitHub Copilot reads only `.github/copilot-instructions.md`. Under the AIFLC model that's all you need there — the compact orchestrator. Every package core lives in `.aiflc/pdlc/` and is read on demand, so adding more packages does **not** grow the always-loaded file:

```powershell
$Source = "<path-to-AIPDLC>"
$Target = "<your-project-path>"

# Place the single orchestrator block in Copilot's slot
New-Item -ItemType Directory -Force -Path "$Target\.github" | Out-Null
Copy-Item "$Source\session-orchestrator.md" "$Target\.github\copilot-instructions.md" -Force

# Copy every package core + rule-details into the uniform home
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

### Context Window Note

Because only the compact orchestrator loads always-on (package cores are read on demand from `.aiflc/pdlc/`), the old single-file size limit is largely lifted — you can install the full chain on Copilot. The remaining Copilot caveat is on-demand file reading, which can be less consistent than Kiro/Claude Code/Cursor: if Copilot doesn't auto-read a core, reference it explicitly (see [Tips for Copilot](#tips-for-copilot)).

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

### Recommended Packages for Copilot

With cores now living in `.aiflc/pdlc/` (read on demand), you can install the full chain. These combinations are common starting points:

| Scenario | Packages | Why |
|----------|----------|-----|
| Quick start | AI-PILC + AI-ADLC | Core lifecycle without generator overhead |
| Architecture | AI-ADLC + AI-DWG | Design → generate |
| Governance | AI-GCE + AI-TGE | Compliance + test quality |
| Idea to project | AI-ILC + AI-PILC | Evaluation → initiation |

---

## Resulting Workspace Structure

After installation (example with 3 packages):

```
your-project/
├── .github/
│   └── copilot-instructions.md          ← The ONLY always-loaded file (orchestrator block)
├── .aiflc/
│   └── pdlc/                            ← AI-* PDLC Family home (cores + rule-details, on-demand)
│       ├── ai-pilc-rules/core-workflow.md
│       ├── ai-pilc-rule-details/
│       ├── ai-adlc-rules/core-workflow.md
│       ├── ai-adlc-rule-details/
│       ├── ai-dwg-rules/core-generator.md
│       └── ai-dwg-rule-details/
├── pdlc-ws/                             ← All runtime outputs (projects, portfolio, ideas, generated workspaces)
│   └── .ai-family-manifest.json         ← Installer tracking
└── (your project files)
```

---

## Verification

1. Open your workspace in VS Code with GitHub Copilot active
2. Open Copilot Chat
3. Type: "Using AI-PILC, initiate a project"
4. **Expected:** Copilot responds with the workflow and begins guiding you

> **Note:** If Copilot doesn't reference the instructions, try `@workspace` prefix: "@workspace Using AI-PILC, initiate a project"

---

## Using the Packages

### Basic Workflow

1. **Start a session:** Tell Copilot which package to use with the activation phrase
2. **Choose depth:** Minimal, Standard, or Comprehensive
3. **Work through stages:** Copilot guides you sequentially
4. **Approve at gates:** Output presented for approval before proceeding
5. **Get deliverables:** Each stage produces one deliverable

### Tips for Copilot

- Use `@workspace` prefix if Copilot doesn't pick up instructions automatically
- Reference the package core explicitly if Copilot doesn't read it: "Read `.aiflc/pdlc/ai-pilc-rules/core-workflow.md` and follow it"
- Reference rule-details files explicitly if Copilot doesn't read them: "Read `.aiflc/pdlc/ai-pilc-rule-details/inception/stage-01-source-analysis.md` and execute it"
- Copilot Chat works better than inline suggestions for workflow execution

---

## Chain Handoffs Between Packages

Packages detect each other through **state marker files**. This works on Copilot if:
- You use Copilot Chat (not inline suggestions)
- Copilot has access to read workspace files

---

## AI-GCE Governance on Copilot

AI-GCE generates governance files, but enforcement is entirely advisory:

| Feature | Status |
|---------|--------|
| Rule generation | ✅ (files created) |
| Hook auto-execution | ❌ |
| Agent triggers | ❌ |
| Compliance logging | ❌ |

**Workaround:** After AI-GCE runs, append a governance reminder section to `copilot-instructions.md`:

```markdown
## Governance (Always Check)

Before completing any file, verify against:
- .governance/rules/security-rules.md
- .governance/rules/architecture-rules.md
```

---

## Limitations and Workarounds

| Limitation | Impact | Workaround |
|-----------|--------|------------|
| Single instructions file | Only the orchestrator lives there | Not a problem — package cores live in `.aiflc/pdlc/`, read on demand |
| On-demand file reading inconsistent | May not auto-read a core or rule-details | Reference files explicitly in prompts |
| No hook/agent execution | AI-GCE enforcement is advisory | Use CI/CD hooks instead |
| Workspace-level only | No per-folder scoping | All packages apply globally |

### When to Consider a Different Platform

If you need:
- AI-GCE enforcement → Use Kiro
- Reliable on-demand file loading → Use Kiro, Claude Code, Cursor, or Cline
- The smoothest full-chain experience → Use Kiro, Claude Code, or Cursor

---

## Uninstalling

```powershell
# Via installer
.\installer\install.ps1 -TargetWorkspace "<your-project-path>" -Uninstall

# Manual
Remove-Item "<your-project-path>\.github\copilot-instructions.md" -ErrorAction SilentlyContinue
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rules" -Directory | Remove-Item -Recurse -Force
Get-ChildItem "<your-project-path>\.aiflc\pdlc\ai-*-rule-details" -Directory | Remove-Item -Recurse -Force
Remove-Item "<your-project-path>\pdlc-ws\.ai-family-manifest.json" -ErrorAction SilentlyContinue
```

> **Warning:** If you had a pre-existing `copilot-instructions.md`, the installer backs it up as `copilot-instructions.md.bak`. Restore it after uninstalling.

---

## Troubleshooting

| Issue | Cause | Solution |
|-------|-------|----------|
| Copilot ignores instructions | File not in correct location | Must be exactly `.github/copilot-instructions.md` |
| Package core not found | Path mismatch | Verify `.aiflc/pdlc/ai-{pkg}-rules/core-*.md` exists |
| "Can't find rule-details" | Copilot not reading workspace files | Reference files explicitly: "Read `.aiflc/pdlc/ai-pilc-rule-details/...`" |
| No structured workflow | Copilot treating as suggestions | Use Copilot Chat, not inline. Try `@workspace` prefix |
| State file not persisting | Copilot not writing files | Use Copilot Chat with "save this to file" instructions |

---

## Platform Capabilities Summary

| Feature | GitHub Copilot |
|---------|:--------------:|
| Core workflow execution | ✅ |
| On-demand file loading | ⚠️ Inconsistent |
| Deliverable file output | ✅ |
| State persistence | ✅ |
| Chain marker detection | ✅ |
| Multi-package install | ✅ All 11 (cores in `.aiflc/pdlc/`) |
| AI-DWG workspace gen | ✅ |
| AI-GCE rule generation | ✅ |
| AI-GCE hook enforcement | ❌ (Kiro only) |
| Depth adaptation | ✅ |
| Session continuity | ✅ (if state file works) |

**GitHub Copilot supports the full chain** now that cores live in `.aiflc/pdlc/`. For governance enforcement (hooks/agents) or the most consistent on-demand loading, Kiro remains the strongest platform.

---

*Part of the [AI-* Family](./README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
*See also: [PLATFORM_CAPABILITIES.md](./PLATFORM_CAPABILITIES.md) for the full cross-platform matrix*
