## Description: <br>
Hd Infoimage helps an agent create high-density infographic images from supplied articles or content using a configured image-generation service and nine visual styles. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dadaniya99](https://clawhub.ai/user/dadaniya99) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, educators, and marketing teams use this skill to convert articles or knowledge content into dense visual infographics for notes, course materials, course content visualization, and social sharing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a ZenMux image-generation credential and references local API key access. <br>
Mitigation: Use runtime-managed secrets and avoid commands or workflows that print API keys from local configuration files. <br>
Risk: The skill may send article content to an external image provider and may send generated images to Feishu. <br>
Mitigation: Avoid confidential source material and confirm the external provider and Feishu destination before running the workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dadaniya99/hd-infoimage) <br>
- [Style 01: Coordinate Blueprint Pop Laboratory](references/style-01-坐标蓝图·波普实验室.md) <br>
- [Style 02: Retro Pop Grid](references/style-02-复古波普网格风.md) <br>
- [Style 03: Folder Thermal Paper](references/style-03-文件夹风格（打印热敏.md) <br>
- [Style 04: Color Block Thermal Paper](references/style-04-色块·热敏纸风（英文.md) <br>
- [Style 05: Retro Journal Archive](references/style-05-复古手帐·档案风.md) <br>
- [Style 06: Archive Mixed Media](references/style-06-档案·混合媒介风（英.md) <br>
- [Style 07: Retro-Future Acid Color Blocks](references/style-07-色块·复古未来酸性风.md) <br>
- [Style 08: Theater Ticket](references/style-08-票据·剧场戏票风.md) <br>
- [Style 09: Claude Clay Style](references/style-09-Claude陶土风.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with prompt text and optional shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can guide image generation through a configured external provider and may reference a downstream Feishu delivery step.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
