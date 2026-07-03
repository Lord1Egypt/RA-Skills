## Description: <br>
Provides installation steps, dependency setup, path guidance, and troubleshooting for integrating the memory-tencentdb four-layer memory system with OpenClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paudyyin](https://clawhub.ai/user/paudyyin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure the memory-tencentdb plugin, including dependency placement, OpenClaw configuration, Gateway restart steps, and installation checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The referenced memory plugin can retain conversation history and build long-term user profiles without clearly documented review, deletion, retention, or scoping controls. <br>
Mitigation: Enable it only after confirming where memory data is stored, how users can inspect and delete it, what retention policy applies, and whether broad capture or L3 profiling can be limited or disabled. <br>
Risk: The installation guidance changes OpenClaw Gateway dependencies and configuration, which can affect the local runtime if applied without review. <br>
Mitigation: Review the commands and configuration before applying them, install dependencies from trusted sources, and keep a backup of the existing OpenClaw configuration. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/paudyyin/memory-tencentdb-setup) <br>
- [OpenClaw documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown installation guide with shell command and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language setup guidance for OpenClaw memory-tencentdb integration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
