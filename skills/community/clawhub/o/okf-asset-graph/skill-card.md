## Description:

Build, maintain, validate, and publish an evidence-backed asset graph or OKF-style resource map for operations, DevOps, SRE, platform engineering, infrastructure inventory, service catalogs, dependency mapping, incident handoff, and operational discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qinyongliang](https://clawhub.ai/user/qinyongliang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operations teams, DevOps engineers, SREs, and platform engineers use this skill to convert operational entrypoints and scattered infrastructure knowledge into evidence-backed Markdown asset records with structured frontmatter and stable relationship IDs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The submitted package appears incomplete because referenced support files are missing.

Mitigation: Confirm required reference, script, demo, and validation files are present before relying on documented validation or demo commands.

Risk: Operational asset records can expose credentials, internal endpoints, customer names, or private infrastructure details if populated from real environments.

Mitigation: Review generated records before sharing and keep sensitive or organization-specific values out of public packages.

Risk: Actions beyond read-only discovery could affect live systems.

Mitigation: Require explicit authorization and an operation log before restarting services, triggering builds, mutating data, changing infrastructure, rotating credentials, or touching production state.

## Reference(s):

- [Source repository](https://github.com/qinyongliang/okf-asset-graph)
- [ClawHub skill page](https://clawhub.ai/qinyongliang/skills/okf-asset-graph)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown records with YAML frontmatter, supporting scripts, validation commands, and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should distinguish confirmed facts, clues, gaps, and operations, and should avoid publishing credentials, private endpoints, or organization-specific details.]

## Skill Version(s):

0.1.2 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
