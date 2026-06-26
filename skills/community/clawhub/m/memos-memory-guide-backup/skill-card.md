## Description: <br>
Use the MemOS Lite memory system to search and use the user's past conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[andy27725](https://clawhub.ai/user/andy27725) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to decide when and how to search a user's long-term conversation memory, retrieve full task summaries or learned experience guides, expand context around a memory hit, and provide access to a memory viewer when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables broad searches over long-term conversation memory, which can expose sensitive user history if invoked without clear intent. <br>
Mitigation: Require explicit user confirmation before sensitive memory searches and keep generated search queries short and purpose-specific. <br>
Risk: The skill can guide agents to retrieve and install learned skills for future sessions. <br>
Mitigation: Require confirmation before any skill_install action and review retrieved skill content before allowing it to persist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/andy27725/memos-memory-guide-backup) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/andy27725) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Text, API Calls] <br>
**Output Format:** [Markdown guidance with tool-call names and decision flow] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides memory_search, task_summary, skill_get, skill_install, memory_timeline, and memory_viewer usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
