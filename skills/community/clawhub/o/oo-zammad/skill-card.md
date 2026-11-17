## Description:

Use Zammad to read, search, create, and update tickets and users through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support teams and service operators can use the skill to find and review Zammad tickets, manage ticket details and articles, and search users. It uses an OOMOL-connected account and requires confirmation before ticket changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup executes unchecked remote code.

Mitigation: Review and install a verified CLI release separately before using the skill.

Risk: Automatic skill synchronization may change other installed agent skills.

Mitigation: Review the CLI's automatic skill synchronization settings before setup.

Risk: Connected Zammad permissions can allow access to more data or actions than a task needs.

Mitigation: Connect only the permissions needed and confirm ticket changes before running write actions.

## Reference(s):

- [Zammad](https://zammad.com/en)
- [Zammad API documentation](https://docs.zammad.org/en/latest/api/intro.html)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Markdown with shell commands and JSON payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands use the live connector schema and require confirmation before ticket writes.]

## Skill Version(s):

1.0.4 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
