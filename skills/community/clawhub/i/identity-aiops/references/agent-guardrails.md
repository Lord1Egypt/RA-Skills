# Agent guardrails — running identity-aiops with a smaller / local model

If you drive these tools with a local model (Llama, Qwen, Mistral … via Goose,
Ollama, LM Studio, or any OpenAI-compatible runtime), you will get noticeably
better results with a short system prompt. This page gives you one, and — more
importantly — tells you which guardrails you **no longer need to write**, because
the tool now enforces them itself.

The distinction matters. A guardrail in a prompt is a request. A guardrail in the
harness is a guarantee. Anything below that we could move into the harness, we did.

## Authorization is not this tool's job — decide it where it belongs

Whether a write should happen is your decision, or the account's. The tool does
not gate it — there is no read-only switch and no approval prompt to configure.
The two right places to control read vs write:

- **The account you connect with.** Give the Keycloak service account (or the
  authentik token) only the roles you want the agent to have — `view-users` /
  `view-events` / `view-clients` and no `manage-*`. A write then fails at the
  server, which is the only place the permission actually lives — no skill-side
  flag can be argued around by a model, but a revoked permission cannot be.
- **Your agent's system prompt.** If you want an observe-only session, tell the
  model not to call the write tools (they are clearly tagged `[WRITE]`).

What the tool *does* guarantee is that you can always see what happened:

## What the tool enforces — do not waste prompt budget on these

| You might be tempted to prompt | Why you don't need to |
|---|---|
| "Don't invent a value when a field is missing" | A field the IdP did not return comes back as `null`, never as `""`. Absent and empty are distinguishable in the payload — a `lastLogin` of `null` means "no sign-in on record", not "signed in at an empty time". |
| "Tell me if the output was cut off" | Every listing returns `{"users": [...], "returned": N, "limit": L, "truncated": true/false}` (same shape for `events`, `groups`, `members`, `clients`, `sessions`, `identityProviders`). Truncation is measured — one extra row is fetched — not guessed from a length coincidence. |
| "Tell me if the analysis only saw part of the data" | The four analyses echo `inputsTruncated` / `feedTruncated`, and `truncated` + `maxRows` when a finding list was capped. The `*Count` fields are always the full totals. |
| "Make it show the number it judged on" | `client_misconfig_audit` ranks clients by `riskScore` — the summed severity weights, echoed as `severityWeights` so the score is recomputable — and every finding carries its own `severity`. `login_failure_rca` findings each carry the counts that tripped them (`failures`, `distinctUsers`, `distinctIps`); the thresholds they were compared against are reported separately under `thresholds`, not on the finding. |
| "Confirm before anything destructive" | Write CLI commands have `--dry-run` plus double confirmation. |
| "Log what you did" | Every call is audited to `~/.identity-aiops/audit.db` regardless of what the model says it did. |

## Platform asymmetry — a teaching error is an answer, not a failure

identity-aiops speaks to **two** identity providers through one tool set, and
they do not have the same APIs. Some tools exist only on one platform. When you
call one against the other platform, it returns a **teaching error** that names
the gap and points at the alternative.

**That error is a definitive answer about the platform, not a broken tool.**
Do not retry it, do not try a different argument, and do not report the tool as
failing. Switch approach, or tell the user the platform does not support it.
This is the single most common way a smaller model wastes a turn here.

### Keycloak-only tools

On an **authentik** target these return `{"error": ...}`:

| Tool | Why | What to do instead |
|---|---|---|
| `user_lockout_status` | authentik keeps no per-user brute-force lockout register | Use `login_failure_rca` over the failed-auth feed |
| `client_sessions` | authentik has no per-provider session listing | Use `user_sessions` per user |
| `client_session_stats` | authentik has no per-client session rollup | Use `user_sessions` per user, or `stale_access_audit` |
| `require_password_reset` | authentik has no required-actions concept | Issue a recovery link from the authentik admin UI |
| `rotate_client_secret` | authentik has no secret-rotation endpoint | Set a new client secret on the OAuth2 provider |

The two reads fail with `Resource '<name>' is not mapped for platform
'authentik'. Mapped resources: ...`; the two writes fail with `<tool> is a
Keycloak-only operation — authentik API v3 has no equivalent API. <hint>`.

### authentik-only data

`stale_access_audit` includes an `orphanedSessions` check that needs a
**global** session list. Only authentik exposes one. On a **Keycloak** target
that check silently contributes nothing — `orphanedSessions` is always `[]` and
`orphanedSessionCount` is always `0`. Do **not** report that as "no orphaned
sessions found" on Keycloak; the check did not run. The other three findings in
that audit are unaffected.

### Everything else works on both

`identity_overview`, `realm_info`, `list_identity_providers`, `list_users`,
`user_detail`, `user_count`, `user_sessions`, `user_credentials`, `list_groups`,
`group_members`, `login_events`, `admin_events`, `list_clients`,
`client_detail`, all four analyses, `disable_user`, `enable_user`,
`revoke_user_sessions`, `update_client_redirect_uris`, `undo_list`,
`undo_apply` — the normalized rows use the same field names on both platforms.

