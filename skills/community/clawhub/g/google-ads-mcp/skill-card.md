## Description:

Manage Google Ads campaigns, keywords, and reporting through AdKit, with campaign changes staged for user approval before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jeannen](https://clawhub.ai/user/jeannen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to connect AdKit and manage Google Ads campaigns, keywords, conversion actions, and performance reports through an AI agent.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Offline conversion uploads take effect immediately and may not use the draft review flow.

Mitigation: Run the upload with validateOnly: true first, review the upload carefully, and get the user's explicit confirmation before submitting it.

## Reference(s):

- [AdKit Google Ads MCP guide](https://adkit.so/features/ads-mcp/google)
- [Google Ads API reference](https://developers.google.com/google-ads/api/reference/rpc)
- [ClawHub release page](https://clawhub.ai/jeannen/skills/google-ads-mcp)

## Skill Output:

**Output Type(s):** [API Calls, Guidance, Configuration instructions, Shell commands]

**Output Format:** [MCP tool calls and concise text or Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Campaign changes are staged for review before publishing; offline conversion uploads run immediately.]

## Skill Version(s):

1.0.0 (source: evidence.json release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
