## Description:

OpenClaw Smartness Eval measures an OpenClaw agent across 14 capability dimensions and produces scores, evidence, risk flags, recommendations, and trends from automated tests and workspace telemetry.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yh22e](https://clawhub.ai/user/yh22e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to evaluate OpenClaw agent capability after upgrades, during periodic self-assessment, when investigating regressions, or when preparing consistent external capability reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can execute workspace test scripts while evaluating an OpenClaw installation.

Mitigation: Install and run it only in a trusted, low-privilege or sandboxed OpenClaw workspace.

Risk: The optional LLM judge can send evaluation summaries externally and uses API credentials from the environment.

Mitigation: Leave --llm-judge disabled unless external sharing is acceptable, keep unrelated API keys out of the environment, and verify provider endpoints before enabling it.

Risk: Evaluation accuracy depends on local OpenClaw state files, scripts, and telemetry being present and representative.

Mitigation: Review generated scores, evidence, and risk flags before relying on the report for release, benchmarking, or public claims.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yh22e/skills/openclaw-smartness-eval)
- [Architecture](docs/ARCHITECTURE.md)
- [Scoring formulas](docs/SCORING.md)
- [Evaluation rubrics](config/rubrics.json)
- [Task suite](config/task-suite.json)
- [Security policy](SECURITY.md)
- [CLEAR framework](https://arxiv.org/html/2511.14136v1)
- [Anthropic agent evaluation guidance](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [JSON and Markdown reports, with optional console output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes evaluation runs, reports, and history under state/smartness-eval/; optional LLM judging can add subjective scoring when explicitly enabled.]

## Skill Version(s):

0.3.2 (source: SKILL.md frontmatter, ClawHub release evidence, artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
