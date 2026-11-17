## Description:

Security-first skill vetting for AI agents. Use before installing any skill from ClawdHub, GitHub, or other sources. Checks for red flags, permission scope, and suspicious patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nidhov01](https://clawhub.ai/user/nidhov01)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to review candidate skills before installation by checking source, permissions, suspicious patterns, and risk level.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may lead an agent to inspect all files in a candidate skill.

Mitigation: Run vetting with least-privilege filesystem access and avoid exposing unrelated sensitive files.

Risk: Optional public GitHub endpoint checks may disclose repository names or metadata through network requests.

Mitigation: Limit network access to intended public GitHub endpoints or skip those checks for private or sensitive repositories.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/nidhov01/skills/nidhov01-skill-vetter)
- [Skill Source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands]

**Output Format:** [Markdown vetting report with optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Checklist-driven review with red flags, permission scope, risk level, verdict, and notes.]

## Skill Version(s):

1.0.0 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
