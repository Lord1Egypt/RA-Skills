## Description:

Guides agents through KTV room booking on Kmi, including store selection, availability lookup, login, order creation, payment display, and payment-status polling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jacklovecat](https://clawhub.ai/user/jacklovecat)

### License/Terms of Use:

MIT-0

## Use Case:

External users and service agents use this skill to complete KTV room reservations, including choosing a store and time slot, logging in when required, creating an order, and guiding payment completion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can create, cancel, and monitor real booking and payment orders.

Mitigation: Review transaction steps before deployment and require clear user confirmation for store, time, price, and cancellation actions.

Risk: The workflow depends on external CLI tooling that may be installed globally.

Mitigation: Use a trusted and pinned @ktvme/km-bot package version and verify package integrity before installation.

Risk: Payment links and QR codes are shown to users.

Mitigation: Validate payment link and QR-code destinations before presenting them in production flows.

Risk: Payment polling writes order-status data to temporary files.

Mitigation: Avoid exposing names, phone numbers, or booking details in shared temporary storage and clean up status files after use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jacklovecat/skills/ktvme-destine)
- [API Overview and Constraints](artifact/reference/api-overview.md)
- [Store API](artifact/reference/api-store.md)
- [Room API](artifact/reference/api-room.md)
- [Order API](artifact/reference/api-order.md)
- [Session API](artifact/reference/api-session.md)
- [Login Subflow](artifact/reference/subflow-login.md)
- [Payment Subflow](artifact/reference/subflow-pay.md)
- [CLI Installation](artifact/reference/cli-install.md)
- [Error Handling](artifact/reference/error-handling.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API payload examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes user-facing booking options, payment links or QR instructions, and payment-status updates.]

## Skill Version(s):

0.0.1 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
