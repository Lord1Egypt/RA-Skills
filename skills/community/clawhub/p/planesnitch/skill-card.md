## Description:

Monitors aircraft near configured locations using public ADS-B feeds or a self-hosted ultrafeeder, then sends configurable alerts to Telegram or webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyb0t](https://clawhub.ai/user/psyb0t)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use planesnitch to monitor aircraft around configured locations and receive alerts for selected aircraft, emergency squawks, or altitude and proximity conditions. They configure ADS-B sources, watchlists, and Telegram or webhook targets in a local YAML file.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence flags repeated Docker examples using a mutable image reference, which can change without a versioned digest.

Mitigation: Wait to install until the image is pinned to a verified digest, and review image updates before adopting them.

Risk: Configured ADS-B sources receive location coordinates, and alert targets receive aircraft position and identification data.

Mitigation: Use a self-hosted ADS-B source when desired, and configure only Telegram or webhook targets that you control or trust.

Risk: The local configuration can contain Telegram bot tokens and webhook credentials in plaintext.

Mitigation: Keep config.yaml out of source control and chat, and mount it read-only in the container.

## Reference(s):

- [Setup and configuration guide](references/setup.md)
- [Project homepage](https://github.com/psyb0t/docker-planesnitch)
- [Plane Alert Database](https://github.com/sdr-enthusiasts/plane-alert-db)
- [ICAO Doc 8643 aircraft type designators](https://www.icao.int/publications/DOC8643/Pages/Search.aspx)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON alerts]

**Output Format:** [Markdown guidance with YAML configuration and shell command examples; JSON webhook alert payloads.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Alerts can include aircraft tracking fields and an optional base64-encoded aircraft type image.]

## Skill Version(s):

1.9.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
