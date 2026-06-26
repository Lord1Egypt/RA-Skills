## Description: <br>
Configures multiple OpenClaw Lark agents for the official @larksuite/openclaw-lark plugin, including thread sessions, reply modes, block streaming, and per-agent Feishu credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cchenwei](https://clawhub.ai/user/cchenwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to collect Lark agent details, preview configuration with dry runs, and run setup commands that create or update local multi-agent configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper can modify local OpenClaw configuration, create agent directories, and adjust session or inter-agent settings. <br>
Mitigation: Run with --dry-run first, review the proposed configuration changes, and restart the gateway only after approval. <br>
Risk: Feishu/Lark app secrets are stored in the local ~/.openclaw/openclaw.json configuration file. <br>
Mitigation: Use appropriate local file permissions, provide only required credentials, and rotate secrets if the local configuration is exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cchenwei/lark-multi-agent-factory) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide local OpenClaw configuration changes and Feishu/Lark credential storage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
