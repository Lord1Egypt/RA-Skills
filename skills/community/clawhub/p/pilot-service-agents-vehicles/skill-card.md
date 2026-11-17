## Description:

Provides NHTSA vehicle record lookups for VIN decoding, makes, models, recalls, and consumer complaints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[teoslayer](https://clawhub.ai/user/teoslayer)

### License/Terms of Use:

AGPL-3.0

## Use Case:

Developers and external users use this skill to discover Pilot Protocol vehicle data agents and query NHTSA vehicle records by VIN or make/model/year.

### Deployment Geography for Use:

Global; data coverage is focused on U.S. vehicle records.

## Known Risks and Mitigations:

Risk: Vehicle lookup inputs, including VINs or make/model/year queries, are sent to external Pilot Protocol service agents.

Mitigation: Submit only vehicle data appropriate for Pilot Protocol processing and review returned records before relying on them.

Risk: Gemini-generated summaries and free-text responses can be incomplete or misleading.

Mitigation: Prefer structured /data queries for factual records and verify summaries against returned source data.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/teoslayer/skills/pilot-service-agents-vehicles)
- [Pilot Protocol](https://pilotprotocol.network)
- [Pilot Skills](https://teoslayer.github.io/pilot-skills/)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Text]

**Output Format:** [Markdown with bash commands, JSON examples, and concise guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Pilot Protocol agent responses may include structured JSON records, plain-text help, or Gemini-generated summaries read through pilotctl inbox.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
