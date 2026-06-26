# NanoGPT Provider Plugin — Project Plan

> **Goal:** Build an OpenClaw provider plugin (`@openclaw/nano-gpt`) that handles auth, dynamic model catalog, and usage tracking via nano-gpt.com's API.

---

## Background

NanoGPT is an AI model aggregator/router with an OpenAI-compatible API. It already works with OpenClaw via manual JSON config (see `docs/06-openclaw-existing-integration.md`), but requires users to hardcode model lists and manually configure capabilities/costs.

**Why a plugin?**
- Dynamic model catalog from `/api/v1/models?detailed=true` — no stale hardcoded lists
- Auto-populate `reasoning`, `vision`, `context_window`, `max_tokens`, `pricing` from API
- First-class `NANOGPT_API_KEY` env var detection + `openclaw onboard` flow
- Usage tracking via `/api/subscription/v1/usage` (daily/monthly limits)
- Balance checking via `/api/check-balance`
- Support all nano-gpt model families: OpenAI, Anthropic, Google, xAI, DeepSeek, Moonshot, Qwen, Groq, and 50+ more

---

## Scope

### In Scope (v1)
1. **Auth** — API key (`NANOGPT_API_KEY`), Bearer token format, `openclaw onboard --nano-gpt-api-key` flow
2. **Dynamic model catalog** — Fetch from `GET /api/v1/models?detailed=true` with API key, map to OpenClaw model objects
3. **Dynamic model resolution** — Accept arbitrary `nano-gpt/<model-id>` refs via `resolveDynamicModel`
4. **Usage tracking** — `fetchUsageSnapshot` from `/api/subscription/v1/usage` + balance from `/api/check-balance`
5. **Documentation** — Provider doc page at `docs/providers/nano-gpt.md` + plugin README

