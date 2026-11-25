## Description:

Scores backlog items with RICE/WSJF/Kano and files GitHub issues for top candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[athola](https://clawhub.ai/user/athola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill during roadmap reviews, retrospectives, and sprint planning to inventory features, compare priorities, identify gaps, and prepare issues for accepted suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research mode may send feature-derived topics to external services, and the scan could not verify the referenced implementation.

Mitigation: Review the data shared and the missing implementation details before using research mode; avoid sending sensitive project topics until that use is acceptable.

## Reference(s):

- [Scoring Framework](artifact/modules/scoring-framework.md)
- [Classification System](artifact/modules/classification-system.md)
- [Tradeoff Dimensions](artifact/modules/tradeoff-dimensions.md)
- [Research Enrichment](artifact/modules/research-enrichment.md)
- [Configuration](artifact/modules/configuration.md)
- [Multi-Metric Evaluation Methodology](https://claude-night-market/plugins/abstract/skills/skills-eval/modules/multi-metric-evaluation-methodology.md)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, GitHub issues]

**Output Format:** [Markdown tables and recommendation reports; GitHub issues for accepted suggestions when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Feature inventories, scoring and tradeoff summaries, and prioritized suggestions; backlog processing is limited to 25 items.]

## Skill Version(s):

1.10.4 (source: server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
