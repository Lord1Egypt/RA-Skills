## Description:

Manages a mihomo (Clash Meta) proxy service on Linux, including configuration, subscription updates, service restarts, node switching, and connection troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lflyice](https://clawhub.ai/user/lflyice)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and administrators use this skill to operate an existing mihomo proxy service on Linux, generate or validate proxy configuration, update subscriptions, switch nodes, and inspect service health.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can alter a persistent system proxy service and restart or enable mihomo through systemd.

Mitigation: Confirm service changes before execution, review and harden the systemd unit, and validate configuration before restarting the service.

Risk: Configuration generation can overwrite /opt/mihomo-config/config.yaml.

Mitigation: Back up the existing config.yaml, generate a staged candidate first, and run mihomo validation before replacing the active configuration.

Risk: Subscription download and shell-based curl invocation can expose users to unsafe argument handling and untrusted input.

Mitigation: Run generation as an unprivileged user, replace shell-based curl execution with safe argument handling, and review subscription input before use.

Risk: The helper script uses a fixed /tmp/sub_raw.txt path for subscription data.

Mitigation: Avoid fixed temporary files by using a private, permission-restricted temporary path for each run.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lflyice/skills/mihomo-proxy)
- [Publisher profile](https://clawhub.ai/user/lflyice)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate mihomo config.yaml content and commands that affect a local systemd-managed proxy service.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
