## Description: <br>
iFlytek Machine Translation translates text between Chinese, English, Japanese, Korean, French, Spanish, German, Russian, Arabic, Thai, Vietnamese, and other supported languages using the iFlytek Machine Translation API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to translate text from direct input, stdin, or files through iFlytek Machine Translation with explicit source and target language options. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Text submitted for translation is sent to iFlytek's external Machine Translation API. <br>
Mitigation: Avoid translating secrets, private files, regulated data, or confidential business text unless that use is approved. <br>
Risk: The artifact includes a local Claude settings file with a packaging command that is not needed for translation. <br>
Mitigation: Remove or ignore the bundled .claude local settings file before using the translation skill. <br>
Risk: The skill reads iFlytek API credentials from environment variables. <br>
Mitigation: Store API keys in the execution environment only and do not place credentials in prompts, source files, or translated content. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingzhe2020/ifly-translate) <br>
- [iFlytek Machine Translation API documentation](https://www.xfyun.cn/doc/nlp/xftrans/API.html) <br>
- [iFlytek console](https://console.xfyun.cn) <br>
- [iFlytek translation service console](https://console.xfyun.cn/services/its) <br>
- [iFlytek translation pricing](https://www.xfyun.cn/services/xftrans?target=price) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, guidance] <br>
**Output Format:** [Plain text by default, optional verbose text, or raw JSON response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XFYUN_APP_ID, XFYUN_API_KEY, and XFYUN_API_SECRET environment variables; reads text from an argument, stdin, or a file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
