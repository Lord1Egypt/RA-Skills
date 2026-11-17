## Description:

Audits Markdown links and local anchors for broken references, with optional external-link checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and documentation maintainers use this skill to check Markdown references before publishing or after reorganizing project files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Declared permissions understate the skill's file access, local execution, and optional network checks.

Mitigation: Review before installing, restrict use to documentation directories, and request corrected permissions and removal of unnecessary Write authority.

Risk: External-link checking may contact sites when enabled.

Mitigation: Run external checks only intentionally with --net and confirm network access is appropriate.

## Reference(s):

- [md-link-audit ClawHub release](https://clawhub.ai/zhaoxinghua09-cell/skills/md-link-audit)

## Skill Output:

**Output Type(s):** [Text, JSON]

**Output Format:** [Console report or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports link issues and an exit status of 0, 1, or 2.]

## Skill Version(s):

1.0.1 (source: release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
