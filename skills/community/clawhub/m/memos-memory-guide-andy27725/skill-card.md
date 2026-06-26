## Description: <br>
Guides an agent to use MemOS Lite memory tools to search and apply a user's past conversations, preferences, task summaries, and related memory context. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents and developers use this skill when a user asks about prior chats, preferences, task history, or stored memory. It helps the agent decide when to search memory, fetch task summaries, inspect surrounding conversation context, or open the memory viewer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent to search broad long-term conversation memory, which may surface sensitive or unrelated prior context. <br>
Mitigation: Limit memory searches to the current task and require confirmation before relying on sensitive or ambiguous recalled information. <br>
Risk: The skill describes persistent skill installation through skill_install without an explicit approval boundary. <br>
Mitigation: Require explicit user approval before any skill_install action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/memos-memory-guide-andy27725) <br>
- [Publisher profile: andy27725](https://clawhub.ai/user/andy27725) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance with tool-call decision flows] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes when to use memory_search, task_summary, skill_get, skill_install, memory_timeline, and memory_viewer.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
