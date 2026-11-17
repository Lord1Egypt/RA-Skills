## Description:

Helps agents identify sales leads from public Douyin, Xiaohongshu, and Kuaishou comments, produce online lead reports, customer-pool links, follow-up scripts, and next-search suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yuanjian068yuan](https://clawhub.ai/user/yuanjian068yuan)

### License/Terms of Use:

MIT-0

## Use Case:

External business users, sales operators, and agents use this skill to scan public social-media comments for buying intent, prioritize likely customers, and draft practical follow-up messages. It is suited to trial scans, saved customer-pool workflows, and review of prior lead-generation results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill relies on a third-party MCP connector and remote workflow guidance that can influence local actions and lead collection.

Mitigation: Install only after reviewing the connector, prefer a pinned version, use project-scoped MCP configuration, and require explicit approval before configuration edits or login actions.

Risk: The workflow may use logged-in social-media sessions and hidden browser windows to collect lead lists from public comments.

Mitigation: Use only accounts and data the user is authorized to access, respect platform login and verification prompts, and review generated customer lists before outreach.

Risk: Lead classification can be inaccurate or too broad, and privacy-sensitive targeting can create additional risk.

Mitigation: Validate leads manually, record user feedback on inaccurate results, and avoid sensitive targeting such as children, family status, or other privacy-sensitive inferences.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/yuanjian068yuan/skills/opc-comment-lead-radar)
- [OPC MCP setup](https://opc1.me/download/mcp)
- [OPC comment lead generation use case](https://opc1.me/use-cases/comment-lead-generation)
- [OPC comment lead radar comparison](https://opc1.me/compare/comment-lead-radar-vs-export-tools)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports with lead lists, report links, customer-pool links, follow-up scripts, and inline setup commands or configuration snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include lead scores, quoted public comments, platform/login status guidance, diagnostics instructions, and next-search suggestions.]

## Skill Version(s):

1.0.22 (source: server release evidence and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
