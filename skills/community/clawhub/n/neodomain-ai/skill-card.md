## Description:

Generate images and videos via Neodomain AI API, including text-to-image, image-to-video, text-to-video, and motion control video generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bandwhite](https://clawhub.ai/user/bandwhite)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content creators use this skill to call Neodomain AI from an agent workflow for text-to-image, reference-image generation, text-to-video, image-to-video, and motion-control video generation. The skill supports model discovery, authentication, generation polling, media download, and generation metadata capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Account tokens are required for API calls and the login helper prints the access token after authentication.

Mitigation: Use environment variables or a secret manager, avoid passing tokens directly in shared shell history, and treat printed tokens as sensitive.

Risk: Prompts, reference URLs, local media selected for upload, and generated outputs may be sent through the Neodomain API and OSS workflow.

Mitigation: Run the skill only with media you are comfortable uploading to the service, and avoid private or regulated content unless retention and deletion behavior is understood.

Risk: Generated media and metadata are written to local output directories.

Mitigation: Review output folders and metadata before sharing them, especially when prompts or returned media URLs may reveal sensitive project context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bandwhite/skills/neodomain-ai)
- [Publisher profile](https://clawhub.ai/user/bandwhite)
- [Neodomain AI API base URL](https://story.neodomain.cn)
- [SKILL.md](artifact/SKILL.md)
- [INSTALL.md](artifact/INSTALL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Files, JSON metadata, Guidance]

**Output Format:** [Markdown instructions with Python CLI commands; generated JPEG, PNG, WebP, and MP4 files with metadata.json]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and NEODOMAIN_ACCESS_TOKEN; generation scripts send prompts and media URLs to the Neodomain API, poll for completion, and download outputs locally.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
