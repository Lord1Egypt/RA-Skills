## Description:

Generates and edits auditable ecommerce product image suites for a single SKU with controlled product facts, reference-image roles, claim records, layout guidance, and AI Hive Nano Banana Pro image generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce sellers, product photographers, and brand teams use this skill to create consistent product image suites for marketplace listings, PDP/A+ assets, social commerce covers, comparison images, and localized product visuals while keeping SKU facts and approved claims traceable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: API keys can be stored locally and used to submit paid AI Hive generation requests.

Mitigation: Install in a virtual environment, use only trusted machines, prefer environment-scoped credentials where possible, and review the local AI Hive config before sharing the workstation.

Risk: Reference images are uploaded to AI Hive during render mode.

Mitigation: Upload only images the user is authorized to send to AI Hive and use brief mode when only prompt validation is needed.

Risk: Generated product images may contain inaccurate parts, colors, labels, claims, text, measurements, or marketplace-sensitive content.

Mitigation: Compare each output against source images and approved records; require human review for claims, measurements, generated text, and platform policy compliance before publication.

Risk: Unpinned dependencies may change behavior over time.

Mitigation: Install in an isolated environment and consider pinning requests as recommended by the security guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/product-image-suite-generation-editing)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive OpenAPI endpoint used by the script](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated prompt text; render/status commands can also produce downloaded image files and JSON status output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses user-provided SKU facts, reference-image roles, suite slots, claim records, and optional generation parameters; render mode uploads selected reference images to AI Hive and downloads PNG results.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
