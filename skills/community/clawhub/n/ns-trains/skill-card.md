## Description:

Check Dutch train schedules, departures, disruptions, and plan journeys using the NS API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eggressive](https://clawhub.ai/user/eggressive)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to look up Dutch rail journeys, station arrivals and departures, current disruptions, station matches, and commute options through the NS API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The NS subscription key could be exposed through the redirect-related risk identified by the security evidence.

Mitigation: Use a low-privilege or free-tier NS key, inject it through a runtime secret mechanism, monitor or rotate it if exposed, and tighten redirect handling before using a valuable subscription.

Risk: The skill requires outbound access to the NS API gateway and a valid NS subscription key.

Mitigation: Run it only in environments where HTTPS access to gateway.apiportal.ns.nl is expected, and keep NS_SUBSCRIPTION_KEY out of committed files and shared logs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/eggressive/skills/ns-trains)
- [NS API Portal](https://apiportal.ns.nl/)
- [NS API Starter Guide](https://apiportal.ns.nl/startersguide)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Plain text command output with train times, delays, platforms, transfers, disruptions, station matches, and commute options.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js and an NS subscription key supplied through NS_SUBSCRIPTION_KEY; legacy NS_API_KEY is supported.]

## Skill Version(s):

1.1.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
