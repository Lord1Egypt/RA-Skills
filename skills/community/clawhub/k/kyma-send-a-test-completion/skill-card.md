## Description:

Run one real, billed chat completion through Kyma API with the user's explicit approval and report back the output and what it cost.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyma-api](https://clawhub.ai/user/kyma-api)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to run a single approved Kyma API model smoke test, verify that a model answers, or compare two models on the same prompt while seeing cost and remaining budget.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can trigger real billed Kyma API test completions.

Mitigation: Ask for fresh explicit approval before each call and state the exact model, prompt, estimated cost, and remaining budget before execution.

Risk: A friendly model name or alias could lead to billing a different model than intended.

Mitigation: Confirm the resolved model id before requesting approval and making the call.

Risk: Automatic retries or extra comparison calls could add unexpected charges.

Mitigation: Treat each retry or additional model as a separate call that requires a new approval.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kyma-api/skills/kyma-send-a-test-completion)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown summary with the model reply, actual cost, latency when comparing models, and remaining budget.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires fresh explicit approval for each billed completion and uses small max token limits for smoke tests.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
