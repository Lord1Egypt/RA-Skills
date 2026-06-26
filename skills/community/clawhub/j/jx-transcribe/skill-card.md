## Description: <br>
Speech-to-text via SkillBoss API Hub (STT, powered by Whisper and more). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users can use this skill to ask an agent for Python-based guidance that sends selected audio files to SkillBoss API Hub for transcription or English translation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends user-selected audio and an API key to SkillBoss. <br>
Mitigation: Install only if SkillBoss is trusted for the audio being transcribed, review SkillBoss data handling and retention policies before sending private or regulated recordings, and prefer a revocable scoped API key. <br>
Risk: The required SKILLBOSS_API_KEY is a sensitive credential. <br>
Mitigation: Store the key in an environment variable or secret manager and avoid committing it to files, prompts, or logs. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/kirkraman/jx-transcribe) <br>
- [SkillBoss API Hub](https://api.skillbossai.com) <br>
- [SkillBoss API v1 endpoint](https://api.skillbossai.com/v1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and API request patterns] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; sends user-selected audio to SkillBoss API Hub for transcription or English translation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
