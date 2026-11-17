## Description:

Download, configure, run, verify, and troubleshoot Insight Claw, an A-share self-selected stock analysis pipeline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[geraltjc](https://clawhub.ai/user/geraltjc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, engineers, and analysts use this skill to set up and run Insight Claw for A-share self-selected stock analysis, verify local reports, and troubleshoot provider, credential, and notification issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs an agent to clone and run mutable remote project code with unhashed dependencies.

Mitigation: Review the upstream project state before installation, pin a reviewed commit and hashed lockfile where possible, and run in a restricted environment with only task-specific credentials.

Risk: Credential values, generated reports, notification payloads, or raw model inputs may contain sensitive information.

Mitigation: Keep secrets local to the checkout or approved secret handling, do not display or commit raw credentials, and upload reports or payloads only with explicit user approval.

Risk: Stock-analysis outputs could be mistaken for independent investment advice or automatic trading instructions.

Mitigation: Ground summaries in generated reports, keep outputs framed as decision-support material for user review, and do not describe the skill as an order-execution system.

## Reference(s):

- [Insight Claw Quickstart](references/quickstart.md)
- [Insight Claw Troubleshooting](references/troubleshooting.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local setup, credential checks, validation runs, troubleshooting, and expected report files.]

## Skill Version(s):

0.3.1 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
