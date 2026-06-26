## Description: <br>
Proofreads Chinese text with iFlytek's Official Document Proofreading API, detecting typos, punctuation issues, word order problems, factual errors, sensitive content, and related document-quality issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qingzhe2020](https://clawhub.ai/user/qingzhe2020) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, writers, editors, and agents use this skill to send Chinese text, including official-document drafts, to iFlytek for proofreading and correction suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Submitted proofreading text is sent to iFlytek using the user's API credentials. <br>
Mitigation: Use only text approved for external processing, and avoid confidential, regulated, or internal documents unless the organization has approved that use. <br>
Risk: API usage can consume quota or create billing exposure. <br>
Mitigation: Use a dedicated iFlytek API key, monitor quota or billing, and rotate credentials according to local policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/qingzhe2020/ifly-text-proofread) <br>
- [iFlytek Official Document Proofreading service](https://www.xfyun.cn/services/textCorrectionOfficial) <br>
- [iFlytek service console](https://console.xfyun.cn/services/s37b42a45) <br>
- [iFlytek pricing](https://www.xfyun.cn/services/textCorrectionOfficial?target=price) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Plain text proofreading report, with optional decoded JSON output when --raw is used.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires iFlytek API credentials. Sends submitted text to iFlytek and truncates input above 220,000 characters.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
