## Description:

Generate or edit raster images for websites, games, UI mockups, product shots, textures, sprites, and other bitmap assets using a host-approved image generation capability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zack-dev-cm](https://clawhub.ai/user/zack-dev-cm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to turn image requests into compact production prompts, invoke host-approved image generation or editing tools, verify outputs, and save selected bitmap assets into projects.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated images can contain inaccurate details, poor text rendering, or rights-sensitive content such as logos, endorsements, or identity-preserving edits.

Mitigation: Review generated images for accuracy, rights-sensitive content, requested invariants, and in-image text before using or publishing them.

Risk: Project-bound image assets can be left outside the workspace or referenced before the selected final output is saved.

Mitigation: Save selected final assets into the workspace, update consuming references, and report the saved path and final prompt.

## Reference(s):

- [Prompting best practices](references/prompting.md)
- [Sample prompts](references/sample-prompts.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance, files]

**Output Format:** [Markdown guidance with prompt specifications, verification notes, saved-path reporting, and optional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in project-bound bitmap image files when the host-approved image generation or editing capability is used.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
