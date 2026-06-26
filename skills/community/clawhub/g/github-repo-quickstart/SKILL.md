---
name: github-repo-quickstart
description: Use when the user wants a fast, low-friction onboarding guide for an unfamiliar GitHub repository. Trigger when a GitHub repo URL is provided, or when the user asks how to quickly understand a repo's purpose, architecture, setup, dependencies, entrypoints, releases, or maintenance status.
---

# GitHub Repo Quickstart

## Overview

This skill produces a compressed, developer-first onboarding guide for an unfamiliar GitHub repository.
It is for cases where the user wants to understand the repo quickly and start using it immediately, without reading the entire README or source tree.

This document stays in English.
Actual user-facing output must follow the user's language by default.
If the user explicitly requests another language, follow the user's explicit request instead.
This rule applies to headings, explanations, directory-tree annotations, pitfalls, and all other visible output.

## Required Workflow

When the user provides a GitHub repository URL, execute the workflow in this exact order.
Do not skip a step unless the repository is inaccessible.

### 1. Fetch_Repo_Skeleton

Goal: identify the repo shape before interpreting details.

Collect:
- Primary language or languages
- Frameworks and runtime family
- Monorepo or single-project layout
- Top-level directory tree
- Build files, package manifests, Docker files, CI files, env examples, and config roots

If an environment provides a helper literally named `Fetch_Repo_Skeleton`, use it first.
Otherwise emulate it with GitHub MCP, repository tree inspection, and manifest discovery.

### 2. Analyze_Dependencies

Goal: understand how the repo is expected to run.

Collect:
- Package managers and dependency manifests
- Runtime versions from files such as `.nvmrc`, `.python-version`, `go.mod`, `Cargo.toml`, `pyproject.toml`, Dockerfiles, toolchain files, or CI configs
- Environment setup hints
- Preferred local setup path
- Whether Docker or Docker Compose is the safest path
- Hidden system dependencies and likely conflicts

If an environment provides a helper literally named `Analyze_Dependencies`, use it first.
Otherwise infer from manifests, Docker files, lockfiles, CI, and task runners.

### 3. Locate_Entrypoints

Goal: show the shortest path into the core business logic.

Collect:
- Main server, CLI, worker, or library entrypoints
- Boot sequence: config load, dependency wiring, database or cache initialization, HTTP or RPC server startup, command dispatch, job loop, or request pipeline
- One or two files the user should read first

If an environment provides a helper literally named `Locate_Entrypoints`, use it first.
Otherwise infer from `main.*`, `cmd/`, `src/main.*`, framework boot files, router setup, and executable targets.

### 4. Check_Releases_And_Health

Goal: prevent the user from onboarding onto a dead or misleading version.

Collect:
- Latest usable release or latest stable tag
- Direct release link
- Maintenance signal: active, slow-moving, or likely unmaintained
- Evidence such as recent commits, release cadence, issue activity, or archived status

If an environment provides a helper literally named `Check_Releases_And_Health`, use it first.
Otherwise inspect GitHub releases, tags, recent commits, and repository metadata.

## Operating Rules

- Never copy the README verbatim. Distill and verify.
- Favor primary evidence from the repository itself over marketing language.
- If Docker exists and looks maintained, recommend Docker first.
- If Docker exists but is obviously stale or incomplete, say so and prefer the local path.
- Prefer commands that are directly copy-pasteable.
- Be explicit about version traps, OS-level dependencies, GPU or CUDA requirements, private submodules, generated code, or outdated docs.
- If evidence is incomplete, say what is confirmed and what is inferred.
- Keep the answer extremely compact. The reader is a developer, not a stakeholder.
- Match the user's language for all user-visible wording.
- If the user's message is mixed-language, follow the dominant language unless the user explicitly asks otherwise.

## Output Contract

Return a Markdown document titled `Repository Quickstart Guide`, but translate the title and section headings into the user's language unless the user explicitly asked for English.
Use the following section structure and keep the tone professional, direct, and practical.

### 1. One-Minute Overview

Include:
- `Core Positioning`: one sentence on what the repo does and what pain it solves
- `Tech Stack`: main language plus primary framework or runtime shape
- `Project Health`: maintenance status, latest release version, and direct download or release link

### 2. Architecture & Tree

Requirements:
- Show only the core tree
- Omit tests, fixtures, static assets, screenshots, and low-signal files unless they are essential to bootstrapping
- Every important directory or file in the tree must have a brief annotation in the user's language

Example style:

```text
repo/
├── cmd/                  # Stores executable entrypoints
├── internal/             # Core business logic
├── pkg/                  # Reusable shared libraries
├── configs/              # Config files and templates
└── Dockerfile            # Container startup path
```

### 3. Quick Start

Include:
- The safest environment recommendation
- Docker-first commands if Docker is the best option
- Clone and dependency-install commands
- Run commands
- A short `Pitfalls` subsection with only high-value traps

Command blocks must be directly executable and minimal.

### 4. Core Logic Navigator

Include:
- A direct sentence equivalent to `If you want to understand the core logic, start from ...`
- The first one or two files to read
- A short execution-flow summary in order
- A practical reading path, not an exhaustive architecture essay

## Response Style

- Keep SKILL.md in English, but generate user-facing output in the user's language
- Be concise, specific, and implementation-oriented
- Prefer file paths over vague descriptions
- Avoid generic praise and filler
- Do not overwhelm the user with exhaustive subsystem coverage
- Optimize for helping the user start coding in minutes
