---
name: llm-verify
description: Verify an LLM API endpoint — model authenticity, billing inflation, relay provenance, performance and silent downgrades. Use when the user asks whether the model they are paying for is genuine, whether a relay or proxy is trustworthy, whether they are being overcharged, or whether a model has been quietly downgraded. 检测 LLM API 端点的真伪、计费掺水、中转来源、性能与降智；当用户问"我用的模型是不是真的"、"这个中转站靠谱吗"、"是不是被降智了"、"计费对不对"时使用。
license: Apache-2.0
---

# llm-verify

`llm-verify` is a single-binary CLI that runs a black-box check against any LLM
API endpoint and answers what the user actually wants to know: am I getting the
model I am paying for, am I being overcharged, and how many relays sit on this
path?

## When to use this

Reach for this skill when the user asks anything like:

- "Is this relay/proxy trustworthy?" "Is this key really Claude?"
- "Has the model been downgraded?" "It feels dumber than it used to."
- "Is the billing right?" "The token counts look off."
- "Check this API endpoint for me."
- Debugging an endpoint that is slow, drops its stream, or breaks tool calls.

## How to run it

```bash
llm-verify --base-url <URL> --api-key <KEY> --model <MODEL_ID>
```

| Flag | Meaning |
|---|---|
| `--protocol anthropic\|openai` | Inferred from the URL and model name if omitted |
| `--depth fast\|balanced\|forensic` | Default `balanced`; `forensic` samples more — slower and costlier, but firmer |
| `--claimed-model <ID>` | Use when the vendor's advertised name differs from the ID you request |
| `--lang en\|zh` | Report language; follows the system locale by default |
| `-o report.html` | HTML report path |
| `--json report.json` | Also emit machine-readable JSON |
| `--no-open` | Do not open a browser |

Credentials can also come from `.env` or the environment:
`LLM_VERIFY_BASE_URL`, `LLM_VERIFY_API_KEY`, `LLM_VERIFY_MODEL`.

## Exit codes

| Code | Meaning |
|---|---|
| 0 | Clean |
| 1 | Failing score, or a suspicious / counterfeit / inconclusive verdict |
| 2 | A hard gate tripped (silent fallback, shared-pool forwarding, tier downgrade, wrapper injection, cache replay, hidden prompt, response replay) |

Suitable as a CI gate as-is.

## Reading the result

The tool reports two **independent** axes. Do not conflate them.

- **Authenticity**: genuine / genuine-with-defects / relayed / suspicious / counterfeit / inconclusive
- **Origin**: direct from vendor / cloud platform / subscription-derived / relay / reconstructed channel / undetermined

A real model behind a relay is "relayed", not "counterfeit". That is a longer
path, not a substituted model.

## Reporting back to the user

1. **Lead with the conclusion, then the evidence.** They want to know whether
   they can rely on it, not all 40 probe lines.
2. **Call out hard gates separately.** They are facts no weighted score excuses.
3. **Not tested is not passed.** Say plainly which probes were skipped.
4. **Carry the confidence across**, especially for identity: adjacent versions
   inside one tier are genuinely hard to separate, and the tool abstains when
   the evidence is thin. Do not supply a verdict it declined to give.
5. **Do not convict on the tool's behalf.** One tier apart is within sampling
   noise; the tool does not accuse there, and neither should you.

## Limits to state honestly

- Resolution stops at tier granularity (flagship / mid / light). Adjacent
  versions inside a tier cannot be separated without distribution baselines.
- The tier call depends on sampling; use `--depth forensic` when it matters.
- An injected system prompt contaminates identity fingerprints, which is why
  the contract layer runs first and downgrades identity confidence when it
  finds injection.
- It cannot prove the server-side weights are the official ones — only that
  behaviour does or does not match expectations.
- Quantised builds (int4 / fp8) can only be given a probability, never a verdict.
