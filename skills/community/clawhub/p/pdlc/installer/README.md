# AI-* Family — Package Installer

Interactive installer that installs one or more AI-* packages into your target workspace using the locked **family-workspace** structure.

---

## What It Does

1. Asks which **platform** you're using (Kiro, Cursor, Claude Code, Cline, Amazon Q, GitHub Copilot)
2. Shows the package catalogue (or lets you pick a preset bundle)
3. Installs **package files** into the platform's rule location, scoped under the family
4. Creates the **family workspace** (`{family}-ws/`) with its locked Level 1 skeleton
5. Bootstraps the data layer and project registry
6. Installs **family tools** (visual tools / extensions) into `{family}-ws/tools/`
7. Deploys the **fabric trio** (`FAMILY_BINDINGS.md`, `GATE_PROTOCOL.md`, `FAMILY_INTERFACE.md`) into the family rule-details root — AI-FLO and AI-DFE read these at runtime to build the routing graph
8. Installs **package agents** into `.kiro/agents/` (Kiro) — e.g. FLO's `FHC__` health check and `FIA__` integrity agent
9. Writes an install manifest inside the family workspace

The **family** is auto-detected from the installer's parent folder name (e.g. `pdlc`).

> **Family tools.** The installer copies the family's `tools/extensions/` into the family
> workspace (`{family}-ws/tools/`) — e.g. the **PDLC Dashboard** (reads its data surface from
> `{family}-ws/data/`, produced by AI-DFE) and the **CommandBoard** trigger palette. Keeping
> tools beside `data/` inside `{family}-ws/` keeps everything family-scoped. Dev-only artifacts
> (`node_modules/`, `dist/`, `demo/`) are excluded, so only the runnable HTML UI, the
> `.vsix`, and the data contract are installed.

> **Fabric trio (REQUIRED for AI-FLO / AI-DFE).** AI-FLO and AI-DFE run in this planning /
> orchestration workspace (NOT inside an AI-DWG-generated dev workspace). They read the fabric
> trio at runtime to build the routing graph; without it AI-FLO returns **NOT READY**
> ("no bindings = no routing"). The installer copies the trio from the family root into the
> family rule-details root (`.kiro/{family}/` on Kiro). Agents are auto-installed on Kiro;
> other platforms use the shortcut-rules blocks documented in each package's INSTALL.md.

---

## Resulting Structure (Kiro example)

```
your-workspace/
├── .kiro/
│   ├── steering/
│   │   └── pdlc/                       ← package CORE files (auto-loaded steering)
│   │       └── ai-pilc-rules/core-workflow.md
│   └── pdlc/                           ← package RULE-DETAILS (on-demand) + fabric trio
│       ├── ai-pilc-rule-details/
│       ├── FAMILY_BINDINGS.md          ← fabric trio (routing graph)
│       ├── GATE_PROTOCOL.md            ← fabric trio (gate matching)
│       └── FAMILY_INTERFACE.md         ← fabric trio (discovery anchor)
│   └── agents/                         ← package agents (Kiro): FHC__, FIA__, …
│
├── pdlc-ws/                            ← FAMILY WORKSPACE (all outputs live here)
│   ├── .ai-family-manifest.json
│   ├── ideas/
│   ├── projects/
│   │   └── PROJECTS.md
│   ├── portfolio/
│   ├── data/
│   │   ├── REGISTRY.json
│   │   ├── CONSUMER_REGISTRY.md
│   │   ├── dfe-state.md
│   │   ├── demands/
│   │   └── history/
│   └── tools/                         ← FAMILY TOOLS (visual tools / extensions)
│       └── extensions/
│           ├── AIFLC-PDLC-Dashboard/  ← HTML dashboard + .vsix (reads ../../data/)
│           └── AIFLC-CommandBoard/    ← trigger palette (HTML + .vsix)
│
└── core/                              ← reserved (future shared infrastructure)
```

> **Kiro split:** core files go under `.kiro/steering/{family}/` (Kiro auto-loads only from `steering/`); rule-details go under `.kiro/{family}/` (read on-demand by the core file). Other platforms use a `{family}-` naming convention — see the per-platform mapping below.

---

## Quick Start

### Windows (PowerShell)

```powershell
# From the family root folder (e.g. pdlc/):
.\installer\install.ps1 -TargetWorkspace "C:\path\to\your\project"
```

### macOS / Linux (Bash)

```bash
./installer/install.sh --target ~/path/to/your/project
```

### Interactive Mode (no arguments)

```powershell
.\installer\install.ps1
```
```bash
./installer/install.sh
```

---

## Preset Bundles

