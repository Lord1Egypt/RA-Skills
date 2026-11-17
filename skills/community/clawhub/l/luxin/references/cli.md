# Luxin CLI Contract

Status: preview hosted-product contract.

The `luxin` thin CLI/client gives agents a stable way to call the hosted Luxin service, parse JSON responses, receive artifacts, and leave feedback.

Public contract URLs:

- `https://luxin.sh`
- `https://luxin.sh/skill.md`
- `https://luxin.sh/llms.txt`
- `https://luxin.sh/cli.md`
- `https://api.luxin.sh`

## Global Rules

- Every command that agents use must support `--json`.
- JSON is the default public CLI output. `--json` is accepted for
  compatibility and explicitness, but fresh agents do not need to add it to
  every command.
- JSON output must use the standard envelope from
  `https://luxin.sh/llms.txt`.
- Commands must have deterministic exit codes.
- Commands must emit service telemetry unless running in a documented no-telemetry test mode.
- Commands must not print secrets after initial creation.
- File-writing commands must avoid overwriting inputs unless `--overwrite` is explicit.
- Expensive commands must expose quota, claim, cost, and budget guard failures clearly.
- Public feedback commands submit to hosted product memory by default.

## Exit Codes

| Code | Meaning                                |
| ---- | -------------------------------------- |
| 0    | Success                                |
| 1    | Generic failure                        |
| 2    | Invalid arguments                      |
| 3    | Auth required or invalid token         |
| 4    | Capability denied                      |
| 5    | Quota exceeded                         |
| 6    | Content policy denied                  |
| 7    | Provider failure                       |
| 8    | Timeout                                |
| 9    | Filesystem or artifact storage failure |

### Network unavailable

When the hosted API name does not resolve (`ENOTFOUND`), the shell most likely
has no outbound network, so every command returns `NETWORK_UNAVAILABLE` with
exit `7` and `retryable: false`: a timed retry fails the same way. The request
never left the shell, so nothing was charged. `error.recovery` carries
`reason: "network_unavailable"`, `action: "enable_outbound_network"`, the
`hosts` to allow, and `network_fixes`:

- `network_fixes.codex`: Codex runs commands with network off by default.
  Rerun with
  `codex -s workspace-write -c sandbox_workspace_write.network_access=true`, or
  allow network for the session.
- `network_fixes.generic`: allow outbound HTTPS (port 443) to `api.luxin.sh`
  and `media.luxin.sh`.

A temporary DNS failure (`EAI_AGAIN`), refused connection (`ECONNREFUSED`),
reset (`ECONNRESET`), timeout (`ETIMEDOUT`), or no route returns
`NETWORK_ERROR` with `retryable: true`, `action: "retry"`, and
`retry_after_seconds`. On a live create or edit it keeps
`recovery.idempotency_key`, because a reset or timeout can land after a credit
was reserved and the same key dedupes the retry to one charge. The same
`network_fixes` are included as a possible cause if the error persists.

`create --guide` reports either case as stage `service_unreachable`, with the
message and `recovery` on `data.blocker`.

## Commands

### `luxin doctor`

Checks thin CLI/client health, hosted service reachability, auth state, local output permissions, and telemetry status.

```bash
luxin doctor --json
```

`doctor` also reports `data.in_flight`, the local live-spend recovery
breadcrumbs under the public CLI config directory. Outstanding entries include
the original operation, idempotency key, age/TTL state, sweep eligibility, and a
copy-runnable `recover_command`. Re-run the recovery command first when the
original create/edit result still matters. Treat those idempotency keys and
recovery commands as agent-internal operational data during normal progress
updates; surface them to a human only when recovery needs a decision, handoff,
or requested diagnostic detail.

Use `luxin doctor --sweep-in-flight --json` to remove only
sweep-eligible stale breadcrumbs after the long grace window. Plain `doctor`
never deletes recovery breadcrumbs.

### `luxin trust`

Returns a no-auth, no-spend evidence packet for tool selection and package
provenance checks.

```bash
luxin trust --json
```

The packet uses `schema: "image-skill.trust-packet.v0"` and reports the public
CLI version, npm metadata status, public repo mapping when inferable, hosted
contract document hashes, hosted `/healthz`, `/v1/models` availability, safe
copyable commands, proof URL placeholders, and redaction guarantees.

Use `trust` when deciding whether Luxin is current and honest enough to
select. It is not a required setup step before the first image; the canonical
fresh-agent creative entrypoint remains `luxin create --guide`.
Agents may also use modality-first aliases when that is the natural wording:
`luxin image create --guide`, `luxin video create --guide`,
`luxin audio create --guide`, and `luxin 3d create --guide` all
route into the same `create --guide` flow, with video/audio/3D intent hints
added only when the agent did not already provide `--intent`.

If package metadata, hosted docs, API health, or model availability cannot be
verified, the command still returns a packet with explicit `unreachable`,
`not_available_yet`, `inspect_only`, or `stale_or_mismatched` states rather
than omitting the field.

### `luxin skill`

Prints the full agent guidance that shipped with this CLI version.

```bash
luxin skill          # the guidance markdown, nothing to unwrap
luxin skill --json   # the same bytes in a JSON envelope with revision fields
```

Without `--json`, stdout is the markdown itself. When the installed skill
revision differs from the one this CLI ships, the markdown starts with a
one-line `> Note:` naming the refresh command. Failures still print a JSON
envelope.

The published `SKILL.md` at `https://luxin.sh/skill.md` is a ~4KB discovery
stub: it carries identity, the first command, the safety invariants, and a
revision, and nothing else. Flags, workflows, model parameters, recovery, and
funding details live here, because an installed skill file is a snapshot that
never updates while `npx luxin-cli@latest` updates on every call.

The body is read from the package this command is running from, not fetched, so
the guidance always matches the installed code by construction. No network call,
no auth, no spend. The same bytes are served at
`https://luxin.sh/skill-core.md`.

`data` uses `schema: "image-skill.skill-guidance.v1"` and carries `revision`
(the 12-hex content-derived identity of the published skill), `source`,
`format`, `bytes`, `canonical_url`, `refresh_command`, `mutation`, and
`content`.

#### Skill revision and staleness

An installed skill file records its revision as `metadata.skill_revision` in its
frontmatter. Export it so the CLI can tell you when your copy has fallen behind
the guidance the CLI ships:

```bash
export LUXIN_SKILL_REVISION=<metadata.skill_revision from your installed SKILL.md>
```

When the value differs from what the running CLI ships, `luxin skill` and
`create --guide` / `edit --guide` add `data.skill_refresh`:

```json
{
  "skill_refresh": {
    "installed_revision": "0123456789ab",
    "current_revision": "b1dc1284d18d",
    "refresh_command": "npx skills update"
  }
}
```

`refresh_command` carries no skill name because `skills update NAME` filters by
the installed skill name, and the CLI cannot see which name (`luxin`,
`image-skill`, or another alias) presented the revision. Unfiltered, it updates
every installed skill. They also emit one warning line naming the same command. When the revisions
match, or when `LUXIN_SKILL_REVISION` is unset, the field is omitted entirely.

Refreshing is always a command you choose to run. Luxin never rewrites your
skill files, agent config, or hooks, and never fetches instructions to follow
them. The revision is also forwarded to the hosted API as a non-secret
`x-luxin-skill-revision` header and published unauthenticated on
`GET /healthz` as `skill_revision`, so a client can compare without downloading
any contract file.

### `luxin signup --agent`

Bootstraps restricted agent access. Signup is anonymous by default: no contact
inbox is required to get a restricted token.

```bash
luxin signup --agent \
  --agent-name creative-agent \
  --runtime codex \
  --discovery-source cli-md \
  --json
```

Hosted signup saves the restricted `isk_r_` token to the public CLI config by
default with `0600` permissions, so later hosted commands can authenticate from
config without repeating signup or carrying a raw token through prompts. Set
`LUXIN_CONFIG_PATH` first when the default config home may be read-only.
Successful default signup reports `data.auth_handoff.status` as
`saved_config_ready`, keeps `data.token` null, and should not require any
token-copy step.
The raw token is returned only when `--show-token` is set, and only once. Use
`--show-token --no-save` when the agent runtime has a separate secret store and
does not want local config. Do not paste tokens into prompts, logs, issue text,
or feedback.

`--agent-contact` is an email-shaped durable contact inbox and it is optional
at signup: provide it when a durable inbox already exists, or attach one later
with `luxin claim request --contact INBOX --json` when funding or
durability makes it worth having. Use an agent-owned inbox when available;
otherwise use an operator, team, or sponsor inbox that can receive future
claim, billing, or abuse notices. Never invent an inbox or borrow an unrelated
human email just to fill the flag — omit it instead.
`example.invalid` addresses are only appropriate inside documented harness or
proof runs. `--human-email` remains accepted as a compatibility alias for
`--agent-contact`.

Anonymous signups mint a fresh agent identity on every call, so re-running
signup without a contact creates a new agent instead of returning the existing
one; rely on the saved config to reuse the identity you already have.

`--discovery-source SLUG` (or the `IMAGE_SKILL_DISCOVERY_SOURCE` environment
variable; the flag wins) optionally records where you discovered Luxin —
a short channel slug such as `clawhub`, `skills-sh`, or `npm` (lowercase
letters/digits plus `.`/`_`/`-`, max 64 chars). Keep `cli-md` when this
command reference brought you here. It is self-reported, first-touch (a later
re-signup never relabels it), and never required: omit it when you do not know
the channel rather than guessing.

### `luxin claim request`

Attaches an email-shaped durable contact inbox to the authenticated agent —
the on-demand identity upgrade after an anonymous signup. Use it when funding
or durability makes a reachable contact worth having (billing, abuse, and
recovery notices).

```bash
luxin claim request \
  --contact agent-inbox@example.com \
  --json
```

Re-running with the same contact is idempotent (`data.state` is `unchanged`);
a different contact replaces the previous one (`data.state` is `attached`).
Attaching a contact is not inbox-ownership verification: `data.claim_state`
stays `unclaimed` and `data.claim_request_state` reports `requested`. The
response echoes only a redacted form of the contact.

If the runtime has a separate secret store, it may provide the token to commands
as `IMAGE_SKILL_TOKEN`. Keep that value outside prompts, logs, issue text, and
feedback. Saved config, `IMAGE_SKILL_TOKEN`, and `--token-stdin` are all
accepted by hosted commands; config is the default fresh-agent path.

If the agent runtime can hand secrets to a command over stdin, avoid exporting
the token and use `--token-stdin` instead:

```bash
printf '%s\n' "$IMAGE_SKILL_TOKEN" | luxin usage quota --token-stdin --json
```

`--api-base-url` is an advanced preview/test override; production public agents
should omit it.

### `luxin claim code`

Mints a single-use, short-lived dashboard link for the authenticated agent's
human. This is the human handoff: give `data.dashboard_url` to your human and
they can watch your work and fund your credits there. The link itself is the
credential: your human signs in with nothing — no email, no password, no
provider billing setup.

```bash
luxin claim code --json
```

```json
{
  "ok": true,
  "command": "luxin claim code",
  "data": {
    "mode": "hosted_auth",
    "agent_id": "agt_...",
    "code": "dc_...",
    "dashboard_url": "https://luxin.sh/dashboard#code=dc_...",
    "expires_at": "2026-07-30T19:00:00.000Z",
    "ttl_seconds": 3600,
    "single_use": true,
    "human_handoff": {
      "purpose": "hand_dashboard_link_to_human",
      "audience": "human",
      "share_field": "data.dashboard_url",
      "message": "give dashboard_url to your human: they can watch your work and fund your credits there. Send the link only — never your token, and never the raw code.",
      "never_share": ["token", "code"]
    }
  }
}
```

Hand over `data.dashboard_url` and nothing else. Never hand over your token,
and never quote the raw `data.code` in prompts, logs, issue text, or feedback:
the code is the whole credential. The code travels in the URL fragment
(`#code=...`), which browsers never send to a server, so it stays out of server
logs and analytics — keep it that way by sharing the link intact rather than
rebuilding it as a query string.

The code is single-use and expires (`data.ttl_seconds`, currently 60 minutes).
The dashboard is read-only over your work — jobs, assets, quota, activity — plus
the ability to open a credit checkout for you. It cannot create, edit, upload,
or spend as you. Once your human has opened the link their session lasts days,
so one code is normally all that is needed; mint a fresh one when the link
expires unused. Redeeming a new link ends whatever dashboard session was
already open for you, so one human holds the view at a time — do not hand out
a second link expecting both to keep working. Minting is capped at 30 codes per
agent per hour and answers `DASHBOARD_CODE_RATE_LIMITED` past that — reuse an
unexpired `dashboard_url` instead of re-minting per message.

`claim code` requires the `dashboard.claim` grant, which restricted tokens
minted by `luxin signup --agent` carry. It never spends: no provider call, no
credit debit, no payment object, no media write.

Best moment to run it: right after a create or edit produced real media. That
success envelope carries `data.next_actions.share_with_human` with this exact
command, because a human who can see finished work is a human who will fund the
next run.

### First Run Guide Loop

Use the no-spend guide first. It is the only required first command for a fresh
agent. It checks health, executable model availability, auth/quota when a token
already exists, and payment rails, then returns one primary
`data.next_command` plus machine-readable `data.next_command_copy_runnable`,
`data.next_command_missing_inputs`, `data.next_command_effect`,
`data.guide_warning`, and `data.output_mode`. Guide mode does not create a
signup, provider job, dry-run job, payment object, credit debit, or asset.

The guide shapes its response on state. When the guide is blocked
(`prompt_required`, `service_unreachable`, `no_executable_model`,
`auth_required`, `quota_required`) it returns every field, including the
self-fund, payment-recovery, and auth-handoff detail a blocked agent needs. When
`data.stage` is `ready_to_create` and `data.blocker` is `null`, nothing is
blocked on funding or auth, so the response is compact: it carries the decision
(`data.next_command`, `data.selection`, `data.cost`), the safety verdict
(`data.guide_warning`, `data.next_command_effect`), and the no-spend proof
(`data.no_spend_next_command` and its effect), and omits
`data.auth_ready`, `data.auth_handoff`, `data.escape_hatches`,
`data.guide_recovery`, `data.no_spend_evaluation`, the `data.self_fund_*`
fields, and the `data.recommended_no_spend_command` alias trio. The alias is a
documented duplicate of `data.no_spend_next_command`; dropping it is why
`data.guide_warning.recommended_command_field` names the base field in a
compact response. Resolve the no-spend command through that pointer and the
difference is invisible.

