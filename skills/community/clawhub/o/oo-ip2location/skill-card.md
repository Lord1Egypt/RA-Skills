## Description:

Looks up domain WHOIS details, IP geolocation and network metadata, and hosted domains through IP2Location.io.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to retrieve domain registration details and IP geolocation, network, or hosted-domain information from IP2Location.io.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can execute downloaded software without a clear approval step or defined limits.

Mitigation: Install a reviewed CLI version yourself or require explicit approval before installation; review which additional agent skills it installs or synchronizes.

Risk: Lookup targets pass through OOMOL to IP2Location.io.

Mitigation: Submit sensitive targets only when that disclosure is intended.

## Reference(s):

- [IP2Location.io](https://www.ip2location.io)
- [IP2Location.io API documentation](https://www.ip2location.io/ip2location-documentation)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [JSON lookup results, presented as concise text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Lookup results depend on IP2Location.io data and account access.]

## Skill Version(s):

1.0.5 (source: skill metadata and server release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
