## Description: <br>
Enable and configure Moltbot/Clawdbot memory search for persistent context, including memorySearch configuration, MEMORY.md, daily logs, and vector search setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Gwsq](https://clawhub.ai/user/Gwsq) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to configure persistent memory search for Moltbot/Clawdbot agents, organize workspace memory files, and troubleshoot memory recall behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Memory indexing can expose secrets, credentials, regulated data, or sensitive personal details if those values are stored in memory files or indexed sessions. <br>
Mitigation: Keep sensitive data out of indexed memory sources; use the local embedding provider for sensitive work, or review remote provider data-handling terms before enabling Voyage or OpenAI embeddings. <br>
Risk: Incorrect memory configuration can produce missing or irrelevant recall results. <br>
Mitigation: Verify memorySearch is enabled, restart the gateway after configuration changes, confirm MEMORY.md exists, and tune minScore or maxResults when results are too narrow or noisy. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/Gwsq/memory-setup-1-0-0) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, configuration, shell commands] <br>
**Output Format:** [Markdown with JSON configuration examples and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides step-by-step setup, verification, and troubleshooting guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
