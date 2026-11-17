## Description:

Glin Profanity MCP provides profanity detection tools for AI assistants reviewing user content, moderation reports, and pre-publishing validation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thegdsks](https://clawhub.ai/user/thegdsks)

### License/Terms of Use:


## Use Case:

Developers and content moderation teams use this skill to add profanity detection and content review tools to AI assistant workflows for batch checks, audit reports, pre-publishing validation, and human-in-the-loop moderation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installation guidance asks users to run a mutable npm MCP server.

Mitigation: Review the npm package and pin a specific trusted version before installing.

Risk: User tracking features can create user-level moderation history without clear data-handling guardrails.

Mitigation: Use tracking features only where moderation policy permits storing user-level history, and confirm storage location, access controls, retention, and deletion procedures.

## Reference(s):

- [glin-profanity-mcp npm package](https://www.npmjs.com/package/glin-profanity-mcp)
- [glin-profanity MCP source package](https://github.com/GLINCKER/glin-profanity/tree/release/packages/mcp)
- [glin-profanity core library](https://www.npmjs.com/package/glin-profanity)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Text or Markdown moderation results with optional JSON configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include profanity flags, censored text, safety scores, action recommendations, corpus statistics, regex patterns, and user moderation history when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
