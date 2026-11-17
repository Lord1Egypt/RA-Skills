## Description:

Guides an agent through user-authorized Pinduoduo purchases on Android via USB ADB, from product search and specification checks to payment and order confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlittlebear](https://clawhub.ai/user/openlittlebear)

### License/Terms of Use:

MIT-0

## Use Case:

Users and their agents use this skill to find and purchase a requested item in the Pinduoduo Android app, verify the selected product and price, and report the resulting order.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An incorrect product, specification, quantity, price, or shop could result in an unintended purchase.

Mitigation: Show the user the item and order details and obtain confirmation before submitting the order.

Risk: Payment involves a wallet PIN and biometric verification.

Mitigation: Use a user-provided PIN only for that transaction and leave biometric verification to the user.

Risk: The shopping workflow depends on a separately installed base skill.

Mitigation: Verify the appium-android-adb base skill and its requirements before installation or use.

## Reference(s):

- [Pdd Android Adb on ClawHub](https://clawhub.ai/openlittlebear/skills/pdd-android-adb)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Text]

**Output Format:** [Markdown with shell commands and order summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a connected Android device and the separate appium-android-adb base skill; pauses for user confirmation and biometric verification.]

## Skill Version(s):

1.0.4 (source: server-resolved release metadata and _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
