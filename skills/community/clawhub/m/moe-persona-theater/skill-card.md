## Description: <br>
Moe Persona Theater gives OpenClaw six ACG-style persona voices for explicit role switching, multi-turn consistency, and technical replies that keep the persona light while preserving clear content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wjp-cn](https://clawhub.ai/user/wjp-cn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to switch OpenClaw between six distinct ACG-style role voices for chat, support, and technical work while preserving clear task output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The selected persona is stored locally in ~/.openclaw/voice-hub.json until cleared. <br>
Mitigation: Use the switchboard clear command or remove the local state file before resetting behavior or sharing the environment. <br>
Risk: Persona styling may change tone or language, including Chinese ACG-style responses. <br>
Mitigation: Clear the active persona or lower persona intensity for formal, professional, or high-precision technical work. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/wjp-cn/moe-persona-theater) <br>
- [README](artifact/README.md) <br>
- [Usage guide](artifact/guide.md) <br>
- [Role roster](artifact/roster.md) <br>
- [Scene examples](artifact/scenes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and plain text with optional shell commands for the local switchboard script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May persist the selected persona in ~/.openclaw/voice-hub.json until cleared.] <br>

## Skill Version(s): <br>
1.0.0 (source: changelog, package.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
