## Description: <br>
Memory Layered helps AI agents maintain a persistent, searchable, and forgettable six-layer file-based memory system for dialogue history, indexes, topic files, reusable skills, active state, and lessons learned. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sheyuy](https://clawhub.ai/user/sheyuy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when an agent needs continuity across sessions without putting all memory into the prompt. It is suited for preserving user preferences, project state, shared multi-agent memory, and lessons learned in local Markdown files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local long-term memory files may contain personal details, project context, or confidential information. <br>
Mitigation: Decide what must never be stored before use, avoid storing secrets, credentials, regulated personal data, or confidential business details without a retention and deletion process, and review memory files periodically. <br>
Risk: Stored memory can become stale, conflict across topic files, or preserve information longer than intended. <br>
Mitigation: Use the read-only review, consolidation, stale-entry cleanup, and archive guidance described by the skill to keep the index aligned with topic files and remove expired entries. <br>


## Reference(s): <br>
- [Server-resolved GitHub source](https://github.com/Sheyuy/agent-skills/tree/main/skills/memory-layered) <br>
- [ClawHub skill page](https://clawhub.ai/sheyuy/memory-layered) <br>
- [Publisher homepage](https://www.botlearn.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash and Markdown examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local memory file structures and maintenance practices for an agent workspace.] <br>

## Skill Version(s): <br>
0.1.0 (source: release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
