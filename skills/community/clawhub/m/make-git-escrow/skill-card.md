## Description:

Create a git escrow bounty for a failing test suite by guiding parameter collection and running the git-escrows submit command.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mlegls](https://clawhub.ai/user/mlegls)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and maintainers use this skill to create escrowed token rewards for test-suite challenges, including checking CLI and wallet configuration, collecting repository and contract parameters, submitting the escrow, and reporting fulfillment instructions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lock ERC20 tokens using a wallet private key.

Mitigation: Use only a dedicated low-value wallet and require final manual confirmation of chain, token, amount, arbiter, oracle, and recipient before any transaction is signed.

Risk: The skill may run unpinned git-escrows package code.

Mitigation: Verify the git-escrows package source and version before installing or executing it.

Risk: A real private key could be exposed through chat, command-line arguments, or shell history.

Mitigation: Keep PRIVATE_KEY in a local .env file and avoid entering a real private key in a command line or chat transcript.

## Reference(s):

- [Project homepage](https://github.com/arkhai-io/git-commit-trading)
- [ClawHub skill page](https://clawhub.ai/mlegls/skills/make-git-escrow)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute git-escrows and git commands after collecting user parameters and verifying .env configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
