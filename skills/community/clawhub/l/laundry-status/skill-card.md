## Description:

Use when the user wants to check washing machine or dryer status, laundry room availability, or which machines are free at Shanghai Jiao Tong University Minhang campus.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rexeno56](https://clawhub.ai/user/rexeno56)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to answer SJTU Minhang campus laundry availability questions, including free washers or dryers, building-specific laundry room status, and estimated machine finish times.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts Haier's IoT service when invoked, so results depend on network availability and the service response.

Mitigation: Surface timeout, network, and API errors to the user and retry later or check connectivity when the service is unavailable.

Risk: Broad English triggers such as washer, dryer, and laundry may activate outside the intended SJTU Minhang campus laundry context.

Mitigation: Invoke the skill only for clearly campus-laundry requests and consider narrowing or documenting triggers during maintenance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rexeno56/skills/laundry-status)
- [ClawHub publisher profile](https://clawhub.ai/user/rexeno56)
- [Haier IoT device detail endpoint](https://yshz-user.haier-ioc.com/position/deviceDetailPage)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text machine status grouped by building, device type, and status, with stderr messages for timeout, network, unknown-building, or API errors.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-backed lookup; defaults to 西21楼 and can query 西16楼 or all configured buildings.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
