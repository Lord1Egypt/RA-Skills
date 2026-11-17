## Description:

Role-based GitOps skill for OpenClaw agents with junior and senior operating modes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[launchthatbot](https://clawhub.ai/user/launchthatbot)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineering teams use this skill to coordinate junior and senior OpenClaw agents in GitHub repositories, with junior agents limited to branch and PR work and senior agents handling review, merge, release, and workflow setup tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful GitHub credentials and repository write workflows.

Mitigation: Review the authentication flow before installation, prefer managed short-lived GitHub App tokens, and avoid pasting private keys or PATs into chat.

Risk: Repository automation templates can grant write permissions for senior release control.

Mitigation: Reduce release workflow permissions until real release steps require them, enforce branch protection, and require CI to pass before merge.

Risk: Onboarding tokens, private keys, and PATs could be exposed if logged or persisted.

Mitigation: Treat onboarding tokens as session-only secrets, do not print secrets in logs, and do not write secrets into repository files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/launchthatbot/skills/launchthatbot-git-team-ops)
- [LaunchThatBot Website](https://launchthatbot.com)
- [LaunchThatBot Discord](https://discord.gg/launchthatbot)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with role-specific status, repository and branch details, changed-file summaries, approval steps, and inline commands or configuration paths when needed.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Prompts for role, repository, and authentication mode before operating; reports the selected junior or senior mode.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter and package.json report 0.1.3)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
