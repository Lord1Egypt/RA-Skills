## Description:

MusicRouter converts music sharing links across Chinese and major international platforms, extracting song details, album artwork, and platform-specific links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leo7723](https://clawhub.ai/user/leo7723)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and end users use MusicRouter to turn a music sharing URL into structured song metadata and links for preferred platforms, then present the result as a readable Markdown response.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Music links may trigger requests to unintended internal or arbitrary hosts.

Mitigation: Validate URL scheme and hostname, block private, link-local, and loopback destinations, and revalidate redirects before running this skill in agents, servers, or shared environments.

Risk: Submitted links and derived metadata are sent to song.link and music platform APIs.

Mitigation: Use only music links appropriate for third-party processing, and avoid submitting private or sensitive URLs.

Risk: Optional logging can retain conversion records locally.

Mitigation: Keep logging disabled on shared systems unless retention is acceptable, restrict log file access, and clear logs according to local policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/leo7723/skills/music-router)
- [Odesli song.link API](https://api.song.link/v1-alpha.1/links)

## Skill Output:

**Output Type(s):** [JSON, Markdown, Shell commands, Guidance]

**Output Format:** [JSON from the converter script and Markdown-formatted music platform links for user-facing responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include detected song metadata, album artwork URL, converted platform links, aggregation link, and an optional local log path when logging is enabled.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
