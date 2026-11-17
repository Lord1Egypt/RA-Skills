## Description:

Media ownership and payment infrastructure over MCP. Publish a video to TikTok, Instagram, YouTube, Facebook, LinkedIn, Vimeo, Vimeo OTT, Mux and Farcaster in one launch, get an on-chain ownership record when it goes out, and search or buy media metadata per use over x402 or MPP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aquaflans](https://clawhub.ai/user/aquaflans)

### License/Terms of Use:

MIT

## Use Case:

Creators and teams use JubJub through an agent to publish and manage media across connected platforms, track ownership and performance, collaborate on content, and search or purchase catalogue items.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill connects an agent to the external JubJub service using an API key or OAuth access.

Mitigation: Use credentials only for the intended account, store API keys securely, and connect only if you trust the service.

Risk: Publishing, destructive, external-facing, paid, and on-chain actions can affect public content, relationships, or funds.

Mitigation: Review the exact target, visibility, schedule, and quoted price where relevant, and confirm each high-impact action before it is performed.

## Reference(s):

- [JubJub MCP endpoint](https://api.jubjubapp.com/v2/mcp)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, Configuration instructions]

**Output Format:** [Natural language responses and structured MCP tool requests/results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate publishing, account changes, or paid catalogue and on-chain actions after user confirmation.]

## Skill Version(s):

1.3.0 (source: server-resolved release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
