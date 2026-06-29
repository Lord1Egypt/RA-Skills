## Description: <br>
Iflytek Text Proofread uses iFlytek's Official Document Proofreading API to detect and suggest corrections for Chinese text, including typos, punctuation, word order, factual issues, sensitive content, and related official-document proofreading errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iflytek.skills](https://clawhub.ai/user/iflytek.skills) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to proofread Chinese text, especially official documents, by submitting user-provided text to iFlytek's proofreading service and returning readable correction findings or decoded JSON. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: User-provided text is sent to iFlytek's third-party proofreading API. <br>
Mitigation: Use the skill only when the user or organization permits that data transfer, and avoid confidential, regulated, personal, or secret material unless approved. <br>
Risk: The skill requires iFlytek API credentials to call the service. <br>
Mitigation: Provide credentials through environment variables and keep them out of prompts, shared files, logs, and rendered responses. <br>


## Reference(s): <br>
- [iFlytek Text Proofread service](https://www.xfyun.cn/services/text_proofread) <br>
- [iFlytek Official Document Proofreading documentation](https://www.xfyun.cn/services/textCorrectionOfficial) <br>
- [iFlytek console service setup](https://console.xfyun.cn/services/s37b42a45) <br>
- [ClawHub skill page](https://clawhub.ai/iflytek.skills/iflytek-text-proofread) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Human-readable command-line text, or decoded JSON when --raw is used] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and iFlytek credentials in IFLY_APP_ID, IFLY_API_KEY, and IFLY_API_SECRET; input text is truncated at 220,000 characters.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
