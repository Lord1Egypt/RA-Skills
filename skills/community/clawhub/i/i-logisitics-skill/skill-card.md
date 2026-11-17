## Description:

JD International Logistics data query skill for shipment tracking, international supply-chain operating metrics, and cross-border small-parcel experience metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jdl-external-skills](https://clawhub.ai/user/jdl-external-skills)

### License/Terms of Use:

MIT-0

## Use Case:

External logistics operators and developers use this skill to query JD international shipment traces, supply-chain operations indicators, and cross-border small-parcel experience indicators through OpenClaw agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses JD logistics tokens to call external logistics APIs.

Mitigation: Use only narrowly scoped tokens, avoid storing secrets in shared user profiles or ~/.env, and rotate credentials if exposure is suspected.

Risk: The bundled security evidence flags TLS bypass behavior as a production concern.

Mitigation: Restore certificate verification before production deployment and review outbound API endpoints during installation.

Risk: Command templates accept user-supplied query values.

Mitigation: Validate and quote user-provided values before command execution, and do not run templates with raw user input.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jdl-external-skills/skills/i-logisitics-skill)
- [Setup guide](artifact/README.md)
- [Logistics trace skill documentation](artifact/skills/joy-logistics-trace/SKILL.md)
- [Logistics indicator skill documentation](artifact/skills/joy-logistics-indicator/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include logistics tracking records, metric query results, command templates, and setup instructions.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
