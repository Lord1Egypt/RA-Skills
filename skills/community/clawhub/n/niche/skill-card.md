## Description:

Trading card marketplace with partial USDC deposits. Browse cards, deposit partial amounts, and complete purchases with secure on-chain escrow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[clementsutjiatma](https://clawhub.ai/user/clementsutjiatma)

### License/Terms of Use:


## Use Case:

External users and agents use this skill to browse trading-card listings, manage watches, and initiate or complete partial USDC escrow purchase flows through the Niche CLI and hosted browser pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may register a recurring background command that runs `niche check-matches` every 15 minutes.

Mitigation: Confirm the cron registration before installing and document how to disable the watch check when it is not wanted.

Risk: The recurring watch command uses an external CLI associated with local auth and wallet state.

Mitigation: Verify what `niche check-matches` can read from `~/.niche/auth.json` and confirm that watch-check credentials cannot authorize deposits, payments, wallet operations, or escrow actions.

Risk: Deposit, confirmation, payment, dispute, and wallet actions affect escrow or wallet state.

Mitigation: Require explicit user confirmation before running commands that place deposits, complete payments, cancel deposits, file disputes, fund wallets, or open signing flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/clementsutjiatma/skills/niche)
- [Hosted Niche UI](https://niche-ddq89ltdk-clement-sutjiatmas-projects.vercel.app)
- [Circle faucet for Base Sepolia USDC](https://faucet.circle.com)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, Guidance]

**Output Format:** [Markdown with inline shell commands and user-facing transaction guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May open hosted browser pages for login, browsing, deposits, confirmations, funding, and card details.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
