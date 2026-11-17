## Description:

Interact with Obsidian vaults via the Obsidian CLI to read, create, search, and manage notes, tasks, and properties, and to support plugin and theme development with reload, JavaScript execution, error capture, screenshots, and DOM inspection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoyaryyj](https://clawhub.ai/user/hoyaryyj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and engineers use this skill to operate a running Obsidian vault from an agent, including note management and plugin or theme debugging workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify notes, tasks, and properties in an Obsidian vault.

Mitigation: Specify the vault and file explicitly for ordinary note tasks, and require confirmation before overwrite, append, or property changes.

Risk: The skill includes powerful plugin and theme development controls such as plugin reloads, screenshots, DOM inspection, and app-context JavaScript evaluation.

Mitigation: Use these controls only for the intended running Obsidian instance, and require confirmation before plugin reloads, screenshots, DOM inspection, or JavaScript evaluation.

Risk: Server security review marked the skill suspicious because ordinary note management is bundled with app-context JavaScript and debugging controls without clear safety boundaries.

Mitigation: Review proposed commands before execution and limit use to workflows where the agent is expected to operate Obsidian directly.

## Reference(s):

- [Obsidian CLI documentation](https://help.obsidian.md/cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Guidance]

**Output Format:** [Markdown with inline Obsidian CLI commands and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a running Obsidian instance; commands can target the active vault or an explicitly named vault, file, or path.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
