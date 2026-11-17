## Description:

Guides agents through discovering Penny Press writing, accessing paid machine-readable editions, and using its Lexicon, quotation collection, and literary witness service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[con-scribe](https://clawhub.ai/user/con-scribe)

### License/Terms of Use:

MIT-0

## Use Case:

External readers and developers use this skill to find Penny Press essays and collections, retrieve paid machine-readable content, and request or verify literary attestations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Machine access to full content or attestations may incur USDC charges.

Mitigation: Check the current price, network, and recipient against the 402 payment instructions before signing.

Risk: Payment workflows can expose wallet credentials if untrusted tooling requests them.

Mitigation: Use only your own trusted wallet tooling; never provide private keys or seed phrases.

## Reference(s):

- [Penny Press](https://www.pennypress.org)
- [Penny Press MCP server](https://www.pennypress.org/mcp)
- [Penny Press payment details](https://www.pennypress.org/.well-known/x402)
- [Penny Press on ClawHub](https://clawhub.ai/con-scribe/skills/penny-press)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Text or Markdown guidance; retrieved content may be JSON or audio]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Machine access to full content and attestations may require USDC payment on Base.]

## Skill Version(s):

1.1.1 (source: frontmatter and ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
