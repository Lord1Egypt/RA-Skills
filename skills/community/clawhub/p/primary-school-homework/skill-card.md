## Description: <br>
小学低年级作业管理助手。支持老师消息解析、睡前检查清单、错题拍照归档、每日闯关复习、每周错题总结（含表扬统计）、备考提醒、作业计时七个模式，适合1-3年级家长使用。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rickytsao-swordedge](https://clawhub.ai/user/rickytsao-swordedge) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Parents and caregivers of primary school students in grades 1-3 use this skill to organize teacher messages, homework checks, wrong-answer review, study reminders, and weekly learning summaries in chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Homework photos, teacher messages, and setup details may contain student names, school names, faces, addresses, class identifiers, or other child-related personal information. <br>
Mitigation: Redact student names, school names, faces, addresses, class identifiers, and anything not needed for the task before sending photos or messages. <br>
Risk: Wrong-answer records and child preferences may remain in chat or platform history after use. <br>
Mitigation: Keep records minimal, avoid sensitive details, and periodically review or delete chat history and stored study notes according to the family's privacy expectations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rickytsao-swordedge/primary-school-homework) <br>
- [Declared homepage](https://github.com/rickytsao-swordedge/primary-school-homework) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-style chat responses with task cards, checklists, wrong-answer records, practice questions, reminders, timing notes, and weekly summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use text or image inputs when the host model supports vision; outputs are intended for parent review before acting on homework or study guidance.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
