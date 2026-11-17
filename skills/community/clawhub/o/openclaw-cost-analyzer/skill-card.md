## Description:

Analyzes OpenClaw token usage and cost, identifies high-consumption patterns such as long conversations, frequent cron activity, and large context, and provides concrete optimization suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to analyze local OpenClaw usage logs, produce cost reports, and identify model, context, cron, and session-management changes that may reduce spend.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local OpenClaw conversation or session logs may contain sensitive prompts, project details, or usage patterns.

Mitigation: Run the skill only when comfortable granting local read access to those logs, and review generated reports before sharing them.

Risk: The full analysis command writes a cost report under the OpenClaw memory directory.

Mitigation: Confirm the report destination and contents are appropriate for the workspace before relying on or distributing the output.

Risk: Model-switching, cron, and cleanup examples can affect future workflow behavior if copied without review.

Mitigation: Treat suggested commands as manual recommendations, review them before execution, and remove recurring cron jobs when they are no longer intended.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/openclaw-cost-analyzer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Console text and Markdown cost report with suggested shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes a local cost-analysis-report.md file under the OpenClaw memory directory when the full analysis command is run.]

## Skill Version(s):

1.0.0 (source: frontmatter, package.json, CHANGELOG, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
