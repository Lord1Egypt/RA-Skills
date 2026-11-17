## Description:

Search YouTube videos, channels, and trends through the AISA YouTube SERP client.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bibaofeng](https://clawhub.ai/user/bibaofeng)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and content researchers use this skill to run YouTube search, trend discovery, channel research, and competitor research through the bundled AISA SERP client.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: YouTube search queries, country and language parameters, and the AISA API key are sent to the AISA relay.

Mitigation: Use only a dedicated AISA_API_KEY and avoid searches or parameters that should not be shared with that service.

Risk: Results depend on the availability and behavior of the AISA relay and YouTube SERP responses.

Mitigation: Review returned results before relying on them for publishing, market analysis, or operational decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bibaofeng/skills/openclaw-aisa-youtube-aisa)
- [Publisher profile](https://clawhub.ai/user/bibaofeng)
- [AISA YouTube search endpoint](https://api.aisa.one/apis/v1/youtube/search?engine=youtube&q=AI+agents+tutorial)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and AISA_API_KEY; sends YouTube search parameters to the AISA relay.]

## Skill Version(s):

1.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
