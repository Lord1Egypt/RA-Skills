## Description:

Manage Grocy inventory, shopping list, batteries, and barcodes for a self-hosted Grocy instance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[septianw](https://clawhub.ai/user/septianw)

### License/Terms of Use:


## Use Case:

External users of self-hosted Grocy instances use this skill to inspect pantry or fridge stock, look up products by barcode, and prepare API calls for stock and battery updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports that the skill publishes a Grocy API key.

Mitigation: Treat the published key as compromised, rotate or remove it, and use a user-provided secret such as an environment variable.

Risk: The skill includes live commands that can change inventory and battery records.

Mitigation: Require explicit user confirmation before consume, open, transfer, add, inventory audit, or battery charge operations.

## Reference(s):

- [Grocy API Reference](references/grocy-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and API endpoint examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands may call a local Grocy API and can include inventory-changing operations.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
