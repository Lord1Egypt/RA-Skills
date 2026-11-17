## Description:

OpenCLI-RS helps agents use a universal command-line hub to automate websites, desktop applications, local CLI tools, data extraction, and content downloads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smallnest](https://clawhub.ai/user/smallnest)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to discover and run OpenCLI/OpenCLI-RS commands for web automation, desktop app control, external CLI management, data collection, and content downloads.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automate browsers, desktop applications, and local CLI tools with broad access to logged-in accounts and local environments.

Mitigation: Review actions before execution, use a disposable browser profile and least-privilege environment for testing, and require explicit confirmation before posting, deletion, desktop-control, file-sending, Docker, Kubernetes, or bulk-download actions.

Risk: The install path and provenance are inconsistent for the level of access requested, and installation examples use global latest package installation.

Mitigation: Pin and verify any downloaded installer, binary, or package before use, and avoid npm/global latest installs from lifecycle scripts in production environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smallnest/skills/opencli-rs)
- [OpenCLI-RS repository](https://github.com/nashsu/opencli-rs)
- [OpenCLI project](https://github.com/jackwener/opencli)
- [OpenClaw documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code, markdown]

**Output Format:** [Markdown guidance with shell command examples and optional JSON, YAML, CSV, and Markdown command outputs]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Some commands require a browser extension, logged-in website sessions, local desktop application access, or optional download tooling such as yt-dlp.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
