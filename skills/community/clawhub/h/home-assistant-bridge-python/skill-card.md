## Description: <br>
Control Home Assistant devices, read sensors, and manage automations using the Python Bridge. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mischa-Petschenig](https://clawhub.ai/user/Mischa-Petschenig) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent query and control a Home Assistant instance through its REST API, including lights, switches, climate devices, scenes, entity state, history, services, and alias mappings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can control real Home Assistant devices, including safety-sensitive device categories when exposed through Home Assistant. <br>
Mitigation: Require explicit user confirmation before commands that affect locks, doors, alarms, garage doors, climate, scenes, or other safety-sensitive devices. <br>
Risk: The setup script stores a long-lived Home Assistant access token in ~/.homeassistant.conf and expects users to source that file. <br>
Mitigation: Use a dedicated, least-privilege, revocable Home Assistant token; keep ~/.homeassistant.conf protected; and avoid loading it from shared shell startup files. <br>
Risk: A compromised token could allow broad access to the configured Home Assistant instance. <br>
Mitigation: Rotate the token if exposure is suspected and review the configured Home Assistant permissions and accessible entities before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Mischa-Petschenig/home-assistant-bridge-python) <br>
- [Home Assistant long-lived access token documentation](https://www.home-assistant.io/docs/authentication/#your-account-profile) <br>
- [Entity ID reference](references/finding-entities.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON examples, and Python command invocations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May execute local Python and shell commands that call a configured Home Assistant REST API and print JSON, status text, or formatted command results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
