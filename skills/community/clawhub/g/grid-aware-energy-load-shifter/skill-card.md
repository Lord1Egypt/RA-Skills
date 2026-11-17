## Description:

Grid-aware energy load shifter for Home Assistant that reads electricity prices, solar forecasts, battery state of charge, and consumption data to schedule deferrable household loads during lower-cost or solar-aligned windows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mrbese](https://clawhub.ai/user/mrbese)

### License/Terms of Use:


## Use Case:

External users and home energy automation developers use this skill to inspect Home Assistant energy entities, estimate load-shifting opportunities, and issue constrained energy-related service calls for devices such as EV chargers, HVAC, water heaters, batteries, and pool pumps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access Home Assistant data and control energy-related household devices when provided with HA_URL and HA_TOKEN.

Mitigation: Use a dedicated low-privilege Home Assistant account, prefer HTTPS, avoid broad admin tokens, and test read-only commands before allowing device control.

Risk: Energy-related service calls may still affect HVAC, water heaters, chargers, scripts, or automations.

Mitigation: Review every call-service target, require explicit confirmation for control actions, and apply an entity allowlist for devices the skill may operate.

Risk: The security scan states that the skill can read and control more household devices than its energy-focused framing clearly limits.

Mitigation: Install only when this Home Assistant access scope is acceptable and keep the skill restricted to documented energy-related domains and entities.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mrbese/skills/grid-aware-energy-load-shifter)
- [Home Assistant Energy Entity Reference](references/energy_entities.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON-producing shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The included Home Assistant bridge commands emit JSON to stdout and require HA_URL and HA_TOKEN environment variables.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
