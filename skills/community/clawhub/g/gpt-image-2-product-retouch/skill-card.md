## Description:

Uses GPT Image 2 through AI Hive to retouch product photography for dust and scratch removal, edge repair, reflection control, material enhancement, color calibration, packaging cleanup, and batch studio consistency while preserving product structure, labels, logos, colors, materials, and sales facts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, marketplace operators, and product-content teams use this skill to guide AI-assisted product-photo retouching and to run the bundled AI Hive image task helper. It is intended for faithful commercial product cleanup, SKU consistency, and review workflows that preserve material, label, logo, color, and structural facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected product images and an AI Hive API key are sent through the helper script.

Mitigation: Use the skill only when this data transfer is acceptable, provide only intended product images, and keep the API key in a protected environment variable or 0600 config file.

Risk: The helper permits configurable API endpoints and downloads generated files from task result URLs.

Mitigation: Use the default AI Hive endpoint, avoid untrusted base URLs or config files, and choose a safe output directory until URL validation, safe filenames, and download limits are added.

Risk: Faithful product retouching can become misleading if true condition details are removed.

Mitigation: Compare each output with the original image and preserve material, label, logo, color, structure, wear, food appearance, medical product condition, and other sales-relevant facts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/gpt-image-2-product-retouch)
- [Publisher profile](https://clawhub.ai/user/wubin1836)
- [AI Hive API endpoint](https://ai-hive.iclip.cn/api)
- [AI Hive API key setup](https://ai-hive.iclip.cn/chat)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration, code]

**Output Format:** [Markdown guidance with bash command examples and a Python helper that submits image tasks, queries task status, and downloads generated image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-selected input images and an AI Hive API key; generated image files are saved to a local output directory unless downloads are disabled.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
