## Description:

httpSMS (httpsms.com). Use this skill for ANY httpSMS request — reading, creating, updating, and deleting data. Whenever a task involves httpSMS, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected httpSMS account can inspect phones, message threads, messages, and billing usage, and can send or delete messages through the httpSMS service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs a downloaded CLI installer without a separate approval step, and the remote installer was not verified.

Mitigation: Install a verified CLI release yourself and prevent the agent from running the automatic installer fallback.

Risk: The connected service can access private messages and perform send or delete actions.

Mitigation: Keep confirmation enabled for every send and deletion, and review requested access to the connected account.

Risk: The hosted connector implementation was not verified.

Mitigation: Check the CLI's bundled-skill synchronization settings before use.

## Reference(s):

- [httpSMS API documentation](https://docs.httpsms.com/)
- [httpSMS homepage](https://httpsms.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, Guidance]

**Output Format:** [oo CLI commands with JSON payloads and JSON connector responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Connector responses include an execution ID.]

## Skill Version(s):

1.0.4 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
