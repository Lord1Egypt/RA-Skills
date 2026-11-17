## Description:

This skill helps editors, ad post-production teams, and product operators turn product-demo B-roll gaps into shot plans, prompts, runnable AI-HIVE video-generation commands, and acceptance checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creative and ecommerce video teams use this skill to plan and generate short product-demo B-roll inserts, produce prompts and task records, and perform deterministic video checks or aspect-ratio edits before platform delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI-HIVE API key and can upload selected media to AI-HIVE.

Mitigation: Install only when the user is comfortable sharing the selected media with AI-HIVE and keep API keys out of prompts, logs, screenshots, and version control.

Risk: Custom --base-url or AI_HIVE_BASE_URL settings could send credentials and media to an untrusted endpoint.

Mitigation: Use the default AI-HIVE endpoint for production keys unless the alternate endpoint is fully trusted and reviewed.

Risk: Generated image or video tasks may be billable.

Mitigation: Review prompts, routing mode, model choice, and pricing snapshot before running generation commands; use small samples before batch work.

Risk: Product B-roll can misrepresent product behavior or rely on unauthorized reference material.

Mitigation: Use authorized inputs, mark unverified claims for review, and check generated clips against product facts before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-demo-broll-generator-ai-hive)
- [AI-HIVE chat and API access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown response with command snippets and optional JSON blueprint or media files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call AI-HIVE OpenAPI, upload selected media, poll tasks, and download generated video assets; generated operations may be billable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
