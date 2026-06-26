# Reference

> This file contains verbatim documentation from docs.openclaw.ai
> Total pages in this section: 15

---

<!-- SOURCE: https://docs.openclaw.ai/reference/credits -->

# Credits - OpenClaw

## The name

OpenClaw = CLAW + TARDIS, because every space lobster needs a time and space machine.

*   **Peter Steinberger** ([@steipete](https://x.com/steipete)) - Creator, lobster whisperer
*   **Mario Zechner** ([@badlogicc](https://x.com/badlogicgames)) - Pi creator, security pen tester
*   **Clawd** - The space lobster who demanded a better name

## Core contributors

*   **Maxim Vovshin** (@Hyaxia, [36747317+Hyaxia@users.noreply.github.com](mailto:36747317+Hyaxia@users.noreply.github.com)) - Blogwatcher skill
*   **Nacho Iacovino** (@nachoiacovino, [nacho.iacovino@gmail.com](mailto:nacho.iacovino@gmail.com)) - Location parsing (Telegram and WhatsApp)
*   **Vincent Koc** ([@vincentkoc](https://github.com/vincentkoc), [@vincent\_koc](https://x.com/vincent_koc)) - Agents, Telemetry, Hooks, Security

## License

MIT - Free as a lobster in the ocean.

> “We are all just playing with our own prompts.” (An AI, probably high on tokens)

---

<!-- SOURCE: https://docs.openclaw.ai/pi-dev -->

# Pi Development Workflow - OpenClaw

This guide summarizes a sane workflow for working on the pi integration in OpenClaw.

## Type Checking and Linting

*   Type check and build: `pnpm build`
*   Lint: `pnpm lint`
*   Format check: `pnpm format`
*   Full gate before pushing: `pnpm lint && pnpm build && pnpm test`

## Running Pi Tests

Run the Pi-focused test set directly with Vitest:

```
pnpm test -- \
  "src/agents/pi-*.test.ts" \
  "src/agents/pi-embedded-*.test.ts" \
  "src/agents/pi-tools*.test.ts" \
  "src/agents/pi-settings.test.ts" \
  "src/agents/pi-tool-definition-adapter*.test.ts" \
  "src/agents/pi-extensions/**/*.test.ts"
```

To include the live provider exercise:

```
OPENCLAW_LIVE_TEST=1 pnpm test -- src/agents/pi-embedded-runner-extraparams.live.test.ts
```

This covers the main Pi unit suites:

*   `src/agents/pi-*.test.ts`
*   `src/agents/pi-embedded-*.test.ts`
*   `src/agents/pi-tools*.test.ts`
*   `src/agents/pi-settings.test.ts`
*   `src/agents/pi-tool-definition-adapter.test.ts`
*   `src/agents/pi-extensions/*.test.ts`

## Manual Testing

Recommended flow:

*   Run the gateway in dev mode:
    *   `pnpm gateway:dev`
*   Trigger the agent directly:
    *   `pnpm openclaw agent --message "Hello" --thinking low`
*   Use the TUI for interactive debugging:
    *   `pnpm tui`

For tool call behavior, prompt for a `read` or `exec` action so you can see tool streaming and payload handling.

## Clean Slate Reset

State lives under the OpenClaw state directory. Default is `~/.openclaw`. If `OPENCLAW_STATE_DIR` is set, use that directory instead. To reset everything:

*   `openclaw.json` for config
*   `credentials/` for auth profiles and tokens
*   `agents/<agentId>/sessions/` for agent session history
*   `agents/<agentId>/sessions.json` for the session index
*   `sessions/` if legacy paths exist
*   `workspace/` if you want a blank workspace

If you only want to reset sessions, delete `agents/<agentId>/sessions/` and `agents/<agentId>/sessions.json` for that agent. Keep `credentials/` if you do not want to reauthenticate.

## References

*   [https://docs.openclaw.ai/testing](https://docs.openclaw.ai/testing)
*   [https://docs.openclaw.ai/start/getting-started](https://docs.openclaw.ai/start/getting-started)

---

<!-- SOURCE: https://docs.openclaw.ai/reference/wizard -->

# Onboarding Wizard Reference - OpenClaw

This is the full reference for the `openclaw onboard` CLI wizard. For a high-level overview, see [Onboarding Wizard](https://docs.openclaw.ai/start/wizard).

## Flow details (local mode)

## Non-interactive mode

Use `--non-interactive` to automate or script onboarding:

```
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice apiKey \
  --anthropic-api-key "$ANTHROPIC_API_KEY" \
  --gateway-port 18789 \
  --gateway-bind loopback \
  --install-daemon \
  --daemon-runtime node \
  --skip-skills
```

Add `--json` for a machine‑readable summary. Gateway token SecretRef in non-interactive mode:

```
export OPENCLAW_GATEWAY_TOKEN="your-token"
openclaw onboard --non-interactive \
  --mode local \
  --auth-choice skip \
  --gateway-auth token \
  --gateway-token-ref-env OPENCLAW_GATEWAY_TOKEN
```

`--gateway-token` and `--gateway-token-ref-env` are mutually exclusive.

### Add agent (non-interactive)

```
openclaw agents add work \
  --workspace ~/.openclaw/workspace-work \
  --model openai/gpt-5.2 \
  --bind whatsapp:biz \
  --non-interactive \
  --json
```

## Gateway wizard RPC

The Gateway exposes the wizard flow over RPC (`wizard.start`, `wizard.next`, `wizard.cancel`, `wizard.status`). Clients (macOS app, Control UI) can render steps without re‑implementing onboarding logic.

## Signal setup (signal-cli)

The wizard can install `signal-cli` from GitHub releases:

*   Downloads the appropriate release asset.
*   Stores it under `~/.openclaw/tools/signal-cli/<version>/`.
*   Writes `channels.signal.cliPath` to your config.

Notes:

*   JVM builds require **Java 21**.
*   Native builds are used when available.
*   Windows uses WSL2; signal-cli install follows the Linux flow inside WSL.

## What the wizard writes

Typical fields in `~/.openclaw/openclaw.json`:

*   `agents.defaults.workspace`
*   `agents.defaults.model` / `models.providers` (if Minimax chosen)
*   `tools.profile` (local onboarding defaults to `"coding"` when unset; existing explicit values are preserved)
*   `gateway.*` (mode, bind, auth, tailscale)
*   `session.dmScope` (behavior details: [CLI Onboarding Reference](https://docs.openclaw.ai/start/wizard-cli-reference#outputs-and-internals))
*   `channels.telegram.botToken`, `channels.discord.token`, `channels.signal.*`, `channels.imessage.*`
*   Channel allowlists (Slack/Discord/Matrix/Microsoft Teams) when you opt in during the prompts (names resolve to IDs when possible).
*   `skills.install.nodeManager`
*   `wizard.lastRunAt`
*   `wizard.lastRunVersion`
*   `wizard.lastRunCommit`
*   `wizard.lastRunCommand`
*   `wizard.lastRunMode`

`openclaw agents add` writes `agents.list[]` and optional `bindings`. WhatsApp credentials go under `~/.openclaw/credentials/whatsapp/<accountId>/`. Sessions are stored under `~/.openclaw/agents/<agentId>/sessions/`. Some channels are delivered as plugins. When you pick one during onboarding, the wizard will prompt to install it (npm or a local path) before it can be configured.

*   Wizard overview: [Onboarding Wizard](https://docs.openclaw.ai/start/wizard)
*   macOS app onboarding: [Onboarding](https://docs.openclaw.ai/start/onboarding)
*   Config reference: [Gateway configuration](https://docs.openclaw.ai/gateway/configuration)
*   Providers: [WhatsApp](https://docs.openclaw.ai/channels/whatsapp), [Telegram](https://docs.openclaw.ai/channels/telegram), [Discord](https://docs.openclaw.ai/channels/discord), [Google Chat](https://docs.openclaw.ai/channels/googlechat), [Signal](https://docs.openclaw.ai/channels/signal), [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles) (iMessage), [iMessage](https://docs.openclaw.ai/channels/imessage) (legacy)
*   Skills: [Skills](https://docs.openclaw.ai/tools/skills), [Skills config](https://docs.openclaw.ai/tools/skills-config)

---

<!-- SOURCE: https://docs.openclaw.ai/reference/token-use -->

# Token Use and Costs - OpenClaw

OpenClaw tracks **tokens**, not characters. Tokens are model-specific, but most OpenAI-style models average ~4 characters per token for English text.

## How the system prompt is built

OpenClaw assembles its own system prompt on every run. It includes:

*   Tool list + short descriptions
*   Skills list (only metadata; instructions are loaded on demand with `read`)
*   Self-update instructions
*   Workspace + bootstrap files (`AGENTS.md`, `SOUL.md`, `TOOLS.md`, `IDENTITY.md`, `USER.md`, `HEARTBEAT.md`, `BOOTSTRAP.md` when new, plus `MEMORY.md` and/or `memory.md` when present). Large files are truncated by `agents.defaults.bootstrapMaxChars` (default: 20000), and total bootstrap injection is capped by `agents.defaults.bootstrapTotalMaxChars` (default: 150000). `memory/*.md` files are on-demand via memory tools and are not auto-injected.
*   Time (UTC + user timezone)
*   Reply tags + heartbeat behavior
*   Runtime metadata (host/OS/model/thinking)

See the full breakdown in [System Prompt](https://docs.openclaw.ai/concepts/system-prompt).

## What counts in the context window

Everything the model receives counts toward the context limit:

*   System prompt (all sections listed above)
*   Conversation history (user + assistant messages)
*   Tool calls and tool results
*   Attachments/transcripts (images, audio, files)
*   Compaction summaries and pruning artifacts
*   Provider wrappers or safety headers (not visible, but still counted)

For images, OpenClaw downscales transcript/tool image payloads before provider calls. Use `agents.defaults.imageMaxDimensionPx` (default: `1200`) to tune this:

*   Lower values usually reduce vision-token usage and payload size.
*   Higher values preserve more visual detail for OCR/UI-heavy screenshots.

For a practical breakdown (per injected file, tools, skills, and system prompt size), use `/context list` or `/context detail`. See [Context](https://docs.openclaw.ai/concepts/context).

## How to see current token usage

Use these in chat:

*   `/status` → **emoji‑rich status card** with the session model, context usage, last response input/output tokens, and **estimated cost** (API key only).
*   `/usage off|tokens|full` → appends a **per-response usage footer** to every reply.
    *   Persists per session (stored as `responseUsage`).
    *   OAuth auth **hides cost** (tokens only).
*   `/usage cost` → shows a local cost summary from OpenClaw session logs.

Other surfaces:

*   **TUI/Web TUI:** `/status` + `/usage` are supported.
*   **CLI:** `openclaw status --usage` and `openclaw channels list` show provider quota windows (not per-response costs).

## Cost estimation (when shown)

Costs are estimated from your model pricing config:

```
models.providers.<provider>.models[].cost
```

These are **USD per 1M tokens** for `input`, `output`, `cacheRead`, and `cacheWrite`. If pricing is missing, OpenClaw shows tokens only. OAuth tokens never show dollar cost.

## Cache TTL and pruning impact

Provider prompt caching only applies within the cache TTL window. OpenClaw can optionally run **cache-ttl pruning**: it prunes the session once the cache TTL has expired, then resets the cache window so subsequent requests can re-use the freshly cached context instead of re-caching the full history. This keeps cache write costs lower when a session goes idle past the TTL. Configure it in [Gateway configuration](https://docs.openclaw.ai/gateway/configuration) and see the behavior details in [Session pruning](https://docs.openclaw.ai/concepts/session-pruning). Heartbeat can keep the cache **warm** across idle gaps. If your model cache TTL is `1h`, setting the heartbeat interval just under that (e.g., `55m`) can avoid re-caching the full prompt, reducing cache write costs. In multi-agent setups, you can keep one shared model config and tune cache behavior per agent with `agents.list[].params.cacheRetention`. For a full knob-by-knob guide, see [Prompt Caching](https://docs.openclaw.ai/reference/prompt-caching). For Anthropic API pricing, cache reads are significantly cheaper than input tokens, while cache writes are billed at a higher multiplier. See Anthropic’s prompt caching pricing for the latest rates and TTL multipliers: [https://docs.anthropic.com/docs/build-with-claude/prompt-caching](https://docs.anthropic.com/docs/build-with-claude/prompt-caching)

### Example: keep 1h cache warm with heartbeat

```
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long"
    heartbeat:
      every: "55m"
```

### Example: mixed traffic with per-agent cache strategy

```
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long" # default baseline for most agents
  list:
    - id: "research"
      default: true
      heartbeat:
        every: "55m" # keep long cache warm for deep sessions
    - id: "alerts"
      params:
        cacheRetention: "none" # avoid cache writes for bursty notifications
```

`agents.list[].params` merges on top of the selected model’s `params`, so you can override only `cacheRetention` and inherit other model defaults unchanged.

Anthropic’s 1M context window is currently beta-gated. OpenClaw can inject the required `anthropic-beta` value when you enable `context1m` on supported Opus or Sonnet models.

```
agents:
  defaults:
    models:
      "anthropic/claude-opus-4-6":
        params:
          context1m: true
```

This maps to Anthropic’s `context-1m-2025-08-07` beta header. This only applies when `context1m: true` is set on that model entry. Requirement: the credential must be eligible for long-context usage (API key billing, or subscription with Extra Usage enabled). If not, Anthropic responds with `HTTP 429: rate_limit_error: Extra usage is required for long context requests`. If you authenticate Anthropic with OAuth/subscription tokens (`sk-ant-oat-*`), OpenClaw skips the `context-1m-*` beta header because Anthropic currently rejects that combination with HTTP 401.

## Tips for reducing token pressure

*   Use `/compact` to summarize long sessions.
*   Trim large tool outputs in your workflows.
*   Lower `agents.defaults.imageMaxDimensionPx` for screenshot-heavy sessions.
*   Keep skill descriptions short (skill list is injected into the prompt).
*   Prefer smaller models for verbose, exploratory work.

See [Skills](https://docs.openclaw.ai/tools/skills) for the exact skill list overhead formula.

---

<!-- SOURCE: https://docs.openclaw.ai/reference/secretref-credential-surface -->

# SecretRef Credential Surface - OpenClaw

This page defines the canonical SecretRef credential surface. Scope intent:

*   In scope: strictly user-supplied credentials that OpenClaw does not mint or rotate.
*   Out of scope: runtime-minted or rotating credentials, OAuth refresh material, and session-like artifacts.

## Supported credentials

### `openclaw.json` targets (`secrets configure` + `secrets apply` + `secrets audit`)

*   `models.providers.*.apiKey`
*   `models.providers.*.headers.*`
*   `skills.entries.*.apiKey`
*   `agents.defaults.memorySearch.remote.apiKey`
*   `agents.list[].memorySearch.remote.apiKey`
*   `talk.apiKey`
*   `talk.providers.*.apiKey`
*   `messages.tts.elevenlabs.apiKey`
*   `messages.tts.openai.apiKey`
*   `tools.web.search.apiKey`
*   `tools.web.search.gemini.apiKey`
*   `tools.web.search.grok.apiKey`
*   `tools.web.search.kimi.apiKey`
*   `tools.web.search.perplexity.apiKey`
*   `gateway.auth.password`
*   `gateway.auth.token`
*   `gateway.remote.token`
*   `gateway.remote.password`
*   `cron.webhookToken`
*   `channels.telegram.botToken`
*   `channels.telegram.webhookSecret`
*   `channels.telegram.accounts.*.botToken`
*   `channels.telegram.accounts.*.webhookSecret`
*   `channels.slack.botToken`
*   `channels.slack.appToken`
*   `channels.slack.userToken`
*   `channels.slack.signingSecret`
*   `channels.slack.accounts.*.botToken`
*   `channels.slack.accounts.*.appToken`
*   `channels.slack.accounts.*.userToken`
*   `channels.slack.accounts.*.signingSecret`
*   `channels.discord.token`
*   `channels.discord.pluralkit.token`
*   `channels.discord.voice.tts.elevenlabs.apiKey`
*   `channels.discord.voice.tts.openai.apiKey`
*   `channels.discord.accounts.*.token`
*   `channels.discord.accounts.*.pluralkit.token`
*   `channels.discord.accounts.*.voice.tts.elevenlabs.apiKey`
*   `channels.discord.accounts.*.voice.tts.openai.apiKey`
*   `channels.irc.password`
*   `channels.irc.nickserv.password`
*   `channels.irc.accounts.*.password`
*   `channels.irc.accounts.*.nickserv.password`
*   `channels.bluebubbles.password`
*   `channels.bluebubbles.accounts.*.password`
*   `channels.feishu.appSecret`
*   `channels.feishu.verificationToken`
*   `channels.feishu.accounts.*.appSecret`
*   `channels.feishu.accounts.*.verificationToken`
*   `channels.msteams.appPassword`
*   `channels.mattermost.botToken`
*   `channels.mattermost.accounts.*.botToken`
*   `channels.matrix.password`
*   `channels.matrix.accounts.*.password`
*   `channels.nextcloud-talk.botSecret`
*   `channels.nextcloud-talk.apiPassword`
*   `channels.nextcloud-talk.accounts.*.botSecret`
*   `channels.nextcloud-talk.accounts.*.apiPassword`
*   `channels.zalo.botToken`
*   `channels.zalo.webhookSecret`
*   `channels.zalo.accounts.*.botToken`
*   `channels.zalo.accounts.*.webhookSecret`
*   `channels.googlechat.serviceAccount` via sibling `serviceAccountRef` (compatibility exception)
*   `channels.googlechat.accounts.*.serviceAccount` via sibling `serviceAccountRef` (compatibility exception)

### `auth-profiles.json` targets (`secrets configure` + `secrets apply` + `secrets audit`)

*   `profiles.*.keyRef` (`type: "api_key"`)
*   `profiles.*.tokenRef` (`type: "token"`)

Notes:

*   Auth-profile plan targets require `agentId`.
*   Plan entries target `profiles.*.key` / `profiles.*.token` and write sibling refs (`keyRef` / `tokenRef`).
*   Auth-profile refs are included in runtime resolution and audit coverage.
*   For SecretRef-managed model providers, generated `agents/*/agent/models.json` entries persist non-secret markers (not resolved secret values) for `apiKey`/header surfaces.
*   For web search:
    *   In explicit provider mode (`tools.web.search.provider` set), only the selected provider key is active.
    *   In auto mode (`tools.web.search.provider` unset), `tools.web.search.apiKey` and provider-specific keys are active.

## Unsupported credentials

Out-of-scope credentials include:

*   `commands.ownerDisplaySecret`
*   `channels.matrix.accessToken`
*   `channels.matrix.accounts.*.accessToken`
*   `hooks.token`
*   `hooks.gmail.pushToken`
*   `hooks.mappings[].sessionKey`
*   `auth-profiles.oauth.*`
*   `discord.threadBindings.*.webhookToken`
*   `whatsapp.creds.json`

Rationale:

*   These credentials are minted, rotated, session-bearing, or OAuth-durable classes that do not fit read-only external SecretRef resolution.

---

<!-- SOURCE: https://docs.openclaw.ai/reference/rpc -->

# RPC Adapters - OpenClaw

OpenClaw integrates external CLIs via JSON-RPC. Two patterns are used today.

## Pattern A: HTTP daemon (signal-cli)

*   `signal-cli` runs as a daemon with JSON-RPC over HTTP.
*   Event stream is SSE (`/api/v1/events`).
*   Health probe: `/api/v1/check`.
*   OpenClaw owns lifecycle when `channels.signal.autoStart=true`.

See [Signal](https://docs.openclaw.ai/channels/signal) for setup and endpoints.

## Pattern B: stdio child process (legacy: imsg)

> **Note:** For new iMessage setups, use [BlueBubbles](https://docs.openclaw.ai/channels/bluebubbles) instead.

*   OpenClaw spawns `imsg rpc` as a child process (legacy iMessage integration).
*   JSON-RPC is line-delimited over stdin/stdout (one JSON object per line).
*   No TCP port, no daemon required.

Core methods used:

*   `watch.subscribe` → notifications (`method: "message"`)
*   `watch.unsubscribe`
*   `send`
*   `chats.list` (probe/diagnostics)

See [iMessage](https://docs.openclaw.ai/channels/imessage) for legacy setup and addressing (`chat_id` preferred).

## Adapter guidelines

*   Gateway owns the process (start/stop tied to provider lifecycle).
*   Keep RPC clients resilient: timeouts, restart on exit.
*   Prefer stable IDs (e.g., `chat_id`) over display strings.

---

<!-- SOURCE: https://docs.openclaw.ai/reference/prompt-caching -->

# Prompt Caching - OpenClaw

Prompt caching means the model provider can reuse unchanged prompt prefixes (usually system/developer instructions and other stable context) across turns instead of re-processing them every time. The first matching request writes cache tokens (`cacheWrite`), and later matching requests can read them back (`cacheRead`). Why this matters: lower token cost, faster responses, and more predictable performance for long-running sessions. Without caching, repeated prompts pay the full prompt cost on every turn even when most input did not change. This page covers all cache-related knobs that affect prompt reuse and token cost. For Anthropic pricing details, see: [https://docs.anthropic.com/docs/build-with-claude/prompt-caching](https://docs.anthropic.com/docs/build-with-claude/prompt-caching)

## Primary knobs

### `cacheRetention` (model and per-agent)

Set cache retention on model params:

```
agents:
  defaults:
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "short" # none | short | long
```

Per-agent override:

```
agents:
  list:
    - id: "alerts"
      params:
        cacheRetention: "none"
```

Config merge order:

1.  `agents.defaults.models["provider/model"].params`
2.  `agents.list[].params` (matching agent id; overrides by key)

### Legacy `cacheControlTtl`

Legacy values are still accepted and mapped:

*   `5m` -> `short`
*   `1h` -> `long`

Prefer `cacheRetention` for new config.

### `contextPruning.mode: "cache-ttl"`

Prunes old tool-result context after cache TTL windows so post-idle requests do not re-cache oversized history.

```
agents:
  defaults:
    contextPruning:
      mode: "cache-ttl"
      ttl: "1h"
```

See [Session Pruning](https://docs.openclaw.ai/concepts/session-pruning) for full behavior.

### Heartbeat keep-warm

Heartbeat can keep cache windows warm and reduce repeated cache writes after idle gaps.

```
agents:
  defaults:
    heartbeat:
      every: "55m"
```

Per-agent heartbeat is supported at `agents.list[].heartbeat`.

## Provider behavior

### Anthropic (direct API)

*   `cacheRetention` is supported.
*   With Anthropic API-key auth profiles, OpenClaw seeds `cacheRetention: "short"` for Anthropic model refs when unset.

### Amazon Bedrock

*   Anthropic Claude model refs (`amazon-bedrock/*anthropic.claude*`) support explicit `cacheRetention` pass-through.
*   Non-Anthropic Bedrock models are forced to `cacheRetention: "none"` at runtime.

### OpenRouter Anthropic models

For `openrouter/anthropic/*` model refs, OpenClaw injects Anthropic `cache_control` on system/developer prompt blocks to improve prompt-cache reuse.

### Other providers

If the provider does not support this cache mode, `cacheRetention` has no effect.

## Tuning patterns

### Mixed traffic (recommended default)

Keep a long-lived baseline on your main agent, disable caching on bursty notifier agents:

```
agents:
  defaults:
    model:
      primary: "anthropic/claude-opus-4-6"
    models:
      "anthropic/claude-opus-4-6":
        params:
          cacheRetention: "long"
  list:
    - id: "research"
      default: true
      heartbeat:
        every: "55m"
    - id: "alerts"
      params:
        cacheRetention: "none"
```

### Cost-first baseline

*   Set baseline `cacheRetention: "short"`.
*   Enable `contextPruning.mode: "cache-ttl"`.
*   Keep heartbeat below your TTL only for agents that benefit from warm caches.

## Cache diagnostics

OpenClaw exposes dedicated cache-trace diagnostics for embedded agent runs.

### `diagnostics.cacheTrace` config

```
diagnostics:
  cacheTrace:
    enabled: true
    filePath: "~/.openclaw/logs/cache-trace.jsonl" # optional
    includeMessages: false # default true
    includePrompt: false # default true
    includeSystem: false # default true
```

Defaults:

*   `filePath`: `$OPENCLAW_STATE_DIR/logs/cache-trace.jsonl`
*   `includeMessages`: `true`
*   `includePrompt`: `true`
*   `includeSystem`: `true`

### Env toggles (one-off debugging)

*   `OPENCLAW_CACHE_TRACE=1` enables cache tracing.
*   `OPENCLAW_CACHE_TRACE_FILE=/path/to/cache-trace.jsonl` overrides output path.
*   `OPENCLAW_CACHE_TRACE_MESSAGES=0|1` toggles full message payload capture.
*   `OPENCLAW_CACHE_TRACE_PROMPT=0|1` toggles prompt text capture.
*   `OPENCLAW_CACHE_TRACE_SYSTEM=0|1` toggles system prompt capture.

### What to inspect

*   Cache trace events are JSONL and include staged snapshots like `session:loaded`, `prompt:before`, `stream:context`, and `session:after`.
*   Per-turn cache token impact is visible in normal usage surfaces via `cacheRead` and `cacheWrite` (for example `/usage full` and session usage summaries).

## Quick troubleshooting

*   High `cacheWrite` on most turns: check for volatile system-prompt inputs and verify model/provider supports your cache settings.
*   No effect from `cacheRetention`: confirm model key matches `agents.defaults.models["provider/model"]`.
*   Bedrock Nova/Mistral requests with cache settings: expected runtime force to `none`.

Related docs:

*   [Anthropic](https://docs.openclaw.ai/providers/anthropic)
*   [Token Use and Costs](https://docs.openclaw.ai/reference/token-use)
*   [Session Pruning](https://docs.openclaw.ai/concepts/session-pruning)
*   [Gateway Configuration Reference](https://docs.openclaw.ai/gateway/configuration-reference)

---

<!-- SOURCE: https://docs.openclaw.ai/reference/transcript-hygiene -->

# Transcript Hygiene - OpenClaw

## Transcript Hygiene (Provider Fixups)

This document describes **provider-specific fixes** applied to transcripts before a run (building model context). These are **in-memory** adjustments used to satisfy strict provider requirements. These hygiene steps do **not** rewrite the stored JSONL transcript on disk; however, a separate session-file repair pass may rewrite malformed JSONL files by dropping invalid lines before the session is loaded. When a repair occurs, the original file is backed up alongside the session file. Scope includes:

*   Tool call id sanitization
*   Tool call input validation
*   Tool result pairing repair
*   Turn validation / ordering
*   Thought signature cleanup
*   Image payload sanitization
*   User-input provenance tagging (for inter-session routed prompts)

If you need transcript storage details, see:

*   [/reference/session-management-compaction](https://docs.openclaw.ai/reference/session-management-compaction)

* * *

## Where this runs

All transcript hygiene is centralized in the embedded runner:

*   Policy selection: `src/agents/transcript-policy.ts`
*   Sanitization/repair application: `sanitizeSessionHistory` in `src/agents/pi-embedded-runner/google.ts`

The policy uses `provider`, `modelApi`, and `modelId` to decide what to apply. Separate from transcript hygiene, session files are repaired (if needed) before load:

*   `repairSessionFileIfNeeded` in `src/agents/session-file-repair.ts`
*   Called from `run/attempt.ts` and `compact.ts` (embedded runner)

* * *

## Global rule: image sanitization

Image payloads are always sanitized to prevent provider-side rejection due to size limits (downscale/recompress oversized base64 images). This also helps control image-driven token pressure for vision-capable models. Lower max dimensions generally reduce token usage; higher dimensions preserve detail. Implementation:

*   `sanitizeSessionMessagesImages` in `src/agents/pi-embedded-helpers/images.ts`
*   `sanitizeContentBlocksImages` in `src/agents/tool-images.ts`
*   Max image side is configurable via `agents.defaults.imageMaxDimensionPx` (default: `1200`).

* * *

Assistant tool-call blocks that are missing both `input` and `arguments` are dropped before model context is built. This prevents provider rejections from partially persisted tool calls (for example, after a rate limit failure). Implementation:

*   `sanitizeToolCallInputs` in `src/agents/session-transcript-repair.ts`
*   Applied in `sanitizeSessionHistory` in `src/agents/pi-embedded-runner/google.ts`

* * *

## Global rule: inter-session input provenance

When an agent sends a prompt into another session via `sessions_send` (including agent-to-agent reply/announce steps), OpenClaw persists the created user turn with:

*   `message.provenance.kind = "inter_session"`

This metadata is written at transcript append time and does not change role (`role: "user"` remains for provider compatibility). Transcript readers can use this to avoid treating routed internal prompts as end-user-authored instructions. During context rebuild, OpenClaw also prepends a short `[Inter-session message]` marker to those user turns in-memory so the model can distinguish them from external end-user instructions.

* * *

## Provider matrix (current behavior)

**OpenAI / OpenAI Codex**

*   Image sanitization only.
*   Drop orphaned reasoning signatures (standalone reasoning items without a following content block) for OpenAI Responses/Codex transcripts.
*   No tool call id sanitization.
*   No tool result pairing repair.
*   No turn validation or reordering.
*   No synthetic tool results.
*   No thought signature stripping.

**Google (Generative AI / Gemini CLI / Antigravity)**

*   Tool call id sanitization: strict alphanumeric.
*   Tool result pairing repair and synthetic tool results.
*   Turn validation (Gemini-style turn alternation).
*   Google turn ordering fixup (prepend a tiny user bootstrap if history starts with assistant).
*   Antigravity Claude: normalize thinking signatures; drop unsigned thinking blocks.

**Anthropic / Minimax (Anthropic-compatible)**

*   Tool result pairing repair and synthetic tool results.
*   Turn validation (merge consecutive user turns to satisfy strict alternation).

**Mistral (including model-id based detection)**

*   Tool call id sanitization: strict9 (alphanumeric length 9).

**OpenRouter Gemini**

*   Thought signature cleanup: strip non-base64 `thought_signature` values (keep base64).

**Everything else**

*   Image sanitization only.

* * *

## Historical behavior (pre-2026.1.22)

Before the 2026.1.22 release, OpenClaw applied multiple layers of transcript hygiene:

*   A **transcript-sanitize extension** ran on every context build and could:
    *   Repair tool use/result pairing.
    *   Sanitize tool call ids (including a non-strict mode that preserved `_`/`-`).
*   The runner also performed provider-specific sanitization, which duplicated work.
*   Additional mutations occurred outside the provider policy, including:
    *   Stripping `<final>` tags from assistant text before persistence.
    *   Dropping empty assistant error turns.
    *   Trimming assistant content after tool calls.

This complexity caused cross-provider regressions (notably `openai-responses` `call_id|fc_id` pairing). The 2026.1.22 cleanup removed the extension, centralized logic in the runner, and made OpenAI **no-touch** beyond image sanitization.

---

<!-- SOURCE: https://docs.openclaw.ai/reference/AGENTS.default -->

# Default AGENTS.md - OpenClaw

## AGENTS.md — OpenClaw Personal Assistant (default)

## First run (recommended)

OpenClaw uses a dedicated workspace directory for the agent. Default: `~/.openclaw/workspace` (configurable via `agents.defaults.workspace`).

1.  Create the workspace (if it doesn’t already exist):

```
mkdir -p ~/.openclaw/workspace
```

2.  Copy the default workspace templates into the workspace:

```
cp docs/reference/templates/AGENTS.md ~/.openclaw/workspace/AGENTS.md
cp docs/reference/templates/SOUL.md ~/.openclaw/workspace/SOUL.md
cp docs/reference/templates/TOOLS.md ~/.openclaw/workspace/TOOLS.md
```

3.  Optional: if you want the personal assistant skill roster, replace AGENTS.md with this file:

```
cp docs/reference/AGENTS.default.md ~/.openclaw/workspace/AGENTS.md
```

4.  Optional: choose a different workspace by setting `agents.defaults.workspace` (supports `~`):

```
{
  agents: { defaults: { workspace: "~/.openclaw/workspace" } },
}
```

## Safety defaults

*   Don’t dump directories or secrets into chat.
*   Don’t run destructive commands unless explicitly asked.
*   Don’t send partial/streaming replies to external messaging surfaces (only final replies).

## Session start (required)

*   Read `SOUL.md`, `USER.md`, `memory.md`, and today+yesterday in `memory/`.
*   Do it before responding.

## Soul (required)

*   `SOUL.md` defines identity, tone, and boundaries. Keep it current.
*   If you change `SOUL.md`, tell the user.
*   You are a fresh instance each session; continuity lives in these files.

*   You’re not the user’s voice; be careful in group chats or public channels.
*   Don’t share private data, contact info, or internal notes.

## Memory system (recommended)

*   Daily log: `memory/YYYY-MM-DD.md` (create `memory/` if needed).
*   Long-term memory: `memory.md` for durable facts, preferences, and decisions.
*   On session start, read today + yesterday + `memory.md` if present.
*   Capture: decisions, preferences, constraints, open loops.
*   Avoid secrets unless explicitly requested.

*   Tools live in skills; follow each skill’s `SKILL.md` when you need it.
*   Keep environment-specific notes in `TOOLS.md` (Notes for Skills).

## Backup tip (recommended)

If you treat this workspace as Clawd’s “memory”, make it a git repo (ideally private) so `AGENTS.md` and your memory files are backed up.

```
cd ~/.openclaw/workspace
git init
git add AGENTS.md
git commit -m "Add Clawd workspace"
# Optional: add a private remote + push
```

## What OpenClaw Does

*   Runs WhatsApp gateway + Pi coding agent so the assistant can read/write chats, fetch context, and run skills via the host Mac.
*   macOS app manages permissions (screen recording, notifications, microphone) and exposes the `openclaw` CLI via its bundled binary.
*   Direct chats collapse into the agent’s `main` session by default; groups stay isolated as `agent:<agentId>:<channel>:group:<id>` (rooms/channels: `agent:<agentId>:<channel>:channel:<id>`); heartbeats keep background tasks alive.

## Core Skills (enable in Settings → Skills)

*   **mcporter** — Tool server runtime/CLI for managing external skill backends.
*   **Peekaboo** — Fast macOS screenshots with optional AI vision analysis.
*   **camsnap** — Capture frames, clips, or motion alerts from RTSP/ONVIF security cams.
*   **oracle** — OpenAI-ready agent CLI with session replay and browser control.
*   **eightctl** — Control your sleep, from the terminal.
*   **imsg** — Send, read, stream iMessage & SMS.
*   **wacli** — WhatsApp CLI: sync, search, send.
*   **discord** — Discord actions: react, stickers, polls. Use `user:<id>` or `channel:<id>` targets (bare numeric ids are ambiguous).
*   **gog** — Google Suite CLI: Gmail, Calendar, Drive, Contacts.
*   **spotify-player** — Terminal Spotify client to search/queue/control playback.
*   **sag** — ElevenLabs speech with mac-style say UX; streams to speakers by default.
*   **Sonos CLI** — Control Sonos speakers (discover/status/playback/volume/grouping) from scripts.
*   **blucli** — Play, group, and automate BluOS players from scripts.
*   **OpenHue CLI** — Philips Hue lighting control for scenes and automations.
*   **OpenAI Whisper** — Local speech-to-text for quick dictation and voicemail transcripts.
*   **Gemini CLI** — Google Gemini models from the terminal for fast Q&A.
*   **agent-tools** — Utility toolkit for automations and helper scripts.

## Usage Notes

*   Prefer the `openclaw` CLI for scripting; mac app handles permissions.
*   Run installs from the Skills tab; it hides the button if a binary is already present.
*   Keep heartbeats enabled so the assistant can schedule reminders, monitor inboxes, and trigger camera captures.
*   Canvas UI runs full-screen with native overlays. Avoid placing critical controls in the top-left/top-right/bottom edges; add explicit gutters in the layout and don’t rely on safe-area insets.
*   For browser-driven verification, use `openclaw browser` (tabs/status/screenshot) with the OpenClaw-managed Chrome profile.
*   For DOM inspection, use `openclaw browser eval|query|dom|snapshot` (and `--json`/`--out` when you need machine output).
*   For interactions, use `openclaw browser click|type|hover|drag|select|upload|press|wait|navigate|back|evaluate|run` (click/type require snapshot refs; use `evaluate` for CSS selectors).

---

<!-- SOURCE: https://docs.openclaw.ai/reference/device-models -->

# Device Model Database - OpenClaw

## Device model database (friendly names)

The macOS companion app shows friendly Apple device model names in the **Instances** UI by mapping Apple model identifiers (e.g. `iPad16,6`, `Mac16,6`) to human-readable names. The mapping is vendored as JSON under:

*   `apps/macos/Sources/OpenClaw/Resources/DeviceModels/`

## Data source

We currently vendor the mapping from the MIT-licensed repository:

*   `kyle-seongwoo-jun/apple-device-identifiers`

To keep builds deterministic, the JSON files are pinned to specific upstream commits (recorded in `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`).

## Updating the database

1.  Pick the upstream commits you want to pin to (one for iOS, one for macOS).
2.  Update the commit hashes in `apps/macos/Sources/OpenClaw/Resources/DeviceModels/NOTICE.md`.
3.  Re-download the JSON files, pinned to those commits:

```
IOS_COMMIT="<commit sha for ios-device-identifiers.json>"
MAC_COMMIT="<commit sha for mac-device-identifiers.json>"

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${IOS_COMMIT}/ios-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/ios-device-identifiers.json

curl -fsSL "https://raw.githubusercontent.com/kyle-seongwoo-jun/apple-device-identifiers/${MAC_COMMIT}/mac-device-identifiers.json" \
  -o apps/macos/Sources/OpenClaw/Resources/DeviceModels/mac-device-identifiers.json
```

4.  Ensure `apps/macos/Sources/OpenClaw/Resources/DeviceModels/LICENSE.apple-device-identifiers.txt` still matches upstream (replace it if the upstream license changes).
5.  Verify the macOS app builds cleanly (no warnings):

```
swift build --package-path apps/macos
```

---

<!-- SOURCE: https://docs.openclaw.ai/reference/api-usage-costs -->

# API Usage and Costs - OpenClaw

This doc lists **features that can invoke API keys** and where their costs show up. It focuses on OpenClaw features that can generate provider usage or paid API calls.

## Where costs show up (chat + CLI)

**Per-session cost snapshot**

*   `/status` shows the current session model, context usage, and last response tokens.
*   If the model uses **API-key auth**, `/status` also shows **estimated cost** for the last reply.

**Per-message cost footer**

*   `/usage full` appends a usage footer to every reply, including **estimated cost** (API-key only).
*   `/usage tokens` shows tokens only; OAuth flows hide dollar cost.

**CLI usage windows (provider quotas)**

*   `openclaw status --usage` and `openclaw channels list` show provider **usage windows** (quota snapshots, not per-message costs).

See [Token use & costs](https://docs.openclaw.ai/reference/token-use) for details and examples.

## How keys are discovered

OpenClaw can pick up credentials from:

*   **Auth profiles** (per-agent, stored in `auth-profiles.json`).
*   **Environment variables** (e.g. `OPENAI_API_KEY`, `BRAVE_API_KEY`, `FIRECRAWL_API_KEY`).
*   **Config** (`models.providers.*.apiKey`, `tools.web.search.*`, `tools.web.fetch.firecrawl.*`, `memorySearch.*`, `talk.apiKey`).
*   **Skills** (`skills.entries.<name>.apiKey`) which may export keys to the skill process env.

## Features that can spend keys

### 1) Core model responses (chat + tools)

Every reply or tool call uses the **current model provider** (OpenAI, Anthropic, etc). This is the primary source of usage and cost. See [Models](https://docs.openclaw.ai/providers/models) for pricing config and [Token use & costs](https://docs.openclaw.ai/reference/token-use) for display.

### 2) Media understanding (audio/image/video)

Inbound media can be summarized/transcribed before the reply runs. This uses model/provider APIs.

*   Audio: OpenAI / Groq / Deepgram (now **auto-enabled** when keys exist).
*   Image: OpenAI / Anthropic / Google.
*   Video: Google.

See [Media understanding](https://docs.openclaw.ai/nodes/media-understanding).

### 3) Memory embeddings + semantic search

Semantic memory search uses **embedding APIs** when configured for remote providers:

*   `memorySearch.provider = "openai"` → OpenAI embeddings
*   `memorySearch.provider = "gemini"` → Gemini embeddings
*   `memorySearch.provider = "voyage"` → Voyage embeddings
*   `memorySearch.provider = "mistral"` → Mistral embeddings
*   `memorySearch.provider = "ollama"` → Ollama embeddings (local/self-hosted; typically no hosted API billing)
*   Optional fallback to a remote provider if local embeddings fail

You can keep it local with `memorySearch.provider = "local"` (no API usage). See [Memory](https://docs.openclaw.ai/concepts/memory).

### 4) Web search tool

`web_search` uses API keys and may incur usage charges depending on your provider:

*   **Brave Search API**: `BRAVE_API_KEY` or `tools.web.search.apiKey`
*   **Gemini (Google Search)**: `GEMINI_API_KEY`
*   **Grok (xAI)**: `XAI_API_KEY`
*   **Kimi (Moonshot)**: `KIMI_API_KEY` or `MOONSHOT_API_KEY`
*   **Perplexity Search API**: `PERPLEXITY_API_KEY`

**Brave Search free credit:** Each Brave plan includes 5/monthinrenewingfreecredit.TheSearchplancosts5/month in renewing free credit. The Search plan costs 5 per 1,000 requests, so the credit covers 1,000 requests/month at no charge. Set your usage limit in the Brave dashboard to avoid unexpected charges. See [Web tools](https://docs.openclaw.ai/tools/web).

### 5) Web fetch tool (Firecrawl)

`web_fetch` can call **Firecrawl** when an API key is present:

*   `FIRECRAWL_API_KEY` or `tools.web.fetch.firecrawl.apiKey`

If Firecrawl isn’t configured, the tool falls back to direct fetch + readability (no paid API). See [Web tools](https://docs.openclaw.ai/tools/web).

### 6) Provider usage snapshots (status/health)

Some status commands call **provider usage endpoints** to display quota windows or auth health. These are typically low-volume calls but still hit provider APIs:

*   `openclaw status --usage`
*   `openclaw models status --json`

See [Models CLI](https://docs.openclaw.ai/cli/models).

### 7) Compaction safeguard summarization

The compaction safeguard can summarize session history using the **current model**, which invokes provider APIs when it runs. See [Session management + compaction](https://docs.openclaw.ai/reference/session-management-compaction).

### 8) Model scan / probe

`openclaw models scan` can probe OpenRouter models and uses `OPENROUTER_API_KEY` when probing is enabled. See [Models CLI](https://docs.openclaw.ai/cli/models).

### 9) Talk (speech)

Talk mode can invoke **ElevenLabs** when configured:

*   `ELEVENLABS_API_KEY` or `talk.apiKey`

See [Talk mode](https://docs.openclaw.ai/nodes/talk).

### 10) Skills (third-party APIs)

Skills can store `apiKey` in `skills.entries.<name>.apiKey`. If a skill uses that key for external APIs, it can incur costs according to the skill’s provider. See [Skills](https://docs.openclaw.ai/tools/skills).

---

<!-- SOURCE: https://docs.openclaw.ai/reference/test -->

# Tests - OpenClaw

*   Full testing kit (suites, live, Docker): [Testing](https://docs.openclaw.ai/help/testing)
*   `pnpm test:force`: Kills any lingering gateway process holding the default control port, then runs the full Vitest suite with an isolated gateway port so server tests don’t collide with a running instance. Use this when a prior gateway run left port 18789 occupied.
*   `pnpm test:coverage`: Runs the unit suite with V8 coverage (via `vitest.unit.config.ts`). Global thresholds are 70% lines/branches/functions/statements. Coverage excludes integration-heavy entrypoints (CLI wiring, gateway/telegram bridges, webchat static server) to keep the target focused on unit-testable logic.
*   `pnpm test` on Node 24+: OpenClaw auto-disables Vitest `vmForks` and uses `forks` to avoid `ERR_VM_MODULE_LINK_FAILURE` / `module is already linked`. You can force behavior with `OPENCLAW_TEST_VM_FORKS=0|1`.
*   `pnpm test`: runs the fast core unit lane by default for quick local feedback.
*   `pnpm test:channels`: runs channel-heavy suites.
*   `pnpm test:extensions`: runs extension/plugin suites.
*   Gateway integration: opt-in via `OPENCLAW_TEST_INCLUDE_GATEWAY=1 pnpm test` or `pnpm test:gateway`.
*   `pnpm test:e2e`: Runs gateway end-to-end smoke tests (multi-instance WS/HTTP/node pairing). Defaults to `vmForks` + adaptive workers in `vitest.e2e.config.ts`; tune with `OPENCLAW_E2E_WORKERS=<n>` and set `OPENCLAW_E2E_VERBOSE=1` for verbose logs.
*   `pnpm test:live`: Runs provider live tests (minimax/zai). Requires API keys and `LIVE=1` (or provider-specific `*_LIVE_TEST=1`) to unskip.

## Local PR gate

For local PR land/gate checks, run:

*   `pnpm check`
*   `pnpm build`
*   `pnpm test`
*   `pnpm check:docs`

If `pnpm test` flakes on a loaded host, rerun once before treating it as a regression, then isolate with `pnpm vitest run <path/to/test>`. For memory-constrained hosts, use:

*   `OPENCLAW_TEST_PROFILE=low OPENCLAW_TEST_SERIAL_GATEWAY=1 pnpm test`

## Model latency bench (local keys)

Script: [`scripts/bench-model.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-model.ts) Usage:

*   `source ~/.profile && pnpm tsx scripts/bench-model.ts --runs 10`
*   Optional env: `MINIMAX_API_KEY`, `MINIMAX_BASE_URL`, `MINIMAX_MODEL`, `ANTHROPIC_API_KEY`
*   Default prompt: “Reply with a single word: ok. No punctuation or extra text.”

Last run (2025-12-31, 20 runs):

*   minimax median 1279ms (min 1114, max 2431)
*   opus median 2454ms (min 1224, max 3170)

## CLI startup bench

Script: [`scripts/bench-cli-startup.ts`](https://github.com/openclaw/openclaw/blob/main/scripts/bench-cli-startup.ts) Usage:

*   `pnpm tsx scripts/bench-cli-startup.ts`
*   `pnpm tsx scripts/bench-cli-startup.ts --runs 12`
*   `pnpm tsx scripts/bench-cli-startup.ts --entry dist/entry.js --timeout-ms 45000`

This benchmarks these commands:

*   `--version`
*   `--help`
*   `health --json`
*   `status --json`
*   `status`

Output includes avg, p50, p95, min/max, and exit-code/signal distribution for each command.

## Onboarding E2E (Docker)

Docker is optional; this is only needed for containerized onboarding smoke tests. Full cold-start flow in a clean Linux container:

```
scripts/e2e/onboard-docker.sh
```

This script drives the interactive wizard via a pseudo-tty, verifies config/workspace/session files, then starts the gateway and runs `openclaw health`.

## QR import smoke (Docker)

Ensures `qrcode-terminal` loads under Node 22+ in Docker:

---

<!-- SOURCE: https://docs.openclaw.ai/reference/RELEASING -->

# Release Checklist - OpenClaw

## Release Checklist (npm + macOS)

Use `pnpm` (Node 22+) from the repo root. Keep the working tree clean before tagging/publishing.

## Operator trigger

When the operator says “release”, immediately do this preflight (no extra questions unless blocked):

*   Read this doc and `docs/platforms/mac/release.md`.
*   Load env from `~/.profile` and confirm `SPARKLE_PRIVATE_KEY_FILE` + App Store Connect vars are set (SPARKLE\_PRIVATE\_KEY\_FILE should live in `~/.profile`).
*   Use Sparkle keys from `~/Library/CloudStorage/Dropbox/Backup/Sparkle` if needed.

1.  **Version & metadata**

*   Bump `package.json` version (e.g., `2026.1.29`).
*   Run `pnpm plugins:sync` to align extension package versions + changelogs.
*   Update CLI/version strings in [`src/version.ts`](https://github.com/openclaw/openclaw/blob/main/src/version.ts) and the Baileys user agent in [`src/web/session.ts`](https://github.com/openclaw/openclaw/blob/main/src/web/session.ts).
*   Confirm package metadata (name, description, repository, keywords, license) and `bin` map points to [`openclaw.mjs`](https://github.com/openclaw/openclaw/blob/main/openclaw.mjs) for `openclaw`.
*   If dependencies changed, run `pnpm install` so `pnpm-lock.yaml` is current.

2.  **Build & artifacts**

*   If A2UI inputs changed, run `pnpm canvas:a2ui:bundle` and commit any updated [`src/canvas-host/a2ui/a2ui.bundle.js`](https://github.com/openclaw/openclaw/blob/main/src/canvas-host/a2ui/a2ui.bundle.js).
*   `pnpm run build` (regenerates `dist/`).
*   Verify npm package `files` includes all required `dist/*` folders (notably `dist/node-host/**` and `dist/acp/**` for headless node + ACP CLI).
*   Confirm `dist/build-info.json` exists and includes the expected `commit` hash (CLI banner uses this for npm installs).
*   Optional: `npm pack --pack-destination /tmp` after the build; inspect the tarball contents and keep it handy for the GitHub release (do **not** commit it).

3.  **Changelog & docs**

*   Update `CHANGELOG.md` with user-facing highlights (create the file if missing); keep entries strictly descending by version.
*   Ensure README examples/flags match current CLI behavior (notably new commands or options).

4.  **Validation**

*   `pnpm build`
*   `pnpm check`
*   `pnpm test` (or `pnpm test:coverage` if you need coverage output)
*   `pnpm release:check` (verifies npm pack contents)
*   `OPENCLAW_INSTALL_SMOKE_SKIP_NONROOT=1 pnpm test:install:smoke` (Docker install smoke test, fast path; required before release)
    *   If the immediate previous npm release is known broken, set `OPENCLAW_INSTALL_SMOKE_PREVIOUS=<last-good-version>` or `OPENCLAW_INSTALL_SMOKE_SKIP_PREVIOUS=1` for the preinstall step.
*   (Optional) Full installer smoke (adds non-root + CLI coverage): `pnpm test:install:smoke`
*   (Optional) Installer E2E (Docker, runs `curl -fsSL https://openclaw.ai/install.sh | bash`, onboards, then runs real tool calls):
    *   `pnpm test:install:e2e:openai` (requires `OPENAI_API_KEY`)
    *   `pnpm test:install:e2e:anthropic` (requires `ANTHROPIC_API_KEY`)
    *   `pnpm test:install:e2e` (requires both keys; runs both providers)
*   (Optional) Spot-check the web gateway if your changes affect send/receive paths.

5.  **macOS app (Sparkle)**

*   Build + sign the macOS app, then zip it for distribution.
*   Generate the Sparkle appcast (HTML notes via [`scripts/make_appcast.sh`](https://github.com/openclaw/openclaw/blob/main/scripts/make_appcast.sh)) and update `appcast.xml`.
*   Keep the app zip (and optional dSYM zip) ready to attach to the GitHub release.
*   Follow [macOS release](https://docs.openclaw.ai/platforms/mac/release) for the exact commands and required env vars.
    *   `APP_BUILD` must be numeric + monotonic (no `-beta`) so Sparkle compares versions correctly.
    *   If notarizing, use the `openclaw-notary` keychain profile created from App Store Connect API env vars (see [macOS release](https://docs.openclaw.ai/platforms/mac/release)).

6.  **Publish (npm)**

*   Confirm git status is clean; commit and push as needed.
*   `npm login` (verify 2FA) if needed.
*   `npm publish --access public` (use `--tag beta` for pre-releases).
*   Verify the registry: `npm view openclaw version`, `npm view openclaw dist-tags`, and `npx -y openclaw@X.Y.Z --version` (or `--help`).

### Troubleshooting (notes from 2.0.0-beta2 release)

*   **npm pack/publish hangs or produces huge tarball**: the macOS app bundle in `dist/OpenClaw.app` (and release zips) get swept into the package. Fix by whitelisting publish contents via `package.json` `files` (include dist subdirs, docs, skills; exclude app bundles). Confirm with `npm pack --dry-run` that `dist/OpenClaw.app` is not listed.
*   **npm auth web loop for dist-tags**: use legacy auth to get an OTP prompt:
    *   `NPM_CONFIG_AUTH_TYPE=legacy npm dist-tag add openclaw@X.Y.Z latest`
*   **`npx` verification fails with `ECOMPROMISED: Lock compromised`**: retry with a fresh cache:
    *   `NPM_CONFIG_CACHE=/tmp/npm-cache-$(date +%s) npx -y openclaw@X.Y.Z --version`
*   **Tag needs repointing after a late fix**: force-update and push the tag, then ensure the GitHub release assets still match:
    *   `git tag -f vX.Y.Z && git push -f origin vX.Y.Z`

7.  **GitHub release + appcast**

*   Tag and push: `git tag vX.Y.Z && git push origin vX.Y.Z` (or `git push --tags`).
*   Create/refresh the GitHub release for `vX.Y.Z` with **title `openclaw X.Y.Z`** (not just the tag); body should include the **full** changelog section for that version (Highlights + Changes + Fixes), inline (no bare links), and **must not repeat the title inside the body**.
*   Attach artifacts: `npm pack` tarball (optional), `OpenClaw-X.Y.Z.zip`, and `OpenClaw-X.Y.Z.dSYM.zip` (if generated).
*   Commit the updated `appcast.xml` and push it (Sparkle feeds from main).
*   From a clean temp directory (no `package.json`), run `npx -y openclaw@X.Y.Z send --help` to confirm install/CLI entrypoints work.
*   Announce/share release notes.

## Plugin publish scope (npm)

We only publish **existing npm plugins** under the `@openclaw/*` scope. Bundled plugins that are not on npm stay **disk-tree only** (still shipped in `extensions/**`). Process to derive the list:

1.  `npm search @openclaw --json` and capture the package names.
2.  Compare with `extensions/*/package.json` names.
3.  Publish only the **intersection** (already on npm).

Current npm plugin list (update as needed):

*   @openclaw/bluebubbles
*   @openclaw/diagnostics-otel
*   @openclaw/discord
*   @openclaw/feishu
*   @openclaw/lobster
*   @openclaw/matrix
*   @openclaw/msteams
*   @openclaw/nextcloud-talk
*   @openclaw/nostr
*   @openclaw/voice-call
*   @openclaw/zalo
*   @openclaw/zalouser

Release notes must also call out **new optional bundled plugins** that are **not on by default** (example: `tlon`).

---

<!-- SOURCE: https://docs.openclaw.ai/reference/session-management-compaction -->

# Session Management Deep Dive - OpenClaw

## Session Management & Compaction (Deep Dive)

This document explains how OpenClaw manages sessions end-to-end:

*   **Session routing** (how inbound messages map to a `sessionKey`)
*   **Session store** (`sessions.json`) and what it tracks
*   **Transcript persistence** (`*.jsonl`) and its structure
*   **Transcript hygiene** (provider-specific fixups before runs)
*   **Context limits** (context window vs tracked tokens)
*   **Compaction** (manual + auto-compaction) and where to hook pre-compaction work
*   **Silent housekeeping** (e.g. memory writes that shouldn’t produce user-visible output)

If you want a higher-level overview first, start with:

*   [/concepts/session](https://docs.openclaw.ai/concepts/session)
*   [/concepts/compaction](https://docs.openclaw.ai/concepts/compaction)
*   [/concepts/session-pruning](https://docs.openclaw.ai/concepts/session-pruning)
*   [/reference/transcript-hygiene](https://docs.openclaw.ai/reference/transcript-hygiene)

* * *

## Source of truth: the Gateway

OpenClaw is designed around a single **Gateway process** that owns session state.

*   UIs (macOS app, web Control UI, TUI) should query the Gateway for session lists and token counts.
*   In remote mode, session files are on the remote host; “checking your local Mac files” won’t reflect what the Gateway is using.

* * *

## Two persistence layers

OpenClaw persists sessions in two layers:

1.  **Session store (`sessions.json`)**
    *   Key/value map: `sessionKey -> SessionEntry`
    *   Small, mutable, safe to edit (or delete entries)
    *   Tracks session metadata (current session id, last activity, toggles, token counters, etc.)
2.  **Transcript (`<sessionId>.jsonl`)**
    *   Append-only transcript with tree structure (entries have `id` + `parentId`)
    *   Stores the actual conversation + tool calls + compaction summaries
    *   Used to rebuild the model context for future turns

* * *

## On-disk locations

Per agent, on the Gateway host:

*   Store: `~/.openclaw/agents/<agentId>/sessions/sessions.json`
*   Transcripts: `~/.openclaw/agents/<agentId>/sessions/<sessionId>.jsonl`
    *   Telegram topic sessions: `.../<sessionId>-topic-<threadId>.jsonl`

OpenClaw resolves these via `src/config/sessions.ts`.

* * *

## Store maintenance and disk controls

Session persistence has automatic maintenance controls (`session.maintenance`) for `sessions.json` and transcript artifacts:

*   `mode`: `warn` (default) or `enforce`
*   `pruneAfter`: stale-entry age cutoff (default `30d`)
*   `maxEntries`: cap entries in `sessions.json` (default `500`)
*   `rotateBytes`: rotate `sessions.json` when oversized (default `10mb`)
*   `resetArchiveRetention`: retention for `*.reset.<timestamp>` transcript archives (default: same as `pruneAfter`; `false` disables cleanup)
*   `maxDiskBytes`: optional sessions-directory budget
*   `highWaterBytes`: optional target after cleanup (default `80%` of `maxDiskBytes`)

Enforcement order for disk budget cleanup (`mode: "enforce"`):

1.  Remove oldest archived or orphan transcript artifacts first.
2.  If still above the target, evict oldest session entries and their transcript files.
3.  Keep going until usage is at or below `highWaterBytes`.

In `mode: "warn"`, OpenClaw reports potential evictions but does not mutate the store/files. Run maintenance on demand:

```
openclaw sessions cleanup --dry-run
openclaw sessions cleanup --enforce
```

* * *

## Cron sessions and run logs

Isolated cron runs also create session entries/transcripts, and they have dedicated retention controls:

*   `cron.sessionRetention` (default `24h`) prunes old isolated cron run sessions from the session store (`false` disables).
*   `cron.runLog.maxBytes` + `cron.runLog.keepLines` prune `~/.openclaw/cron/runs/<jobId>.jsonl` files (defaults: `2_000_000` bytes and `2000` lines).

* * *

## Session keys (`sessionKey`)

A `sessionKey` identifies _which conversation bucket_ you’re in (routing + isolation). Common patterns:

*   Main/direct chat (per agent): `agent:<agentId>:<mainKey>` (default `main`)
*   Group: `agent:<agentId>:<channel>:group:<id>`
*   Room/channel (Discord/Slack): `agent:<agentId>:<channel>:channel:<id>` or `...:room:<id>`
*   Cron: `cron:<job.id>`
*   Webhook: `hook:<uuid>` (unless overridden)

The canonical rules are documented at [/concepts/session](https://docs.openclaw.ai/concepts/session).

* * *

## Session ids (`sessionId`)

Each `sessionKey` points at a current `sessionId` (the transcript file that continues the conversation). Rules of thumb:

*   **Reset** (`/new`, `/reset`) creates a new `sessionId` for that `sessionKey`.
*   **Daily reset** (default 4:00 AM local time on the gateway host) creates a new `sessionId` on the next message after the reset boundary.
*   **Idle expiry** (`session.reset.idleMinutes` or legacy `session.idleMinutes`) creates a new `sessionId` when a message arrives after the idle window. When daily + idle are both configured, whichever expires first wins.
*   **Thread parent fork guard** (`session.parentForkMaxTokens`, default `100000`) skips parent transcript forking when the parent session is already too large; the new thread starts fresh. Set `0` to disable.

Implementation detail: the decision happens in `initSessionState()` in `src/auto-reply/reply/session.ts`.

* * *

## Session store schema (`sessions.json`)

The store’s value type is `SessionEntry` in `src/config/sessions.ts`. Key fields (not exhaustive):

*   `sessionId`: current transcript id (filename is derived from this unless `sessionFile` is set)
*   `updatedAt`: last activity timestamp
*   `sessionFile`: optional explicit transcript path override
*   `chatType`: `direct | group | room` (helps UIs and send policy)
*   `provider`, `subject`, `room`, `space`, `displayName`: metadata for group/channel labeling
*   Toggles:
    *   `thinkingLevel`, `verboseLevel`, `reasoningLevel`, `elevatedLevel`
    *   `sendPolicy` (per-session override)
*   Model selection:
    *   `providerOverride`, `modelOverride`, `authProfileOverride`
*   Token counters (best-effort / provider-dependent):
    *   `inputTokens`, `outputTokens`, `totalTokens`, `contextTokens`
*   `compactionCount`: how often auto-compaction completed for this session key
*   `memoryFlushAt`: timestamp for the last pre-compaction memory flush
*   `memoryFlushCompactionCount`: compaction count when the last flush ran

The store is safe to edit, but the Gateway is the authority: it may rewrite or rehydrate entries as sessions run.

* * *

## Transcript structure (`*.jsonl`)

Transcripts are managed by `@mariozechner/pi-coding-agent`’s `SessionManager`. The file is JSONL:

*   First line: session header (`type: "session"`, includes `id`, `cwd`, `timestamp`, optional `parentSession`)
*   Then: session entries with `id` + `parentId` (tree)

Notable entry types:

*   `message`: user/assistant/toolResult messages
*   `custom_message`: extension-injected messages that _do_ enter model context (can be hidden from UI)
*   `custom`: extension state that does _not_ enter model context
*   `compaction`: persisted compaction summary with `firstKeptEntryId` and `tokensBefore`
*   `branch_summary`: persisted summary when navigating a tree branch

OpenClaw intentionally does **not** “fix up” transcripts; the Gateway uses `SessionManager` to read/write them.

* * *

## Context windows vs tracked tokens

Two different concepts matter:

1.  **Model context window**: hard cap per model (tokens visible to the model)
2.  **Session store counters**: rolling stats written into `sessions.json` (used for /status and dashboards)

If you’re tuning limits:

*   The context window comes from the model catalog (and can be overridden via config).
*   `contextTokens` in the store is a runtime estimate/reporting value; don’t treat it as a strict guarantee.

For more, see [/token-use](https://docs.openclaw.ai/reference/token-use).

* * *

## Compaction: what it is

Compaction summarizes older conversation into a persisted `compaction` entry in the transcript and keeps recent messages intact. After compaction, future turns see:

*   The compaction summary
*   Messages after `firstKeptEntryId`

Compaction is **persistent** (unlike session pruning). See [/concepts/session-pruning](https://docs.openclaw.ai/concepts/session-pruning).

* * *

## When auto-compaction happens (Pi runtime)

In the embedded Pi agent, auto-compaction triggers in two cases:

1.  **Overflow recovery**: the model returns a context overflow error → compact → retry.
2.  **Threshold maintenance**: after a successful turn, when:

`contextTokens > contextWindow - reserveTokens` Where:

*   `contextWindow` is the model’s context window
*   `reserveTokens` is headroom reserved for prompts + the next model output

These are Pi runtime semantics (OpenClaw consumes the events, but Pi decides when to compact).

* * *

## Compaction settings (`reserveTokens`, `keepRecentTokens`)

Pi’s compaction settings live in Pi settings:

```
{
  compaction: {
    enabled: true,
    reserveTokens: 16384,
    keepRecentTokens: 20000,
  },
}
```

OpenClaw also enforces a safety floor for embedded runs:

*   If `compaction.reserveTokens < reserveTokensFloor`, OpenClaw bumps it.
*   Default floor is `20000` tokens.
*   Set `agents.defaults.compaction.reserveTokensFloor: 0` to disable the floor.
*   If it’s already higher, OpenClaw leaves it alone.

Why: leave enough headroom for multi-turn “housekeeping” (like memory writes) before compaction becomes unavoidable. Implementation: `ensurePiCompactionReserveTokens()` in `src/agents/pi-settings.ts` (called from `src/agents/pi-embedded-runner.ts`).

* * *

## User-visible surfaces

You can observe compaction and session state via:

*   `/status` (in any chat session)
*   `openclaw status` (CLI)
*   `openclaw sessions` / `sessions --json`
*   Verbose mode: `🧹 Auto-compaction complete` + compaction count

* * *

## Silent housekeeping (`NO_REPLY`)

OpenClaw supports “silent” turns for background tasks where the user should not see intermediate output. Convention:

*   The assistant starts its output with `NO_REPLY` to indicate “do not deliver a reply to the user”.
*   OpenClaw strips/suppresses this in the delivery layer.

As of `2026.1.10`, OpenClaw also suppresses **draft/typing streaming** when a partial chunk begins with `NO_REPLY`, so silent operations don’t leak partial output mid-turn.

* * *

## Pre-compaction “memory flush” (implemented)

Goal: before auto-compaction happens, run a silent agentic turn that writes durable state to disk (e.g. `memory/YYYY-MM-DD.md` in the agent workspace) so compaction can’t erase critical context. OpenClaw uses the **pre-threshold flush** approach:

1.  Monitor session context usage.
2.  When it crosses a “soft threshold” (below Pi’s compaction threshold), run a silent “write memory now” directive to the agent.
3.  Use `NO_REPLY` so the user sees nothing.

Config (`agents.defaults.compaction.memoryFlush`):

*   `enabled` (default: `true`)
*   `softThresholdTokens` (default: `4000`)
*   `prompt` (user message for the flush turn)
*   `systemPrompt` (extra system prompt appended for the flush turn)

Notes:

*   The default prompt/system prompt include a `NO_REPLY` hint to suppress delivery.
*   The flush runs once per compaction cycle (tracked in `sessions.json`).
*   The flush runs only for embedded Pi sessions (CLI backends skip it).
*   The flush is skipped when the session workspace is read-only (`workspaceAccess: "ro"` or `"none"`).
*   See [Memory](https://docs.openclaw.ai/concepts/memory) for the workspace file layout and write patterns.

Pi also exposes a `session_before_compact` hook in the extension API, but OpenClaw’s flush logic lives on the Gateway side today.

* * *

## Troubleshooting checklist

*   Session key wrong? Start with [/concepts/session](https://docs.openclaw.ai/concepts/session) and confirm the `sessionKey` in `/status`.
*   Store vs transcript mismatch? Confirm the Gateway host and the store path from `openclaw status`.
*   Compaction spam? Check:
    *   model context window (too small)
    *   compaction settings (`reserveTokens` too high for the model window can cause earlier compaction)
    *   tool-result bloat: enable/tune session pruning
*   Silent turns leaking? Confirm the reply starts with `NO_REPLY` (exact token) and you’re on a build that includes the streaming suppression fix.

---

<!-- SOURCE: https://docs.openclaw.ai/ci -->

# CI Pipeline - OpenClaw

The CI runs on every push to `main` and every pull request. It uses smart scoping to skip expensive jobs when only docs or native code changed.

## Job Overview

| Job | Purpose | When it runs |
| --- | --- | --- |
| `docs-scope` | Detect docs-only changes | Always |
| `changed-scope` | Detect which areas changed (node/macos/android/windows) | Non-docs PRs |
| `check` | TypeScript types, lint, format | Push to `main`, or PRs with Node-relevant changes |
| `check-docs` | Markdown lint + broken link check | Docs changed |
| `code-analysis` | LOC threshold check (1000 lines) | PRs only |
| `secrets` | Detect leaked secrets | Always |
| `build-artifacts` | Build dist once, share with other jobs | Non-docs, node changes |
| `release-check` | Validate npm pack contents | After build |
| `checks` | Node/Bun tests + protocol check | Non-docs, node changes |
| `checks-windows` | Windows-specific tests | Non-docs, windows-relevant changes |
| `macos` | Swift lint/build/test + TS tests | PRs with macos changes |
| `android` | Gradle build + tests | Non-docs, android changes |

## Fail-Fast Order

Jobs are ordered so cheap checks fail before expensive ones run:

1.  `docs-scope` + `code-analysis` + `check` (parallel, ~1-2 min)
2.  `build-artifacts` (blocked on above)
3.  `checks`, `checks-windows`, `macos`, `android` (blocked on build)

Scope logic lives in `scripts/ci-changed-scope.mjs` and is covered by unit tests in `src/scripts/ci-changed-scope.test.ts`.

## Runners

| Runner | Jobs |
| --- | --- |
| `blacksmith-16vcpu-ubuntu-2404` | Most Linux jobs, including scope detection |
| `blacksmith-32vcpu-windows-2025` | `checks-windows` |
| `macos-latest` | `macos`, `ios` |

## Local Equivalents

```
pnpm check          # types + lint + format
pnpm test           # vitest tests
pnpm check:docs     # docs format + lint + broken links
pnpm release:check  # validate npm pack
```

