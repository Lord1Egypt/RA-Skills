## Description:

OsmO lets an AI place and manage real phone calls, handle inbound calls, and return call summaries, transcripts, and recordings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[getosmo](https://clawhub.ai/user/getosmo)

### License/Terms of Use:

MIT-0

## Use Case:

People use this skill to ask an AI to call businesses or contacts, manage eligible scheduled calls and call-backs, and review the outcome of calls. It previews the recipient and call request for user confirmation before dialing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Calls and their related information are handled by OsmO's hosted service; the security scan does not establish what data the service handles.

Mitigation: Review OsmO's privacy information and avoid sharing sensitive details unless comfortable with the service's handling of them.

Risk: A call reaches a real person and may make a request or change on the user's behalf.

Mitigation: Before dialing, show the recipient's name and number and the exact request OsmO will make; place the call only after the user confirms.

## Reference(s):

- [OsmO](https://getosmo.app)

## Skill Output:

**Output Type(s):** [API Calls, Text, Configuration instructions]

**Output Format:** [MCP tool requests and returned call summaries, transcripts, and recording links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Call request reason is limited to 300 characters, context to 700 characters, and a request can include up to five recipients; features depend on the account plan.]

## Skill Version(s):

1.1.0 (source: frontmatter, ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
