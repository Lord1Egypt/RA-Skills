## Description:

Enables agents to use Krump Verify for on-chain dance-move verification against Story IP, including USDC.k and x402/EVVM payment flows on Story Aeneid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arunnadarasa](https://clawhub.ai/user/arunnadarasa)

### License/Terms of Use:


## Use Case:

External users, developers, and agents use this skill to verify dance moves against registered Story IP assets, pay with USDC.k or x402/EVVM receipts, and call the KrumpVerify contract surface.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users or agents may approve payments, deposits, or contract calls against incorrect contract or relayer addresses.

Mitigation: Verify contract and relayer addresses independently before approving USDC.k, depositing funds, or submitting transactions.

Risk: Wallets with broad signing authority or excess funds can increase loss exposure during autonomous payment flows.

Mitigation: Use narrowly funded wallets and grant only the signing authority needed for the intended verification flow.

Risk: The verification fee may differ from documented defaults.

Mitigation: Read the live verificationFee() value and confirm the amount before approval, deposit, or receipt use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/arunnadarasa/skills/krumpverify)
- [ClawHub](https://clawhub.ai/)
- [Story Aeneid explorer](https://aeneid.storyscan.io)
- [Story Aeneid RPC](https://aeneid.storyrpc.io)
- [Krump x402 relayer](https://krump-x402-relayer.fly.dev)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with contract calls, addresses, command examples, and configuration values]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces informational guidance only; no executable code is bundled in the skill artifact.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
