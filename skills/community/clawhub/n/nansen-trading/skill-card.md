## Description:

Execute DEX swaps on Solana, Base, Ethereum, Arbitrum, Polygon or Robinhood Chain (including cross-chain bridges) and Hyperliquid perpetual trades. Use when buying or selling a token, getting a swap quote, executing a trade, or opening/closing/managing a perp position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and trading agents use this skill to request quotes and execute or manage DEX swaps, cross-chain bridges, and Hyperliquid perpetual trades through the Nansen CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wallet password may be stored in a local plaintext file, exposing signing credentials if that file or host is compromised.

Mitigation: Prefer a secure credential store or runtime entry; avoid saving the password in plaintext.

Risk: Trade and perpetual order commands can sign and submit irreversible transactions, and non-interactive runs proceed without a confirmation prompt by default.

Mitigation: Review the proposed transaction with --dry-run and require explicit approval before submitting; use NANSEN_REQUIRE_CONFIRM=1 when non-interactive confirmation is needed.

## Reference(s):

- [Nansen Trading skill release](https://clawhub.ai/nansen-devops/skills/nansen-trading)
- [Nansen CLI package on npm](https://www.npmjs.com/package/nansen-cli)
- [Nansen CLI project](https://github.com/nansen-ai/nansen-cli)
- [Browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance, Configuration instructions]

**Output Format:** [Markdown with inline shell commands and trading instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may initiate signed, irreversible trades; dry-run previews are available.]

## Skill Version(s):

0.1.14 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
