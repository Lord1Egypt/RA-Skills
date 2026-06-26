## Description: <br>
Translate foreign-language audio into English text using OATDA's unified audio API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[devcsde](https://clawhub.ai/user/devcsde) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate uploaded foreign-language audio recordings into English text through OATDA. It helps an agent prepare authenticated OATDA audio translation requests, choose the default Whisper translation model, and present the returned English text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads selected audio recordings to OATDA for translation, and recordings may contain sensitive personal, medical, financial, or confidential content. <br>
Mitigation: Only use it when sending the recording to OATDA is intentional; avoid private or regulated conversations unless authorized. <br>
Risk: The skill requires an OATDA API key for authenticated requests. <br>
Mitigation: Store the key in the documented environment variable or credentials file, and never print the full key in logs or user-facing output. <br>
Risk: Large base64 JSON uploads can be harder to inspect and may exceed request limits. <br>
Mitigation: Prefer the documented multipart upload path for local audio files and keep audio under the documented 25MB limit. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/devcsde/oatda-translate-audio) <br>
- [Publisher Profile](https://clawhub.ai/user/devcsde) <br>
- [OATDA](https://oatda.com) <br>
- [OATDA Audio Models API](https://oatda.com/api/v1/llm/models?type=audio) <br>
- [OATDA Translations API](https://oatda.com/api/v1/llm/translations) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration guidance, API calls] <br>
**Output Format:** [Markdown with inline bash commands and JSON response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, an OATDA API key, and an audio file up to 25MB; presents the returned English translation text.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
