## Description:

Media Processor automates image and video processing for local files and remote URLs, including download, compression, watermarking, and format conversion.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mobai-6543](https://clawhub.ai/user/mobai-6543)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to process media assets before publishing or storage, such as compressing videos, transcoding video to H.264, converting images to JPEG, or adding text watermarks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unrestricted remote URLs can allow requests to internal networks or unexpectedly large downloads.

Mitigation: Run with restricted network egress and prefer URL allowlisting, private-network blocking, and download size and time limits before accepting untrusted URLs.

Risk: Caller-provided output paths can overwrite writable files.

Mitigation: Use a dedicated output directory and validate output paths before execution.

Risk: Media processing through FFmpeg and unpinned dependencies increases execution and supply-chain exposure.

Mitigation: Use an isolated environment, keep FFmpeg handling constrained, and pin dependencies for deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mobai-6543/skills/media-processor-agent)

## Skill Output:

**Output Type(s):** [Files, Text]

**Output Format:** [Processed media files plus plain-text status messages and output paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processed images or videos are written to a requested or derived output path.]

## Skill Version(s):

1.1.0 (source: server release metadata; artifact frontmatter says 1.2.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
