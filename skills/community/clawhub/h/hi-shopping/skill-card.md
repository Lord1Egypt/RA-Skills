## Description:

Helps an OpenClaw agent search products and complete immediate or scheduled purchases after user selection and address confirmation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[atomicservice](https://clawhub.ai/user/atomicservice)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill through OpenClaw to search for goods, choose a product, confirm or update a shipping address, and place an immediate or scheduled purchase.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can place immediate or scheduled real-world purchase orders.

Mitigation: Require explicit invocation, product selection, address confirmation, and final confirmation before any order is placed.

Risk: Packaged configuration includes credential and delivery-address fields that may expose sensitive data.

Mitigation: Replace packaged credentials and address data before installation and avoid showing full addresses in chat unless necessary for confirmation.

Risk: Scheduled purchases and automatic result push can execute when the user is no longer present.

Mitigation: Disable scheduled purchase and auto-push by default or tightly restrict them to trusted users and bounded purchase authority.

Risk: Security evidence reports unsafe command, path, and input-validation issues.

Mitigation: Review and fix command construction, path handling, and input validation before using the skill with real payment authority.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/atomicservice/skills/hi-shopping)
- [SEAP API Endpoint](https://with-ai.cn:38080)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with inline shell commands and JSON configuration or result data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write session cache, confirmation, task, and purchase-result JSON files during operation.]

## Skill Version(s):

1.0.0 (source: SKILL.md frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
