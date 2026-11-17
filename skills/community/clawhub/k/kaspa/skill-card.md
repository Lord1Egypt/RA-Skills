## Description:

Simple self-custody CLI wallet for Kaspa that lets agents check balances, send KAS, generate payment URIs, estimate fees, and query network status.

This skill is ready for commercial/non-commercial use.

## Publisher:

[manyfestation](https://clawhub.ai/user/manyfestation)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users can use this skill to automate Kaspa wallet operations from an agent workflow, including balance checks, fee estimates, payment URI generation, mnemonic generation, and KAS transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real wallet secrets such as private keys and mnemonics.

Mitigation: Use testnet first, avoid putting real keys or mnemonics in normal shell history or shared automation logs, and keep credentials in protected environment handling.

Risk: The skill can broadcast irreversible Kaspa transactions.

Mitigation: Require out-of-band human confirmation of the destination address, amount, network, and fees before allowing an agent to run send commands.

Risk: The release has under-scoped dependency and install safeguards.

Mitigation: Inspect and pin the kaspa dependency before installation, and run the wallet in an isolated environment.

## Reference(s):

- [Kaspa Docs](https://docs.kaspa.org/)
- [Kaspa Explorer](https://explorer.kaspa.org/)
- [kaspa-py SDK](https://github.com/aspect-build/kaspa-py)
- [ClawHub Skill Page](https://clawhub.ai/manyfestation/skills/kaspa)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses environment variables for wallet credentials and network selection; transaction workflows should include human confirmation.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
