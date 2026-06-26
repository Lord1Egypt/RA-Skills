---
name: julia-openclaw-token-optimizer
description: Julia's OpenClaw Token Optimizer: Scans LLM prices, benchmarks models, patches config for cheapest optimal. Use for cost optimization, model rotation.

# Usage

1. session_status → current model/cost.
2. web_search 'current LLM pricing [provider] input/output per million tokens'.
3. gateway config.schema.lookup 'agents.defaults.modelSelection'.
4. Benchmark: spawn subagent with test prompts on cheap models.
5. Recommend: Cost/speed/quality matrix.
6. gateway config.patch {modelSelection: {primary: 'best-cheap-model'}}.

References: [providers.md](providers.md) for price APIs.

## Optimization Rules
- Prefer fast/cheap for simple tasks.
- Quality for creative/complex.
- Rotate on rate limits.

Example: 'Optimize my config for cheap reasoning' → Search prices, patch.