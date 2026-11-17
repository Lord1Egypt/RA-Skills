## Description:

Find high-quality Instagram photos for any destination or place by searching Instagram posts, downloading candidate images, scoring them for quality and place fit, and returning the best matches with source URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[psyduckler](https://clawhub.ai/user/psyduckler)

### License/Terms of Use:


## Use Case:

External users and content teams use this skill to find ranked Instagram photo candidates for destinations, attractions, restaurants, or other places. It is useful when an agent needs scenic or representative image options with source URLs and local file paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads public image candidates to /tmp during execution.

Mitigation: Delete temporary image files after use if local retention is not desired.

Risk: Returned Instagram images may be subject to platform terms, copyright, publicity rights, or other reuse limits.

Mitigation: Review image rights and Instagram platform terms before public or commercial reuse.

Risk: Vision scoring is subjective and may rank images that are visually strong but not appropriate for the intended destination or use.

Mitigation: Review ranked candidates manually before publishing or using them in customer-facing materials.

## Reference(s):

- [Instagram media endpoint pattern](https://www.instagram.com/p/{shortcode}/media/?size=l)
- [ClawHub skill page](https://clawhub.ai/psyduckler/skills/instagram-photo-find)
- [Publisher profile](https://clawhub.ai/user/psyduckler)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown with ranked results, brief descriptions, source URLs, and local file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns a ranked list of image candidates scored by a vision model; downloaded images are stored temporarily under /tmp.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
