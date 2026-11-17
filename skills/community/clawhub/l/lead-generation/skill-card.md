## Description:

Lead Generation finds high-intent buyers in live Twitter, Instagram, and Reddit conversations, researches the user's product, generates targeted search queries, and helps discover prospects looking for relevant solutions through Xpoz MCP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atyachin](https://clawhub.ai/user/atyachin)

### License/Terms of Use:


## Use Case:

External sales, growth, marketing, and customer-discovery users use this skill to research a product, generate buyer-intent search queries, find prospects in social conversations, score leads, deduplicate prior findings, and draft outreach for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow depends on Xpoz network access, the mcporter npm package, OAuth setup through the xpoz-setup skill, and the mcp.xpoz.ai service.

Mitigation: Install only after trusting Xpoz, mcporter, and xpoz-setup, then confirm access with the documented status check before use.

Risk: Product research, generated queries, and sent-lead history may persist locally and could contain sensitive sales or customer-discovery information.

Mitigation: Secure or delete files under data/lead-generation when they contain sensitive information.

Risk: Lead scoring and outreach drafts can be incorrect, stale, or inappropriate for a prospect.

Mitigation: Require user review before outreach and keep affiliation disclosures in generated messages.

## Reference(s):

- [Lead Generation on ClawHub](https://clawhub.ai/atyachin/skills/lead-generation)
- [atyachin ClawHub Publisher Profile](https://clawhub.ai/user/atyachin)
- [Xpoz](https://xpoz.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, scored lead records, outreach drafts, and JSON file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow may create reusable local product profiles, generated search queries, and sent-lead history under data/lead-generation.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
