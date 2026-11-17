## Description:

Submit real-world outcomes for Gougoubi conditions using deterministic evidence from condition skills and public market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and prediction-market operators use this skill to map public market evidence to Gougoubi condition outcomes and submit one result per eligible condition. It supports resolved-only settlement, full proposal submission when outcomes are clear, and explicit forced fallback submission for pending conditions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Blockchain submissions may be irreversible and high impact if proposal, chain, signer, or condition results are wrong.

Mitigation: Require manual confirmation of chain, signer, proposal, condition results, calldata, fees, and dry-run output before any real submission.

Risk: The skill references unbundled relative project scripts for result submission.

Mitigation: Use only in a controlled repository where the referenced scripts are known, reviewed, and pinned.

Risk: Forced fallback submission can submit outcomes for pending conditions.

Mitigation: Prefer resolved-only mode and use force mode only when explicitly requested by the user.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/chinasong/skills/gougoubi-submit-real-results)
- [Gougoubi Website](https://gougoubi.ai)
- [Gougoubi Repository](https://github.com/gougoubi/gougoubi)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON with submitted, skipped, failed, warning, and transaction-hash fields, with shell commands when invoking project scripts is appropriate.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Result submission should preserve evidence mapping with transaction outcomes and avoid duplicate submissions for conditions that already have results.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
