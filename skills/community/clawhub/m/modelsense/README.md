# ModelSense

> The right model for the right job.

ModelSense is an OpenClaw skill that recommends the optimal LLM model and effort level for any task. Unlike cost routers that always pick the cheapest model, ModelSense picks the **most capable** model for your specific task — then lets you choose how much quality you want to buy.

## What it does

Tell ModelSense what you're trying to do. It figures out:
- What type of task it is (code, reasoning, writing, math, long-context…)
- Which benchmarks are most relevant (HumanEval, GPQA, MATH, SWE-bench…)
- Which of your configured providers has the best model for this
- What effort level fits (quick / balanced / deep / research)

Then it gives you a ranked recommendation with a plain-English explanation of *why*.

## vs ClawRouter

| | ClawRouter | ModelSense |
|---|---|---|
| Goal | Cheapest model that *can* handle the job | Model that *excels* at this class of problem |
| Routing | Automatic, every request | On-demand advisory |
| Basis | 15-dimension heuristic rules | Benchmark data + task analysis |
| Payment | USDC wallet required | Uses your existing providers |
| Transparency | Shows routing tier | Explains benchmark reasoning |

They're complementary. ModelSense helps you choose; ClawRouter helps you route.

## Usage

Just ask in natural language:
```
Which model should I use to audit this Solidity contract?
What's the best setup for writing a research paper?
Use the best model for this task: [your task]
```

ModelSense can also **auto-switch** your session model or **delegate** to a sub-agent running the recommended model.

## Effort Levels

| Level | Quality | Cost | Use when |
|-------|---------|------|----------|
| `quick` | Good enough | $ | Fast summaries, classification, drafts |
| `balanced` | High | $$ | Most everyday tasks (default) |
| `deep` | Best + thinking | $$$ | Complex reasoning, code audits |
| `research` | Maximum | $$$$ | No quality/cost tradeoff |

## Data

- `data/benchmarks.yaml` — Benchmark definitions, what they measure, which models lead
- `data/models.yaml` — Model catalog with benchmark strengths, cost, context window

### Keeping data fresh

Model pricing is updated automatically every Monday via GitHub Actions.
Benchmark data is updated manually with each model release.

## Install

```bash
# Add to your OpenClaw skills path
ln -s /path/to/modelsense ~/.agents/skills/modelsense
```

Or via ClawHub (coming soon):
```bash
clawhub install modelsense
```

## License

MIT
