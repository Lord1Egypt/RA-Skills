## Description:

Generate green-screen raster subject assets with an image model and convert them into transparent PNGs with robust chroma-key cutout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[act-chao](https://clawhub.ai/user/act-chao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and designers use this skill to create transparent foreground bitmap assets such as stickers, sprites, props, icons, and collectibles from green-screen source images. It guides prompt construction, chroma-key processing, QA review, and project asset integration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented cutout command points to an unbundled script at a hardcoded Windows user path.

Mitigation: Before use, confirm the chroma-key script is bundled with the installed skill and invoke it through a relative, reviewed path.

Risk: The artifact behavior allows automatic installation of Python dependencies.

Mitigation: Install dependencies only through an explicit reviewed setup process with pinned versions from trusted sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/act-chao/skills/green-screen-cutout-assets)
- [Server-resolved GitHub source](https://github.com/ACT-chao/green-screen-cutout-assets-skill/tree/master/green-screen-cutout-assets)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with prompts, file paths, command examples, QA criteria, and integration checklist items]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May result in transparent PNG assets, JSON cutout reports, contact sheets, and asset manifest updates when followed by an agent.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
