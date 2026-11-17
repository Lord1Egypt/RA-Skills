## Description:

ShipStation (shipstation.com). Use this skill for ANY ShipStation request — searching and reading data. Whenever a task involves ShipStation, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can retrieve ShipStation inventory levels, warehouse details, and purchase order information through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup can install software or make broader agent changes beyond the ShipStation read tasks.

Mitigation: Review the installer or selected release and approve CLI setup separately; review or disable automatic skill synchronization before allowing it.

Risk: The connected account can expose ShipStation data to the skill.

Mitigation: Grant only the ShipStation access needed for the requested work.

## Reference(s):

- [ShipStation API documentation](https://docs.shipstation.com/getting-started)
- [ShipStation](https://www.shipstation.com/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ShipStation skill release on ClawHub](https://clawhub.ai/oomol/skills/oo-ship-station)

## Skill Output:

**Output Type(s):** [JSON, text, guidance]

**Output Format:** [JSON data with concise natural-language explanations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only inventory, warehouse, and purchase-order information.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
