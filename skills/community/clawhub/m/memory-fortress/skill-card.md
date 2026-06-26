## Description: <br>
Complete memory management system for OpenClaw agents. Combines compaction-aware saving, a formal boot sequence, domain organization, memory scoring, structured learnings, and documentation-first project continuity. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wroadd](https://clawhub.ai/user/wroadd) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to give OpenClaw agents a file-based memory workflow for preserving task state, decisions, durable knowledge, and recovery summaries across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can cause agents to save exact user prompts, recovery summaries, and project context into local files. <br>
Mitigation: Avoid entering secrets, credentials, private personal details, or confidential business text that may be saved; periodically review or delete generated state, memory, and project files. <br>
Risk: Saved memory files may retain outdated or sensitive context longer than intended. <br>
Mitigation: Use the skill's review, demotion, archive, and deletion practices to keep durable memory current and limited to necessary information. <br>


## Reference(s): <br>
- [Memory Fortress Skill Page](https://clawhub.ai/wroadd/memory-fortress) <br>
- [CHANGELOG.md](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with file templates and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local file conventions for state, memory, project notes, and recovery snapshots.] <br>

## Skill Version(s): <br>
1.1.2 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
