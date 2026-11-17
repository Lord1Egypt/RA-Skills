## Description:

P图 is a creative image-processing skill that helps agents load, save, resize, crop, convert, enhance, filter, stitch, remove backgrounds from, and add text to local images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform common local image-editing tasks in Python, including image resizing, enhancement, filters, compositing, simple background removal, and text overlays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads input images and writes output images on the local filesystem.

Mitigation: Use caller-controlled input and output paths, avoid sensitive directories, and review output locations before saving images.

Risk: The package depends on Pillow for image parsing and processing.

Mitigation: Install in a virtual environment and pin Pillow to a reviewed version with a lockfile or hashes in stricter environments.

Risk: Installing or running image-processing code with elevated privileges can increase the impact of dependency or path mistakes.

Mitigation: Avoid administrator or root installs and run the skill with least-privilege filesystem access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hgta23/skills/p)
- [README](artifact/README.md)
- [Skill instructions](artifact/SKILL.md)
- [Usage example](artifact/example.py)

## Skill Output:

**Output Type(s):** [Code, Files, Guidance]

**Output Format:** [Python API calls, local image files, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses Pillow for local image processing and writes image outputs only to paths selected by the caller.]

## Skill Version(s):

1.0.0 (source: server release metadata, SKILL.md, README.md, and src/p_skill/__init__.py)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
