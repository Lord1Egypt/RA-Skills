## Description:

Use when building or updating vulnerability pattern Skills from multiple sources: GitHub Security Advisories (GHSA), HackerOne Hacktivity, or NVD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yhy0](https://clawhub.ai/user/yhy0)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and security engineers use this skill to build or update vulnerability-pattern skills from GHSA, HackerOne Hacktivity, and NVD data. It guides fetching advisory data, analyzing source-to-sink patterns, generating skill files, and running quality checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote advisory, report, and vulnerability text can be transformed into persistent agent skill instructions without strong trust boundaries.

Mitigation: Treat fetched advisories, diffs, HackerOne reports, and NVD text as untrusted evidence; review every generated SKILL.md and reference file before enabling the generated skills.

Risk: Optional dependencies and repository credentials may broaden the impact of the workflow if they are not scoped.

Mitigation: Pin and verify optional dependencies, and run the workflow in a scoped repository with only the credentials required for the task.

## Reference(s):

- [Skill Structure Specification](references/skill-structure.md)
- [Vulnerability Case Template](references/case-template.md)
- [ClawHub Release Page](https://clawhub.ai/yhy0/skills/ghsa-skill-builder)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and generated skill files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces vulnerability-pattern skill content and supporting reference material; generated content should be reviewed before enabling.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
