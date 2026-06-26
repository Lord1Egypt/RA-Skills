## Description: <br>
Helps agents check and update ProxyGate CLI, SDK dependencies, installed skills, and the update-check cache when ProxyGate updates are requested or detected. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jwelten](https://clawhub.ai/user/jwelten) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to keep ProxyGate CLI, SDK dependencies, and installed ProxyGate skills current after an explicit update request or a detected update notification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can lead an agent to change global npm packages, project dependencies, installed ProxyGate skills, and local update-cache state. <br>
Mitigation: Confirm the update is specifically for ProxyGate, review exact commands and target versions before execution, and verify the installed CLI version after updating. <br>
Risk: Broad triggers such as generic CLI or SDK upgrade requests could cause unintended ProxyGate updates. <br>
Mitigation: Do not treat generic prompts like upgrade cli as approval to update ProxyGate without explicit user confirmation. <br>


## Reference(s): <br>
- [ProxyGate CLI Command Reference](references/commands.md) <br>
- [ProxyGate Gateway Docs](https://gateway.proxygate.ai/docs) <br>
- [ClawHub skill page](https://clawhub.ai/jwelten/pg-update) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Markdown with inline bash commands and checklists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose npm package updates, ProxyGate skill refreshes, and local cache file changes.] <br>

## Skill Version(s): <br>
0.2.1 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
