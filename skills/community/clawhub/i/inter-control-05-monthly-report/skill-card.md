## Description:

Generates structured Chinese monthly internal-control compliance reports from monthly complaint, logistics exception, supplier, and risk-incident data for Cainiao Logistics, Cainiao Post, and Taobao Flash Purchase.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nic-yuan](https://clawhub.ai/user/nic-yuan)

### License/Terms of Use:

MIT-0

## Use Case:

Internal control and compliance teams use this skill to turn monthly operational, complaint, supplier, and incident data into management-ready compliance reports with summaries, trend tables, major incidents, and next-month action items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste unnecessary personal identifiers, privileged legal details, or confidential case text into the agent environment.

Mitigation: Remove unnecessary sensitive details before use unless an approved internal process allows that information in the agent environment.

Risk: Monthly reports can be incomplete or misleading when required operational data is missing.

Mitigation: Use the skill's simplified or data-insufficient reporting modes and explicitly mark data gaps before management review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nic-yuan/skills/inter-control-05-monthly-report)
- [Referenced glossary](docs/GLOSSARY.md)
- [Referenced insufficiency handling](docs/INSUFFICIENCY-HANDLING.md)
- [Referenced rule update SOP](docs/RULE-UPDATE-SOP.md)
- [Referenced output conflict SOP](docs/LINKING-SOP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown-style Chinese compliance report with tables and action-oriented summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided monthly business data; can produce simplified reports when data is incomplete.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata); artifact frontmatter reports 1.7.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
