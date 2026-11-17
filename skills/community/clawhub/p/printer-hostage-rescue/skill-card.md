## Description:

Use when a printer refuses to print: 'ink low' / 'cartridge error' / 'non-genuine chip' / 'paper jam' with no paper / WiFi printing broken. Diagnoses by failure class, unlocks region/cartridge DRM tricks legally, configures driverless AirPrint/Mopria printing, and replaces subscription-ink trap behavior.

This skill is ready for commercial/non-commercial use.

## Publisher:

[voronindenis5](https://clawhub.ai/user/voronindenis5)

### License/Terms of Use:

MIT

## Use Case:

Home and SOHO printer users use this skill to diagnose common print failures, troubleshoot queues and connectivity, and configure driverless printing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clearing an entire print queue or restarting a printing service can lose pending jobs.

Mitigation: Inspect pending jobs first, get approval before clearing queues or restarting services, and prefer canceling only the affected job.

Risk: Firmware changes or settings resets can disrupt printer configuration.

Mitigation: Get approval, follow procedures for the exact printer model, and back up settings before making changes.

Risk: Network discovery may scan devices outside the intended scope.

Mitigation: Confirm the network or subnet to scan before starting discovery.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/voronindenis5/skills/printer-hostage-rescue)
- [Publisher profile](https://clawhub.ai/user/voronindenis5)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Plain-text diagnostic output and Markdown guidance with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include commands that change print queues, printer settings, or network diagnostics.]

## Skill Version(s):

1.0.0 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
