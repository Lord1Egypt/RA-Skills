## Description:

SMS Alert (smsalert.co.in). Use this skill for ANY SMS Alert request — reading, creating, and updating data. Whenever a task involves SMS Alert, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use the skill to read SMS Alert account information, manage OTP workflows, and send SMS messages through their connected OOMOL account. It provides live action schemas before constructing requests and marks message-sending actions as writes that require confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security assessment reports that setup runs unchecked downloads and the CLI may silently install additional agent skills.

Mitigation: Review the CLI installation separately and use a verified release. If only SMS functionality is needed, set OO_SKILLS_SYNC_DISABLED=1 to prevent startup skill writes.

Risk: Sending SMS or generating an OTP delivers a message and changes account state.

Mitigation: Confirm the exact recipient, message, and payload with the user before running a write action, and retain the user's confirmation.

Risk: The connected service processes SMS account credentials and request data.

Mitigation: Use the skill only with an SMS account and OOMOL connection the user trusts.

## Reference(s):

- [SMS Alert developer API documentation](https://kb.smsalert.co.in/developers-api/)
- [SMS Alert](https://www.smsalert.co.in/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON action results and shell commands, with setup and usage guidance in Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions that send messages are state-changing operations and require confirmation of the exact payload and effect.]

## Skill Version(s):

1.0.6 (source: frontmatter, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
