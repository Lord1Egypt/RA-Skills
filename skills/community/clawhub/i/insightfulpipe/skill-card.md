## Description: <br>
Query and manage marketing data across 40+ platforms, including Google Analytics, Google Ads, Facebook Ads, Instagram, Shopify, HubSpot, Klaviyo, TikTok, LinkedIn, and more. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[insightfulpipe](https://clawhub.ai/user/insightfulpipe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Marketing analysts, operators, and developers use this skill to discover connected accounts, inspect action schemas, query marketing and business platform data, and run confirmed write operations through the InsightfulPipe CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The required token can access connected marketing and business platforms. <br>
Mitigation: Use the least-privileged INSIGHTFULPIPE_TOKEN available and verify the npm package source before installation. <br>
Risk: Write operations can modify connected services when run with insightfulpipe action and --yes. <br>
Mitigation: Require explicit user confirmation before running any write operation. <br>
Risk: Platform actions and request bodies vary, so guessed parameters can produce failed or misleading results. <br>
Mitigation: Run account discovery and helper schema commands before executing queries or actions, and replace all placeholders with real IDs. <br>


## Reference(s): <br>
- [InsightfulPipe homepage](https://insightfulpipe.com) <br>
- [InsightfulPipe npm package](https://www.npmjs.com/package/insightfulpipe) <br>
- [ClawHub skill page](https://clawhub.ai/insightfulpipe/insightfulpipe) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/insightfulpipe) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the insightfulpipe CLI and a pre-configured INSIGHTFULPIPE_TOKEN.] <br>

## Skill Version(s): <br>
0.1.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
