## Description:

Manage treasury balances, payment drafts, approvals, x402 purchases, Polymarket positions, and Pump.fun trades through the Moltbank CLI with strict per-session credential isolation and per-agent OAuth scope consent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[capuzr](https://clawhub.ai/user/capuzr)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and finance teams use this skill to guide agents through Moltbank CLI workflows for treasury reads, payment drafting, x402 purchases, trading-related actions, and approval handling. It is intended for sessions where a human operator can approve credential selection, scope consent, installation, and mutating financial actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide high-impact financial actions, including payment drafts, x402 purchases, Polymarket orders, and Pump.fun trades.

Mitigation: Use it only with a Moltbank account and agent profile intended for these permissions, and require explicit approval in the current chat before any mutating financial action.

Risk: Browser approval and consent URLs could be misused if an operator follows an unverified origin.

Mitigation: Show or follow only URLs whose origin is verified as app.moltbank.bot, and treat missing or mismatched consent URLs as ordinary errors.

Risk: Credential confusion across concurrent agents could expose the wrong account or permissions.

Mitigation: Select an agent profile at session start, fix MOLTBANK_CREDENTIALS_PATH for the session, and switch profiles only after explicit user instruction.

Risk: Setup and update flows can install software on the user's machine.

Mitigation: Run only the approved install or update commands after explicit user approval, and prefer pinned or otherwise verified installation where the runtime supports it.

## Reference(s):

- [Moltbank homepage](https://app.moltbank.bot)
- [ClawHub skill page](https://clawhub.ai/capuzr/skills/moltbank)
- [Publisher profile](https://clawhub.ai/user/capuzr)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON]

**Output Format:** [Markdown guidance with CLI commands and JSON-oriented command output expectations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the local moltbank CLI, explicit user approval for setup and mutating financial actions, and a fixed MOLTBANK_CREDENTIALS_PATH for each session.]

## Skill Version(s):

0.1.11 (source: frontmatter, skill.json, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
