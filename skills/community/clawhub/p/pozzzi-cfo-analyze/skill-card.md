## Description:

Analyzes uploaded Excel, WPS, DingTalk, Tencent Docs, and CSV business reports in Chinese and returns core conclusions, data attribution, decision recommendations, and chart code.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aikawabigsky309](https://clawhub.ai/user/aikawabigsky309)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and decision-makers at Chinese small and medium businesses use this skill to ask natural-language questions over uploaded reports and receive business-facing analysis. It is intended to support financial, operations, sales, and HR reporting workflows with conclusions, attribution, recommendations, and visualization guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive business files and an OpenClaw token are sent to backend endpoints whose destination and controls are not fully described in the release evidence.

Mitigation: Use only in a trusted backend environment after confirming upload destination, token scope, request logging, and explicit user confirmation for file transfer.

Risk: Generated analysis, recommendations, and chart code may be incomplete or low confidence when uploaded report data is insufficient.

Mitigation: Review confidence labels, data-source notes, and insufficiency messages, and require human review before using results for important business decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aikawabigsky309/skills/pozzzi-cfo-analyze)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown with tables, numbered recommendations, confidence labels, and chart code]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include low-confidence or data-insufficiency notices when the uploaded reports do not support an answer.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
