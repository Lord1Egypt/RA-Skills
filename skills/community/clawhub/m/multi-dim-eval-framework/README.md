# Multi-Dimensional Evaluation Framework Designer

> Designs a multi-dimensional evaluation framework for AI systems where single-score benchmarks lose information. Use when comparing experiments/agents across qualitatively different dimensions, when canonical metrics aren't available for legacy systems, or when explaining *which* dimension drove an outcome matters more than ranking.

A Claude Skill for designing custom multi-dimensional evaluation frameworks. Built on the MADEF (Multi-Agent Deliberation Evaluation Framework) pattern, generalized to any domain where multi-output AI systems need multi-axis comparison.

## Install

### Claude Code

```bash
clawhub install multi-dim-eval-framework
```

Or manually clone:

```bash
git clone https://github.com/<org>/multi-dim-eval-framework.git ~/.claude/skills/multi-dim-eval-framework
```

### OpenClaw / Hermes / Cursor

Standard agentskills.io-compatible install per platform.

## Quickstart

Once installed, the skill activates when you describe an evaluation question with multiple qualitative axes. Example interaction:

> **You**: I have 4 multi-agent debate experiments. The latest one added claims/verification infra. How do I compare them rigorously?
>
> **AI** (with skill): *[Stage 1 elicitation]* "Let's design an evaluation framework. First, what's the question the comparison should answer? Are you asking about grounding quality (how well decisions are tied to evidence), process dynamics (how disagreement and progress evolve over rounds), or both? And which 2-3 of the experiments have you formed strong priors about? Those are our calibration cases."

The skill walks 4 stages (domain → taxonomy → rubric → judgment) producing a scorecard format calibrated to your specific evaluation question.

## What this skill does

This skill enforces a specific evaluation pattern:

1. **Group-organized**: dimensions cluster into 2-4 groups by what layer they evaluate (evidence / process / structure)
2. **Canonical/proxy duality**: every dimension has both an ideal measurement and a fallback for incomplete data
3. **Group-wise reporting (no composite)**: forbids the single-score collapse that destroys multi-dim information
4. **Failure-mode transparent**: every dimension lists conditions where its score is unreliable
5. **Calibration-first**: framework freezes only after running on known-quality instances and verifying ordinals

The pattern comes from MADEF v1, used to evaluate 4 multi-agent deliberation experiments across 12 dimensions. memory-bench-designer is a parallel instantiation of the same pattern for memory eval (4 families × 8 dimensions). Both are referenced inside the skill.

## When NOT to use

- You need a single comparable benchmark number → use HumanEval / MMLU / domain-specific benchmark, not a custom framework
- The system has a clear single quality metric (perplexity, accuracy) → no point in multi-dim
- You're not yet running comparisons across instances → the framework needs at least 2 calibration cases
- You want automated scoring → this skill produces a *scorecard format* and procedural rules, but scoring is human-in-the-loop for proxy work

## Files

```
multi-dim-eval-framework/
├── SKILL.md
├── README.md
├── LICENSE
├── references/
│   ├── group-design-principles.md   # 5 design + 5 meta-principles
│   ├── canonical-vs-proxy-decision.md
│   ├── madef-axes.md                # 12-axis reference for deliberation
│   └── memory-bench-taxonomy.md     # 4×8 alt shape for memory eval
├── examples/
│   ├── deliberation-system-eval.md  # MADEF applied to 4 experiments
│   └── cross-domain-rag-eval.md     # adapting the pattern to RAG
└── templates/
    ├── axes-design-worksheet.md     # fill-in for your own axes
    └── scorecard.md.tmpl            # output format
```

## Background

This skill captures a methodology that emerged from running multiple deliberation experiments and a separate memory-eval benchmark. The shared pattern (multi-group + canonical-explicit + group-wise reporting) was named MADEF and frozen as v1 after calibration on 4 experiments.

The skill generalizes the pattern: the 3-group structure is one instantiation, but the *principles* (no composite, canonical/proxy duality, failure-mode transparency, calibration before claims) apply to any domain where AI systems are evaluated across multiple qualitative axes.

## Versioning

Following [SemVer](https://semver.org/).

- `0.1.0` initial release with 12-axis MADEF reference, 4-family alt taxonomy, design worksheet, scorecard template, 2 examples

## License

MIT

## Contributing

Issues and PRs welcome. Particularly interested in:

- Cross-domain example contributions (adapting the pattern to your evaluation domain)
- Refinements to canonical/proxy decision rules
- Iteration log entries from real applications (what calibration revealed)
