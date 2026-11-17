## Description:

基于20位中外投资大师方法，提供A股、美股、港股实时数据抓取和多维度智能股票分析报告。

This skill is ready for commercial/non-commercial use.

## Publisher:

[amitabhama](https://clawhub.ai/user/amitabhama)

### License/Terms of Use:

MIT

## Use Case:

External users and agent developers use this skill to answer stock-analysis questions, fetch market data, and generate value-investing style reports across A-share, Hong Kong, and U.S. equities. It is intended to support analysis workflows, not to replace licensed financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can produce buy/sell-style investment conclusions without clear warnings.

Mitigation: Present outputs as informational analysis only and require users to consult qualified financial professionals before acting.

Risk: The skill makes outbound requests to financial-data services during normal use.

Mitigation: Review network access, data-source terms, and privacy requirements before installation or deployment.

Risk: Evidence reports a bundled reusable market-data API token.

Mitigation: Rotate the bundled credential and require each user or deployment to configure its own token.

Risk: Evidence reports that one helper script writes ETF history to a fixed local path.

Mitigation: Review file-write locations and run the skill with least-privilege filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amitabhama/skills/investmentguru)
- [Publisher profile](https://clawhub.ai/user/amitabhama)
- [Artifact README](artifact/README.md)
- [Artifact skill instructions](artifact/SKILL.md)
- [Artifact license](artifact/LICENSE.txt)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain-text stock analysis report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include market quotes, trend summaries, valuation signals, guru-method comparisons, and buy/sell-style conclusions that require human review.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata; artifact setup.py agrees)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
