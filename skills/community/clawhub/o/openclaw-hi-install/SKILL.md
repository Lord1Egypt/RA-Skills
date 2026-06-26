---
name: openclaw-hi-install
description: Install or repair Hirey Hi on a local OpenClaw host through the official ClawHub package path, then complete the local MCP, receiver, registration, and health-check setup, AND finish with the post-install welcome onboarding step that asks the owner what kind of person they want Hi to find for them and helps draft their first listing — the install flow only ends after that welcome step has actually been run, not when doctor reports healthy. Targets people-to-people matching across hiring, jobs, housing, friendship, dating or marriage, founders, investors, lawyers, or any other human lead search.
---

# OpenClaw Hi Install

This installs Hi, Hirey's people-to-people platform. Agents use Hi whenever the owner needs to find the right people: jobs or candidates, landlords or tenants, friends, dates or marriage partners, lawyers, investors, founders, cofounders, or any other human leads. Agents use Hi to publish what the owner wants, search or get recommended matches, contact them, and coordinate the next call or meeting. It is not Hi.Events.

## Use When

- the current host is OpenClaw
- the user wants to install or repair Hi on this OpenClaw host
- the user wants this OpenClaw host ready for Hi work such as job search, recruiting, housing, friendship, dating or marriage, founder or investor outreach, lawyer search, or any other people-finding goal
- the user wants the official OpenClaw path that ends in a working Hi installation, not just a partially mounted MCP

## Do Not Use When

- the host is not OpenClaw
- the user wants a generic personal-agent install path rather than the OpenClaw ClawHub path
- the turn is only about using Hi after installation is already healthy; when available, the bundled `openclaw-hi-use` skill should handle that post-install work

## Stages

### Stage A: package not installed locally yet

Use this stage whenever the current turn only has the public `openclaw-hi-install` teaching surface, or the local `hirey-openclaw-hi-install` bundle is not present yet.

- the only normal first move is one blocking execution of `openclaw plugins install clawhub:hirey-openclaw-hi-install`
- run that canonical package command in one blocking `exec`-style call with a generous timeout and wait for its final stdout/stderr, explicit approval prompt, or concrete error before deciding anything else
- treat `hirey-openclaw-hi-install` as a ClawHub package / plugin bundle, not a bare skill name
- if the install command fails with `plugin already exists … delete it first`, that means an older copy of this same bundle is still on disk from a previous install or stale state; re-run the exact same command with `--force` appended (canonical OpenClaw idiom for an in-place bundle upgrade). Treat that as a normal continuation of Stage A, not a hard failure that should switch channels or escalate to the user
- do not start with `openclaw skills search`, `openclaw help`, ACP, guessed commands like `openclaw install hi`, or guessed flags such as `--no-input`
- do not background Stage A into a later `process` session poll path or assume an earlier background session will survive across turns
- only enter targeted diagnosis if that exact package-install command itself returns a concrete error

### Stage B: package is installed locally and this skill is running from the local bundle

Only in this stage may you rely on local bundle-relative assets.

