## Description:

SF Express (open.sf-express.com). Use this skill for ANY SF Express request — reading, creating, updating, and deleting data. Whenever a task involves SF Express, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Operations teams use this skill to query shipment details and manage SF Express orders, tracking, freight services, printing, and station workflows through a connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Child waybill numbers may be allocated without confirming the target order and quantity.

Mitigation: Confirm the target order and requested quantity before allocating child waybill numbers.

Risk: The setup instructions run a remote installer whose release has not been verified.

Mitigation: Install the oo CLI separately from a verified release instead of running the mutable remote installer automatically.

Risk: Connecting an account permits sensitive shipment data and approved business changes to pass through OOMOL; external runtime behavior was not verified.

Mitigation: Use an approved account and review each requested operation and its effect before execution.

## Reference(s):

- [SF Express developer portal](https://open.sf-express.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [SF Express ClawHub release](https://clawhub.ai/oomol/skills/oo-sf-express)

## Skill Output:

**Output Type(s):** [API responses, JSON, Shell commands, Guidance]

**Output Format:** [Structured shipment data and concise natural-language guidance; shell commands may be used to invoke actions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions can read shipment data or change shipment and station records; review the intended effect before state-changing actions.]

## Skill Version(s):

1.0.5 (source: frontmatter, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
