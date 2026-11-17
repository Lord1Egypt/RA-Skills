## Description:

Monitor DigitalOcean VPS droplets by listing instances and fetching CPU, memory, disk, and bandwidth metrics with summaries using the DigitalOcean API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[elandivar](https://clawhub.ai/user/elandivar)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect DigitalOcean droplet inventory, utilization, bandwidth, and health signals from an agent session.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The required DigitalOcean API token can expose account access if copied into shared prompts, logs, or transcripts.

Mitigation: Use a scoped or read-only token when available, store it outside shared logs, and avoid pasting token values into agent-visible text.

Risk: Droplet inventory and monitoring output can reveal server names, IDs, regions, statuses, and raw metric time series.

Mitigation: Review output before sharing it and redact infrastructure identifiers or metric details that should remain private.

Risk: Metric collection may be incomplete or fail when DigitalOcean Monitoring is not enabled for a droplet.

Mitigation: Confirm Monitoring is enabled before relying on CPU, memory, disk, or bandwidth summaries.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/elandivar/skills/neomano-vps-monitoring)
- [DigitalOcean API endpoint](https://api.digitalocean.com)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Guidance]

**Output Format:** [JSON metrics output with concise text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3, DIGITALOCEAN_TOKEN, and DigitalOcean Monitoring enabled for metric collection.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
