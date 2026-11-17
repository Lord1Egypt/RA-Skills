## Description:

Initializes hersona persona on first use of a profile and assists in maintaining the applied speech style if deviation is detected during conversation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiro-0x](https://clawhub.ai/user/shiro-0x)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to initialize a Hersona persona for a profile and receive guidance to reapply or maintain the intended speech style during conversation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can encourage profile-level persona and speech-style changes.

Mitigation: Install it only when the agent should adopt and maintain the Hersona persona/style for the relevant profile.

Risk: The suggested SOUL.md default command may make persona behavior more persistent than a session-scoped preference.

Mitigation: Review or avoid the suggested SOUL.md default command when persona changes should remain manual or session-scoped.

## Reference(s):

- [Server-resolved GitHub provenance](https://github.com/shiro-0x/hersona/tree/main/skills/hersona-initializer)
- [Hersona project homepage](https://github.com/shiro-0x/hersona)
- [ClawHub skill page](https://clawhub.ai/shiro-0x/skills/hersona-initializer)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, network access, credential use, or hidden system changes were reported by evidence.security.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata; SKILL.md frontmatter reports 0.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
