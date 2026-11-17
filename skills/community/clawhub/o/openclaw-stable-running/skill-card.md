## Description:

OpenClaw Stable Running provides operations guidance and scripts for keeping an OpenClaw gateway running continuously with process supervision, health checks, reconnection, resumable tasks, cleanup, and monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[foxyy1126](https://clawhub.ai/user/foxyy1126)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to configure OpenClaw for unattended operation with service supervision, automatic restart, reconnect behavior, resumable task state, resource cleanup, and log monitoring.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent service, PM2, and cron setup can change host behavior if applied without deployment review.

Mitigation: Confirm each command and path against the target deployment, run under a dedicated low-privilege openclaw user where possible, and prepare rollback steps before unattended use.

Risk: The network monitor can change the default route without enough safeguards.

Mitigation: Fix and test the routing logic with known interface names before enabling it, and keep it disabled until route changes are reviewed.

Risk: Environment files used by service managers may contain secrets.

Mitigation: Protect the .env file with strict permissions and avoid exposing secret values in logs or shared configuration.

Risk: Cleanup automation can remove logs or temporary files needed for diagnosis.

Mitigation: Scope cleanup paths narrowly, validate retention settings, and test deletion behavior before scheduling the script.

## Reference(s):

- [Task Resume Reference](references/task-resume.md)
- [OpenClaw Documentation](https://docs.openclaw.ai)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with shell, JavaScript, YAML, INI, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational runbooks and script/configuration examples for OpenClaw service supervision and recovery.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
