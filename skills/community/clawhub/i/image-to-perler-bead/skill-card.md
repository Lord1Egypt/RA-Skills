## Description:

Converts user-provided photos into Perler or Hama bead patterns with printable HTML grids, PNG previews, material lists, and optional JSON pattern data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhouhuijia](https://clawhub.ai/user/zhouhuijia)

### License/Terms of Use:

MIT-0

## Use Case:

External craft users and agents assisting them use this skill to turn portraits, logos, pet photos, cartoons, or other images into bead craft patterns, printable guides, and material counts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Dependency installation uses Pillow without a pinned version.

Mitigation: Install dependencies only in an isolated environment and pin or approve a known Pillow version before running the converter.

Risk: Very large image, width, height, or cell-size settings can exhaust local CPU, memory, or disk resources.

Mitigation: Use practical bead dimensions, avoid oversized source images, and review generated output sizes before batch processing.

Risk: Crafting the generated design involves heat tools and possible cutting or trimming.

Mitigation: Supplement the generated craft guide with heat and blade safety precautions appropriate for the user and workspace.

## Reference(s):

- [Advanced usage](references/advanced.md)
- [Crafting guide](references/crafting_guide.md)
- [Palette reference](references/palette.md)
- [ClawHub skill page](https://clawhub.ai/zhouhuijia/skills/image-to-perler-bead)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance, files]

**Output Format:** [Markdown guidance plus generated HTML pattern files, PNG previews, console material summaries, and optional JSON pattern data.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a local image path and bead pattern options such as width, height, fit or cover mode, dither, color codes, grid display, and cell size.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
