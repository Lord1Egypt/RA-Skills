## Description:

Generates structured meeting minutes, tracks decisions and follow-ups, and syncs the rendered minutes to Feishu documents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terrycarter1985](https://clawhub.ai/user/terrycarter1985)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and team facilitators use this skill to turn meeting context into standardized minutes, decisions, follow-ups, and a Feishu document link for collaboration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting content is synced to Feishu by default, which can expose confidential discussions if the destination or document permissions are wrong.

Mitigation: Confirm the target Feishu document, recipients, and sharing permissions before syncing confidential or sensitive meeting notes.

Risk: Shell-command examples use meeting titles, Markdown content, and document IDs that may originate from users.

Mitigation: Pass user-controlled values through a safe argument API or validated parameters instead of raw shell interpolation.

## Reference(s):

- [Feishu Sync Guide](references/feishu-sync.md)
- [Minutes Sync on ClawHub](https://clawhub.ai/terrycarter1985/skills/minutes-sync)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown meeting minutes with action tables, checklist follow-ups, Feishu sync status, and a document link.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Missing meeting details are marked as [待补充]; Feishu sync depends on configured document tooling and permissions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
