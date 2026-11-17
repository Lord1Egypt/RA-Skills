## Description:

Manage grocery shopping on Knuspr.de via the knuspr-cli for product search, cart management, delivery slot reservation, shopping lists, order history, deals, favorites, and meal suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lars147](https://clawhub.ai/user/lars147)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to operate a Knuspr.de grocery account through a bundled Python CLI, including searching products, managing carts and lists, reserving delivery slots, reviewing order history, and generating shopping suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access sensitive Knuspr account login material and saved session or credential files.

Mitigation: Prefer interactive login, avoid command-line passwords and saved credential files, and protect or remove any local session or credential files after use.

Risk: The CLI can modify a live shopping account by adding many items, repeating orders, reserving or releasing slots, and changing lists or favorites.

Mitigation: Require explicit user confirmation for cart, slot, list, favorite, and reorder changes, and keep checkout as a user-reviewed action outside the skill.

Risk: The README states the CLI uses an unofficial Knuspr interface, so service changes may break behavior or produce unexpected results.

Mitigation: Verify cart contents, prices, delivery slots, and account changes in Knuspr before relying on the result.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lars147/skills/knuspr-cli)
- [Knuspr CLI command reference](artifact/references/commands.md)
- [Knuspr.de](https://www.knuspr.de)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, Text, JSON]

**Output Format:** [Markdown guidance with shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The skill instructs agents to use --json for programmatic CLI parsing and to show prices and totals before cart changes.]

## Skill Version(s):

0.1.0 (source: server release metadata and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
