## Description: <br>
Control Raspberry Pi GPIO pins remotely by setting specified pins HIGH or LOW through RPC calls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yevladimir](https://clawhub.ai/user/yevladimir) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent invoke Raspberry Pi GPIO on and off actions against a controlled local Raspberry Pi setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change physical hardware state through Raspberry Pi GPIO pins. <br>
Mitigation: Use it only with hardware you control, avoid safety-critical or high-power devices, and require explicit human confirmation for sensitive actions. <br>
Risk: The GPIO request path relies on a hardcoded local HTTP endpoint. <br>
Mitigation: Edit the endpoint for the target Raspberry Pi, keep it on a controlled local network, and restrict access before deployment. <br>
Risk: Unvalidated actions or pin numbers could reach the Pi-side service. <br>
Mitigation: Add local validation for allowed actions and safe GPIO pins before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yevladimir/led-ctrl) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses an action and GPIO pin parameter for gpio_on and gpio_off operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
