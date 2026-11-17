## Description:

Python SDK for Binance Smart Chain that helps agents create AI-generated meme tokens and perform experimental token buy and sell operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[moonnfunofficial](https://clawhub.ai/user/moonnfunofficial)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to create meme tokens on BSC by combining AI image generation, MoonnFun platform metadata, and blockchain transaction workflows. It can also guide balance checks and experimental token trading operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SDK operations can spend wallet funds through BSC token creation and trading transactions.

Mitigation: Review the code before installation, use a dedicated low-balance wallet, and never use a main wallet private key.

Risk: The default image generation endpoint uses HTTP, which is unsuitable for sensitive prompts or metadata.

Mitigation: Configure an HTTPS image API endpoint or use a self-hosted service before sending sensitive prompts.

Risk: Buy and sell quote failures can remove slippage protection by falling back to zero minimum received.

Mitigation: Treat trading methods as high risk, avoid low-liquidity trades, and manually review transaction parameters before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/moonnfunofficial/skills/moonfunsdk)
- [Artifact README](artifact/README.md)
- [Python SDK README](artifact/python/README.md)
- [Security guide](artifact/python/SECURITY.md)
- [Changelog](artifact/python/CHANGELOG.md)
- [MoonnFun platform](https://moonn.fun)
- [BSC explorer](https://bscscan.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python and shell code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include wallet, RPC, platform, and image API configuration details for BSC token workflows.]

## Skill Version(s):

1.0.6 (source: server release metadata, package __version__, setup.py, CHANGELOG)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
