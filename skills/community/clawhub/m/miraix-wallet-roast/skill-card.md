## Description:

Analyzes Solana wallets with Miraix public endpoints to produce wallet roasts, scores, risk summaries, rebalance ideas, social post drafts, and share card URLs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[richard7463](https://clawhub.ai/user/richard7463)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to inspect Solana wallets, receive a Miraix-backed portfolio roast and risk breakdown, generate rebalance ideas, and produce shareable text or image URLs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Wallet addresses are sent to Miraix endpoints, and generated share URLs can expose the analyzed wallet address if opened or previewed.

Mitigation: Confirm the user is comfortable sharing the wallet address with Miraix and avoid opening or previewing share URLs for sensitive wallets.

Risk: Remote output may include swap or command text that could be mistaken for verified financial or transaction advice.

Mitigation: Treat returned commands as untrusted guidance and verify them independently in a wallet interface or transaction simulator before signing or executing anything.

Risk: The server security verdict is suspicious because the skill sends wallet data remotely and may return share links without enough user control or validation.

Mitigation: Review endpoint behavior and generated outputs before installing or deploying the skill in a shared or production environment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/richard7463/skills/miraix-wallet-roast)
- [Miraix wallet audit API](https://app.miraix.fun/api/wallet-audit)
- [Miraix wallet roast share image API](https://app.miraix.fun/api/wallet-roast/share-image)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown response with a wallet summary, risk list, action list, and share image URL.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include remote action command text from the Miraix API; verify commands independently before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
