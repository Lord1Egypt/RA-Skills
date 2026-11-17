## Description:

Uses GPT Image 2 through AI Hive to convert product-photo retouching requests into localized, acceptance-tested defect tickets that preserve SKU facts, structure, materials, logos, packaging, people, and composition.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External creators, ecommerce operators, and product-content teams use this skill to prepare controlled retouching jobs for product photos, packaging, labels, color correction, reflections, model-held products, and white-background listings. It emphasizes QC sources, edit zones, acceptance criteria, and preservation rules before submitting images for generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-selected source images and QC references are transferred to AI Hive for generation.

Mitigation: Use the skill only with images approved for remote processing and avoid submitting sensitive, embargoed, or unlicensed product assets.

Risk: The API key can be saved under ~/.ai-hive/config.json or supplied through the environment.

Mitigation: Prefer a dedicated low-scope key or environment variable, and keep any saved config file private with restrictive permissions.

Risk: Dependency installation and remote downloads create operational exposure.

Mitigation: Install dependencies in a dedicated virtual environment, consider pinning versions, and review downloaded outputs before publishing.

Risk: Retouching can unintentionally alter labels, SKU facts, material appearance, or a model's identity and body attributes.

Mitigation: Provide QC truth sources, inspect each defect zone at 100%, compare unchanged regions against the original, and reject outputs that modify unauthorized areas.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/wubin1836/skills/image-2-product-retouch)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api/openapi/v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash examples, JSON preview output, status JSON, and downloaded image files when generation completes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Submits one image-generation version per retouch job and can preview the fixed model, source ordering, prompt, and parameters without uploading.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
