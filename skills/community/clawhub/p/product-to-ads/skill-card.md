## Description:

Generates professional advertising images from product URLs using the Ad-Ready pipeline on ComfyDeploy, with optional brand profiles, funnel-stage targeting, model or talent inputs, and multi-format output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pauldelavallaz](https://clawhub.ai/user/pauldelavallaz)

### License/Terms of Use:


## Use Case:

External marketers, brand teams, and creative operators use this skill to turn product URLs and product assets into ad-ready image-generation runs for campaign funnel stages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Auto-fetch can retrieve arbitrary product URLs and upload retrieved assets to a cloud service.

Mitigation: Use trusted product URLs and assets, avoid auto-fetch for untrusted or internal URLs, and run the skill in a sandbox with restricted network access.

Risk: Product data, uploaded images, model references, logos, and generated outputs interact with ComfyDeploy.

Mitigation: Review privacy, confidentiality, and rights before submitting assets or product data to the workflow.

Risk: Talent or model image inputs may involve likeness rights and sensitive appearance handling.

Mitigation: Use only images for which the user has consent and rights, and avoid supplying real talent/model images without clear authorization.

Risk: Generated ad content may contain inaccurate product claims or brand-inconsistent creative choices.

Mitigation: Review generated outputs before publication, especially product claims, CTA language, brand fit, and regulated-category messaging.

## Reference(s):

- [Product to Ads (Ad-Ready) ClawHub listing](https://clawhub.ai/pauldelavallaz/skills/product-to-ads)
- [pauldelavallaz ClawHub publisher profile](https://clawhub.ai/user/pauldelavallaz)
- [ComfyDeploy queue endpoint used by the skill](https://api.comfydeploy.com/api/run/deployment/queue)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands; generated advertising assets are saved as image files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use product URLs, product images, brand logos, reference ads, model or talent images, brand profiles, funnel-stage prompt profiles, aspect ratios, language, and creative briefs.]

## Skill Version(s):

1.4.0 (source: server evidence release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
