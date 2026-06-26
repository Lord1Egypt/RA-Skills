## Description: <br>
Huo15 Multi Agent coordinates parallel OpenClaw subagents for task assignment, worker execution, result collection, and summary reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jobzhao15](https://clawhub.ai/user/jobzhao15) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to split independent work across multiple OpenClaw subagents, track worker status, and collect results into a coordinated response. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Command-capable subagents may perform actions beyond the user's intended scope. <br>
Mitigation: Limit subagent tools and permissions to the minimum needed before use, especially for exec, process, purchasing, and network-capable actions. <br>
Risk: Task text, worker state, and logs may be retained under the OpenClaw activity directory. <br>
Mitigation: Avoid placing secrets in task descriptions and review ~/.openclaw/workspace/memory/activity/multi-agent for retained data after use. <br>
Risk: Shell helpers write and delete local worker data with weak validation around worker IDs and user-provided strings. <br>
Mitigation: Inspect and patch the shell scripts before operational use, and use simple trusted identifiers and task strings until validation is strengthened. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown, JSON] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes coordination state and logs under ~/.openclaw/workspace/memory/activity/multi-agent when helper scripts are used.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence and SKILL.md version history) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
