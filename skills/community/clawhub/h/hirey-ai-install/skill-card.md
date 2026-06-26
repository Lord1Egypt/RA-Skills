## Description: <br>
Installs or repairs Hirey AI on a local OpenClaw host through the ClawHub package path, then completes local MCP, receiver, registration, and health-check setup for Hi people-finding workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yzlee](https://clawhub.ai/user/yzlee) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agent operators use this skill to install or repair Hirey AI/Hi on a local OpenClaw host. The configured host can then use Hi to publish people-finding needs, search or receive matches, contact leads, and coordinate follow-up across hiring, housing, friendship, dating, founder, investor, legal, and related workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes real local OpenClaw installation and routing changes, including hook ingress and MCP configuration. <br>
Mitigation: Install it only on an OpenClaw host where Hirey AI/Hi connectivity is intended, and review the setup result before treating the installation as complete. <br>
Risk: The setup generates and stores a hook token and binds the current chat for replies. <br>
Mitigation: Use the skill only on a trusted local host and avoid sharing generated host configuration or tokens. <br>
Risk: The host is registered with the external Hi service. <br>
Mitigation: Proceed only when the user wants this OpenClaw host connected to Hirey AI/Hi for people-finding workflows. <br>
Risk: Force reinstall or cleanup behavior can alter an existing Hirey AI/OpenClaw setup. <br>
Mitigation: Review existing customizations before using force reinstall or cleanup paths. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yzlee/hirey-ai-install) <br>
- [Publisher profile](https://clawhub.ai/user/yzlee) <br>
- [Hirey AI Hi service](https://hi.hirey.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce host setup status, installation handoff guidance, registration instructions, and health-check summaries.] <br>

## Skill Version(s): <br>
0.1.54 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
