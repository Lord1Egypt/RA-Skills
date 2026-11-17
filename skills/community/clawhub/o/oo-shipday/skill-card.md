## Description:

Use Shipday through an OOMOL-connected account to read, create, update, and delete delivery data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users of a Shipday account can ask an agent to retrieve orders and carrier information, track delivery progress, and manage delivery orders through the oo CLI connector.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run an unverified remote installer, and its dependency may change other agent skills.

Mitigation: Review and install a verified CLI release before enabling the skill, and review or disable automatic agent-skill synchronization.

Risk: Order creation and edits change Shipday data, while deletion removes an order.

Mitigation: Keep approval for the exact payload and effect of each order change, and require explicit approval for the deletion target.

Risk: Delivery data passes through OOMOL.

Mitigation: Confirm this data flow is acceptable for the connected Shipday account.

## Reference(s):

- [Shipday](https://www.shipday.com/)
- [Shipday API documentation](https://docs.shipday.com/reference)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, API Calls, Shell commands, Guidance]

**Output Format:** [Natural language responses, oo CLI commands, and JSON payloads]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Order creation and edits require user approval; deletions require explicit approval.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
