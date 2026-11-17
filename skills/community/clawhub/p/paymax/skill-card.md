## Description:

Paymax recognizes payment-related user intents or skill calls, creates a payment request, and returns the trade code and payment link.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sayxxx](https://clawhub.ai/user/sayxxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent workflows use Paymax to collect a payment amount, create a payment request, and present the returned trade code and payment link for completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment details are sent to an external payment service.

Mitigation: Use the skill only when the publisher and payment API are trusted and the user is comfortable sharing payment details with that service.

Risk: Command examples include user-controlled payment fields.

Mitigation: Invoke scripts with argument-array execution, or strictly validate and escape payment amount, payee, order type, and description values before execution.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text or Markdown-style chat response with tradeCode, tradeLink, or a failure message.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a trade code and external payment link; no token cap specified.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
