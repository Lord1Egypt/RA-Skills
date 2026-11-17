## Description:

Use Productive to read and manage tasks and time entries through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing work in Productive can use this skill to inspect tasks and time entries, and create, update, or delete records through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The first-time setup fallback executes remote installation code without a separate approval step.

Mitigation: Review and approve CLI installation separately, including any changes to installed agent skills, before running it.

Risk: Create, update, and delete actions can change Productive data.

Mitigation: Keep explicit approval controls for writes and deletions; confirm the exact payload and effect before a write and the target before a deletion.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Productive](https://productive.io)
- [Productive API authorization guide](https://developer.productive.io/guides/authorization)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [oo CLI commands with JSON request payloads and Productive results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action schemas should be checked before requests; write and delete actions require user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
