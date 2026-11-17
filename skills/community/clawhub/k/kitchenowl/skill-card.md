## Description:

Use kitchenowl-cli from terminal with pipx install, auth, and core read/write commands for KitchenOwl.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apetersson](https://clawhub.ai/user/apetersson)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to install and operate KitchenOwl through the kitchenowl CLI for authentication, server settings, households, shopping lists, recipes, and user lookup workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A third-party CLI package or project could be different from the one the user intends to trust.

Mitigation: Verify the kitchenowl-cli package and KitchenOwl CLI GitHub project before installation or upgrade.

Risk: KitchenOwl authentication tokens are stored in a local config file.

Mitigation: Treat the KitchenOwl config file as sensitive and avoid exposing token contents in agent output.

Risk: Delete, remove-item, and bulk-edit commands can modify or remove KitchenOwl data.

Mitigation: Start with read-only commands, use explicit IDs and household scope, and ask for confirmation before destructive actions.

## Reference(s):

- [KitchenOwl CLI Command Reference](references/commands.md)
- [KitchenOwl CLI GitHub Project](https://github.com/kitchenowl/kitchenowl-cli)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include JSON-oriented CLI usage guidance when command output is consumed programmatically.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
