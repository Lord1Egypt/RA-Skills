## Description: <br>
Discover and write typed relationships between Obsidian vault notes. Uses plain Markdown and YAML - no plugins required. Works with any AI agent that has file access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dial481](https://clawhub.ai/user/dial481) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and knowledge workers use this skill to analyze Obsidian vault notes, discover meaningful typed relationships, and write approved Markdown/YAML relationship metadata. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read selected Obsidian vault notes, which may expose private knowledge-base content. <br>
Mitigation: Limit the folders, note counts, and topics the agent may inspect, and avoid granting access to unrelated vault areas. <br>
Risk: The skill can edit Markdown and YAML relationship metadata, which could add incorrect links or damage note structure. <br>
Mitigation: Keep backups or version control, review findings before writes during normal use, and verify modified notes after writing. <br>
Risk: Autonomous mode can make relationship edits without per-link approval. <br>
Mitigation: Use autonomous mode only with clear limits on folders, note counts, and allowed relationship types, and require a summary of changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dial481/obsidian-vault-linker) <br>
- [Wikilink Types](https://github.com/penfieldlabs/obsidian-wikilink-types) <br>
- [Penfield](https://penfield.app) <br>
- [Penfield OpenClaw Plugin](https://github.com/penfieldlabs/openclaw-penfield) <br>
- [Obsidian skill by steipete](https://clawhub.ai/steipete/obsidian) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Configuration, Shell commands, Guidance] <br>
**Output Format:** [Markdown with optional YAML frontmatter edits and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose or write typed wikilinks and YAML relationship metadata after user approval or within explicitly granted autonomous limits.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
