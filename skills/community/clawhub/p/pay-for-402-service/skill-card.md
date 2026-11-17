## Description:

This skill helps an agent handle A402 HTTP 402 Payment Needed flows by checking wallet readiness, invoking the Alipay payment CLI, retrying the protected request with proof, and sending a fulfillment acknowledgment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kangleyi](https://clawhub.ai/user/kangleyi)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when a service returns an A402 or HTTP 402 Payment Needed response and the user intends to complete payment through Alipay. It guides the agent through wallet checks, payment initiation, payment-status query, protected-resource retry, and fulfillment acknowledgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill initiates a payment flow through an external CLI and should only be used when the user expects an Alipay 402 payment flow.

Mitigation: Use it only for expected 402 Payment Needed responses, confirm the payment in Alipay yourself, and do not continue after payment initiation until the user confirms completion.

Risk: The release depends on npm installation and the external alipay-bot CLI.

Mitigation: Install and run it in an environment where npm package installation is controlled and the alipay-bot binary is expected.

Risk: Payment-flow parameters such as filenames, trade numbers, and resource URLs can create command or path-injection risk if accepted unchecked.

Mitigation: Apply the skill's documented validation rules for filenames, numeric trade numbers, HTTPS resource URLs, and fulfillment acknowledgment arguments before executing commands.

Risk: Payment outputs may contain URLs, QR-code media paths, or payment-related identifiers that must be handled exactly and carefully.

Mitigation: Preserve CLI output needed for the payment flow, use the documented domain and media-path checks, and avoid exposing credentials, signatures, keys, or payment proofs beyond what the CLI intentionally returns.

## Reference(s):

- [Payment Skills Homepage](https://github.com/alipay/payment-skills)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command snippets and possible JSON or Markdown CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires npm, alipay-bot, and AIPAY_OUTPUT_CHANNEL; pauses after payment initiation until the user confirms payment completion.]

## Skill Version(s):

1.0.5 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
