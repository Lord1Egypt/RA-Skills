## Description: <br>
Monitors child agent status and generates concise progress summaries every 30 seconds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangxiaofei860208-source](https://clawhub.ai/user/wangxiaofei860208-source) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent coordinators use this skill to monitor active child agents, summarize their current work in short status phrases, and report only meaningful progress changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on subagent and session-history access, so status summaries may expose recent worker activity to the coordinating agent. <br>
Mitigation: Use it only in agent workspaces where reviewing child-agent progress is expected, and avoid including sensitive details in user-facing summaries. <br>
Risk: Over-frequent polling can create noisy notifications or unnecessary tool usage. <br>
Mitigation: Follow the artifact guidance to poll no more than every 30 seconds and notify users only when status changes or a worker completes or fails. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wangxiaofei860208-source/lobster-agent-summary) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with command examples and status-summary text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Summaries are intended to be 3-5 words, checked no more often than every 30 seconds, and reported when status changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
