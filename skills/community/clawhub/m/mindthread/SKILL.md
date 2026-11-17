---
name: mindthread
description: Schedule, publish and manage Threads (threads.net) posts through MindThread. Draft posts in the account's voice, publish now or at a set time, queue posts, review cloud-patrol reply drafts, and read views and engagement. Use when the user asks to post, schedule, queue or analyze Threads content, or to review replies waiting for approval.
version: 0.3.0
metadata:
  openclaw:
    requires:
      env:
        - MINDTHREAD_API_KEY
      bins:
        - mindthread
    primaryEnv: MINDTHREAD_API_KEY
    envVars:
      - name: MINDTHREAD_API_KEY
        required: true
        description: MindThread API key from https://mindthread.tw/settings (Settings → API keys). mt_test_ keys are a free sandbox where writes are simulated.
      - name: MINDTHREAD_ACCOUNT
        required: false
        description: Default Threads account as @handle or account id, used when -a is omitted.
    install:
      - kind: node
        package: mindthread-cli
        bins: [mindthread]
    emoji: "🧵"
    homepage: https://github.com/ppcvote/mindthread-cli
---

# MindThread: Threads scheduling for agents

MindThread publishes to Threads through Meta's official API. The `mindthread` CLI wraps its REST API. Always add `--json` when you need to read a result; human output is for showing the user.

## Setup check

```bash
mindthread whoami --json      # plan, key permissions, calls left today, connected accounts
mindthread accounts --json    # pick the account: use threads_username (@handle) or id with -a
```

If the command exits with code 4, the key is missing or rejected: ask the user to create one at https://mindthread.tw/settings (Settings → API keys) and set `MINDTHREAD_API_KEY`. Do not try other keys.

## Core workflow

1. **Draft** (publishes nothing): `mindthread generate "<topic>" -a @handle -n 3 --json`
2. **Show the drafts to the user** and get approval for the exact text before posting, unless the user told you to post without review.
3. **Publish or schedule** exactly one of:
   - now: `mindthread post "<text>" -a @handle --now --json`
   - at a time: `mindthread post "<text>" -a @handle --at 2026-11-01T09:00:00+08:00 --json` (always include the UTC offset; relative `+2h` also works)
   - best slot: `mindthread post "<text>" -a @handle --best-time --json` (text only, 500 chars max)
   - images: add `--media <https url>` (repeat for a carousel of 2-10); video: `--video <https url>`. URLs must be public https.
   - long text: put it in a file and use `--file post.txt`; over 500 chars becomes a thread automatically.
4. **Or queue it** to publish at the account's own time slots: `mindthread queue add "<text>" -a @handle --json` (`--draft` keeps it for approval).
5. **Verify**: `mindthread schedules -a @handle --json` or `mindthread queue list -a @handle --json`.

Pass `--idempotency-key <unique-id>` on post and queue commands when you might retry, so a retry never posts twice.

## Exit codes and what to do

| Code | Meaning | Do this |
|------|---------|---------|
| 0 | ok | read the JSON |
| 2 | usage error | fix the command; nothing was sent |
| 3 | waiting for the owner (`approval_required`) | give the user the `human_url` from the error, **do not resend**; check later with `mindthread approval <id> --json` |
| 4 | missing or rejected key | ask the user for a valid key |
| 5 | rate limited | wait `retry_after_seconds`; do not loop |
| 1 | other error | read `error.code` and `error.message`; for `insufficient_scope` tell the user the `fix` text; for `content_rules_violated` rewrite the text to satisfy the listed rules |

## Replies (cloud patrol)

```bash
mindthread patrol pending -a @handle --json          # drafted replies waiting for review
mindthread patrol approve <id> --json                # send as drafted
mindthread patrol approve <id> --reply "<edited>"    # send an edited reply
mindthread patrol reject <id> --json                 # never send
mindthread patrol keywords -a @handle --json         # AI keyword suggestions (one AI call; once per 24 h)
```

Show each draft to the user before approving unless they delegated the decision. Turning patrol on can require the owner's confirmation; that is expected.

## Results

```bash
mindthread insights -a @handle -p 7d --json   # posts in the period; total_views is lifetime, not per period
mindthread patrol stats -a @handle --json     # views and likes earned by patrol replies
mindthread events --since <iso> --json        # post.published, post.failed, reply.sent, approval.decided …
```

## Rules

- Never publish with `--now` or approve a reply the user has not seen, unless the user explicitly asked you to act without review.
- Never invent numbers or claims in posts; if the account has content rules with `facts`, only those numbers are allowed.
- Do not retry a request that returned `approval_required`; the server runs it once the owner confirms.
- Read `warnings[]` in every response (they never block). `off_hours` and `stale_time_reference` question the time or a word like "yesterday"; `changed_since_last_viewed` means the text, media or time changed since the user last looked at it (or since you last read it): show the user the removed and added sentences before releasing it. Editing a draft is not the user seeing it.
- Anything not covered here: `mindthread api GET /openapi.json` lists every endpoint; call one with `mindthread api <METHOD> <path> -d '<json>'`.
