## Description: <br>
Control Xiaomi smart home devices via Home Assistant API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Pipluuup](https://clawhub.ai/user/Pipluuup) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and home automation operators use this skill to translate Xiaomi or Xiao AI device requests into Home Assistant service calls for configured speakers, air conditioners, and other smart home devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token-backed Home Assistant API calls can change real Xiaomi smart home devices. <br>
Mitigation: Use a dedicated least-privilege Home Assistant token and install only when device control is intended. <br>
Risk: Broad natural-language triggers may send unintended state-changing commands. <br>
Mitigation: Restrict the Home Assistant URL and entity list, and require explicit confirmation for ambiguous or state-changing requests. <br>
Risk: Access tokens can be exposed if placed in shared prompt or configuration files. <br>
Mitigation: Keep tokens in a secure environment variable or protected local configuration and avoid logging them. <br>


## Reference(s): <br>
- [Home Assistant Entity Reference](references/entities.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Pipluuup/haxiaomicontrol) <br>
- [Publisher Profile](https://clawhub.ai/user/Pipluuup) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON payload examples, and Python helper code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Home Assistant entity IDs, service names, HA_URL, and HA_TOKEN supplied by the user environment or configuration.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
