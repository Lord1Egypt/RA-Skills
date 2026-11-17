## Description:

End-to-end AI-powered pipeline for creating 3D-printable IP character figurines with three-mode image generation and automated Blender modeling for STL export.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emergencescience](https://clawhub.ai/user/emergencescience)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and makers use this skill to turn text prompts or reference images into collectible-style character concepts and Blender-generated meshes for 3D printing. It supports image-reference generation, procedural modeling, print-oriented modifiers, and STL or editable Blender output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses API credentials and may send prompts or reference images to external image-generation providers.

Mitigation: Avoid confidential prompts or reference images and use restricted, low-quota API keys.

Risk: The skill includes Blender automation that creates generated files under /tmp/skullpanda_output.

Mitigation: Review scripts before execution and run them only in a fresh/background Blender session.

Risk: Server security evidence marks the release suspicious because the 3D-printing workflow combines credentials with automation.

Mitigation: Review before installing or running, and apply the server-provided guidance for credential and execution isolation.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/emergencescience/skills/ipdesign-3dprint)
- [Google AI Studio](https://aistudio.google.com)
- [Comfy Cloud](https://platform.comfy.org)
- [EvoLink](https://evolink.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, Python, and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce or guide creation of Blender scene files and STL/OBJ/3MF mesh exports when executed with Blender.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
