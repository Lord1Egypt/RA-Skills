---
name: peripheral-vision
version: 1.0.0
description: >
  Monitors adjacent systems, upstream dependencies, and downstream consumers
  for changes that could affect your current work — before they break it.
  Like biological peripheral vision detects movement at the edges of your
  visual field, this skill detects movement at the edges of your code's
  dependency field.
author: J. DeVere Cooley
category: situational-awareness
tags:
  - dependency-monitoring
  - change-detection
  - context-awareness
  - proactive
metadata:
  openclaw:
    emoji: "👁️"
    os: ["darwin", "linux", "win32"]
    cost: free
    requires_api: false
    tags:
      - zero-dependency
      - cognitive
      - awareness
---

# Peripheral Vision

> "You don't crash because you weren't looking ahead. You crash because you weren't looking to the side."

## What It Does

When you're deep in a module, your attention is foveal — focused on the code directly in front of you. But the code that breaks your work is rarely the code you're staring at. It's the code *next to* it: the upstream service that changed its response format, the downstream consumer that started sending unexpected input, the shared utility that someone refactored while you were mid-feature.

Peripheral Vision creates a **situational awareness field** around your current work context. It continuously scans the edges of your attention and alerts you to changes that are:
1. Not in the files you're editing
2. But in files that your files depend on, interact with, or assume stability from

## The Awareness Model

### Visual Field Anatomy

In human vision:
- **Foveal**: The 2° center. Maximum detail. Where you're looking right now.
- **Parafoveal**: The next 5°. Some detail. Aware but not focused.
- **Peripheral**: Everything else. No detail. Detects motion and threats.

In code:
| Zone | Code Equivalent | What Peripheral Vision Does |
|---|---|---|
| **Foveal** | Files you're actively editing | Nothing (you're already looking here) |
| **Parafoveal** | Files directly imported/called by your files | Monitors for recent changes |
| **Peripheral** | Files that interact transitively — shared deps, consumers, upstream providers | Scans for changes that could cascade to you |
| **Blind Spot** | Files you have no awareness of but are connected through implicit channels (shared DB, env vars, runtime config) | Attempts detection through co-change analysis |

## The Six Peripheral Channels

### Channel 1: Upstream Drift
**Monitors:** Libraries, modules, and services your code imports or calls.

```
SCANS FOR:
├── Interface changes (new required params, removed fields, renamed exports)
├── Behavioral changes (same interface, different semantics)
├── Version bumps in dependencies that affect your used surface area
├── Deprecation warnings for functions you actively use
└── Changelog entries tagged "breaking" in your dependency tree
```

### Channel 2: Downstream Pressure
**Monitors:** Code that imports, calls, or depends on your code.

```
SCANS FOR:
├── New consumers of your module you didn't know about
├── Consumers using your code in ways you didn't intend
├── Consumers that would break if you change your current interface
├── Test files in other modules that test your behavior (coupling signal)
└── Downstream code that reimplements your functionality (trust signal)
```

### Channel 3: Sibling Mutations
**Monitors:** Other files in your module or directory that were recently changed by someone else.

```
SCANS FOR:
├── Changes to shared utilities, helpers, or constants you use
├── Changes to configuration files that affect your module's behavior
├── New files that might conflict with or duplicate your current work
├── Refactors that changed naming conventions your code follows
└── Changes to test infrastructure or fixtures your tests depend on
```

### Channel 4: Schema Tremors
**Monitors:** Database schemas, API contracts, protobuf definitions, GraphQL types — any shared data shape.

```
SCANS FOR:
├── Column additions/removals in tables your code queries
├── Type changes in fields your code reads or writes
├── New constraints (NOT NULL, UNIQUE) that could cause your writes to fail
├── API version changes in services you consume
└── Protobuf/GraphQL field deprecations or renames
```

### Channel 5: Environmental Shifts
**Monitors:** Infrastructure, configuration, and deployment context changes.

