## Description:

Restores punctuation, sentence breaks, and paragraph structure for unformatted Chinese text from OCR, ASR, or copied web content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnny-ztsd](https://clawhub.ai/user/johnny-ztsd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content-processing workflows use this skill to clean unformatted Chinese text by adding punctuation, sentence breaks, paragraphing, and generated paragraph titles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Traditional Chinese input may be converted to Simplified Chinese, which can be unsuitable for legal, archival, quoted, or style-sensitive material.

Mitigation: Review output before using it where original script, exact wording, or citation fidelity matters.

Risk: Punctuation, paragraphing, and generated titles can change how readers interpret the original text.

Mitigation: Compare important passages against the source text and treat titles as generated summaries rather than original content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/johnny-ztsd/skills/jz-chinese-text-punctuation-restoration)
- [Publisher home page](https://www.cnblogs.com/know-data)
- [Agent Skills specification](https://agentskills.io/specification)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files]

**Output Format:** [Plain text plus a separate titled text file when paragraph titles are generated]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May convert Traditional Chinese input to Simplified Chinese and may add concise multi-level paragraph titles.]

## Skill Version(s):

1.0.2 (source: server release metadata; artifact metadata V1.0.2-202609181729)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
