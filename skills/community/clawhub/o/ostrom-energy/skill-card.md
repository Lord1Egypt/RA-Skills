## Description:

Fetch Ostrom hourly electricity spot prices, find cheapest appliance/EV charging windows, and trigger smart-home actions from price thresholds.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pmagnomuller](https://clawhub.ai/user/pmagnomuller)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect current or upcoming Ostrom electricity spot prices, identify low-cost run windows for appliances or EV charging, and optionally control smart-home devices from verified price thresholds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Control mode can run local shell commands when --execute is enabled.

Mitigation: Use dry-run first and enable --execute only with command strings the user wrote and verified.

Risk: Local .env and home configuration files can provide credentials and other runtime settings.

Mitigation: Use only trusted local configuration files and store Ostrom credentials with the same care as other API secrets.

Risk: The optional installer creates a persistent wrapper in ~/.local/bin.

Mitigation: Skip the installer when a persistent local command is not desired and run the skill from its directory with bash run.sh.

## Reference(s):

- [Ostrom Energy ClawHub Page](https://clawhub.ai/pmagnomuller/skills/ostrom-energy)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output and Markdown usage guidance with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Ostrom API credentials; control mode is dry-run unless --execute is passed.]

## Skill Version(s):

1.0.1 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
