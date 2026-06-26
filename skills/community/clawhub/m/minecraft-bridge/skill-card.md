## Description: <br>
Local HTTP bridge for Mineflayer-based live control of a Minecraft Java bot, including state reads and in-game actions such as movement, mining, crafting, following, and chat. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[en1r0py1865](https://clawhub.ai/user/en1r0py1865) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to connect an agent-controlled bot to a live Minecraft Java world, inspect live bot state, and issue bounded in-game actions through the local bridge. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local control API is unauthenticated and can issue live bot actions. <br>
Mitigation: Keep the bridge bound to localhost, do not expose the port publicly, and stop the bridge when it is no longer needed. <br>
Risk: The slash-command endpoint can change the world or other players' experience if the bot has elevated permissions. <br>
Mitigation: Avoid granting operator or cheat-level permissions unless required, and prefer dedicated server administration tools for administrative commands. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/en1r0py1865/minecraft-bridge) <br>
- [Project Homepage](https://github.com/en1r0py1865/minecraft-skill) <br>
- [Minecraft Bridge API Specification](artifact/references/api-spec.md) <br>
- [Minecraft Bridge Dependency Guide](artifact/references/dependency-guide.md) <br>
- [Minecraft Bridge Troubleshooting](artifact/references/troubleshooting.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands, HTTP endpoint guidance, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local setup and runtime guidance for a Minecraft bridge; actions affect the connected game world when the bridge is running.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
