## Description:

GatherUp (gatherup.com). Use this skill for ANY GatherUp request — searching and reading data. Whenever a task involves GatherUp, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected GatherUp account can use the skill to retrieve business locations and customer records, including listing records or looking up a record by ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup runs installation scripts that have not been verified in the provided artifact.

Mitigation: Review and approve CLI installation separately, and use a verified release.

Risk: Startup synchronization can make broader changes to other agent skills.

Mitigation: If those changes are unwanted, disable synchronization with OO_SKILLS_SYNC_DISABLED=1.

Risk: GatherUp customer data is routed through OOMOL.

Mitigation: Confirm that routing GatherUp customer data through OOMOL is acceptable.

## Reference(s):

- [GatherUp homepage](https://gatherup.com/)
- [GatherUp API documentation](https://apidocs.gatherup.com/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance, JSON]

**Output Format:** [Markdown instructions with shell command examples and JSON payloads; connector results are returned as JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses the connected GatherUp account; action inputs follow the live connector schema.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
