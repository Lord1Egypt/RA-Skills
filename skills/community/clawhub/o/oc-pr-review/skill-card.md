## Description:

Guides an agent through a Pull Request review workflow using GitHub CLI, including change analysis, security review, test coverage review, performance assessment, code quality checks, report generation, and optional Feishu notification.

This skill is ready for commercial/non-commercial use.

## Publisher:

[penghang1223](https://clawhub.ai/user/penghang1223)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering reviewers use this skill to inspect GitHub pull requests for security, test coverage, performance, and code quality concerns, then produce a structured review report. It can also help draft or publish GitHub review comments and send Feishu summaries when the user explicitly requests those actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may access authenticated GitHub pull request data, including private repository details available to the user's GitHub CLI session.

Mitigation: Use an account with only the needed repository access and ask the agent to draft findings before taking any publishing action.

Risk: Publishing GitHub reviews, line comments, or Feishu notifications can externally share sensitive review findings.

Mitigation: Require explicit confirmation before posting review comments, requesting changes, approving a PR, or sending Feishu messages.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/penghang1223/skills/oc-pr-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown review reports with inline shell commands and checklists]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include suggested GitHub review actions or Feishu notification summaries for user confirmation.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
