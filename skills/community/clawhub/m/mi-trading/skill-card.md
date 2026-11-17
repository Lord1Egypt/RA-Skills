## Description:

Trade tokens on Solana using the ClawDex CLI when the user asks to swap tokens, check balances, get quotes, or manage a Solana trading wallet.

This skill is ready for commercial/non-commercial use.

## Publisher:

[davidpolotm](https://clawhub.ai/user/davidpolotm)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to operate a Solana trading wallet through ClawDex, including balance checks, swap quotes, simulations, real swaps, and post-trade verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to install an unpinned global trading CLI.

Mitigation: Pin and verify the ClawDex CLI before use, and avoid relying on an arbitrary PATH executable.

Risk: The skill can execute real wallet swaps.

Mitigation: Use only a dedicated low-value wallet, set conservative guardrails first, simulate trades before execution, and require explicit approval for every real swap after showing the final trade terms.

## Reference(s):

- [Mi Trading on ClawHub](https://clawhub.ai/davidpolotm/skills/mi-trading)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline bash commands and JSON-oriented CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires machine-parseable JSON CLI output for trading checks, simulations, and swaps.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
