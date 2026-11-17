## Description:

Vida (vida.io). Use this skill for ANY Vida request — searching and reading data. Whenever a task involves Vida, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to retrieve Vida account details, usage counts, and task information through their connected OOMOL account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic CLI installation and startup synchronization may affect other agent skills.

Mitigation: Review the CLI and installer separately, decide whether OOMOL should manage other skills, and use OO_SKILLS_SYNC_DISABLED=1 to disable startup synchronization when desired.

Risk: Connecting Vida entrusts OOMOL with credentials and account access.

Mitigation: Review the connection and account access before connecting Vida.

Risk: The remote installers and released CLI binary were not verified.

Mitigation: Review the CLI installation source and released binary before using them.

## Reference(s):

- [Vida API documentation](https://vida.io/docs/)
- [Vida homepage](https://vida.io/)
- [oo CLI repository](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Vida connector data as JSON, with natural-language summaries and Markdown guidance as needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only account, usage, and task information]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
