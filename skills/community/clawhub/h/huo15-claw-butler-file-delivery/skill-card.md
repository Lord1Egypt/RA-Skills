## Description:

Delivers user-requested files to a paired 龙虾管家 (Claw Butler) desktop or mobile client through the client file.push capability when normal WebChat file delivery is unsupported.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaobod1](https://clawhub.ai/user/zhaobod1)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks to receive, open, download, save, or export a file produced during a task. It guides reliable delivery to a paired Claw Butler client and helps avoid failed WebChat file sends or dead local-path links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An agent could push arbitrary local files instead of files the user asked to receive.

Mitigation: Use the skill only for user-requested files or files created during the current task.

Risk: Large-file URL delivery can expose sensitive data if the upload target is not approved.

Mitigation: Get explicit approval before uploading sensitive large files to external storage for URL-based delivery.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, JSON parameters, API calls, guidance]

**Output Format:** [Markdown guidance with JSON invocation parameters]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces agent-facing delivery guidance for small-file base64 pushes and large-file URL handoff.]

## Skill Version(s):

1.0.0 (source: release evidence and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
