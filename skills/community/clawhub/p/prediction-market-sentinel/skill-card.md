## Description:

Monitor Polymarket prediction market wallets and detect new trades in real time for wallet tracking, new-position detection, and prediction-market activity monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dagangtj](https://clawhub.ai/user/dagangtj)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor Polymarket wallet activity and receive guidance for detecting new or changed orders. Review is needed before relying on it for arbitrary wallet monitoring because the security evidence says the included script tracks a fixed wallet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence says the monitor ignores the requested wallet address and tracks a hardcoded Polymarket wallet.

Mitigation: Correct and review wallet-parameter handling before using the skill for arbitrary wallet monitoring.

Risk: The monitor writes local log and state files under the user's workspace.

Mitigation: Document and approve the required file permissions, and inspect the configured paths before execution.

Risk: The monitor sends requests to Polymarket's CLOB API.

Mitigation: Approve network egress to the Polymarket endpoint and review what wallet data is sent before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dagangtj/skills/prediction-market-sentinel)
- [Polymarket CLOB orders endpoint](https://clob.polymarket.com/orders?maker=$WALLET_ADDRESS&limit=1)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline bash commands and plain-text monitoring notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local log and state files used by the bundled monitor script.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
