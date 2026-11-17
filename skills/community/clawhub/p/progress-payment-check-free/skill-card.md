## Description:

工程进度款支付计算表逐项核对（逐行复算、合计勾稽、重复与空缺检测），每条结论引用原文行号，本免费版执行引擎声明的免费检查项。

This skill is ready for commercial/non-commercial use.

## Publisher:

[chenqg618](https://clawhub.ai/user/chenqg618)

### License/Terms of Use:

MIT-0

## Use Case:

External construction and engineering users can use this skill to locally check copied progress-payment worksheets for arithmetic mismatches, total-row errors, duplicate contract sections, and blank required fields. It is intended for worksheet review support and does not replace contract, legal, or quantity-survey review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may treat arithmetic worksheet findings as contract, legal, or quantity-survey approval.

Mitigation: Use the output as a local calculation check only, then confirm payment decisions against the contract, supporting measurement records, and qualified review.

Risk: The free version omits higher-risk checks such as over-contract payment, inverted cumulative values, out-of-range rates, and negative payment detection.

Mitigation: Run separate checks for omitted items before payment approval, especially where cumulative totals, contract caps, or unusual rates matter.

Risk: Missing headers or incomplete worksheet text can prevent a valid conclusion.

Mitigation: Provide the worksheet with required headers and source rows; when the skill reports insufficient input, treat the run as no conclusion.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chenqg618/skills/progress-payment-check-free)

## Skill Output:

**Output Type(s):** [text, json, shell commands, guidance]

**Output Format:** [Plain text or JSON findings with source line numbers and summary fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally with Node standard-library code; accepts JSON or copied worksheet text.]

## Skill Version(s):

1.0.33 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
