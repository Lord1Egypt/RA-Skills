## Description: <br>
强制进度检查点。当龙虾助手在执行任务时超过60秒没有完成，必须立即向用户发送进度反馈，说明：任务是否正常运行、当前执行到哪个步骤、预计还要多久。用于防止用户对长时间运行任务的不确定感。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chrislawyeryounger-spec](https://clawhub.ai/user/chrislawyeryounger-spec) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and workflow authors use this skill to send clear progress updates during long-running searches, crawling, batch file processing, multi-step writing, external API calls, and other tasks with uncertain runtime. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may interrupt long-running work with progress messages. <br>
Mitigation: Use it where proactive status reporting is desired, and keep its priority language subordinate to platform and user-instruction boundaries. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown progress-update messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No code execution; produces human-facing status, progress, and time-estimate guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
