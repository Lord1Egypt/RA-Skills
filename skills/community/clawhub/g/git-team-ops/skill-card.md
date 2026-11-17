## Description:

Role-based GitOps skill for OpenClaw agents with junior and senior operating modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[launchthatbot](https://clawhub.ai/user/launchthatbot)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to coordinate OpenClaw coding agents in GitHub repositories with junior PR-only roles and senior review, merge, release, and workflow-management roles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The senior release workflow template grants repository write permissions before concrete release logic is implemented.

Mitigation: Review copied workflow templates before installation and reduce senior release workflow permissions to read-only until write access is required.

Risk: Unreviewed workflow actions or installer commands may change repository automation behavior.

Mitigation: Pin actions/checkout and the ClawHub installer to reviewed versions before deploying into sensitive repositories.

Risk: Long-lived personal access tokens increase exposure if credentials are logged or stored.

Mitigation: Prefer short-lived GitHub App installation tokens, avoid printing secrets, and do not write secrets into repository files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/launchthatbot/skills/git-team-ops)
- [LaunchThatBot Website](https://launchthatbot.com)
- [Package Repository URL](https://github.com/launchthatbot/git-ops.git)
- [Discord Support](https://discord.gg/launchthatbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands, file paths, GitHub workflow configuration, and action summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports role mode, repository, branch, changed files or workflows, and the next required human approval step.]

## Skill Version(s):

0.1.5 (source: frontmatter, package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
