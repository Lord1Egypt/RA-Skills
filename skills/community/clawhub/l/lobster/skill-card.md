## Description:

Lobster is a workflow runtime for AI agents that runs deterministic typed pipelines with approval gates for multi-step automation, monitoring, data processing, email triage, and workflows that should halt before side effects.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guwidoe](https://clawhub.ai/user/guwidoe)

### License/Terms of Use:


## Use Case:

Developers and agent operators use Lobster to run repeatable multi-step workflows, process typed JSON pipelines, monitor PRs or issues, and require explicit approval before side effects such as sending messages or continuing a workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad shell execution can run arbitrary commands and create side effects in the current workspace.

Mitigation: Use Lobster only in trusted workspaces, review pipelines before execution, avoid untrusted input in shell-backed workflows, and require approvals before side effects.

Risk: Credentialed remote actions through Clawdbot integration can expose or misuse CLAWD_TOKEN.

Mitigation: Scope CLAWD_TOKEN narrowly, provide it only when Clawdbot integration is needed, and review any remote-action workflow before approval.

Risk: Persistent workflow state may store sensitive data in the default state directory.

Mitigation: Set LOBSTER_STATE_DIR to a project-specific location and manage that directory according to the sensitivity of workflow state.

Risk: Installing an unpinned Lobster package version can change workflow behavior over time.

Mitigation: Review or pin the Lobster package version before installation.

## Reference(s):

- [Lobster ClawHub skill page](https://clawhub.ai/guwidoe/skills/lobster)
- [Publisher profile](https://clawhub.ai/user/guwidoe)
- [Contribution repository linked in skill documentation](https://github.com/guwidoe/lobster-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON examples, YAML workflow examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce approval tokens, JSON tool-mode envelopes, table output, and persistent state guidance depending on the selected Lobster workflow.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
