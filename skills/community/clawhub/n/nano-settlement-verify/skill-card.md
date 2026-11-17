## Description:

Checks whether a Nano (XNO) payment to the expected account for the expected raw amount has been confirmed before fulfilling a paid request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dhyabi2](https://clawhub.ai/user/dhyabi2)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and sellers accepting Nano payments use this read-only check to verify a buyer's block hash, quoted amount, and recipient account before delivering a paid service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The selected Nano RPC endpoint receives the block hash, expected amount, and account.

Mitigation: Choose a trusted HTTPS RPC endpoint before checking payments.

Risk: A public block hash can be presented again for another order.

Mitigation: Record served block hashes and reject reuse, or quote a unique amount per order.

Risk: An unconfirmed block or unreachable node does not prove settlement.

Mitigation: Wait and retry verification; fulfill only after a confirmed matching verdict.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/dhyabi2/skills/nano-settlement-verify)
- [Default Nano RPC endpoint](https://rpc.nano.to)

## Skill Output:

**Output Type(s):** [Text]

**Output Format:** [JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [One verdict with an exit code distinguishing confirmed payment, pending confirmation, mismatch or missing block, and unreachable node.]

## Skill Version(s):

1.0.0 (source: ClawHub release and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
