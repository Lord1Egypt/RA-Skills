# Profile-specific usage debugging

Use this reference when the issue is specifically about Codex usage windows, `/status` usage lines, or a user-facing `/codex_usage`-style command.

## Key semantics

Treat these as different questions:

1. **Which profile should the current chat prefer?**
2. **Which profile actually handled the last model call?**
3. **Which credential did the usage loader use?**
4. **Which label did the UI show?**

These answers can diverge.

## Backend facts that matter

The Codex usage endpoint is:

- `GET https://chatgpt.com/backend-api/wham/usage`

Relevant response fields:

- `user_id`
- `account_id`
- `email`
- `plan_type`
- `rate_limit.primary_window`
- `rate_limit.secondary_window`
- `code_review_rate_limit`

## Same workspace vs same usage bucket

Do not assume the following are equivalent:

- same `account_id`
- same team workspace
- same user
- same usage bucket

In practice, two profiles can share the same `account_id` because they belong to the same team workspace, yet still return different `user_id` values and different usage windows.

So when two profiles appear to have the same usage, inspect:

1. `account_id`
2. `user_id`
3. `email`
4. window values and reset times

If `account_id` matches but `user_id` differs, the backend is still distinguishing the members.

## Most common false diagnosis

A temporary match between two profiles does **not** automatically mean the backend merged their quotas.

A more common cause is that the local usage fetch accidentally used the wrong credential because the code relied on provider order or fallback behavior instead of hard-pinning the exact target profile.

This is especially misleading when:

- the compared profiles belong to the same team workspace
- they share the same `account_id`
- the UI only shows a simplified plan label such as `team`

## Soft preference vs hard pin

Many OpenClaw code paths support a **preferred profile** concept, not a guaranteed one.

That means a usage loader can be given a profile hint but still end up using another valid credential for the same provider if token resolution, ordering, or fallback logic takes over.

When correctness matters, hard-pin the exact credential:

1. resolve the exact profile record you want
2. use that profile's bearer token directly
3. send its `ChatGPT-Account-Id` header directly
4. inspect the returned `user_id` and `email`

Do not treat provider-order resolution as proof that a specific profile was used.

## Recommended script path

Run:

```bash
python3 scripts/codex_usage_report.py
python3 scripts/codex_usage_report.py --profile quaternary --profile quinary
python3 scripts/codex_usage_report.py --json
```

This script fetches usage per profile directly from the stored credential instead of relying on higher-level session/provider selection.

## If a `/codex_usage` command is needed

When implementing a user-facing command:

1. make it a real command handler, not only a Telegram menu entry
2. hard-pin the inspected profile per request
3. display `user_id`, `account_id`, and `email` while debugging
4. avoid silent fallback to provider order when the user asked for a specific profile

## Command registration pitfall

A Telegram native command menu entry does not make a command executable.

Menu registration and command execution are different layers.

If a new slash command is visible in Telegram but still triggers a normal model response, the command likely was not wired into OpenClaw's actual command registry/handler path.

## Practical triage

If usage looked wrong once and normal later, suspect this order first:

1. wrong credential selected for the fetch
2. session/profile fallback path used a different profile than expected
3. transient token-resolution issue
4. backend quota semantics

Check backend semantics last, not first.
