---
name: neomano-x
description: Draft, revise, and publish X (Twitter) posts with an image using the X API. Use when the user asks for a tweet/post for X, wants to attach an image, and requires a human approval step (“PUBLICAR” or “PUBLISH”) before actually posting.
metadata: {"clawdbot":{"emoji":"𝕏","requires":{"bins":["python3"],"env":["X_API_KEY","X_API_SECRET","X_ACCESS_TOKEN","X_ACCESS_TOKEN_SECRET"]},"primaryEnv":"X_API_KEY"}}
---

## Safety / approval rule (mandatory)

- Never publish unless the user explicitly replies with **PUBLICAR** or **PUBLISH** (uppercase).
- Before publishing, always show the final text + the image you will use.

## Credentials (do not hardcode)

Provide these as environment variables (recommended: `~/.openclaw/.env` on the gateway machine):

- `X_API_KEY`
- `X_API_SECRET`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`

## One-time setup

### 1) Create the venv (once)

```bash
python3 {baseDir}/scripts/bootstrap_venv.py
```

Rationale: this avoids system-wide installs (PEP 668 / externally-managed Python) and keeps dependencies isolated to this skill.

Note: the `.venv/` directory is intentionally *not* shipped in the skill package; each user creates it locally.

### 2) If you do NOT have Access Token Secret (UI changed)

Use the OAuth 1.0a 3‑legged flow to obtain `X_ACCESS_TOKEN` + `X_ACCESS_TOKEN_SECRET`.

Prereq: set an allowed callback URL in your X app settings (any HTTPS URL is fine, even a dummy page).
Recommended: set `X_OAUTH_CALLBACK=https://example.com/callback` (and whitelist it in the app).

Start:

```bash
# run inside the venv
python3 {baseDir}/scripts/run.py dry-run --text "(noop)"  # just to verify venv exists
{baseDir}/.venv/bin/python {baseDir}/scripts/oauth1_flow.py auth-start
```

Open the printed `AUTH_URL`, approve, then copy `oauth_verifier` from the browser redirect URL.

Finish:

```bash
{baseDir}/.venv/bin/python {baseDir}/scripts/oauth1_flow.py auth-finish \
  --oauth-token "..." \
  --oauth-token-secret "..." \
  --oauth-verifier "..."
```

## Workflow

1. Ask for: tweet text idea + the image (a local path or an inbound media file path).
2. Produce a **draft** tweet (and alt-text suggestion for the image).
3. Iterate revisions until the user is happy.
4. When the user says **PUBLICAR** or **PUBLISH**:

```bash
python3 {baseDir}/scripts/run.py publish --text "..." --image "/path/to/image.jpg"
```

If the user did not approve, only run dry-run:

```bash
python3 {baseDir}/scripts/run.py dry-run --text "..." --image "/path/to/image.jpg"
```

## Notes

- Image upload uses the v1.1 media upload endpoint.
- Tweet creation uses the v2 tweets endpoint.
