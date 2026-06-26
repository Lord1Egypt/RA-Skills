## Description: <br>
将口语化任务转为结构化工单并自动保存，助力会议记录和待办事项整理办公自动化。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linyao58](https://clawhub.ai/user/linyao58) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Office staff and agents use this skill to turn informal task notes, meeting summaries, and todo descriptions into saved work-ticket text files for follow-up. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves whatever office text the user provides into a persistent exports folder. <br>
Mitigation: Use it only for notes that are acceptable to store as files, and avoid passwords, regulated data, confidential meeting details, or personal information unless the storage location and retention policy are approved. <br>
Risk: Generated work tickets may preserve raw informal instructions that need human review before follow-up. <br>
Mitigation: Review generated ticket files before using them as authoritative task records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linyao58/office-auto) <br>


## Skill Output: <br>
**Output Type(s):** [text, files] <br>
**Output Format:** [Plain text status message and UTF-8 text work-ticket file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates timestamped Task_*.txt files under ./data/exports.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
