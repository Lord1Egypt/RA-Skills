## Description:

Searches and analyzes LLM benchmark results within a fixed benchmark universe, then produces evidence-based model strength and weakness reports or domain-leader summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chekhovin](https://clawhub.ai/user/chekhovin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, evaluators, and technical decision makers use this skill to compare model benchmark performance, identify domain leaders, explain benchmark meaning and trustworthiness, and produce structured reports with score provenance, caveats, and exclusions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark conclusions may be misleading if they rely on stale, ambiguous, image-extracted, vendor-reported, or methodologically defective leaderboard rows.

Mitigation: Check cited sources, exact model row names, benchmark variants, access dates, and benchmark-specific caveats before relying on the report.

Risk: The skill may guide browsing of current benchmark pages and screenshot inspection when tables are not machine-readable.

Mitigation: Use this behavior only for benchmark research, and treat image-extracted values as higher-risk until confirmed against readable source material.

## Reference(s):

- [Benchmark Source](references/benchmark-source.md)
- [Core Dimensions](references/core-dimensions.md)
- [Search Playbook](references/search-playbook.md)
- [Data Defect Warnings](references/data-defect-warnings.md)
- [Report Templates](references/report-template.md)
- [Epoch AI benchmark correlations](https://epoch.ai/data-insights/benchmark-correlations)
- [Why benchmarking is hard](https://epoch.ai/gradient-updates/why-benchmarking-is-hard)
- [Fantastic Bugs and Where to Find Them in AI Benchmarks](https://arxiv.org/abs/2511.16842)
- [Infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise)
- [Hugging Face evaluation with Inspect AI](https://huggingface.co/docs/inference-providers/guides/evaluation-inspect-ai)
- [LightEval documentation](https://huggingface.co/docs/lighteval/main/en/index)
- [Open Benchmark Index](https://huggingface.co/spaces/OpenEvals/open_benchmark_index)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Guidance]

**Output Format:** [Markdown reports with evidence tables and concise benchmark caveats]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports include scope, normalized model identity, benchmark evidence, comparisons, data-defect warnings, confidence, methodology, and exclusions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
