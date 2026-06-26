## Description: <br>
Mi-MemoryStack is a personalized memory framework that retrieves and stores user memories so an agent can preserve user context across conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Nikol-coder](https://clawhub.ai/user/Nikol-coder) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add cross-session memory retrieval and asynchronous memory saving for agents that need user preferences, identity context, and conversation continuity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically store and send user IDs and conversation text to an API endpoint configured in the source files. <br>
Mitigation: Use only an endpoint you control, move secrets out of code, add explicit opt-in and opt-out controls, redact sensitive content, and define retention and deletion behavior before deployment. <br>
Risk: The skill can replace core OpenClaw workspace instructions and make memory retrieval and saving mandatory in every turn. <br>
Mitigation: Review and narrow or remove the bundled workspace instruction overrides before deployment, and ensure users can disable memory behavior when appropriate. <br>
Risk: The release security verdict is suspicious because the behavior requires careful review even though it is not clearly malicious. <br>
Mitigation: Install only after source review and security review, then monitor daemon activity and API calls during operation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Nikol-coder/mi-memorystack) <br>
- [Installation guide](artifact/安装教程.md) <br>
- [Workspace instruction template](artifact/xiugai/AGENTS.md) <br>
- [Persona template](artifact/xiugai/SOUL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown instructions with shell commands and JSON command output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start a background memory daemon, write local queue files, and call a configured API endpoint for memory search and save operations.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
