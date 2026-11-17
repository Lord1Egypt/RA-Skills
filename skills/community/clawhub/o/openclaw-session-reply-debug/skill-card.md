## Description:

Diagnose OpenClaw "message sent but no assistant reply" issues, then safely switch active model references with primary + multi-fallback support, including heartbeat-triggered recovery to the highest available model.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zxs1633079383](https://clawhub.ai/user/zxs1633079383)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to diagnose OpenClaw sessions where messages are sent but no assistant reply appears, then validate model availability and switch active model references to a working primary or fallback model.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persistently modify OpenClaw model configuration and session cache files.

Mitigation: Run the model-switching scripts in dry-run mode first, review the planned file changes, and apply only after the selected target model has passed the documented probes.

Risk: Provider probes send configured API credentials to the provider endpoint in OpenClaw configuration.

Mitigation: Use trusted HTTPS provider base URLs and verify OpenClaw provider settings before running probes or enabling automated fallback.

Risk: Diagnostic output may expose provider settings or operational details if copied into support channels.

Mitigation: Review and redact session, config, log, and probe output before sharing it outside the trusted operator context.

Risk: Heartbeat or cron integration with --apply can repeatedly change persistent model settings.

Mitigation: Manually test the exact command, confirm backup behavior and post-switch replies, then enable automation only with the intended primary and fallback order.

## Reference(s):

- [OpenClaw Model Connectivity Test Runbook](openclaw-model-connectivity-test.md)
- [OpenClaw Session Troubleshooting README](README.md)
- [ClawHub Skill Page](https://clawhub.ai/zxs1633079383/skills/openclaw-session-reply-debug)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON examples, and optional JavaScript script execution.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include dry-run plans, provider probe results, selected model details, changed file counts, backup paths, and post-switch verification steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
