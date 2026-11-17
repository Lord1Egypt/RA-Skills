## Description:

Connects OpenClaw agents to Pipedream Connect apps with per-agent OAuth isolation, first-class MCP tool exposure, live connected-account discovery, and dynamic catalog browsing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick-software](https://clawhub.ai/user/maverick-software)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to configure, maintain, and troubleshoot the OpenClaw Pipedream integration, including platform credentials, per-agent app connections, MCP tool activation, live catalog discovery, and icon handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles powerful app-access tokens and Pipedream client credentials.

Mitigation: Review and harden token-handling paths, restrict permissions on OpenClaw secrets, mcporter config, logs, and copied scripts, and avoid printing the secrets vault.

Risk: Optional cron automation can keep token refresh behavior running after setup.

Mitigation: Enable cron only when it is needed, review the exact crontab entry before keeping it, and document how to remove it.

Risk: OAuth access tokens may appear in mcporter Authorization headers and related operational files.

Mitigation: Treat mcporter configuration and token-refresh logs as sensitive and keep their file permissions restricted.

## Reference(s):

- [Pipedream Connect on ClawHub](https://clawhub.ai/maverick-software/skills/pipedream-connect)
- [Installation Guide](INSTALL.md)
- [Reference Implementation](reference/README.md)
- [Pipedream Connect Apps API](https://api.pipedream.com/v1/connect/{projectId}/apps)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline code blocks and file path references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include operational checklists, RPC names, configuration paths, and references to bundled implementation snapshots.]

## Skill Version(s):

1.6.0 (source: server release metadata and changelog, released 2026-03-21)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
