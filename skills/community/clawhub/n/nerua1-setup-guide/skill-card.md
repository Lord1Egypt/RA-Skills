## Description: <br>
Battle-tested setup guide for a multi-agent AI system on Apple Silicon, covering install order, local and cloud model trade-offs, shared memory, inter-agent communication, backup practices, and operational pitfalls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nerua1](https://clawhub.ai/user/nerua1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill as an operational setup guide for building and maintaining a multi-agent AI workflow on Apple Silicon, including OpenClaw, Claude Code, local models, shared memory, and messaging integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guide discusses disabling sandboxing for external-volume and symlink workflows, which can increase exposure if applied broadly. <br>
Mitigation: Keep sandboxing enabled unless a specific external-volume problem requires an exception, and document any exception before using it. <br>
Risk: Persistent multi-agent memory can unintentionally retain secrets or sensitive operational details. <br>
Mitigation: Use a dedicated memory vault with no secrets and review what is stored before mining or sharing memory across agents. <br>
Risk: WhatsApp mirroring can forward logs and prompts outside the local console. <br>
Mitigation: Enable WhatsApp mirroring only for channels where prompts, logs, and notifications are safe to forward. <br>
Risk: Related skills or commands referenced by the guide may change local configuration or credentials. <br>
Mitigation: Review and scan related skills before installation, and inspect proposed commands before running them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nerua1/nerua1-setup-guide) <br>
- [Publisher profile](https://clawhub.ai/user/nerua1) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only guidance; commands should be reviewed before execution in the target environment.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
