## Description:

iFlytek Official Document Proofreading detects and corrects Chinese text issues including typos, punctuation, word order, factual mistakes, sensitive content, and other supported proofreading categories.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iflytek.skills](https://clawhub.ai/user/iflytek.skills)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content teams use this skill to proofread Chinese text, especially official documents, through the iFlytek proofreading API. It can check direct text input, standard input, or a local text file and return readable findings or decoded JSON.

### Deployment Geography for Use:

Global, subject to iFlytek service availability and organizational approval for sending text to the external service.

## Known Risks and Mitigations:

Risk: User-provided text is sent to iFlytek's external proofreading service using the user's iFlytek API credentials.

Mitigation: Use the skill only for text approved for that data flow, and avoid confidential, regulated, or sensitive documents unless the organization has approved submission to iFlytek.

Risk: The API request requires IFLY_APP_ID, IFLY_API_KEY, and IFLY_API_SECRET credentials in the runtime environment.

Mitigation: Store credentials in environment variables or an approved secret manager, rotate them according to policy, and avoid placing them in prompts, files, or logs.

Risk: Texts longer than 220,000 characters are truncated before proofreading, so omitted text will not be checked.

Mitigation: Split long documents into approved chunks and review combined results before relying on the proofreading output.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/iflytek.skills/skills/iflytek-text-proofread)
- [iFlytek text proofreading service](https://www.xfyun.cn/services/text_proofread)
- [iFlytek official document proofreading documentation](https://www.xfyun.cn/services/textCorrectionOfficial)
- [iFlytek service console](https://console.xfyun.cn/services/s37b42a45)
- [iFlytek pricing information](https://www.xfyun.cn/services/textCorrectionOfficial?target=price)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, API calls, JSON]

**Output Format:** [Human-readable terminal text or decoded JSON response]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes one text input stream per invocation and truncates inputs above 220,000 characters.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
