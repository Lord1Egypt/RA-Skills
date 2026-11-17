## Description:

Search configured torrent indexers through Jackett's Torznab API for releases, indexers, and capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imyukehan](https://clawhub.ai/user/imyukehan)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and power users with a trusted Jackett instance use this skill to search configured torrent indexers, inspect indexer capabilities, and receive release results as JSON or XML.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses a Jackett API key to query configured torrent indexers.

Mitigation: Store the credential file with owner-only permissions and rotate the API key if it may have been exposed.

Risk: Search output can include download, magnet, details, or private tracker URLs that may contain sensitive tokens.

Mitigation: Avoid sharing raw output and redact tracker URLs or tokens before logging or posting results.

Risk: The skill depends on the configured Jackett service and the trustworthiness of its indexers and results.

Mitigation: Use a trusted local HTTPS or loopback Jackett endpoint and review returned results before acting on them.

## Reference(s):

- [Torznab feed schema](http://torznab.com/schemas/2015/feed)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON, XML]

**Output Format:** [Markdown guidance with shell commands; parsed search results are JSON by default and raw XML when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Parsed results default to a limit of 20 and include a meta object plus a results array; raw XML can be larger.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
