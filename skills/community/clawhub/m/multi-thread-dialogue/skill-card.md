## Description: <br>
Multi-thread dialogue architecture that helps an agent route longer or independent work to background sub-agents while tracking status, interruptions, reviews, and monitoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[philonis](https://clawhub.ai/user/philonis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to coordinate multi-step work across foreground and background agent tasks, including task routing, status handling, interruption, and optional two-phase review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad natural-language commands such as stop or interrupt can accidentally affect an active background task. <br>
Mitigation: Use explicit task-number commands when stopping, interrupting, or checking work during multi-task sessions. <br>
Risk: Task orchestration state can expose task metadata if shared too broadly. <br>
Mitigation: Keep task state scoped to the active workspace and review status summaries before sharing them outside the task context. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/philonis/multi-thread-dialogue) <br>
- [Project homepage listed in artifact metadata](https://github.com/openclaw/multi-thread-dialogue) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes task state markers such as DONE, DONE_WITH_CONCERNS, NEEDS_CONTEXT, and BLOCKED.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
