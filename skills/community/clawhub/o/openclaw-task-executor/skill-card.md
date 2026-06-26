## Description: <br>
Classifies tasks by complexity, guides planning before execution, coordinates subagents when appropriate, and reports progress and results continuously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tomuiv](https://clawhub.ai/user/tomuiv) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to standardize OpenClaw task execution with upfront task classification, planning, progress reporting, retry behavior, and bounded subagent coordination. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may encourage subagent coordination, retries, and sensitive operations during task execution. <br>
Mitigation: Keep normal limits on subagent count, retries, timeouts, and require authorization before sensitive operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tomuiv/openclaw-task-executor) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with task plans, progress updates, command suggestions, and result summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only workflow; no hidden scripts, credential handling, or install-time behavior were reported by the security evidence.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
