## Description:

Enrich company and person profiles and verify identity signals through an OOMOL-connected FullContact account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to enrich company and person profiles and verify identity signals through FullContact using their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time setup runs a remote CLI installer whose code was not verified and does not clearly request approval before execution.

Mitigation: Install a reviewed, version-pinned oo CLI separately and decide whether to allow agent-skill synchronization.

Risk: Person and company identifiers submitted for enrichment or verification are processed by OOMOL and FullContact.

Mitigation: Submit only identifiers you intend those services to process.

## Reference(s):

- [oo CLI repository](https://github.com/oomol-lab/oo-cli)
- [FullContact homepage](https://www.fullcontact.com/)
- [FullContact enrichment API documentation](https://docs.fullcontact.com/docs/enrich-overview)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and Markdown instructions with inline shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned fields depend on the selected FullContact action and its live schema.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
