# loop-engine-governance

## Overview

`loop-engine-governance` adds policy enforcement to OpenClaw workflows by routing decisions through Loop Engine transitions and guards.

## Modes of operation

### Local governance mode (no external LLM provider)

- Uses Loop Engine runtime, guards, and audit trail only.
- No external LLM API calls occur in this mode.
- Suitable for human-only and automation-only loop flows.

### LLM-augmented mode (external provider calls enabled)

- Enabled only when a provider adapter is explicitly configured.
- Provider-backed examples call external APIs and may transmit prompt/evidence context to that provider.

## Installation

```bash
# Core (required for all modes)
npm install @loop-engine/sdk @loop-engine/adapter-memory @loop-engine/adapter-openclaw

# Optional: provider-backed adapters (install only what you use)
npm install @loop-engine/adapter-anthropic @anthropic-ai/sdk
npm install @loop-engine/adapter-openai openai
npm install @loop-engine/adapter-grok
```

## Configuration

- Local mode requires loop definitions, storage, and guard registry configuration only.
- Provider-backed mode additionally requires the corresponding provider adapter and API key.
- External provider calls are activated by adapter usage (for example `createOpenAIActorAdapter(...)`), not by Loop Engine core alone.

## Environment variables

Provider keys are required only for provider-backed examples:

| Example | Mode | Required env var |
|---|---|---|
| `example-expense-approval.ts` | local governance | none |
| `example-openclaw-integration.ts` | local governance + OpenClaw gateway | none |
| `example-ai-replenishment-claude.ts` | provider-backed (Anthropic) | `ANTHROPIC_API_KEY` |
| `example-infrastructure-change-openai.ts` | provider-backed (OpenAI) | `OPENAI_API_KEY` |
| `example-fraud-review-grok.ts` | provider-backed (xAI) | `XAI_API_KEY` |

Additional provider key used elsewhere in this repo:

- `GOOGLE_AI_API_KEY` for `@loop-engine/adapter-gemini` examples and adapter usage.

## External network and data flow

- **No provider adapter configured:** no external LLM network calls.
- **Provider adapter configured:** prompt/evidence context passed to `createSubmission(...)` may be sent to:
  - OpenAI (`@loop-engine/adapter-openai`)
  - Anthropic (`@loop-engine/adapter-anthropic`)
  - xAI Grok (`@loop-engine/adapter-grok`)
  - Google Gemini (`@loop-engine/adapter-gemini`)
- OpenClaw integration (`@loop-engine/adapter-openclaw`) uses a WebSocket gateway connection (`gatewayUrl`, default `ws://127.0.0.1:18789`) for event forwarding.

## Sensitive data guidance

- Do not send raw PII, PHI, PCI, credentials, or other regulated data to provider-backed examples without review.
- Redact, tokenize, or minimize sensitive fields before submitting evidence context.
- Review provider retention, training, and contractual controls before production use.

## Provenance

