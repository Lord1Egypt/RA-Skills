## Description:

Manage shopping cart operations via n8n webhook integration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haresh-sai06](https://clawhub.ai/user/haresh-sai06)

### License/Terms of Use:


## Use Case:

External users and commerce automation agents use this skill to manage shopping cart actions, including adding products, removing products with confirmation, and updating quantities through configured local n8n webhooks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Invoking the skill may change shopping cart state through local n8n webhooks.

Mitigation: Install only when the intended local webhook implementation is configured, and confirm destructive cart actions before execution.

Risk: The skill describes calls to localhost webhooks but does not define the server-side webhook behavior.

Mitigation: Review the local n8n webhook implementation separately before deployment.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, API calls, guidance]

**Output Format:** [Text guidance with local webhook endpoints and user confirmation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires intended local n8n webhook endpoints; cart-changing actions should be confirmed as described by the skill.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
