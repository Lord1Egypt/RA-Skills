## Description:

Llm Memory V9 provides a public framework for linking a user-specified local private configuration directory into an agent skill workspace.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xkzs2007](https://clawhub.ai/user/xkzs2007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep public workspace templates separate from private local memory, agent rules, tool configuration, and other user-controlled files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The postinstall hook can link or copy broad private local content into the trusted skill directory.

Mitigation: Set CNB_PRIVATE_WORKSPACE only to a narrow, reviewed directory containing files intended for agent use.

Risk: Imported private files such as AGENTS.md, TOOLS.md, MEMORY.md, scripts, or config files can affect agent behavior after installation.

Mitigation: Review private workspace contents before installation and avoid home folders, synced folders, or shared directories.

Risk: Users who do not need private configuration import still receive an install hook path.

Mitigation: Install with hooks disabled when private local configuration import is not required.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xkzs2007/skills/llm-memory-integration)
- [Hook documentation](artifact/hooks/README.md)
- [Workspace template documentation](artifact/workspace_template/README.md)

## Skill Output:

**Output Type(s):** [Files, Configuration, Guidance, Shell commands]

**Output Format:** [Markdown guidance and local workspace files or symlinks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses optional CNB_PRIVATE_WORKSPACE to link or copy user-controlled local files at install time.]

## Skill Version(s):

9.0.1 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
