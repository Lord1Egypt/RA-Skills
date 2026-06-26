---
name: provider-probe
description: |
  Probe and verify whether an OpenAI-compatible baseURL is a real single-model endpoint or a multi-model aggregation pool. Use when auditing model providers, checking /models output, comparing completions vs responses support, validating claimed model IDs like gpt-5.4, or producing a provider trust/stability report for OpenClaw routing decisions.
---

# Provider Probe

Use this skill to investigate model providers behind OpenAI-compatible base URLs.

## When to use
Trigger this skill when the user asks to:
- verify whether a provider's claimed model is real
- inspect a baseURL for hidden/mixed model pools
- compare multiple providers for the same claimed model
- determine whether a provider is better suited as primary or fallback
- create a trust/stability report for model routing

## Core method
Always use a layered evidence approach:
1. Read provider config or ask for baseURL + apiKey + claimed model id.
2. Call `/models` and inspect whether the returned pool contains mixed vendors or suspicious aliases.
3. Check metadata like `owned_by`, model naming conventions, and whether one baseURL exposes many unrelated model families.
4. Probe both `/responses` and `/chat/completions` with minimal prompts.
5. Run short capability tests and repeated stability tests.
6. Summarize with a confidence rating rather than absolute certainty.

## Confidence labels
- **High confidence real / most likely genuine**: stable, coherent endpoint behavior, believable output structure, low ambiguity.
- **Medium confidence / likely routed or wrapped**: works, but signs suggest aggregation, aliasing, or proxy adaptation.
- **Low confidence / unusable now**: 404, repeated timeout, incompatible shape, or too little evidence.

## Output contract
Always report:
- 当前做到哪了 / what was tested
- 当前阻塞点 / what remains uncertain
- 下一步动作 / recommended next step

For final results, include:
1. Config facts
2. `/models` findings
3. Endpoint compatibility findings
4. Repeated stability findings
5. Capability/format findings
6. Final trust judgment
7. Recommendation: primary / fallback / avoid

## Tooling
Prefer the bundled script for deterministic testing:
- `scripts/provider_probe.py`

Usage:
```bash
python3 scripts/provider_probe.py --config /root/.openclaw/openclaw.json --providers ypemc omgteam vpsai --model gpt-5.4
```

Or probe a custom URL directly:
```bash
python3 scripts/provider_probe.py --base-url https://example.com/v1 --api-key sk-xxx --model gpt-5.4
```

## Interpretation heuristics
Treat a provider as a likely aggregation pool when several of these appear together:
- `/models` returns many unrelated model families
- `owned_by` values are mixed or inconsistent
- the claimed model id looks like a routing alias rather than a canonical model id
- `/responses` and `/chat/completions` compatibility is uneven or surprising
- behavior is stable enough to work but not coherent enough to look like a single official upstream

## Files
- Reference checklist: `references/provider-probe-checklist.md`
- Probe script: `scripts/provider_probe.py`
