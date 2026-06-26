## Description: <br>
Generate structured meeting minutes from templates, sync to Feishu, and track action items. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external collaborators use this skill to turn meeting context into structured Chinese meeting minutes, including agenda, decisions, open issues, and action items. It can also support Feishu document creation and local follow-up tracking when those workflows are appropriate. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting notes may contain confidential or sensitive information and can be sent to Feishu during sync. <br>
Mitigation: Review meeting content before sync, use local Markdown-only output for confidential meetings, and confirm the separate feishu-doc skill is approved for the workspace. <br>
Risk: Action items may be retained locally for follow-up. <br>
Mitigation: Review saved action items and avoid storing sensitive names, deadlines, or decisions in local memory when retention is not appropriate. <br>


## Reference(s): <br>
- [Meeting minutes template](references/template.md) <br>
- [ClawHub skill listing](https://clawhub.ai/terrycarter1985/meeting-minutes-cn) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown meeting minutes with tables, optional Feishu document creation command, and optional action-item checklist.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create a Feishu document through a separate Feishu skill and may append action items to memory/YYYY-MM-DD.md.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