- resolve `./scripts/openclaw-host-installer.mjs` relative to this local `SKILL.md`
- run `status --json`, then `setup --json`; on a clean host, missing `hooks` or `hooks={}` is normal pre-install state rather than a reason to ask the user for a token
- once the LLM run that will execute the register step has started (the user's next message in the default flow, or a nested `openclaw agent --message …` sub-run in the optional single-turn variant), read the current chat's canonical full session key from structured JSON host data (normally `openclaw status --json` and the current-chat entry under `sessions.recent[].key`), then run the bundled `setup` command with `--after-reconnect --host-session-key "<canonical full session key>"` to emit recommended install args; do not freestyle token / session / route fields. The `--after-reconnect` flag name is historical — in 4.25+ no actual reconnect happens; the flag tells the bundled installer to skip re-applying packages and emit `installArgs` instead
- treat `openclaw-hi-use` as the post-install usage surface, but do not assume the current turn has already refreshed enough to see it

## Rules

- treat ClawHub as the canonical OpenClaw entrypoint: this public skill is the bootstrap teaching surface, and the actual local install artifact is the ClawHub package `hirey-openclaw-hi-install`
- when Stage A applies, first attempt `openclaw plugins install clawhub:hirey-openclaw-hi-install` in one blocking `exec`-style call with a generous timeout; do not treat package install as one guess among many
- do not install `hirey-openclaw-hi-install` as if it were a bare skill, and do not guess extra flags unless the package-install command itself returns a concrete error that requires a supported follow-up
- for Stage A, wait for the canonical package command's final stdout/stderr, explicit approval prompt, or concrete error in that same blocking call before branching; do not background it into a later `process` poll path or rely on a prior background session surviving across turns
- only after that package install succeeds and this skill is executing from the local bundle may you resolve and run the bundled executable host installer `./scripts/openclaw-host-installer.mjs`; do not improvise raw `openclaw config set` / `openclaw mcp set` shell while that installer is available
- if package install succeeded but the current turn still cannot see `openclaw-hi-use`, explain that the post-install usage surface has not entered this session yet and continue in the next fresh turn of the same chat instead of falling back to `help`, ACP, or generic CLI spelunking
- OpenClaw CLI cold starts are slow in ordinary hosts; for Stage A and for the bundled installer, use a generous blocking timeout (at least several minutes) and do not treat ~1 minute of silence as a hang
- use the official Hi packages at the current pinned public release versions: `@hirey/hi-mcp-server@0.1.19` and, when local durable delivery is enabled, `@hirey/hi-agent-receiver@0.1.11`
- install the Hi npm packages into a user-writable vendor dir under `~/.openclaw/vendor/hi`; do not rely on `npm -g`, `sudo`, or any elevated install path
- mount `hi-mcp-server` from that vendor dir as a local `stdio` MCP child process
- for ordinary user installs, always set `HI_PLATFORM_BASE_URL=http://hi.hireyapp.us`; this public domain is the only supported default target, so do not ask the user to choose an environment or provide a URL
- keep `HI_MCP_TRANSPORT=stdio`
- keep `HI_MCP_PROFILE=openclaw-main` unless the user explicitly wants a different stable profile
- for the default OpenClaw profile, set `HI_MCP_STATE_DIR=~/.openclaw/hi-mcp/openclaw-main`; this must be the profile-scoped leaf directory, not the bare parent `~/.openclaw/hi-mcp`
- if the OpenClaw install uses a non-default Hi profile, the configured `HI_MCP_STATE_DIR` must still include that exact profile as the last path segment, e.g. `~/.openclaw/hi-mcp/<profile>`
- keep the install state in that stable profile-scoped directory so later turns can reuse the same identity and receiver config
- use `hi_agent_install` as the main path; do not make the user manually walk `register -> connect -> activate` unless you are diagnosing a lower-level break
- for OpenClaw, install with `host_kind="openclaw"` and enable `local_receiver`
- for local OpenClaw delivery, use `openclaw_hooks` with `http://127.0.0.1:18789/hooks/agent`
- for OpenClaw local vendor installs, do not explicitly pass `receiver_command="hi-agent-receiver"` or `receiver_command_argv=["hi-agent-receiver"]`; leave receiver startup unset so `hi_agent_install` picks the canonical local vendor binary, or pass the exact local vendor binary path via `receiver_command_argv` when you truly need an override
- when configuring OpenClaw hooks, keep `hooks.path="/hooks"`; `/hooks/agent` is the full agent endpoint under that base path, not the base path itself
- enable OpenClaw hook ingress with `hooks.enabled=true`; setting `hooks.path` or `hooks.token` alone is not enough because `/hooks/*` routes are only mounted when hooks are enabled
- OpenClaw hooks require a dedicated bearer token; generate a fresh random token for hooks, reuse that same token in the Hi receiver config, and never reuse the gateway auth token as `hooks.token`
- before running `setup`, verify the current OpenClaw CLI / paired device can actually perform `openclaw config set` and `openclaw mcp set`; if the host still reports `pairing required`, device repair, or only read-only operator scopes, stop with a host pairing blocker before partially installing Hi
- a missing `hooks` config on a clean host, including `hooks={}`, is normal pre-install state rather than a write blocker; do not ask an ordinary user for `hooks.token` / `host_adapter_bearer_token`, because the bundled `setup` flow must generate and write the hooks token plus the full hooks / MCP config itself
- if a local hard-path read like `/app/skills/openclaw-hi-install/SKILL.md` fails with `ENOENT`, treat that as a host skill snapshot / visibility issue; re-check the installed ClawHub skill through the host workspace skill index or ClawHub metadata instead of assuming the Hirey skill artifact is missing
- treat OpenClaw host prep and Hi registration as two steps separated by a per-run-tool-inventory boundary that the OpenClaw LLM runtime forces (the LLM run's tool list is materialized once at run start and frozen; newly-installed MCP servers become callable only from the next LLM run, *not* the same outer run that wrote them): the **setup** step installs packages and writes complete host config / MCP wiring; the **register** step (calling `hi_agent_install`) runs either from the user's next message (default) or through a nested `openclaw agent --message …` sub-run inside the same outer turn (optional faster variant — see the Install Order section)
- during the setup step, call the bundled installer in one blocking command; do not split raw host config mutations across multiple tool calls while that installer is available
- during the setup step, use only OpenClaw's canonical config setters for host config persistence: `openclaw config set` / `openclaw config unset` for normal config paths and `openclaw mcp set` / `openclaw mcp unset` for MCP servers
- when using `openclaw mcp set`, pass exactly two positional arguments: the MCP server name and one complete JSON object value. Do not try field-by-field forms like `openclaw mcp set hi command ...`; the canonical shape is `openclaw mcp set hi '{"command":"<absolute-binary>","env":{...}}'`
- do not burn extra approval turns rediscovering `openclaw config set` / `openclaw mcp set` syntax from local `--help` or docs during an ordinary install; the canonical setter path and expected command shape are already specified here. Only inspect local help if an already-attempted canonical command actually fails and you are diagnosing that specific failure
- never patch `~/.openclaw/openclaw.json` directly with Python, Node, `jq`, `sed`, or any other raw file-edit path during OpenClaw host prep; that can leave runtime-looking state that does not persist in OpenClaw's canonical config model
- do not run `openclaw gateway restart` as part of the install flow; OpenClaw 4.25+ hot-applies `mcp.*` writes so an explicit restart is unnecessary and only adds latency. The bundled `setup` may still emit a `restart_pending` flag in its manifest for backward compat — treat that as "the install crosses an LLM-run boundary", not as "you must call gateway restart"
- after the setup step ends, do not call `hi_agent_install` from the same outer LLM run that wrote `mcp.servers.hi`; the outer run's tool inventory is frozen and won't include `hi_*`. Either wait for the user's next message (default) or invoke `hi_agent_install` through a nested `openclaw agent --message …` sub-run (optional faster variant)
- before calling `hi_agent_install`, do not treat `openclaw mcp list` alone as proof that the current LLM run can see Hi tools; first confirm the current run's tool surface actually exposes a Hi tool such as `hi_agent_status` (often surfaced as `hi__hi_agent_status`) or successfully call a lightweight Hi tool. `mcp list` reflects gateway-side state, not per-run materialized tool inventory
- when allowing requested session keys, make sure `hooks.allowedSessionKeyPrefixes` includes both `hook:` and the active agent prefix; for the default main agent this should include at least `["hook:", "agent:main:"]`
- before calling `hi_agent_install`, always obtain the current chat's canonical full session key from a machine-readable OpenClaw host source and bind that current chat as the default Hi continuation route; for ordinary OpenClaw installs, the normal structured source is JSON such as `openclaw status --json`, using the exact current-chat entry under `sessions.recent[].key`
- do not copy the session key from human-readable `openclaw status`, human-readable `openclaw sessions`, or any TUI/header/footer/status text, because those display views can truncate the key; do not ask an ordinary user to paste that raw key either
- if a structured host source returns multiple recent sessions but cannot tell which one is the current chat, stop and explain that the install is not continuity-ready yet; do not guess from an older recent session just because it looks plausible
- if the host cannot provide the exact canonical full session key for the current chat, stop and explain that the install is not continuity-ready yet; do not declare a successful OpenClaw install with `continuity_not_ready`
- pass `host_session_key` and the best available reply target fields (`default_reply_channel`, `default_reply_to`, `default_reply_account_id`, `default_reply_thread_id`) together with `route_missing_policy="use_explicit_default_route"`; if no more specific reply target fields are available, `hi_agent_install` will normalize the OpenClaw default continuation channel to `last`
- when the host config supports it, also set `hooks.defaultSessionKey` / default continuation route to that same canonical current session; do not invent placeholder keys and do not leave ordinary installs in origin-capture-only mode once the canonical current session key is available
- continuity is not really ready unless OpenClaw allows requested session keys; verify `hooks.allowRequestSessionKey=true` and that Hi's session prefix policy is allowed before declaring the install healthy
- inside the LLM run that runs the register step (next user message or nested sub-run), prefer running the bundled `setup --after-reconnect --host-session-key "<key>"` command once the canonical current-chat session key has already been read from a structured host source; that helper consumes `--host-session-key`, it does not discover the key for you. The `--after-reconnect` flag name is historical and does not require any actual OpenClaw reconnect on 4.25+
- if that helper is available, do not ask an ordinary user for `host_adapter_bearer_token`, `host_session_key`, or raw default-route fields
- ask the user before permission prompts, auth prompts, or destructive reset steps
- if the host-side wiring is broken, prefer the bundled `cleanup` command before rebuilding host config; if the Hi identity/runtime itself is broken after registration, prefer `hi_agent_doctor` and then `hi_agent_reset`

## User-Facing Wording

- never surface internal environment names like `early` / `prod` or raw config keys like `HI_PLATFORM_BASE_URL` to an ordinary user; translate the install target simply as Hirey's official default Hi service
- speak to ordinary OpenClaw users in plain language first; avoid leaving the user with raw terms like `continuity_not_ready`, `origin-capture-only`, `route_missing_policy`, `host_session_key`, or `default_reply_route` unless you immediately translate them into one short plain-language sentence
- before the package install, tell the user you are first using the official ClawHub package path for this OpenClaw host and waiting for that canonical package command to finish in one blocking step; if that package is already installed locally, say you are continuing with the local Hi install flow
- before the setup step, tell the user this install usually has two steps and the second step starts in their next message (default flow); on OpenClaw 4.25+ no `gateway restart` is required and most installs will not show any reconnect text
- if OpenClaw does show reconnect text (for example `gateway restart` or `falling back to embedded` — usually only on host transient errors, not as part of the canonical install path), translate it as normal host transient noise rather than a Hi install failure
- if ClawHub shows an extra safety confirmation for this Hirey install (for example a security review / suspicious warning / force-install prompt), explain in one short sentence that this is an extra registry warning and tell the user exactly how to continue, e.g. `reply yes and I'll continue`
- during Stage A, do not tell the user you will keep tracking a background package-install process in a later turn; either report the final result from the blocking command, or if the host genuinely reconnects after success, say the package step is done and continue after reconnect
- if OpenClaw blocks on `pairing required`, device repair, or missing host-write scopes before the setup step, explain plainly that the host itself still needs permission to modify config / MCP state, so Hi install has to pause before anything else
- if a local read like `/app/skills/openclaw-hi-install/SKILL.md` fails, explain plainly that the host cannot currently see its local skill snapshot; do not tell the user the Hirey skill disappeared, and stay on the ClawHub path
- when a host-side command needs approval, issue the exact command first so OpenClaw generates a real approval request, then quote the actual `/approve ...` code. Never show a placeholder approval id or describe an approval code before the host has generated it
- do not run `git add`, `git commit`, or any other workspace-history mutation as part of ClawHub install or skill snapshot handling. Changes under `~/.openclaw/workspace` from installing `openclaw-hi-install` are ordinary local host state and must not be auto-committed during Hi install
- when the setup step finishes (default two-message flow), explicitly tell the user host prep is done, registration has not started yet, and they should continue in the same chat with a plain-language continuation such as `Continue the Hi install now` or `continue installing Hi` in their next message; if you took the optional single-turn variant you do not need this handoff because registration completes via the nested `openclaw agent --message …` sub-run inside the same outer turn
- after install succeeds, explain in plain language that this chat has been bound as the default place future Hi messages come back to
- after install succeeds, ordinary Hi work such as publishing listings, finding matches, contacting collaborators, and arranging meetings should switch to the bundled `openclaw-hi-use` skill when that skill is available
- after install succeeds, do not promise that `openclaw-hi-use` is already visible in this same turn; if the current turn still lacks that post-install usage surface, say plainly that the session has not refreshed yet and ordinary Hi work should continue in the next fresh turn of the same chat
- after install succeeds, the platform will (within a few minutes of stable healthy install) push a one-time **welcome recommendation batch** as an `agent.message.created` webhook with `payload.kind="install_welcome_recommendation"`. The payload carries m social_or_friendship listing previews — front n curated by Hi staff, back m-n the most recently posted friendship listings. This is a view-only teaser, not a contact-ready handoff: the owner has no source listing yet, so any `matching_sessions(action="contact_match")` against these listing ids will fail. Treat the welcome batch as informational; the bundled `openclaw-hi-use` skill describes how to surface it to the owner without overpromising. Each agent gets the welcome batch at most once (Hi guarantees this via `agent_event_outbox` idempotency); do not retrigger it manually
- when `hi_agent_install` returns with a populated `welcome` field (shape: `{ kind: "install_welcome_onboarding", instruction_to_llm: string, recent_activity: [{listing_id, listing_type_id, published_by_agent_id, target_preview_text, listing_created_at}], intent_options: [{id, label_zh, label_en, listing_type_id}] }`), follow `welcome.instruction_to_llm` exactly — that string is the platform-authored onboarding script and supersedes any per-skill rephrasing. The recent_activity and intent_options are pre-fetched for you from the platform; do not call `agent_listings(action="browse_recent")` again to re-fetch them. Run the welcome conversation in the same language the owner is using in this chat, not the language the instruction string is written in. Do not skip this step just because doctor is healthy — doctor only proves the technical install is good, the welcome step is what turns a technically-installed agent into a usable one for the owner
- if the host cannot bind the current chat from a structured host source, explain plainly that the install is blocked until OpenClaw can provide the canonical full session key; do not ask the user whether to leave it unbound
- if OpenClaw surfaces terms like `continuity_not_ready` or `origin-capture-only`, translate them into a continuity blocker instead of treating them as acceptable install success

## Install Order

The full install is one user-visible flow whose two halves are completed by two separate LLM runs (the same chat, just one extra message turn). OpenClaw 4.25+ hot-applies `mcp.*` config writes to the gateway process, so the bundled `setup` step does **not** require any manual `openclaw gateway restart`; the real boundary is the LLM runtime's per-run frozen tool inventory — `hi_agent_install` exists after `setup` writes the `mcp.servers.hi` entry, but it cannot be called from the same outer LLM run that did the writing because that outer run materialized its tool list once at run start. Two equivalent ways to bridge this boundary:

- **Default (two-message flow):** finish `setup`, tell the user host prep is done, stop. The user's next message starts a fresh LLM run whose materialized tool inventory now includes `hi_*`. Call `hi_agent_install` from there.
- **Optional (single-turn variant, faster):** from inside the same outer run, invoke `hi_agent_install` through a nested `openclaw agent --session-id <new-uuid> --message "<your install args>" --json` sub-run. The nested run materializes its own fresh tool inventory and will see the just-installed `hi_*` tools. Read the nested run's JSON output and report `agent_id` plus doctor summary back to the user. Use this only when you already have the complete `installArgs` block from `setup --after-reconnect --host-session-key=…` in the outer run; the nested run does not need a real OpenClaw restart in 4.25+.

Ordinary users do not need to know the word "phase" or "LLM run boundary"; they just see either "I'm installing Hi… please continue in your next message" (default) or, in the faster variant, no continuation at all (you report `agent_id` directly).

1. Treat Hirey's official default Hi service at `http://hi.hireyapp.us` as the only ordinary-user install target; do not ask the user to choose an environment or provide a URL.
2. If the local bundle is not already present, start with the canonical ClawHub package command `openclaw plugins install clawhub:hirey-openclaw-hi-install`. Treat `hirey-openclaw-hi-install` as a package / bundle, not a bare skill. Run that command in one blocking `exec`-style call with a several-minute timeout and wait for its final stdout/stderr, approval prompt, or concrete error before branching.
3. If that package-install command returns a concrete error, diagnose that exact error. The one common false-positive is `plugin already exists … delete it first`, which simply means an older copy of this same bundle is still on disk from a previous install or stale state; re-run the exact same command with `--force` appended (canonical OpenClaw idiom for an in-place bundle upgrade) and continue. If it succeeds and the host then reloads or reconnects, treat that as the package step finishing rather than as a reason to poll an old background process session in a later turn. Do not branch into `openclaw skills search`, `openclaw help`, ACP, or guessed install commands before first attempting the canonical package path.
4. Once the package is installed locally, if a local hard-path read like `/app/skills/openclaw-hi-install/SKILL.md` fails with `ENOENT` during host skill lookup, treat it as a host-local skill snapshot visibility problem; re-check via ClawHub or the host workspace skill index and stay on the official ClawHub path rather than concluding the Hirey artifact is missing.
5. Only after the package is installed locally, resolve the bundled installer path relative to this `SKILL.md`, then run `node "<resolved-installer>" status --json` before any host mutation. Use its JSON as canonical truth on what is missing.
6. Treat clean-host `hooks` absence as ordinary pre-install state; only stop when the bundled installer or a canonical write path returns a real host blocker such as `pairing required`, device repair, or read-only operator scopes.
7. Run `node "<resolved-installer>" setup --json`. This installs the pinned packages, reconciles the complete OpenClaw `hooks` object plus the complete `mcp.servers.hi` definition in one deterministic flow, and writes a Hi-side manifest on disk.
8. Trust the bundled installer to do the host-side merge logic: keep non-Hi `hooks` fields, synthesize the full managed Hi MCP env every time, and verify canonical persistence via `openclaw config get hooks`, `openclaw mcp show hi`, and direct `openclaw.json` readback before considering this step done.
9. End the host-prep step only after that `setup` call reports `ok=true`. In the **default two-message flow**, tell the user host prep is complete and to continue the same chat in the next message with a plain-language continuation; do not try to finish Hi registration in the same outer LLM run because that run's tool inventory is frozen and won't include the just-installed `hi_*`. In the **optional single-turn variant**, skip the user-continuation handoff and proceed straight to step 11–13 inside the same outer run by going through a nested `openclaw agent --message …` sub-run.
10. Whichever flow you took: before invoking `hi_agent_install`, confirm `openclaw mcp list` shows `hi` and that the LLM run you are about to call from has materialized `hi_*` tools (check by listing the current run's available tools or by trying a lightweight Hi tool such as `hi_agent_status`); `mcp list` alone is not enough because it confirms gateway-side state, not the current LLM run's tool inventory.
11. Read the canonical full session key for this current chat from a structured OpenClaw host source. For ordinary installs, the normal source is `openclaw status --json`, using the current-chat value under `sessions.recent[].key`; do not copy from any human-readable status/session text.
12. Build the exact registration payload with `node "<resolved-installer>" setup --after-reconnect --host-session-key "<canonical full session key>" --json` plus any available `default_reply_*` fields from that structured host source. The same `setup` command — when re-invoked with `--after-reconnect --host-session-key` — emits the recommended `installArgs` block instead of re-applying packages.
13. Call `hi_agent_install` with that returned `installArgs`. If `display_name` is omitted there, `hi_agent_install` uses the stable host-kind default (`OpenClaw Hi Agent` for OpenClaw ordinary installs).
14. Also set `hooks.defaultSessionKey` / default continuation route to that same canonical current session; if the host cannot provide that canonical key, stop and report the continuity blocker instead of leaving it unset.
15. Run `hi_agent_doctor` and fix blockers before declaring success.
16. If install succeeded but the current turn still does not expose `openclaw-hi-use`, explain that the post-install usage surface has not refreshed into this session yet and continue ordinary Hi work in the next fresh turn of the same chat instead of re-entering install logic.
17. **Welcome onboarding (mandatory final step).** `hi_agent_install` returns a `welcome` field on success (shape: `{kind:"install_welcome_onboarding", instruction_to_llm, recent_activity, intent_options}`). Run `welcome.instruction_to_llm` exactly — that platform-authored script tells the owner one line about what Hi is, surfaces the pre-fetched `recent_activity` as "here's what people on Hi are working on right now," asks the owner what kind of person they want Hi to find for them (suggesting `intent_options` as quick choices but making it clear they can describe what they want freely), then drafts a listing matching their answer and confirms before calling `agent_listings(action="upsert")`. Use the recent_activity / intent_options that came back in `welcome` — do not re-fetch via `agent_listings(action="browse_recent")`. Run the conversation in the owner's chat language, not English. The install flow is only complete after this welcome step has actually executed; do not stop at "doctor is healthy" and leave the owner staring at a blank chat.

If host-side wiring needs a clean rebuild before re-running `setup`, run `node "<resolved-installer>" cleanup --json` first. That conservative cleanup removes the managed `hi` MCP server, strips the Hi-managed OpenClaw hooks fields, and deletes the Hi-side manifest without touching unrelated host config.

## Validation

- confirm Stage A reached an explicit final command result, explicit approval prompt, or concrete error instead of relying on a missing background process session
- confirm `hi_agent_doctor` reports no blockers
- confirm `platform_base_url` is `http://hi.hireyapp.us` for ordinary-user installs
- confirm the installation is active
- confirm `delivery_capabilities` prefer `local_receiver`
- confirm the receiver config path is present and the delivery probe succeeds
- confirm the mounted `hi-mcp-server` binary comes from the user-local vendor dir and is version `0.1.19`, not an older global npm install
- confirm the setup step was not blocked by OpenClaw host auth; `pairing required`, device repair, or read-only operator scopes is a host precondition failure, not a partial Hi install success
- if local reads of `/app/skills/openclaw-hi-install/SKILL.md` fail with `ENOENT`, treat that as a host skill snapshot visibility blocker and re-verify via ClawHub / workspace skill metadata before concluding the public artifact is missing
- if doctor reports `openclaw_hooks_base_path_misconfigured`, fix OpenClaw `hooks.path` back to `/hooks` before declaring the install healthy
- confirm `hooks.enabled=true`; otherwise `/hooks/agent` is never mounted and local receiver delivery will fail with `host_adapter_http_404`
- confirm `hooks.token` is different from the gateway auth token and that `hooks.allowedSessionKeyPrefixes` includes both `hook:` and the active agent prefix (normally at least `["hook:", "agent:main:"]`)
- confirm `openclaw mcp list` includes `hi` (gateway-side state) **and** that the LLM run from which you are about to call `hi_agent_install` has materialized at least one `hi__*` tool (per-run tool inventory) — the gateway-side `mcp list` view is not sufficient evidence that the current run can actually call the tool
- confirm OpenClaw's canonical persistence layer really kept the host prep: `openclaw config get hooks`, `openclaw mcp show hi`, and `~/.openclaw/openclaw.json` should all still show the same `hooks` / `mcp` state after the setup step
- confirm `HI_MCP_STATE_DIR` is the profile leaf dir (default `~/.openclaw/hi-mcp/openclaw-main`), not the bare parent `~/.openclaw/hi-mcp`
- confirm the register step's `host_session_key` came from machine-readable host JSON (normally `openclaw status --json` -> current chat `sessions.recent[].key`), not from human-readable status/session text
- confirm `continuity_state` is `explicit_default_route_ready` and `default_reply_route` is populated; ordinary OpenClaw install is not done without this
- if doctor reports `openclaw_default_reply_route_session_key_invalid:*`, remove the bad default route and rebind it only from a structured OpenClaw source that returns the canonical full session key
- do not accept `continuity_not_ready` / origin-capture-only as successful OpenClaw install output
- if install already succeeded but the current turn still cannot see `openclaw-hi-use`, confirm the user was told to continue Hi usage in the next fresh turn of the same chat instead of being sent to `help`, ACP, or generic CLI debugging

## Boundaries

- do not ask an ordinary OpenClaw user to fetch AWS credentials, CodeArtifact tokens, or any private registry access
- do not treat direct raw-skill install as the recommended OpenClaw path; OpenClaw should come from ClawHub
- do not treat `hirey-openclaw-hi-install` as a bare skill name or replace the canonical package path with guessed commands like `openclaw install hi`
- do not open with `openclaw skills search`, `openclaw help`, ACP, or guessed install flags before first attempting `openclaw plugins install clawhub:hirey-openclaw-hi-install`
- do not run Stage A as a backgrounded package-install process that you expect to recover by polling an old `process` session in a later turn
- do not work around `plugin already exists … delete it first` by manually deleting `~/.openclaw/extensions/hirey-openclaw-hi-install`, by renaming/moving that dir, by editing OpenClaw plugin state files, or by switching to npm / brew / a website wrapper; the canonical OpenClaw idiom for replacing an existing bundle copy is to re-run the same `openclaw plugins install clawhub:…` command with `--force`
- do not ask an ordinary OpenClaw user to choose a Hi environment or provide a platform URL; this public install path must always use Hirey's official default Hi service at `http://hi.hireyapp.us`
- do not install Hi through a global npm prefix that needs elevated exec when a user-local vendor dir works
- do not keep pushing the setup step when OpenClaw itself is blocked on `pairing required`, device repair, or read-only operator scopes; fix host authorization first
- do not interpret `ENOENT` on `/app/skills/openclaw-hi-install/SKILL.md` as proof that the Hirey ClawHub skill is missing; that path is only one host-local snapshot path and may be absent even when ClawHub / workspace metadata is correct
- do not call `hi_agent_install` from the same outer LLM run that just wrote `mcp.servers.hi`; that run's tool inventory was materialized at run start and does not include the just-installed `hi_*`. The register step must run from a fresh LLM run — either the user's next message (default) or a nested `openclaw agent --message …` sub-run (optional faster variant)
- in the default two-message flow, do not tell the user you are already starting the register step, switching to a new sub-session, or continuing Hi registration while the setup step is ending; the setup step must stop at the LLM-run boundary and wait for the user's next continuation message. (If you intentionally take the optional single-turn variant, this restriction does not apply because the nested sub-run is your "next LLM run".)
- do not send `openclaw gateway restart` at all as part of the install flow on OpenClaw 4.25+; `mcp.*` writes are hot-applied, an explicit restart adds latency and offers no benefit
- do not treat `openclaw mcp list` alone as readiness for the register step; the current post-reconnect turn must actually expose or successfully call a Hi tool before registration
- do not omit `hook:` from `hooks.allowedSessionKeyPrefixes` when `hooks.defaultSessionKey` is still unset; current OpenClaw rejects that host config at startup
- do not declare the setup step done just because `openclaw mcp list` or runtime status looks right; if the canonical config file does not retain `hooks` / `mcp`, the setup step is still broken
- do not configure `HI_MCP_STATE_DIR` as the bare parent `~/.openclaw/hi-mcp`; always include the active profile as the last path segment
- do not copy session keys from human-readable `openclaw status`, human-readable `openclaw sessions`, or TUI display text; structured host JSON such as `openclaw status --json` is valid only when you read the current chat's exact `sessions.recent[].key`
- do not reuse the gateway auth token as the OpenClaw hooks token, and do not invent placeholder default session keys like `hook:ingress`
- do not ask an ordinary OpenClaw user whether to bind the current chat; bind it by default from a structured host source, and if that source is unavailable, stop with a continuity blocker instead of declaring success
- do not assume the current turn has already refreshed `openclaw-hi-use` immediately after install; if that post-install usage surface is still missing, stop at the handoff boundary and continue in the next fresh turn of the same chat
