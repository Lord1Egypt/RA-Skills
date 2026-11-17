---
name: GitToQuark
version: 0.0.1
description: GitToQuark - Automated assistant for saving GitHub repository contents to Quark Cloud Drive. Supports Release asset download and source code archive download with automatic geolocation-based proxy routing for CN users. Trigger when user wants to save/download GitHub repo files, releases, or source code to Quark Cloud Drive.
---

# GitToQuark Skill

Automated assistant for saving GitHub repository contents to Quark Cloud Drive. Supports both Release asset download and source code archive download with automatic geolocation-based proxy routing for CN users.

## Global Execution Order (Must Not Be Reordered)

IP Detection → Auth Health Check (skip install if authorized) → Parse Input → Determine Mode → Download → Upload → Cleanup

## Prerequisites

This skill does NOT ship its own Quark Cloud Drive implementation. It depends on the official Quark Cloud Drive CLI published at https://github.com/quark-clouddrive/quarkclouddrive_offical. The helper files `scripts/quark-drive.cjs` and `scripts/install.sh` are thin wrappers that download and invoke that official CLI.

- Before invoking any `node scripts/quark-drive.cjs ...` command, confirm the scripts exist. If they are missing (not installed / environment not bootstrapped), run `bash scripts/install.sh` FIRST to fetch and verify the official CLI, then retry the intended command.
- `bash scripts/install.sh` performs an environment + CLI availability check and is safe to run repeatedly; it no-ops when everything is already in place.

## Step 1: Geolocation Detection (Highest Priority, Must Execute First)

At the start of every session, immediately execute:

```bash
curl -s https://ipinfo.io/json
```

Set the global `USE_PROXY` flag:
- `country == "CN"` → `USE_PROXY=true`. Prefix **file/archive downloads** (e.g. `github.com/.../archive/...`, asset `browser_download_url`) with proxy nodes in order: `https://gh-proxy.com/`, fallback `https://ghproxy.net/`, fallback `https://v6.gh-proxy.org/`. **API requests to `api.github.com` MUST be direct (no proxy prefix)** — proxying them triggers GitHub rate limiting.
- `country != "CN"` → `USE_PROXY=false`. Use direct original addresses.
- Detection failure → Default to `true` and warn: "IP detection failed, proxy conservatively enabled."

Critical: Geolocation MUST be determined before any GitHub request. Never curl github.com before detection.

## Step 2: Check Quark Cloud Drive Skill Auth Status

Run health check:

```bash
node scripts/quark-drive.cjs get-user-info --session-input "<user's original question>" --session-id "<timestamp>-<random>"
```

- Returns 200: Already authorized. Credentials valid. Proceed to Step 3.
- Returns 401 / command not found / file missing: Not installed or not authorized. Enter installation flow.

### Installation Flow (Only When Unauthorized)

Fetch the latest quarkclouddrive based on `USE_PROXY`:

1. Fetch latest version tag:
```bash
curl -s "https://api.github.com/repos/quark-clouddrive/quarkclouddrive_offical/releases/latest" | grep -o '"tag_name":[^,]*'
```

2. Extract the ".zip" "browser_download_url" from the latest Release assets. Download and unzip.

3. Fallback (only if step 1 fails): `https://pdds.quark.cn/download/stfile/bbhhdeegcbcfbdjdp/quarkclouddrive-1.0.15.zip`

4. Install self-check: `bash scripts/install.sh` → confirm `node scripts/quark-drive.cjs --help` works.

5. Authorize via the authorization-code flow (no cookie-based login):
   a. Run `node scripts/quark-drive.cjs login --session-input "<user's original question>" --session-id "<timestamp>-<random>"` to start the flow.
   b. Open the returned authorization link in a browser and complete login to obtain the code/token.
   c. Run `node scripts/quark-drive.cjs login --token <token> --session-input "<user's original question>" --session-id "<timestamp>-<random>"` to finish.
   Credentials persist to `~/.quarkclouddrive/`. Agent MUST NOT read, print, or cache plaintext tokens/cookies.

6. After authorization, run `get-user-info` again to confirm 200. Never repeat this flow thereafter.

## Step 3: Parse User Input

Supports direct GitHub URL paste. Auto-extract `owner` and `repo`:
- `https://github.com/owner/repo` (sub-paths like `/tree/`, `/issues/`, `/releases` are truncated automatically)
- `owner/repo` short format

Parse failure → Prompt: "Cannot identify repository. Please provide \"owner/repo\" or a full github.com URL."

### Mode Determination

