## Description:

Claims a specified amount of a Huawei Cloud BSS coupon for an enterprise sub-account and can display the resulting coupon inventory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Huawei Cloud enterprise account administrators use this skill to claim a transferable BSS coupon for a sub-account and review the resulting coupon inventory.

### Deployment Geography for Use:

Global (Huawei Cloud BSS is documented as a global service)

## Known Risks and Mitigations:

Risk: Coupon-transfer safeguards are incomplete, so a live claim may not be adequately restricted.

Mitigation: Do not rely on the advertised restrictions until they are enforced in both execution paths; review the --dry-run request and use credentials limited to verified claim and list permissions before confirming a live claim.

Risk: A ledger in a shared directory can expose other files to overwriting.

Mitigation: Use a ledger directory only you can modify and secure temporary-file creation before relying on the ledger safeguards.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/wlc-dev/skills/huawei-cloud-voucher-claim)
- [IAM policies](references/iam-policies.md)
- [CLI installation guide](references/cli-installation-guide.md)
- [Verification method](references/verification-method.md)
- [Acceptance criteria](references/acceptance-criteria.md)
- [Data flow diagram](references/dataflow-diagram.md)

## Skill Output:

**Output Type(s):** [Shell commands, Text, JSON]

**Output Format:** [Console text or JSON]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [A live claim requires explicit --confirm; --dry-run previews the request.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
