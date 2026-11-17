## Description:

Applies MBTI-style presets, individual types, and custom blends to an agent's communication, problem-solving approach, coding style, and work rhythm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codesstar](https://clawhub.ai/user/codesstar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to switch Claude Code or OpenClaw into MBTI-inspired communication and coding work styles, including presets, individual MBTI types, custom blends, and recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent personality settings can make lasting changes to agent behavior.

Mitigation: Keep use session-only unless persistence is intentional; before saving, review the exact CLAUDE.md or SOUL.md target, the inserted MBTI block, and the removal path.

Risk: Some personality presets may push the agent toward speed or style over normal engineering safeguards.

Mitigation: Review generated work for correctness, security, tests, and tool use, especially in work or shared environments.

## Reference(s):

- [Personality Presets](references/presets.md)
- [MBTI Personality Type Definitions for Claude Code](references/mbti-types.md)
- [Custom Personality Dimensions](references/dimensions.md)
- [MBTI 16 Type Research](references/mbti-research.md)
- [ClawHub Skill Page](https://clawhub.ai/codesstar/skills/mbti-style)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational text and Markdown, with optional file edits to CLAUDE.md or SOUL.md when the user requests saved personality settings.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English prompts; session-only by default, with project or global persistence only after explicit save intent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
