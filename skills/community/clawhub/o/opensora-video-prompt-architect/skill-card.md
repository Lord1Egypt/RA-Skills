## Description:

Turn rough video ideas into structured OpenSora prompt packs, reference-aware motion instructions, shot plans, and focused debugging loops.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gpt-img-2](https://clawhub.ai/user/gpt-img-2)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, marketers, and developers use this skill to turn rough text-to-video, image-to-video, or video-to-video ideas into compact prompts, shot plans, continuity constraints, and debugging guidance for OpenSora-related workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The optional MCP setup runs unpinned third-party code from GitHub.

Mitigation: Use the text-only workflow when possible; before installing the MCP, review the repository, prefer a pinned commit or signed release, avoid automatic acceptance flags where possible, and run it with minimal filesystem and environment access.

Risk: The skill references an independent OpenSora 2 resource and generation workspace, not the official Open-Sora project.

Mitigation: Present outputs as prompt-writing assistance for the referenced workspace and avoid claiming official Open-Sora behavior or authoritative model support.

## Reference(s):

- [OpenSora 2 Prompt Guide](https://opensora2.com/blog/opensora-2-prompt-guide)
- [OpenSora 2 Free AI Video Prompts](https://opensora2.com/free-ai-video-prompts)
- [OpenSora 2 Generator Workspace](https://opensora2.com/generator)
- [OpenSora 2 Text-to-Video](https://opensora2.com/text-to-video)
- [OpenSora 2 Image-to-Video](https://opensora2.com/image-to-video)
- [OpenSora 2 Video-to-Video](https://opensora2.com/video-to-video)
- [Raw Skill](https://opensora2.com/skills/opensora-video-prompt-architect/SKILL.md)
- [MCP Source](https://github.com/gpt-img-2/opensora2-prompt-mcp)
- [ClawHub Listing](https://clawhub.ai/gpt-img-2/skills/opensora-video-prompt-architect)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with prompt sections, shot plans, optional shell commands, and concise debugging guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Text-only by default; optional MCP setup may provide read-only helper tools when installed.]

## Skill Version(s):

1.0.0 (source: release evidence and OpenClaw metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
