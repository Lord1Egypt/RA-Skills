## Description:

Claims Gougoubi winner, governance, and LP rewards for one or more addresses through a one-click reward-claiming workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and crypto operators use this skill to claim available Gougoubi reward classes for one or more wallet addresses. It is best suited for fast profile-style or quick reward collection when the user wants claim status and transaction hashes summarized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill supports real crypto reward claiming and may trigger transactions with gas, signer, recipient, calldata, or contract-address effects.

Mitigation: Before any non-dry-run claim, inspect the actual script source and verify the network, contract addresses, signer, gas, recipients, and calldata.

Risk: The skill relies on unbundled local project scripts, so the behavior depends on separately installed code.

Mitigation: Install only when the separate Gougoubi project scripts are trusted, verify they come from the intended repository or release, and run with a least-privilege wallet or environment with no unrelated secrets exposed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/chinasong/skills/gougoubi-claim-all-rewards)
- [Gougoubi website](https://gougoubi.ai)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Guidance]

**Output Format:** [Structured JSON with command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns per-address claim status, transaction hashes, warnings, and retryable failure details when available.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
