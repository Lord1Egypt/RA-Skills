## Description:

Atomic node skill to share a file in Google Drive using the gog CLI.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zvirb](https://clawhub.ai/user/zvirb)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill when a user asks to share a specific Google Drive file or folder with a named recipient or make it public. It guides the agent to form a gog CLI sharing command and expect a JSON permission confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change Google Drive sharing permissions and may expose files or folders if the target, recipient, sharing type, or role is wrong.

Mitigation: Require confirmation of the exact file or folder, recipient or public sharing type, and permission role before running gog.

Risk: The schema example grants writer access even though the directive uses reader access.

Mitigation: Default to reader access and use writer only when the user explicitly requests write permission.

## Reference(s):


## Skill Output:

**Output Type(s):** [shell commands, guidance, json]

**Output Format:** [Markdown instructions with an inline gog command and a JSON output expectation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Google Drive file or folder ID, sharing type, role, and recipient email when user-based sharing is requested.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
