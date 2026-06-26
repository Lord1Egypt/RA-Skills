## Description: <br>
Provides text-to-speech access to ElevenLabs and OpenAI voices through SkillBoss using one API key and zero markup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to generate text-to-speech audio through SkillBoss using ElevenLabs and OpenAI voices without managing separate provider accounts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a SkillBoss API key that may enable many paid API categories beyond text-to-speech. <br>
Mitigation: Use scoped keys or spending limits where available, and require explicit approval before non-TTS calls or sensitive text is sent externally. <br>
Risk: The setup flow points agents to a remote setup file. <br>
Mitigation: Inspect the remote setup file before running it and confirm that installed behavior matches the intended TTS use case. <br>


## Reference(s): <br>
- [SkillBoss Console](https://skillboss.co/console?utm_source=clawhub&utm_medium=skill&utm_campaign=text-to-speech-api) <br>
- [SkillBoss Setup File](https://skillboss.co/skill.md) <br>
- [SkillBoss Products](https://skillboss.co/products) <br>
- [ClawHub Skill Page](https://clawhub.ai/kirkraman/kirk-text-to-speech-api) <br>
- [Publisher Profile](https://clawhub.ai/user/kirkraman) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, code, configuration] <br>
**Output Format:** [Markdown instructions with shell commands, curl examples, and Python code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY for API calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
