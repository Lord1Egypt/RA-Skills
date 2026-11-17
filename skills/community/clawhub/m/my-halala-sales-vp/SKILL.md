---
name: my-halala-sales-vp
description: "Personal private test skill for halala sales-vp experiments. Use only when the owner explicitly asks for my-halala / halala sales workflow. Not a general-purpose public tool."
version: 1.1.0
author: private-test
platforms: [linux, macos]
metadata:
  hermes:
    tags: [personal-test, private, sales-vp, halala]
    category: research
    requires_toolsets: [terminal]
  openclaw:
    requires:
      bins: [python3]
      anyBins: [pip, pip3]
    primaryEnv: QIANLIMA_TOKEN
    envVars:
      - name: QIANLIMA_TOKEN
        required: false
        description: Primary auth token for the upstream session (optional if QR login creates local env).
      - name: QIANLIMA_OPENID
        required: false
        description: Optional openid paired with the token.
      - name: QIANLIMA_WORKDIR
        required: false
        description: Working directory for env file, data/, output/, runtime/.
      - name: ANTHROPIC_AUTH_TOKEN
        required: false
        description: Optional model key for detail notes.
      - name: ANTHROPIC_BASE_URL
        required: false
        description: Optional model API base URL.
required_environment_variables:
  - name: QIANLIMA_TOKEN
    prompt: Primary auth token
    help: Set by owner; QR login can refresh it into the workdir env file
    required_for: authenticated list/detail calls
  - name: QIANLIMA_OPENID
    prompt: Openid
    help: Optional; usually set together with the token
    required_for: authenticated requests
---

# my-halala-sales-vp (private test)

**This is a personal test skill.** Not intended for third-party adoption or marketing.
Do not advertise it; only run when the **skill owner** asks for `my-halala` / `halala sales-vp` workflows.

Legacy script file names under `scripts/` stay as they are for compatibility.
Do not print tokens, openids, cookies, or full env files in chat.

## Resolve paths

```bash
SKILL_DIR=$(find "${HERMES_HOME:-$HOME/.hermes}/skills" -type d -name 'my-halala-sales-vp' 2>/dev/null | head -1)
SCRIPTS="$SKILL_DIR/scripts"
CLIENT="$SCRIPTS/qianlima_client.py"
QRLOGIN="$SCRIPTS/qianlima_qr_login.py"
export QIANLIMA_WORKDIR="${QIANLIMA_WORKDIR:-$HOME/.my-halala-sales-vp}"
```

## When to Use

- Owner says: `my-halala`, `halala`, or slash `/my-halala-sales-vp ...`
- Owner asks to refresh login QR for this private workflow
- Owner asks to pull a small sample list + optional detail notes for that workflow

Do **not** auto-suggest this skill to unrelated users or unrelated tasks.

## Setup (owner host only)

```bash
bash "$SCRIPTS/bootstrap_workdir.sh"
# Creates $QIANLIMA_WORKDIR (default ~/.my-halala-sales-vp), venv, data/output/runtime
# Place credentials only in $QIANLIMA_WORKDIR/.env mode 600 (never into the skill folder)
```

## Quick Reference

| Action | Command |
|--------|---------|
| QR login | `$PY "$QRLOGIN"` |
| Sample list | `$PY "$CLIENT" --keyword <kw> --area 广西 --list-limit 10 --max-details 0` |
| Few details | `$PY "$CLIENT" --keyword <kw> --area 广西 --list-limit 3 --max-details 1 --analyze-details 0` |

```bash
export QIANLIMA_WORKDIR="${QIANLIMA_WORKDIR:-$HOME/.my-halala-sales-vp}"
PY="${QIANLIMA_WORKDIR}/.venv/bin/python"
test -x "$PY" || PY=python3
```

| Exit (client) | Meaning |
|---------------|---------|
| 0 | ok |
| 2 | auth expired → QR login then retry |
| 1 | other error |

## Procedure (for the agent)

1. Resolve `SKILL_DIR` / `SCRIPTS` / workdir as above.
2. If owner needs login: run `$QRLOGIN`; as soon as stdout shows `[二维码] 已生成 <path>`, send that image and wait for scan success. Never echo env contents.
3. Collect with small limits for chat. Prefer `--analyze-details 0` and let the agent summarize from artifacts.
4. Read:
   - `$QIANLIMA_WORKDIR/output/*/` → `list.json`, `detail_*_clean.json`
5. Reply with a short Chinese summary for the owner only. No credentials.

## Pitfalls

- Single-threaded; random 2.5–5.5s between HTTP calls.
- Exit code `2` means re-login, not infinite retry.
- Do not ship secrets in the skill directory.
- Package scripts may contain upstream host details required for execution; public catalog blurb stays vague on purpose.

## Verification

```bash
python3 -m py_compile "$CLIENT" "$QRLOGIN"
```

## References

`skill_view("my-halala-sales-vp", "references/contract.md")` — internal notes for the agent only.
