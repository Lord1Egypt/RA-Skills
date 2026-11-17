## Description:

Turns pet photos into cinematic character posters through a two-stage Mew API workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[shuminliu026](https://clawhub.ai/user/shuminliu026)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to transform pet photos into themed character hero images and finished cinematic movie posters while preserving pet identity and readable poster text.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires a mew.design API key and sends pet images, poster text, and generated assets to Mew APIs.

Mitigation: Confirm the user is comfortable sharing those inputs with Mew before generation, and ask for or validate the API key only when needed.

Risk: Local-only pet images may need to be uploaded to a third-party file host before the downstream APIs can use them.

Mitigation: Prefer user-controlled public image URLs, explain the privacy tradeoff for temporary uploads, and obtain explicit consent before uploading.

Risk: Generated posters can fail if the transformed pet no longer resembles the source pet or if poster text overlaps the pet silhouette.

Mitigation: Inspect each stage, retry once with stronger identity-preservation cues when needed, and retry poster composition with stricter text-safe layout instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shuminliu026/skills/pet-movie-poster)
- [Mew image-process API endpoint](https://api.mew.design/open/api/image/process)
- [Mew design-generate API endpoint](https://api.mew.design/open/api/design/generate)

## Skill Output:

**Output Type(s):** [Markdown, API Calls, Shell commands, Guidance]

**Output Format:** [Markdown with image links and optional inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a final poster image URL and original image link after Mew API generation.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
