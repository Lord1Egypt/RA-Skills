## Description: <br>
Provides agent guidance for using SkillBoss to call a speech-to-text API with OpenAI Whisper through an OpenAI-compatible endpoint. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external agent users can use this skill to configure credentials and call SkillBoss for speech-to-text transcription through an OpenAI-compatible API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required SkillBoss API key may enable paid access to many non-speech APIs. <br>
Mitigation: Use the skill only in environments where SkillBoss spend and scope are acceptable, and prefer a narrower speech-to-text integration if transcription is the only requirement. <br>
Risk: Audio and request data are sent through a third-party API gateway. <br>
Mitigation: Use this skill only when the user or organization trusts SkillBoss with the submitted data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-speech-to-text-api) <br>
- [SkillBoss setup](https://skillboss.co/skill.md) <br>
- [SkillBoss console](https://skillboss.co/console) <br>
- [SkillBoss API endpoint](https://api.skillboss.co/v1/run) <br>
- [SkillBoss products](https://skillboss.co/products) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends requests to a third-party API gateway.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
