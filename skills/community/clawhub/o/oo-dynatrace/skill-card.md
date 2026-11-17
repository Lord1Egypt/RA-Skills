## Description:

Search and read Dynatrace monitored entities and problems through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to retrieve Dynatrace monitored entity details, entity lists, and problem records from an already connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup includes a remote CLI installer that executes changing third-party code; its persistent effects could not be fully assessed.

Mitigation: Review the CLI installation separately, use a pinned and independently verified release, and explicitly approve installation and any bundled-skill changes.

Risk: Dynatrace access runs through the OOMOL connection.

Mitigation: Use narrowly scoped Dynatrace read permissions and understand that access runs through OOMOL.

## Reference(s):

- [Dynatrace API documentation](https://docs.dynatrace.com/docs/dynatrace-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Dynatrace on ClawHub](https://clawhub.ai/oomol/skills/oo-dynatrace)

## Skill Output:

**Output Type(s):** [API Calls, Text, JSON]

**Output Format:** [JSON action results with concise explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only entity and problem queries; action inputs follow the live connector schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
