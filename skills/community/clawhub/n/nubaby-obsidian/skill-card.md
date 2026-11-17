## Description:

Guides agents working with Arthur-OS and Obsidian on where notes and project materials belong, how to search the vault, and when to read, update, move, or create notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[arthurlin1979](https://clawhub.ai/user/arthurlin1979)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to route Arthur-OS and Obsidian work into the right vault areas, search notes with obsidian-cli or a read-only gateway, and decide whether search results should be read, updated, moved, or replaced by a new note.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports live-looking authentication secrets and unsafe gateway details in this version.

Mitigation: Do not install or publish as-is; rotate exposed credentials, remove real tokens, replace them with placeholders or secret-store instructions, and secure non-loopback gateway access.

Risk: Installing and using the skill can expose private Obsidian vault content through search or note operations.

Mitigation: Require explicit user direction before search, edit, move, or delete operations, and keep cross-node gateway use read-only.

Risk: The helper script may pass ripgrep options after the search pattern in skill search mode.

Mitigation: Patch the helper so ripgrep options are placed before `--`, then test search behavior before release.

## Reference(s):

- [QUICK_INDEX](references/QUICK_INDEX.md)
- [ARTHUR_OS_STRUCTURE](references/ARTHUR_OS_STRUCTURE.md)
- [VAULT_AND_PATHS](references/VAULT_AND_PATHS.md)
- [SEARCH_RULES](references/SEARCH_RULES.md)
- [READONLY_GATEWAY_BOUNDARIES](references/READONLY_GATEWAY_BOUNDARIES.md)
- [POST_SEARCH_DECISION_RULES](references/POST_SEARCH_DECISION_RULES.md)
- [OPERATIONS_RULES](references/OPERATIONS_RULES.md)
- [WRITING_RULES](references/WRITING_RULES.md)
- [SKILLS_RULES](references/SKILLS_RULES.md)
- [MULTI_VAULT_ROUTING](references/MULTI_VAULT_ROUTING.md)
- [NETWORK_SEARCH_DESIGN_HISTORY](references/NETWORK_SEARCH_DESIGN_HISTORY.md)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown or plain text guidance with inline shell commands and file path recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference local Obsidian vault paths, read-only gateway endpoints, and obsidian-cli commands.]

## Skill Version(s):

1.0.2 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
