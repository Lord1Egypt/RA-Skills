## Description: <br>
Applies MBTI-based personality presets, individual types, recommendations, and custom blends to an agent's communication and coding style. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codesstar](https://clawhub.ai/user/codesstar) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to switch an assistant into MBTI-inspired communication, problem-solving, and coding styles, including session-only styles and optional persisted project or global personality settings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persisted project or global personality settings can change future agent behavior. <br>
Mitigation: Use session-only mode by default, and review the exact personality block before saving it to project or global configuration. <br>
Risk: Some personality styles encourage faster or less formal coding habits that may reduce testing or documentation discipline. <br>
Mitigation: Treat personality as tone and workflow guidance only; continue to review code, tests, security, and technical correctness before using outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/codesstar/mbti-style) <br>
- [GitHub repository link from README](https://github.com/codesstar/mbti-personality) <br>
- [README](artifact/README.md) <br>
- [Personality Presets](artifact/references/presets.md) <br>
- [MBTI Personality Type Definitions](artifact/references/mbti-types.md) <br>
- [Custom Personality Dimensions](artifact/references/dimensions.md) <br>
- [MBTI Research Notes](artifact/references/mbti-research.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Plain text and Markdown instructions, with optional persisted Markdown blocks in CLAUDE.md or SOUL.md] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual Chinese and English interaction; default behavior is session-only unless the user asks to save a personality.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
