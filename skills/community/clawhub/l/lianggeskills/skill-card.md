## Description: <br>
专为亮哥打造的务实、高效、带情绪支持的 Web3/AI 工作流助手。基于艾森豪威尔矩阵和四类任务状态进行高频管理。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[271498019](https://clawhub.ai/user/271498019) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users who want a Chinese-language Web3/AI work assistant can use this skill to triage tasks, track task status, receive reminders, and get brief emotional support responses. It is especially tailored to a user working in crypto, on-chain trading, meme-coin monitoring, alpha discovery, and AI news tracking. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task titles, blockers, and status history are stored in local task memory and may contain sensitive work details. <br>
Mitigation: Avoid storing secrets, private keys, credentials, or sensitive account details in task titles or blockers. <br>
Risk: Abandoned tasks are deleted from the active local task workspace, which can cause data loss if used accidentally. <br>
Mitigation: Review task names before issuing abandon commands and consider adding an undo or archive step before deployment in stricter workflows. <br>
Risk: Periodic reminders and proactive check-ins may be disruptive outside the intended work rhythm. <br>
Mitigation: Adjust the configured work hours, timezone, reminder intervals, and trigger phrases before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/271498019/lianggeskills) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/271498019) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Chinese-language task updates, reminder messages, status summaries, and supportive responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local task memory and reads a local quote library for emotional-support responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
