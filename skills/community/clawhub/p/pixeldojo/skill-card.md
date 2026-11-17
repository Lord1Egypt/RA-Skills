## Description:

Access PixelDojo's API for AI image and video generation. Use when an agent needs to create images or videos, choose a model from the live PixelDojo catalog, check async job status, or download finished assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[blovett80](https://clawhub.ai/user/blovett80)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative agents use this skill to submit PixelDojo image or video generation jobs, inspect the live model catalog, poll job status, and return downloaded asset paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key can be sent to a non-default API endpoint if PIXELDOJO_API_BASE is overridden.

Mitigation: Use the default PixelDojo HTTPS API base unless a trusted PixelDojo-compatible endpoint has been reviewed.

Risk: Prompts and input image URLs are submitted to the PixelDojo service.

Mitigation: Avoid confidential prompts, private image URLs, and regulated data unless the service terms and data handling are acceptable.

Risk: Generated assets are downloaded from service-provided URLs and saved to local disk.

Mitigation: Choose output paths deliberately and review downloaded files before reuse or redistribution.

## Reference(s):

- [PixelDojo ClawHub Skill Page](https://clawhub.ai/blovett80/skills/pixeldojo)
- [Publisher Profile](https://clawhub.ai/user/blovett80)
- [PixelDojo Homepage](https://pixeldojo.ai)
- [PixelDojo API Base](https://pixeldojo.ai/api/v1)
- [PixelDojo Model Catalog](references/model-catalog.md)
- [PixelDojo Live Models Endpoint](https://pixeldojo.ai/api/v1/models)

## Skill Output:

**Output Type(s):** [Shell commands, API Calls, Files, Guidance]

**Output Format:** [Markdown with shell commands, JSON status output, local file paths, and generated image or video files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires PIXELDOJO_API_KEY, optional PIXELDOJO_API_BASE, and curl, jq, and python3. Generated assets are saved persistently to user-selected or default output paths.]

## Skill Version(s):

1.3.3 (source: server release evidence and artifact/api.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
