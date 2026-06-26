## Description: <br>
Huo15 OpenClaw Multi Agent helps coordinate parallel OpenClaw subagents with task assignment, worker execution, and result summaries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhaobod1](https://clawhub.ai/user/zhaobod1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to coordinate OpenClaw subagents for parallel task execution, task tracking, and result aggregation in coding or analysis workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad activation language may trigger subagent orchestration without clear user intent. <br>
Mitigation: Narrow activation phrases and require explicit confirmation before spawning workers. <br>
Risk: Subagent orchestration can increase cost, share task context with additional sessions, or leave work running longer than intended. <br>
Mitigation: Set concurrency, depth, timeout, and model limits before use, and monitor active subagent tasks through the available subagent status tools. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhaobod1/huo15-openclaw-multi-agent) <br>
- [Publisher profile](https://clawhub.ai/user/zhaobod1) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands and configuration that spawn or track subagents; review before running.] <br>

## Skill Version(s): <br>
2.3.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
