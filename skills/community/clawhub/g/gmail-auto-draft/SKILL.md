---
name: gmail-auto-draft
description: Monitor Gmail inbox, read incoming emails, generate personalized follow-up replies with OpenAI, and save replies into Gmail Drafts for human review. Use when the user wants Gmail auto-monitoring, AI-assisted client email responses, draft-before-send workflows, or agency inbox automation.
---

# Gmail Auto Draft

Use this skill to build or run a review-safe Gmail reply workflow: read new emails, generate AI reply text, and save drafts instead of sending directly.

## Quick workflow

1. Prepare Google OAuth credentials.
2. Use local GMN endpoint (`openclaw:main`) or set external OpenAI key.
3. Run one-shot mode to validate draft creation.
4. Tune query and prompt style.
5. Switch to polling mode for continuous monitoring.

## Run commands

Install dependencies:

```bash
cd skills/gmail-auto-draft/scripts
python3 -m pip install -r requirements.txt
```

Default backend (local GMN via OpenClaw gateway):

```bash
export OPENAI_BASE_URL="http://127.0.0.1:18789/v1"
export OPENAI_MODEL="openclaw:main"
```

Or use OpenAI directly:

```bash
export OPENAI_API_KEY="your_openai_key"
export OPENAI_MODEL="gpt-4o-mini"
```

One-shot test:

```bash
./run_once.sh --auth-mode local --max-emails 3
```

Continuous monitor:

```bash
./run_once.sh --poll-interval 60 --max-emails 5 --mark-read
```

Upwork demo profile (lead-focused query + fixed agency tone):

```bash
./run_upwork_demo.sh --auth-mode local --max-emails 5
```

## Common options

- `--query`: Gmail search filter for target emails.
- `--max-emails`: max messages per cycle.
- `--poll-interval`: seconds between cycles (`0` means run once).
- `--openai-model`: model name (default `openclaw:main`).
- `--openai-base-url`: OpenAI-compatible base URL (default `http://127.0.0.1:18789/v1`).
- `--agency-profile`: business context for OpenAI prompt.
- `--agency-profile-file`: load agency context from a text file.
- `--style-rules`: response style constraints.
- `--style-rules-file`: load style rules from a text file.
- `--query-file`: load Gmail query from a text file.
- `--mark-read`: mark processed messages as read.
- `--processed-label`: label for already drafted emails (default `openclaw_auto_drafted`).

## Output behavior

The script prints JSON for each cycle:
- `processed`: number of drafted replies
- `created_drafts`: draft metadata
- `skipped`: skipped message reasons
- `errors`: per-message errors

## Resources

- Script: `scripts/gmail_auto_draft.py`
- Runner: `scripts/run_once.sh`
- Demo runner: `scripts/run_upwork_demo.sh`
- Dependencies: `scripts/requirements.txt`
- Setup guide: `references/setup.md`
- Prompt/query tuning: `references/prompt-tuning.md`
- Demo config: `references/upwork-demo/agency_profile.txt`
- Demo config: `references/upwork-demo/style_rules.txt`
- Demo config: `references/upwork-demo/gmail_query.txt`
