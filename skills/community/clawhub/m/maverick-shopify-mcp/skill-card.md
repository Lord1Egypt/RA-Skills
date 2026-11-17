## Description:

Search, read, and work with Shopify products, orders, customers, and shop data through a local MCP wrapper.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

External Shopify merchants and store operators use this skill to inspect shop data and manage products, orders, customers, and other Shopify data through the connected store.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The unrestricted admin tool permits destructive store changes beyond the dedicated product tools.

Mitigation: Use a read-only Shopify token for exploration. Before enabling writes, restrict or disable the generic admin tool and require explicit approval for each proposed change, especially deletion. Verify the configured shop hostname before supplying the token.

## Reference(s):

- [Shopify skill release on ClawHub](https://clawhub.ai/maverick/skills/maverick-shopify-mcp)
- [mcporter project](https://github.com/openclaw/mcporter)
- [uv documentation](https://docs.astral.sh/uv/)

## Skill Output:

**Output Type(s):** [JSON, Text]

**Output Format:** [Structured JSON from Shopify tools, with optional natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results reflect the connected Shopify store and token permissions.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
