## Description:

iFlytek Machine Translation translates text between Chinese, English, Japanese, Korean, French, Spanish, German, Russian, Arabic, Thai, Vietnamese, and other supported languages using iFlytek's Machine Translation API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to translate short text, standard input, or explicitly selected files through the iFlytek Machine Translation API. It is useful when an agent needs direct multilingual translation output and the user has approved iFlytek credentials and data handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Translated text, standard input, or explicitly selected files are sent to iFlytek's external translation service.

Mitigation: Use only with content your organization has approved for that provider; do not translate secrets, regulated personal data, or confidential documents unless approved.

Risk: The skill signs requests with XFYUN credentials from environment variables.

Mitigation: Store credentials only in the expected environment variables and avoid placing credentials in translation input or files.

## Reference(s):

- [Iflytek Translate on ClawHub](https://clawhub.ai/iflytek.skills/skills/iflytek-translate)
- [iFlytek Machine Translation Service](https://www.xfyun.cn/services/machine_translation)
- [iFlytek Machine Translation API Documentation](https://www.xfyun.cn/doc/nlp/xftrans/API.html)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration guidance]

**Output Format:** [Plain text translation by default, with optional JSON response output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires XFYUN_APP_ID, XFYUN_API_KEY, and XFYUN_API_SECRET; sends selected text to the iFlytek translation API.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
