## Description:

OpenSETI helps users contribute compute power to analyze Breakthrough Listen radio telescope data, run distributed SETI scans, and participate in token-rewarded anomaly discovery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[synergysize](https://clawhub.ai/user/synergysize)

### License/Terms of Use:


## Use Case:

Developers and technically capable external users use OpenSETI to register a wallet, request work units, run FFT-based SETI signal analysis, and submit scan results to a coordinator.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts a coordinator that can direct downloads and receives wallet-linked scan activity.

Mitigation: Run it only if the coordinator operator is trusted, prefer a sandboxed environment, and avoid custom coordinator URLs unless you control and trust them.

Risk: The skill stores a wallet address locally and sends wallet and result data over the network.

Mitigation: Use a wallet appropriate for public or semi-public contribution tracking and review the local configuration before sharing the environment.

Risk: Continuous scanning can keep consuming compute and network resources.

Mitigation: Use one-shot scans for initial review, monitor resource usage, and run continuous mode only in an environment intended for ongoing compute contribution.

## Reference(s):

- [OpenSETI ClawHub listing](https://clawhub.ai/synergysize/skills/openseti-skill)
- [Breakthrough Listen Open Data Archive](https://breakthroughinitiatives.org/opendatasearch)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead users to run local CLI commands that contact a coordinator and persist wallet configuration.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
