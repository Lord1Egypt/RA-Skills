## Description:

Use this skill to list and retrieve DynaPictures templates or generate images through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and creative teams use the skill to browse DynaPictures templates and generate images from them through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic setup may execute changing remote code and introduce broader agent changes without clear approval.

Mitigation: Review and approve CLI installation separately, including any bundled skills it adds or synchronizes. Prefer a verified, version-pinned installation and prevent automatic setup until reviewed.

Risk: Using the connected service involves OOMOL account access and handling of template or image data.

Mitigation: Confirm that OOMOL's account access and handling of template and image data suit your needs.

## Reference(s):

- [DynaPictures API documentation](https://dynapictures.com/docs/)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [ClawHub release](https://clawhub.ai/oomol/skills/oo-dynapictures)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Text, Image URLs]

**Output Format:** [Markdown guidance with shell command and JSON examples; action results are returned as JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Image generation returns hosted image URLs; available templates and results depend on the connected DynaPictures account.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
