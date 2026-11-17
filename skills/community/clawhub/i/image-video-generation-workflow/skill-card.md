## Description:

Guides agents through a local image and video generation workflow that combines ComfyUI or MCP image tooling, browser review, source-pack research, and reusable prompt/workflow capture.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codeman840425-del](https://clawhub.ai/user/codeman840425-del)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative workflow builders use this skill to structure local image or video generation loops, compare outputs in a browser, gather supporting references, and preserve stable prompts, parameters, workflow JSON, and review decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs users toward third-party repositories, videos, and image references that may change or include unsafe, incompatible, or low-quality workflows.

Mitigation: Review each external source, repository, model, and local command before using it, and keep only validated prompts, parameters, workflow files, and source links.

Risk: Using a single inspiration source or tutorial as authoritative guidance can lead to unstable or misleading image and video generation workflows.

Mitigation: Compare GitHub, video, and visual-reference sources by role, run a minimal local loop first, and change only one prompt or parameter group at a time.

## Reference(s):

- [MeiGen-AI-Design-MCP](https://github.com/jau123/MeiGen-AI-Design-MCP)
- [mcp-image](https://github.com/shinpr/mcp-image)
- [z-image-studio](https://github.com/iconben/z-image-studio)
- [YouTube workflow reference](https://www.youtube.com/watch?v=7aEQnTsI6zs)
- [Bilibili workflow reference](https://www.bilibili.com/video/BV14mrfBSEdq/)
- [Flickr visual reference](https://www.flickr.com/photos/dianeworland/55055024432/)
- [ClawHub skill page](https://clawhub.ai/codeman840425-del/skills/image-video-generation-workflow)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration, shell commands]

**Output Format:** [Markdown workflow guidance with inline tool, repository, and review steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Chinese-language workflow guidance; produces recommendations and reusable generation assets rather than executing code itself.]

## Skill Version(s):

2.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