```
SCANS FOR:
├── Changes to environment variables your code reads
├── Changes to Docker/container configurations
├── CI/CD pipeline modifications that affect your build/test/deploy
├── Infrastructure changes (new regions, changed timeouts, updated limits)
└── Changes to shared tooling (linter rules, formatter settings, build configs)
```

### Channel 6: Temporal Neighbors
**Monitors:** Files that historically change at the same time as your files (co-change analysis).

```
SCANS FOR:
├── Files that have changed in the same commit as your files > 3 times
├── Files that have changed within 24h of your files > 5 times
├── Files that have triggered the same CI failures as your files
└── Files that share the same bug-fix pattern as your files
```

## How It Works

```
Phase 1: CONTEXT CAPTURE
├── Identify the foveal zone (files currently open/modified)
├── Trace parafoveal zone (direct dependencies, both import and export)
├── Map peripheral zone (transitive deps, shared resources, co-changers)
└── Identify blind spots (connected through implicit channels)

Phase 2: CHANGE DETECTION
├── For each zone, detect changes since your work started:
│   ├── Git: commits by others to files in your awareness field
│   ├── Schema: migrations or type definition changes
│   ├── Config: environment or infrastructure changes
│   └── Dependency: upstream version bumps or changelog entries
├── Classify each change by relevance to your current work
└── Score impact probability (how likely this affects you)

Phase 3: ALERT TRIAGE
├── Filter out noise (changes with < 20% impact probability)
├── Classify remaining by urgency:
│   ├── STOP: Your current work may be invalidated
│   ├── REVIEW: Your current work should account for this
│   ├── NOTE: Awareness-only, no action needed yet
│   └── EMERGING: Pattern forming, not yet actionable
└── Generate contextual alert with specific implications for your work

Phase 4: CONTINUOUS MONITOR
├── Re-scan periodically (configurable interval)
├── Update awareness field as your focus shifts
├── Accumulate pattern data for temporal neighbor analysis
└── Fade old alerts that are no longer relevant
```

## Alert Format

```
╔══════════════════════════════════════════════════════════════╗
║               PERIPHERAL VISION ALERT                       ║
║          Context: You're working on src/checkout/            ║
╠══════════════════════════════════════════════════════════════╣
║                                                              ║
║  🔴 STOP (1)                                                 ║
║  ├── [Schema] payments table: 'currency' column type changed ║
║  │   from varchar(3) to enum — your INSERT will fail         ║
║  │   Changed by: @devB in migration 2025_03_01_alter_pmts    ║
║  │   Action: Update PaymentBuilder to use enum values        ║
║                                                              ║
║  🟡 REVIEW (2)                                               ║
║  ├── [Upstream] CartService.getTotal() now returns            ║
║  │   {amount, currency} instead of just amount               ║
║  │   Changed by: @devC in commit a8f3d2e (2h ago)            ║
║  │   Action: Destructure correctly or your amounts are objects║
║  │                                                           ║
║  ├── [Sibling] src/checkout/utils.ts was refactored          ║
║  │   formatPrice() renamed to formatCurrency()               ║
║  │   Changed by: @devA in commit b9c4e1f (4h ago)            ║
║  │   Action: Update your imports before pushing              ║
║                                                              ║
║  🔵 NOTE (1)                                                 ║
║  ├── [Temporal] test/fixtures/cart-data.json was updated     ║
║  │   This file co-changes with checkout/ 73% of the time     ║
║  │   Your checkout tests may need updated fixtures            ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

## When to Invoke

- When starting a new feature branch (establish your awareness field)
- Before committing (check what changed around you while you were focused)
- Before opening a PR (ensure your work accounts for parallel changes)
- After pulling from main (understand what landed near your code)
- When a CI build fails unexpectedly (was it your change or a peripheral one?)

## Why It Matters

The most frustrating bugs aren't the ones you introduced. They're the ones that were introduced *next to* you, while you were focused on your own work, in code you had no reason to look at. By the time you discover them, you've built on top of broken assumptions.

Peripheral Vision doesn't replace careful code review. It gives your code review **peripheral awareness** — so you're not just reviewing what changed, but what changed *around* what changed.

Zero external dependencies. Zero API calls. Pure git and static analysis.
