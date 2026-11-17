## Description:

Trade prediction markets on Polymarket by searching markets, placing orders, and managing positions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rachelbastian](https://clawhub.ai/user/rachelbastian)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to connect an agent to LuckyLobster's Polymarket trading API for market search, wallet and position review, order placement, cancellation, closing, and redemption workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give agents broad real-money trading authority over a funded account.

Mitigation: Use a dedicated low-balance account or constrained budget, and require explicit confirmation or dry runs before placing orders, approving tokens, closing positions, or redeeming funds.

Risk: The skill instructs users to persist a live trading API key in local configuration or environment files.

Mitigation: Prefer a protected secret store, avoid workspace .env storage for live keys, and revoke and rotate the LuckyLobster key immediately if it is exposed.

## Reference(s):

- [LuckyLobster homepage](https://luckylobster.io)
- [Lucky Lobster ClawHub listing](https://clawhub.ai/rachelbastian/skills/lucky-lobster)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance]

**Output Format:** [Markdown guidance with HTTP, JSON, JavaScript, and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses LUCKYLOBSTER_API_KEY for authenticated API requests.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
