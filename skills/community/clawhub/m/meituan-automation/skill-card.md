## Description:

This skill lets an agent control a USB-debug-enabled Android phone to search Meituan restaurants, add menu items to a cart, and stop at checkout for user payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oscarka](https://clawhub.ai/user/oscarka)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users can use this skill to automate Meituan food-ordering workflows on a connected Android device, including restaurant search, menu navigation, cart management, and checkout review before manual payment.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill provides broad control of a USB-debug-enabled Android phone and Meituan account.

Mitigation: Install it only when the user intentionally wants an agent to control that device and account.

Risk: The packaged HTTP server exposes unauthenticated device-control operations, including taps, swipes, text entry, cart actions, checkout navigation, and address reads.

Mitigation: Run the server only on localhost or behind authentication, and require explicit user confirmation before sensitive operations.

Risk: The skill can expose personal delivery data while navigating checkout and address screens.

Mitigation: Limit use to trusted local environments and review outputs before sharing logs or agent transcripts.

Risk: Automated UI actions can add unintended items or advance to checkout if the app state differs from expectations.

Mitigation: Keep the physical device visible, review the cart and checkout page manually, and complete payment only by explicit user action.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/oscarka/skills/meituan-automation)
- [Meituan](https://www.meituan.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON or plain-text CLI status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Controls a local Android device and reports app state, cart, address, and checkout status; payment remains a manual user action.]

## Skill Version(s):

1.0.1 (source: evidence.release.version)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
