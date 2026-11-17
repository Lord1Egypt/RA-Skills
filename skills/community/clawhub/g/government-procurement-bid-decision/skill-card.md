## Description:

Analyzes government procurement opportunities using historical tender and award data to recommend whether to bid, identify competitors and restrictions, and estimate a bid price range.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhiliaobiaoxun](https://clawhub.ai/user/zhiliaobiaoxun)

### License/Terms of Use:

MIT-0

## Use Case:

Procurement teams and bidders assess government tenders, compare historical awards and likely competitors, and prepare evidence-backed bid/no-bid and pricing decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill checks account status and upgrade notices outside the main analysis.

Mitigation: Review those account interactions before use and restrict outbound access to the intended service.

Risk: An API key may persist in a local configuration file.

Mitigation: Use a preconfigured credential where possible and protect or remove locally stored keys when no longer needed.

Risk: Project and company queries are sent to Zhiliaobiaoxun; trial registration uses hashed device features.

Mitigation: Avoid submitting sensitive queries and opt into registration only after reviewing the data shared.

Risk: Historical procurement data may not support a reliable bid or pricing conclusion.

Mitigation: Check source citations, data gaps, and assumptions before making a commercial decision.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zhiliaobiaoxun/skills/government-procurement-bid-decision)
- [Zhiliaobiaoxun skill documentation](https://ai.zhiliaobiaoxun.com/docs/skill)
- [Analysis workflow](references/workflow.md)
- [Report template](references/report-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, HTML]

**Output Format:** [Markdown decision report; shareable HTML report in full mode]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bid recommendation, price range, competitor assessment, supporting citations, and a disclaimer.]

## Skill Version(s):

1.0.9 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
