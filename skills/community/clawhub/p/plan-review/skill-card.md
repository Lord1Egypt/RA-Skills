## Description:

Plan & Review generates validated Chinese-language pre-market, intraday, and post-market market research reports from checked market snapshots.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fize](https://clawhub.ai/user/fize)

### License/Terms of Use:

MIT-0

## Use Case:

External users and analysts use this skill to prepare market plans and reviews from validated data bundles, with evidence identifiers attached to quantitative claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Market reports may be incorrect or misleading if generated from missing, stale, or unvalidated market data.

Mitigation: Run the skill's prepare and validate workflow for the requested phase and deliver reports only when the data bundle and report validation are ready.

Risk: The release description mentions trading journals and discipline scoring that the security guidance says users should not expect yet.

Mitigation: Use the skill for validated market-report workflows only until the publisher aligns the description with implemented behavior.

Risk: Readers could mistake research plans and reviews for execution instructions.

Mitigation: Keep outputs as research reports with evidence identifiers and do not connect the skill to trading execution tools.

## Reference(s):

- [Plan & Review on ClawHub](https://clawhub.ai/fize/skills/plan-review)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown market reports with workflow command guidance and JSON readiness/status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports must be generated from ready data bundles and validated before delivery; quantitative claims require evidence identifiers.]

## Skill Version(s):

1.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
