## Description:

Upscale, inspect, or compress JPG, PNG, or WebP images locally on macOS or Windows, including automatic or user-selected photo, portrait, digital-art, sharp-detail, balanced, and fast profiles; 1K/2K/4K/8K output; custom long edges; strict target file sizes; batch folders; aspect-ratio preservation; offline reuse; and verified download fallbacks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harven-droid](https://clawhub.ai/user/harven-droid)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect local images, select an enhancement profile, upscale images to resolution presets or custom long edges, batch process folders, and compress images to target file sizes while keeping processing local.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill downloads and runs a pinned native image-processing runtime and model files.

Mitigation: Use trusted cache and mirror locations only, keep SHA-256 verification enabled, and prefer offline mode after setup when downloads are no longer needed.

Risk: Batch image processing can affect many local files if pointed at the wrong folder.

Mitigation: Run it only on intended image folders, use dry-run for compression batches, and rely on the default non-overwrite behavior unless replacement is explicitly intended.

Risk: AI upscaling reconstructs texture and can create plausible-looking detail that was not present in the source image.

Mitigation: Describe enhanced results as reconstruction, not factual recovery, and use comparison crops when quality claims matter.

Risk: Large 8K jobs may fail or consume substantial GPU memory, system memory, and temporary disk space.

Mitigation: Check platform support and available storage before processing, then retry GPU-memory failures with smaller tile sizes such as 256 or 128.

## Reference(s):

- [Algorithm Profiles](references/algorithms.md)
- [Platform and Storage Reference](references/platforms.md)
- [Upstream Licenses and Attribution](references/licenses.md)
- [Upscayl NCNN command-line runtime](https://github.com/upscayl/upscayl-ncnn)
- [Upscayl model files](https://github.com/upscayl/upscayl/tree/main/resources/models)

## Skill Output:

**Output Type(s):** [guidance, shell commands, files, configuration]

**Output Format:** [Markdown guidance with bash commands; generated image files and optional JSON inspection reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Processes local JPG, PNG, and WebP inputs; writes PNG, JPG, or WebP upscales and JPEG compressed outputs without overwriting by default.]

## Skill Version(s):

1.2.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
