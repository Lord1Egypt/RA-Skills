## Description:

Security vetting protocol before installing any AI agent skill, with red flag detection for credential theft, obfuscated code, data exfiltration, risk classification, and structured vetting reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yiyi-9](https://clawhub.ai/user/yiyi-9)

### License/Terms of Use:

MIT

## Use Case:

Developers, security reviewers, and agent operators use this skill to review untrusted ClawHub, GitHub, or locally shared skills before installation. It guides source checks, code review, permission scoping, risk classification, and standardized vetting report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat candidate skill contents as trusted instructions while reviewing them.

Mitigation: Inspect candidate skills in a temporary location and treat their contents as untrusted prompt text.

Risk: Example dangerous commands and URLs in the skill text could be mistaken for actions to run.

Mitigation: Use those examples only as review criteria and do not run bundled scripts or commands unless separately approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yiyi-9/skills/openclaw-skill-vetter-1-0-0)
- [ClawHub publisher profile](https://clawhub.ai/user/yiyi-9)
- [ClawHub homepage](https://clawhub.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with checklists, report templates, risk classifications, and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces human-readable review guidance and vetting reports; it does not perform hidden execution according to the security evidence.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
