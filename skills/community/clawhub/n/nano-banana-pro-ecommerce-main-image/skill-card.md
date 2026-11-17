## Description:

使用 Nano Banana Pro 通过 AI Hive 生成移动端缩略图清晰、品牌一致、适合电商转化的商品主图，覆盖货架电商、内容电商、跨境 Listing 和 SKU 系列。

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce operators, marketers, and developers use this skill to generate or edit product main images from prompts and optional reference media for marketplaces, content commerce, cross-border listings, and SKU series. It emphasizes thumbnail readability, product accuracy, channel-safe composition, and batch-consistent visual grammar.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow requires an AI Hive API key and may upload selected product media to the configured AI Hive endpoint.

Mitigation: Use a dedicated API key where possible, keep secrets out of shared logs, upload only media you are authorized to process, and prefer the default trusted endpoint unless another endpoint is deliberately approved.

Risk: Remote generation results are downloaded to a local output directory and the security evidence flags unsafe remote-result download handling.

Mitigation: Choose a controlled output directory, inspect generated files before reuse, and avoid running the workflow from locations where unexpected file writes could matter until download path validation is fixed.

Risk: The bundled script includes broader AI Hive capabilities beyond the ecommerce image-generation workflow.

Mitigation: Review commands before execution and use the skill-specific generate, task, upload, and init interface for this release.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/wubin1836/skills/nano-banana-pro-ecommerce-main-image)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, image files, JSON status]

**Output Format:** [Markdown guidance with bash commands; generated image files are downloaded locally and task/status responses may be JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports optional reference images, batch size, aspect-ratio/model parameters, routing mode, output directory, and no-download task submission.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
