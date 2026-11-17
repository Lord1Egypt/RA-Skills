## Description:

Report the Kyma API account balance, this connection's spend cap, amount spent, remaining budget and reset date, plus recent credit ledger entries, and hand back the top-up link when the balance is low.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyma-api](https://clawhub.ai/user/kyma-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check Kyma API account credits, per-connection spend limits, recent ledger activity, and whether funds or cap remain before running billed Kyma API actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The user may treat a stale or failed billing check as current account state.

Mitigation: Report only live tool results; if a balance or spend check fails, state that the value is unknown rather than estimating it.

Risk: A top-up link could be mistaken for an automatic payment action.

Mitigation: Present the billing-page link for user review and make clear that the user completes any payment themselves.

Risk: A billed action could run before the user sees current budget constraints.

Mitigation: Check balance and remaining cap before billed actions, then ask for explicit go-ahead before continuing.

## Reference(s):

- [Kyma API integrations](https://kymaapi.com/integrations)
- [ClawHub skill page](https://clawhub.ai/kyma-api/skills/kyma-check-spend-and-credits)
- [Publisher profile](https://clawhub.ai/user/kyma-api)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Concise text or Markdown summary with current billing values, ledger notes, and relevant account links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only responses based on current Kyma API account balance, spend-cap, transaction, and top-up-link results.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
