## Description: <br>
MBTI Personality lets agents switch communication tone, thinking style, and work rhythm across presets, MBTI types, and custom combinations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codesstar](https://clawhub.ai/user/codesstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose an MBTI-inspired working style for an AI coding assistant, including session-only personality changes and optional saved personality blocks for future Claude Code or OpenClaw sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent personality blocks can change future agent behavior in project or global configuration files. <br>
Mitigation: Keep the skill session-only unless persistence is intentional, and inspect any CLAUDE.md or SOUL.md personality block before saving it globally. <br>
Risk: Some persona styles may encourage unsafe coding habits such as skipping tests or standards. <br>
Mitigation: Review selected presets before use and keep normal code review, testing, and project quality gates in place. <br>
Risk: The skill changes coding behavior as well as communication tone. <br>
Mitigation: Install and enable it only where behavior-shaping assistant instructions are acceptable for the project. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/codesstar/mbti-personality) <br>
- [README](artifact/README.md) <br>
- [Personality Presets](artifact/references/presets.md) <br>
- [MBTI Types](artifact/references/mbti-types.md) <br>
- [Custom Dimensions](artifact/references/dimensions.md) <br>
- [MBTI Research Notes](artifact/references/mbti-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text, with optional CLAUDE.md or SOUL.md personality blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can operate session-only by default or persist a selected personality when the user explicitly asks to save it.] <br>

## Skill Version(s): <br>
1.4.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
