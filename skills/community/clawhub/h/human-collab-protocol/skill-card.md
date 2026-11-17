## Description:

Helps a user prepare and follow up on meetings or one-to-one conversations by asking clarifying questions, drafting a shared Context Card, creating a private collaboration prompt, and summarizing meeting output.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nonvnet-ux](https://clawhub.ai/user/nonvnet-ux)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and external collaborators use this skill to prepare shared meeting context, clarify intended decisions, and turn Feishu meeting notes into confirmed outputs, task assignments, Context Card updates, and local meeting memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated Context Cards or post-meeting Outputs may omit nuance or misstate decisions, owners, or deadlines.

Mitigation: Review and confirm generated Context Cards and Outputs before allowing Feishu document updates, task creation, or local memory writes.

Risk: Confirmed follow-up actions can create or update Feishu documents and assigned tasks.

Mitigation: Install only for workflows where Feishu meeting preparation and follow-up are intended, and keep user confirmation as the gate before external changes.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/nonvnet-ux/skills/human-collab-protocol)
- [人机协作协议 v1.0](https://www.feishu.cn/docx/JSFIdBEVeoo6mYxdlCNcmnxHnxb)
- [落地操作手册 v1.0](https://www.feishu.cn/docx/VG9qdaLwroC2kMx027Sc6X12nrb)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Plain text meeting artifacts and follow-up summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are separated into a participant-facing Context Card, a user-private collaboration prompt, and a confirmed post-meeting output with decisions, open questions, updates, and task follow-up.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