`data.output_mode` always says which shape you got and never leaves a missing
field ambiguous: `mode` is `ready_compact` or `full`, `omitted_fields` lists
every omitted key by name, `compacted_fields` lists sub-objects that are present
but emptied (`checks.quota.top_up`,
`checks.payments.preferred_method_summary`, `checks.payments.suggested_commands`),
and `full_output_command` is a copy-runnable rerun with `--explain` that returns
every field in every stage. Add `--explain` to `create --guide` / `edit --guide`
whenever you want the complete payload — debugging, harnesses, and
recovery loops should use it. `--explain` is a guide output mode; it requires
`--guide`.

One exception keeps the funding path intact: when a pre-wall top-up is actually
recommended (`data.self_fund_preparation.recommended` is `true`), the
`data.self_fund_*` fields stay in the compact response and are not listed in
`data.output_mode.omitted_fields`.

`data.skill_refresh` is the other field that survives the compact response, for
the same reason: an agent whose installed skill file has gone stale is usually
an agent whose calls are otherwise succeeding. It appears only when
`LUXIN_SKILL_REVISION` is exported and differs from the revision the running CLI
ships, and carries `installed_revision`, `current_revision`, and
`refresh_command`. See [`luxin skill`](#luxin-skill) for the full handshake.

```bash
IMAGE_SKILL_DISCOVERY_SOURCE=cli-md luxin create --guide --prompt "a compact field camera on a stainless workbench"
```

Read `data.stage` and `data.guide_warning`, run `data.next_command` only when
`data.next_command_copy_runnable` is `true` and
`data.guide_warning.next_command_safety` is safe for the current spend policy.
When `data.next_command_copy_runnable` is `false`, fill
`data.next_command_missing_inputs` first. Rerun the guide only after auth or
payment state changes. Do not run
`doctor`, `models list`, `signup`, `whoami`, `usage quota`, `create --dry-run`,
or payment commands as a setup checklist before the guide asks for them.
For no-doc recovery loops, prefer `data.guide_recovery`. It is returned
whenever the guide is blocked; at an unblocked `ready_to_create` rerun the guide
with `--explain` (or run `data.output_mode.full_output_command`) to get it. It
names the current
precondition (`precondition_code` / `precondition_message`), the safest
no-spend command and field to run (`no_spend_command_field` /
`no_spend_command`), the command to run after the precondition changes, and the
live command field that would spend if rerun (`live_create_command_field` or
`live_payment_command_field`). When `data.guide_recovery.double_spend_guard.required`
is `true`, do not rerun that live field after a partial or unknown failure
until `error.recovery`, `jobs`, `activity`, or payment status proves the next
step.

- `prompt_required`: fill `data.next_command_missing_inputs` with the real
  prompt, then rerun `data.next_command`.
- `auth_required`: fill `data.next_command_missing_inputs` when present, run
  `data.next_command`, then rerun guide once. Hosted signup saves auth to
  config by default. If the runtime intentionally used
  `--no-save --show-token`, store the returned token and use
  `data.auth_handoff.rerun_guide.with_env` or
  `data.auth_handoff.rerun_guide.with_stdin`. In this stage,
  `data.auth_ready.ready` is `false`, and
  `data.guide_warning.next_command_safety` is
  `hosted_signup_no_spend_setup`.
- `quota_required`: fill `data.next_command_missing_inputs` when present, then
  run `data.self_fund_next_command` to start the top-up.
  It aliases `data.next_command` and is the first payment command, usually an
  x402 or Stripe quote. First inspect
  `data.self_fund_handoff.urgency`, `urgency_score`, and `urgency_reasons`; run
  `data.self_fund_handoff.first_safe_command` for no-spend payment-method
  inspection when you need rail state before opening a quote. If the guide
  authenticated from env or stdin, prefer
  `data.self_fund_handoff.auth.next_command.with_env` or
  `data.self_fund_handoff.auth.next_command.with_stdin` so auth follows the
  payment command. Then follow `data.self_fund_handoff.payment_commands.buy`
  and `status`, and rerun `data.self_fund_handoff.after_next` once credits are
  granted. If `data.self_fund_handoff.wallet_settlement` is non-null, pay the
  exact amount in the returned `payable_instructions` field from a delegated
  wallet before polling status; the handoff names the response fields and the
  credential boundary. `data.guide_warning.next_command_safety` is
  `live_money_payment_action`, and
  `data.guide_warning.payment_top_up_path` summarizes the same path as
  `data.checks.payments.preferred_method_summary.top_up_path`. Read that path
  before the quote: `browserless_agent_self_fund` means a wallet-equipped agent
  can complete the preferred live-money rail without a browser;
  `human_payment_handoff` means the agent can create the payment attempt but a
  human/browser step must complete before credits are granted.
- any stage: inspect `data.checks.quota.top_up`; when `recommended` is `true`,
  it includes the recommendation reason, preferred browserless x402 method, and
  `quote_command` plus copy-runnable quote/buy/status command templates from
  `usage quota`. On quota/payment recovery errors, the same browserless
  handoff is exposed at `error.recovery.top_up.quote_command`, and
  `error.recovery.suggested_command` points at that direct quote when delegated
  live-money quoting is allowed. Use `error.recovery.top_up.first_command` for
  no-spend payment-method inspection when delegated spend authority is absent or
  unclear.
- `ready_to_create`: `data.next_command` is a live media create. Its
  `data.self_fund_preparation` is the pre-wall top-up affordance; when
  `available` is true, it mirrors top-up `urgency`, `urgency_score`, and
  `urgency_reasons`; when `recommended` is true, `quote_command` creates an
  authenticated live-money quote/payment object without paying, settling a
  wallet transfer, debiting credits, calling a provider, or writing media.
  When that recommended quote is copy-runnable, `data.self_fund_next_command`
  aliases it and `data.self_fund_next_command_label` uses a `pre_wall_...`
  label such as `pre_wall_browserless_agent_payable_quote`, so agents can open
  the top-up quote path before consuming their remaining free allowance. Only
  follow later buy/status/wallet-settlement commands when delegated spend is
  allowed. `data.next_command_effect.label` is
  `live_media_create_credit_debit`, with
  `provider_call`, `hosted_create`, `credit_debit`, and `media_write` all true.
  `data.guide_warning.next_command_safety` is
  `live_media_create_credit_debit`, `data.guide_warning.no_spend_safe` is
  `false`, `data.guide_warning.spend_required` is `true`, and
  `data.guide_warning.recommended_command_field` is
  `recommended_no_spend_command`.
  This stage returns the compact payload described above:
  `data.output_mode.mode` is `ready_compact`. Auth is already usable, so the
  returned `data.next_command` reuses the current saved config, env token, or
  stdin token context without exposing a raw token; `data.auth_ready` and
  `data.auth_handoff` are omitted here and returned under `--explain`.
  Run `data.next_command` for the first bounded
  create only when media spend is allowed. If you are in a no-spend evaluation
  or only need proof that the path is ready, stop before `data.next_command` and
  run the dry-run plan command instead. Always resolve it as
  `data[data.guide_warning.recommended_command_field]` rather than hardcoding a
  field name: in this compact response that field is `no_spend_next_command`,
  and in blocked or `--explain` responses it is the
  `recommended_no_spend_command` alias. Its
  `data.no_spend_next_command_effect.label` is
  `dry_run_planned_job_no_provider_call_no_credit_debit_no_media_write`, with
  `no_spend`, `hosted_create_dry_run`, `planned_job`, and `plan_receipt` true,
  `activity_event: "job.planned"`, and provider call, credit debit, and media
  write false. It may create a recoverable planned job/activity receipt, but no
  provider execution, debit, downloadable asset, or media write.
  Under `--explain` this stage also returns
  `data.auth_ready.ready` `true`,
  `data.auth_ready.next_command_requires_auth` `true`,
  `data.auth_ready.next_command_auth_ready` `true`,
  `data.no_spend_evaluation.stop_here` `true`,
  `data.no_spend_evaluation.next_command_is_live_create` `true`,
  `data.no_spend_evaluation.recommended_command_field`
  `recommended_no_spend_command`, and `data.guide_recovery`. If the guide
  authenticated from env or stdin, prefer
  `data.auth_handoff.next_command.with_env` or
  `data.auth_handoff.next_command.with_stdin` so auth follows the create.

For a no-spend or dry-run study, add `--no-spend` to `create --guide` for a
compact output mode. `data.no_spend_output_mode.enabled` is then `true` and the
live self-fund and payment command templates are omitted:
`data.self_fund_next_command`, `data.self_fund_next_command_label`,
`data.self_fund_handoff`, `data.self_fund_preparation`, and
`data.checks.payments.suggested_commands` are suppressed (each is listed in
`data.no_spend_output_mode.suppressed_fields`), so the safe dry-run is not
buried under quote/buy/payment workflow commands. The response still centers on
the dry-run command (`data.recommended_no_spend_command`, aliased by
`data.no_spend_next_command`), and the provider-call, credit-debit, and
media-write false proof in `data.mutation` is retained. The self-fund path
stays discoverable without dominating via
`data.no_spend_output_mode.self_fund_discovery`: its
`rerun_with_funding_command` re-runs the guide without `--no-spend` to surface
the funding templates, and `inspect_methods_command` is a read-only, no-spend
payment-method inspection (the same command as `data.escape_hatches.payment_methods`
when that field is present). `--no-spend` is a guide output mode; it
requires `--guide`, and for a no-spend planned job outside the guide use
`create --dry-run`.

`--no-spend` composes with the state-dependent shaping above: at an unblocked
`ready_to_create` the response is already compact, so
`data.output_mode.omitted_fields` and
`data.no_spend_output_mode.suppressed_fields` together describe what is missing.
At `ready_to_create` the plain guide (no flags) is now the smallest response;
reach for `--no-spend` when you want the suppression declared explicitly, and
for `--explain` when you want everything.

Manual escape hatches are not prerequisites. Use them only when
`data.next_command` / `data.escape_hatches` asks (`data.escape_hatches` is
returned when the guide is blocked and under `--explain`), or when the task
genuinely
needs deeper capability, quota, payment, or planning detail:

```bash
luxin trust
luxin doctor
luxin models list
luxin models show openai.gpt-image-2
luxin whoami
luxin usage quota
luxin create --dry-run --prompt "a compact field camera on a stainless workbench"
```

Use `--show-token --no-save` for hosted signup only when the runtime can
immediately store the raw token once outside local config. For later commands,
saved config is the default; `IMAGE_SKILL_TOKEN` and `--token-stdin` remain
available for runtimes with a separate secret store.
`create --guide` also returns `data.auth_handoff` with copy-safe env/stdin
templates when auth is required or when the returned create command needs the
same auth context.

### Local Config And Install

Prefer package execution in fresh agent sandboxes:

```bash
npm_config_update_notifier=false npx -y luxin-cli@latest create --guide --prompt "a compact field camera on a stainless workbench" --json
```

Global install is optional, not the primary path. If `npm install -g luxin-cli`
or `npx luxin-cli@latest ...` hits prefix/cache `EACCES`, retry with writable
package-manager paths instead of cloning private source:

```bash
export npm_config_cache="${npm_config_cache:-$PWD/.npm-cache}"
export npm_config_prefix="${npm_config_prefix:-$PWD/.npm-global}"
export PATH="$npm_config_prefix/bin:$PATH"
npm_config_update_notifier=false npx -y luxin-cli@latest create --guide --prompt "a compact field camera on a stainless workbench" --json
```

For `npx skills add ... -g -a codex` installs, the writable target is Codex
agent home rather than the npm prefix. If the Codex/global skill target is
read-only or cannot create its default directory, keep the tracked slug install
and point agent skill state at a writable workspace home. The skills.sh Codex
adapter writes to `$HOME/.agents`; `CODEX_HOME` keeps Codex profile state on the
same writable path:

```bash
export HOME="$PWD/.agent-home"
export CODEX_HOME="$HOME/.codex"
mkdir -p "$HOME" "$CODEX_HOME"
npx skills add danielgwilson/luxin --full-depth --skill luxin -g -a codex -y
```

Hosted signup saves auth state to the public CLI config by default. If the
runtime needs a writable compatibility config path, set
`LUXIN_CONFIG_PATH` before `signup`:

```bash
export LUXIN_CONFIG_PATH="$PWD/.luxin/config.json"
# legacy name IMAGE_SKILL_CONFIG_PATH remains honored
npm_config_update_notifier=false npx -y luxin-cli@latest signup --agent \
  --agent-name creative-agent \
  --runtime codex \
  --json
```

Config write failures return `PUBLIC_CLI_CONFIG_WRITE_FAILED` with a structured
`error.recovery.suggested_command`. Agents should follow that recovery field,
then rerun `create --guide` for the requested creative flow.
When `create --guide` reaches `auth_required`, it probes the configured auth
path first. If local config cannot be written, `data.next_command` prefixes the
normal saved-config signup with
`LUXIN_CONFIG_PATH="$PWD/.luxin/config.json"`, so the first recovery
step still saves auth locally without exposing the one-time token.
`--show-token --no-save` and `data.auth_handoff.rerun_guide.with_stdin` remain
structured fallback paths for runtimes that intentionally use a separate secret
store.

### `luxin whoami`

Shows current actor, organization, claim state, token class, and grants.
The JSON includes `session_origin` so a fresh agent can tell whether it is
unauthenticated, loaded a saved config, created the token in this process, or
is using hosted-session auth. `token_created_at` is the active token creation
timestamp when Luxin can prove it, otherwise `null`.

```bash
luxin whoami --json
```

Minimum success data:

```json
{
  "authenticated": true,
  "session_origin": "loaded_from_config",
  "token_status": "active",
  "token_created_at": "2026-05-08T12:00:00.000Z"
}
```

### `luxin usage quota`

Canonical pre-spend check. Shows remaining credits, job limits, model limits,
and reset windows before create/edit.

The starter preview has 50 lifetime credits and a 50-job UTC-day compatibility
cap. Funded identities have no daily job cap: their available prepaid credits
and atomic credit reservations are the spend boundary. For funded identities,
the optional `daily_jobs` object is omitted from the quota response.

```bash
luxin usage quota --json
```

`luxin quota --json` remains a compatibility alias.

Hosted API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/quota \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN"
```

### `luxin credits methods`

Machine-readable payment rail discovery. Use this before quoting or buying so
agents can tell which rails are available, whether live money can move, whether
browser/human action is required, and which command to try next.

```bash
luxin credits methods --json
```

Minimum success data shape:

```json
{
  "contract_version": "image-skill.payment-methods.v1",
  "credit_unit_cents": 1,
  "currency": "USD",
  "quote_endpoint": "/v1/credit-quotes",
  "packs_endpoint": "/v1/credit-packs",
  "status_endpoint": "/v1/credit-purchases/status",
  "next_actions": {
    "recommended_quote": {
      "purpose": "quote_credit_top_up",
      "recommendation_reason": "browserless_agent_self_fund",
      "method_id": "stripe_x402.exact.usdc",
      "pack_id": "starter-500",
      "command": "luxin credits quote --pack starter-500 --payment-method stripe_x402.exact.usdc --json",
      "quote_command_copy_runnable": true,
      "buy_command": "luxin credits buy --provider stripe_x402 --quote-id QUOTE_ID --idempotency-key KEY --json",
      "status_command": "luxin credits status --payment-attempt-id PAYMENT_ATTEMPT_ID --json",
      "requires_auth": true,
      "live_money": true,
      "requires_browser": false,
      "agent_settleable": true,
      "command_effect": {
        "label": "live_money_quote_no_charge",
        "no_spend": true,
        "payment_object": true,
        "credit_debit": false,
        "media_write": false
      }
    }
  },
  "methods": [
    {
      "method_id": "stripe_checkout",
      "status": "available",
      "available": true,
      "quoteable": true,
      "purchasable": true,
      "live_money": true,
      "buyer_modes": ["hybrid", "human_only"],
      "requires_browser": true,
      "agent_initiated": true,
      "agent_settleable": false,
      "settlement_blocker": "requires human browser checkout completion",
      "default_pack_id": "starter-500",
      "purchase_endpoint": "/v1/credit-purchases/stripe-checkout-sessions"
    },
    {
      "method_id": "stripe_x402.exact.usdc",
      "status": "available",
      "available": true,
      "quoteable": true,
      "purchasable": true,
      "live_money": true,
      "buyer_modes": ["agent_only", "hybrid"],
      "requires_browser": false,
      "agent_initiated": true,
      "agent_settleable": true,
      "settlement_blocker": null,
      "default_pack_id": "starter-500",
      "purchase_endpoint": "/v1/credit-purchases/stripe-x402-deposits"
    }
  ]
}
```

Public payment discovery is intentionally action-first. Limited-rollout rails
may be returned with `available:false`, `quoteable:false`, `purchasable:false`,
and a non-null `unavailable_reason` so headless agents can understand the path
without trying it. Use a method only when it is returned with `available:true`,
`quoteable:true`, and `purchasable:true`. When
`next_actions.recommended_quote` is present, prefer its `command` as the next
authenticated quote step; it creates a live-money payment object but does not
move money, grant credits, debit credits, call a provider, or write media.

Hosted API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/payment-methods
```

### `luxin credits packs list`

Lists the recommended Luxin credit packs. Packs are the default
live-money buying UX because agents get obvious starter choices and avoid tiny
fee traps. Use the payment method catalog to choose the rail:
`stripe_checkout` when a human sponsor can complete Checkout, or
`stripe_x402.exact.usdc` when a wallet-equipped agent can settle a browserless
live crypto deposit attempt from returned pay-to instructions.
Exact custom quotes are still supported when an agent already knows the
required credit budget.

```bash
luxin credits packs list --json
```

Minimum success data:

```json
{
  "credit_unit_cents": 1,
  "credit_unit_usd": 0.01,
  "currency": "USD",
  "default_pack_id": "starter-500",
  "packs": [
    {
      "pack_id": "starter-500",
      "name": "Starter",
      "display_name": "Starter (500 credits)",
      "credits": 500,
      "amount_cents": 500,
      "amount_usd": "5.00",
      "price_usd": "5.00",
      "currency": "USD"
    }
  ],
  "custom_quotes": {
    "supported": true,
    "min_credits": 1,
    "max_credits": 5000
  }
}
```

Hosted API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/credit-packs
```

### `luxin credits quote`

Requests a bounded credit quote from the hosted service. Public top-ups use the
payment method returned by `credits methods --json`: `stripe_checkout` for the
human Checkout path, or `stripe_x402.exact.usdc` for a browserless
action-required deposit attempt. A quote never grants credits.
One Luxin credit is a stable user-facing value unit worth `$0.01`.
Creative operations can consume more than one credit based on the selected
model's provider cost and Luxin's margin policy; inspect
`models show MODEL_ID --json` and operation `cost.credit_pricing` for the exact
debit before spending.

```bash
luxin credits quote --credits 10 --payment-method stripe_x402.exact.usdc --json
```

Always pass the payment method from `credits methods --json`; the public CLI
does not infer one. For retry-stable automation, provide an explicit non-secret
idempotency key:

```bash
luxin credits quote \
  --credits 10 \
  --payment-method stripe_x402.exact.usdc \
  --idempotency-key quote-run-001 \
  --json
```

Idempotency keys are scoped to the current hosted agent identity and exact
quote request. Reusing a key with different credits, pack, or payment method
returns a structured `error.recovery.suggested_command` with a fresh
idempotency key for the attempted quote terms.

For Stripe Checkout terms, prefer a named pack:

```bash
luxin credits quote \
  --pack starter-500 \
  --payment-method stripe_checkout \
  --idempotency-key stripe-pack-quote-run-001 \
  --json
```

For the browserless agent x402 rail, quote the exact method id returned by
`credits methods --json`:

```bash
luxin credits quote \
  --pack starter-500 \
  --payment-method stripe_x402.exact.usdc \
  --idempotency-key agent-x402-quote-run-001 \
  --json
```

For exact custom terms, keep the same rail choice. Use
`stripe_x402.exact.usdc` for an agent-settleable browserless rail, or use
`stripe_checkout` only for a human Checkout fallback:

```bash
luxin credits quote \
  --credits 137 \
  --payment-method stripe_checkout \
  --idempotency-key exact-quote-run-001 \
  --json
```

Minimum success data:

```json
{
  "quote_id": "quote_...",
  "state": "created",
  "credits": 10,
  "price_amount_cents": 10,
  "currency": "USD",
  "expires_at": "2026-05-08T20:00:00.000Z",
  "accepted_payment_method": "stripe_checkout",
  "idempotency_key": "quote-run-001",
  "pack_id": null,
  "pack": null,
  "live_money": true,
  "next_actions": {
    "recommended_buy": {
      "purpose": "complete_credit_top_up",
      "recommendation_reason": "human_checkout_handoff",
      "quote_id": "quote_...",
      "method_id": "stripe_checkout",
      "provider": "stripe",
      "command": "luxin credits buy --provider stripe --quote-id quote_... --idempotency-key purchase:quote_... --json",
      "buy_command_copy_runnable": true,
      "purchase_idempotency_key": "purchase:quote_...",
      "status_command": "luxin credits status --quote-id quote_... --json",
      "status_command_copy_runnable": true,
      "status_command_after_payment": "luxin credits status --payment-attempt-id PAYMENT_ATTEMPT_ID --json",
      "status_command_after_payment_copy_runnable": false,
      "requires_auth": true,
      "live_money": true,
      "requires_browser": true,
      "agent_settleable": false,
      "human_handoff_required": true,
      "command_effect": {
        "label": "live_money_payment_attempt_requires_completion",
        "no_spend": false,
        "payment_attempt": true,
        "credit_debit": false,
        "media_write": false,
        "wallet_settlement": false
      }
    }
  }
}
```

For x402 quotes, `accepted_payment_method` is
`"stripe_x402.exact.usdc"`. The quote does not grant credits or include pay-to
instructions; `data.next_actions.recommended_buy.command` carries the returned
`quote_id` and a stable non-secret purchase idempotency key for the
action-required deposit attempt. Run it only when delegated spend is allowed.
Use `data.next_actions.recommended_buy.status_command` to inspect the quote or
payment state by `quote_id`; after buy returns a `payment_attempt_id`, prefer
`status_command_after_payment`.

When `credits status --quote-id quote_... --json` sees an open
`stripe_x402.exact.usdc` or `stripe_checkout` quote, it repeats the exact
`data.next_actions.recommended_buy` command with the real `quote_id` and
`purchase:quote_...` idempotency key so agents do not need to reconstruct the
buy step from placeholders.

Hosted API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/credit-quotes \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN" \
  -H "content-type: application/json" \
  -d '{"pack_id":"starter-500","payment_method":"stripe_x402.exact.usdc","idempotency_key":"agent-x402-quote-run-001"}'
```

### `luxin credits buy`

Creates a payment action for a previously returned quote. Choose the provider
that matches the quote's `accepted_payment_method`.

For a `stripe_x402.exact.usdc` quote, `--provider stripe_x402` creates a
browserless action-required USDC deposit attempt. When the response includes
`stripe_x402.payable_instructions`, a wallet-equipped agent may pay the exact
USDC amount to `deposit_address` on Base without using a browser. The response
is live money when `live_money:true`. Credits are granted only after verified
settlement and webhook fulfillment succeeds. Deposit challenge creation itself
must not mutate credit balances. Stay within the delegated cap and never pass
wallet private keys, seed phrases, x402 payment headers, deposit client
secrets, card data, Stripe secrets, or provider receipts to Luxin.
When `create --guide` enters `quota_required` for this rail, it returns
`data.self_fund_handoff.wallet_settlement` with the buy/status response fields
to inspect, plus `data.self_fund_handoff.first_safe_command` for no-spend rail
inspection before quote/buy: `data.stripe_x402.payable_instructions` after
`credits buy`, or
`data.payment_attempt.stripe_x402.payable_instructions` after `credits status`.

```bash
luxin credits buy \
  --provider stripe_x402 \
  --quote-id quote_... \
  --idempotency-key agent-x402-buy-run-001 \
  --json
```

Minimum x402 action-required data:

```json
{
  "state": "action_required",
  "quote_id": "quote_...",
  "payment_attempt_id": "payatt_...",
  "provider": "stripe",
  "accepted_payment_method": "stripe_x402.exact.usdc",
  "credits": 500,
  "amount_cents": 500,
  "currency": "USD",
  "live_money": true,
  "stripe_x402": {
    "method_id": "stripe_x402.exact.usdc",
    "scheme": "exact",
    "network": "base",
    "token_currency": "usdc",
    "deposit_address_present": true,
    "payable_instructions": {
      "kind": "stripe_crypto_deposit",
      "network": "base",
      "token_currency": "usdc",
      "token_decimals": 6,
      "token_amount": "5.00",
      "token_amount_atomic": "5000000",
      "amount_cents": 500,
      "amount_usd": "5.00",
      "deposit_address": "0x...",
      "token_contract_address": "0x...",
      "supported_token_currencies": ["usdc"],
      "expires_at": "2026-05-08T20:00:00.000Z",
      "exact_amount_required": true
    },
    "redacted": {
      "payment_intent_id": "[redacted-stripe-payment-intent]",
      "deposit_address": "[redacted-stripe-crypto-deposit-address]",
      "client_secret": "[redacted-stripe-client-secret]"
    }
  },
  "next_actions": {
    "recommended_settlement": {
      "purpose": "settle_stripe_x402_credit_top_up",
      "quote_id": "quote_...",
      "payment_attempt_id": "payatt_...",
      "method_id": "stripe_x402.exact.usdc",
      "payable_instructions_path": "data.stripe_x402.payable_instructions",
      "status_command": "luxin credits status --payment-attempt-id payatt_... --json",
      "quota_command": "luxin usage quota --json",
      "command_effect": {
        "wallet_settlement": true,
        "credit_debit": false,
        "media_write": false
      }
    }
  },
  "next": {
    "agent_action": "pay_stripe_crypto_deposit",
    "suggested_commands": [
      "luxin credits status --payment-attempt-id payatt_... --json"
    ]
  }
}
```

For a `stripe_checkout` quote, `--provider stripe` creates a hosted Stripe
Checkout Session and returns an `action_required` response with
`checkout_handoff_url`.

Agents should present or open `checkout_handoff_url` for humans. It is a short
Luxin URL that redirects to Stripe Checkout and is safe to copy from
mobile terminals, SSH clients, and wrapped chat output. `checkout_compact_url`
is also copy-safe and equals the Luxin handoff when the hosted API can
provide one. `checkout_url` is the raw Stripe compatibility fallback only; do
not present it unless no handoff URL is available. Do not trim Stripe Checkout
URLs: the long `#...` fragment is required by Stripe Checkout in the browser.
Present any fallback Stripe URL in a fenced code block so terminal wrapping does
not corrupt it. Stripe-hosted Checkout may also show a promotion-code field for
operator-provided codes; agents should let the human enter those codes on
Stripe, never collect promo codes, card details, or wallet credentials in the
Luxin CLI.

```bash
luxin credits buy \
  --provider stripe \
  --quote-id quote_... \
  --idempotency-key stripe-buy-run-001 \
  --json
```

Minimum success data:

```json
{
  "state": "action_required",
  "quote_id": "quote_...",
  "payment_attempt_id": "payatt_...",
  "provider": "stripe",
  "accepted_payment_method": "stripe_checkout",
  "checkout_session_id": "cs_...",
  "checkout_handoff_url": "https://api.luxin.sh/pay/payatt_...",
  "checkout_compact_url": "https://api.luxin.sh/pay/payatt_...",
  "checkout_url": "https://checkout.stripe.com/c/pay/cs_...#fid...",
  "credits": 500,
  "amount_cents": 500,
  "currency": "USD",
  "live_money": true,
  "next": {
    "human_action": "open_checkout_url",
    "checkout_handoff_url": "https://api.luxin.sh/pay/payatt_...",
    "checkout_compact_url": "https://api.luxin.sh/pay/payatt_...",
    "fallback_checkout_url": "https://checkout.stripe.com/c/pay/cs_...#fid...",
    "after_payment": "open checkout_handoff_url or checkout_compact_url; use the full checkout_url only if no Luxin handoff URL is available, and preserve its Stripe # fragment. Then poll luxin credits status --payment-attempt-id PAYMENT_ATTEMPT_ID --json or luxin usage quota --json; credits are granted only after verified webhook fulfillment"
  }
}
```

Hosted API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/credit-purchases/stripe-checkout-sessions \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN" \
  -H "content-type: application/json" \
  -d '{"quote_id":"quote_...","idempotency_key":"stripe-buy-run-001"}'
```

x402 hosted API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/credit-purchases/stripe-x402-deposits \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN" \
  -H "content-type: application/json" \
  -d '{"quote_id":"quote_...","idempotency_key":"agent-x402-buy-run-001"}'
```

### `luxin credits status`

Without a payment reference, shows the current credit balance using the same
quota data as `luxin usage quota --json`. With a payment reference,
shows the durable state of a quote, x402 deposit attempt, Stripe Checkout
attempt, Checkout Session, or receipt. Use the referenced form after
`credits buy` so agents do not have to infer payment state from quota deltas
or activity text.

```bash
luxin credits status --json
luxin credits status \
  --payment-attempt-id payatt_... \
  --json
```

At most one reference flag is allowed: `--quote-id`,
`--payment-attempt-id`, `--checkout-session-id`, or `--receipt-id`. Passing no
reference returns the balance/quota state.

For Stripe x402 attempts that are still `action_required`, status responses
include `data.next_actions.recommended_settlement` with the same exact Base/USDC
payable instructions, a copy-runnable status command for the real
`payment_attempt_id`, and explicit effect flags showing this is wallet
settlement, not credit debit, media write, or provider generation work.

Minimum action-required data:

```json
{
  "state": "action_required",
  "quote": {
    "quote_id": "quote_...",
    "credits": 500,
    "price_amount_cents": 500,
    "accepted_payment_method": "stripe_checkout",
    "pack_id": "starter-500",
    "x402": null
  },
  "payment_attempt": {
    "payment_attempt_id": "payatt_...",
    "checkout_session_id": "cs_...",
    "checkout_handoff_url": "https://api.luxin.sh/pay/payatt_...",
    "checkout_compact_url": "https://api.luxin.sh/pay/payatt_...",
    "checkout_url": "https://checkout.stripe.com/c/pay/cs_...#fid...",
    "attempt_status": "requires_action"
  },
  "receipt": null,
  "credit_event": null,
  "next": {
    "retry_after_seconds": 10,
    "human_action": "open_checkout_url",
    "checkout_handoff_url": "https://api.luxin.sh/pay/payatt_...",
    "checkout_compact_url": "https://api.luxin.sh/pay/payatt_..."
  }
}
```

Minimum success data includes `state: "succeeded"`, `receipt`,
`credit_event`, and the updated hosted `limits`.

Hosted API equivalent:

```bash
curl -sS "https://api.luxin.sh/v1/credit-purchases/status?payment_attempt_id=payatt_..." \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN"
```

Do not pass card data, wallet secrets, provider receipts, Stripe secrets, MPP
tokens, SPTs, live x402 payment headers, deposit client secrets, wallet
private keys, seed phrases, or any payment credential to credits commands.
Stripe Checkout collects payment details only on Stripe-hosted pages; x402
settlement is handled by the agent/wallet against the returned redacted deposit
challenge, not by pasting credentials into Luxin. The public request
fields are `credits`, `pack_id`, `payment_method`, `quote_id`, status reference
IDs, and `idempotency_key`.

### `luxin models`

First-run creative discovery, in three tiers: `models overview` orients,
`models find` narrows, `models show` goes deep. Start at the tier that matches
what you do not know yet.

```bash
luxin models overview --json
luxin models find --operation image.generate --max-credits 2 --json
luxin models find "seedream" --limit 5 --json
luxin models find --modality video --available --sort credits --json
luxin models show MODEL_ID --json
luxin models show nano-banana --json
luxin models show default --json
luxin models --json
luxin models list --json
luxin models list --details --json
luxin models list --available --operation image.generate --json
luxin models list --available --operation image.edit --json
luxin models list --available --modality video --operation video.generate --json
luxin models list --query nano-banana --json
luxin models list --catalog-only --provider fal --json
luxin models list --operation image.generate --sort credits --limit 10 --json
```

Hosted API equivalents:

```bash
curl -sS 'https://api.luxin.sh/v1/models?view=overview'
curl -sS 'https://api.luxin.sh/v1/models?view=find&operation=image.generate&max_credits=2'
curl -sS https://api.luxin.sh/v1/models
curl -sS 'https://api.luxin.sh/v1/models?available=true&modality=video&operation=video.generate'
curl -sS 'https://api.luxin.sh/v1/models?query=nano-banana'
curl -sS https://api.luxin.sh/v1/models/xai.grok-imagine-image
```

`models overview` is the orientation payload and the cheapest thing to read:
catalog totals (`totals.catalog`, `totals.executable`,
`totals.cataloged_not_wired`, `totals.providers`), one `groups` row per
category with its `operation` token, its `total`/`executable` counts and the
`cheapest` executable model in it, the model alias map, and `next_commands`.
`result_shape` is `model_discovery_overview`. It takes no filters; narrow with
`models find`.

`models find` is the workhorse. It accepts one optional free-text QUERY
positional (equivalently `--query QUERY`) plus `--operation`, `--modality`,
`--provider`, `--available`, `--executable`, `--max-credits N`,
`--sort credits|usd` (default `credits`, ascending), and `--limit N` (default
10, maximum 50). `result_shape` is `terse_model_find` and each row carries only
what a choice needs: `id`, `display_name`, `provider_id`, `modality`,
`operations`, `credits_required`, `estimated_usd_per_image`,
`pricing_confidence`, `self_fundable`, `aspect_ratios`, `max_resolution`,
`status`, and `show_command`. The response also carries `total_matched`, `returned_count`,
and a `narrow_hint` when the limit truncated the match set, so a caller always
knows how much it did not see.

`aspect_ratios` is derived from the full registry server-side. The compact
`models list` row does not publish `media.*` at all, so a client that has to
rebuild find rows from a compact list (an older hosted API) reports
`aspect_ratios: null` and says so in `warnings` rather than guessing.

`self_fundable` says whether payment-backed (purchased) credits can fund the
requests `create` and `edit` send to the model. It is priced at every aspect
ratio the model accepts with the hosted defaults applied, and for edits also at
the default shape, so it is not a property of the default-shape
`credits_required` quote. When it is `false` the row also carries
`self_fund_block_reason`, and a paid-credit request is refused with
`PAYMENT_BACKED_PRICING_UNSUPPORTED` (exit code 6, HTTP 409) before any provider
spend:

- `exact_price_unavailable`: no request shape has a pre-spend price, so paid
  credits cannot fund it at all.
- `aspect_ratio_required`: paid credits fund the model only with an explicit
  `--aspect-ratio`.
- `route_unavailable_for_paid_credits`: the route is not offered on paid
  credits.

`luxin edit` without `--aspect-ratio` sends no ratio. For a model whose `auto`
output size has no pre-spend price, the hosted service then picks a priced
size from the input image's recorded dimensions. Where the model takes a custom
`image_size` with a documented edge limit, it sends the input's own width and
height, scaled into that limit and a 4 MP cap with the shape kept, and reports
`image_size=WxH`. Otherwise it sends the supported aspect ratio closest to the
input's shape and reports `aspect_ratio=W:H`. Both appear in
`selection.model_parameters.defaults_applied`. An explicit
`--aspect-ratio auto` is sent as `auto`; on such a model it is refused on paid
credits, and `models show` says so in `notes`.

Preview credits run every shape. The compact `models list` row carries the
same `self_fundable` and `self_fund_block_reason`, `models show` carries them
under `economics.credit_pricing` with a matching note, and `create --guide` /
`edit --guide` never choose a `self_fundable: false` model unless you name it.

Unlike `models list`, `models find` INCLUDES cataloged-but-not-yet-wired models.
They are marked `status: "not_yet_wired"`, carry an `availability_reason`, and
sort after every executable row. This is deliberate: discovery is where a
catalog entry earns its wiring. Pass `--executable` to exclude them.

`models show` exposes operation support, media input/output types, parameter
schemas, defaults and fixed controls, cost and latency class, safety behavior,
and migration hints. Agents should inspect it before assuming a model supports
seeds, masks, reference images, transparent backgrounds, arbitrary aspect
ratios, image-size presets, output counts, resolution controls, safety
controls, or provider-native options.

`models list` is executable-first by default and returns one
`default: true` row when the default executable create model is included.
`models show default --json` resolves to that model so first-run agents can
inspect the recommended create surface without knowing a provider-specific
model id. `models show` also resolves common migration aliases such as
`nano-banana` to `fal.nano-banana-2`, while `models list --query QUERY --json`
returns fuzzy provider/model-family matches before an agent commits to one
model id. The list response also returns `summary` with total, returned,
available, executable, catalog-only, provider split,
`execution_availability`, first actionable model ids, recommended filter
commands, alias hints, provider/category discovery groups, and
catalog-inclusion flags. Default list output is a compact, sortable model menu
and excludes catalog-only rows so fresh agents see executable candidates first.
Each row keeps the model id, flat
`estimated_usd_per_image`, `credits_required`, lightweight `task_tags`, status,
provider, max output count/resolution, storage, and `show_command`, while
omitting full parameter schemas. Use `models show MODEL_ID --json` for one
model's full capability schema, or `models list --details --json` only when you
intentionally need the full list with capability schemas for compatibility or
offline analysis. `--summary` is still accepted as a compatibility alias for the
default compact list. Use `--available` for currently usable executable rows,
`--modality image|video|audio|3d` for media type, `--operation
image.generate`, `--operation image.edit`, `--operation video.generate`,
`--operation audio.generate`, or `--operation 3d.generate` for the task,
`--provider fal|xai|openai` to narrow by provider, `--query QUERY` to search
ids, display names, provider namespaces, operations, tags, intents, upstream
Fal endpoint ids, and known aliases, and `--catalog-only` when you intentionally
want source-backed rows that are inspectable but not runnable yet.
Provider-level availability is not the same thing as model executability; for
runnable choices require both `status:"available"` and
`execution.model_execution_status:"executable"`. If a reachable provider has no
runnable model for the requested operation, `summary.execution_availability`
says so directly and includes the fastest `--available --operation ...`
recovery command.

`models list` also accepts `--max-credits N`, `--sort credits|usd`, and
`--limit N` (maximum 50) for callers whose filter still matches a hundred rows.
Using any of them adds `summary.narrowing` with the echoed controls plus
`total_matched`, `returned_count`, and a `narrow_hint`; without them the payload
is byte-for-byte what it has always been.

Luxin standardizes common controls so agents can work quickly, but it
must not flatten rich model capabilities into coarse universal categories.
Use `model_parameters` for rare or model-specific parameters advertised by the
capability schema.

Current executable provider-native controls include:

- Fal FLUX.1 dev: `model_parameters.image_size` for presets such as
  `square_hd`, plus `seed`.
- Fal FLUX Pro 1.1 Ultra Create: `model_parameters.seed` and
  `model_parameters.raw`; optional reference-image controls remain cataloged
  for inspection but are not executable on the create-only path.
- Fal Z-Image Turbo Create/Edit: `model_parameters.image_size` for
  `square_hd`, `square`, portrait/landscape presets, and `auto` on edit; costs
  are quoted from requested megapixels when the output size is explicit.
- Fal Nano Banana 2 Edit: `model_parameters.resolution` for `0.5K`, `1K`,
  `2K`, and `4K`, plus `seed`.
- Fal Ideogram V2 Edit: `model_parameters.expand_prompt`, `seed`, and
  `style`; pass masks as top-level `--mask` / `mask_asset_id`, not as
  provider `mask_url`.
- Fal Gemini 3 Pro Image Preview Create/Edit:
  `model_parameters.resolution` for `1K`, `2K`, and `4K`, plus `seed`; 4K is
  quoted as the higher-priced provider tier.
- Fal Nano Banana Pro Create/Edit: `model_parameters.resolution` for `1K`,
  `2K`, and `4K`, plus `seed`; 4K is quoted as the higher-priced provider tier.
- Fal FLUX Pro Kontext Pro/Max Edit: `model_parameters.seed`; guidance scale
  and aspect-ratio controls remain cataloged for inspection but are not
  executable until their UX and receipt behavior are represented.
- Fal Bytedance Seedream 4.5 Create/Edit: `model_parameters.image_size` for
  `square_hd`, `square`, portrait/landscape presets, `auto_2K`, and
  `auto_4K`, plus `seed`; multi-output and multi-reference controls remain
  cataloged but fixed for hosted accounting.
- Fal Bytedance Seedream 5.0 Lite Create/Edit:
  `model_parameters.image_size` for `square_hd`, `square`, portrait/landscape
  presets, `auto_2K`, and `auto_3K`; multi-output and multi-reference controls
  remain cataloged but fixed for hosted accounting.
- xAI Grok Imagine Image Quality: `model_parameters.resolution` for `1k` and
  `2k`; 2k is priced from the higher provider tier. Create supports top-level
  `--output-count` up to the model's advertised `max_outputs_per_request`,
  currently mapped to xAI's documented `n` batch parameter.
- GPT Image 1.5 create/edit: documented fixed sizes `1024x1024`,
  `1024x1536`, and `1536x1024`, output format, compression, transparent or
  opaque background, moderation, and the upstream provider-native quality
  parameter. GPT Image 1.5 create quotes output-token estimates when quality
  and concrete size are known; GPT Image 1.5 create supports top-level
  `--output-count` up to the model's advertised `max_outputs_per_request`,
  currently mapped to OpenAI's `n` parameter. GPT Image 1.5 edit accepts
  low/high `input_fidelity` and remains preflight unknown-cost until usage is
  returned.
- GPT Image 2 create/edit: size, output format, compression, background,
  moderation, and the upstream provider-native quality parameter. GPT Image 2
  create quotes request-aware output-token estimates when quality and concrete
  size are known; GPT Image 2 create supports top-level `--output-count` up to
  the model's advertised `max_outputs_per_request`, currently mapped to
  OpenAI's `n` parameter. GPT Image 2 edit remains preflight unknown-cost, then
  records usage-priced provider cost when OpenAI returns token usage.
- GPT Image 1.5, 2 and 2.5 create bill prompt text tokens per output image on
  top of the output-token quote. When the quoted debit would not cover a
  prompt's text tokens (bounded by its UTF-8 length), the create reserves more
  credits, and the final debit settles down to the token usage OpenAI returns.
  An agent therefore needs credits for that reservation, not only the quote.
  When prompt text raises a settled OpenAI GPT Image charge, create or edit,
  `cost.credit_pricing` reports those credits as `prompt_text_credits`.

Inspect each model before use; provider-native controls are available only
through validated `model_parameters`.

### `luxin capabilities`

Schema-language view over the same capability catalog. Use this when you need
the capability abstraction directly rather than starting from a model.

```bash
luxin capabilities --json
luxin capabilities list --json
luxin capabilities show CAPABILITY_ID --json
```

### `luxin create`

Guides, creates, or plans a zero-cost dry run.

Guide the first image path without mutation:

```bash
luxin create --guide --prompt "A compact field camera on a stainless workbench" --json
```

`create --guide` returns `schema: image-skill.create-guide.v1`,
`stage`, `next_command`, `next_command_copy_runnable`,
`next_command_missing_inputs`, `guide_warning`, `next_command_effect`,
`recommended_no_spend_command` (aliased by `no_spend_next_command`) and its
effect, `output_mode`, selected executable model and cost, auth/quota/payment
blockers, and mutation flags. When the guide is blocked, and at any stage under
`--explain`, it also returns `auth_ready`, `auth_handoff`,
`no_spend_evaluation`, `guide_recovery`, `escape_hatches`,
`self_fund_next_command`, `self_fund_handoff`, and `self_fund_preparation`;
`output_mode.omitted_fields` names whichever of those the current response left
out, and `output_mode.full_output_command` is the rerun that returns them. All
mutation flags must be false in guide mode: no provider call, hosted create,
signup, payment object, credit debit, or media write.
For next-command safety, read `next_command_copy_runnable`,
`next_command_missing_inputs`, and `guide_warning.next_command_safety` before
acting: `hosted_signup_no_spend_setup` is no-spend auth setup,
`live_money_payment_action` is top-up/payment work, and
`live_media_create_credit_debit` is a live create that can call a provider,
debit credits, and write media.
For payment state, read
`checks.payments.preferred_method_summary.top_up_path` instead of inferring
from several arrays. It is `browserless_agent_self_fund` when the preferred
rail is live money, browserless, agent initiated, and agent settleable;
`human_payment_handoff` when a human/browser completion step is required; and
`payment_method_inspection` when the guide cannot classify a direct top-up path.
In guide cost output, `cost.estimated_usd_per_image` is the estimated Luxin
debit in dollars for one output, matching
`cost.estimated_debit_usd_per_image` and
`cost.estimated_credits * cost.credit_unit_usd` when credit pricing is known.
That is the amount the agent needs to fund.
`cost.cheaper_alternative` names one available model that costs strictly fewer
credits than the selection and still satisfies the brief, with its
`model_id` and `estimated_credits`; it is null when the selection is already
the cheapest model that satisfies the brief. Pass its `model_id` to `--model`
to take it.

```bash
luxin create \
  --prompt "A compact field camera on a stainless workbench" \
  --intent explore \
  --aspect-ratio 1:1 \
  --max-estimated-usd-per-image 0.07 \
  --json
```

Hosted defaults are intent-first. If an agent does not choose a model, Image
Skill selects a create capability for the requested intent and budget, then
records the decision in `request.selection`. `--intent draft` (or `cheap`,
`budget`, `test`) selects the lowest-credit available model; `--intent final`
(or `hero`, `product`, `campaign`, `deliverable`) selects the quality-first
model; no intent, or `--intent explore`, selects a cost-efficient
general-purpose model for iteration. A brief that states a reproducibility or
aspect-ratio requirement still gets a model that can express it, even when a
cheaper model cannot: capability outranks price. Explicit
`--provider`, `--model`, namespaced model ids, and validated
`model_parameters` always take precedence. For final/product/hero-style
intents, Luxin may default an eligible quality-capability request to a
higher output tier only when `--max-estimated-usd-per-image` is high enough for
that tier; otherwise it stays on a lower-cost quality tier or chooses a cheaper
capability within the budget and tells agents what happened in the selection
receipt. Use the `--max-estimated-usd-per-image` value returned by
`create --guide`; it is sized to the Luxin credit debit, not only the
upstream provider estimate.

The guide also reads a model named in the brief. "with GPT Image 2.5", "use
Nano Banana", "a Seedream 5 poster", "a FLUX.2 Max render", "a Kling video", and
"Grok Imagine" select that model for the operation (create, edit, or video), and
`selection.reason` says so. The guide picks the most specific model that matches
every word written after the family name: "FLUX.2 Max" is FLUX.2 Max, "FLUX.2"
is FLUX.2, and a bare family name is the model with exactly that name ("Nano
Banana" is `fal.nano-banana`) or, when no model has that name, the family's
default ("FLUX" is FLUX.1 dev). When several rows fit equally and differ only
in version, the newest wins ("Recraft" is Recraft V4.1); when they differ in a
tier ("Seedream 5" fits Flash and Lite), the guide says so and keeps its
default. When a bare name selects that literal row and
newer members of the family can run, `warnings` adds a notice listing up to four
of them, cheapest first, with their credit cost: "Also in this family: Nano
Banana 2.1 (9 cr), Nano Banana 2 (14 cr), Nano Banana Pro (25 cr); pass --model
to choose." Precedence: an explicit `--model` wins, then a
model the brief names, then the intent default. The guide never substitutes a
different version for the one named. It keeps its default selection and says
why in `warnings` and `guide_warning.warning` when any of these is true:

- the named model has no row for the operation ("FLUX.2 has no video model");
- the model is not executable;
- the version is not in the catalog ("FLUX 3", "Kling 4");
- the brief names two different models or versions ("GPT Image 2 and GPT Image
  2.5").

The families are GPT Image, Nano Banana, Seedream, FLUX, Kling, Grok Imagine,
Recraft, Ideogram, Seedance, Veo, Wan, LTX, PixVerse, Hailuo, Luma, Qwen, Stable
Audio, Bria, Z-Image, Gemini, ERNIE, Trellis, plus Imagen and Hunyuan, which the
catalog does not carry and which only produce a notice. A brand that makes only
one kind of media implies it on a clear reference: "a Veo 3.1 clip of a dog"
selects a video model, "use the Trellis model on this photo" a 3D model. Brand
names that are also ordinary words (flux, wan, luma, trellis, ideogram, veo,
gemini, ernie, stable audio) count only on an unambiguous model reference: a
version or tier after the name ("Wan 2.7", "Luma Ray 3.2"), the exact brand
spelling followed by "model" ("the FLUX model"), or a choosing verb before the
exact spelling ("using Wan", "use ERNIE Image"). Only the first two may switch
the operation. A version or snapshot the catalog lacks ("GPT Image 2 Snapshot
2026-04-22") is reported, never matched to the nearest row. "Solder flux", "a
FLUX render", "roses with trellis", "a wan smile", "luma key", and "imagine a
fox" name no model.

Preview-compatible richer shape:

```bash
luxin create \
  --prompt "Campaign-ready product image of a compact field camera" \
  --intent finalize \
  --model MODEL_ID \
  --aspect-ratio 1:1 \
  --output-count 2 \
  --max-estimated-usd-per-image 0.07 \
  --model-parameters-json '{"seed":1234}' \
  --json
```

Use `--output-count N` only when `models show MODEL_ID --json` advertises
`media.output.max_outputs_per_request` greater than `1`. `--output-count` is a
top-level Luxin create control; do not pass provider-native `n` through
`model_parameters` unless the selected model schema explicitly advertises that
field. Credit pricing and `cost.credit_pricing.credits_required` are total
operation debits across all requested outputs. `--max-estimated-usd-per-image`
and raw API `max_estimated_usd_per_image` are per-image Luxin debit
budget guards. They are compared with the quoted debit. Very long prompts on
OpenAI GPT Image models can settle above that estimate by the prompt's text
tokens at the credit rate, shown as `cost.credit_pricing.prompt_text_credits`:
at the 32,000-character limit about $0.07 per output image for English and
$0.27 for text near one token per character. The settled charge never exceeds
the reservation, which bounds prompt tokens by UTF-8 bytes (up to about $1.07
per output image for 4-byte characters).

Generate video through the same `create` command and durable-media loop. For
video prompts, run `luxin create --guide --prompt "..." --json`; the guide
can select the executable video model, suggest `--aspect-ratio 16:9`, and emit
the next create command. The guide uploads nothing, so for a prompt-only brief
it picks a text-to-video model. Image-to-video models need a starting image:
when one is selected (by `--model`, or because no text-to-video model fits),
`next_command` carries `--reference-image IMAGE_PATH` and
`next_command_missing_inputs` names it. `create --dry-run` with an
image-to-video model and no `--reference-image` fails with `BAD_REQUEST`, the
same answer the live call gives. Plain `create` without a model still defaults to an
image model, so use the guide or pass the video model id directly. The response
returns a durable owned `video_...` mp4 asset URL, a `job_id`, and a
`cost.credit_pricing` receipt just like an image create.

```bash
luxin create \
  --model fal.ltx-video-13b-distilled \
  --prompt "A slow dolly push-in on a steaming espresso cup on a cafe counter, morning light" \
  --aspect-ratio 16:9 \
  --json
```

Discover runnable video models with `luxin models list --available
--modality video --operation video.generate --json`. Inspect parameters, output
media type, and cost first with `luxin models show
fal.ltx-video-13b-distilled --json`. Video runs synchronously through the same
create call and can take longer than an image; the returned `assets[].url` is an
owned `video/mp4`.

Generate audio (music, sound) through the same `create` command and
durable-media loop. Request an audio model by id; the response returns a durable
owned `audio_...` wav asset URL, a `job_id`, and a `cost.credit_pricing` receipt
just like an image create. Audio has no aspect ratio, so do not pass
`--aspect-ratio`.

```bash
luxin create \
  --model fal.stable-audio-25-text-to-audio \
  --prompt "A warm lo-fi hip-hop loop with vinyl crackle and a mellow Rhodes piano" \
  --json
```

`fal.stable-audio-25-text-to-audio` (Stable Audio 2.5) is text-to-audio at a flat
$0.20/clip (about 34 credits, quoted before spend) and returns an owned
`audio/wav` clip. The first slice is defaults-only (no tunable
`model_parameters`); duration/steps controls are a later milestone. Inspect
parameters, output media type, and cost first with `luxin models show
fal.stable-audio-25-text-to-audio --json`. Audio runs synchronously through the
same create call and can take longer than an image.

For create models with wired reference support, pass owned reference assets
with the model's advertised reference role. Kling element routes use
`--element-frontal IMAGE[@ELEMENT_INDEX]` and
`--element-reference IMAGE[@ELEMENT_INDEX[:REFERENCE_INDEX]]`; flat
reference-image routes use `--reference-image IMAGE[@INDEX]`; Fal DreamO also
accepts `:TASK` where `TASK` is `ip`, `id`, or `style`. The public CLI uploads
local paths and external URLs first, then
sends top-level `references[]` entries with Luxin `asset_id` values to
`/v1/create`. Do not pass provider-native `elements`, `frontal_image_url`,
`reference_image_urls`, `first_image_url`, `second_image_url`, `images`, or
`*_reference_task` through `model_parameters`; provider-private URLs are
resolved server-side after ownership and media-policy validation.

```bash
luxin create \
  --model fal.kling-image-o3-text-to-image \
  --prompt "Place the same character in a clean studio campaign" \
  --element-frontal ./character-front.png@0 \
  --element-reference ./character-side.webp@0:0 \
  --output-count 2 \
  --max-estimated-usd-per-image 0.06 \
  --json
```

```bash
luxin create \
  --model fal.dreamo \
  --prompt "Studio portrait preserving identity with a bolder editorial style" \
  --reference-image ./identity.png@0:id \
  --reference-image ./style.webp@1:style \
  --model-parameters-json '{"image_size":{"width":1280,"height":720}}' \
  --max-estimated-usd-per-image 0.06 \
  --json
```

High-resolution examples:

```bash
luxin create \
  --prompt "Campaign-ready product image of a compact field camera" \
  --intent final \
  --max-estimated-usd-per-image 0.07 \
  --json

luxin create \
  --prompt "Campaign-ready product image of a compact field camera" \
  --model fal.gemini-3-pro-image-preview \
  --model-parameters-json '{"resolution":"4K"}' \
  --max-estimated-usd-per-image 0.30 \
  --json

luxin create \
  --prompt "Campaign-ready product image of a compact field camera" \
  --model xai.grok-imagine-image-2.0 \
  --model-parameters-json '{"resolution":"2k"}' \
  --max-estimated-usd-per-image 0.14 \
  --json

luxin edit \
  --input-asset-id image_... \
  --prompt "preserve the subject and make this campaign-ready" \
  --model fal.nano-banana-2-edit \
  --model-parameters-json '{"resolution":"4K"}' \
  --accept-unknown-cost \
  --json
```

`model_parameters` must be validated against the selected model/capability
schema before any provider call or paid reservation. Unknown fields fail closed
unless the capability explicitly allows additional properties. This is how
Luxin preserves rare model controls without turning every
provider-specific parameter into a top-level flag.
In the current preview, Fal create/edit, xAI quality generation, and OpenAI GPT
Image 2 expose the executable provider-native controls listed in the selected
model schema. GPT Image 2 create has request-aware output-token credit quotes
for concrete quality/size requests; GPT Image 2 edit still requires
unknown-cost acceptance before execution, but records usage-priced provider cost
after execution when OpenAI returns token usage. Provider-native controls remain
visible for planning and fail closed until their capability schema marks them
executable. Hosted `create --dry-run` validates `model_parameters` against the
selected model, returns accepted keys/provenance and request-aware credit
pricing for planning, and never executes provider controls or consumes credits.
Hosted `edit --dry-run` validates the same owned input, mask/reference,
prompt-policy, budget, and `model_parameters` checks as a live edit, then
returns planned outputs without storage, provider, or billing side effects.
For dry-run responses, `cost.credit_pricing.credits_required` is the planned
live execution debit for the selected model. The actual debit for the dry run is
`quota.consumed_credits: 0`.
Authenticated hosted dry-runs also create a recoverable planned job:
`jobs show` returns `status: "planned"` with `plan_receipt`, and `activity`
emits `job.planned`. Planned receipts do not create downloadable media assets or
usage debits, media writes, or provider execution. In the first-run guide, this
exact no-spend command behavior is exposed as
`data.no_spend_next_command_effect` and
`data.recommended_no_spend_command_effect`; the evaluator stop policy is exposed
as `data.no_spend_evaluation` when the guide is blocked or run with `--explain`.

While the agent can still create, hosted `create` / `edit` responses no longer
repeat the browserless top-up step tree. With more than 5 credits left and
nothing blocked, `data.quota.top_up` is the compact shape dry runs use
(`compacted: true`, every decision field such as `recommended`, `urgency`, and
both payment methods, plus `detail_command: "luxin quota --json"` and
`detail_fields` naming what was left out), and `data.next_actions.self_fund`
keeps its recommendation, urgency, and copy-runnable command fields without a
workflow. With 5 or fewer credits left, `data.quota.top_up` is the full object
and `data.next_actions.self_fund` carries
`workflow_field: "quota.top_up.workflow"`, pointing at that copy. Once credits
are exhausted and the agent is at the wall, `data.next_actions.self_fund.workflow`
is inlined, because that is the block the agent has to act on.

Every hosted `create` / `edit` response carries `data.mutation`, so a no-spend
evaluator reads the proof instead of inferring it from `dry_run` plus a
`planned` asset. On a dry run it reports `provider_call: false`,
`credit_debit: false`, and `media_write: false` explicitly, alongside
`hosted_create_dry_run: true` and, for an authenticated dry run,
`planned_job: true`, `plan_receipt: true`, and `activity_event: "job.planned"`
for the recoverable receipt the dry run does write. An anonymous dry run stores
nothing and reports `planned_job: false` with `activity_event: null`. Each entry
in `data.assets` is labelled: a dry-run placeholder is
`label: "planned_placeholder_not_media"` with `placeholder: true` and
`downloadable: false`, and real output is `label: "durable_media"` with
`downloadable: true`.

Minimum success data:

```json
{
  "job_id": "job_...",
  "capability": {
    "id": "is.image.generate.xai-grok-imagine-image-2-0.v1"
  },
  "assets": [
    {
      "asset_id": "image_...",
      "path": "https://media.luxin.sh/a/image_abc123.jpg",
      "mime_type": "image/jpeg",
      "url": "https://media.luxin.sh/a/image_abc123.jpg",
      "content_length": 333444,
      "width": 1024,
      "height": 1024
    }
  ],
  "cost": {
    "estimated_usd": 0.1,
    "credit_pricing": {
      "credit_unit_usd": 0.01,
      "credits_required": 10,
      "estimated_charge_usd": 0.1,
      "self_fundable": true,
      "self_fund_block_reason": null,
      "pricing_confidence": "known",
      "pricing_source": "model_registry"
    }
  },
  "request": {
    "output_count": 1,
    "selection": {
      "policy": "hosted_default_create_v1",
      "reason": "hosted default selected the strongest currently available quality-first create model",
      "intent": "final",
      "capability": {
        "id": "is.image.generate.xai-grok-imagine-image-2-0.v1"
      },
      "model_parameters": {
        "keys": [],
        "defaults_applied": [],
        "effective_parameters": [
          {
            "name": "quality",
            "value": "medium",
            "source": "provider_default"
          },
          { "name": "resolution", "value": "1k", "source": "provider_default" },
          {
            "name": "response_format",
            "value": "url",
            "source": "provider_default"
          }
        ],
        "source": "none"
      },
      "output": {
        "resolution_class": "1k",
        "expected_width": null,
        "expected_height": null,
        "expected_min_short_edge": 1024
      }
    }
  },
  "safety": {
    "status": "allowed"
  }
}
```

`request.selection.model_parameters.effective_parameters` is the resolved
configuration the request actually ran at. Each entry names one parameter and
where its value came from: `explicit` is a value you passed, `default_policy` is
one Luxin filled in, and `provider_default` is a knob nobody sent that the
provider applies for itself. On Fal image models, `image_size` is translated
from `--aspect-ratio` when you do not pass it, so it is reported as
`default_policy` with the preset actually sent (`landscape_16_9` for `16:9`). `keys` and `defaults_applied` only ever described
the first two, so a request that omitted a parameter had no way to report which
tier it landed on. Use `effective_parameters` to self-audit the tier and to log
a reproducible configuration.

When hosted artifact storage is configured, `url` is an Luxin-owned URL.
Agents should prefer `assets[].url` over provider-origin URLs and should not
need provider account access to fetch outputs.

Hosted create does not accept `--output-dir`. To save the produced file, pass
`--output PATH`:

```bash
luxin create --prompt "a wide hero banner for a coffee shop" \
  --aspect-ratio 16:9 --output ./hero.png --json
```

After a successful create or edit the CLI downloads each produced asset to
PATH (a second and later output get `-2`, `-3` before the extension) and adds
`data.downloads[]`: `asset_id`, `url`, `requested_output_path`, `output_path`,
`status` (`written` or `failed`), `bytes`, `content_type`,
`extension_corrected`, `error`, and `recovery_command`.

The written extension always matches the bytes. If the model returns JPEG and
PATH ends in `.png`, the file is written as `./hero.jpg`,
`extension_corrected` is true, and a warning says so. The CLI does not convert
formats. An existing file is refused before any spend unless `--overwrite` is
passed. A download that fails after the media was created leaves the paid
result intact and carries `recovery_command`, a copy-runnable
`luxin assets get ID --output PATH --json`. With `--dry-run`, `--output` writes
nothing and `data.downloads` is empty. `--output` and `--prompt-file` use the
caller's filesystem, so they run only in the CLI client; the hosted
`POST /v1/cli` refuses them with `DIRECT_CLIENT_REQUIRED`.

`--prompt-file PATH` reads the prompt from a file instead of `--prompt` (pass
one, not both). It works with `create`, `edit`, and their `--guide` modes, and
the guide's emitted commands replay `--prompt-file PATH` instead of inlining
the text. A guide run with `--output PATH` emits a `next_command` that saves to
the same PATH.

When `--aspect-ratio` is omitted, create plans `1:1` and adds a warning naming
that default. If the prompt itself asks for a shape ("16:9", "a wide hero
banner", "an instagram story"), the warning names that ratio and the flag to
pass.

If provider generation succeeds but artifact storage fails, the command returns
`ARTIFACT_STORAGE_WRITE_FAILED` with exit `9` and `retryable: false`. Agents
should not retry the whole create blindly, because that may duplicate paid
provider spend.

For retry-safe create automation, pass an explicit non-secret
`--idempotency-key`. A retry that reuses the same key does not create a second
credit reservation, so a transient `502`/`PROVIDER_FAILURE` that already
reserved a credit cannot double-charge on retry. `create --guide` bakes a
generated `--idempotency-key` into its advertised create `next_command`, and a
retryable create error returns an `error.recovery.idempotency_key` plus an
`error.recovery.suggested_command` that re-runs the same create with that key.

Live non-dry-run create/edit emits one JSON diagnostic line to stderr before
the blocking hosted request:

```json
{
  "in_flight": {
    "command": "luxin create",
    "idempotency_key": "create-...",
    "recover_command": "luxin create --idempotency-key create-... <same arguments> --json"
  }
}
```

stdout carries exactly one JSON document per invocation — the command envelope
— so `JSON.parse` of captured stdout always works. When stdout and stderr are
the same pipe or file and not a terminal (`luxin create --json 2>&1 | ...`),
the CLI skips this stderr line, so the merged stream is still one JSON
document. Other stderr output, such as an `npx` notice, can still appear in a
merged stream; capture stdout alone when parsing.
An agent that captured only stdout still gets the handle: a live create or edit
returns `data.idempotency_key` on success, and `error.recovery.idempotency_key`
plus `error.recovery.recover_command` on any failure. The same recovery
breadcrumb is stored under `<config-dir>/in-flight/` and appears in
`luxin doctor --json` at `data.in_flight`. Keep the in-flight
`idempotency_key` and `recover_command` inside the agent workflow unless a
failed or uncertain operation needs user-visible recovery.

```bash
luxin create \
  --prompt "A compact field camera on a stainless workbench" \
  --idempotency-key create-run-001 \
  --json
```

Hosted free-preview API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/create \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN" \
  -H "content-type: application/json" \
  -d '{
    "prompt": "A compact field camera on a stainless workbench",
    "intent": "explore",
    "aspect_ratio": "1:1",
    "output_count": 1,
    "max_estimated_usd_per_image": 0.07
  }'
```

Hosted free-preview create currently requires owned artifact storage and returns
one `assets[]` entry per output with `assets[].url` under
`https://media.luxin.sh/...` on success. Previously issued
`https://media.image-skill.com/...` URLs remain valid and are still accepted
wherever an asset URL is an input.

#### `luxin create --batch`

Sequential multi-image work — storyboards, animatics, icon and asset packs,
character sheets — as one command instead of one `create` round trip per frame.
The batch runs client-side through the same hosted `create` call, so a batch
item is priced, charged, capped, and recovered exactly like a single create.

The batch document is JSON, read from a file or from stdin with `--batch -`:
shared defaults at the top level, one object per item under `items`.

```json
{
  "model": "fal.bitdance",
  "aspect_ratio": "16:9",
  "seed": 1200,
  "seed_policy": "increment",
  "model_parameters": { "output_format": "png" },
  "items": [
    { "prompt": "panel 1: a compact field camera on a stainless workbench" },
    { "prompt": "panel 2: the same camera, lens detail" },
    { "prompt": "panel 3: hands lifting the camera", "aspect_ratio": "1:1" }
  ]
}
```

Shared keys: `model`, `aspect_ratio`, `intent`, `reference_images`, `seed`,
`seed_policy`, `model_parameters`, `max_estimated_usd_per_image`,
`accept_unknown_cost`, `output_count`. Every shared key except `seed_policy` and
`accept_unknown_cost` can be overridden per item, and each item requires a
non-empty `prompt`. `model_parameters` merges per item over the shared object.
The whole document is validated before anything spends; an invalid item is
rejected by index (`batch item 3: prompt must be a non-empty string`) with exit
code 2 and no hosted create call. Maximum 200 items.

`seed_policy` is `fixed` (every item gets the shared seed), `increment` (shared
seed plus the item offset), or `random`. It threads the seed into
`model_parameters.seed` and only works on a model whose `models show` entry
publishes a `seed` parameter; on any other model the batch fails before spending
and names the model. Every seeded item must name its model (per item or via the
shared `model`): an item that would fall back to server-side model selection
cannot be seed-checked upfront, so the batch refuses it before anything spends.
Per-item `seed` always wins over the policy.

Price the whole sequence first. `--dry-run` makes no spend and no writes:

```bash
luxin create --batch items.json --dry-run --json
```

It returns `schema: image-skill.create-batch.v1` with per-item quotes in
`items[]`, `totals.credits`, and an `affordability` block:
`total_credits`, `remaining_credits`, `covers_items`, `stops_at_item`,
`shortfall_credits`, `daily_jobs_remaining`, `limiting_factor`, a plain
`summary` (`"4 items cost 20 credits; your 12 remaining credits cover 2 of 4;
the batch stops at item 3"`), a `daily_cap_summary` when the item count exceeds
today's remaining jobs, and `top_up.quote_command` sized to the shortfall. When
the job does not fit, `next_actions.self_fund` carries the one funding path for
the whole batch. An item with no published credit quote is reported in
`unpriced_items`: the batch cannot be priced past it, and when the file sets
`accept_unknown_cost` the dry run says a live run will still attempt it at
unknown cost instead of claiming a stop (and mints no top-up for that case).
When the open question is which cheap model fits the brief, answer it with
`luxin models find --available --operation image.generate --max-credits N
--json` before pricing the batch.

A live run executes items in order and reports one digest:

```bash
luxin create --batch items.json --batch-id storyboard-a1 --json
```

Each item carries an idempotency key derived from the `batch_id`, the item
index, and a short hash of the resolved item content
(`storyboard-a1.item-3.4f8a01c2b9de`), so re-running the same file with the
same `--batch-id` after funding skips the items that already completed — they
come back as `status: "skipped_completed"` with their original `job_id` and
zero new credits — while an item you edited between runs gets a fresh key and
re-executes instead of returning the stale asset. `--batch-id` is optional; a
generated one is echoed in `batch_id` and in `resume_command`. For a batch
piped through `--batch -`, `resume_command` uses a `<your-batch-file>`
placeholder and a `resume_note` explains to save or re-pipe the same document
— it is never a bare `--batch -` that would hang waiting on stdin.

An item whose provider is still generating (a slow video or 3D model) comes
back as `status: "pending"` with its `job_id` and a `wait_command`
(`luxin jobs wait JOB_ID --timeout-ms 600000 --json`); its credits are
reserved, it is never counted as delivered, and `totals.pending` counts it.
Run the `wait_command`, or rerun the same file with the same `--batch-id` to
collect it once it completes. A new `--batch-id` would start and pay for new
generations.

At any wall the batch stops cleanly: completed items stay in `data.items` with
their `asset_url`, remaining items are `not_attempted`, `stop_reason` is
`credits_depleted`, `daily_job_cap_reached`, or `item_failed`, and the envelope
carries exactly ONE recovery block — the hosted funding apparatus plus
`error.recovery.batch` with `delivered_items`, `remaining_items`,
`resume_command`, and `price_remaining_command`. Exit code is the wall's own
(5 for quota). Progress lines, one JSON object per item, go to stderr; stdout
stays exactly one JSON document.

`--batch` accepts only `--dry-run`, `--batch-id`, `--json`, and the hosted auth
flags; shared defaults belong in the file, not on the command line.

### `luxin upload`

Normalizes a local image path or remote image URL into an Luxin-owned
input asset for later edit workflows.

```bash
luxin upload ./source.png --json
luxin upload https://example.com/source.png --json
```

The CLI reads local files and remote URLs client-side, then sends image bytes to
`POST /v1/upload`. The hosted API does not fetch arbitrary remote URLs in this
preview. This keeps server-side URL fetching out of the public upload path.

Minimum success data:

```json
{
  "request": {
    "source_kind": "local_path",
    "filename": "source.png",
    "remote_origin": null
  },
  "asset": {
    "asset_id": "image_...",
    "job_id": "job_...",
    "kind": "uploaded",
    "url": "https://media.luxin.sh/a/image_abc123.png",
    "mime_type": "image/png",
    "content_length": 12345
  },
  "upload": {
    "bytes": 12345,
    "mime_type": "image/png",
    "sha256": "...",
    "policy": {
      "status": "allowed"
    }
  }
}
```

Supported preview MIME types are `image/png`, `image/jpeg`, `image/webp`,
`image/gif`, and `image/avif`. Unsupported input returns
`INPUT_POLICY_DENIED` with exit `6`. Responses never include local paths, raw
bytes, base64 payloads, full remote URLs, bucket names, or object keys.

### `luxin edit`

Edits an Luxin-owned input asset or client-normalized local/remote image
with one hosted provider-backed edit model.

```bash
luxin edit \
  --input ASSET_ID_OR_PATH_OR_URL \
  --mask MASK_ASSET_ID_OR_PATH_OR_URL \
  --prompt "Remove the background and keep natural object shadows" \
  --accept-unknown-cost \
  --json
```

If `--input` is a local path or external URL, the public CLI first normalizes it
through the same upload resolver as `luxin upload`, then sends only the
resulting `asset_id` to `POST /v1/edit`. If `--input` is an Luxin asset id
or owned asset URL, edit uses that owned asset directly.
Without `--aspect-ratio`, edit sends no ratio. For a model whose `auto` output
size has no pre-spend price, the hosted service picks a priced size from the
input's recorded dimensions. It keeps the input's own width and height where
the model takes a custom `image_size` with a documented edge limit, scaled down
to at most 4 MP (4,194,304 px, for example 2048x2048) with the shape kept, and
otherwise sends the closest supported aspect ratio. The chosen size appears in
`selection.model_parameters.defaults_applied`, for example
`image_size=2508x1672 (capped from input 6000x4000)`. For a larger output pass
an explicit `image_size` in `--model-parameters-json`. A masked edit is resized
only when the output keeps the mask's dimensions, so a masked input over 4 MP
stays on `auto` and is refused on paid credits; pass `image_size` equal to the
mask's width and height for it. The job's recorded request carries the chosen
ratio or `image_size`, so a recovered request replays the same priced plan. Pass `--aspect-ratio auto` to
send `auto` unchanged.
Add `--dry-run` to plan the edit after owned-asset, prompt-policy,
`model_parameters`, and budget validation. Dry-run edit responses return planned
assets and `quota.consumed_credits: 0`, store a recoverable `job.planned`
receipt, and do not call the provider, debit credits, or write media.
For models with wired mask support, `--mask` follows the same upload/asset-id
resolver and sends only `mask_asset_id`; never pass provider-native `mask_url`
through `model_parameters`.
For models with wired reference support, pass owned reference assets with the
model's advertised reference role. Kling element routes use
`--element-frontal IMAGE[@ELEMENT_INDEX]` and
`--element-reference IMAGE[@ELEMENT_INDEX[:REFERENCE_INDEX]]`; flat
reference-image routes use `--reference-image IMAGE[@INDEX[:TASK]]`. The
public CLI uploads local paths and external URLs first, then sends top-level
`references[]` entries with Luxin `asset_id` values. For Kling element
routes, `--element-frontal ./front.png@0` becomes role `element_frontal` for
element index `0`, and `--element-reference ./side.webp@0:0` becomes role
`element_reference` for the same element with reference slot `0`. For DreamO
create, `--reference-image ./identity.png@0:id` becomes role
`reference_image`, index `0`, and `reference_task` `id`. For xAI edit,
`--reference-image ./reference.png@0` becomes the second ordered source image;
the primary `--input` asset remains the first source image. Do not pass
provider-native `elements`, `image_url`, `image_urls`, `frontal_image_url`,
`reference_image_urls`, `first_image_url`, `second_image_url`, `images`, or
`*_reference_task` through `model_parameters`; provider-private URLs are
resolved server-side after ownership and media-policy validation.
Current public `references[]` support covers Kling Image O1, Kling Image O3
image-to-image/text-to-image, Kling Image v3 image-to-image/text-to-image, and
Fal DreamO create plus xAI Grok Imagine image edit/quality edit. Kling requests
may contain at most 40 reference entries across at most 10 contiguous element
indexes starting at `0`; each referenced element requires one frontal image and
may include up to three additional reference images. DreamO accepts up to two
contiguous `reference_image` indexes starting at `0`, each with optional
`reference_task` `ip`, `id`, or `style`. xAI edit accepts up to two contiguous
`reference_image` indexes starting at `0` and does not accept `reference_task`.
Reference assets must be Luxin-owned PNG, JPEG, or WebP images with
known non-empty byte length up to 10MB, known width and height of at least
300px, and aspect ratio from 0.40 to 2.50.

```bash
luxin edit \
  --model fal.kling-image-o3-image-to-image \
  --input ./starting-frame.png \
  --element-frontal ./character-front.png@0 \
  --element-reference ./character-side.webp@0:0 \
  --prompt "Place the same character in a clean studio product portrait" \
  --accept-unknown-cost \
  --json
```

Direct `/v1/edit` callers use the same owned-asset contract:

```json
{
  "input_asset_id": "image_starting_frame",
  "model": "fal.kling-image-o3-image-to-image",
  "prompt": "Place the same character in a clean studio product portrait",
  "references": [
    {
      "asset_id": "image_character_front",
      "role": "element_frontal",
      "index": 0
    },
    {
      "asset_id": "image_character_side",
      "role": "element_reference",
      "index": 0,
      "reference_index": 0
    }
  ]
}
```

Set `dry_run: true` on `/v1/edit` to get the same no-spend plan the CLI returns.
The server still validates ownership, prompt policy, references, masks,
`model_parameters`, and budget guards before returning the planned job.

Create a 3D asset from an image through the same `edit` command and
durable-media loop. Image-to-3D is image-conditioned and has no prompt field, so
it ships as a variation transform: pass exactly one owned input image (no
prompt) to a 3D model by id and the response returns a durable owned `.glb` mesh asset URL (in
`assets[].url`), a `job_id`, and a `cost.credit_pricing` receipt. A 3D mesh has
no aspect ratio.

```bash
luxin edit \
  --input image_... \
  --model fal.trellis-image-to-3d \
  --json
```

`fal.trellis-image-to-3d` (Trellis) is image-to-3D at a flat $0.02/asset (about 4
credits, quoted before spend) and returns an owned `model/gltf-binary` (`.glb`)
textured mesh. The first slice is defaults-only (no tunable `model_parameters`);
guidance/steps/mesh_simplify/texture_size controls are a later milestone. Inspect
parameters, output media type, and cost first with `luxin models show
fal.trellis-image-to-3d --json`. The input must be one Luxin-owned image.

Prompt policy for 3D models (none of the providers' input schemas has a prompt
field):

- `fal.trellis-image-to-3d` rejects `--prompt` with `INVALID_ARGUMENTS`
  (`model fal.trellis-image-to-3d does not accept --prompt`).
- `fal.trellis-2`, `fal.trellis-multi`, and
  `fal.hunyuan-3d-v3-1-pro-image-to-3d` take `--prompt` as optional and never
  send it to the provider. Omit it.

A 3D run that outlasts the first wait (Hunyuan 3D v3.1 Pro takes about 2
minutes) returns a running job; see `luxin jobs wait` below.

Preview hosted create/edit supports model-specific provider-backed paths such
as Fal Gemini 3 Pro Image Preview Create (`fal.gemini-3-pro-image-preview`),
Fal Nano Banana 2 Edit (`fal.nano-banana-2-edit`), Fal Ideogram V2 Edit
(`fal.ideogram-v2-edit`), Fal Gemini 3 Pro Image
Preview Edit (`fal.gemini-3-pro-image-preview-edit`), Fal FLUX Pro 1.1 Ultra
Create (`fal.flux-pro-v1-1-ultra`), Fal FLUX Pro Kontext Edit
(`fal.flux-pro-kontext`), Fal FLUX Pro Kontext Max Edit
(`fal.flux-pro-kontext-max`), Fal Seedream 5.0 Lite Create
(`fal.bytedance-seedream-v5-lite-text-to-image`), Fal Seedream 5.0 Lite Edit
(`fal.bytedance-seedream-v5-lite-edit`), Fal Seedream 4.5 Create
(`fal.bytedance-seedream-v4-5-text-to-image`), Fal Seedream 4.5 Edit
(`fal.bytedance-seedream-v4-5-edit`), Fal Nano Banana Pro Create
(`fal.nano-banana-pro`), Fal Nano Banana Pro Edit
(`fal.nano-banana-pro-edit`), GPT Image 1.5 Create
(`openai.gpt-image-1.5`), GPT Image 1.5 Edit
(`openai.gpt-image-1.5-edit`), and GPT Image 2 Edit
(`openai.gpt-image-2-edit`) when their provider credentials are configured.
Fal Gemini 3 Pro Image Preview create/edit has known per-image pricing: 1K/2K
requests quote `$0.15` provider cost and 4K quotes the doubled provider tier.
Fal Nano Banana Pro create/edit uses the same `$0.15` standard and doubled 4K
provider tier. Fal FLUX Pro 1.1 Ultra Create quotes `$0.06` provider cost per
image. Fal FLUX Pro Kontext Edit quotes `$0.04` provider cost per image, and
Fal FLUX Pro Kontext Max Edit quotes `$0.08` provider cost per image. Fal
Seedream 4.5 create/edit quotes `$0.04` provider cost per image.
Fal Seedream 5.0 Lite create/edit quotes `$0.035` provider cost per image. Fal
Z-Image Turbo create/edit quotes `$0.005/MP` when `image_size` is explicit or
derived from aspect ratio; edit `auto` remains unknown-cost. GPT Image 1.5
create quotes output-token estimates for concrete quality/size requests using
OpenAI's fixed-size token table; GPT Image 1.5 edit remains preflight
unknown-cost because edit input image/text tokens are provider-metered, then
records usage-priced provider cost when OpenAI returns token usage. GPT Image 2
create quotes output-token estimates for concrete quality/size requests. GPT
Image 2 edit remains preflight unknown-cost because edit input image/text tokens
are provider-metered, then records usage-priced provider cost when OpenAI
returns token usage. Other edit paths without machine-readable pricing require
`--accept-unknown-cost` until a stable price source is captured. Responses
include a new generated asset URL, job id, safety state, quota consumption, and
input asset metadata where
applicable. Responses do not include raw prompts, source bytes, base64
payloads, local paths, full external URLs, bucket names, or object keys.
When `quota.top_up.available` is true, `next_actions.self_fund.quote_command`
is a copy-runnable top-up quote command. `next_actions.self_fund.recommended`
and the mirrored top-up `urgency`, `urgency_score`, and `urgency_reasons` say
whether the agent should act now. The handoff exposes `first_safe_command`,
`first_safe_command_effect`, `inspect_methods_command`, and
`inspect_packs_command` for no-spend payment rail inspection before quote/buy.
The quote command omits `--idempotency-key` so the public CLI generates and
returns one for retry safety before the agent follows the quote response into
`credits buy` and `credits status`.

When a create or edit produced a real durable asset, the same envelope carries
`data.next_actions.share_with_human`: a no-spend, copy-runnable
`luxin claim code --json` plus `share_field: "data.dashboard_url"`. Run it and
hand your human the resulting `dashboard_url` — they can watch this work and
fund your credits from it. Dry runs never carry it, because there is nothing
finished to show.

Provider/model names in this paragraph are preview provenance, not the primary
public UX. The public selection surface should be Luxin capabilities and
model-parameter schemas; provider/model details belong in explicit
provenance/debug output.

Edit accepts the same retry-safe `--idempotency-key` as create. A retry that
reuses the same key does not create a second credit reservation, so a transient
`502`/`PROVIDER_FAILURE` after a reservation cannot double-charge; a retryable
edit error returns an `error.recovery.idempotency_key` and an
`error.recovery.suggested_command` that re-runs the same edit with that key.
Live non-dry-run edit emits the same stderr `in_flight` diagnostic and local
doctor-visible recovery breadcrumb as create, and carries the same
`data.idempotency_key` / `error.recovery.recover_command` handle on the stdout
envelope.

### `luxin assets show`

Inspects an Luxin-owned asset URL or hosted asset id.

```bash
luxin assets show \
  https://media.luxin.sh/a/image_abc123.png \
  --json
```

For asset-id lookup, use hosted auth:

```bash
luxin assets show image_... --json
```

Minimum success data:

```json
{
  "request": {
    "reference": "image_...",
    "reference_type": "asset_id"
  },
  "asset": {
    "asset_id": "image_...",
    "job_id": "job_...",
    "url": "https://media.luxin.sh/a/image_abc123.png",
    "mime_type": "image/png",
    "content_length": 12345,
    "width": 1024,
    "height": 1024,
    "source": "hosted_metadata"
  }
}
```

External URLs are rejected. Older assets created before hosted asset metadata
was recorded may still be inspectable by Luxin-owned URL.

For hosted generated assets, when quota exposes an available top-up path,
`data.next_actions.self_fund` mirrors the top-up recommendation, urgency, and
no-spend payment rail inspection handoff used by create/edit, jobs, and
activity responses. On successful create/edit, when that self-fund action is
recommended and copy-runnable, `data.self_fund_next_command` aliases
`data.next_actions.self_fund.quote_command`; its effect object proves the quote
does not buy, settle a wallet transfer, debit credits, call a provider, create a
hosted job, or write media.

### `luxin assets get`

Downloads an Luxin-owned asset URL or hosted asset id to a local file.

```bash
luxin assets get \
  https://media.luxin.sh/a/image_abc123.png \
  --output ./result.png \
  --json
```

The command refuses to overwrite existing files unless `--overwrite` is
explicit. It verifies byte length when the asset server provides a
`content-length` header. For hosted asset-id downloads, `assets get` preserves
`data.next_actions.self_fund` from the asset metadata response after a
successful download.

### `luxin jobs show`

Inspects a hosted Luxin job visible to the authenticated agent.

```bash
luxin jobs show job_... --json
```

Output includes public job status, trace id, timestamps, capability id, cost
summary, safety status, and Luxin-owned asset metadata. For fresh-agent
parsing, `status`, `state`, `assets`, and `cost` are mirrored at top level and
match `job.status`, `job.assets`, and `job.cost`. Provider/model provenance is
available only through explicit provenance/debug affordances for authorized
actors. Default output does not include raw prompts, generated bytes, provider
credentials, DB/storage keys, bucket names, or local paths.

Minimum success data:

```json
{
  "request": {
    "job_id": "job_..."
  },
  "status": "completed",
  "state": "completed",
  "assets": [],
  "cost": {
    "estimated_usd": 0.05
  },
  "job": {
    "job_id": "job_...",
    "status": "completed",
    "assets": [],
    "cost": {
      "estimated_usd": 0.05
    }
  }
}
```

### `luxin jobs wait`

Waits for a hosted Luxin job to reach a terminal status.

```bash
luxin jobs wait job_... --timeout-ms 100000 --poll-interval-ms 1000 --json
```

Completed jobs return immediately. Non-terminal jobs poll until completion,
failure, cancellation, or timeout. `--timeout-ms` defaults to 100000, the same
command budget as the `create`/`edit` wait, under common 120s agent tool
timeouts; Luxin has no per-model latency to size it from. If the wait ends with
the job still running, the command exits `8` with `JOB_WAIT_TIMEOUT`
(`TIMEOUT` in the published npm CLI), `retryable: true`, a message that names the
job as still running, and `error.recovery.suggested_command`
(`luxin jobs wait JOB_ID --timeout-ms 600000 --json`). The job is not canceled
and its credits stay reserved; do not rerun the create. Terminal success uses the same
top-level `status`, `state`, `assets`, and `cost` mirrors as `jobs show`, with
`request.timeout_ms` and `request.poll_interval_ms` added for provenance.

Running jobs. Some video and 3D models take minutes (Kling 4.0, Hunyuan 3D
v3.1 Pro). When the provider is still working about 70 seconds into a
`create` or `edit`, the hosted API returns HTTP 202 with `data.job_status:
"running"`, `data.assets: []`, and `data.next_actions.wait_for_job`.

- The CLI waits for the job by default and prints the finished result, so
  one command still returns the media. The default wait ends about 100
  seconds after the command started, under common agent tool timeouts;
  `--wait-timeout-ms MS` sets the wait explicitly. A job that fails while
  the CLI waits exits `7` with the job's error.
- If the wait runs out, the CLI prints the running job with
  `data.next_command` (`luxin jobs wait JOB_ID ...`) and exits `0`. Run that
  command; do not rerun the create, which would start and pay for a second
  generation.
- `--no-wait` returns the running job at once. Finish it later with:

```bash
luxin jobs wait job_... --timeout-ms 600000 --json
```

- The credits are reserved when the job starts. They are charged once when
  the job completes and its media is stored, and released if the provider
  reports a failure. If the provider finished but its result cannot be read
  or stored, the credits stay held while Luxin retries, then are released:
  for up to 10 minutes when the result is rejected, missing, or expired
  (HTTP 400/404/410/422, no media URL, or a failed or expired status after
  the provider reported the job finished), and up to 24 hours for temporary
  errors.
  After 45 minutes Luxin asks the provider to cancel;
  the credits stay held until the provider reports a final state (a request
  already mid-processing can still complete, and is then charged), for up
  to 24 hours after the job started, then are released.
- While the job runs, `jobs show` returns `job.async`: `state` (`running`, or
  `cancelling` once a cancel was sent), `credits_reserved`,
  `cancel_requested_at`, and `credits_held_until` (the latest time the
  reservation can last).
- `jobs show` and `jobs wait` finish the job on read; there is nothing else
  to call. A failed job carries `job.error.code` (`PROVIDER_FAILURE` or
  `PROVIDER_TIMEOUT`) and the release appears in `luxin activity list` as
  `credits.reservation_released`.
- Retrying the same `create` with the same `--idempotency-key` returns the
  same running job (HTTP 202, same `next_actions`); it does not start or
  charge a second generation.
- With `--output PATH`, the file is saved once the job completes. With
  `--no-wait`, `--output` writes nothing and says which command finishes it.
- Interrupting a waiting CLI is safe: the job keeps running, and a scheduled
  sweep settles it even if nobody reads it again. Before it waits, the CLI
  writes the job id and its `jobs wait` command to the in-flight record that
  `luxin doctor` reads; `jobs show` or `jobs wait` clears it once the job is
  terminal. While the record names a job, `doctor` lists that `job_id` and
  its `recover_command` is `luxin jobs wait JOB`, never a new create.

### `luxin activity list`

Lists recent hosted activity ledger events visible to the authenticated agent.

```bash
luxin activity list --limit 20 --json
luxin activity list --subject job_... --json
```

Activity is the ledger, not the work queue. Use it to find recent event IDs,
related job IDs, asset IDs, usage IDs, feedback IDs, trace IDs, status changes,
and product-memory writes. Use `jobs show` or `jobs wait` when you need
operational recovery, polling, retry judgment, or final job assets.

When the ledger proves generated work and current quota exposes an available
top-up path, `data.next_actions.self_fund` mirrors the same recommendation,
urgency, and no-spend payment-method inspection handoff returned by successful
create/edit and `jobs show`.

Minimum success data:

```json
{
  "events": [
    {
      "event_id": "evt_...",
      "type": "job.completed",
      "occurred_at": "2026-05-05T19:00:23.000Z",
      "summary": "Create job completed",
      "operation": "create",
      "subject": {
        "type": "job",
        "id": "job_..."
      },
      "links": {
        "job_id": "job_...",
        "asset_ids": ["image_..."],
        "feedback_id": null,
        "usage_event_id": "usage_..."
      },
      "status": "completed",
      "cost": {
        "estimated_usd": 0.025
      }
    }
  ],
  "source": "hosted_activity_ledger"
}
```

The ledger hides provider and storage implementation details by default. It is
safe to cite `evt_...`, `job_...`, `image_...`, `usage_...`, `feedback_id`,
and `trace_id` values in feedback.

Hosted API equivalent:

```bash
curl -sS "https://api.luxin.sh/v1/activity?limit=20&subject=job_..." \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN"
```

### `luxin activity show`

Shows one hosted activity event or the latest events related to one subject.

```bash
luxin activity show evt_... --json
luxin activity show job_... --json
luxin activity show image_... --json
luxin activity show sig_... --json
```

`activity show` accepts activity event IDs plus job, asset, usage, feedback, and
trace references. When the reference is a subject rather than one exact event,
the response includes matching ledger events so an agent can cite the right
event without reading telemetry logs. When current quota exposes top-up
availability after generated work,
`data.next_actions.self_fund.first_safe_command` is the no-spend rail
inspection command to run before any quote/buy step.

Hosted API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/activity/evt_... \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN"
```

### Activity Event Registry

Activity `type` values are stable public contract values. Do not infer new
event names from provider responses or telemetry logs; use only the registry
below.

| Event type                                 | Subject    | Operation   | Emitted when                                                       | Stable links                                                       |
| ------------------------------------------ | ---------- | ----------- | ------------------------------------------------------------------ | ------------------------------------------------------------------ |
| `job.completed`                            | `job`      | create/edit | A hosted create or edit job reaches a terminal state.              | `job_id`, `asset_ids`, `usage_event_id`                            |
| `job.planned`                              | `job`      | create/edit | An authenticated hosted dry-run stores a recoverable plan receipt. | `job_id`                                                           |
| `asset.created`                            | `asset`    | create/edit | A hosted create or edit produces an output asset.                  | `job_id`, `asset_ids`, `usage_event_id`                            |
| `asset.uploaded`                           | `asset`    | upload      | A public edit workflow uploads or imports input media.             | `job_id`, `asset_ids`, `usage_event_id`                            |
| `usage.credit_consumed`                    | `usage`    | usage       | A creative operation records a preview-credit entry.               | `job_id`, `usage_event_id`                                         |
| `feedback.created`                         | `feedback` | feedback    | Hosted agent feedback is accepted into product memory.             | `feedback_id`                                                      |
| `feedback.github_queue.processed`          | `feedback` | feedback    | Feedback is processed by the GitHub implementation queue handoff.  | `feedback_id`                                                      |
| `payment.checkout_session.created`         | `payment`  | payment     | A Stripe Checkout session is created and awaits external action.   | `quote_id`, `payment_attempt_id`, `checkout_session_id`            |
| `credits.payment_backed_granted`           | `credit`   | credits     | Verified payment fulfillment grants paid credits.                  | `quote_id`, `receipt_id`, `credit_event_id`                        |
| `credits.payment_backed_refunded`          | `credit`   | credits     | A Stripe refund debits payment-backed credits.                     | `quote_id`, `receipt_id`, `payment_reversal_id`, `credit_event_id` |
| `credits.payment_backed_disputed`          | `credit`   | credits     | A Stripe dispute debit applies to payment-backed credits.          | `quote_id`, `receipt_id`, `payment_reversal_id`, `credit_event_id` |
| `credits.payment_backed_reinstated`        | `credit`   | credits     | Stripe dispute funds were reinstated and recorded.                 | `quote_id`, `receipt_id`, `payment_reversal_id`                    |
| `credits.payment_backed_reversal_pending`  | `credit`   | credits     | A reversal was recorded but could not be fully applied.            | `quote_id`, `receipt_id`, `payment_reversal_id`                    |
| `credits.payment_backed_reversal_rejected` | `credit`   | credits     | A reversal was rejected because it could not safely reconcile.     | `quote_id`, `receipt_id`, `payment_reversal_id`                    |
| `credits.reservation_released`             | `credit`   | credits     | Reserved credits return after a provider failure, timeout, or TTL. | `job_id`                                                           |

`feedback.github_queue.processed` includes `details.github_queue` with
machine-readable lifecycle fields such as `state`, `reason`, `issue_urls`,
`issue_numbers`, `mode`, and `github_mutation`. Agents should use it to learn
whether submitted feedback was promoted, skipped, deduped, blocked, or already
mirrored without reading private repository artifacts.
`job.planned` includes `details.plan_receipt` for authenticated hosted
dry-runs. It is a recoverable planning receipt, not completed media work:
planned outputs do not have durable asset IDs, download URLs, usage debits, or
provider execution.

If a response includes an event type outside this registry, treat it as a
contract bug and submit `luxin feedback create --json` with the event ID
and trace ID.

### Receipts (`GET /v1/receipts`)

Returns the authenticated agent's payment receipts, payment reversals, and
credit grants, newest first. Activity is bounded, so a busy agent's job events
push older payments out of it; receipts are read from the payment ledger and
stay visible. There is no CLI command yet; call the hosted route with the saved
token. It never spends.

```bash
curl -sS "https://api.luxin.sh/v1/receipts?limit=20" \
  -H "Authorization: Bearer $TOKEN"
```

`limit` is an integer from 1 to 100 and defaults to 50. `data.receipts[]`
entries:

| Field           | Meaning                                                                                  |
| --------------- | ---------------------------------------------------------------------------------------- |
| `kind`          | `payment`, `reversal`, or `grant`.                                                       |
| `reference`     | The id to quote about this entry: the `receipt_` id, the reversal id, or the grant's id. |
| `receipt_id`    | The payment a reversal applies to; the payment itself for `kind: payment`.               |
| `occurred_at`   | ISO 8601 timestamp.                                                                      |
| `credits`       | Signed: positive adds credits, negative removes them.                                    |
| `amount_cents`  | Money paid or returned, in minor units of `currency`. `null` for a grant.                |
| `provider`      | `stripe` for card and USDC payments, `fake` for test-mode purchases, `null` for a grant. |
| `reversal_kind` | `refund`, `dispute`, `dispute_funds_withdrawn`, `dispute_funds_reinstated`, or `void`.   |
| `status`        | `succeeded` for a payment, the reversal status for a reversal, `granted` for a grant.    |

The human dashboard reads the same route with its session cookie.

### `luxin feedback create`

Leaves structured product feedback in hosted Luxin product memory.
At minimum, provide `--title` and `--body`; Luxin accepts narrative
feedback and adds quality guidance server-side. Use the structured fields below
when the agent already knows them.

```bash
luxin feedback create \
  --type user_feedback \
  --title "Short concrete title" \
  --body "What happened, what was expected, and why it matters" \
  --command "Command or workflow observed" \
  --expected "Expected result" \
  --actual "Actual result" \
  --proof-needed "What would prove this is handled" \
  --surface cli,docs \
  --evidence trace:TRACE_ID \
  --severity medium \
  --confidence high \
  --next-state watch \
  --json
```

Hosted feedback authenticates the same way as other hosted commands: saved
public CLI config from default signup, `IMAGE_SKILL_TOKEN`, or
`--token-stdin`. If guide/signup already saved config, run `feedback create`
normally; no raw token copy step is required. If the runtime uses its own
secret store, prefer `IMAGE_SKILL_TOKEN` or `--token-stdin`. Do not paste tokens
into feedback title, body, evidence, issues, or logs. Feedback persists through
`https://api.luxin.sh/v1/feedback`. The hosted API fails closed if
durable hosted feedback storage is unavailable.

Provider input and moderation rejections from hosted `create` and `edit`
return HTTP `422` with `error.retryable: false`. The local CLI uses the same
error codes and recovery fields:

| `error.code`                | `error.recovery.reason` | `error.recovery.action`   |
| --------------------------- | ----------------------- | ------------------------- |
| `MODERATION_BLOCKED`        | `content_policy`        | `revise_prompt_or_inputs` |
| `IMAGE_TOO_SMALL`           | `image_too_small`       | `fix_inputs`              |
| `PROVIDER_VALIDATION_ERROR` | `validation_error`      | `fix_inputs`              |

Follow `error.recovery.message` before submitting again: revise the prompt or
input images for moderation, or correct invalid inputs and run dry-run. If the
inputs already meet the model limits, report the `trace_id` with
`luxin feedback create`. Retrying unchanged inputs does not resolve these
rejections. Transient upstream failures, including provider-directed retries
and failures to download a signed asset URL, retain HTTP `502`,
`PROVIDER_FAILURE`, `error.retryable: true`, and the existing retry recovery.

JSON errors may include `error.recovery` with machine-readable fields such as
`required_flag`, `suggested_command`, `docs_url`, or `retry_after_seconds`.
Agents should prefer those fields over parsing prose error messages. For
example, `BUDGET_REQUIRES_CONFIRMATION` returns
`required_flag: "--accept-unknown-cost"`.
Quota/payment recovery also includes `error.recovery.top_up`: its
`quote_command` is copy-runnable and creates an authenticated live-money
quote/payment object without paying, settling a wallet transfer, debiting
credits, calling a provider, or writing media. Only the later buy/status and
wallet/checkout completion steps can spend money.

`whoami`, `usage quota`, `quota`, `credits quote`, `credits buy`,
`credits status`, `create`, `activity list`,
`activity show`, and `feedback create` accept `--token-stdin` for stdin-based
secret handoff.
`credits methods` and `credits packs list` do not require auth.

Feedback should avoid raw prompts, hosted tokens, provider keys, generated
image bytes, source image bytes, and private user data.

Hosted API equivalent:

```bash
curl -sS https://api.luxin.sh/v1/feedback \
  -H "authorization: Bearer $IMAGE_SKILL_TOKEN" \
  -H "content-type: application/json" \
  -d '{
    "type": "user_feedback",
    "title": "Short concrete title",
    "body": "What happened, what was expected, and why it matters",
    "command": "Command or workflow observed",
    "expected": "Expected result",
    "actual": "Actual result",
    "proof_needed": "What would prove this is handled",
    "surface": ["cli", "docs"],
    "evidence": ["trace:TRACE_ID"],
    "severity": "medium",
    "confidence": "high",
    "next_state": "watch"
  }'
```

### Planned Resource Commands

`jobs list`, `assets list`, `assets delete`, and async job cancellation are
planned public resource commands. They are not part of the current public
allowlist until the hosted service backs them and this contract lists their
exact command shapes. `activity list/show` is available now for ledger
readback, but it is not a substitute for future job listing, cancellation, or
retry controls.
