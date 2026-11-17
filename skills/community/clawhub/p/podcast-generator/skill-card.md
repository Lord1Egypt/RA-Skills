## Description:

Convert articles, blog posts, or any text into professional podcast scripts and TTS audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elevo11](https://clawhub.ai/user/elevo11)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn source text into solo or dialogue podcast scripts, generate TTS audio, and review usage statistics. The skill includes SkillPay billing support for paid generation workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can make real SkillPay billing calls.

Mitigation: Run billing commands only where charges are explicitly approved and the SkillPay API key is intended for that environment.

Risk: Generated podcast scripts and audio files may be written to uncontrolled paths.

Mitigation: Use reviewed input and output paths, and execute the skill in an isolated workspace away from sensitive files.

Risk: Podcast text may be sent to external TTS processing.

Mitigation: Avoid using confidential or sensitive source text unless the external TTS handling is approved.

Risk: Dependency behavior can change if edge-tts or related tools are installed without pinning.

Mitigation: Prefer a pinned dependency setup before using the skill in production or shared environments.

## Reference(s):

- [Podcast Script Templates](artifact/references/script-templates.md)
- [SkillPay API Endpoint](https://skillpay.me/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown scripts, MP3 audio files, JSON billing or statistics responses, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports solo and dialogue script formats, optional audio synthesis through edge-tts, and local usage statistics tracking.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
