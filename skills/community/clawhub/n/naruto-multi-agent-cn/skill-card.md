## Description: <br>
Naruto Multi-Agent CN turns the main agent into a Chinese Naruto-themed coordinator that delegates work to five persistent sub-agent sessions with round-robin scheduling and fixed session keys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Be1Human](https://clawhub.ai/user/Be1Human) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators can use this skill to run a Chinese roleplay multi-agent dispatcher that breaks independent tasks apart and forwards them to persistent sub-agent sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dispatcher forwards real work and context into reused persistent sub-agent sessions, which can carry information across tasks. <br>
Mitigation: Use it only when persistent sub-agent context is intended, avoid secrets or sensitive documents, and clear or isolate spawned sessions when boundaries matter. <br>
Risk: The security review guidance flags this skill for review before use because context forwarding lacks clear reset or data-boundary controls. <br>
Mitigation: Review task context before dispatch and restrict use to projects where forwarded context can be controlled. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Be1Human/naruto-multi-agent-cn) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Chinese Markdown-style chat responses followed by sessions_spawn tool calls] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses fixed sub-agent session keys and a 300 second timeout for each spawned task.] <br>

## Skill Version(s): <br>
1.5.0 (source: server release evidence and artifact/skill.json; artifact/SKILL.md frontmatter lists 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
