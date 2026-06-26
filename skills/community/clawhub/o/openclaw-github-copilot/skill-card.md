## Description: <br>
Use GitHub Copilot as your OpenClaw coding agent via the built-in copilot-bridge for first-time setup, default-model switching, auth or alias troubleshooting, and the shortest working path to `copilot-bridge/github-copilot`. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yanglinzhen](https://clawhub.ai/user/yanglinzhen) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to configure GitHub Copilot as the default OpenClaw coding agent, validate Copilot availability, run the official login flow when needed, and troubleshoot model alias or session issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper scripts can change the configured OpenClaw default model. <br>
Mitigation: Review the command path first, then confirm the result with `openclaw models status --plain`. <br>
Risk: GitHub Copilot authentication may require an interactive browser or device-code flow. <br>
Mitigation: Use the official `openclaw models auth login-github-copilot` command in a trusted interactive terminal. <br>
Risk: Command execution in a development or maintainer context may carry account or environment authority. <br>
Mitigation: Use least-privilege credentials and non-production environments unless production authority is intentionally required. <br>


## Reference(s): <br>
- [OpenClaw CLI model documentation](https://docs.openclaw.ai/cli/models) <br>
- [ClawHub skill page](https://clawhub.ai/yanglinzhen/openclaw-github-copilot) <br>
- [Setup Guide](references/setup-guide.md) <br>
- [Troubleshooting](references/troubleshooting.md) <br>
- [Publish Checklist](references/publish-checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance is operational and centered on OpenClaw CLI commands, status checks, authentication, and default-model configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
