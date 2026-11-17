## Description:

This skill helps agents plan and generate modular product detail page visual backgrounds with Nano Banana 2 through AI Hive, covering hero, problem, benefit, proof, usage, specification, and lifestyle sections.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

E-commerce operators, designers, and developers use this skill to turn approved product references, copy, and evidence into ordered PDP, Amazon A+, marketplace, and Shopify visual modules. It supports image-generation workflows where final text, claims, certifications, and comparison data are laid out and checked outside the generated image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reference images, prompts, and product evidence are sent to AI Hive during generation.

Mitigation: Use only reference images, claims, and product data that are approved for upload to AI Hive.

Risk: The security summary says the helper trusts remote service responses in ways that could contact unintended network locations or write files outside the chosen output folder.

Mitigation: Run the skill in a dedicated working directory or sandbox and prefer --no-download or a constrained output directory until filename handling is fixed.

Risk: The helper requires an AI Hive API key and the requests dependency.

Mitigation: Protect API keys, avoid committing local config files, and install dependencies in a virtual environment with pinned versions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/nano-banana-2-product-detail-page)
- [AI Hive API access page](https://ai-hive.iclip.cn/chat)
- [AI Hive API endpoint used by the helper](https://ai-hive.iclip.cn/api)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, files]

**Output Format:** [Markdown guidance with bash command examples; helper script output includes task IDs, status JSON, and downloaded image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a fixed Nano Banana 2 image model through AI Hive, accepts optional reference images, and can run with --no-download for task-only output.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
