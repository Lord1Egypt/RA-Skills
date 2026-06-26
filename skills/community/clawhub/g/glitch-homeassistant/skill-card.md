## Description: <br>
Control and monitor Home Assistant smart devices using commands for lights, switches, covers, climate, locks, scenes, and scripts through the Home Assistant API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chris6970barbarian-hue](https://clawhub.ai/user/chris6970barbarian-hue) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and developers use this skill to configure Home Assistant access and issue command-line control or status requests for supported smart-home entities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks users to configure a long-lived Home Assistant access token and may save configuration locally. <br>
Mitigation: Verify exactly which ha-cli executable will run before entering a token, prefer a least-privileged Home Assistant account or token, and protect or avoid saved config.json. <br>
Risk: Commands can affect physical smart-home devices, including locks, covers, scenes, scripts, and climate controls. <br>
Mitigation: Require manual confirmation for high-impact actions and review requested commands before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chris6970barbarian-hue/glitch-homeassistant) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke Home Assistant API actions through the user's local ha-cli setup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
