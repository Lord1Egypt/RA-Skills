## Description:

Order groceries from Picnic supermarket - search products, manage cart, schedule delivery.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mpociot](https://clawhub.ai/user/mpociot)

### License/Terms of Use:


## Use Case:

External users with a Picnic account use this skill to search grocery products, manage a cart, inspect delivery slots and history, and prepare an order for completion in the Picnic app.

### Deployment Geography for Use:

Germany and Netherlands

## Known Risks and Mitigations:

Risk: The skill handles Picnic account credentials, cart contents, address, delivery history, and other account data.

Mitigation: Review the skill before installing, avoid entering the Picnic password as a command-line argument, and do not share output from login or two-factor authentication flows.

Risk: The included debug script can print raw account delivery data.

Mitigation: Do not use the debug script during normal operation, and remove or quarantine it before installing the skill in shared environments.

Risk: Commands can modify a user's cart or selected delivery slot.

Mitigation: Confirm with the user before adding or removing products, clearing the cart, or setting a delivery slot; final checkout remains in the Picnic app.

## Reference(s):

- [ClawHub Picnic skill page](https://clawhub.ai/mpociot/skills/picnic)

## Skill Output:

**Output Type(s):** [shell commands, configuration, JSON, guidance]

**Output Format:** [Markdown instructions with inline shell commands; CLI commands return JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Picnic account and country code DE or NL; authentication details are stored in the local user config.]

## Skill Version(s):

1.0.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
