## Description:

Proactively organizes files and folders while working by learning structure preferences, thinking ahead for scale, and optimizing for future access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and other agent users use this skill to keep workspace structure coherent as files are created, moved, renamed, grouped, or archived. The skill proposes organization changes, asks for confirmation, and records confirmed preferences for future work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Learned organization patterns may capture sensitive work, personal, shared, private, or archival habits if reused without review.

Mitigation: Review or clear patterns.md when preferences could reveal sensitive habits or should no longer be reused automatically.

Risk: Organization proposals may move, rename, or group files in ways that disrupt access patterns if applied without confirmation.

Mitigation: Follow the skill's confirmation loop before reorganizing and only auto-apply patterns that the user has explicitly confirmed.

## Reference(s):

- [Skill Instructions](artifact/SKILL.md)
- [Organization Principles](artifact/principles.md)
- [Learned Patterns](artifact/patterns.md)
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/organize)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown prose with structured organization proposals and preference notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires explicit user confirmation before reorganizing and may update patterns.md with confirmed organization preferences.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
