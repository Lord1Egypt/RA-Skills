## Description: <br>
Transcribe audio to text using SkillBoss API Hub powered by OpenAI Whisper, requiring an API key and no local model download. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[godferylindsay](https://clawhub.ai/user/godferylindsay) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to send selected audio files to SkillBoss API Hub for speech-to-text transcription and optional translation to English. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to SkillBoss for cloud transcription and may contain confidential, regulated, or consent-sensitive content. <br>
Mitigation: Use only recordings that are appropriate for SkillBoss processing and confirm SkillBoss data handling terms before sending sensitive audio. <br>
Risk: The skill requires a SKILLBOSS_API_KEY credential. <br>
Mitigation: Keep the API key scoped, stored outside prompts and source files, and rotated if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/godferylindsay/godfery-transcribe) <br>
- [SkillBoss API Hub](https://api.skillbossai.com) <br>
- [SkillBoss setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and text transcription output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY and sends selected audio to SkillBoss for processing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
