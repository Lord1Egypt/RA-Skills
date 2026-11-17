## Description:

Photo Captions generates platform-tuned social media captions for user-provided photography and optional shooting context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, photographers, and agents use this skill to turn a photo and optional context such as location, subject, mood, camera, lens, or film stock into native captions for social and photography platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically calls for a separate photo-edit-analysis skill to run on user images.

Mitigation: Disclose the additional photo analysis step before use and make it opt-in when users do not want photos or context passed to another skill.

Risk: Captions can become misleading if the photo context or gear details are incomplete.

Mitigation: Use only user-provided or directly observable details, omit unknown gear, and review captions before publication.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown sections with platform-specific captions and optional edit analysis]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces distinct caption styles for Instagram, Flickr, X, Glass, Tumblr, Bluesky, Threads, 500px, Reddit, Facebook, VSCO, Substack, and Pinterest; gear details are included only when provided.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
