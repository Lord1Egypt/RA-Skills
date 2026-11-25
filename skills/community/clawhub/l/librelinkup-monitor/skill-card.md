## Description:

Monitor FreeStyle Libre CGM glucose telemetry via LibreLinkUp cloud API with zero-cost monitor-gated alerts for lows and rapid drops.

This skill is for research and development only.

## Publisher:

[jstrowd-bit](https://clawhub.ai/user/jstrowd-bit)

### License/Terms of Use:

MIT

## Use Case:

Caregivers use this skill to configure scheduled monitoring of glucose readings shared through a secondary LibreLinkUp account and surface low or rapidly falling readings for notification. It is intended for informational and personal research use, not as a replacement for medical monitoring or clinical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Glucose readings or alerts may be stale, delayed, or unavailable.

Mitigation: Treat the monitor as supplemental; check the primary sensor/app and verify unexpected readings with an independent fingerstick meter.

Risk: Caregiver credentials and glucose data need careful handling.

Mitigation: Use a secondary caregiver account, store credentials in a restricted local configuration file, and do not expose secrets in chat.

Risk: Scanner coverage is incomplete because one referenced image was not fully inspected.

Mitigation: Review the image and the complete skill package before installation.

## Reference(s):

- [GitHub source repository](https://github.com/jstrowd-bit/LibreLinkUp-monitor)
- [ClawHub skill page](https://clawhub.ai/jstrowd-bit/skills/librelinkup-monitor)
- [LibreLinkUp Cloud API Reference](references/api_reference.md)
- [Gotchas and Failure Modes](references/gotchas_and_failure_modes.md)
- [Hermes Agent documentation](https://hermes-agent.nousresearch.com)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Code, Text]

**Output Format:** [Markdown with shell commands, Python code, JSON configuration, and monitor status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The poller emits a status line; alert behavior depends on configured thresholds and scheduled polling.]

## Skill Version(s):

0.1.0 (ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
