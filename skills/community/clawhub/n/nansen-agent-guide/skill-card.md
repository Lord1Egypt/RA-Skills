## Description:

Routing guide -- when to use `nansen agent` (AI research) vs direct CLI data commands. Use when deciding how to answer a user's research question with Nansen tools.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this guide to choose Nansen's AI agent for research synthesis or direct CLI commands for structured data. It also explains account authentication and preference-aware product feedback workflows.

### Deployment Geography for Use:

Global, subject to Nansen's documented platform availability and geographic checks.

## Known Risks and Mitigations:

Risk: The guide includes direct Nansen data queries and may submit product feedback when the account's saved preference permits it.

Mitigation: Confirm the selected account and expected query costs before running commands; check the saved feedback preference and review report contents before relying on submission.

## Reference(s):

- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, JSON]

**Output Format:** [Markdown guidance with shell command examples and a JSON feedback example]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples can invoke Nansen account queries with their documented credit costs; feedback workflows check the account's saved preference.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
