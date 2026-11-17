## Description:

Deploy and start OpenClaw Agent Control with one command (backend + frontend) using skill-based workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiangagentlabs](https://clawhub.ai/user/jiangagentlabs)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to deploy, start, and validate an OpenClaw Agent Control backend and frontend from a ClawHub skill workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill deploys mutable remote code and npm scripts with broad host and network impact.

Mitigation: Review scripts/deploy_project.sh and the target repository before running it, and prefer a pinned, trusted commit.

Risk: The default deployment path and service binding can expose more host privileges or network access than intended.

Mitigation: Run the deployment as an unprivileged user outside /root and restrict MONITOR_PORT and PORT to trusted interfaces.

Risk: A custom REPO_URL can change the deployed code and dependency tree.

Mitigation: Use a custom REPO_URL only when the repository and npm dependencies are fully trusted.

## Reference(s):

- [Usage (EN)](references/USAGE.en.md)
- [Usage (ZH-CN)](references/USAGE.zh-CN.md)

## Skill Output:

**Output Type(s):** [shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and deployment guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include service URLs, log paths, port settings, environment variables, and validation steps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
