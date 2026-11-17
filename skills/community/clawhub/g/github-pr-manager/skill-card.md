## Description:

GitHub PR Manager helps an agent manage pull request lifecycles, including PR setup, CI monitoring, review handling, issue replies, and follow-up until merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[godnight](https://clawhub.ai/user/godnight)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to delegate routine GitHub pull request management, including status checks, reviewer feedback triage, small fixes, comments, and tracking until the PR is merged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent PR automation may use broad GitHub credentials for repository-changing actions.

Mitigation: Use an existing gh login or a short-lived fine-grained token limited to the target repository, and require explicit manual approval for commits, pushes, force-pushes, workflow changes, scheduled jobs, and public replies.

Risk: Scheduled PR tracking can continue after it is no longer needed.

Mitigation: Avoid or remove cron-based tracking unless there is a clear cleanup plan, and disable tracking when the PR closes or merges.

Risk: Prepared reviewer replies or issue comments may be posted publicly on behalf of the user.

Mitigation: Review comment text and target threads before posting, especially when the skill suggests clarifications, disagreement, or maintainer-facing requests.

## Reference(s):

- [GitHub PR management workflow](references/workflow.md)
- [PR reply templates](references/templates.md)
- [GitHub PR Manager on ClawHub](https://clawhub.ai/godnight/skills/github-pr-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, GitHub CLI/API examples, status summaries, and prepared PR comments]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs can include repository-changing commands and public reply text, so users should review them before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
