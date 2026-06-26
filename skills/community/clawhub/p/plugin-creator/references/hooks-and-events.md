# Hooks and Event Types

This reference focuses on three questions:

1. Which hooks can return values.
2. Why those return values matter.
3. Where session state should live.

For exact field names and return types, treat `src/plugins/types.ts` as authoritative when a local repo checkout is available. Use `docs/automation/hooks.md` as the semantic guide.

## Core hook return-value matrix

| Hook | Returns values? | Typical return data | Why it matters |
| --- | --- | --- | --- |
| `before_model_resolve` | Yes | `providerOverride` / `modelOverride` | Change provider or model before a run starts. |
| `before_prompt_build` | Yes | `systemPrompt`, `prependContext`, `prependSystemContext`, `appendSystemContext` | Inject or rewrite prompt structure. |
| `inbound_claim` | Yes | `handled` | Claim an inbound message and stop the default handling path. |
| `message_sending` | Yes | `content` / `cancel` | Rewrite or cancel outbound text. |
| `before_tool_call` | Yes | `params`, `block`, `blockReason` | Modify tool params or block the tool call. |
| `tool_result_persist` | Yes (sync) | `message` | Rewrite the tool-result transcript before it is written. |
| `before_message_write` | Yes (sync) | `message` / `block` | Rewrite or block any message before transcript persistence. |
| `subagent_spawning` | Yes | `deliver`, `provider`, `model`, `message`, `metadata`, etc. | Rewrite policy before a subagent is created. |
| `subagent_delivery_target` | Yes | `targetSessionKey` | Change where subagent results are delivered. |

These hooks do not usually return business data; they are mainly for observation:

- `message_received`
- `message_sent`
- `llm_input`
- `llm_output`
- `after_tool_call`
- `session_start`
- `session_end`
- `before_reset`
- `agent_end`

## Why return values matter, by impact layer

### 1. Runtime decision layer

- `before_model_resolve`
- `before_prompt_build`

Value:

- Centralize model-routing and prompt-shaping strategy in the plugin layer.
- Let you implement model routing, prompt injection, and cache-friendly context assembly without rewriting business code.

### 2. Routing and sending layer

- `inbound_claim`
- `message_sending`

Value:

- Claim or rewrite message flow for routing rules, branding prefixes, or channel-level interception.
- `message_sending` is closer to true outbound behavior; `before_message_write` is not an outbound hook.

### 3. Tool-governance layer

- `before_tool_call`
- `tool_result_persist`

Value:

- Govern calls before execution: parameter correction, safety blocks, audit markers.
- Govern persistence before write: redaction, truncation, noise reduction.

### 4. Session-persistence layer

- `before_message_write`

Value:

- Final synchronous control point before transcript persistence.
- Useful for protecting sensitive data or filtering noise before it lands in history.

## Where session state can live

Common choices:

### 1. Process memory (recommended default)

Pattern:

- Keep `Map<sessionId, SessionState>` in the plugin module
- Initialize on `session_start`; clean up on `session_end` or `before_reset`

Pros:

- Fast and simple
- Great for short-lived session flags

Limits:

- Lost on process restart
- Only valid inside the current gateway process

### 2. Session storage or plugin files (when persistence matters)

Pattern:

- Use `api.runtime.agent.session.*` helpers when appropriate
- Write state to session-related files or plugin-owned persistent files

Pros:

- Survives restart
- Good for audit trails or long-lived state

Limits:

- You must handle concurrency and I/O cost
- Bad design here can slow hot paths

### 3. External storage (multi-node or multi-instance)

Pattern:

- Write asynchronously to a remote database or event system

Pros:

- Works across instances
- Strongest observability story

Limits:

- Higher network, reliability, and security complexity

## Recommended session-activation pattern

Goal: start recording only after the plugin is actually used in the current session.

Recommended approach:

1. Use `sessionId` as the primary state key.
2. Activate state only when the plugin is truly used, for example when:
   - a plugin command is invoked
   - a plugin skill command is invoked
   - a plugin tool is called
3. After activation, record the events you need, such as:
   - `message_received`
   - `llm_input`
   - `llm_output`
   - `before_tool_call`
   - `after_tool_call`
   - optionally `message_sending` and `message_sent`
4. Clean up on `session_end` or `before_reset`.

## Tool limitations you should state explicitly

### 1. Registered does not mean usable

- A tool may still be filtered by `tools.profile`, `tools.allow`, `tools.deny`, or `tools.alsoAllow`.
- Validate runtime tool availability, not just `plugins inspect` output.

### 2. Tools do not execute themselves

- Tools must be called by the agent or reached through deterministic command dispatch.
- Defining a tool does not guarantee the model will choose it.

### 3. Model-driven paths are nondeterministic

- A skill-guided tool call is still a model decision.
- If you need determinism, prefer `command-dispatch: tool` or `api.registerCommand(...)`.

### 4. Synchronous hooks are not for heavy I/O

- `tool_result_persist` and `before_message_write` are synchronous rewrite points.
- Prefer async queues or fire-and-forget append behavior for heavy observability work.

### 5. Menu visibility is not the same as executability

- Whether a command appears in a menu depends on the surface and `commands.native` / `commands.nativeSkills`.
- The real execution check is whether the command can be sent and run successfully.

## Common semantic traps

### Trap 1: treating `message_received` as outbound

`message_received` is inbound: user/channel → OpenClaw.

### Trap 2: treating `before_message_write` as the universal outbound pre-send hook

It runs before transcript persistence. It does not guarantee control over the final outbound text sent on every channel.

### Trap 3: misreading where skill-command rewrite happens

For non-`command-dispatch: tool` skills, the host core rewrites the skill command into a skill-guided request. That rewrite is not implemented by a plugin hook. See `src/auto-reply/reply/get-reply-inline-actions.ts`.

## Debugging order

1. Confirm the hook name and return structure against `src/plugins/types.ts`.
2. Confirm the plugin is loaded and the hook is registered with `openclaw plugins inspect <id>`.
3. Confirm the current surface actually exercises that hook path.
4. Cross-check session logs and plugin telemetry.
5. If tools or skills are involved, also inspect tool policy, session snapshot behavior, and command visibility config.
