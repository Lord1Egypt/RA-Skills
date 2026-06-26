---
name: hi-register
description: Register the Hi agent on this OpenClaw host AFTER the `clawhub:hirey` ClawPack plugin has been installed. Use whenever `hi_agent_install` is in your tool inventory but no Hi state exists yet (for example, the user just installed the plugin in the previous turn and is now sending the second message of the install flow), or whenever the user asks to "set up", "register", "complete the install of", "activate", or "connect" Hi. CRITICAL — `hi_agent_install` is the AGENT-side registration tool on the Hi platform; it is structurally different from `openclaw plugins install`, which is a system-side CLI that just lays the plugin on disk. Never confuse the two. Never report a fabricated `agent_id`.
---

# Hi Register (post-install)

This skill is the **second turn** of the Hi install flow on OpenClaw 5.2+ ClawPack. It loads automatically when the `clawhub:hirey` plugin is installed and the next outer LLM run starts.

## Use when

- the `clawhub:hirey` plugin is installed locally and `hi_agent_install` is in your current run's tool inventory
- the user is sending a fresh message after the plugin install ran in a previous turn (typical: the user said `continue` or anything else after being told "send another message to finish setup")
- OR: the user explicitly asks to register / set up / activate / connect Hi
- OR: a Hi tool returned an error like `hi_agent_state_missing` / `agent_not_registered`

## Do not use when

- the plugin is not installed yet (run `clawhub:hirey` install via the `openclaw-hi-install` skill first)
- the agent is already registered and `hi_agent_status` reports active

## Steps (turn 2 — registration)

1. Verify `hi_*` tools are in your current outer run's tool inventory before you call anything (try a lightweight call like `hi_agent_status`). If they are not, you are still in the same outer run as `openclaw plugins install` — your tool inventory was frozen before the plugin loaded; STOP and tell the user "send another message — OpenClaw doesn't refresh my tool list mid-turn." Do **not** fabricate `agent_id`.
2. Read the canonical full session key for the current chat from a structured host source: `openclaw status --json` → `sessions.recent[0].key`. Do not copy from human-readable status text (it can be truncated).
3. Call `hi_agent_install` with at minimum:
   - `host_session_key`: the session key from step 2
   - `default_reply_channel: "last"`
   - and if your structured host source provides them: `default_reply_to`, `default_reply_account_id`, `default_reply_thread_id`
   - `route_missing_policy: "use_explicit_default_route"` so Hi binds the current chat as the default reply target
4. Report the **real** values returned by the tool: `agent_id`, `hooks_ready`, `connected`, `activated`, `push_ready`. Never edit them. Never make them up.
5. Run `hi_agent_doctor` (with `probe_delivery: true` if you want a full end-to-end check) to verify; if it reports blockers, surface them honestly to the user.
6. If `hi_agent_install` returned a `welcome` field (shape: `{kind:"install_welcome_onboarding", instruction_to_llm, recent_activity, intent_options}`), follow `welcome.instruction_to_llm` exactly — it is the platform-authored onboarding script and supersedes any per-skill rephrasing. Use the `recent_activity` and `intent_options` that came back in `welcome` directly; do not call `agent_listings(action="browse_recent")` again to re-fetch them. Run the welcome conversation in the user's chat language.

## Anti-patterns

- ❌ Reporting `agent_id` you did not get back from `hi_agent_install`. `agent_id` looks like `ag_<12-hex>`; if you have not actually run the tool, the only correct answer is "I cannot register yet — please send another message."
- ❌ Pretending `hooks_ready=true` / `connected=true` / `activated=true` to make the install look one-shot. The user discovers the lie the first time they call any Hi tool.
- ❌ Calling `openclaw plugins install …` from this turn to "redo the install" — the plugin is already installed; you just need to call `hi_agent_install` (the AGENT-side registration tool, not the system-side CLI).
- ❌ Skipping the `welcome` onboarding when `hi_agent_install` returns one. Doctor being healthy is necessary but not sufficient — install is only "done for the user" after the welcome conversation has actually surfaced what Hi is and what they want it to find for them.

## Naming clarification (critical to avoid confusion)

There are two install-shaped commands in scope, and they are **not** the same thing:

| | `openclaw plugins install clawhub:hirey` | `hi_agent_install` (this tool) |
|---|---|---|
| Where it runs | OpenClaw CLI (system) | Hi platform (agent runtime) |
| What it does | Lands the plugin tarball on disk + registers it with the gateway | Registers an AGENT identity for this OpenClaw host on the Hi platform; sets up hooks for push delivery; activates installation; subscribes to event topics |
| When | Stage A (turn 1) | Stage B (turn 2) |
| Required tool inventory | available in any LLM run | only in LLM runs whose inventory was materialized AFTER the plugin loaded |
| Sufficient to use Hi? | NO — you have tools but no agent identity | YES — after this returns successfully, hi_* tools work |

If only the system-side install ran, the user has a non-functional plugin: the tools surface but every call fails because there is no agent identity bound to this host. `hi_agent_install` is the step that makes Hi actually work.
