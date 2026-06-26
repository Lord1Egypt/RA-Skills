## Description: <br>
A human-agent collaboration protocol skill that helps a user prepare for meetings or one-to-one communications, share a concise Context Card with participants, and follow up on Feishu meeting notes with decisions, open questions, task assignments, and document updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nonvnet-ux](https://clawhub.ai/user/nonvnet-ux) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees and external collaborators use this skill to prepare shared meeting context, clarify decision goals, and turn Feishu meeting records into confirmed follow-up outputs. It is intended for communication workflows where the user remains responsible for confirming shared documents, task owners, deadlines, and final decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Meeting context, transcript links, task assignments, deadlines, and document updates may expose private or organization-sensitive information if shared too broadly. <br>
Mitigation: Review Context Card content, transcript access, task assignees, deadlines, document updates, and memory storage before confirming actions; notify participants and follow local law and organization policy before recording meetings or sharing transcript links. <br>
Risk: Incorrectly extracted decisions or unclear meeting notes could create misleading follow-up tasks or document changes. <br>
Mitigation: Require user confirmation of Context Card content and follow-up Output before creating Feishu tasks, updating documents, or recording meeting output. <br>


## Reference(s): <br>
- [Human-Agent Collaboration Protocol on ClawHub](https://clawhub.ai/nonvnet-ux/human-collab-protocol) <br>
- [Human-Agent Collaboration Protocol v1.0](https://www.feishu.cn/docx/JSFIdBEVeoo6mYxdlCNcmnxHnxb) <br>
- [Implementation Manual v1.0](https://www.feishu.cn/docx/VG9qdaLwroC2kMx027Sc6X12nrb) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Plain text templates for Context Cards, collaboration prompts, and meeting follow-up outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Context Card and follow-up Output content require user confirmation before Feishu document, task, or memory updates.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
