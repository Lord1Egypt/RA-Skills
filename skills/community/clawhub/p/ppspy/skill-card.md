## Description: <br>
Search and analyze Shopify stores, Facebook ads, ad monitoring, and sales tracking using the PPSPY e-commerce intelligence API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fanyanggod](https://clawhub.ai/user/fanyanggod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers, operators, and e-commerce analysts use this skill to query PPSPY for Shopify store intelligence, Facebook ad research, ad monitoring, and sales monitoring. It requires a PPSPY API key and may consume account credits or monitoring quota. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Queries are sent to the PPSPY service and may expose submitted store, advertiser, product, or monitoring targets. <br>
Mitigation: Use the skill only with PPSPY data sharing that is acceptable for the account and organization. <br>
Risk: API calls can consume PPSPY credits or monitoring quota. <br>
Mitigation: Monitor credit and quota usage before running broad searches or creating monitoring tasks. <br>
Risk: Monitoring tools can create, stop, or delete ad and sales monitoring groups or tasks. <br>
Mitigation: Require explicit user confirmation before mutating monitoring groups or tasks. <br>
Risk: The integration depends on a third-party npm package and a PPSPY API key. <br>
Mitigation: Install only trusted package versions and use a rotatable API key with usage monitoring. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fanyanggod/ppspy) <br>
- [PPSPY homepage](https://www.ppspy.com) <br>
- [PPSPY API site](https://api.ppspy.com/) <br>


## Skill Output: <br>
**Output Type(s):** [API calls, Analysis, Guidance, Configuration] <br>
**Output Format:** [Markdown and structured tool results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses PPSPY_API_KEY and the ppspy-mcp-server npm package; API calls may consume PPSPY credits or monitoring quota.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
