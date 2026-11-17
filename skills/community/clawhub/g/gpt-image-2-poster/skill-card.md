## Description:

Helps agents prepare structured GPT Image 2 poster briefs and AI Hive image-generation commands for event, product launch, promotion, hiring, exhibition, conference, Chinese-language, and bilingual poster layouts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, designers, and marketing teams use this skill to have an agent structure poster requirements, generate AI Hive commands for GPT Image 2, and preserve text-heavy fields for later human layout and proofreading.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A locally stored AI Hive API key can be sent to a custom API endpoint if the base URL is overridden.

Mitigation: Use the default HTTPS endpoint and avoid --base-url or AI_HIVE_BASE_URL unless the destination server is trusted.

Risk: The tool depends on runtime installation of requests and network access to AI Hive services.

Mitigation: Install dependencies in an isolated environment with pinned versions where possible.

Risk: Generated poster imagery and layout placeholders may still contain inaccurate or misleading event, product, speaker, price, legal, or brand information.

Mitigation: Use approved source materials for factual fields and perform character-level review before publishing or printing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-poster)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; generated tasks can return JSON status and downloaded PNG files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI_HIVE_API_KEY, supports reference images and batch generation, and saves generated files to the configured output directory.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact changelog top entry is 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
