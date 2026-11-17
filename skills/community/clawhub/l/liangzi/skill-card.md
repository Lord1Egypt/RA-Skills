## Description:

良子数字分身技能。当用户想以良子的风格说话、互动、模仿良子发言、或问"如果良子会怎么说"时激活。激活后所有回复以良子的土味抽象风格输出。

This skill is ready for commercial/non-commercial use.

## Publisher:

[sxcllllaw11](https://clawhub.ai/user/sxcllllaw11)

### License/Terms of Use:

MIT-0

## Use Case:

External users activate this persona skill to have an agent answer in the Chinese Liangzi roleplay style, including short livestream-like phrasing, recurring catchphrases, and light entertainment responses. The skill is intended for stylistic interaction rather than factual advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Roleplay conversations may be summarized into a persistent plaintext memory file without clear consent or retention limits.

Mitigation: Make memory storage opt-in, tell users when summaries are saved, exclude sensitive details, and provide a way to inspect and delete the memory file.

Risk: Persona roleplay may drift into sensitive topics or targeted personal commentary.

Mitigation: Follow the artifact guidance to switch back to normal assistant behavior for sensitive topics and avoid malicious personal attacks.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sxcllllaw11/skills/liangzi)
- [Skill definition](artifact/SKILL.md)
- [Liangzi character configuration](artifact/characters/liangzi.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Conversational Chinese text, optionally with lightweight Markdown formatting]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Persona-styled output may include slang, catchphrases, self-deprecating humor, and Bilibili-style emotive markers.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
