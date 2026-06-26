## Description: <br>
Dynamic attachment injection helps agents add changing context without modifying the system prompt. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to keep dynamic lists such as skills, agents, and memory summaries out of the system prompt while still making them available when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local agent and skill markdown files, which can include private workflows or sensitive notes. <br>
Mitigation: Use it only in repositories where that local context is appropriate to inspect. <br>
Risk: Generated registry or AGENTS.md changes could affect future agent behavior. <br>
Mitigation: Review generated registry and prompt-context changes before relying on them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/lobster-attachment-inject) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell command examples and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces registry and prompt-context guidance; no hidden code execution or data export was found in the release security evidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
