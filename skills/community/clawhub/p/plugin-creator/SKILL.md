---
name: plugin-creator
description: Build, review, and debug OpenClaw plugins with the official plugin SDK. Use when creating or modifying `extensions/<id>` plugins, `openclaw.plugin.json`, plugin-shipped skills, tools, hooks, slash commands, manifests, or tests, and when diagnosing why a plugin, hook, skill, command, or tool is loaded but unavailable at runtime.
---

# Plugin Creator

Use this skill to build or debug OpenClaw plugins. Prefer the official SDK surface, official documentation, and existing plugin patterns over generic plugin assumptions.

## Why plugins exist

Plugins exist to extend OpenClaw **without forking the host**.

That matters because most user needs are not “change everything.” They are usually one of these:

- teach the agent a new capability
- let the user trigger a deterministic shortcut
- react to an event in the runtime
- package repeatable domain knowledge

The philosophical goal is not to put all custom logic into one plugin. The goal is to place each behavior at the **smallest correct boundary** so it stays understandable, testable, and portable.

When deciding what to build, start from the user need, not from the mechanism. Ask:

- What exact problem is the user trying to solve?
- Who should initiate the behavior: the user, the agent, or the runtime?
- Does the behavior need judgment, determinism, or passive observation?
- What is the smallest unit that solves the need cleanly?

If you answer those questions first, the plugin shape usually becomes obvious.

## Mental model: hook vs tool vs command vs skill

These are different layers. Do not collapse them into “plugin stuff.”

### Hooks — react to runtime events

Use a hook when the behavior should happen **because something else happened**.

- Mental model: an interception point or observer in the runtime lifecycle
- Good for: auditing, rewriting, guardrails, telemetry, prompt shaping, policy enforcement
- Ask for a hook when the real question is: “When X happens, should I observe it, modify it, or block it?”

### Tools — give the agent a capability

Use a tool when the agent needs to **do something** during reasoning.

- Mental model: a callable capability inside the agent's toolbox
- Good for: API calls, deterministic computations, external actions, structured lookups
- Ask for a tool when the real question is: “Should the model be able to choose this action mid-run?”

### Slash commands / native commands — give the user a deterministic shortcut

Use a command when the user should be able to **explicitly trigger** a behavior without relying on model judgment.

- Mental model: a direct entrypoint, not an AI-selected capability
- Good for: status, toggles, admin actions, explicit workflows, manual overrides
- Ask for a command when the real question is: “Should the user be able to force this immediately?”

### Skills — package reusable knowledge and workflow

Use a skill when the problem is not “run this one function,” but “help the model reason in a repeatable way.”

- Mental model: a reusable playbook for judgment, workflow, and domain knowledge
- Good for: domain-specific analysis, multi-step procedures, standard operating methods, decomposition guidance
- Ask for a skill when the real question is: “Does the model need better thinking structure, not just a new API?”

### Practical decision rule

- If the user explicitly triggers it, start by considering a **command**.
- If the model should choose it during reasoning, start by considering a **tool**.
- If it should happen because the runtime reached a lifecycle point, start by considering a **hook**.
- If the main value is judgment, reusable reasoning, or process guidance, start by considering a **skill**.

Many good plugins combine more than one layer. The mistake is not combining them. The mistake is combining them **without separating responsibilities**.

## Decomposing user needs

When a user says “I want a plugin that does X,” do not immediately design files. Decompose the request.

### Step 1: find the real trigger

- User-triggered → likely command
- Agent-triggered → likely tool
- Event-triggered → likely hook
- Knowledge/workflow-triggered → likely skill

### Step 2: split the request by responsibility

Most plugin requests contain multiple concerns mixed together:

- invocation: how behavior starts
- decision logic: how behavior decides what to do
- side effects: what external action happens
- state: what must be remembered
- visibility: what the user should see

Split those concerns before coding. A clean plugin often looks like:

1. a thin registration layer in `index.ts`
2. small implementation modules per responsibility
3. tests that validate each boundary separately

### Step 3: choose the smallest correct unit

Prefer:

- one command per clear user intent
- one tool per clear capability
- one hook per lifecycle concern
- one skill per coherent reasoning workflow

Avoid “mega plugins” that mix unrelated behavior just because the code lives in one package.

### Step 4: verify all four layers

Every plugin feature should be checked at four layers:

1. **Manifest** — is the plugin declared correctly?
2. **Registration** — does the plugin actually register the command/tool/hook/skill?
3. **Runtime** — can the runtime reach and execute it?
4. **Surface** — can the user actually observe or trigger it where expected?

