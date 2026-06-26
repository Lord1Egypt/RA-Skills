## Description: <br>
Routes Arthur-OS and Obsidian note work by deciding where content belongs, how to search it, and when to read, edit, move, create, or defer note operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[arthurlin1979](https://clawhub.ai/user/arthurlin1979) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators working with Arthur-OS or Obsidian use this skill to route notes, reports, project documents, server documents, skill documents, and AI outputs into the right vault areas. It also guides local and read-only gateway search, post-search decisions, and cautious note operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security evidence reports exposed fixed Obsidian gateway or plugin credentials and private network details. <br>
Mitigation: Remove those credentials from the release, rotate them before installation, and require user-supplied scoped credentials outside the skill text. <br>
Risk: The security evidence reports note mutation and deletion workflows. <br>
Mitigation: Keep remote access read-only and LAN-limited, and require explicit confirmation before create, move, rename, direct edit, or delete actions. <br>
Risk: The skill depends on local Obsidian tooling and gateway access. <br>
Mitigation: Declare required local tools and verify the vault path before performing any operation that affects files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/arthurlin1979/nubaby-obsidian) <br>
- [QUICK_INDEX.md](references/QUICK_INDEX.md) <br>
- [VAULT_AND_PATHS.md](references/VAULT_AND_PATHS.md) <br>
- [ARTHUR_OS_STRUCTURE.md](references/ARTHUR_OS_STRUCTURE.md) <br>
- [SEARCH_RULES.md](references/SEARCH_RULES.md) <br>
- [READONLY_GATEWAY_BOUNDARIES.md](references/READONLY_GATEWAY_BOUNDARIES.md) <br>
- [POST_SEARCH_DECISION_RULES.md](references/POST_SEARCH_DECISION_RULES.md) <br>
- [OPERATIONS_RULES.md](references/OPERATIONS_RULES.md) <br>
- [WRITING_RULES.md](references/WRITING_RULES.md) <br>
- [SKILLS_RULES.md](references/SKILLS_RULES.md) <br>
- [MULTI_VAULT_ROUTING.md](references/MULTI_VAULT_ROUTING.md) <br>
- [NETWORK_SEARCH_DESIGN_HISTORY.md](references/NETWORK_SEARCH_DESIGN_HISTORY.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file path recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are decision guidance for Obsidian vault routing, search, and note operations; actions that create, move, rename, edit, or delete notes require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
