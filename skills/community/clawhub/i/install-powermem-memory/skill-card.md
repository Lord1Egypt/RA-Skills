## Description: <br>
Step-by-step guide to install and configure the PowerMem long-term memory plugin for OpenClaw, including setup paths, options, troubleshooting, and auto-capture and auto-recall behavior. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teingi](https://clawhub.ai/user/teingi) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install and configure PowerMem as a long-term memory backend. It helps set up local CLI mode or HTTP server mode, verify plugin health, and understand configuration and troubleshooting steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent automatic memory can store sensitive or regulated conversation content longer than intended. <br>
Mitigation: Install only when long-term memory is intended, avoid storing secrets or regulated data, and review or delete memories periodically. <br>
Risk: HTTP server mode can expose memory access if bound broadly without protection. <br>
Mitigation: Prefer local CLI and SQLite mode for personal use; protect HTTP mode with authentication, TLS or a trusted network boundary, and clear access controls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/teingi/install-powermem-memory) <br>
- [PowerMem GitHub repository](https://github.com/oceanbase/powermem) <br>
- [memory-powermem installation guide](https://github.com/ob-labs/memory-powermem/blob/main/INSTALL.md) <br>
- [PowerMem environment example](https://github.com/oceanbase/powermem/blob/master/.env.example) <br>
- [PowerMem issues](https://github.com/oceanbase/powermem/issues) <br>
- [PowerMem Introduction](artifact/powermem-intro.md) <br>
- [Config & Commands Quick Reference](artifact/config-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces installation, verification, configuration, and troubleshooting guidance for PowerMem memory setup.] <br>

## Skill Version(s): <br>
0.2.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
