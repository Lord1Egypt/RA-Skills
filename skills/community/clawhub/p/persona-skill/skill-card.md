## Description:

Helps OpenClaw users explicitly initialize, rebuild, or update a persistent agent persona and related preference files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tower1229](https://clawhub.ai/user/tower1229)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users use this skill to interview and create a new agent persona or to apply explicitly requested updates to an existing persona profile.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persona initialization can replace persistent agent behavior, memory, and user preference files.

Mitigation: Confirm overwrites when files already exist and review the resulting changes before relying on the persona.

Risk: Chinese-language and MBTI-based reference material may not fit every user's preferences.

Mitigation: Review the generated profile for language, fit, and unwanted assumptions.

## Reference(s):

- [ClawHub persona-skill release](https://clawhub.ai/tower1229/skills/persona-skill)
- [Publisher homepage (listed in skill metadata; not verified import provenance)](https://github.com/tower1229/Zhuang-Yan)
- [Persona initialization flow](references/protocols/initialization-flow.md)
- [Persona update protocol](references/protocols/persona-update.md)

## Skill Output:

**Output Type(s):** [Markdown, Configuration, Guidance]

**Output Format:** [Markdown persona and preference files with a brief confirmation message]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Initialization rewrites SOUL.md, MEMORY.md, USER.md, and persona/PERSONA_PROFILE.md and updates managed IDENTITY.md fields; profile updates patch IDENTITY.md and persona/PERSONA_PROFILE.md.]

## Skill Version(s):

1.2.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
