## Description:

ModelPilot helps agents test, compare, promote, replace, and clean up local Ollama models using repeatable two-round benchmarks, no-think checks, and local-only safety boundaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[patmenciu](https://clawhub.ai/user/patmenciu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate installed local Ollama models on repeatable task prompts, no-think behavior, structured output stability, and replacement readiness. It supports local workflow decisions without cloud APIs, uploads, model downloads, or automatic model deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Benchmark reports can overstate replacement readiness because mechanical checks do not prove semantic quality.

Mitigation: Require human semantic review and two clean benchmark rounds before replacing a workflow model; keep the previous model and configuration available for rollback.

Risk: Prompts, logs, or benchmark outputs may contain sensitive local data if real files are used.

Mitigation: Use fictional prompt sets by default, only use user-named files for the task, and keep benchmark outputs local.

Risk: No-think model names or instructions may not guarantee clean output.

Mitigation: Check outputs for thinking traces and avoid promoting a model into automation when leakage appears.

Risk: Untrusted or edited benchmark JSON can produce misleading reports.

Mitigation: Review benchmark inputs and reports manually, and rerun benchmarks from trusted model and prompt configurations when results affect replacement decisions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/patmenciu/skills/modelpilot)
- [README](README.md)
- [Example Benchmark Report](outputs/example_report.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional shell commands, JSON benchmark results, and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local-only Ollama workflow; benchmark scripts use installed models and fictional or explicitly selected prompt files.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
