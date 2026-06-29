## Description: <br>
Iflytek Translate translates text between Chinese, English, Japanese, Korean, French, Spanish, German, Russian, Arabic, Thai, Vietnamese, and other languages through the iFlytek Machine Translation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, agents, and end users use this skill to translate user-provided text or file/stdin content with an iFlytek account and configured API credentials. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for translation, including file or stdin content, is sent to iFlytek for processing. <br>
Mitigation: Do not submit secrets, credentials, confidential business text, personal data, or regulated content unless third-party translation is approved for that data. <br>
Risk: The skill requires iFlytek API credentials to call the translation service. <br>
Mitigation: Configure credentials through environment variables and rotate or revoke them if they may have been exposed. <br>
Risk: Single-request input length is documented as limited to 4096 bytes. <br>
Mitigation: Split longer text into smaller segments before translation and review the combined output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/iflytek-translate) <br>
- [iFlytek Machine Translation product page](https://www.xfyun.cn/services/machine_translation) <br>
- [iFlytek Machine Translation API documentation](https://www.xfyun.cn/doc/nlp/xftrans/API.html) <br>
- [iFlytek console service setup](https://console.xfyun.cn/services/its) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, shell commands, configuration guidance] <br>
**Output Format:** [Plain text translation by default, optional raw JSON response, and Markdown usage examples with shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XFYUN_APP_ID, XFYUN_API_KEY, and XFYUN_API_SECRET; single request text is documented as limited to 4096 bytes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
