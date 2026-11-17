## Description:

Batch image processing - compress, resize, format convert, watermark, EXIF clean, and crop. All local, no upload needed.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and operations teams use this skill to batch-process local image files for compression, resizing, format conversion, watermarking, EXIF cleanup, cropping, and platform-specific publishing presets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local image paths and writes processed files, which can expose private images or create files in unintended locations.

Mitigation: Use explicit input paths, write to a private output directory, keep overwrite disabled unless replacement is intended, and avoid shared or world-writable output folders.

Risk: Large or untrusted image batches and extreme resize settings can consume excessive local resources.

Mitigation: Run a small sample first, keep practical file and dimension limits, and use max_files or similar limits for large folders.

Risk: The manifest declares a DeepSeek model even though the skill is described as local-first image processing.

Mitigation: Review runtime data handling expectations before use and avoid providing sensitive images unless the execution environment matches the local-processing claim.

## Reference(s):

- [Image Works ClawHub Page](https://clawhub.ai/harrylabsj/skills/image-works)
- [Reference README](references/README.md)
- [Preset Definitions](references/presets.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Files, JSON]

**Output Format:** [Markdown guidance with CLI examples, processed image files, and text or JSON processing reports.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads user-provided local image paths and writes processed files to the configured output directory; default max_files is 1000.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
