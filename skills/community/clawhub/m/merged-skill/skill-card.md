## Description:

Generate professional social cards and magazine-style posters for Xiaohongshu, WeChat, magazine posters, carousel images, and other high-quality visual content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gf1023456](https://clawhub.ai/user/gf1023456)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, marketers, and agent users use this skill to turn articles, product notes, screenshots, travel material, or photos into rendered social cards, Xiaohongshu carousel images, and WeChat cover pairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may rely on npx or git commands that install mutable external code.

Mitigation: Review the exact commands before installation and prefer a pinned commit or trusted package version.

Risk: Generated workflows may fetch online images, fonts, or map resources.

Mitigation: Confirm before allowing external fetching, prefer local assets for sensitive work, and record image sources when web assets are used.

Risk: Prompts or generated HTML may include private locations or real API tokens.

Mitigation: Use placeholder credentials, avoid private location details, and remove secrets from generated files before rendering or sharing.

## Reference(s):

- [Skill definition](artifact/SKILL.md)
- [English README](artifact/README.en.md)
- [Layout recipes](artifact/references/layout-recipes.md)
- [Theme presets](artifact/references/theme-presets.md)
- [Style system](artifact/references/style-system.md)
- [Production workflow](artifact/references/production-workflow.md)
- [Image overlay guidance](artifact/references/image-overlay.md)
- [Map component](artifact/references/map-component.md)
- [QA checklist](artifact/references/qa-checklist.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTML, CSS, JavaScript snippets, and local render commands; generated task files can render PNG social cards.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces single-file HTML/CSS poster frames for fixed social-media canvas sizes and can invoke Playwright rendering and validation.]

## Skill Version(s):

1.0.0 (source: target metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
