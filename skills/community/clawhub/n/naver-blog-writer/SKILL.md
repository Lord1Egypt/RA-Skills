# Naver Blog Publisher

Publish prepared content to Naver Blog from an authenticated local browser on the buyer machine.

Best for:
- `naver publish`
- `naver blog publish`
- `korean blog publish`

First run:
- `doctor -> setup -> dry_run -> login once -> live`

Production support:
- `macOS`

Use when:
- a user already has final content and wants `naver publish`, `naver blog publish`, or `korean blog publish`
- an OpenClaw agent needs a reliable publish endpoint, not a writing/SEO ideation tool
- the buyer can run a local Mac runner and complete one-time Naver login

Do not use when:
- the user needs the post drafted from scratch
- the environment cannot run a local runner
- the task is only research, SEO planning, or topic ideation

Inputs:
- `TITLE`
- `BODY`
- optional `TAGS`
- optional `PUBLISH_AT`

Outputs:
- live publish: `naver_publish_result`
- preview: `dry_run` result with synthetic `published_url`
- readiness check: `doctor/capabilities` JSON

Recovery fields always expected on failure:
- `error`
- `next_action`
- `setup_command`
- `login_command`
- `hint`
- `estimated_minutes`

## Runtime Config

- `OPENCLAW_OFFERING_ID` default `naver-blog-writer`
- `SETUP_URL` or `PROOF_TOKEN + SETUP_ISSUE_URL`
- `OPENCLAW_OFFERING_EXECUTE_URL` preferred
- fallback: `CONTROL_PLANE_URL + ACP_ADMIN_API_KEY`
- `X_LOCAL_TOKEN` optional and auto-loaded from `~/.config/naver-thin-runner/config.json`
- `LOCAL_DAEMON_PORT` default `19090`

## Flow

1. `doctor/capabilities`
2. if `RUNNER_NOT_READY`, run setup
3. run `publish_dry_run`
4. if `login_required=true`, run one-time login before `publish_live`
5. `publish_live`

## Commands

If the tool files are available, use them directly:

```bash
openclaw/skill-pack/naver-blog-writer/tools/doctor_capabilities
openclaw/skill-pack/naver-blog-writer/tools/publish_dry_run --title "Title" --body "Body" --tags "tag1,tag2"
openclaw/skill-pack/naver-blog-writer/tools/publish_live --title "Title" --body "Body" --tags "tag1,tag2"
```

One-time setup:

```bash
npx @y80163442/naver-thin-runner setup --setup-url "<SETUP_URL>" --auto-service both
```

Or proof-first:

```bash
npx @y80163442/naver-thin-runner setup \
  --proof-token "<PROOF_TOKEN>" \
  --setup-issue-url "<SETUP_ISSUE_URL>" \
  --auto-service both
```

One-time login:

```bash
npx @y80163442/naver-thin-runner login
```

Start local daemon if needed:

```bash
npx @y80163442/naver-thin-runner daemon start --port 19090
```

## Common Failures

`RUNNER_NOT_READY`
- setup has not been completed on this Mac yet

`AUTH_EXPIRED`
- complete one-time Naver login again before the next live publish

`LOCAL_DAEMON_DOWN`
- start the local daemon and retry

`UNSUPPORTED_PLATFORM`
- production support is currently macOS

## Billing

- `publish_live` is the paid path
- `publish_dry_run` is a preview path and should not create a billable live publish

## Notes

- This product is a publisher, not a writer
- keep `offering_id=naver-blog-writer` for compatibility
- buyer credentials and session stay on the local runner machine
- advanced contract and schema docs live in `docs/ACP_CONTRACT.md` and `docs/OFFERING_SCHEMA.md`
