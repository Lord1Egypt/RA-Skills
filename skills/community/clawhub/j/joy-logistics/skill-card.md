## Description:

Queries JD International Logistics tracking data, global supply-chain operating indicators, and cross-border package experience metrics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[joy-logistics](https://clawhub.ai/user/joy-logistics)

### License/Terms of Use:

MIT-0

## Use Case:

Logistics and operations users can ask an agent to retrieve shipment tracking details, supply-chain operating indicators, and cross-border package fulfillment metrics from JD logistics services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API tokens and logistics data may be exposed if credentials are stored broadly or reused.

Mitigation: Use narrowly scoped, revocable tokens and avoid storing credentials in shell startup files.

Risk: The helper scripts disable normal TLS certificate validation for HTTPS requests.

Mitigation: Restore standard TLS certificate validation before production use.

Risk: Command invocation guidance can be mishandled if untrusted input is assembled into shell strings.

Mitigation: Run scripts only from trusted environments and use safe argument-array execution when automating calls.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/joy-logistics/skills/joy-logistics)
- [ISC platform](http://isc.jd.com)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, JSON]

**Output Format:** [Markdown tables and narrative summaries, with JSON returned by helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a token environment variable and returns logistics or metrics data from external JD/Ochama API calls.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
