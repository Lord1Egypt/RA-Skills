# code-reviewer

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8+-green.svg)](https://python.org)
[![Platforms](https://img.shields.io/badge/Platforms-Android%20%7C%20iOS%20%7C%20General-orange.svg)](#supported-platforms)

> AI-powered code review with severity grading. Platform-aware rules for Android, iOS, and general projects.

## ✨ What It Does

Point it at your code changes → get a structured review with **P0 / P1 / P2** severity grading. Auto-detects your platform and applies specialized rules across up to 9 review dimensions.

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

1. **Detect** — Identifies platform from project markers (`build.gradle` → Android, `*.xcodeproj` → iOS, `go.mod` → Go, `tsconfig.json` → TypeScript)
2. **Diff** — Extracts changes via `git diff` (staged, unstaged, commits, branches)
3. **Review** — AI applies platform/language-specific rules across multiple dimensions
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

### Android (9 dimensions)

Auto-detected by: `build.gradle*`, `AndroidManifest.xml`

| # | Dimension | What It Checks |
|---|---|---|
| 1 | **Thread safety** | Main-thread network/IO, SharedPreferences off main thread |
| 2 | **Deadlock & jank** | Nested locks, `runBlocking` on main thread, oversized `synchronized` blocks |
| 3 | **Memory management** | Activity/Context leaks, Handler inner-class retaining outer, Bitmap not recycled |
| 4 | **Lifecycle safety** | View access after `onStop`, ViewModel holding View reference, LiveData from wrong thread |
| 5 | **Logic correctness** | Integer overflow, float equality, concurrent collection modification |
| 6 | **Exception handling** | Swallowed exceptions, overly broad catch, exception thrown in `finally` |
| 7 | **Data consistency** | Transaction atomicity, cache/DB sync, state races in SSE/Flow |
| 8 | **API compatibility** | Missing `Build.VERSION.SDK_INT` guards, deprecated API usage |
| 9 | **Architecture** | ViewModel touching View directly, Repository with UI logic, illegal cross-module dependencies |

### iOS (9 dimensions)

Auto-detected by: `*.xcodeproj`, `Podfile`, `Package.swift`

| # | Dimension | What It Checks |
|---|---|---|
| 1 | **Threading safety** | UI updates off main thread, data races on shared state |
| 2 | **Deadlock & jank** | GCD deadlocks, main queue sync from main thread, blocking calls on main |
| 3 | **Memory safety** | Retain cycles in closures, unowned vs weak misuse, delegate strong references |
| 4 | **Resource leaks** | Unclosed file handles, NotificationCenter observers not removed, timer not invalidated |
| 5 | **Logic correctness** | Force unwrap crashes, index-out-of-bounds, incorrect optional chaining |
| 6 | **Exception handling** | Unhandled `Result` cases, missing `do-catch`, silent `try?` failures |
| 7 | **Data consistency** | CoreData context threading, UserDefaults race, Combine publisher state |
| 8 | **API compatibility** | Missing `@available` guards, deprecated API usage |
| 9 | **Architecture** | ViewController business logic, circular dependencies, broken MVVM/VIPER layer |

### General (7 dimensions)

Applied to any project not identified as Android or iOS.

| # | Dimension | What It Checks |
|---|---|---|
| 1 | **Correctness** | Logic errors, off-by-one, wrong operator precedence |
| 2 | **Thread safety** | Shared mutable state, missing synchronization |
| 3 | **Memory** | Leaks, unbounded growth, missing cleanup |
| 4 | **Performance** | N+1 queries, unnecessary allocations, blocking calls |
| 5 | **API design** | Unclear contracts, missing null checks, poor error types |
| 6 | **Error handling** | Unhandled error paths, silent failures |
| 7 | **Security** | Hardcoded secrets, injection risks, insecure storage |

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

- **Duplicate merging** — Same issue in 3+ files → merged into one finding with count
- **API change tracking** — Signature changed? Automatically checks if all callers are updated
- **Test coverage hints** — Changed code without test updates → gentle reminder
- **Large diff protection** — 5000+ lines → warns before proceeding
- **Auto-filtered files** — Skips generated code, binaries, lock files, vendor dirs



## 🏗 Architecture

```
code-reviewer/
├── SKILL.md                    # AI agent instructions
└── references/
    ├── review-general.md       # General review rules
    ├── review-android.md       # Android-specific rules (9 dimensions)
    ├── review-ios.md           # iOS-specific rules (9 dimensions)
    ├── review-typescript.md    # TypeScript-specific rules (7 dimensions)
    ├── review-go.md            # Go-specific rules (7 dimensions)
    └── review-skill-vetter.md  # Agent/LLM skill security review rules
```

## Requirements

- Git repository
- An AI coding assistant (OpenClaw, Claude Code, GitHub Copilot, etc.)

## Feedback

Found a bug or want a new language covered?
[Open an issue →](https://github.com/TimeAground/code-reviewer/issues)

## License

MIT
