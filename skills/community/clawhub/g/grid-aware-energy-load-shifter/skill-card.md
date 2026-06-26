## Description: <br>
Grid-aware energy load shifter for Home Assistant that reads electricity prices, solar forecasts, battery state, and consumption data to schedule deferrable residential loads into cheaper or solar-rich windows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mrbese](https://clawhub.ai/user/mrbese) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers with Home Assistant use this skill to inspect energy pricing, solar, battery, consumption, and controllable load entities, then plan or execute load shifts for EV charging, HVAC, water heaters, batteries, and demand response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use Home Assistant service calls to control real energy devices such as HVAC, water heaters, batteries, EV chargers, scripts, or automations. <br>
Mitigation: Use a dedicated least-privilege Home Assistant account and token, start with read-only commands, and require manual approval before any call-service action. <br>
Risk: Broad service-call access could affect devices outside the intended energy-management scope if permissions are too permissive. <br>
Mitigation: Keep Home Assistant permissions limited to approved energy entities and rely on the skill's energy-domain allowlist for call-service operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mrbese/grid-aware-energy-load-shifter) <br>
- [Home Assistant Energy Entity Reference](references/energy_entities.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, JSON] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires HA_URL and HA_TOKEN; Home Assistant control actions can affect real energy devices.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
