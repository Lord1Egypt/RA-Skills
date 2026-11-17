## Description:

Manage 节点小宝 (Node Baby Link / JDxB) remote access service on Linux, including installation, service control, status checks, logs, pairing codes, updates, and uninstall.

This skill is ready for commercial/non-commercial use.

## Publisher:

[skipper-chen](https://clawhub.ai/user/skipper-chen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and Linux operators use this skill to manage a JDxB remote-access service from an agent session, including install, service lifecycle, logs, pairing, and removal tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install and update actions can download remote JDxB archives and run the resulting service with persistent root-level execution.

Mitigation: Use only on a trusted Linux host, review the installer path before use, and verify the download source and archive integrity before running install or update.

Risk: The documented curl-to-sudo-bash path executes remote content directly with elevated privileges.

Mitigation: Avoid the one-liner; fetch installer content separately, inspect it, and run only the reviewed script with the minimum necessary privileges.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/skipper-chen/skills/jdxb)
- [Publisher profile](https://clawhub.ai/user/skipper-chen)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs focus on Linux service management actions for the bundled JDxB script.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
