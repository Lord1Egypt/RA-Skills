## Description:

Read and change Pinterest Ads campaigns, ad groups, ads, and reports through the AdKit MCP connector, with changes saved as drafts for user approval before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeannen](https://clawhub.ai/user/jeannen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect Pinterest ad accounts, inspect campaign performance, and prepare campaign, ad group, and ad changes for review and approval.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects to a Pinterest Ads account and can prepare campaign changes through the Pinterest API.

Mitigation: Review the proposed draft and its changes before publishing; publish only after the user approves.

## Reference(s):

- [AdKit Pinterest Ads setup and usage guide](https://adkit.so/features/ads-mcp/pinterest)
- [Pinterest API v5 reference](https://developers.pinterest.com/docs/api/v5/)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Structured API request payloads and concise text summaries or reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read requests return results directly; write requests are staged as drafts for user approval before publishing.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
