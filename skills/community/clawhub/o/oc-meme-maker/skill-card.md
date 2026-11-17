## Description:

Search meme templates, suggest formats, and generate local or hosted image memes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hillstreet-ph](https://clawhub.ai/user/hillstreet-ph)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and community managers can search a curated set of meme templates, choose a format for a topic, and generate a local or hosted meme.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local rendering downloads template images from their listed source URLs, while hosted rendering sends captions to Imgflip.

Mitigation: Review template sources and avoid sending sensitive caption text to the hosted service; use local rendering for private captions.

Risk: Hosted rendering uses Imgflip account credentials.

Mitigation: Use your own credentials and keep them private.

## Reference(s):

- [ClawHub release](https://clawhub.ai/hillstreet-ph/skills/oc-meme-maker)
- [Curated meme template registry](artifact/references/templates.json)

## Skill Output:

**Output Type(s):** [Image files, URLs, Text]

**Output Format:** [SVG or PNG meme images, hosted image URLs, and text or JSON template listings]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Local rendering writes an image file; hosted rendering returns a URL. PNG output requires a supported browser, and Imgflip rendering requires user credentials.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
