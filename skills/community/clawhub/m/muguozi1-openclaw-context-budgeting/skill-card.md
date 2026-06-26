## Description: <br>
Manage and optimize OpenClaw context window usage via partitioning, pre-compression checkpointing, and information lifecycle management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[muguozi1](https://clawhub.ai/user/muguozi1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage long-running OpenClaw sessions when context usage is high, checkpoint important decisions before compaction, and reduce token cost or latency from oversized context. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Checkpoint summaries can capture sensitive information from the active session. <br>
Mitigation: Review HOT_MEMORY.md before compaction and avoid storing credentials, secrets, or private raw data in checkpoint memory. <br>
Risk: Compaction can discard details that are not represented in the checkpoint summary. <br>
Mitigation: Preserve important raw data elsewhere before cleanup and summarize key decisions, status, and next steps before running the compaction script. <br>
Risk: The included tests and examples are placeholders and do not prove production behavior. <br>
Mitigation: Treat quality badges cautiously and validate the workflow in the target OpenClaw environment before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/muguozi1/muguozi1-openclaw-context-budgeting) <br>
- [Publisher profile](https://clawhub.ai/user/muguozi1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct the agent to update checkpoint memory before invoking compaction behavior.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
