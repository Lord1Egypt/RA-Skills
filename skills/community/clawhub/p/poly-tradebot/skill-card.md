## Description:

Poly Tradebot fetches CNBC world news, classifies articles into geopolitics or macroeconomics, and produces Polymarket-oriented trading analysis with market recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rafimchmd](https://clawhub.ai/user/rafimchmd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn recent CNBC news into structured prediction-market analysis, including topic classification, related Polymarket market discovery, and concise YES or NO recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved market-analysis files may contain sensitive URLs, prompts, or conclusions and may be reused later to regenerate tables.

Mitigation: Review or delete files written under memory/ when the underlying URLs, prompts, or analysis should not be retained.

Risk: Prediction-market recommendations can be incorrect, stale, or mistaken for financial advice.

Mitigation: Treat recommendations as analysis only, verify live market data independently, and apply human review before making trading decisions.

## Reference(s):

- [Topic Classification Rules](artifact/references/classification_rules.md)
- [Output Format Templates](artifact/references/output_templates.md)
- [CNBC World News](https://www.cnbc.com/world/?region=world)

## Skill Output:

**Output Type(s):** [markdown, text, files, guidance]

**Output Format:** [Markdown tables and per-article Markdown analysis files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May save article analyses and regenerated trading tables under memory/.]

## Skill Version(s):

1.0.4 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
