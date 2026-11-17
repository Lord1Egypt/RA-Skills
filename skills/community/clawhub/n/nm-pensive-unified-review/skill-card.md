## Description:

Orchestrates multi-domain review (code, arch, tests, security) in a single pass.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to select and coordinate code, architecture, test, API, security, shell, and Makefile reviews. It helps produce evidence-based findings, prioritized recommendations, and an integrated action plan before changes are merged.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports system-install and file-changing behavior.

Mitigation: Review commands before running them, isolate repository tests and Make inspection from sensitive files and credentials, and request a preview and approval before applying changes.

Risk: Security analysis coverage is incomplete: 13 of 15 components were scanned, two were partially inspected, and static tool-misuse analysis was degraded.

Mitigation: Treat the scan as partial evidence and manually review the relevant skill files and commands before use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-pensive-unified-review)
- [Project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/pensive)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Markdown, Shell commands]

**Output Format:** [Markdown review reports with findings, evidence, recommendations, and action plans; may include shell or Make command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Single review stream; content varies with detected codebase domains and selected review mode.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