| Bundle | Packages | Use Case |
|--------|----------|----------|
| **Full** | AI-ILC + AI-PILC + AI-PPM + AI-FLO + AI-POLC + AI-UXD + AI-ADLC + AI-DWG + AI-GCE + AI-TGE + AI-DFE | New project, complete family |
| **Minimal** | AI-PILC + AI-ADLC + AI-DWG | New project, quick start |
| **Architecture** | AI-ADLC + AI-DWG + AI-GCE | Architecture → workspace → governance |
| **Governance** | AI-GCE + AI-TGE | Existing workspace, add compliance |
| **Portfolio** | AI-ILC + AI-PILC + AI-PPM + AI-FLO | Multi-project portfolio management |
| **Custom** | You pick | Mix and match |

---

## Per-Platform Path Mapping

| Platform | Core file → | Rule-details → |
|----------|-------------|----------------|
| **Kiro** | `.kiro/steering/{family}/{pkg}-rules/{core}.md` | `.kiro/{family}/{pkg}-rule-details/` |
| **Amazon Q** | `.amazonq/rules/{family}/{pkg}-rules/{core}.md` | `.amazonq/{family}/{pkg}-rule-details/` |
| **Cursor** | `.cursor/rules/{family}-{pkg}-workflow.mdc` | `.{family}/{pkg}-rule-details/` |
| **Cline** | `.clinerules/{family}-{pkg}-core.md` | `.{family}/{pkg}-rule-details/` |
| **Claude Code** | `CLAUDE_{FAMILY}_{PKG}.md` | `.{family}/{pkg}-rule-details/` |
| **Copilot** | `.github/copilot-instructions-{family}-{pkg}.md` | `.{family}/{pkg}-rule-details/` |

Platforms with reliable nested-folder loading (Kiro rule-details, Amazon Q) use folder nesting; the rest use a `{family}-` filename prefix to achieve family scoping.

---

## Flags

| Flag | Description |
|------|-------------|
| `--target` / `-TargetWorkspace` | Path to the workspace |
| `--platform` / `-Platform` | `kiro`, `cursor`, `claude-code`, `cline`, `amazonq`, `copilot` |
| `--packages` / `-Packages` | Comma-separated package names (e.g., `ai-pilc,ai-adlc`) |
| `--bundle` / `-Bundle` | `full`, `minimal`, `arch`, `governance`, `portfolio` |
| `--dry-run` / `-DryRun` | Show what would be installed without copying |
| `--force` / `-Force` | Overwrite existing files without prompting |
| `--uninstall` / `-Uninstall` | Remove installed packages (reads manifest) |

---

## Examples

```powershell
.\installer\install.ps1 -TargetWorkspace "C:\Projects\my-app" -Platform kiro -Packages "ai-pilc,ai-adlc"
.\installer\install.ps1 -TargetWorkspace "C:\Projects\my-app" -Bundle minimal -DryRun
```
```bash
./installer/install.sh --target ~/projects/my-app --platform cursor --packages ai-gce,ai-tge
./installer/install.sh --target ~/projects/my-app --bundle full
```

---

## Uninstall

The manifest lives at `{family}-ws/.ai-family-manifest.json`. Uninstall removes the package files; it then asks whether to also remove the family workspace (your project data) — answer **no** to preserve your work.

```powershell
.\installer\install.ps1 -TargetWorkspace "C:\Projects\my-app" -Uninstall
```
```bash
./installer/install.sh --target ~/projects/my-app --uninstall
```

---

## Structural Rules (enforced by the installer)

- **`{family}-ws/` is created at the workspace root only** — never nested inside another folder.
- **Level 1 skeleton is fixed**: `ideas/`, `projects/`, `portfolio/`, `data/`.
- **`data/` is the Data Fabric (AI-DFE) territory** — bootstrapped empty; DFE writes here at runtime.
- **The fabric trio is deployed to the family rule-details root** (`.kiro/{family}/` on Kiro) — per-family copies of `FAMILY_BINDINGS.md`, `GATE_PROTOCOL.md`, `FAMILY_INTERFACE.md`; removed on uninstall.
- **Multiple families coexist**: installing a second family creates its own `{family}-ws/` alongside the first; neither interferes with the other.
- **Re-running the installer** on an existing family is update-mode — packages are added/updated, the workspace skeleton is preserved.

---

## Notes

- Each package is independently installable — order doesn't matter.
- The installer never modifies your existing project files — only adds AI-* package files + the family workspace.
- Chain detection happens at runtime (via state markers), not at install time.
- See [PLATFORM_CAPABILITIES.md](../PLATFORM_CAPABILITIES.md) for what works on each platform.

---

*Part of the [AI-* Family](../README.md) — Injectable Workflow Packages for AI-Assisted Software Delivery*
