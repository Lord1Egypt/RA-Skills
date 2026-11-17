## Description:

Gives AI agents persistent memory for Gmail thread context using BlueColumn storage and recall endpoints.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill when an agent manages Gmail and needs to store, recall, or search thread history through BlueColumn persistent memory.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send and persist Gmail-derived summaries in an external BlueColumn memory service.

Mitigation: Use it only with approval to share that email context with BlueColumn, and redact secrets, personal data, financial terms, and confidential thread details before storage.

Risk: The skill documentation does not provide deletion or retention guidance for stored thread summaries.

Mitigation: Confirm retention and deletion procedures with BlueColumn documentation or support before storing sensitive or regulated email context.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration]

**Output Format:** [Markdown with inline bash code blocks and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends Gmail-derived summaries to an external memory service.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
