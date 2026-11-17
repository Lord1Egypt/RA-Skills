## Description:

Industry Diagnosis is an OpenClaw agent skill that takes an industry or product category name, gathers market evidence, scores it with a four-dimension strategy framework, and generates an eight-section Markdown diagnosis report for strategic decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ysw-2025](https://clawhub.ai/user/ysw-2025)

### License/Terms of Use:

MIT-0

## Use Case:

External users, founders, brand operators, investors, and chain-brand strategists use this skill to assess whether to enter an industry or category and how to shape market entry strategy. The skill produces structured market-capacity, trend, competition, differentiation, risk, and opportunity analysis in Markdown.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated reports append promotional material and a QR-code reference for 位道策划, which may be inappropriate for neutral or internal reports.

Mitigation: Review generated reports before sharing and remove promotional footer content when neutrality or internal-use requirements apply.

Risk: The skill relies on web searches and market-source synthesis, so strategic conclusions can be affected by stale, inconsistent, or unverifiable public data.

Mitigation: Confirm key figures against recent independent sources and retain the skill requirement to mark unverifiable data as pending verification.

## Reference(s):

- [Server-resolved GitHub source](https://github.com/ysw-2025/industry-diagnosis)
- [Project homepage](https://mp.weixin.qq.com/s/wKNvt5GS3JxPmRcpAMGdEg)
- [Industry Diagnosis Methodology](references/methodology.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, files]

**Output Format:** [Markdown report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generates an eight-module industry diagnosis report and may write a file named for the analyzed industry and date when the agent has file access.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
