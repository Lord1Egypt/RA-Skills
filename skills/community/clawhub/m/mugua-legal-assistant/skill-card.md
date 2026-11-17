## Description:

Connects agents to the Mugua Legal API for legal consultation, case element extraction, and complete case analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yzw23333](https://clawhub.ai/user/yzw23333)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and legal-service teams use this skill to route user questions or case materials to the Mugua Legal API and receive consultation answers, extracted case elements, or case analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send confidential legal data and the API token to a configurable external URL, including a test endpoint.

Mitigation: Install only with a trusted Mugua API endpoint, prevent event or user input from changing base_url, and avoid real privileged or highly sensitive legal documents until the destination and data-handling expectations are approved.

Risk: Users may transmit sensitive legal case materials without understanding where the data is sent.

Mitigation: Require explicit user consent before transmission and use simulated or low-sensitivity data during initial testing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yzw23333/skills/mugua-legal-assistant)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [JSON response containing status fields and legal consultation or case analysis data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes success, code, message, data, and request_id fields.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata and artifact metadata.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
