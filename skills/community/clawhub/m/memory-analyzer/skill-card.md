## Description: <br>
Analyzes conversation history, extracts user preferences and feedback, updates memory files automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TevfikGulep](https://clawhub.ai/user/TevfikGulep) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to analyze conversation history, extract durable user preferences, and prepare updates for long-term memory files such as MEMORY.md, AGENTS.md, USER.md, IDENTITY.md, and SOUL.md. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read conversation history and change long-term memory files. <br>
Mitigation: Use it only with explicit approval and a visible diff before changes are applied to AGENTS.md, IDENTITY.md, SOUL.md, USER.md, or MEMORY.md. <br>
Risk: Bundled output contains personal and operational details that could be persisted or redistributed. <br>
Mitigation: Remove memory_analyzer_output.json before installation and avoid storing contact details, account details, workflow secrets, or unverified preferences in memory files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TevfikGulep/memory-analyzer) <br>
- [Skill homepage](https://clawhub.com/skills/memory-analyzer) <br>
- [Publisher profile](https://clawhub.ai/user/TevfikGulep) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Guidance] <br>
**Output Format:** [Markdown notes and structured JSON memory-update suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose persistent updates to long-term agent memory files.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
