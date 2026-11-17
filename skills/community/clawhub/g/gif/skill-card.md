## Description:

Find, search, and create GIFs with proper optimization and accessibility.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and content teams use this skill to find GIF sources, generate optimized GIFs from video, choose video alternatives when appropriate, and apply accessibility practices for animated media.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using the Giphy or Tenor API examples sends search terms and API keys to those providers.

Mitigation: Avoid sensitive GIF queries and use API keys that are appropriate for third-party GIF search.

Risk: Animated GIFs can create accessibility issues when loops are long or flashes are too frequent.

Mitigation: Provide pause controls for loops longer than five seconds, respect prefers-reduced-motion, include descriptive alt text, and keep flashing content under three flashes per second.

## Reference(s):

- [ClawHub GIF Skill](https://clawhub.ai/ivangdavila/skills/gif)
- [Giphy Search API example](https://api.giphy.com/v1/gifs/search?api_key=$GIPHY_API_KEY&q=thumbs+up&limit=10)
- [Tenor Search API example](https://tenor.googleapis.com/v2/search?key=$TENOR_API_KEY&q=thumbs+up&limit=10)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, HTML, and API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires ffmpeg for GIF creation; optionally uses gifsicle, GIPHY_API_KEY, and TENOR_API_KEY.]

## Skill Version(s):

1.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
