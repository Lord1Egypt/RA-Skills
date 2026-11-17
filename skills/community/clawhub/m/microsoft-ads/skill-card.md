## Description:

Read and change Microsoft Advertising (Bing Ads) campaigns from an AI agent through the AdKit MCP connector, using the official Microsoft Advertising API v13. Every change is saved as a draft that the user approves before it goes live. Use when the user wants to run, change, or check Microsoft or Bing ads. Not for Microsoft Ads strategy or ad copy advice.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeannen](https://clawhub.ai/user/jeannen)

### License/Terms of Use:

MIT-0

## Use Case:

Advertisers and marketing operations teams use this skill to connect an AdKit project to Microsoft Advertising, inspect campaign data and reports, and prepare campaign, ad group, ad, or keyword changes for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment was benign with medium confidence, but one local path-like reference could not be resolved, leaving some evidence incomplete.

Mitigation: Consider this scan limitation when deciding whether to install.

Risk: Changes to campaigns, ad groups, ads, or keywords can affect live advertising once published.

Mitigation: Review the saved draft and publish only after the user approves the proposed changes.

## Reference(s):

- [AdKit Microsoft Ads connector guide](https://adkit.so/features/ads-mcp/microsoft)
- [Microsoft Advertising API documentation](https://learn.microsoft.com/advertising)

## Skill Output:

**Output Type(s):** [API calls, JSON, Guidance]

**Output Format:** [Markdown guidance with JSON API request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read requests run immediately; write requests are saved as drafts for user review and require approval before publishing.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
