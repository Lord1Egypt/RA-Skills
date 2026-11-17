## Description:

Guides agents to combine multiple authorized reference images into new GPT Image 2 outputs through AI Hive, with explicit role contracts for identity, product, clothing, scene, lighting, composition, and brand style.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Creative, brand, and e-commerce teams use this skill to direct an agent through multi-reference image generation where each reference image has a narrow, auditable role. It is suited for product advertising, character continuity, outfit and scene composition, furniture placement, and market asset generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an AI Hive API key and can store or read that credential from local configuration or environment variables.

Mitigation: Use a dedicated low-privilege API key, avoid sharing the generated config file, and rotate the key if it is exposed.

Risk: Reference media selected by the user is uploaded to AI Hive for generation.

Mitigation: Use only authorized media and avoid uploading confidential, regulated, or third-party content unless that use is approved.

Risk: Generated files may be downloaded into a local output directory.

Mitigation: Run from a contained environment and choose an output directory where accidental overwrites or downloaded content will not affect important files.

Risk: A custom AI_HIVE_BASE_URL or --base-url can route requests to a non-default endpoint.

Mitigation: Keep the default endpoint unless the alternate service is fully trusted and approved.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wubin1836/skills/gpt-image-2-multi-reference-image)
- [AI Hive API Access](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline bash commands and Python helper invocation patterns]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces prompts, reference-role contracts, command examples, task IDs, and locally downloaded generated image files when executed with AI Hive credentials.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
