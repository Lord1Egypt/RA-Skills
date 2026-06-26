## Description: <br>
Control Home Assistant smart home devices, lights, scenes, and automations via moltbot-ha CLI with configurable safety confirmations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iamvaleriofantozzi](https://clawhub.ai/user/iamvaleriofantozzi) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External users and smart-home developers use this skill to let an agent discover and control Home Assistant entities through the moltbot-ha CLI while preserving confirmation flows for critical devices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can help an agent control smart-home devices, including devices that may affect physical safety or security. <br>
Mitigation: Keep confirmation enabled for locks, alarms, garage doors, covers, scripts, and automations, and require explicit user approval before any forced critical action. <br>
Risk: A broad Home Assistant token can grant more device access than the user intends. <br>
Mitigation: Use a dedicated Home Assistant token where possible, keep HA_TOKEN out of files and logs, and configure allowed_entities and blocked_entities for sensitive devices. <br>
Risk: The release depends on the external moltbot-ha CLI package. <br>
Mitigation: Install only after verifying trust in the external package and publisher. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/iamvaleriofantozzi/moltbot-ha) <br>
- [Home Assistant REST API documentation](https://developers.home-assistant.io/docs/api/rest/) <br>
- [Moltbot documentation](https://docs.molt.bot/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference JSON output from the moltbot-ha CLI when users request programmatic state data.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata and CHANGELOG, released 2026-02-02) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
