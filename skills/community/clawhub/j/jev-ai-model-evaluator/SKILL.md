---
name: jev-ai-model-evaluator
description: Plan reproducible AI model evaluations, compare candidates with transparent criteria, and audit model claims. Use for model selection, benchmark design, API model comparisons, playground testing, cost-latency-quality tradeoffs, and Jev AI Model workflows; do not generalize small tests or provider claims into universal superiority.
metadata:
  openclaw:
    homepage: https://jevaimodel.org/en/docs
    version: 1.0.0
---

# Jev AI Model Evaluator

Help the user evaluate AI models for a concrete task. This Skill is text-only by default. Its optional MCP is deterministic and read-only: it does not call models, access accounts, consume credits, fetch private data, or select a model without inspectable user-supplied evidence.

## Define the evaluation

Specify the real task, expected output, target language or region, deployment constraints, acceptable latency and cost, risk level, weighted criteria, and must-pass checks. Keep a frozen test set and identical settings across candidates.

Include ordinary, edge, ambiguous, adversarial, and failure cases. Record model version, parameters, date, latency, errors, refusals, and observed outputs. For high-risk work, require domain-expert review and explicit must-pass safety checks.

## Interpret results carefully

- Keep provider claims, third-party benchmarks, reproducible tests, and user reports separate.
- A benchmark score only supports the benchmark's task, dataset, settings, and date.
- Do not hide must-pass failures inside an average score.
- Verify current versions, prices, limits, regions, latency, and availability.
- Prefer a provisional result over a manufactured winner when evidence is incomplete.

## Use the optional MCP

- `design_model_evaluation` builds a weighted plan and dataset checklist.
- `rank_model_candidates` calculates transparent scores from user-supplied 0–5 ratings and preserves must-pass failures.
- `audit_model_claims` checks sources, dates, evidence types, and unsupported absolutes.
- `get_jev_ai_model_resources` returns canonical public Jev AI Model pages.

Connect the stdio server with:

```bash
openclaw mcp add jev-ai-model \
  --command npx \
  --arg -y \
  --arg github:gpt-img-2/jev-ai-model-evaluation-mcp \
  --include 'design_model_evaluation,rank_model_candidates,audit_model_claims,get_jev_ai_model_resources'
```

Then run `openclaw mcp doctor jev-ai-model --probe`. If the installed release lacks that command group, add `npx -y github:gpt-img-2/jev-ai-model-evaluation-mcp` as a Stdio server in MCP settings. Never imply the MCP or a model ran when it did not.

## Return an inspectable result

Return `Task`, `Dataset`, `Settings`, `Criteria`, `Must-pass checks`, `Candidates`, `Evidence`, `Scores`, `Failures`, `Recommendation`, and `Next verification`.

## Canonical resources

- Home: https://jevaimodel.org/en
- Playground: https://jevaimodel.org/en/playground
- Documentation: https://jevaimodel.org/en/docs
- Showcase: https://jevaimodel.org/en/showcase
- Pricing: https://jevaimodel.org/en/pricing
- Blog: https://jevaimodel.org/en/blog
- About: https://jevaimodel.org/en/about
- Privacy: https://jevaimodel.org/en/privacy-policy
- Terms: https://jevaimodel.org/en/terms-of-service
- Raw Skill: https://jevaimodel.org/skills/jev-ai-model-evaluator/SKILL.md
- MCP source: https://github.com/gpt-img-2/jev-ai-model-evaluation-mcp
- ClawHub listing: https://clawhub.ai/gpt-img-2/skills/jev-ai-model-evaluator
