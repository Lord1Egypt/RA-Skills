## Description:

LLMBooster guides an agent through a four-step Plan, Draft, Self-Critique, and Refine workflow to improve response quality for complex analysis, review, and writing tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[danlct27](https://clawhub.ai/user/danlct27)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, technical writers, and other ClawHub users use LLMBooster to structure complex prompts and improve answers for analysis, comparison, decision support, code review, and technical documentation. The skill can also expose /booster commands for status, statistics, and thinking-depth configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad analysis-style triggers may activate the workflow when a user did not intend to use it.

Mitigation: Review the trigger conditions before installation and use /booster disable or a lower thinking depth when the workflow is not wanted.

Risk: The skill may write a small local usage-statistics file.

Mitigation: Confirm local state retention is acceptable before installation, especially in environments with strict telemetry or workspace-state policies.

Risk: The disclosed /booster Python command path and inspected syntax issue may affect CLI reliability.

Mitigation: Test /booster status, stats, and depth commands in a staging workspace before relying on command handling.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/danlct27/skills/llmbooster)
- [Publisher profile](https://clawhub.ai/user/danlct27)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with optional inline shell commands and status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses prompt templates for Plan, Draft, Self-Critique, and Refine steps; optional /booster commands can change enablement, status, statistics, and thinking depth.]

## Skill Version(s):

1.7.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
