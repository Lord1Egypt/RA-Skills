## Description:

Provides agent guidance for compressing, resizing, converting, uploading, and pipeline-processing JPEG, PNG, WebP, and AVIF images with rv-image-optimize.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ziji1224054593](https://clawhub.ai/user/ziji1224054593)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to generate safe image-compression, format-conversion, resize, upload, and compress-then-upload CLI workflows. It is suited for batch image folders, WebP or AVIF conversion, FormData upload configuration, chunked resumable upload guidance, and JSON result summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can run an unpinned npm CLI.

Mitigation: Review before installing and prefer a pinned, vetted rv-image-optimize version or a lockfile-managed local binary.

Risk: Upload and pipeline workflows can send local files with supplied authorization data.

Mitigation: Use only trusted endpoints and credentials, avoid putting live cookies or bearer tokens into prompts, and use preview mode before real uploads when possible.

Risk: Destructive image flags can delete or replace source files.

Mitigation: Use output directories by default and require explicit user approval before delete-original or replace-original workflows.

## Reference(s):

- [Image Compressor Reference](reference.md)
- [Rv-image-optimize project homepage](https://github.com/ziji1224054593/Rv-image-optimize)
- [ClawHub skill page](https://clawhub.ai/ziji1224054593/skills/image-compressor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Recommends structured JSON CLI output for agent summaries.]

## Skill Version(s):

3.0.30 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
