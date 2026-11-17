## Description:

Helps jewelry brands, merchants, photography teams, and social commerce creators turn authorized jewelry try-on requests into visual briefs, prompts, runnable AI-HIVE commands, task records, and quality checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, jewelry sellers, and production teams use this skill to plan and optionally run AI-HIVE jewelry try-on image generation for e-commerce, advertising, social commerce, and marketing workflows. It emphasizes authorized inputs, product-structure preservation, billable-generation confirmation, and human review of factual claims.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API client can forward the user's API key and selected media to an unvalidated custom endpoint.

Mitigation: Use the default AI-HIVE endpoint; avoid --base-url or AI_HIVE_BASE_URL unless the endpoint is controlled and trusted.

Risk: Generation may be billable and may upload user-selected media.

Mitigation: Confirm every billable generation and upload only images or media the user is authorized to share with AI-HIVE.

Risk: Generated jewelry try-on previews may overstate product facts or imply unauthorized use of people, brands, or materials.

Mitigation: Manually review gemstone grades, certificates, weights, materials, proportions, endorsements, and usage rights before publication.

## Reference(s):

- [AI-HIVE chat and API key setup](https://ai-hive.iclip.cn/chat)
- [AI-HIVE default API endpoint](https://ai-hive.iclip.cn/api)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/jewelry-tryon-preview-ai-hive)
- [Publisher profile](https://clawhub.ai/user/wubin1836)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown responses with JSON files and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce blueprint.json and downloaded image files when generation commands are executed.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
