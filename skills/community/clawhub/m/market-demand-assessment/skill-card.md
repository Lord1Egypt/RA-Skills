## Description:

Market Demand Assessment helps the CECEP Valiant market department screen customer inquiries through information checks, product classification, five-dimension scoring, and R&D cost estimation, then produce a visual HTML assessment form.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanzhian-patsnap](https://clawhub.ai/user/yuanzhian-patsnap)

### License/Terms of Use:

MIT-0

## Use Case:

Market and business development employees use this skill to pre-screen customer chemical-product inquiries before involving R&D. It supports go/no-go decisions by checking inquiry completeness, classifying product fit, scoring commercial and technical attractiveness, estimating R&D cost, and preparing either an R&D push form or a polite rejection template.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may enter customer inquiries or internal product information into the workflow.

Mitigation: Install and use the skill only in an approved business environment, and avoid real confidential data until data-sharing expectations are confirmed.

Risk: Real-time data retrieval depends on separate Zhihuiya MCP authorization and enabled agent tooling.

Mitigation: Verify the Zhihuiya MCP setup before relying on database-backed conclusions; without it, use the skill as an assessment framework only.

Risk: The score and final recommendation can affect whether an inquiry is escalated to R&D.

Mitigation: Have market or supervisory staff review borderline and high-impact decisions before sending an R&D push form or rejection response.

## Reference(s):

- [Screening Method](references/01_screening_method.md)
- [Market Analysis HTML Template](references/market_analysis_template.html)
- [Zhihuiya Open Platform](https://open.zhihuiya.com/)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with HTML form/template references and generated business text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a printable/exportable HTML analysis form, R&D push-form content, scoring conclusions, and rejection email wording.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
