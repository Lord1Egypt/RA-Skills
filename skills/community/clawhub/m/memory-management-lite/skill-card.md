## Description: <br>
A practical memory management system for OpenClaw: importance scoring, time-decay cleanup, write triggers, hybrid retrieval, and daily maintenance workflow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuchang9337-dev](https://clawhub.ai/user/xuchang9337-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to decide what should be saved, retrieve prior preferences or decisions before answering, and maintain memory files over time without unbounded accumulation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist personal preferences, decisions, contacts, or other user information across sessions. <br>
Mitigation: Review what is saved, avoid secrets and private account data, and scope long-term memory to information the user explicitly wants retained. <br>
Risk: The maintenance workflow can delete memory logs older than 30 days. <br>
Mitigation: Archive before deleting and migrate important content into long-term or topic files before cleanup runs. <br>
Risk: The cron workflow includes optional OpenClaw configuration and API-key-related backup steps. <br>
Mitigation: Remove those backup steps unless the user has explicitly consented and the backup location is secured. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xuchang9337-dev/memory-management-lite) <br>
- [Publisher profile](https://clawhub.ai/user/xuchang9337-dev) <br>
- [Artifact homepage](https://clawhub.com/skills/memory-management) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file layouts, JSON cron examples, and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces agent-facing memory write, recall, cleanup, and scheduling guidance; it does not provide executable source code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
