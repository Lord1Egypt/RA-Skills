## Description: <br>
OpenClaw Omni Expert helps agents install, configure, diagnose, automate, and remotely support OpenClaw environments through remote desktop tooling, workflow orchestration, monitoring, and troubleshooting guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thinkbugs](https://clawhub.ai/user/thinkbugs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and support operators use this skill to install and configure OpenClaw, diagnose OpenClaw issues, create agents and workflows, and perform remote support tasks through supported remote-control software. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad unattended authority to change local or remote computers. <br>
Mitigation: Review commands before running autopilot or fix-all modes, and avoid production machines unless backups are available. <br>
Risk: Remote support workflows may expose sensitive screenshots, session credentials, SSH keys, API keys, or other secrets. <br>
Mitigation: Use least-privileged remote accounts and provide credentials only when the publisher and target workflow are trusted. <br>
Risk: Automated repair actions may make incorrect or unwanted system changes. <br>
Mitigation: Run diagnostics first, confirm proposed fixes, and keep a recovery path before allowing automated remediation. <br>


## Reference(s): <br>
- [OpenClaw Omni Expert ClawHub Release](https://clawhub.ai/thinkbugs/openclaw-omni-expert) <br>
- [OpenClaw Agent and Workflow Orchestration Guide](references/agent-workflow-guide.md) <br>
- [OpenClaw Configuration Best Practices](references/config-best-practices.md) <br>
- [OpenClaw Desktop Remote Guide](references/desktop-remote-guide.md) <br>
- [OpenClaw Intelligent Diagnosis Guide](references/intelligent-diagnosis-guide.md) <br>
- [OpenClaw Remote Support Guide](references/remote-support.md) <br>
- [OpenClaw System Requirements](references/system-requirements.md) <br>
- [OpenClaw Troubleshooting Guide](references/troubleshooting-guide.md) <br>
- [RustDesk Releases](https://github.com/rustdesk/rustdesk/releases) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with command examples, configuration snippets, and code-oriented instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include remote-support and automated repair steps that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
