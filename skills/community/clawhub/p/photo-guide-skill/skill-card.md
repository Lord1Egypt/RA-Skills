## Description:

Photo Guide helps an agent analyze uploaded photos, extract available EXIF data, infer shooting parameters from visual features, and provide practical shooting, editing, and learning guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dcison](https://clawhub.ai/user/dcison)

### License/Terms of Use:

MIT-0

## Use Case:

External users and photography learners use this skill to understand how a photo was likely shot, compare inferred settings with EXIF metadata when available, and receive beginner-friendly capture and post-processing advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Photo EXIF data can include precise GPS or location metadata that may be exposed to the agent context.

Mitigation: Strip GPS/location metadata from personal photos before using the skill unless the user intentionally wants that metadata analyzed.

Risk: The skill can automatically install an unpinned Python image dependency.

Mitigation: Use a virtual environment, require approval before dependency installation, and pin or lock Pillow before deployment.

Risk: When EXIF is missing or image quality is low, shooting parameters are visual estimates and may be imprecise.

Mitigation: Label non-EXIF values as inferred ranges and widen ranges when image quality or metadata is insufficient.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dcison/skills/photo-guide-skill)
- [Photography basics](references/photography-basics.md)
- [Photography style templates](references/style-templates.md)
- [Post-processing guide](references/post-processing-guide.md)
- [EXIF extraction script](scripts/extract_exif.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown report with tables, concise prose, and optional shell-command usage for local EXIF extraction]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Language follows the user's prompt; EXIF-backed values are distinguished from visual estimates.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
