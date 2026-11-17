## Description:

Helps agents prepare and run GPT Image 2 multi-reference image-generation jobs through AI Hive using per-reference responsibility contracts for allowed attributes, denied attributes, ownership, identity sources, layout anchors, and conflict priorities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, marketers, and ecommerce operators use this skill to compose 2-8 reference images into a single GPT Image 2 request while preserving subject, product, identity, layout, scene, and copy-space responsibilities. It is suited to catalog, advertising, social, product-detail, lookbook, interior, packaging, and other reviewable commercial image workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected reference images and generated prompts are sent to AI Hive for processing.

Mitigation: Use only images and prompts approved for AI Hive handling, and remove confidential or unlicensed content unless sharing is authorized.

Risk: API keys may be exposed if pasted into shared shell commands, committed files, or permissive config files.

Mitigation: Prefer AI_HIVE_API_KEY or the protected config file, keep real keys out of examples and version control, and verify local config permissions.

Risk: Network timeouts can make users resubmit a generation job and create duplicate work or cost.

Mitigation: Use the returned task ID with the status command after a timeout before starting a new generation.

Risk: Generated images can still blend identities, product attributes, text, or layouts contrary to the reference contract.

Mitigation: Review each output against the allow, deny, ownership, conflict, and consistency-lock fields before publication, then reduce references or strengthen conflict rules when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/image-2-multi-reference-image)
- [AI Hive OpenAPI endpoint](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown instructions with bash commands, JSON preview/status output, and downloaded PNG image files when generation is run.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed GPT Image 2 public model ID, accepts 2-8 reference images, supports routing and generation parameters, and can preview the constructed prompt before upload.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