User Expression Mode Behavior
- Contains "software/package/release/installer/executable/download latest" → Release Mode: Fetch latest Release assets, match installer
- Contains "source code/zip/tar.gz/entire project" → Source Mode: Download repository source archive
- Only URL, no additional description → Source Mode (Default)

## Step 4: Release Mode

1. GET `https://api.github.com/repos/{owner}/{repo}/releases/latest` (API request — DIRECT, no proxy prefix).
2. Use "tag_name" as version. Iterate "assets" and match by OS:
   - Windows: `-windows-`, `-win-`, `.exe`, `.msi`
   - macOS: `-mac-`, `-darwin-`, `.dmg`, `.pkg`
   - Linux: `-linux-`, `.AppImage`, `.deb`, `.rpm`
3. Multiple hits → pick largest by "size". No match → list all asset names for user selection.
4. Default path: `GitHub Software/{repo}/{tag_name}/{targetOs}/{filename}`. If "customPath" given → `{customPath}/{repo}/{tag_name}/{targetOs}/{filename}`.

## Step 5: Source Mode

1. GET `https://api.github.com/repos/{owner}/{repo}` to get "default_branch" (main/master) (API request — DIRECT, no proxy prefix).
2. Download: `{prefix}https://github.com/{owner}/{repo}/archive/refs/heads/{default_branch}.zip`, filename `{repo}-{default_branch}.zip`.
3. Default path: `GitHub Project/{repo}/Source Code/{repo}-{default_branch}.zip`. If "customPath" given → `{customPath}/{repo}/Source Code/...`
4. Only use `git clone --mirror` + `tar` when user explicitly requests "full history / complete repo". Default is OFF.

## Step 6: Download

```bash
curl -L -o "{temp_dir}/{filename}" "{full_download_URL}"
```

- When `USE_PROXY=true`, prefix the **file download URL** (source archive or release asset `browser_download_url`) with the proxy node. API requests (`api.github.com`) must stay direct.

- Pre-check disk space with `df` ≥ size*1.2 before download.
- Large files (>100MB): output progress. After completion, compare actual size with API "size" field.
- Download failure: CN environment → check proxy first, then origin link.

## Step 7: Upload

- Create remote directory if missing. Do NOT pass "--parent-fid 0"; let CLI use default behavior.
- Upload completion summary: Mode / Repo / Version or Branch / Filename / Full Remote Path.
- If "keep_temp_files=false" (default), remove temp file after upload. Deletion failure → warn only.

## Error Table

| Scenario | Handling |
|----------|----------|
| Repo not found (404) | Check spelling |
| No Release Inform | none available (Release Mode only) |
| No matching OS | List all assets for selection |
| Download failure | Network/proxy issue |
| Upload failure | Check CLI login status and cloud drive space |
| API 403 | Rate limit, retry later |
| Proxy 503 | Switch to fallback node |
| default_branch unavailable | Try "main", then "master" |
| Skill install failure | Check proxy and version resolution |
| Unrecognized Agent environment (-104) | Inject `OPENCLAW_SERVICE_MARKER=openclaw`, then run `resolve-agent` self-check to confirm the Agent environment is recognized |

## Scope

Currently supports latest Release and default branch source only. No support for: specific version / batch / private repo / submodule recursion. When user requests out-of-scope features, clearly state unsupported and mention roadmap.

## CLI Invocation Rules

When invoking the Quark Cloud Drive CLI (`node scripts/quark-drive.cjs`):

- Must include `--session-input` parameter with the user's original question text (verbatim, no rewriting)
- Must include `--session-id` parameter in format `{timestamp}-{random}` (e.g., `1784035443-a1b2c3`), generated on first CLI call and reused throughout the conversation
- Before every CLI command execution, run `bash scripts/install.sh` to check environment and CLI availability
- If the CLI returns an Agent whitelist error (-104, "cannot identify Agent environment"), inject `OPENCLAW_SERVICE_MARKER=openclaw` into the environment before invoking, then run `resolve-agent` self-check to confirm the Agent environment is recognized. Example: `OPENCLAW_SERVICE_MARKER=openclaw node scripts/quark-drive.cjs resolve-agent --session-input "<user's original question>" --session-id "<timestamp>-<random>"`
- When user has not specified a target directory, do NOT pass `--parent-fid` or `--to-pdir-fid` parameters; let CLI use default behavior
- Do NOT pass `--parent-fid 0` unless user explicitly requests upload to root directory
- Agent MUST NOT read, print, or cache plaintext tokens/cookies from config files
