## Description:

Closes empty Solana SPL token accounts to reclaim rent SOL, tracks Ghost Point earnings, claims SOUL rewards, manages encrypted local wallets, and reports lifetime and epoch stats through gp-cli.

This skill is ready for commercial/non-commercial use.

## Publisher:

[graveyardprotocol](https://clawhub.ai/user/graveyardprotocol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to install and operate gp-cli for Solana wallet maintenance: adding or removing local wallets, closing empty SPL token accounts, reclaiming rent SOL, checking Ghost Point statistics, and claiming SOUL rewards.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The wallet-capable CLI can auto-confirm blockchain actions across saved wallets when --all or --yes is used.

Mitigation: Prefer dry-run first and avoid --all or --yes unless the wallet, accounts, reclaimed SOL, protocol fee, and claim details have already been reviewed.

Risk: Installing a mutable global npm package can change behavior across runs.

Mitigation: Install a pinned gp-cli version in a constrained environment before running wallet-affecting commands.

## Reference(s):

- [Graveyard Protocol CLI source repository](https://github.com/graveyardprotocol/gp-cli)
- [Graveyard Protocol CLI ClawHub page](https://clawhub.ai/graveyardprotocol/skills/gp-cli-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with shell command examples and JSON output examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands support JSON mode; close-empty with --all can emit newline-delimited JSON per wallet.]

## Skill Version(s):

1.2.2 (source: server release, target metadata, and skill metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
