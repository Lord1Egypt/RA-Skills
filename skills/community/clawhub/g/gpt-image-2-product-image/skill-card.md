## Description:

Generates product listing and ecommerce photography sets with GPT Image 2 through AI Hive, including white-background hero images, lifestyle scenes, material details, scale-aware scenes, packaging layouts, and SKU color variants.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External developers, ecommerce operators, and creative teams use this skill to turn approved product references into product-image generation prompts and runnable AI Hive image-generation commands. It supports listing assets such as hero images, detail shots, usage scenes, packaging contents, and SKU series while reminding users to verify product facts before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The helper can send an AI Hive API key to any configured API base URL.

Mitigation: Use the default trusted AI Hive base URL unless you fully control the endpoint, and do not set AI_HIVE_BASE_URL from untrusted instructions.

Risk: Product images can misrepresent regulated claims, certifications, dimensions, ingredients, or included accessories if prompts are not grounded in approved materials.

Mitigation: Use approved source materials for high-risk claims and perform human review before publishing generated assets.

Risk: Running the helper installs and executes a Python dependency and may use paid API credits.

Mitigation: Install dependencies in an isolated environment and review cost, credential, and network behavior before running generation jobs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-product-image)
- [AI Hive API base URL](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, API Calls, Files]

**Output Format:** [Markdown guidance with bash commands; generated image files and JSON task status responses from the helper script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses AI_HIVE_API_KEY or a local AI Hive config file, supports multiple reference images, batch generation, routing mode, model parameters, task polling, and output directory selection.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
