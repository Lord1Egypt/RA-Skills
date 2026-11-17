## Description:

Orchestrates marketing data collection from Instagram, Meta Ads, SEO, competitors, and website audits to generate a comprehensive marketing audit report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adarshvmore](https://clawhub.ai/user/adarshvmore)

### License/Terms of Use:


## Use Case:

Marketing operators and growth teams use this skill to coordinate a multi-source marketing audit from a brand's Instagram handle or website domain. It aggregates collector results and produces a report-ready marketing audit.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Marketing handles, website domains, and audit outputs may be passed to multiple collector skills and configured external marketing services.

Mitigation: Confirm the target brand data is appropriate to share with the configured collectors and services before running the skill.

Risk: The orchestrator depends on separate collector skills and a report generator whose behavior is outside this artifact.

Mitigation: Review and verify each configured collector skill, report generator, and required API key handling before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/adarshvmore/skills/marketing-orchestrator)
- [Publisher profile](https://clawhub.ai/user/adarshvmore)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown report with aggregated raw audit data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires either an Instagram handle or a website domain as input.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
