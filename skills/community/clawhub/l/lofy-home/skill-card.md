## Description: <br>
Smart home control for the Lofy AI assistant — scene modes (study, chill, sleep, morning, grind), device management via Home Assistant REST API, presence-based automation, natural language commands for lights, music, thermostat, and PC wake-on-LAN. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrey401](https://clawhub.ai/user/harrey401) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and smart-home operators use this skill to control Home Assistant devices, activate scene modes, manage lights, media, thermostat settings, and wake a PC from natural-language commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change real smart-home devices using broad natural-language commands. <br>
Mitigation: Review the quick-command phrases before installation and require explicit confirmation for multi-device scenes, presence modes, HVAC changes, and wake-on-LAN actions. <br>
Risk: Home Assistant credentials may allow broad device access. <br>
Mitigation: Use a least-privilege Home Assistant token and keep the integration on a trusted local network. <br>
Risk: Misconfigured entity IDs or unreachable Home Assistant services can cause failed or unintended actions. <br>
Mitigation: Configure device entity IDs explicitly, prompt when mappings are missing, and report unreachable services with a connection-check recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/harrey401/lofy-home) <br>
- [Publisher profile](https://clawhub.ai/user/harrey401) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline JSON and bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces brief action confirmations, device-failure reports, configuration prompts, and Home Assistant REST API command guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