This prevents a common failure mode: “the code exists, therefore the feature works.”

## Evidence priority

When something is unclear, use this priority order:

1. Public behavior explicitly promised in official docs.
2. Published SDK types, manifest/schema references, and other stable plugin-facing contracts that do not require a full local source checkout.
3. Existing plugin patterns in the OpenClaw repo when the repo source is available, for example `extensions/observability-lab/`.
4. Project-specific operational experience and known pitfalls.

If layers 3 or 4 conflict with layers 1 or 2, trust layers 1 and 2. Also separate “current repo implementation observations” from “stable public contract” in your write-up.

## What to do first

1. Classify the task first.
   - If you are creating or refactoring plugin structure, read `references/plugin-layout-and-registration.md` first.
   - If you are working on hooks or event observation, read `references/hooks-and-events.md` first.
   - If the issue is “the plugin seems registered but does not work at runtime”, read `references/pitfalls-and-debugging.md` first.
   - If you are adding tests, validating packaging, or tightening the dev workflow, read `references/testing-and-workflow.md` first.
   - If you are not sure which official source to trust first, read `references/official-docs.md` first.

2. Confirm the plugin boundary before writing code.
   - Decide whether this plugin is a tool, hook, command, skill, service, channel, provider, or a combination.
   - Then split the problem into four layers:
     - whether the manifest declares it
     - whether registration actually happens
     - whether runtime agent / gateway flows can really use it
     - whether the relevant surface actually displays or exposes it
   - Start with the smallest verifiable slice. Do not pile on multiple capabilities at once.

3. Prefer an existing pattern before inventing one.
   - `extensions/observability-lab/`: best for learning combined tool, typed hook, plugin skill, and slash-command patterns.
   - `extensions/open-prose/`: useful for learning plugin-shipped skill packaging.
   - `extensions/lobster/` and `extensions/llm-task/`: useful for optional tools via `optional: true`.

## Workflow

1. Choose the location and shape first.
   - When developing inside the OpenClaw repo, prefer `extensions/<plugin-id>/`.
   - When developing outside the repo, keep the same directory shape and SDK import discipline.

2. Build the smallest valid skeleton first.
   - At minimum, create `package.json`, `openclaw.plugin.json`, and `index.ts`.
   - If plugin code frequently references SDK types, add a local `api.ts` barrel.
   - If the plugin grows beyond a tiny surface, split command / hook / tool / skill / shared state into separate modules.

3. Add capabilities after the boundary is clear.
   - tools use `api.registerTool(...)`
   - commands use `api.registerCommand(...)`
   - typed hooks use `api.on(...)`
   - lower-level or more generic hook work should consult `api.registerHook(...)`
   - plugin-shipped skills are declared via the `skills` field in `openclaw.plugin.json`

4. Pass the pre-install validation gate before any install step.
   - Run the most direct scoped test first: `pnpm test -- extensions/<plugin-id>/` or `pnpm test -- extensions/<plugin-id>/index.test.ts`
   - When developing inside the OpenClaw repo, run at least one `pnpm build`
   - If the touched surface extends beyond the local plugin, add `pnpm check` and the appropriate broader `pnpm test`
   - Only after those pass may you proceed to `pnpm openclaw plugins inspect <id>`, install, restart, and real-surface verification

5. Then do post-install and runtime verification.
   - `pnpm openclaw plugins inspect <id>`
   - install / restart / real conversation-surface verification
   - read session logs or `systemPromptReport` when needed

6. Any new deliverable package must get a new version.
   - Update the plugin `package.json` version before repackaging.
   - Every new remote handoff or installable iteration needs a fresh patch version.
   - Always give the remote operator the latest tgz filename, the exact version, and an optional checksum. Do not say “install the package in dist” without naming the file.

## Pre-install validation

If the task includes “hand this to someone to install”, “ship to a remote environment”, “build a tgz”, or “prepare install instructions”, pre-install validation is mandatory. Do not treat `openclaw plugins install ...` as the first validation step.

Minimum gate for in-repo plugin development:

1. scoped tests pass
2. `pnpm build` passes
3. the target runtime version is known before compatibility and packaging claims are made

Recommended order:

```bash
pnpm test -- extensions/<plugin-id>/index.test.ts
pnpm build
pnpm check
pnpm openclaw plugins inspect <plugin-id> --json
```

Execution rules:

