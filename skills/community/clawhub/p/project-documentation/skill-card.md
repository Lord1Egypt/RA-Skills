## Description:

Complete workflow for project documentation including ADRs, PRDs, personas, and docs organization.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wpank](https://clawhub.ai/user/wpank)

### License/Terms of Use:


## Use Case:

Developers and project teams use this skill to set up or improve project documentation, including ADRs, PRDs, personas, runbooks, roadmaps, and a docs-first directory structure.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mutable npx or GitHub installation sources can change between review and installation.

Mitigation: Prefer a pinned ClawHub/package version or inspect the package before installation.

Risk: Global installation can make the skill available across future agent sessions where it may not be intended.

Mitigation: Use per-project installation when the skill should be limited to one workspace.

## Reference(s):

- [Project Documentation on ClawHub](https://clawhub.ai/wpank/skills/project-documentation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown templates and structured documentation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to create documentation structure and templates; no executable code is bundled.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
