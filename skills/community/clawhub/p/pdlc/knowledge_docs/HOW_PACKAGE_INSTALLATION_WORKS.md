# How Package Installation Works

**Purpose:** Explains how AI-* Family packages are installed into an AI workspace — the file copy mechanism, steering file placement, platform support, and coexistence model that allows multiple packages to operate in the same workspace.

---

## What Installation Means

AI-* packages are not compiled software. They are injectable workflow packages — collections of markdown files (rules, templates, steering) that an AI assistant loads at session start. "Installation" means copying these files into the right location so the AI platform can find and load them.

```
PACKAGE SOURCE (e.g., ai-pilc/)
├── ai-pilc-rules/core-workflow.md
├── ai-pilc-rule-details/...
└── setup/INSTALL.md
        │
        ▼  (copy to workspace)
YOUR WORKSPACE
├── .kiro/
│   └── steering/
│       └── ai-pilc-rules.md (or symlink to package)
├── ai-pilc-rules/
│   └── core-workflow.md
└── ai-pilc-rule-details/
    └── ...
```

---

## The Installation Pattern

Every package follows the same structure:

### Step 1: Copy Package Files

Copy the package's rule folder and detail folder into your workspace:
- `{package}/ai-{pkg}-rules/` → your workspace root
- `{package}/ai-{pkg}-rule-details/` → your workspace root

### Step 2: Configure Platform Loading

Tell your AI platform to load the core file at session start. The mechanism varies by platform:

| Platform | Loading Mechanism |
|----------|------------------|
| **Kiro** | Add to `.kiro/steering/` (auto-loaded) or reference in settings |
| **Cursor** | Add to `.cursorrules` or `.cursor/rules/` |
| **Windsurf** | Add to `.windsurfrules` |
| **GitHub Copilot** | Add to `.github/copilot-instructions.md` |
| **Cline** | Add to `.clinerules` |
| **Generic** | Include in system prompt or project instructions |

### Step 3: Verify

Start a new AI session. The AI should acknowledge the package rules and offer to begin the workflow.

---

## Platform-Specific Installation

### Kiro (Primary Target)

```
{workspace}/
├── .kiro/
│   └── steering/
│       └── ai-pilc-workflow.md  ← Points to/contains core-workflow
├── ai-pilc-rules/
│   └── core-workflow.md         ← Master orchestration (always loaded)
└── ai-pilc-rule-details/
    ├── common/
    ├── inception/
    ├── assessment/
    ├── planning/
    └── definition/
```

Kiro auto-loads all `.kiro/steering/*.md` files. The core workflow file is the entry point — it references detail files as needed during execution.

### Other Platforms (Universal)

For platforms that use a single rules file:
1. The core workflow file (`core-workflow.md`) serves as the single entry point
2. Detail files are loaded on-demand when the workflow reaches relevant stages
3. Installation instructions specify which file to reference in the platform's config

---

## Coexistence (Multiple Packages)

Multiple AI-* packages can coexist in the same workspace:

```
{workspace}/
├── ai-pilc-rules/         ← Project Initiation
├── ai-pilc-rule-details/
├── ai-adlc-rules/         ← Architecture Design
├── ai-adlc-rule-details/
├── ai-dwg-rules/          ← Workspace Generator
├── ai-dwg-rule-details/
└── ai-gce-rules/          ← Governance Engine
    ai-gce-rule-details/
```

**Context management:** Only ONE package's core file is active per session. The AI loads the relevant workflow for the current task. Switching packages = starting a new session with a different core file loaded.

**Exception:** AI-GCE and AI-TGE run alongside AI-DLC v1 (concurrent, not sequential). Their rules coexist with whatever build workflow is active.

---

## What Gets Installed (Per Package)

| Package | Core File | Detail Files | Templates |
|---------|-----------|:------------:|:---------:|
| AI-ILC | `core-workflow.md` | 12 files | 6 templates |
| AI-PILC | `core-workflow.md` | 18 files | 14 templates |
| AI-ADLC | `core-workflow.md` | 25+ files | 13 templates |
| AI-DWG | `core-generator.md` | 30+ files | 48 templates |
| AI-GCE | `core-generator.md` | 20+ files | 12 templates |
| AI-TGE | `core-engine.md` | 18 files | 6 templates |
| AI-POLC | `core-workflow.md` | 15+ files | 10 templates |
| AI-UXD | `core-workflow.md` | 15+ files | 10 templates |

---

## The Core File Loading Pattern

Every package has exactly ONE core file that serves as the AI's entry point:

| Package Type | Core File Name | What It Does |
|-------------|---------------|--------------|
| Lifecycle packages | `core-workflow.md` | Orchestrates multi-stage interactive workflow |
| Generators | `core-generator.md` | Orchestrates one-shot generation with modes |
| Engines | `core-engine.md` | Orchestrates hybrid strategy + observation |

The core file:
1. Defines the package's role (persona adoption)
2. Lists all phases and stages
3. References detail files (loaded when stage is reached)
4. Defines chain contract (what it reads/produces)
5. Contains state management logic (resume/continuity)

Detail files are NOT pre-loaded — they're read on-demand when the workflow reaches their stage. This keeps context efficient.

---

## Version Management

Each package has a version in its README and core file. When updating:
1. Download/pull the new version
2. Replace the rules and details folders
3. Existing output (PIP, AP, DW, etc.) is NOT affected — it's already generated
4. State files remain valid across versions (backward compatible)

---

## Related Documents

| Document | Location |
|----------|----------|
| How Steering File Loading Works | `knowledge_docs/HOW_STEERING_FILE_LOADING_WORKS.md` |
| How Multi-Platform Support Works | `knowledge_docs/HOW_MULTI_PLATFORM_SUPPORT_WORKS.md` |
| How to Run the Full Chain | `knowledge_docs/HOW_TO_RUN_THE_FULL_CHAIN.md` |
| Family Structure | `FAMILY_STRUCTURE.md` |

*Knowledge Document | Created: 2026-06-12 | Updated: 2026-06-13 | Author: [Mohammad Maheri](https://www.linkedin.com/in/mohammad-maheri-8399565b)*
