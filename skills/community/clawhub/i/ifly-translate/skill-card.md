## Description:

iFlytek Machine Translation translates text between Chinese, English, Japanese, Korean, French, Spanish, German, Russian, Arabic, Thai, Vietnamese, and other languages using the iFlytek Machine Translation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to translate user-provided text through iFlytek's Machine Translation service from direct text, stdin, or files. It is useful when an agent needs command-line translation support without adding Python package dependencies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Text submitted for translation is sent to iFlytek's external translation service.

Mitigation: Do not translate secrets, private documents, regulated data, or proprietary content unless that use is approved by the user's organization and iFlytek's terms.

Risk: The skill requires user-provided iFlytek API credentials in environment variables.

Mitigation: Store credentials securely, limit credential exposure in shell history and logs, and rotate credentials if they may have been exposed.

Risk: The bundled .claude/settings.local.json contains a packaging allow rule unrelated to translation behavior.

Mitigation: Review and remove the bundled local settings rule before redistribution if it is not needed.

## Reference(s):

- [iFlytek Machine Translation API documentation](https://www.xfyun.cn/doc/nlp/xftrans/API.html)
- [iFlytek Console](https://console.xfyun.cn)
- [iFlytek Translation Service Console](https://console.xfyun.cn/services/its)
- [iFlytek Translation Pricing](https://www.xfyun.cn/services/xftrans?target=price)
- [ClawHub skill page](https://clawhub.ai/qingzhe2020/skills/ifly-translate)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Plain text translation by default, optional verbose text, or raw JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XFYUN_APP_ID, XFYUN_API_KEY, and XFYUN_API_SECRET environment variables; sends selected text to iFlytek's external translation API.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
