## Description: <br>
家庭教育习惯养成追踪与教育付出记录系统，当用户提及习惯养成、坏习惯干预、记录孩子的行为变化、分析干预效果、教育付出总结、孩子内驱力建立等话题时激活，用于替代用户重复描述背景，直接进行习惯记录、分析和查询。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[silent404](https://clawhub.ai/user/silent404) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents or caregivers use this skill with an agent to record child habit formation, behavior interventions, caregiver contributions, and related education notes in a local SQLite database, then query or summarize progress. It also guides the agent to distinguish intrinsic-motivation habits from externally driven habits when offering practical parenting suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist sensitive child behavior, habit, intervention, and caregiver contribution records in a local database. <br>
Mitigation: Configure the database path for the user's own environment, restrict file permissions, and obtain explicit confirmation before creating or changing sensitive family records. <br>
Risk: Broad activation rules can cause the agent to record or query family data when the user only intended a general discussion. <br>
Mitigation: Confirm the requested operation and target habit before creating, updating, querying, merging, archiving, or deleting records. <br>
Risk: Parenting analysis and intervention summaries may be incomplete or misleading if based on sparse or subjective records. <br>
Mitigation: Present summaries as decision support, preserve the user's original context, and avoid replacing professional medical, psychological, or educational advice. <br>


## Reference(s): <br>
- [Database Schema Reference](references/schema.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/silent404/habit-education) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, Python helper calls, and SQLite-backed record summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, update, query, merge, archive, or delete local habit, intervention, and caregiver contribution records.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
