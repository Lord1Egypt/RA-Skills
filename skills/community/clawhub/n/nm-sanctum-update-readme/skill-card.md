## Description:

Refreshes README structure favoring concision (an index, not a manual)

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers maintaining repositories use this skill to research relevant README examples, reshape a README into a concise index, apply the edits, and report verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The scanner reports a potential overwrite of a predictable temporary file. The scan was partial because two local references were unresolved.

Mitigation: Review the temporary-file behavior before installation, especially before running the skill on a shared system; the partial scan does not establish that all referenced material was assessed.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/athola/skills/nm-sanctum-update-readme)
- [Project homepage (skill metadata)](https://github.com/athola/claude-night-market/tree/master/plugins/sanctum)

## Skill Output:

**Output Type(s):** [Markdown, Files, Guidance, Analysis]

**Output Format:** [README Markdown edits with a concise verification report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is based on the target repository and the references available during the workflow.]

## Skill Version(s):

1.10.3 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
