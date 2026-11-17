## Description:

Issues new Huawei Cloud BSS vouchers to sub-customer or partner accounts through KooCLI, with an SDK fallback when KooCLI is unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wlc-dev](https://clawhub.ai/user/wlc-dev)

### License/Terms of Use:

MIT-0

## Use Case:

Cloud developers and operations teams use this skill to issue vouchers to Huawei Cloud partner or sub-customer accounts, including batch issuance. They can preview the request and review per-customer outcomes.

### Deployment Geography for Use:

Global (Huawei Cloud BSS is a global service; the default region is cn-north-1).

## Known Risks and Mitigations:

Risk: Voucher issuance grants financial benefits and may be irreversible; weaknesses in safeguards could cause unintended or duplicate issuance.

Mitigation: Use narrowly scoped credentials, preview each batch, require user approval, keep the ledger in a private directory, avoid concurrent runs, and reconcile uncertain outcomes with Huawei before retrying.

Risk: Operation validation and duplicate protection need strengthening for this write action.

Mitigation: Confirm the intended issue operation and target details before execution, and verify ambiguous results with Huawei rather than retrying blindly.

## Reference(s):

- [KooCLI installation and credential guide](references/cli-installation-guide.md)
- [IAM policies](references/iam-policies.md)
- [Verification method and limits](references/verification-method.md)
- [Data flow diagram](references/dataflow-diagram.md)
- [Acceptance criteria](references/acceptance-criteria.md)

## Skill Output:

**Output Type(s):** [Text, JSON, Guidance]

**Output Format:** [Human-readable issuance summary or JSON result, plus an optional request preview.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports batch targets and reports per-customer successes and errors; live issuance requires --confirm and can be previewed with --dry-run.]

## Skill Version(s):

1.0.6 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
