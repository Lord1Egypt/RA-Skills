## Description: <br>
Analyzes product main images and optional additional images with multimodal AI to extract structured visual attributes and image prompts for e-commerce product records. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linkfox-ai](https://clawhub.ai/user/linkfox-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External e-commerce sellers and developers use this skill to turn product lists with image URLs into structured visual attributes, grouped attribute distributions, and tabular results for comparison. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Product image URLs, listing data, prompts, and supplied context may be sent to LinkFox for analysis. <br>
Mitigation: Use the skill only with data approved for transfer to LinkFox, avoid confidential catalog data, and keep prompts and context narrowly scoped. <br>
Risk: The artifact describes automatic feedback reporting to a separate LinkFox endpoint without clear consent. <br>
Mitigation: Disable or avoid feedback reporting unless users have explicitly agreed to that separate data transfer. <br>
Risk: The release security verdict is suspicious because feedback behavior expands data sharing beyond the image-analysis API. <br>
Mitigation: Review the skill before installation and confirm the feedback behavior matches the intended deployment policy. <br>


## Reference(s): <br>
- [API Reference](references/api.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/linkfox-ai/linkfox-multimodal-extract-attributes) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, json] <br>
**Output Format:** [Markdown guidance with API parameters, shell examples, and JSON response structures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces product records enriched with attributeName and attributeValue, grouped attribute summaries, table columns, and token cost when the LinkFox API call succeeds.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
