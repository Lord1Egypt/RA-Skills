## Description:

Researches public music, artist, playlist, and podcast information across Spotify, Spotify Podcasts, Apple Podcasts, Discogs, and SoundCloud through Crawlora, returning JSON.

This skill is ready for commercial/non-commercial use.

## Publisher:

[crawlora-org](https://clawhub.ai/user/crawlora-org)

### License/Terms of Use:

MIT-0

## Use Case:

Listeners, researchers, and developers use this skill to find public track, album, artist, playlist, podcast, and record-release details and compare available catalog information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Lookup terms, public profile or media URLs, and the API key are sent to Crawlora.

Mitigation: Avoid sensitive private searches and account identifiers; keep the key in the environment and use the provided helper rather than embedding it in commands or files.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/crawlora-org/skills/music-podcast-research)
- [Crawlora API and key setup](https://crawlora.net)
- [Endpoint reference](reference/endpoints.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands]

**Output Format:** [JSON lookup results and Markdown guidance with shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Public catalog data; searches can be paginated and require a Crawlora API key.]

## Skill Version(s):

1.0.19 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
