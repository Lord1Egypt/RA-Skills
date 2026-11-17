## Description: <br>
Guides agents through go-to-market planning for products, covering positioning, pricing, channel strategy, launch planning, and growth metrics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product teams, founders, marketers, and agents use this skill to draft structured go-to-market plans for SaaS, consumer applications, enterprise products, regional market entry, pricing optimization, and launch campaigns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requests command execution and file-writing capabilities without explaining why those powers are needed for a planning template. <br>
Mitigation: Run it in a constrained workspace and only allow shell commands or file writes after explicit review. <br>
Risk: The skill accepts optional callback URLs and may be used with sensitive business planning data. <br>
Mitigation: Avoid sending confidential product, customer, pricing, or market-entry data to callback URLs unless the endpoint is trusted. <br>
Risk: Go-to-market recommendations can be based on static or public information and may not reflect current market conditions. <br>
Mitigation: Validate positioning, pricing, and channel recommendations with current market research, user interviews, and business review before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/go-to-market-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands, configuration] <br>
**Output Format:** [Markdown text with tables and occasional shell snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include structured GTM strategy sections, positioning statements, pricing options, channel plans, launch timelines, and growth metrics.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
