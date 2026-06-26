## Description: <br>
Searches and recommends suitable prompts from a curated Nano Banana Pro image generation prompt library based on the user's needs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dophinl](https://clawhub.ai/user/dophinl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators, marketers, and developers use this skill to find image-generation prompt templates, compare examples, and customize selected prompts for articles, products, social posts, posters, and other visual assets. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill fetches and refreshes mutable prompt reference data from GitHub, so local results may change over time. <br>
Mitigation: Review scripts/setup.js before installation and use manual or pinned reference updates when stable, auditable prompt data is required. <br>
Risk: Prompt recommendations may involve external preview-image URLs. <br>
Mitigation: Review external media links before sharing or using them in sensitive channels. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dophinl/nano-banana-pro-prompts) <br>
- [YouMind Nano Banana Pro prompt gallery](https://youmind.com/nano-banana-pro-prompts?utm_source=nano-banana-pro-prompts-recommend) <br>
- [Prompt reference data path](https://github.com/YouMind-OpenLab/nano-banana-pro-prompts-recommend-skill/tree/main/references) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown responses with prompt recommendations, preview links, optional sample images, and fenced prompt text for custom remixes.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends at most three matching library prompts per request, supports later customization after user selection, and includes an attribution footer.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
