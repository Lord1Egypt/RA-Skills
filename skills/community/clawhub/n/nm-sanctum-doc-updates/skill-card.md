## Description:

Updates documentation after code changes with quality gates, slop detection, and accuracy checks

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to update project documentation after code changes, check documentation quality and accuracy, and review proposed edits before previewing them.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review marks the skill suspicious with medium confidence, citing plugin-registration checks and instructions that may expand documentation work into functional changes.

Mitigation: Review whether plugin registration changes are appropriate before installation; the scanner analysis is partial, so assess the skill directly.

## Reference(s):

- [Sanctum project homepage listed in skill metadata](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)
- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-doc-updates)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Guidance]

**Output Format:** [Markdown documentation edits, shell commands, and review summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on the documentation targets and checks selected for each change.]

## Skill Version(s):

1.10.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
