## Description:

Given a keyword, this skill uses Jiimore market data to find niche markets, evaluate entry value with configurable criteria, and produce a recommendation list.

This skill is ready for commercial/non-commercial use.

## Publisher:

[linkfox-ai](https://clawhub.ai/user/linkfox-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External marketplace sellers and analysts use this skill to compare niche-market opportunities for a seed keyword and decide which markets are worth entering. It filters and scores Jiimore data by demand, search volume, brand count, concentration, CPC, growth, and new-product success signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release was flagged suspicious because it includes feedback reporting and broad credential, payment, file, and endpoint behaviors.

Mitigation: Install only after reviewing LinkFox trust assumptions, payment actions, uploads, and endpoint configuration; avoid custom LINKFOX_* endpoints with real credentials.

Risk: Market queries, generated reports, account or API-key context, feedback content, and uploaded files may be exposed to LinkFox or related services.

Mitigation: Avoid private inputs and files unless approved, store API keys in a secret manager, and review generated reports before sharing or uploading them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/linkfox-ai/skills/linkfox-expert-niche-market-recommendation)
- [Jiimore niche keyword API reference](skills/linkfox-jiimore-get-niche-info-by-keyword/references/api.md)
- [Niche recommendation method overview](skills/niche-recommendation-method/SKILL.md)
- [S0 Jiimore niche discovery](skills/niche-recommendation-method/references/steps/S0.md)
- [S1 hard filtering](skills/niche-recommendation-method/references/steps/S1.md)
- [S2 scoring](skills/niche-recommendation-method/references/steps/S2.md)
- [S3 sorting and output](skills/niche-recommendation-method/references/steps/S3.md)
- [Report layout reference](skills/linkfox-report-generator/references/analysis-layouts.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration, files]

**Output Format:** [Markdown recommendation list with optional HTML report file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommendations are derived from Jiimore fields; missing source fields should be marked as not returned.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
