## Description:

Photo Toolkit helps agents convert RAW, JPG, and HEIC photos to JPG thumbnails, find files by EXIF shooting date, generate layout previews, deflicker timelapse frames, and assemble JPG frames into MP4 video.

This skill is ready for commercial/non-commercial use.

## Publisher:

[konanok](https://clawhub.ai/user/konanok)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, creators, and photo workflow agents use this skill to run local utilities for camera photo conversion, EXIF date filtering, preview generation, timelapse deflickering, and video assembly.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency setup may use package managers, pip, or sudo-level system changes.

Mitigation: Install in a virtual environment where possible, review the setup script before running it, and prefer pinned dependencies.

Risk: Generated thumbnails can preserve EXIF metadata, which may expose private camera, time, or location details.

Mitigation: Use --no-exif when outputs may be shared outside a private workflow.

Risk: Batch photo utilities can create or modify many local files during conversion, preview generation, deflickering, or video assembly.

Mitigation: Use dry-run modes where available, confirm input and output directories, and keep backups for destructive or in-place workflows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/konanok/skills/photo-toolkit)
- [Project homepage](https://github.com/konanok/photo-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with bash commands; generated artifacts may include JPG thumbnails, JSON reports or file lists, preview JPGs, and MP4 videos.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs local scripts against user-supplied photo directories; EXIF metadata may be preserved by default unless disabled.]

## Skill Version(s):

1.0.0 (source: frontmatter, VERSION, changelog released 2026-05-20, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
