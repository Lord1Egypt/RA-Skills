## Description:

Execute DEX swaps on Solana or Base (including cross-chain bridges) and Hyperliquid perpetual trades. Use when buying or selling a token, getting a swap quote, executing a trade, or opening/closing/managing a perp position.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nansen-devops](https://clawhub.ai/user/nansen-devops)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and traders use this skill to quote and manage token swaps, cross-chain bridges, Solana limit orders, and Hyperliquid perpetual positions through the Nansen CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On-chain swaps and perpetual orders are irreversible after signing or broadcast, and non-interactive execution may proceed without a prompt.

Mitigation: Inspect the command's --dry-run plan before execution. Set NANSEN_REQUIRE_CONFIRM=1 when each broadcast must wait for explicit approval, and use --yes only when skipping confirmation is intended.

Risk: The wallet password protects the ability to sign trades.

Mitigation: Keep NANSEN_WALLET_PASSWORD in protected storage and out of prompts, logs, and session memory.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nansen-devops/skills/nansen-trading)
- [Nansen CLI package on npm](https://www.npmjs.com/package/nansen-cli)
- [Nansen browser login platform scope](https://github.com/nansen-ai/nansen-cli/blob/main/docs/browser-login.md#preview-platform-scope)

## Skill Output:

**Output Type(s):** [Shell commands, Guidance]

**Output Format:** [Markdown with inline shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include trade quotes, execution results, and position or account status.]

## Skill Version(s):

0.1.13 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