- `pnpm check` is not always required for the smallest isolated plugin-local change, but once the touched surface crosses plugin-local boundaries, do not skip it.
- Put `plugins inspect` before install so you can confirm manifest / registration / diagnostics before debugging a failed install.
- If you are handing off a package, run `npm pack --pack-destination dist`, then provide the exact latest `dist/<package>-<version>.tgz` filename, version, and checksum.
- If the target environment is not the current runtime, explicitly verify the target OpenClaw version. Since `2026.3.23`, plugin compatibility is resolved against the active runtime version during install, so do not rely on stale constants.
- For correction releases such as `2026.3.23-2`, do not reuse an older tgz. Repack and hand off the new deliverable version explicitly.

## Non-negotiable constraints

- Import production plugin code only from `openclaw/plugin-sdk/<subpath>` official surfaces; do not import core `src/**` paths directly.
- `openclaw.plugin.json` must exist, and `configSchema` must stay strict.
- Skill YAML frontmatter is only for skill metadata; it does not attach tools to the agent.
- A plugin tool being “registered” does not mean it is automatically usable by the current agent; tool policy may still filter it.
- Every conclusion must carry enough local context to stand on its own; do not rely on unstated prior conversation context.
- Keep wording objective; avoid subjective phrasing.
- For any tool-related design, explicitly describe tool availability, triggerability, and determinism limits.
- `api.registerCommand(...)`, plugin-shipped skills, skill commands, `command-dispatch: tool`, and native command menu visibility are different mechanisms; do not blur them together.
- Prefer `before_model_resolve` / `before_prompt_build` for prompt injection; treat `before_agent_start` as a compatibility path only.
- If the plugin needs runtime help, prefer `api.runtime.*` instead of bypassing the SDK into host internals.
- If a plugin is being handed off for remote installation, the deliverable must be the newest tgz with the new version; do not present an older package path, filename, or hash as current.
- Install is not the start of validation; if the pre-install gate is not green, do not ask anyone to run `openclaw plugins install ...`.
- Before handoff, say which step validates manifest, registration, runtime, and surface discoverability. Do not collapse those layers into a vague “already tested”.

## Handling abnormal cases

Plugins fail in predictable ways. Treat failure handling as part of the design, not as a cleanup step.

### When behavior is ambiguous

- If the same user need could be solved by a hook, a tool, or a command, do not guess.
- Explain the tradeoff in plain language:
  - command = deterministic and user-controlled
  - tool = agent-controlled and flexible
  - hook = passive or interceptive runtime behavior
- Pick the smallest mechanism that preserves the intended user experience.

### When config or environment is missing

- Fail clearly, not silently.
- Return actionable errors that say what is missing and where it should be configured.
- Distinguish “plugin loaded” from “plugin usable” — many runtime failures are configuration failures, not registration failures.

### When external dependencies fail

- Prefer narrow failures over global breakage.
- Let one failing API call or optional integration degrade one capability, not crash the whole plugin.
- If a capability is optional, model that explicitly in command output, tool errors, or docs.

### When state can drift or disappear

- Assume in-memory state is temporary.
- If state must survive restart, make persistence explicit.
- Validate restored state before trusting it.
- Design for recovery, not just the happy path.

### When debugging unexpected behavior

Use this order:

1. confirm the plugin is loadable
2. confirm the target capability is registered
3. confirm the runtime path can actually reach it
4. confirm the user-facing surface exposes it as expected
5. only then treat it as a deeper logic bug

This order matters because many “logic bugs” are actually loading, policy, or surface-discovery problems.

## Design philosophy for users

The job is not just to expose SDK features. The job is to help the user get the behavior they actually want.

That means you should be able to explain, in simple language:

- why this behavior belongs in a hook, tool, command, or skill
- why it is split into these pieces and not fewer or more
- what happens on the happy path
- what happens on the failure path
- what the user can rely on, and what remains probabilistic or policy-gated

If you cannot explain the design simply, the design is probably still too tangled.

## Delivery standard

When plugin development or debugging is complete, the output should cover at least:

- plugin shape and directory structure
- key registration points
- which official docs or source entrypoints were used
- which validations were run
- which conclusions belong to manifest / registration / runtime / surface discoverability
- whether any residual risk remains around tool policy, hook semantics, config schema, or installation flow

## References

- Layout and registration: `references/plugin-layout-and-registration.md`
- Hooks and events: `references/hooks-and-events.md`
- Testing and dev workflow: `references/testing-and-workflow.md`
- Pitfalls and debugging: `references/pitfalls-and-debugging.md`
- Official docs entrypoints: `references/official-docs.md`
- In-repo example map: `references/example-map.md`
