## Description: <br>
Production-grade operational guide for creating, managing, optimizing, and documenting Meta (Facebook/Instagram) ad campaigns via the Facebook Ads MCP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[benkalsky](https://clawhub.ai/user/benkalsky) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing operators, growth teams, and agents use this skill to plan Meta ad campaigns, create campaign objects through Facebook Ads MCP tools, review spend and performance, and document campaign decisions with approval and safety guardrails. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed campaign changes can cause accidental ad spend or launch incorrect ads. <br>
Mitigation: Confirm Facebook Ads MCP permissions, create campaign entities in PAUSED status, set spending limits, preview ads, and activate only after human approval. <br>
Risk: Customer-list uploads and CAPI event parameters can expose regulated personal data. <br>
Mitigation: Do not upload customer lists or send CAPI PII unless the organization has documented consent, data minimization, opt-out handling, and SHA-256 hashing controls. <br>
Risk: Using the wrong ad account, page, pixel, or dataset can misroute spend and corrupt reporting. <br>
Mitigation: Verify the ad account, linked page, dataset details, pixel installation, billing status, and Event Match Quality before creating or changing campaigns. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/benkalsky/meta-ads-mcp) <br>
- [Account, Architecture & Naming](references/campaign-architecture.md) <br>
- [Budget Strategy & Audience Targeting](references/budget-and-audience.md) <br>
- [Ad Formats, Copy & Asset Generation](references/creative-and-copy.md) <br>
- [Pixel/CAPI Tracking & Retargeting](references/tracking-and-retargeting.md) <br>
- [Campaign Creation, KPIs & Documentation](references/campaign-operations.md) <br>
- [Pre-Campaign Intake Questions](references/intake-questions.md) <br>
- [Safety Guardrails](references/safety-guardrails.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, configuration] <br>
**Output Format:** [Markdown guidance with MCP tool names, checklists, campaign structures, and documentation templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational recommendations and paused-by-default campaign creation steps; it does not independently activate campaigns without approval.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
