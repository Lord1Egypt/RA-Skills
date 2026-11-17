## Description:

Growth Engineer for mobile apps and agent runtimes including OpenClaw and Hermes. Correlate analytics, crashes, billing, feedback, store signals, and repo context into proposal drafts that can flow into agent chat, GitHub issues, or draft pull requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wotaso-dev](https://clawhub.ai/user/wotaso-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and product teams use this skill to collect mobile app growth, stability, monetization, store, feedback, and repository signals, then turn them into proposal drafts for agent chat, GitHub issues, or draft pull requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can install or update local code and helper CLIs.

Mitigation: Use a dedicated workspace and least-privileged OS user, and review or disable self-update behavior when reproducible reviewed code is required.

Risk: The skill can run on a schedule and perform recurring automation.

Mitigation: Review configured cron or scheduler entries before enabling unattended runs, and keep the runner scoped to the intended workspace.

Risk: The skill handles valuable provider credentials for analytics, billing, crash, store, SEO, and GitHub integrations.

Mitigation: Use keychains or secret managers where possible, keep tokens out of chat and repo files, and grant only the minimum scopes needed.

Risk: GitHub issue or pull request creation can mutate repository state when write access is configured.

Mitigation: Enable GitHub artifact creation only when explicitly desired, and prefer read-only GitHub access for analysis-only deployments.

Risk: An ASC installer path may use a curl-to-bash pattern.

Mitigation: Avoid the curl-to-bash ASC installer path and use reviewed installation steps instead.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wotaso-dev/skills/growth-engineer)
- [Skill homepage](https://github.com/Wotaso/growth-engineer-skill)
- [Advanced Setup](references/advanced-setup.md)
- [Setup And Scheduling](references/setup-and-scheduling.md)
- [Required Secrets](references/required-secrets.md)
- [Input Schema](references/input-schema.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, configuration snippets, JSON summaries, issue drafts, and proposal drafts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local outbox files, GitHub issues, or draft pull requests when explicitly configured.]

## Skill Version(s):

1.0.210 (source: release evidence, package.json, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
