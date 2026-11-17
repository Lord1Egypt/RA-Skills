## Description:

Generates single-file, horizontal-swipe HTML presentation decks, deck visuals, and social cover pages using editorial magazine or Swiss International visual systems.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haixiandaxia-jpg](https://clawhub.ai/user/haixiandaxia-jpg)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, presenters, and developers use this skill to turn articles, outlines, screenshots, or product material into browser-presentable HTML decks, optional generated visuals, and social cover assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated decks can load third-party web scripts or fonts.

Mitigation: For sensitive decks, remove or vendor remote dependencies and prefer offline local assets for icons, fonts, animations, and maps.

Risk: The deck-generation workflow reads and writes local presentation files.

Mitigation: Review requested source paths and output paths before running generated shell commands or writing presentation artifacts.

Risk: Hosted HTML decks can expose private presentation content if published to a shared or sensitive origin.

Mitigation: Redact sensitive content before sharing and avoid hosting generated decks on an origin that also contains private application data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/haixiandaxia-jpg/skills/haixian-ppt-skill)
- [Publisher profile](https://clawhub.ai/user/haixiandaxia-jpg)
- [Project homepage from ClawHub metadata](https://github.com/op7418/guizang-ppt-skill)
- [Quality checklist](references/checklist.md)
- [Components reference](references/components.md)
- [Image prompt rules](references/image-prompts.md)
- [Editorial layout library](references/layouts.md)
- [Swiss layout library](references/layouts-swiss.md)
- [Screenshot framing rules](references/screenshot-framing.md)
- [Swiss layout lock](references/swiss-layout-lock.md)
- [Swiss map component](references/swiss-map-component.md)
- [Editorial theme presets](references/themes.md)
- [Swiss theme presets](references/themes-swiss.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript, and shell command snippets; generated artifacts are single-file HTML decks and image assets when requested.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require local filesystem access and Node.js for Swiss deck validation; generated HTML may use local or third-party web assets depending on the selected template.]

## Skill Version(s):

1.0.0 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
