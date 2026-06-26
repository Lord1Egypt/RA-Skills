---
name: ginstall-oneclick
version: 0.1.0
description: >-
  GInstall OneClick — one-click installation of GitHub projects: plan, clone,
  install Node deps, run dev scripts. Use when the user wants a GitHub Node.js
  repo set up locally via the ginstall CLI (monorepo tree URLs, GITHUB_TOKEN).
metadata:
  openclaw:
    requires:
      bins: [node, git]
    homepage: https://github.com/ginstall-oneclick/ginstall-oneclick
    envVars:
      - name: GITHUB_TOKEN
        required: false
        description: >-
          GitHub token (PAT) for private repositories or when unauthenticated
          raw/clone fails; optional for public repos only.
---

# GInstall OneClick — GitHub installer

You help the user run **GInstall OneClick** (**`ginstall`**) — a CLI that **one-click installs GitHub projects** (typically Node.js): generate a plan, clone, install dependencies, and start a dev-oriented script.

## When to trigger

- User pastes `owner/repo`, a full `github.com` URL, or a monorepo **`/tree/<branch>/<subpath>`** URL.
- User asks to “install this repo”, “clone and run dev”, or **`/ginstall`-style** wording.

## Prerequisites

- **`ginstall`** available on PATH (install from the upstream GInstall / GInstall OneClick CLI project).
- **`node`** and **`git`** on PATH (declared in skill metadata).

## Procedure

1. **Normalize URL** — accept `owner/repo`, `owner/repo@branch`, full `github.com` URLs, **`/tree/<branch>/<subpath>`** for monorepos.
2. **Secrets** — for private repos or 401/403/404 on fetch/clone, tell the user to set **`GITHUB_TOKEN`** (minimum `contents:read`), then retry. Never paste tokens into chat or save them into shared plan files.
3. **Run `ginstall` with quoted repo URL** — prefer:

```bash
ginstall "<repo-url>" --mode guided --env-mode scan
```

CI / non-interactive:

```bash
ginstall "<repo-url>" --yes --mode assisted --env-mode scan
```

Plan-only (no execute):

```bash
ginstall "<repo-url>" --mode manual --env-mode plan
```

4. **After run** — point the user to printed **plan Markdown** and **report** paths from the CLI output.

## Flags reference

| Flag / env | Role |
|------------|------|
| `--yes`, `CI`, `GINSTALL_NON_INTERACTIVE`, `GINSTALL_YES` | Non-interactive; auto-approve steps |
| `--mode` / `GINSTALL_MODE` | `manual` \| `guided` \| `assisted` \| `auto` |
| `--env-mode` / `GINSTALL_ENV_MODE` | `manual` \| `scan` \| `plan` |
| `--run-timeout` / `GINSTALL_RUN_TIMEOUT` | Dev/run step cap (seconds) |
| `--work-dir` / `-w` | Workspace root for clone + logs |
| `GITHUB_TOKEN` | Private GitHub + authenticated HTTPS clone |

## Verification

- Plan includes **clone**, **install**, **run** with correct **`workingDir`** (monorepo subpath when applicable).
- Warn on **engines.node** mismatch, optional **native toolchain** for packages like `sharp`.

## Usage examples (ClawHub)

1. **Interactive:** User says “Install https://github.com/microsoft/TypeScript locally with GInstall.” → run  
   `ginstall "https://github.com/microsoft/TypeScript" --mode guided --env-mode scan`

2. **Monorepo:** User provides `https://github.com/org/mono/tree/main/packages/app` → quote the full tree URL in `ginstall "<url>"`.

3. **Automation:** User wants CI setup with no prompts →  
   `ginstall "owner/repo" --yes --mode assisted --env-mode scan`

## Upstream CLI

This file is the **OpenClaw skill** only. Install or build **`ginstall`** from the GInstall OneClick CLI repository:

<https://github.com/YunzhouLi-hub/GInstall-OneClick>
