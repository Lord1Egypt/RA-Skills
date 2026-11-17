## Description:

MCP server for the DRAIN payment protocol. Agents discover service providers, open USDC payment channels on Polygon, and call services such as LLM, scraping, image generation, VPN, and more.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kimbo128](https://clawhub.ai/user/kimbo128)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to discover DRAIN-compatible service providers, open Polygon USDC payment channels, send paid service requests, and reclaim unspent channel funds when work is complete.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires a funded wallet private key in the local MCP environment.

Mitigation: Use only a dedicated low-value wallet for this skill and never reuse a main wallet or high-value key.

Risk: The documented install command uses an unpinned global drain-mcp package.

Mitigation: Verify the package and source before installation, and prefer a pinned reviewed version for repeatable deployments.

Risk: The local MCP process can sign transactions and paid requests with the configured wallet key.

Mitigation: Confirm payment actions before use, keep channel deposits small, monitor channel balances, and close channels promptly when work is complete.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/kimbo128/skills/hs58)
- [Handshake58 Website](https://handshake58.com)
- [DRAIN Repository](https://github.com/kimbo128/DRAIN)
- [drain-mcp npm Package](https://www.npmjs.com/package/drain-mcp)
- [Provider Directory](https://handshake58.com/directory)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, JSON, and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js >= 18, internet access, drain-mcp, and a locally configured DRAIN_PRIVATE_KEY.]

## Skill Version(s):

4.0.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
