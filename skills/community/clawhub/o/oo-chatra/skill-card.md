## Description:

Chatra (chatra.com). Use this skill for any Chatra request, including reading, creating, updating, and deleting data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Support agents use this skill to retrieve Chatra visitor and message data, send or edit messages, update visitor records, and delete messages through a connected Chatra account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Fallback setup may execute a downloaded CLI installer without a separate approval step.

Mitigation: Review and verify the CLI release yourself, and require approval before any downloaded installer runs.

Risk: Connecting Chatra allows OOMOL to process account data.

Mitigation: Review the connection permissions and limit access to the account data needed for the task.

Risk: Write actions change Chatra data, and destructive actions remove messages.

Mitigation: Confirm the exact payload and effect before writes; explicitly approve the target before deletions.

## Reference(s):

- [Chatra](https://chatra.com/)
- [Chatra API documentation](https://chatra.com/help/api/#rest-api)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [oo CLI install guide](https://cli.oomol.com/install-guide.md)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON action payloads and Chatra action responses, with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetch the live action schema before building a payload; writes and deletions require user confirmation.]

## Skill Version(s):

1.0.2 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
