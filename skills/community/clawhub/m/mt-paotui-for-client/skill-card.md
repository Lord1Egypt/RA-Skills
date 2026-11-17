## Description:

美团跑腿 is a Meituan errand-ordering assistant for pickup-and-delivery, purchasing, queue or registration help, moving or disposal help, and other local errand requests.

This skill is ready for commercial/non-commercial use.

## Publisher:

[meituan-tech](https://clawhub.ai/user/meituan-tech)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to prepare Meituan errand orders, compare service options, preview fees and timing, submit only user-confirmed orders, and guide payment. It handles real account authorization, address information, contact phone numbers, order submission, and payment-link creation.

### Deployment Geography for Use:

China mainland

## Known Risks and Mitigations:

Risk: The skill can access a Meituan account flow, address book, real phone numbers, order submission, and payment-link creation.

Mitigation: Install and use only with explicit user authorization, preserve token secrecy, preview order details before submission, and require clear user confirmation before placing or paying for an order.

Risk: The security summary reports under-disclosed background fingerprinting and self-update behavior.

Mitigation: Before deployment, require publisher documentation for the bundled @sec/cliguard daemon, including reported fingerprint data, update authentication, disable and removal steps, and the reason obfuscated code is necessary.

Risk: Real errand orders can create financial charges and may be difficult to reverse after confirmation.

Mitigation: Maintain two-step confirmation, re-confirm unusually high fees, and make the user review service type, addresses, item details, fee, and timing before submission.

Risk: The release is marked suspicious by the authoritative security evidence.

Mitigation: Review and scan the bundled code and dependencies before installation or enterprise rollout, with particular attention to obfuscated code, bundled dependencies, and network behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/meituan-tech/skills/mt-paotui-for-client)
- [Command and parameter reference](references/commands.md)
- [Error handling reference](references/errors.md)
- [Order parameter reference](references/params.md)
- [Passport authorization reference](passport-auth/reference.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language Markdown responses with command-backed order previews, confirmation prompts, status messages, and payment guidance.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Meituan account authorization and real contact, address, order, and payment details; user-facing output is intentionally summarized.]

## Skill Version(s):

1.0.5 (source: release evidence, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