### Out of Scope (v1)
- Custom provider selection (NanoGPT's `X-Provider` header routing)
- TEE attestation
- Image/video generation (separate capability registration)
- OAuth device login flow (API key is sufficient)
- Multi-key / key rotation

---

## Technical Decisions

### Provider ID
`nano-gpt` — matches the canonical service name. Model refs: `nano-gpt/openai/gpt-5.2`, `nano-gpt/anthropic/claude-opus-4.6`.

### Base URL
- Canonical: `https://nano-gpt.com/api/v1`
- Subscription-only requests use `/api/subscription/v1` (handled by nano-gpt server-side based on account)
- Alt domains available but not needed in plugin (nano-gpt routes correctly by model ID)

### API Compatibility
- `api: "openai-completions"` — standard OpenAI-compatible endpoint, no special headers needed beyond `Authorization: Bearer`

### Model Cost
NanoGPT returns `pricing.prompt` and `pricing.completion` in $/million tokens. Map directly to OpenClaw's `cost.input` / `cost.output`. `cacheRead`/`cacheWrite` not charged by NanoGPT at this layer — set to `0`.

### Context Window / Max Tokens
NanoGPT returns `context_length` (max input) and `max_output_tokens`. Use these directly.

### Capabilities
Map NanoGPT `capabilities` object to OpenClaw model `input`/`reasoning` flags:
- `vision: true` → `input: ["text", "image"]`
- `reasoning: true` → `reasoning: true`
- Default: `input: ["text"]`

### Env Var
`NANOGPT_API_KEY`

### Auth Flow
1. User runs `openclaw onboard --nano-gpt-api-key <key>`
2. Plugin stores key in `env.NANOGPT_API_KEY`
3. Catalog fetch uses it to get user-specific pricing

---

## File Structure

```
extensions/nano-gpt/               # In-repo development path
  OR
@openclaw/nano-gpt/              # npm package path (published)

├── package.json
├── openclaw.plugin.json
├── index.ts                      # defineSingleProviderPluginEntry
└── src/
    ├── provider.test.ts
    └── usage.ts                  # fetchUsageSnapshot + fetchBalance
```

---

## Implementation Phases

### Phase 1 — Skeleton + Static Provider
- [ ] Set up `package.json` + `openclaw.plugin.json`
- [ ] Implement `defineSingleProviderPluginEntry` with hardcoded model list (1-2 models)
- [ ] **Test:** Provider registration — `describe("acme-ai provider")`, `it("resolves dynamic models")`, `it("returns catalog when API key is available")`, `it("returns null catalog when no key")`
- [ ] **Test:** Auth method — verify `resolveProviderApiKey` returns correct shape
- [ ] Verify `openclaw onboard --nano-gpt-api-key` flow works
- [ ] Verify chat completions work end-to-end

### Phase 2 — Dynamic Catalog
- [ ] Replace hardcoded models with `catalog.run()` fetching `GET /api/v1/models?detailed=true`
- [ ] Map all NanoGPT model fields to OpenClaw model schema
- [ ] Handle `vision`, `reasoning`, `context_length`, `max_output_tokens`, `pricing`
- [ ] Handle missing/null fields gracefully (default safe values)
- [ ] **Test:** Catalog fetch returns correct model count and field mapping for known NanoGPT response shape
- [ ] **Test:** Defensive mapping — handles null `capabilities`, null `pricing`, missing `max_output_tokens`
- [ ] **Test:** Catalog returns `null` when API key is absent (not an error)

### Phase 3 — Dynamic Model Resolution
- [ ] Add `resolveDynamicModel` to accept arbitrary model IDs (needed for any model ref a user types)
- [ ] Fall back to conservative defaults for unknown model capabilities
- [ ] **Test:** `resolveDynamicModel` returns correct shape for arbitrary model ID
- [ ] **Test:** Unknown model gets safe defaults (text-only, no reasoning, 128k context)

### Phase 4 — Usage Tracking
- [ ] Implement `resolveUsageAuth` + `fetchUsageSnapshot` from `/api/subscription/v1/usage`
- [ ] Implement `fetchBalance` from `/api/check-balance`
- [ ] Wire into OpenClaw's `session_status` display
- [ ] **Test:** `fetchUsageSnapshot` parses daily/monthly usage JSON correctly
- [ ] **Test:** `fetchBalance` returns correct USD balance shape
- [ ] **Test:** `resolveUsageAuth` returns null when no API key is set

### Phase 5 — Documentation + Polish
- [ ] Write `docs/providers/nano-gpt.md` (OpenClaw provider doc)
- [ ] Add `README.md` with install + quick-start
- [ ] Package and test install from npm

---

## Key Risks

| Risk | Likelihood | Mitigation |
|---|---|---|
| NanoGPT model API changes schema | Low | Map defensively; log unknown fields |
| NanoGPT auth token format differs in edge cases | Low | Test with both `sk-nano-` and legacy UUID keys |
| Dynamic catalog slows down model listing | Medium | Cache catalog for session duration; do not refetch on every request |
| NanoGPT subscription vs pay-as-you-go routing confusion | Medium | Document the two base URLs; plugin uses canonical `/api/v1` |
| Model IDs contain slashes (`anthropic/claude-opus-4.6`) — splitting for provider ID | High | NanoGPT already uses `provider/model` format; no splitting needed |

---

## Testing Reference

Every phase includes inline test checklist items (above). The testing pattern follows the OpenClaw SDK exactly:

```typescript
import { describe, it, expect, vi } from "vitest";

describe("nano-gpt provider", () => {
  it("resolves dynamic models", () => {
    const model = provider.resolveDynamicModel!({
      modelId: "custom-model-v2",
    } as any);
    expect(model.id).toBe("custom-model-v2");
    expect(model.provider).toBe("nano-gpt");
  });

  it("returns catalog when API key is available", async () => {
    const result = await provider.catalog.run({
      resolveProviderApiKey: () => ({ apiKey: "test-key" }),
    } as any);
    expect(result?.provider?.models).toHaveLength(2);
  });
});
```

For mocking the runtime in isolated unit tests:
```typescript
import { createPluginRuntimeStore } from "openclaw/plugin-sdk/runtime-store";
import type { PluginRuntime } from "openclaw/plugin-sdk/runtime-store";

const store = createPluginRuntimeStore<PluginRuntime>("test");
const mockRuntime = { agent: { resolveAgentDir: vi.fn() }, config: { ... } } as unknown as PluginRuntime;
store.setRuntime(mockRuntime);
// tests...
store.clearRuntime();
```

Run: `pnpm test -- tests/provider.test.ts`

---

## Open Questions for Brian

1. **Package name:** `@openclaw/nano-gpt` or `@openclaw/provider-nano-gpt`? (Check OpenClaw convention)
2. **In-repo vs npm publish:** Should this live in the OpenClaw repo (`extensions/nano-gpt/`) or be a standalone npm package?
3. **Subscription vs pay-as-you-go:** NanoGPT has two routing paths (`/api/v1` vs `/api/subscription/v1`). Should the plugin expose both, or just canonical?
4. **Catalog caching:** Should catalog refresh be on-demand (first use) or on a schedule (e.g., daily)?
5. **Key question:** Does Brian want me to scaffold and implement Phase 1-3 now, or just the plan + research so he can review before coding?
