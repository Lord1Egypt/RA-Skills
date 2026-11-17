## Description:

Mode Switch Kit helps an agent guide users through switching a local machine stack between YAML-defined modes covering VPN state, background agents, local services, and model tier, with watchdog repair for the current mode.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ccy123abcd](https://clawhub.ai/user/ccy123abcd)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users use this skill to configure and operate local mode switching for work, gaming, rendering, or similar setups where VPN, background agents, local services, and model tiers need to change together.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mode switches can change VPN state and may disrupt connectivity or terminate local processes.

Mitigation: Review the YAML configuration carefully, run selftests and dry runs first, and avoid scheduling the watchdog or using real VPN and service commands until process ownership checks and VPN unknown-state handling are tightened.

Risk: Running the switcher with elevated privileges can increase the impact of incorrect process stops or service commands.

Mitigation: Run with the least privileges needed for the configured services and prefer monitor-only service entries until the machine-specific commands have been verified.

## Reference(s):

- [Mode Switch Kit design patterns](references/patterns.md)
- [Mode Switch Kit ClawHub page](https://clawhub.ai/ccy123abcd/skills/mode-switch-machine-stack)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with inline shell commands, Python script paths, and YAML configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local Python standard-library workflow; includes dry-run and selftest guidance before real mode switching.]

## Skill Version(s):

0.1.1 (source: frontmatter, CHANGELOG, version file, release evidence; released 2026-09-12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
