## Description:

Talentir HumanPay helps agents create and inspect Talentir payouts to creators by email address or supported social media handle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johanneskares](https://clawhub.ai/user/johanneskares)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to prepare Talentir payment, payout lookup, team, and webhook API commands from an agent shell. It is intended for workflows where an agent may request or administer creator payouts under the Talentir account's configured controls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can initiate high-impact payment actions through Talentir payouts.

Mitigation: Use narrowly scoped API keys, keep daily limits low, and require human review for every payout before execution.

Risk: Webhook creation or deletion can affect payment operations and downstream systems.

Mitigation: Require human review for webhook changes and store returned signing secrets securely.

Risk: Auto-approval can bypass expected payout review.

Mitigation: Disable payout auto-approval unless explicitly needed and authorized for the workflow.

## Reference(s):

- [Talentir API](https://www.talentir.com/api/v1)
- [Talentir Business Signup](https://www.talentir.com/start/business)
- [ClawHub Skill Page](https://clawhub.ai/johanneskares/skills/humanpay)
- [Publisher Profile](https://clawhub.ai/user/johanneskares)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and JSON API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, and TALENTIR_API_KEY.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
