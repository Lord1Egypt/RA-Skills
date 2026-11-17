## Description:

Generates A-share market closing reports with index, capital-flow, sentiment, valuation, and global market data, then sends a Feishu card and saves a Markdown archive.

This skill is ready for commercial/non-commercial use.

## Publisher:

[icemanzb](https://clawhub.ai/user/icemanzb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, financial analysts, and operations teams use this skill to generate a recurring A-share closing report and distribute it through Feishu after market close.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Embedded API credentials are present in the artifact and may expose third-party services or user accounts.

Mitigation: Remove embedded secrets, rotate affected credentials, and load required keys from environment variables or a secret manager before installation.

Risk: The skill sends generated reports to a Feishu recipient, including a hard-coded default target.

Mitigation: Require an explicit Feishu target and send confirmation before scheduled or automated use.

Risk: The skill depends on external market-data services and companion skills for report content.

Mitigation: Review and pin dependency skills, monitor API quotas, and treat report values as market-data summaries that require user review.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/icemanzb/skills/oracle-report)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Artifact Metadata](artifact/_meta.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files]

**Output Format:** [Markdown report, Feishu card payload, and command-line status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires market-data credentials and outbound network access; can be run manually or on a weekday schedule.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
