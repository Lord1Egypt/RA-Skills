## Description: <br>
Simple text-based memory system for AI assistants with an auto-install script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crystaria](https://clawhub.ai/user/crystaria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI assistant users use Memory Boost to preserve user preferences, project history, decisions, and session logs across conversations and multiple assistants. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive or private information in local memory files across sessions. <br>
Mitigation: Do not store secrets, credentials, regulated data, client-confidential material, or private personal details; inspect and prune memory files regularly. <br>
Risk: Shared memory files can carry stale, incorrect, or overbroad context into later sessions or other assistants. <br>
Mitigation: Review memory files before relying on them, keep entries concise, and correct or remove outdated decisions and preferences. <br>
Risk: The install script creates and updates workspace-level memory files. <br>
Mitigation: Run it only in the intended project directory and consider project-specific memory storage instead of shared home-level memory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crystaria/memory-boost) <br>
- [Clawdis homepage](https://clawhub.ai/skills/memory-boost) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command snippets and generated local Markdown memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates MEMORY.md, MEMORY_INDEX.md, and dated memory/*.md files when the install script and skill workflow are used.] <br>

## Skill Version(s): <br>
1.1.1 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
