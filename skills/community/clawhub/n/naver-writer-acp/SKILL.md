---
name: naver-writer-acp
description: Publish Naver Blog posts through the ACP marketplace flow (buyer-local thin-runner + sealed payload + offering execute). Use when a user asks to write/publish a Naver post, recover RUNNER_NOT_READY onboarding, run one-time thin-runner setup/login, or submit a publish job that should route through your ACP offering (`naver-blog-writer`) for paid service execution.
---

# Naver Writer ACP (Marketplace-connected)

Use this skill for the **real ACP commerce path**:

1. preflight local daemon
2. recover with setup_url when runner is not ready
3. one-time thin-runner setup/login
4. publish via ACP offering execute (paid path)

## Required runtime assumptions

- Buyer machine: macOS + `@y80163442/naver-thin-runner`
- Local daemon available on `127.0.0.1:${LOCAL_DAEMON_PORT:-19090}`
- For paid marketplace path: `OPENCLAW_OFFERING_EXECUTE_URL` is configured

## Core commands

## 1) Preflight

```bash
scripts/preflight.sh
```

If runner is not ready, it returns:

```json
{
  "error": "RUNNER_NOT_READY",
  "setup_url": "https://...",
  "next_action": "RUN_SETUP"
}
```

## 2) Setup runner (one-time)

```bash
scripts/setup_runner.sh --setup-url "<setup_url>"
# then user login once:
npx @y80163442/naver-thin-runner login
```

Or proof-based mode:

```bash
scripts/setup_runner.sh --proof-token "<proof_token>" --setup-issue-url "https://<control-plane>/v3/onboarding/setup-url/issue"
```

## 3) Publish

```bash
scripts/publish.sh --title "제목" --body "본문" --tags "tag1,tag2"
```

Publish flow:

- preflight
- `GET /v1/local/identity`
- `POST /v1/local/seal-job`
- submit to `OPENCLAW_OFFERING_EXECUTE_URL` (preferred, paid path)
- fallback: direct `/v2/jobs/dispatch-and-wait` (admin/internal only)

## Environment variables

See `references/setup.md`. Key variables:

- `X_LOCAL_TOKEN`
- `LOCAL_DAEMON_PORT` (default `19090`)
- `OPENCLAW_OFFERING_ID` (default `naver-blog-writer`)
- `OPENCLAW_OFFERING_EXECUTE_URL` (required for paid path)
- `PROOF_TOKEN`, `SETUP_ISSUE_URL` (for auto setup_url issue)

## Safety notes

- Never commit real tokens/keys.
- Keep `ACP_ADMIN_API_KEY` for internal debugging only.
- For real commerce metrics/billing, use offering execute path (not direct dispatch fallback).

## References

- `references/setup.md`
- `references/ops-checklist.md`
