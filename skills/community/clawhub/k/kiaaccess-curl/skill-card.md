## Description:

Query and command a Kia vehicle directly with curl against the Kia Owners API (api.owners.kia.com), without running the MCP server. Use when the user wants a one-off read of their Kia's status, location, or EV charge state, or to lock/unlock/start climate from the shell — "check my Kia", "is the car locked", "what's the EV9 charge", "lock the car from the terminal". Requires KIA_USERNAME/KIA_PASSWORD and a one-time SMS/email MFA bootstrap.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrischall](https://clawhub.ai/user/chrischall)

### License/Terms of Use:

MIT-0

## Use Case:

Vehicle owners and developers can use one-off shell requests to read a Kia vehicle's status, location, and EV charge information, or to carry out a specifically requested remote action such as locking the doors or starting climate control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Temporary files may expose account credentials, refresh tokens, or vehicle responses.

Mitigation: Use a private temporary directory with restrictive permissions and clean it up; protect the saved refresh token as an account credential.

Risk: Vehicle-control examples can trigger unintended actions if run without checking the target and requested operation.

Mitigation: Verify the target vehicle and run only the explicitly requested command; do not execute combined examples wholesale.

## Reference(s):

- [Ready-to-run requests](references/requests.md)
- [Kia Owners API](https://api.owners.kia.com/apigw/v1)

## Skill Output:

**Output Type(s):** [Shell commands, API calls, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON/jq examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses account credentials and a saved refresh token; vehicle commands should be limited to the user's explicit request.]

## Skill Version(s):

2.1.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
