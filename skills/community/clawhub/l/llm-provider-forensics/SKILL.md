---
name: llm-provider-forensics
description: |
  Forensically verify what model family or routing layer may actually sit behind a claimed LLM endpoint or model ID. Use when an agent must investigate whether a provider is genuine, proxied, aliased, aggregated, wrapped, or currently unusable across OpenAI-compatible protocol layers, GPT/OpenAI, Anthropic/Claude, Google Gemini, GLM/Zhipu, Qwen/Tongyi, Kimi/Moonshot, MiniMax, DeepSeek, and mixed compatibility gateways. Supports deeper family-fingerprint analysis, long-context tests, structured-output stress, refusal and variance profiling, streaming/error clues, repeated stability checks, and cross-provider comparison reports.
---

# LLM Provider Forensics

Agent-facing forensic skill for identifying what an LLM endpoint most likely is.

## Trigger conditions
Use this skill when asked to:
- verify whether a claimed model is genuine
- identify which family an endpoint most resembles
- distinguish focused route vs wrapped route vs aggregation pool
- compare multiple providers claiming to expose the same model
- evaluate primary/fallback/avoid decisions
- deeply audit suspicious gateways for GPT / Claude / Gemini / GLM / Qwen / Kimi / MiniMax / DeepSeek behavior

## Core rule
Do not output false certainty. Produce a confidence-based operational judgment.

## Coverage
Families:
- OpenAI-compatible protocol layer
- GPT / OpenAI-style
- Claude / Anthropic-style
- Gemini / Google-style
- GLM / Zhipu-style
- Qwen / Tongyi-style
- Kimi / Moonshot-style
- MiniMax-style
- DeepSeek-style
- mixed aggregation pool / compatibility gateway

Dimensions:
- catalog topology
- protocol compatibility
- response schema shape
- repeated stability
- strict formatting control
- family fingerprinting
- long-context retention
- structured-output stress
- refusal/safety style
- randomness / variance profile
- streaming / error fingerprints
- cross-protocol consistency

**Current implementation note:**
- `openai-compatible` now means **protocol layer only**, not GPT-family proof.
- The deepest automatic suite is strongest for **OpenAI-compatible / mixed gateway** providers.
- Anthropic-native and Gemini-native routes currently have solid protocol/family checks, plus native deep tests, but protocol success alone must not be read as family proof.
- Treat all family conclusions as confidence-based and inspect references before overclaiming.

## Investigation workflow
1. Identify likely protocol family or families.
2. Probe catalog/list endpoints when available.
3. Probe minimal inference endpoints for each plausible protocol family.
4. Separate **protocol-layer conclusion** from **suspected model family conclusion**.
5. Run repeated stability tests on the best working route.
6. Run strict formatting tests.
7. Run deeper advanced dimensions when the user prioritizes realism over speed.
8. Inspect family fingerprint evidence and produce a confidence-based judgment.

## References to load as needed
- Main checklist: `references/forensics-checklist.md`
- Advanced dimensions: `references/advanced-dimensions.md`
- Error/stream/variance: `references/error-stream-variance.md`
- Protocol specifics: `references/protocol-openai.md`, `references/protocol-anthropic.md`, `references/protocol-gemini.md`, `references/protocol-glm.md`
- Family fingerprints: `references/fingerprint-*.md`
- Native deep tests: `references/deep-claude.md`, `references/deep-gemini.md`

## Final labels
- `high-confidence-focused-or-genuine-route`
- `medium-confidence-likely-routed-or-wrapped`
- `high-confidence-multi-model-aggregation-pool`
- `low-confidence-or-unusable`

Use `high-confidence-focused-or-genuine-route` sparingly. It should require:
- stable repeated success
- no strong mixed-pool signal
- coherent family fingerprint
- and no obvious gateway-normalization red flags in deep tests

## Agent output contract
Return sections in this order:
1. Declared facts
2. Availability status
3. Protocol-layer findings
4. Suspected model-family findings
5. Stability findings
6. Capability/format findings
7. Advanced-dimension findings
8. Final judgment
9. Need-human-review items
10. Recommended operational posture

## Preferred execution
```bash
python3 scripts/llm_provider_forensics.py --config /root/.openclaw/openclaw.json --providers omgteam ypemc vpsai --model gpt-5.4 --deep
```

