## Description:

Generates high-density visual infographics from user-provided articles or content, with nine supported visual styles and 4K-oriented image generation prompts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dadaniya99](https://clawhub.ai/user/dadaniya99)

### License/Terms of Use:

MIT-0

## Use Case:

Content creators, educators, and knowledge workers use this skill to turn articles, notes, and course material into dense visual infographic prompts and generated image assets for knowledge sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may expose a local API key if an agent follows credential-printing instructions.

Mitigation: Do not allow the skill to print local API keys, and remove or rewrite credential-reading instructions before use.

Risk: The skill may send generated images to Feishu through an unspecified external-delivery script.

Mitigation: Use only non-sensitive content and require explicit approval before any external delivery.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dadaniya99/skills/hd-infoimage)
- [Publisher profile](https://clawhub.ai/user/dadaniya99)
- [Skill definition](artifact/SKILL.md)
- [Style 01: Coordinate Blueprint Pop Laboratory](artifact/references/style-01-坐标蓝图·波普实验室.md)
- [Style 02: Retro Pop Grid](artifact/references/style-02-复古波普网格风.md)
- [Style 03: Folder Thermal Paper](artifact/references/style-03-文件夹风格（打印热敏.md)
- [Style 04: Color Block Thermal Paper](artifact/references/style-04-色块·热敏纸风（英文.md)
- [Style 05: Vintage Journal Archive](artifact/references/style-05-复古手帐·档案风.md)
- [Style 06: Archival Mixed Media](artifact/references/style-06-档案·混合媒介风（英.md)
- [Style 07: Retro-Futurist Acid Graphic](artifact/references/style-07-色块·复古未来酸性风.md)
- [Style 08: Theater Ticket](artifact/references/style-08-票据·剧场戏票风.md)
- [Style 09: Claude Terracotta](artifact/references/style-09-Claude陶土风.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with image-generation prompts and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce image files when used with a configured image generation service.]

## Skill Version(s):

1.2.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
