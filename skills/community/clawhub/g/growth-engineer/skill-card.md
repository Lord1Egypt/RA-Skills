## Description: <br>
Growth Engineer for mobile apps and agent runtimes including OpenClaw and Hermes that correlates analytics, crashes, billing, feedback, store signals, and repo context into proposal drafts for agent chat, GitHub issues, or draft pull requests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wotaso-dev](https://clawhub.ai/user/wotaso-dev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and product engineers use this skill to correlate mobile app analytics, monetization, crashes, feedback, store signals, and repository context into execution-ready growth proposals. It supports local setup, connector checks, scheduled health reviews, and optional delivery to chat, GitHub issues, or draft pull requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently modify host configuration, schedule recurring runs, update itself, and execute configured shell commands. <br>
Mitigation: Review setup changes before enabling automation, avoid curl-to-bash and self-update paths in production, and check cron, shell profile, and agent configuration changes after setup. <br>
Risk: Broad API tokens or production repository access could allow unintended reads or writes to external services. <br>
Mitigation: Use least-privilege and read-only tokens where possible, scope connectors to intended apps and accounts, and enable GitHub issue or pull request creation only when that behavior is wanted. <br>
Risk: Generated proposals may be delivered to chat, GitHub issues, or draft pull requests when configured. <br>
Mitigation: Keep GitHub artifact creation disabled by default and require human review before acting on generated proposals. <br>


## Reference(s): <br>
- [Growth Engineer Skill Homepage](https://github.com/Wotaso/growth-engineer-skill) <br>
- [ClawHub Skill Page](https://clawhub.ai/wotaso-dev/skills/growth-engineer) <br>
- [Advanced Setup](references/advanced-setup.md) <br>
- [Setup And Scheduling](references/setup-and-scheduling.md) <br>
- [Required Secrets](references/required-secrets.md) <br>
- [Input Schema](references/input-schema.md) <br>
- [Issue Template](references/issue-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands, JSON configuration guidance, and generated proposal drafts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local proposal drafts, chat outbox entries, GitHub issues, or draft pull requests when configured by the user.] <br>

## Skill Version(s): <br>
1.0.207 (source: server release, SKILL.md metadata, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
