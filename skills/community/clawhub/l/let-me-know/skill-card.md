## Description: <br>
Notify the user before starting any long-running task and keep them updated. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fogyoy](https://clawhub.ai/user/fogyoy) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to keep users informed during long-running tasks with a pre-flight notice, periodic progress heartbeats, and immediate completion or failure updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security summary identifies a high-impact gateway restart fallback without explicit user approval. <br>
Mitigation: Require explicit user approval or remove the gateway restart fallback before installing or using the skill. <br>
Risk: Heartbeat messages may expose sensitive log details while reporting task progress. <br>
Mitigation: Summarize progress at a high level and avoid sending secrets, credentials, private paths, or sensitive log excerpts in heartbeat messages. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline command examples and message templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Progress messages should reflect current task state rather than repeated static templates.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
