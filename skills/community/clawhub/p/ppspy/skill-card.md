## Description:

Search and analyze Shopify stores, Facebook ads, ad monitoring, and sales tracking using PPSPY e-commerce intelligence API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[fanyanggod](https://clawhub.ai/user/fanyanggod)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and e-commerce operators use this skill to search Shopify stores and products, inspect Facebook ads, monitor ad campaigns, and track sales through PPSPY. It helps agents answer market research and competitor intelligence questions and create or manage PPSPY monitoring tasks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: PPSPY API calls and monitoring tasks can consume paid credits or quota.

Mitigation: Use a revocable PPSPY API key with spending or quota limits, and review calls that request records or create monitoring tasks before execution.

Risk: Create, edit, delete, stop, or cancel actions can change the user's PPSPY account state.

Mitigation: Require explicit approval before account-changing monitoring actions.

Risk: The skill depends on a globally installed ppspy-mcp-server npm package.

Mitigation: Install only when PPSPY and the npm package are trusted, and avoid installing or running it with administrator privileges.

## Reference(s):

- [PPSPY Homepage](https://www.ppspy.com)
- [PPSPY API Account Portal](https://api.ppspy.com/)
- [ClawHub Skill Page](https://clawhub.ai/fanyanggod/skills/ppspy)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with setup commands and PPSPY result summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Shopify store, product, advertisement, ad monitoring, and sales monitoring results from PPSPY; account actions can consume credits or quota.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
