## Description: <br>
Speech-to-text via SkillBoss API Hub (STT, powered by Whisper and more). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to transcribe audio files and translate audio to English through SkillBoss API Hub without downloading local speech models. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are uploaded to SkillBoss for transcription. <br>
Mitigation: Avoid confidential or regulated recordings unless SkillBoss privacy and retention practices are acceptable for the use case. <br>
Risk: The SKILLBOSS_API_KEY may grant account access or incur usage charges if exposed. <br>
Mitigation: Store the API key in a protected environment variable and do not paste it into prompts, logs, or shared files. <br>


## Reference(s): <br>
- [SkillBoss API Hub](https://api.skillbossai.com) <br>
- [ClawHub release page](https://clawhub.ai/kirkraman/martin-transcribe) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and returned transcription text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and a selected audio file; chosen audio is uploaded to SkillBoss for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
