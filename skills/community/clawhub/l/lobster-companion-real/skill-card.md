## Description:

Provides agent guidance for a P2P encrypted companion-coordination system covering partner pairing, shared schedules, task coordination, real-time synchronization, and emergency contact workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to guide an agent through private companion-coordination workflows, including encrypted pairing, shared calendar and task operations, authorized location or health sharing, and emergency check-ins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks users to handle sensitive relationship data, including location, health, emergency, and shared-password or document workflows.

Mitigation: Confirm consent, sharing boundaries, revocation, and deletion behavior before using those workflows.

Risk: The release relies on install scripts and mutable dependencies that were not independently reviewed in the provided security evidence.

Mitigation: Inspect installation scripts before execution, pin and verify dependencies, install only from trusted sources, and avoid elevated privileges unless required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/puppetcat-fire/skills/lobster-companion-real)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown with inline shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may reference local tools and companion-protocol dependencies that should be reviewed and pinned before use.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
