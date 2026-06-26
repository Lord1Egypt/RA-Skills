## Description: <br>
Speech-to-text via SkillBoss API Hub (STT, powered by Whisper and more). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kirkraman](https://clawhub.ai/user/kirkraman) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agents use this skill to transcribe audio or translate speech to English through SkillBoss API Hub without local model setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected audio files are sent to SkillBoss API Hub for transcription, which can expose confidential, regulated, or consent-sensitive recordings. <br>
Mitigation: Use only audio approved for this vendor and policy, and avoid sensitive recordings unless permitted. <br>
Risk: The skill requires a sensitive API credential. <br>
Mitigation: Use a properly scoped SKILLBOSS_API_KEY and avoid exposing it in prompts, logs, code snippets, or shared files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kirkraman/kirk-transcribe) <br>
- [SkillBoss API Hub](https://api.skillbossai.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, API calls, Configuration] <br>
**Output Format:** [Markdown with Python code examples and API request payloads] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SKILLBOSS_API_KEY; selected audio is sent to SkillBoss API Hub for transcription or English translation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
