## Description:

Writes tickets a reader can assess at a glance, with the why inline or a link away.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and teams use this skill to write or revise Jira, GitHub, GitLab, and other tracker tickets. It helps keep the outcome and reason clear, preserve project conventions, and link tickets with their merge requests.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ticket text can expose secrets or credentials.

Mitigation: Review the draft before saving and remove any secrets or credentials.

Risk: Generic tracker guidance may not match a project's conventions or current workflow behavior.

Mitigation: Check recent tickets or the project template and confirm tracker-specific rules before posting.

## Reference(s):

- [Claude Night Market Leyline plugin](https://github.com/athola/claude-night-market/tree/master/plugins/leyline)
- [Rath 2018: issue links in commits across six projects](https://arxiv.org/abs/1804.02433)
- [Nath 2025: trace links in release artifacts](https://arxiv.org/abs/2511.18187)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Ticket titles and descriptions in the project's tracker format, often Markdown or tracker-specific markup]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Adapts headings and markup to project conventions; may include acceptance criteria, reproduction steps, and links.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
