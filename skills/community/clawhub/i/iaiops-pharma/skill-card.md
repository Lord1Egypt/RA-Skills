## Description:

Provides pharmaceutical manufacturing agents with read-first guidance and diagnostics for cleanroom, process-water, and GMP operations across BACnet/IP, Modbus, HART-IP, and OPC UA.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zw008](https://clawhub.ai/user/zw008)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, automation engineers, and validation teams use it to inspect industrial signals, assess cleanroom and pharmaceutical-water readings against site-supplied limits, investigate alarms and downtime, and prepare configuration or evidence outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad activation terms may cause the skill to be invoked for unrelated requests.

Mitigation: Invoke it only for relevant pharmaceutical or industrial-control tasks, consistent with ClawScan guidance.

Risk: Network discovery or device interaction may reach industrial systems.

Mitigation: Use discovery and device operations only with an authorized target.

Risk: A BACnet write can affect facility controls, and an assessment without verified site limits may be incomplete.

Mitigation: Keep BACnet writes within the site's MOC and approval process; provide verified site limits and treat missing-limit results as ungraded.

## Reference(s):

- [Industrial-AIOps Pharma on ClawHub](https://clawhub.ai/zw008/skills/iaiops-pharma)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Structured diagnostic results and operational guidance, typically JSON or Markdown, with configuration drafts when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-first; assessments depend on supplied readings, declared relationships, and site-approved limits. Missing limits are identified rather than treated as passing.]

## Skill Version(s):

0.34.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
