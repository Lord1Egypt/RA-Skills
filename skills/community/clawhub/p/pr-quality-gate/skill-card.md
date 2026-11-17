## Description:

PR Quality Gate coordinates structured pull request review, AI-assisted fix suggestions, and GitHub Issue tracking so code is checked before merge.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zlszhonglongshen](https://clawhub.ai/user/zlszhonglongshen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to review pull requests, identify quality and security issues, create tracking issues, request fix suggestions for high-severity findings, and produce merge guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can change GitHub repository state through issue creation, PR comments, statuses, or merge-related actions.

Mitigation: Require clear user approval for repository write actions and confirm the target repository and pull request before executing them.

Risk: The workflow can invoke kimi-cli, which may share code or security findings with a third-party service.

Mitigation: Use the external CLI only where third-party code sharing is permitted, and avoid sending secrets or sensitive repository content.

Risk: Automated review and fix suggestions may be incomplete or incorrect.

Mitigation: Have a reviewer validate high-severity findings, generated code snippets, and final merge guidance before relying on the gate outcome.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zlszhonglongshen/skills/pr-quality-gate)
- [Skill README](artifact/README.md)
- [Workflow Manifest](artifact/workflow.json)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown review report with issue links, gate status, and optional code snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce GitHub Issue IDs and PR comment or status links when repository write actions are approved.]

## Skill Version(s):

1.0.0 (source: release metadata and workflow.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
