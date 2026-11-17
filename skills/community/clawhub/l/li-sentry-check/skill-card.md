## Description:

Li Sentry Check inspects remote Linux servers over SSH with key-based authentication, runs configured read-only health checks for system resources, services, logs, and security signals, and generates Markdown or JSON reports with anomaly highlighting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[43622283](https://clawhub.ai/user/43622283)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations engineers use this skill to inspect Linux servers over SSH, collect resource, service, log, and security status, and generate health reports with highlighted anomalies.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invalid service names can reach a remote bash command path over SSH.

Mitigation: Reject invalid service names locally before any SSH execution and do not send validation failure messages through remote bash.

Risk: First-time SSH host trust can be accepted automatically.

Mitigation: Pre-populate known_hosts for production targets instead of relying on accept-new host key behavior.

Risk: Untrusted edits to targets.yaml or checks.yaml can change hosts, accounts, keys, services, or allowed commands.

Mitigation: Protect both YAML files from untrusted edits and review changes before running inspections.

Risk: Reports can include sensitive host, service, log, and security information.

Mitigation: Treat generated Markdown and JSON reports as sensitive system data and restrict sharing and storage accordingly.

Risk: SSH inspection privileges may expose more system data than needed.

Mitigation: Run with a dedicated least-privilege SSH inspection account.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/43622283/skills/li-sentry-check)
- [README.en.md](artifact/README.en.md)
- [Design documentation](artifact/design.md)
- [Inspection command allowlist](artifact/references/checks.yaml)
- [Target server configuration](artifact/references/targets.yaml)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown or JSON inspection reports with setup and run commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports can be written to stdout or a local file and may contain sensitive system data.]

## Skill Version(s):

0.4.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
