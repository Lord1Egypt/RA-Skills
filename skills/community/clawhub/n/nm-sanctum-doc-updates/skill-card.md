## Description:

Updates documentation after code changes with quality gates, slop detection, and accuracy checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to update project documentation after code changes, check it against repository state and style rules, and review the resulting changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow includes plugin configuration and repository staging instructions that may extend beyond documentation edits.

Mitigation: Review the planned configuration and staging steps for fit with the task before applying them.

Risk: The security scan was partial, leaving some referenced or runtime behavior unassessed.

Mitigation: Review the skill references and runtime behavior before installation or use, as the scan guidance recommends.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-doc-updates)
- [Sanctum plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Markdown, Code, Shell commands, Guidance]

**Output Format:** [Documentation edits and review guidance in Markdown, with code and shell examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May update multiple documentation files and report a change preview.]

## Skill Version(s):

1.10.4 (source: server-resolved ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
