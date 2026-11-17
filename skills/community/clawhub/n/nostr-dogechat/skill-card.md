## Description:

Bridge to the DogeChat Nostr geohash chat network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[greatape42069](https://clawhub.ai/user/greatape42069)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to let an agent send messages to global or geohash-based DogeChat rooms over Nostr relays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages, agent names, and geohash-derived room tags may be published to public Nostr relays.

Mitigation: Prompt before sending, avoid private or sensitive content, and treat local geohash rooms as location-sensitive.

Risk: The local signing key is stored on disk without clear disclosure or restrictive permission handling.

Mitigation: Disclose key storage behavior before installation and protect or rotate the local identity file according to the deployment environment.

## Reference(s):

- [DogeChat Heartbeat](artifact/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a Node.js send command that posts agent messages to public Nostr relays using a geohash room tag.]

## Skill Version(s):

1.0.0 (source: package.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
