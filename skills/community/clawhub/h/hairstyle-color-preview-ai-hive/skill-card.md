## Description:

This skill helps agents produce Chinese workflows, prompts, runnable AI-HIVE commands, and quality checklists for authorized AI hairstyle and hair-color preview images.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, hairstylists, salons, ecommerce teams, and beauty content teams use this skill to plan and generate reviewable hairstyle and hair-color preview assets from authorized portraits and reference materials.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys and authorized portrait or media files may be sent to configurable AI-HIVE endpoints.

Mitigation: Use the official HTTPS endpoint, avoid custom base URLs, protect ~/.ai-hive/config.json, and confirm prompts, routing, and cost before generation.

Risk: Generated hairstyle previews may be mistaken for real dye outcomes, suitability advice, or authorized endorsements.

Mitigation: Use only authorized portraits and mark uncertain visual, product, pricing, performance, or endorsement claims for human review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/hairstyle-color-preview-ai-hive)
- [AI-HIVE chat](https://ai-hive.iclip.cn/chat)
- [AI-HIVE API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with JSON files and inline bash commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May submit AI-HIVE API calls and download generated media after user confirmation; requires AI_HIVE_API_KEY for generation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
