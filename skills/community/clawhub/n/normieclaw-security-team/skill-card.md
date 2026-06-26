## Description: <br>
Automates security, platform, and memory audits for an OpenClaw environment, reporting critical risks that need attention. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nollio](https://clawhub.ai/user/nollio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to run security scans, platform health checks, memory audits, accepted-risk tracking, and trend summaries for OpenClaw workspaces. It can support manual checks or scheduled audit workflows when the user has reviewed the configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad local scans may inspect secrets, project files, and git history. <br>
Mitigation: Keep scan_directories narrow, review the configured targets before running, and avoid sharing audit outputs because they may describe sensitive findings. <br>
Risk: Network-capable health checks and optional dashboard or webhook workflows may expose operational details if configured carelessly. <br>
Mitigation: Use only intended domains and services, and leave scheduled scans, dashboard sync, and webhook sync disabled until the data flow is understood. <br>
Risk: Server security review marked the release suspicious and noted that its read-only and local-only claims may be overstated. <br>
Mitigation: Review or fix the shell scripts before relying on the skill as a security monitor, especially in workspaces containing secrets. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/nollio/normieclaw-security-team) <br>
- [README.md](README.md) <br>
- [SECURITY.md](SECURITY.md) <br>
- [DASHBOARD-SPEC.md](dashboard-kit/DASHBOARD-SPEC.md) <br>
- [NormieClaw support](https://normieclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports with JSON scan results, remediation guidance, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store audit history and accepted-risk state in local skill data files when configured.] <br>

## Skill Version(s): <br>
1.0.3 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
