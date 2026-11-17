## Description:

噗滋（pozzzi）报表官 - 图表代码生成工具，接收 pozzzi-cfo-analyze 返回的 viz_specs 并为 Excel、WPS、钉钉和腾讯文档生成可粘贴的图表代码。

This skill is ready for commercial/non-commercial use.

## Publisher:

[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and spreadsheet power users use this skill to turn analyzed dataset visualization specs into chart code for Excel, WPS, DingTalk, or Tencent Docs. It supports common chart types for reporting workflows where generated code is reviewed and pasted into the target tool.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated VBA, macros, scripts, or formulas may be incorrect or inappropriate for the target spreadsheet environment.

Mitigation: Review generated code and test it in the target application before running it on important reports.

Risk: Dataset IDs and visualization specifications may be processed by the backing visualization API.

Mitigation: Submit only dataset identifiers and visualization details that are appropriate for that API to process.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/skills/pozzzi-cfo-visualize)

## Skill Output:

**Output Type(s):** [text, code, guidance]

**Output Format:** [Markdown with target-tool code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated chart code targets Excel, WPS, DingTalk, or Tencent Docs and should be tested in the target application before use.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
