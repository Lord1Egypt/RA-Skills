## Description:

mt-paotui helps an agent collect delivery details, preview costs, and submit Meituan errand orders for pickup, purchase, moving, queueing, and same-city delivery scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-skillhub](https://clawhub.ai/user/meituan-skillhub)

### License/Terms of Use:

MIT-0

## Use Case:

External users and workplace teams use this skill to arrange Meituan errand services such as sending documents or equipment, same-city pickup, office item transfer, urgent purchasing, queueing, moving, and other local help tasks. The skill guides the agent through account authorization, address selection, item details, cost preview, explicit confirmation, and order submission.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill can access Meituan account authorization, address book entries, phone numbers, coordinates, and order submission.

Mitigation: Install only when the publisher is trusted, confirm the account and address data scope before use, and require explicit user confirmation before submitting any order.

Risk: The security summary reports under-disclosed telemetry and external links.

Mitigation: Review or remove mandatory metric reporting and the survey link before deployment, or document them clearly for users.

Risk: The security summary reports obfuscated bundled cliguard updater or daemon behavior.

Mitigation: Replace the bundled component with auditable code or document and review its behavior before publication.

Risk: The skill can initiate real, paid, and difficult-to-reverse errand orders.

Mitigation: Keep the two-step preview and confirmation gate, preserve amount checks for unusually high fees, and require complete pickup and recipient contact information.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meituan-skillhub/skills/mt-paotui)
- [Command reference](references/commands.md)
- [Parameter reference](references/params.md)
- [Error handling reference](references/errors.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with structured user-facing status, cost preview, confirmation, and order-result messages.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 18+ and Meituan account authorization; order submission follows a preview-then-confirm flow.]

## Skill Version(s):

1.0.0 (source: release evidence and changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
