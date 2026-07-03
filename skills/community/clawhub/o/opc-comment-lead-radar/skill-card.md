## Description: <br>
Find Customers · 找客户 helps agents identify sales leads from public Douyin, Xiaohongshu, and Kuaishou comments and turn them into customer lists, follow-up scripts, online reports, and next-search suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanjian068yuan](https://clawhub.ai/user/yuanjian068yuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Merchants, sales teams, and social-media operators use this skill to scan public comment areas for buying intent, prioritize prospects, generate follow-up wording, and review lead outcomes. It is designed for trials, saved customer pools, and follow-up workflows that use the user's own platform access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can add a persistent MCP connector and trigger npx execution in the user's agent host. <br>
Mitigation: Review the MCP configuration before enabling it, approve connector trust prompts deliberately, and install only if the ppxc-leads MCP connector is acceptable in the target environment. <br>
Risk: The connector can use the user's social-platform login state while scanning public comments. <br>
Mitigation: Use only accounts and platform sessions the user is authorized to use, avoid unnecessary scans, and follow platform rules and applicable privacy or marketing laws. <br>
Risk: Lead reports may profile named public commenters and generate outreach suggestions. <br>
Mitigation: Limit collection, storage, and outreach to appropriate business purposes, review suggested leads and messages before contacting anyone, and honor consent, opt-out, and local compliance requirements. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanjian068yuan/skills/opc-comment-lead-radar) <br>
- [OPC MCP setup page](https://opc1.me/download/mcp) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown reports and guidance with links, lead lists, follow-up scripts, MCP setup snippets, and status summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include online report links, customer-pool links, search progress, public comment excerpts, lead IDs, and suggested content angles when returned by the connector.] <br>

## Skill Version(s): <br>
1.0.13 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
