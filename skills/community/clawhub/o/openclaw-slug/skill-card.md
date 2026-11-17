## Description:

Connects agents to the WHOOP Developer Platform with official OAuth to fetch, normalize, and render recovery, sleep, strain, workout, profile, and body measurement data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gavinchengcool](https://clawhub.ai/user/gavinchengcool)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to authorize WHOOP access, fetch daily or weekly WHOOP metrics, normalize them into a stable schema, and prepare concise text or Markdown health reports for a selected chat channel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill stores WHOOP OAuth tokens locally.

Mitigation: Use a private token directory with restrictive permissions and avoid sharing token files or paths.

Risk: The skill can fetch and persist sensitive health, profile, and body measurement data.

Mitigation: Write outputs to private locations, avoid shared /tmp paths for retained data, and delete raw exports when no longer needed.

Risk: WHOOP summaries can be sent to chat channels or scheduled for repeated delivery.

Mitigation: Confirm the destination before sending, keep scheduled pushes channel-specific in their payload, and use duplicate-send state for recurring jobs.

Risk: The artifact includes a partner API surface with privileged write operations.

Mitigation: Do not use or expose partner operations unless the operator explicitly needs them and controls the required credentials.

Risk: Broad WHOOP OAuth scopes may expose more data than a task requires.

Mitigation: Request the minimum WHOOP scopes needed for the intended report before starting OAuth authorization.

## Reference(s):

- [WHOOP Skill Instructions](artifact/SKILL.md)
- [WHOOP API Quick Reference](artifact/references/whoop_api.md)
- [Normalized Output Schema](artifact/references/output_schemas.md)
- [Troubleshooting](artifact/references/troubleshooting.md)
- [WHOOP OpenAPI Specification](artifact/references/openapi.json)
- [WHOOP API Server](https://api.prod.whoop.com/developer)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration guidance]

**Output Format:** [Markdown or plain text reports, JSON data files, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Channel-aware report formatting for generic, Discord, Slack, WhatsApp, and Telegram outputs.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
