## Description: <br>
为重要会议制作结构化的会前材料（HTML网页 + 腾讯文档），用于整理背景信息、议程、待确认事项和沟通策略。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Monica8825](https://clawhub.ai/user/Monica8825) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external collaborators use this skill to prepare structured meeting briefs from meeting details, user-provided files, and public research. It produces background summaries, agenda and issue analysis, action checklists, communication strategy notes, and optional Tencent Docs sync for live meeting notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting briefs may include confidential, regulated, personal, or competitively sensitive information from user-provided files and meeting context. <br>
Mitigation: Use only materials the user is authorized to share, keep sensitive content scoped to the intended meeting, and review the brief before distribution. <br>
Risk: Optional Tencent Docs sync sends generated brief content and any attachment-derived information to an external service. <br>
Mitigation: Enable Tencent Docs sync only when the user deliberately requests it and has confirmed the destination is appropriate for the meeting materials. <br>
Risk: Online research and extracted document content can be stale, incomplete, or uncertain. <br>
Mitigation: Retain source notes and uncertainty labels, cross-check important facts, and mark unresolved items as待确认 before using the brief in a meeting. <br>


## Reference(s): <br>
- [HTML Template Guide](references/html-template-guide.md) <br>
- [Meeting Prep HTML Template](assets/meeting-prep-template.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/Monica8825/meeting-prep-brief) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [HTML brief, optional Markdown/Tencent Docs content, and concise setup or preview instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May process user-provided meeting materials and can optionally sync generated content to Tencent Docs when the user has configured the required token.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
