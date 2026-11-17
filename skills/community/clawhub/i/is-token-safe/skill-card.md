## Description:

Evaluates a crypto token contract for scam risks and returns a safety level with supporting reasons for trading and agent decision workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dokbawi80](https://clawhub.ai/user/dokbawi80)

### License/Terms of Use:


## Use Case:

Developers and agent builders use this skill to screen token addresses for common scam indicators before using them in trading bots, prediction-market agents, or token discovery pipelines. Its result should be treated as an advisory risk signal rather than a sole safety decision.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may understate token risk or fail open, creating a false sense of safety.

Mitigation: Treat results as advisory, require independent review or additional scanners, and test failure paths before relying on the output.

Risk: Automated trading flows could act on an unreliable safety signal.

Mitigation: Do not allow the skill output alone to authorize trades or token approvals; add policy gates and human or multi-signal confirmation.

Risk: External RPC and honeypot API calls can fail, time out, or return incomplete data.

Mitigation: Handle null results conservatively, monitor provider errors, and verify the intended chain and token address before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dokbawi80/skills/is-token-safe)
- [Publisher profile](https://clawhub.ai/user/dokbawi80)
- [Honeypot API](https://api.honeypot.is/v2/IsHoneypot)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON risk report with risk level and reason summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Risk level is summarized as low, medium, or high; unavailable checks may return null values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