- **Canonical repository:** https://github.com/loopengine/loop-engine
- **Skill source path:** `packages/adapter-openclaw/loop-engine-governance/`
- **Maintainer organization:** Better Data, Inc. (https://betterdata.co)
- **Documentation site:** https://loopengine.io/docs/integrations/openclaw

## Package/source references

- `@loop-engine/adapter-openclaw`: https://www.npmjs.com/package/@loop-engine/adapter-openclaw
- `@loop-engine/sdk`: https://www.npmjs.com/package/@loop-engine/sdk
- `@loop-engine/adapter-openai`: https://www.npmjs.com/package/@loop-engine/adapter-openai
- `@loop-engine/adapter-anthropic`: https://www.npmjs.com/package/@loop-engine/adapter-anthropic
- `@loop-engine/adapter-grok`: https://www.npmjs.com/package/@loop-engine/adapter-grok
- `@loop-engine/adapter-gemini`: https://www.npmjs.com/package/@loop-engine/adapter-gemini

## What this skill does

Wires [Loop Engine](https://loopengine.io) into OpenClaw so that any workflow
step can be governed by:

- **Human approval gates** — transitions only a named human actor can trigger
- **AI confidence guards** — block AI recommendations below a threshold
- **Evidence capture** — attach structured context to every decision
- **Audit trail** — every transition is attributed, timestamped, and immutable

## How it works with OpenClaw

```
OpenClaw agent proposes action
        ↓
Loop Engine evaluates guards       ← @loop-engine/adapter-openclaw
        ↓
Human approves (if policy requires)
        ↓
OpenClaw executes the approved action
```

Guards are enforced at the runtime level — not in prompts.

## How governance weighting works

Three types of weighting evaluated in sequence — all must pass:

**1. Confidence threshold (numeric gate)**
Every AI actor submission carries a 0–1 confidence score. The guard blocks
the transition if the score falls below the configured threshold.

**2. Guard priority (hard vs soft)**
Hard failures block the transition regardless of everything else.
A human-only guard is an absolute block — no confidence score overrides it.

**3. Evidence completeness (structural gate)**
The evidence-required guard checks for specific fields before allowing a
transition. Missing any required field blocks the transition.

**Evaluation order:**
```
1. Actor authorized for this signal?
2. Required evidence fields present?
3. Confidence score above threshold?
4. All hard guards pass?
```

## Quick start (no API key required)

```typescript
import { createLoopSystem, parseLoopYaml, CommonGuards, guardEvidence } from '@loop-engine/sdk'
import { MemoryAdapter } from '@loop-engine/adapter-memory'

const definition = parseLoopYaml(`
  loopId: approval.workflow
  name: Approval Workflow
  version: 1.0.0
  initialState: pending
  states:
    - stateId: pending
      label: Pending Approval
    - stateId: approved
      label: Approved
      terminal: true
  transitions:
    - transitionId: approve
      from: pending
      to: approved
      signal: approve
      allowedActors: [human]
      guards: [human-only]
`)

const system = createLoopSystem({
  storage: new MemoryAdapter(),
  guards: CommonGuards,
})

const loop = await system.startLoop({ definition, context: {} })

// Only a human actor can approve — AI and automation actors are blocked.
// guardEvidence strips PII fields and prompt-injection patterns before
// the evidence object is forwarded to any external LLM adapter.
await system.transition({
  loopId: loop.loopId,
  signalId: 'approve',
  actor: { id: 'alice', type: 'human' },
  evidence: guardEvidence({ reviewNote: 'Looks good' }),
})
```

## Examples included

| File | Provider | API key |
|---|---|---|
| `example-expense-approval.ts` | None | Not required |
| `example-ai-replenishment-claude.ts` | Anthropic Claude | `ANTHROPIC_API_KEY` |
| `example-infrastructure-change-openai.ts` | OpenAI GPT-4o | `OPENAI_API_KEY` |
| `example-fraud-review-grok.ts` | xAI Grok 3 | `XAI_API_KEY` |

All examples use synthetic data. Do not use real PII or regulated data
without reviewing your provider's data processing agreements.

## Evidence sanitization

All evidence objects must be guarded before being forwarded to external LLM adapters.
`guardEvidence` (exported from `@loop-engine/sdk`) enforces three rules at the skill boundary:

1. **PII field blocking** — fields whose names match known PII patterns (`ssn`, `email`, `phone`,
   `dob`, `password`, `token`, `healthrecord`, `mrn`, and 20+ others) are dropped before forwarding.
2. **Prompt injection stripping** — string values beginning with role prefixes (`system:`, `user:`,
   `assistant:`) are stripped to prevent instruction injection via evidence payloads.
3. **Value length cap** — string values are truncated at 512 characters to prevent context stuffing.

Always wrap caller-supplied evidence with `guardEvidence()` before passing it to
`system.transition()`. The Quick Start above shows the correct pattern.

## Security notes

- Local governance mode runs without external LLM provider calls.
- Provider-backed mode requires explicit adapter activation and the corresponding API key.
- Evidence and prompt context can leave the local environment only in provider-backed mode.
- This skill does not claim compliance certifications or data-processing guarantees.

## Documentation

https://loopengine.io/docs/integrations/openclaw

## License

MIT-0 — free to use, modify, and redistribute. No attribution required.

`@loop-engine/*` packages: Apache-2.0
Provider SDKs: licensed by their respective maintainers