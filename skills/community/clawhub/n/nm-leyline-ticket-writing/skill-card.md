## Description:

Writes tickets a reader can assess at a glance, with the why inline or a link away

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to create and edit tickets in Jira, GitLab, GitHub, and other trackers. It helps make the outcome, reason, acceptance criteria, and links clear while preserving each project's established ticket format.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticket content could expose secrets or credentials if they are included in a description.

Mitigation: Do not include secrets or credentials in tickets.

## Reference(s):

- [Tracker Mechanics](modules/tracker-mechanics.md)
- [Declared project homepage (Clawdis metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [Rath 2018: issue links in commits](https://arxiv.org/abs/1804.02433)
- [Nath 2025: trace links in release artifacts](https://arxiv.org/abs/2511.18187)

## Skill Output:

**Output Type(s):** [Guidance, Text, Markdown]

**Output Format:** [Markdown ticket descriptions and editing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Tracker-specific formats vary; Jira REST v3 descriptions use Atlassian Document Format.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
