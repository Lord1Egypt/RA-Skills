## Description:

Intelligent Driving DSS provides China-focused decision support for L2-L5 automated-driving scenarios by combining traffic-law checks, NEV system modeling, scenario stress testing, and risk alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikewongonline](https://clawhub.ai/user/mikewongonline)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and automotive engineers use this skill to analyze Chinese traffic-law scenarios, compare NEV models, estimate energy consumption, and generate compliance-oriented decision reports. Outputs are reference guidance and should be reviewed before use in legal, safety, or driving decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides high-stakes driving, vehicle safety, and legal reference guidance.

Mitigation: Require human review against current official sources before relying on generated analysis for legal, safety, purchasing, or driving decisions.

Risk: Evidence security guidance flags under-scoped automatic document downloads and skill-file updates.

Mitigation: Do not allow automatic downloads or skill-file updates; require explicit approval, HTTPS-only sources, staging, checksums, and review before reuse.

Risk: The security verdict is suspicious despite no visible malicious behavior.

Mitigation: Install only when a China-focused automotive and legal reference skill is needed, and review generated reports before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikewongonline/skills/intelligent-driving-dss)
- [Compliance review guide](artifact/compliance-review-guide.md)
- [Core traffic rules](artifact/core-traffic-rules/README.md)
- [NEV system module](artifact/nev-system-module/README.md)
- [Market rankings](artifact/market-rankings/README.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, guidance]

**Output Format:** [Markdown narrative with structured checklists, decision reports, matrices, and JSON-backed analysis where applicable]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include legal, vehicle-safety, energy-consumption, market-comparison, and uncertainty notes derived from bundled reference material.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
