## Description:

Browse and search music from monochrome.tf (Tidal-based Hi-Fi streaming), including artists, albums, tracks, lyrics, recommendations, and streaming URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ricanwarfare](https://clawhub.ai/user/ricanwarfare)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to discover music metadata and request streaming-related URLs through Monochrome/Tidal-proxy endpoints. It is suited for music search, album and artist lookup, lyrics retrieval, and recommendation workflows where the user is authorized to access the requested music.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can direct users to third-party Tidal-proxy endpoints and generated streaming URLs.

Mitigation: Use it only for music the user is legally authorized to access, and avoid unauthorized downloading or redistribution.

Risk: Community API instances may receive queries, track identifiers, or other request metadata.

Mitigation: Prefer the documented primary instance, avoid account-related or sensitive identifiers, and do not send private data through community endpoints.

Risk: Streaming quality and URL behavior may depend on external service compatibility and rate limits.

Mitigation: Validate endpoint responses before use and apply delays for bulk requests.

## Reference(s):

- [Monochrome Web](https://monochrome.tf)
- [Primary Monochrome API Instance](https://eu-central.monochrome.tf)
- [API Status](https://tidal-uptime.jiffy-puffs-1j.workers.dev)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API calls, Guidance]

**Output Format:** [Markdown guidance with endpoint examples and JSON API response expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Tidal-proxy endpoint paths, curl examples, streaming URL guidance, metadata fields, and quality options.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
