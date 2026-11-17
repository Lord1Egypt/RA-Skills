## Description:

Generate or edit AI images with the NanoPhoto.AI Nano Banana Pro API, including text-to-image generation, image-to-image editing from public image URLs, generation status checks, and polling until completion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nanophotohq](https://clawhub.ai/user/nanophotohq)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agents use this skill to generate new images from prompts or edit images from public URLs through NanoPhoto.AI's Nano Banana Pro API. It is useful when an agent needs to submit a request, poll for completion, and return the resulting image URL and status details.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Image prompts and public edit-image URLs are sent to NanoPhoto.AI.

Mitigation: Use the skill only for content you are comfortable sharing with NanoPhoto.AI, and avoid confidential images or sensitive prompt content unless NanoPhoto's data handling is acceptable.

Risk: API keys can be exposed if passed on shared command lines or logged systems.

Mitigation: Configure NANOPHOTO_API_KEY through the skill environment or another secure environment-variable mechanism instead of passing it with --api-key.

Risk: Edit mode requires public image URLs and does not support local files or base64 uploads.

Mitigation: Provide only authorized, publicly reachable image URLs and limit edit requests to at most eight input images.

## Reference(s):

- [NanoPhoto.AI](https://nanophoto.ai)
- [NanoPhoto API Key Settings](https://nanophoto.ai/settings/apikeys)
- [Nano Banana Pro API Reference](references/api.md)
- [ClawHub Skill Page](https://clawhub.ai/nanophotohq/skills/nanophoto-nano-banana-pro)
- [ClawHub Publisher Profile](https://clawhub.ai/user/nanophotohq)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API examples, and final image result details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return NanoPhoto generation IDs, status responses, progress values, and final image URLs from the third-party service.]

## Skill Version(s):

1.0.1 (source: server evidence release version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
