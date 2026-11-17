## Description:

MBTI personality system for AI agents that switches communication tone, thinking style, and work rhythm across presets, MBTI types, and custom combinations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codesstar](https://clawhub.ai/user/codesstar)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to adjust an AI coding assistant's personality, communication style, and working rhythm for brainstorming, mentoring, review, fast delivery, or custom collaboration styles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist behavior-changing instructions into agent configuration files.

Mitigation: Keep personality changes session-only by default, and inspect any CLAUDE.md or SOUL.md changes before saving them, especially at global scope.

Risk: Some profiles encourage skipping tests, documentation, standards, review, or production safeguards.

Mitigation: Do not use those profiles for production-sensitive work, and retain normal engineering review, testing, documentation, and security practices regardless of personality style.

Risk: Changing personality can also change coding workflow, not only tone.

Mitigation: Treat the skill as a collaboration-style aid and confirm that correctness, security, tool usage, and technical decisions remain governed by project requirements.

## Reference(s):

- [Personality Presets](references/presets.md)
- [MBTI Personality Type Definitions](references/mbti-types.md)
- [Custom Personality Dimensions](references/dimensions.md)
- [MBTI Research Notes](references/mbti-research.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown and conversational text, with optional configuration blocks written to agent instruction files when the user chooses persistent mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual English and Chinese flows; default behavior is session-only unless the user asks to save a personality]

## Skill Version(s):

1.4.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
