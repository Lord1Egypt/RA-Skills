## Description: <br>
Coordinates sub-agents to break down complex tasks, run delegated work in the background, and summarize important progress for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xaiohuangningde](https://clawhub.ai/user/xaiohuangningde) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to coordinate complex agent tasks by decomposing work, delegating search, analysis, execution, and monitoring to sub-agents, and receiving summarized status updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can coordinate high-autonomy delegation, including browsing, script execution, automation, and background monitoring. <br>
Mitigation: Require explicit user confirmation before spawning child agents, running scripts, crawling sites, or starting monitoring. <br>
Risk: Background sub-agent work can reduce user visibility into active tasks and decisions. <br>
Mitigation: Keep background tasks visible, summarize important progress, and make delegated tasks easy to stop. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/xaiohuangningde/meta) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown or plain text task breakdowns, delegated work summaries, and status updates.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May coordinate background sub-agent activity for browsing, analysis, script execution, automation, and monitoring when the user allows it.] <br>

## Skill Version(s): <br>
1.0.0 (source: skill.json and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
