## Description:

Read HoneyBook client-portal data from a shell with fpx and direct API requests after capturing a vendor session from a signed-in browser tab, without running the honeybook-mcp server.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and HoneyBook clients with an active vendor portal session can use shell commands to read shared files, workspace details, payment methods, and related client-portal data without the HoneyBook MCP server.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Captured session credentials and HoneyBook responses can expose sensitive client data when stored in temporary files.

Mitigation: Keep session values in shell variables where possible, restrict access to temporary files, and remove them after use.

Risk: The instructions include a message-sending flow that can email a vendor, despite the skill being described as read-focused.

Mitigation: Use read requests unless sending is intended; before any send operation, verify the vendor, subject, and message content.

Risk: The security assessment reports incomplete scan coverage because some referenced paths were missing.

Mitigation: Review the full skill contents and its referenced paths before use, with particular attention to session handling and message sending.

## Reference(s):

- [HoneyBook requests for fpx + curl](artifact/references/requests.md)
- [ContextMint Bridge releases](https://github.com/nullnet-app/contextmint-bridge/releases)
- [ContextMint Bridge project](https://github.com/nullnet-app/contextmint-bridge)
- [Fetchproxy extension details](https://github.com/chrischall/fetchproxy#extension)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with shell commands, curl examples, and jq expressions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes portal-session setup and read-request examples; also documents an optional message-sending flow.]

## Skill Version(s):

1.4.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
