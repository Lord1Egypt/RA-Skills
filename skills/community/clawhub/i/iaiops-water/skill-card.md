## Description:

Provides read-only water-treatment operations analysis across Modbus, OPC-UA, and HART-IP instrumentation, with cross-protocol diagnostics for data quality, downtime, alarms, and OEE.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Water-treatment operators, developers, and engineers can use the skill to inspect read-only plant instrumentation and analyze water-quality readings, alarms, data quality, and downtime. It supports operational review while leaving site-specific limits and treatment decisions to qualified personnel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Water-quality compliance results depend on configured limits and supplied required CT values, which may not match the site's permit or applicable requirements.

Mitigation: Confirm limits and required CT values against the current permit and applicable state requirements before relying on results.

Risk: Cross-protocol downtime or upstream attribution can be misleading when timestamps or declared line relationships are incomplete.

Mitigation: Verify timestamps and declared equipment relationships with site records before treating an attribution as causal.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zw008/skills/iaiops-water)
- [Publisher profile](https://clawhub.ai/user/zw008)

## Skill Output:

**Output Type(s):** [Analysis, Guidance, Text, Configuration instructions]

**Output Format:** [Markdown and structured tool results, with configuration or shell guidance when relevant]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on supplied readings, site configuration, and applicable limits.]

## Skill Version(s):

0.34.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
