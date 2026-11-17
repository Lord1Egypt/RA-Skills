## Description:

Manage GoldenClaw (GCLAW) on Solana. Create wallet, claim from faucet, check balance, send tokens, view history. For OpenClaw AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[goldenclaworg](https://clawhub.ai/user/goldenclaworg)

### License/Terms of Use:

MIT

## Use Case:

External OpenClaw users and agents use Golden Claw to create or recover an encrypted Solana wallet, claim GCLAW from the GoldenClaw faucet, inspect balances and history, and send GCLAW or SOL donation transactions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill creates and stores an encrypted crypto wallet and can sign GCLAW or SOL transactions.

Mitigation: Use an isolated OPENCLAW_DATA_DIR, set conservative GCLAW_TX_LIMIT and GCLAW_DAILY_LIMIT values, verify recipient and donation addresses before signing, and avoid meaningful funds until the skill and dependencies are reviewed.

Risk: The skill can auto-install mutable npm dependencies at runtime.

Mitigation: Pin and review dependencies before deployment, then install from a controlled environment rather than relying on runtime installation.

Risk: Wallet recovery accepts a seed phrase through command arguments.

Mitigation: Do not pass a real seed phrase through shell or chat command arguments; use a fresh low-value wallet for testing and handle recovery secrets outside shared logs or transcripts.

Risk: The skill contacts Solana RPC endpoints and goldenclaw.org for balances, history, faucet claims, and transactions.

Mitigation: Run only in environments where those network calls are expected, and review configured endpoints such as SOLANA_RPC_URL and GCLAW_FAUCET_URL before use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/goldenclaworg/skills/goldenclaw)
- [GoldenClaw Website and Faucet](https://goldenclaw.org)
- [GCLAW Token on Solscan](https://solscan.io/token/8fUqKCgQ2PHcYRnce9EPCeMKSaxd14t7323qbXnSJr4z)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text and Markdown command responses with wallet addresses, balances, transaction status, configuration hints, and links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May initiate Solana RPC and faucet API calls and sign GCLAW or SOL transactions when used with wallet credentials.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact SKILL.md and package.json report 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
