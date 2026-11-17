## Description:

iFlytek Official Document Proofreading detects and corrects errors in Chinese text, including typos, punctuation, word order, factual mistakes, sensitive content, and related document proofreading issues.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qingzhe2020](https://clawhub.ai/user/qingzhe2020)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and document authors use this skill to proofread Chinese text and official documents through iFlytek's remote proofreading API. It can check text supplied as an argument, stdin, or a file and return highlighted issues with explanations and correction suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The text being proofread, including file contents passed with --file, is sent to iFlytek's remote service.

Mitigation: Use the skill only when the organization permits this vendor and data flow; avoid confidential, regulated, or personal documents unless that use is approved.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/qingzhe2020/skills/ifly-text-proofread)
- [iFlytek Official Document Proofreading](https://www.xfyun.cn/services/textCorrectionOfficial)
- [iFlytek console service](https://console.xfyun.cn/services/s37b42a45)
- [iFlytek pricing details](https://www.xfyun.cn/services/textCorrectionOfficial?target=price)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Human-readable text with issue listings, or decoded JSON when --raw is used.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires iFlytek credentials; sends selected text to iFlytek's remote API; truncates input above 220,000 characters.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
