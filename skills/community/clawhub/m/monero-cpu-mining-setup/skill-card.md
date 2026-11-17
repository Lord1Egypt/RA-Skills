## Description:

Step-by-step guide to safely download, configure, and run XMRig for low-impact Monero CPU mining on Windows, Linux, and macOS systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liumaimiao](https://clawhub.ai/user/liumaimiao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to generate setup guidance for running XMRig-based Monero CPU mining on authorized Windows, Linux, or macOS hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mining on hardware without explicit authorization can violate policy or law.

Mitigation: Use the skill only for hardware you own or are explicitly allowed to operate for Monero mining.

Risk: Unverified miner downloads may expose users to malware.

Mitigation: Download XMRig from the official release source and verify checksums before running it.

Risk: The sample pool configuration uses an unencrypted connection.

Mitigation: Replace sample pool settings with a current TLS-enabled endpoint before mining.

Risk: CPU mining can increase temperature, power consumption, and hardware wear.

Mitigation: Use low-impact settings, monitor system temperature and electricity cost, and avoid unsuitable shared, workplace, cloud, or poorly cooled machines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liumaimiao/skills/monero-cpu-mining-setup)
- [XMRig Releases](https://github.com/xmrig/xmrig/releases)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON configuration and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes download verification, authorization, temperature monitoring, and pool configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
