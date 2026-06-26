---
name: lobster-rank
description: Scan locally installed OpenClaw skills, collect evidence data, submit to the lobster ranking server for scoring, and let the user confirm uploading their result to the public leaderboard. Use when the user asks to score, rate, evaluate, rank, or certify their lobster / AI agent capability set, or wants to upload their score to the leaderboard.
dependencies:
  env:
    - name: OPENCLAW_API_KEY
      description: Lobster leaderboard API key. Obtain from https://lobster-rank.wondercv.com/me. Can also be passed via --api-key flag.
      required: true
  network:
    - host: lobster-rank.wondercv.com
      purpose: Lobster leaderboard server (operated by skill publisher). Receives skill metadata for scoring.
  localFiles:
    - path: "~/.openclaw/openclaw.json or ~/Library/Application Support/QClaw/openclaw/config/openclaw.json"
      purpose: Read apiKey field only for authentication. No other fields are used or transmitted.
---

# Lobster Rank

This skill scans your locally installed OpenClaw skills, collects metadata (skill names, structure flags, file counts, descriptions), and submits it to the lobster leaderboard server for scoring. No file contents, credentials, or personal data are sent — only structural metadata and heuristic signals. The scoring algorithm runs server-side.

## Prerequisites

You need a **Lobster API Key** before submitting.

- Get it at: https://lobster-rank.wondercv.com/me
- Set it as an environment variable for convenience:
  ```bash
  export OPENCLAW_API_KEY=your_key_here
  ```
- Or pass it directly with `--api-key` on every command.

> **Privacy note:** The script reads `openclaw.json` only to extract your `apiKey` field for authentication — no other fields are used or transmitted. It collects skill metadata (skill names, whether scripts/references/assets exist, file count, description) and heuristic signals (multi-model usage, log availability). No file contents, credentials, or personal data are sent. All data is submitted to the leaderboard server at `https://lobster-rank.wondercv.com` which is operated by the skill publisher.

## Workflow

### Step 1 — Scan & Submit

Run the scanner. It collects metadata about your installed skills and sends the raw data to the server for scoring.

```bash
python3 scripts/lobster_submit.py
```

With explicit API key:

```bash
python3 scripts/lobster_submit.py --api-key lbk_xxxxxxxxxxxx
```

**Live Challenge mode** (higher credibility, blends in a real-time challenge score):

```bash
python3 scripts/lobster_submit.py --mode live-challenge --challenge-score 85
```

**Dry run** (scan only, do not send to server):

```bash
python3 scripts/lobster_submit.py --dry-run
```

### Step 2 — Review the Result

The script prints the score returned by the server. Present it to the user in a readable format, including:

- Total score and grade
- Title
- Number of skills counted
- Evaluation mode
- Pending token expiry time

Ask the user: **"要将这个成绩上传到排行榜吗？"**

If they say yes, proceed to Step 3. If no, stop — the pending score stays valid for 24 hours and can be confirmed on the website.

### Step 3 — Confirm Upload

Pass the `pending_token` from Step 2:

```bash
python3 scripts/lobster_submit.py --confirm <pending_token>
```

On success the script prints a confirmation. Tell the user their score is now on the leaderboard.

### Step 4 — View on Leaderboard

Direct the user to:

```
https://lobster-rank.wondercv.com
```

Or their personal page:

```
https://lobster-rank.wondercv.com/me
```

## Discovery Paths

The scanner checks these locations for skills:

- `~/.openclaw/workspace/skills`
- `~/Library/Application Support/QClaw/openclaw/config/skills`

And these for config / logs:

- `~/.openclaw/openclaw.json`
- `~/Library/Application Support/QClaw/openclaw/config/openclaw.json`
- `~/Library/Logs/QClaw/openclaw`

To scan a custom path:

```bash
python3 scripts/lobster_submit.py --root /path/to/skills
```

## Rules

- Do not invent skills or fabricate evidence.
- The scoring algorithm runs server-side; do not attempt to predict or influence it.
- If no user-installed skills are found, stop and report the issue.
- If the API key is missing or invalid, ask the user to retrieve it from https://lobster-rank.wondercv.com/me.
- If the pending token has expired, re-run Step 1 to get a fresh evaluation.
