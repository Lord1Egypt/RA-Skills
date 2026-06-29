## Description: <br>
Batch image processing - compress, resize, format convert, watermark, EXIF clean, and crop. All local, no upload needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harrylabsj](https://clawhub.ai/user/harrylabsj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, creators, and content operators use this skill to batch-process local images for compression, resizing, conversion, watermarking, EXIF cleanup, cropping, and platform-specific publishing presets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can scan many local image files and write processed outputs. <br>
Mitigation: Review input globs, directory choices, and maximum file settings before running batch jobs. <br>
Risk: Existing output files could be replaced if overwrite is enabled. <br>
Mitigation: Keep overwrite disabled unless replacing prior outputs is intentional. <br>


## Reference(s): <br>
- [Image Works ClawHub listing](https://clawhub.ai/harrylabsj/image-works) <br>
- [Reference README](references/README.md) <br>
- [Platform presets](references/presets.json) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration, Guidance, Text] <br>
**Output Format:** [Processed image files with a structured processing report and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes local input paths, directories, or glob patterns and writes outputs to the configured output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
