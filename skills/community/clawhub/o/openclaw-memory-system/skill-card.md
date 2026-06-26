## Description: <br>
OpenClaw 记忆系统 adds multimodal memory, project/agent/user isolation, natural-language correction, and version control for OpenClaw agents. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nick-Liu1989](https://clawhub.ai/user/Nick-Liu1989) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers running OpenClaw instances use this skill to persist and retrieve text, image, and tool-call memories, isolate those memories by project, agent, and user, and correct stored memories from natural-language feedback. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores persistent user, project, image, and tool-call memories without clear privacy, retention, or sharing boundaries in the evidence. <br>
Mitigation: Define allowed memory categories, retention expectations, and sharing rules before deployment; disable or tightly scope cross-user sharing. <br>
Risk: Server security evidence reports inconsistent packaging, including missing skills/, configs/, tests/, and scripts/postinstall.js. <br>
Mitigation: Confirm the complete package contents with the publisher and review installation behavior before enabling the skill. <br>
Risk: Optional Feishu integration can send memory data to an external service. <br>
Mitigation: Configure Feishu only when external transmission of memory data is approved, and avoid sending sensitive memory content. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/Nick-Liu1989/openclaw-memory-system) <br>
- [README.md](artifact/README.md) <br>
- [QUICKSTART.md](artifact/QUICKSTART.md) <br>
- [RELEASE.md](artifact/RELEASE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with JavaScript examples, shell commands, and JSON configuration snippets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces instructions and examples for persistent memory storage, namespace configuration, memory correction, and optional Feishu integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata, manifest.json, package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
