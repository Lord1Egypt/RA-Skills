## Description:

Autotask (datto.com). Use this skill for ANY Autotask request — searching and reading data. Whenever a task involves Autotask, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Autotask users with an OOMOL-connected account use this skill to inspect entity metadata and retrieve or query Companies, Contacts, and Tickets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute remote code that has not been verified.

Mitigation: Review setup before installing and use a separately verified oo CLI release.

Risk: Startup may write to agent skill directories, and the connector accesses the connected Autotask account through OOMOL.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 when startup writes are not wanted, and connect only the Autotask account and permissions needed.

## Reference(s):

- [oo CLI command reference](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md)
- [Autotask REST API authentication documentation](https://www.autotask.net/help/developerhelp/Content/APIs/REST/General_Topics/REST_Security_Auth.htm)
- [Autotask PSA](https://www.datto.com/products/autotask-psa/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON data and text guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-focused queries for Companies, Contacts, Tickets, and Autotask metadata]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
