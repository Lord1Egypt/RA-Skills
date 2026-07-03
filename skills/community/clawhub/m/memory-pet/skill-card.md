## Description: <br>
A pet-themed memory compression skill that uses ASCII pet interactions, Python-managed local state, affinity decay, escape behavior, and context-summary storage to help an agent save and recall conversation memories. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ldxs001](https://clawhub.ai/user/ldxs001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent developers use this skill to add a lightweight virtual-pet interface for saving, summarizing, and recalling conversation memories. It is best suited for playful personal workflows where local memory persistence and possible deletion are acceptable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist broad conversation summaries and keywords to local files, which may capture sensitive information from the active chat. <br>
Mitigation: Use it only in conversations suitable for local memory storage, and avoid chats containing secrets, credentials, health, legal, financial, or business-sensitive information. <br>
Risk: Pet escape and fusion behavior can delete stored pet memories. <br>
Mitigation: Review or back up the skill data directory before relying on saved memories, and treat escape or fusion as potentially irreversible data-loss events. <br>
Risk: The release evidence reports that permission documentation understates or contradicts the memory persistence and deletion behavior. <br>
Mitigation: Review the security guidance and the permission notes before deployment, and require user confirmation before enabling the memory-saving workflow. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ldxs001/skills/memory-pet) <br>
- [Guide](references/guide.md) <br>
- [Permissions](references/permissions.md) <br>
- [Examples](references/examples.md) <br>
- [Changelog](references/changelog.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown responses with ASCII art, inline shell commands, and local JSON state managed through Python CLI scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save conversation summaries, keywords, pet state, food logs, and recall data under the skill data directory.] <br>

## Skill Version(s): <br>
0.5.0 (source: frontmatter and changelog, released 2026-06-03) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
