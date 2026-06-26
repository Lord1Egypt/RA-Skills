## Description: <br>
Self-improving learning loop inspired by Hermes Agent. Automatically extracts successful workflows, creates skills, and persists knowledge across sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mystour](https://clawhub.ai/user/mystour) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to add periodic self-reflection to OpenClaw workflows, extract reusable skills from successful sessions, and curate persistent local memory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create persistent memories and new agent skills from session activity. <br>
Mitigation: Keep LEARNING_AUTO_CREATE=false and review generated memory entries and SKILL.md files before reuse. <br>
Risk: Persisted memories may capture secrets or confidential project details from sessions. <br>
Mitigation: Avoid running it on sessions containing sensitive information and periodically inspect or delete the .openclaw memory and skills it creates. <br>


## Reference(s): <br>
- [Hermes Agent](https://github.com/NousResearch/hermes-agent) <br>
- [Hermes Docs](https://hermes-agent.nousresearch.com/) <br>
- [Agent Skills Specification](https://agentskills.io/specification) <br>
- [SQLite FTS5 Documentation](https://www.sqlite.org/fts5.html) <br>
- [ClawHub Release Page](https://clawhub.ai/mystour/hermes-learning-loop) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline bash commands and generated SKILL.md content] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write local .openclaw memory, state, and skill files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
