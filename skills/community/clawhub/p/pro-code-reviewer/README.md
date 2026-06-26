# code-reviewer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Platforms](https://img.shields.io/badge/Platforms-Android%20%7C%20iOS%20%7C%20General-orange.svg)](#supported-platforms)

> AI-powered code review with severity grading. Platform-aware rules for Android, iOS, and general projects.

## ✨ What It Does

Point it at your code changes → get a structured review with **P0 / P1 / P2** severity grading. Auto-detects your platform and applies specialized rules.

```
> review

✅ 2 issues found

P0 🔴 Coroutine launched in Activity without lifecycle scope
   src/MainActivity.kt:42
   → Use lifecycleScope.launch instead of GlobalScope.launch

P1 🟡 RecyclerView adapter not using DiffUtil
   src/adapter/UserAdapter.kt:15
   → Replace notifyDataSetChanged() with DiffUtil for better performance
```

## 🧠 How It Works

1. **Detect** — Identifies platform from project files (`build.gradle` → Android, `*.xcodeproj` → iOS)
2. **Diff** — Extracts changes via `git diff` (staged, unstaged, commits, branches)
3. **Review** — AI applies platform-specific rules across multiple dimensions
4. **Report** — Outputs structured findings with severity, location, and fix suggestions

## 🎯 Three Review Modes

| Mode | Command | Focus |
|---|---|---|
| **Standard** | `review` | Full review — P0, P1, P2 |
| **Quick** | `quick review` | P0 only — "can I merge this?" |
| **Security** | `security review` | Injection, auth bypass, key leaks |

## 📋 Severity Levels

| Level | Meaning | Examples |
|---|---|---|
| **P0** 🔴 | Must fix | Crash, data loss, security vulnerability, deadlock |
| **P1** 🟡 | Should fix | Race condition, resource leak, unhandled error path |
| **P2** 🔵 | Nice to have | Naming, structure, minor redundancy |

## Supported Platforms

| Platform | Auto-detect | Review Dimensions |
|---|---|---|
| **Android** | `build.gradle*`, `AndroidManifest.xml` | Lifecycle safety, coroutine leaks, Room transactions, ProGuard, 9 dimensions total |
| **iOS** | `*.xcodeproj`, `Podfile`, `Package.swift` | Threading safety, retain cycles, dispatch deadlocks, 9 dimensions total |
| **General** | Everything else | Correctness, thread safety, memory, performance, API design, error handling, security |

## 🚀 Quick Start

### Install

```bash
# OpenClaw
clawhub install code-reviewer

# Claude Code
cp -r code-reviewer/ your-project/.claude/skills/

# GitHub Copilot
cp -r code-reviewer/ your-project/.agents/skills/
```

### Use

```
review                    # All uncommitted changes
review staged             # Only staged changes
review abc1234            # Specific commit
review last 5 commits     # Recent commits
review branch feature-x   # Branch diff vs main
```

## 🛡 Smart Behaviors

- **Duplicate merging** — Same issue in 3+ files → merged into one finding
- **API change tracking** — Signature changed? Checks if callers are updated
- **Test coverage hints** — Changed code without test updates → gentle reminder
- **Large diff protection** — 5000+ lines → warns before proceeding
- **Auto-filtered files** — Skips generated code, binaries, lock files, vendor dirs

## 📄 HTML Reports

```
review, generate HTML report
```

Saves to `.code-reviews/` and opens in browser. Add `.code-reviews/` to `.gitignore`.

For a deterministic local pipeline (generate template JSON / validate JSON / render HTML) when HTML is requested, use:
`scripts/run_review.ps1` (PowerShell) or the Python scripts in `scripts/`.

## 🏗 Architecture

```
code-reviewer/
├── SKILL.md                    # AI agent instructions
├── evals/
│   └── evals.json               # Regression prompts
├── references/
│   ├── review-general.md       # General review rules (7 dimensions)
│   ├── review-android.md       # Android-specific rules (9 dimensions)
│   └── review-ios.md           # iOS-specific rules (9 dimensions)
└── scripts/
    ├── make_review_json.*      # JSON template generator (py/ps1)
    ├── render_report.*         # HTML report renderer (py/ps1)
    └── run_review.ps1          # One entry point (validate + render)
```

## Requirements

- Git repository
- An AI coding assistant (OpenClaw, Claude Code, GitHub Copilot, etc.)

## License

MIT
