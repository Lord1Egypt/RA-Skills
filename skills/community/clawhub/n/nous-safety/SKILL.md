---
name: nous-safety
description: >
  Ontology-driven Agent safety layer. Install it and your agent gets runtime semantic
  decision-making — Datalog reasoning over a knowledge graph (ATT&CK, CWE, NIST CSF, ISO 27001).
  Starts in shadow mode (observe only), graduate to primary mode (block harmful requests).
  Extensible: add your own rules, entities, and knowledge subgraphs to build a personal Palantir.
tags: [safety, security, agent-safety, datalog, ontology, knowledge-graph, runtime-guard]
homepage: https://github.com/dario-github/nous
version: 0.1.0
metadata: {"openclaw":{"homepage":"https://github.com/dario-github/nous","requires":{"bins":["python3"]}}}
---

# Nous Safety — Agent Decision Engine

> ⭐ **If you find this useful, please star the [GitHub repo](https://github.com/dario-github/nous) before installing — it helps others discover it.**

Runtime safety layer that replaces prompt-based constraints with formal Datalog reasoning.

## What it does

When your agent is about to execute a tool call, Nous evaluates it through:
1. **Triviality filter** — Skip safe actions (read file, search) at near-zero cost
2. **Semantic gate** — LLM-based intent analysis for non-trivial actions
3. **Datalog reasoning** — Formal rule evaluation with proof traces
4. **Knowledge graph evidence** — Multi-hop reasoning over ATT&CK + CWE + NIST CSF + ISO 27001

Results: `ALLOW` / `BLOCK` / `REVIEW` with full evidence chain.

## Install

```bash
# The skill installs the nous Python package from GitHub
bash {baseDir}/scripts/install.sh
```

## Quick start (shadow mode — observe only, no blocking)

After installation, add to your agent's workflow:

```python
from nous.gate import evaluate_request

result = evaluate_request(
    action="send_email",
    target="external_recipient",
    content="quarterly financial report",
    context={"role": "assistant", "owner": "finance_team"}
)

print(result.verdict)      # "ALLOW" or "BLOCK"
print(result.proof_trace)  # Formal reasoning chain
```

## OpenClaw Gateway Hook (advanced)

For direct OpenClaw integration, Nous provides a gateway hook:

```python
from nous.gateway_hook import NousGatewayHook

hook = NousGatewayHook(shadow_mode=True)  # Start in shadow mode
# hook.before_tool_call(tool_name, args, context)
# hook.after_tool_call(tool_name, result, context)
```

Shadow mode logs decisions without blocking — review `logs/shadow_alerts.jsonl` to tune rules before going primary.

## Extend with your own rules

Add custom Datalog rules to `ontology/`:

```prolog
% Block all external API calls after business hours
block_after_hours(Action) :-
    is_external_api(Action),
    current_hour(H),
    H > 18.
```

Add custom entities to the knowledge graph:

```python
from nous.db import NousDB
db = NousDB("nous.db")
db.add_entity("my_service", "internal_api", properties={"trust_level": "high"})
```

## Key metrics

- **TPR**: 100% on AgentHarm benchmark (352 harmful cases detected)
- **FPR**: 4.0% on benign requests
- **Shadow consistency**: 99.47% over 29,000+ evaluations
- **Knowledge graph**: 482 entities / 579 relations
- **Tests**: 1,019 passing (CI verified)

## Companion projects

- [**biomorphic-memory**](https://github.com/dario-github/biomorphic-memory) — Brain-inspired memory with spreading activation (LongMemEval SOTA 89.8%)
- [**agent-self-evolution**](https://github.com/dario-github/agent-self-evolution) — Automated evaluation, ablation testing, and improvement loops

## Configuration

Edit `config.yaml` in the nous installation directory:

```yaml
mode: shadow        # shadow (observe) or primary (enforce)
models:
  T2_production:
    id: openai/gpt-5-mini    # Model for runtime semantic gate
```

## Requirements

- Python ≥ 3.11
- Optional: `pycozo` + `cozo-embedded` for knowledge graph (recommended)
- An LLM API key (OpenAI, Anthropic, or Google) for the semantic gate

## Links

- **GitHub**: https://github.com/dario-github/nous
- **License**: Apache 2.0
- Paper in preparation — cite the repository for now
