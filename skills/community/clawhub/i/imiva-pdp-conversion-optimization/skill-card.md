## Description:

商品页转化率优化 helps brand merchants, ecommerce operators, designers, and content teams use IMIVA MCP to restructure product detail pages around purchase doubts, verified selling points, detail modules, parameters, and calls to action.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wubin1836](https://clawhub.ai/user/wubin1836)

### License/Terms of Use:

MIT-0

## Use Case:

External ecommerce teams and agents use this skill to plan, configure, and run IMIVA product-detail-page generation tasks after confirming product facts, materials, channel requirements, budget, and source rights.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged for review because it runs a changing npm package with the user's token and inherited environment.

Mitigation: Use a dedicated low-privilege IMIVA token, remove unrelated secrets from the environment, run from a clean sandbox, and pin a reviewed package version before production use.

Risk: IMIVA task creation can consume credits when generation settings are submitted.

Mitigation: Check credits, confirm model, quantity, resolution, and budget with the user before creating paid tasks, and save task IDs for follow-up instead of resubmitting blindly.

Risk: Generated product page assets can contain inaccurate claims or unauthorized reference usage if product facts and rights are not verified.

Mitigation: Use only user-confirmed product facts, verify reference-material rights, and require human review for prices, certifications, performance claims, brand assets, and platform policy fit before publishing.

## Reference(s):

- [IMIVA homepage](https://imiva.ecpro.com/)
- [MCP configuration example](artifact/references/mcp-config.example.json)
- [ClawHub skill page](https://clawhub.ai/wubin1836/skills/imiva-pdp-conversion-optimization)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include IMIVA task arguments, budget checks, task IDs, result links, and human review checkpoints.]

## Skill Version(s):

1.0.0 (source: artifact frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
