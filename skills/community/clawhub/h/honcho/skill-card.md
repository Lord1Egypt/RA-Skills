## Description: <br>
Installs and enables @honcho-ai/openclaw-honcho, runs setup to configure Honcho memory, and restarts the OpenClaw gateway while disclosing external upload and ongoing conversation observation behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VVoruganti](https://clawhub.ai/user/VVoruganti) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install Honcho memory support, migrate selected legacy memory files with confirmation, and enable ongoing memory recall across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected memory files and ongoing conversation content can be sent to Honcho or a configured self-hosted endpoint. <br>
Mitigation: Install only in workspaces where this upload is acceptable, review the file list and destination during setup, and proceed only after explicit confirmation. <br>
Risk: Observation and network activity continue across sessions while the plugin remains enabled. <br>
Mitigation: Disable the plugin with openclaw plugins disable openclaw-honcho when ongoing observation is not desired. <br>
Risk: The Honcho API key and plugin configuration are written to ~/.openclaw/openclaw.json. <br>
Mitigation: Use a revocable Honcho API key and protect access to the local OpenClaw configuration file. <br>


## Reference(s): <br>
- [Long Term Memory with Honcho on ClawHub](https://clawhub.ai/VVoruganti/honcho) <br>
- [Honcho](https://honcho.dev) <br>
- [Honcho App](https://app.honcho.dev) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires interactive confirmation before data upload; may write OpenClaw configuration and enable ongoing network activity.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
