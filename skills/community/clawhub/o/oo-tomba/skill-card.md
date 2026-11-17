## Description:

Search and read Tomba contact and company data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search for and read contact and company information in Tomba, including domain searches, email lookups and verification, enrichment, and technology discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: First-time CLI setup may execute downloaded software whose installer and binary behavior have not been verified.

Mitigation: Review and approve CLI installation separately before allowing setup to execute downloaded code.

Risk: CLI startup may synchronize additional agent skills, a broader change not described in detail by the skill.

Mitigation: Set OO_SKILLS_SYNC_DISABLED=1 to prevent startup synchronization, and review the CLI environment controls.

Risk: Contact data sent through the service is processed by OOMOL and Tomba, and use may incur charges.

Mitigation: Submit only contact data you intend both services to process, and consider applicable usage charges.

## Reference(s):

- [OO CLI commands and environment controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Tomba](https://tomba.io)
- [Tomba API documentation](https://docs.tomba.io/)
- [Tomba skill release](https://clawhub.ai/oomol/skills/oo-tomba)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Structured Tomba results with concise text guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the connected Tomba account, the live action schema, and available service data.]

## Skill Version(s):

1.0.6 (source: skill frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
