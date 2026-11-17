## Description:

Meeting Memory helps agents store, recall, and search meeting notes using BlueColumn persistent memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluecolumnconsulting-lgtm](https://clawhub.ai/user/bluecolumnconsulting-lgtm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add persistent meeting memory to agent workflows, including storing meeting summaries, quick notes, and recall queries for prior discussions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Meeting notes, summaries, and recall queries may be sent to and persisted by an external BlueColumn service.

Mitigation: Use only after confirming consent, retention, deletion, tenant isolation, and redaction practices for the meetings being stored.

Risk: Confidential, regulated, credential-bearing, or internal-only discussion content could be stored outside the user's intended trust boundary.

Mitigation: Avoid storing sensitive meeting content unless the deployment has approved data handling controls and redaction procedures.

## Reference(s):

- [BlueColumn API documentation](https://bluecolumn.ai/docs)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a BlueColumn API key and sends meeting note text, summaries, tags, and recall queries to BlueColumn endpoints.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
