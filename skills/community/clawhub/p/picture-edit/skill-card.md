## Description:

Picture Edit provides local image loading, editing, enhancement, filters, compositing, background removal, and text overlay through a Python/Pillow API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hgta23](https://clawhub.ai/user/hgta23)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Picture Edit to script local image workflows such as resizing, cropping, format conversion, enhancement, filtering, stitching, simple background removal, and text overlays.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Opening untrusted image files can expose the runtime to vulnerabilities in image parsing dependencies.

Mitigation: Use trusted images when possible and pin Pillow to a reviewed version before deployment.

Risk: Image outputs are written to caller-supplied paths and can overwrite files if paths are chosen carelessly.

Mitigation: Write generated images to a dedicated output directory and review output paths before running workflows.

Risk: The documentation and examples are Chinese-first, which can increase operator error for teams that do not read Chinese.

Mitigation: Translate or review the API examples before production use.

## Reference(s):

- [Picture Edit ClawHub Skill Page](https://clawhub.ai/hgta23/skills/picture-edit)
- [Artifact README](artifact/README.md)
- [Artifact SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Guidance, Files]

**Output Format:** [Markdown guidance with Python code examples and shell commands; executed workflows may write image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local Pillow operations; security evidence reports no hidden network access, persistence, credential use, or destructive behavior.]

## Skill Version(s):

1.0.0 (source: release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