## What still needs a prompt

These are model-behaviour problems the harness cannot fix from the outside.

⚠️ **`login_failure_rca`'s order is not on one comparable quantity.** It does sort its findings
worst-first, but the sort key falls back from `failures` to `distinctUsers`, so the two storm findings
(`lockout-storm` and `expired-credential-storm`, neither of which has a `failures` key) are
ranked by a user count against another finding's failure count. Its findings carry neither a `rank` nor a `severity`. Weigh each
finding's own counts rather than its position. `client_misconfig_audit` is different: its
`riskScore` ordering is stated in the payload and can be rechecked.

Recommended setup for a local model (adapt it to your agent client):

```text
You operate a Keycloak or authentik identity provider through the
identity-aiops MCP tools.

TOOL USE
- Before answering any question about the current identity environment, you
  MUST call a tool. Never answer from memory or assumption.
- Actually invoke the tool. Do not describe the call you would make, and do not
  emit an example JSON response in place of calling it.
- If a tool call fails, report the real error verbatim. Never fill the gap with
  a plausible-sounding answer.
- Some tools are Keycloak-only and return an error explaining that on
  authentik. That is a correct answer about the platform, not a tool failure:
  do not retry it, and follow the alternative the error names.

READING RESULTS
- Read the whole result before concluding. Listings return "returned", "limit",
  and "truncated". If "truncated" is true, say so and re-run with a higher
  limit instead of treating the partial result as complete.
- `login_failure_rca` findings are not ranked on one comparable quantity and carry no rank.
  Weigh each finding's own counts and say which one you acted on; never treat the first as
  the headline.
- The analyses return "inputsTruncated" / "feedTruncated". When either is true,
  every count is a lower bound — a threshold may have gone unreached only
  because the events that would have reached it were never fetched. Never
  report a clipped analysis as an all-clear.
- A null field means the IdP did not return that value. Report it as "not
  available" — never infer it. A null lastLogin is "no sign-in on record"; a
  null passwordPolicy is "the realm did not report one", not "no policy".
- Report values exactly as returned. Do not normalise, translate, or prettify
  usernames, event types, error codes, or ids.

IDENTIFIERS — do not confuse these
- A user id (Keycloak UUID, authentik integer pk) is not a username. Tools take
  the id; get it from list_users.
- A client's internal id (what client_detail and the client writes take) is not
  its clientId (the public OAuth identifier shown to end users). list_clients
  returns both.
- A group id is not a group name or path.
- A realm is a Keycloak concept. authentik has no realms; its target's realm
  field is a label only.

SCOPE
- Separate observation from interpretation. State what the tools returned, then
  any interpretation, clearly marked as such.
- Do not assert that an account is compromised, dormant, or misconfigured
  unless a tool result supports it. These conclusions get people locked out.
- Do not add generic identity-security advice that does not follow from the
  tool output.
```

## Recommended setup for a local model

Start with a connection that *cannot* write, verify, and widen the account's
permission only when you trust the setup. Identity writes are unusually
consequential — `disable_user` and `revoke_user_sessions` lock a person out of
everything behind the IdP.

```bash
# Give the Keycloak service account only view-* roles (or an authentik token
# without manage scope). A write then fails at the server, not on a flag a
# model can argue around. Then:
identity-aiops doctor
```

Optionally annotate the audit trail with who is operating and why — recorded on
every row, never required:

```bash
export IDENTITY_AUDIT_APPROVED_BY="your.name@example.com"
export IDENTITY_AUDIT_RATIONALE="access review 2026-07-20"
```

## If your model still struggles

Some behaviours are model-capacity limits rather than prompt problems:

- **Multi-tool workflows time out or drift.** Prefer the four analysis tools —
  `login_failure_rca`, `stale_access_audit`, `client_misconfig_audit`,
  `mfa_coverage_analysis` do the multi-step correlation inside one call, so the
  model does not have to chain reads and keep user ids straight.
- **The model ignores later tool results in a long context.** Event feeds are
  the worst offender: `login_events` with the default `max_results=200` is a
  lot of rows. Filter with `event_type` and `user`, and lower `max_results` —
  the `truncated` flag will tell you when you cut too deep.
- **The model reports "no data" from a long feed.** Check `returned` in the
  reply it received; if it is non-zero, the model dropped the payload rather
  than the tool returning nothing. Ask a narrower question.
- **The model retries a Keycloak-only tool on authentik.** Put the
  platform-asymmetry paragraph from the system prompt above near the *top* of
  your prompt, not the bottom.
- **The model describes calls instead of making them.** This is usually a
  runtime/tool-calling-format mismatch, not a prompt problem — check that your
  client advertises the tools in the format your model was trained on.

Feedback on running this with a specific local model is genuinely useful —
open an issue at
[github.com/AIops-tools/Identity-AIops](https://github.com/AIops-tools/Identity-AIops/issues)
with the model, runtime, and what went wrong.
