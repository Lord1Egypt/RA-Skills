## Description:

Provides read-only monitoring and analysis for energy and substation telemetry over IEC 60870-5-104, DNP3, and IEC 61850 MMS.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and utility operations engineers use this skill to inspect substation telemetry, check protocol links, analyze event sequences, and diagnose data quality. It supports read-only monitoring over IEC-104, DNP3, and IEC 61850 MMS.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan was partial because three referenced paths were absent, so the benign verdict has incomplete context.

Mitigation: Review the missing paths and install only if the unavailable context is acceptable.

Risk: Interrogations and integrity polls generate real traffic on operational links.

Mitigation: Use only on authorized targets; check link status first and keep reads within the approved scope.

## Reference(s):

- [Industrial-AIOps Energy release page](https://clawhub.ai/zw008/skills/iaiops-energy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Analysis, Guidance]

**Output Format:** [Text or Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only telemetry results and analysis; available details depend on the selected protocol and configured target.]

## Skill Version(s):

0.2.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
