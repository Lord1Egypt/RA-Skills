## Description:

Checks an OpenClaw workspace for environment setup, file integrity, gateway status, backup status, log errors, disk usage, permissions, and related issues, then reports findings and suggested manual fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tangsuann](https://clawhub.ai/user/tangsuann)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run local health checks before troubleshooting, after environment updates, or during periodic OpenClaw maintenance. It is intended to inspect and report problems without automatically modifying configuration, installing packages, or restarting services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security scan reports broad local shell checks and a command-injection risk through log filenames.

Mitigation: Review before installing, run only in trusted OpenClaw workspaces, and harden log-reading command construction to avoid shell interpretation before use on shared or untrusted systems.

Risk: The diagnostic script reads local OpenClaw configs, logs, selected skill files, environment-variable presence, disk paths, and backup paths.

Mitigation: Use it only when local diagnostic access to those paths is acceptable, and avoid running it in environments where untrusted users can influence inspected files or filenames.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tangsuann/skills/openclaw-self-check)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with pass, warning, issue, and suggested manual fix sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports whether API keys are configured without displaying their values.]

## Skill Version(s):

2.1.0 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
