## Description: <br>
AI poster-making skill for style recreation, creative product poster generation, and livestream preview posters, with prompt templates, copywriting guidance, style analysis guidance, and a helper script for image generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dizhu](https://clawhub.ai/user/dizhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing, ecommerce, and content teams use this skill to plan and generate product posters, livestream announcement posters, social media creative, and brand promotional assets. The skill helps an agent analyze reference styles, draft compliant poster copy, assemble detailed image-generation prompts, and optionally call an image-generation script. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The helper script may send an OpenRouter API key to the Ofox API endpoint. <br>
Mitigation: Use OFOX_API_KEY with the current script, avoid setting OPENROUTER_API_KEY for this skill unless endpoint selection is corrected, and review the script before installation. <br>
Risk: Poster prompts can include confidential product, launch, pricing, or campaign details that are sent to an external image provider. <br>
Mitigation: Do not include confidential campaign or product details unless the user has approved sharing them with the configured image-generation provider. <br>


## Reference(s): <br>
- [Poster Maker on ClawHub](https://clawhub.ai/dizhu/poster-maker) <br>
- [Prompt templates](references/Prompt模板.md) <br>
- [Copywriting principles](references/文案原则.md) <br>
- [Style analysis guide](references/风格分析指南.md) <br>
- [Ofox image generation API endpoint](https://api.ofox.ai/v1/images/generations) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Text, Shell commands, Code, Files] <br>
**Output Format:** [Markdown guidance, image-generation prompts, shell commands, and generated image files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an Ofox API key; the helper script can read either OFOX_API_KEY or OPENROUTER_API_KEY.] <br>

## Skill Version(s): <br>
1.7.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
