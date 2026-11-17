## Description:

Automatically analyze and reduce OpenClaw token waste through context compression, tool-call deduplication insights, model selection guidance, and session hygiene checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mkhaytman87](https://clawhub.ai/user/mkhaytman87)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw users use this skill to analyze token consumption, plan context compression, check session health, and estimate token budgets before larger task batches.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Compressed session summaries may persist private session excerpts, customer data, personal information, proprietary code, or secrets.

Mitigation: Use explicit --session values, treat generated compressed files as confidential, and review stored summaries before sharing or reusing them.

Risk: --cleanup --apply can request an OpenClaw gateway restart when stuck sessions are detected.

Mitigation: Run cleanup in plan-only mode first and use --cleanup --apply only when a gateway restart is acceptable.

Risk: Token savings, preflight budgets, and model recommendations are heuristic estimates.

Mitigation: Use the estimates for planning and review, not as authoritative billing or model-selection decisions.

## Reference(s):

- [Token Optimizer Operating Notes](references/operating-notes.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Text reports, JSON reports, Markdown compression snapshots, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write baseline configuration, exported JSON reports, and compressed session summaries under the OpenClaw workspace when invoked with the corresponding flags.]

## Skill Version(s):

1.0.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
