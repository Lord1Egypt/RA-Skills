## Description:

Upload images to img402.dev and return a public URL for sharing, embedding, posting, or other workflows that need a hosted image link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[img402](https://clawhub.ai/user/img402)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, external users, and agents use this skill to upload local image files and return public CDN URLs for messages, documents, social platforms, or other contexts that require a publicly reachable image.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Uploaded images are public and may be permanent, especially files at or under 1 MB.

Mitigation: Review files before upload and do not upload internal screenshots, personal data, secrets, API keys, regulated data, or other content that should not be public.

Risk: Images over 1 MB may require either temporary retention or a paid x402 flow for permanence.

Mitigation: Confirm the required retention before upload; shrink images below 1 MB for free permanent hosting when appropriate, or use the paid flow only when long-term retention is needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/img402/skills/image-hosting)
- [img402](https://img402.dev)
- [Coinbase Payments MCP](https://docs.cdp.coinbase.com/mcp)
- [Paying x402 APIs](https://img402.dev/blog/paying-x402-apis)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Guidance]

**Output Format:** [Markdown guidance with bash/curl snippets and JSON response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl; upload responses include a public URL, content type, size, and expiresAt retention value.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
