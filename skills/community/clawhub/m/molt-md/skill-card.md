## Description:

Cloud-hosted markdown collaboration for agents and humans. One API call to create, one link to share. End-to-end encrypted, no account required.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bndkts](https://clawhub.ai/user/bndkts)

### License/Terms of Use:


## Use Case:

Agents, developers, and human collaborators use this skill to create, read, update, and share cloud-hosted Markdown documents and workspaces through molt-md's API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected Markdown content is sent to molt-md's cloud API.

Mitigation: Upload only content appropriate for the service and avoid credentials, confidential local context, or regulated data unless separately approved.

Risk: Returned document and workspace keys grant access, and write keys grant modification rights.

Mitigation: Store write keys in a dedicated secret store and keep them out of generic agent memory, plaintext config, logs, and transcripts.

Risk: The security summary flags encryption claims that do not match the documented API examples.

Mitigation: Do not rely on the encryption claim for sensitive workflows without an independent review of the service security model.

Risk: Remotely re-fetched skill text could differ from the reviewed artifact.

Mitigation: Treat the reviewed artifact as authoritative and review any newly fetched skill text before following it.

Risk: Lost document or workspace keys cannot be recovered.

Mitigation: Save required IDs and keys immediately in approved secret storage.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bndkts/skills/molt-md)
- [molt-md API documentation](https://github.com/bndkts/molt-md/blob/main/API.md)
- [molt-md website](https://molt-md.com)
- [molt-md skill documentation](https://molt-md.com/skill.md)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, API calls, Configuration, Guidance]

**Output Format:** [Markdown guidance with curl examples and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires external API access; returned document and workspace keys are high-value secrets; documents and workspaces expire after 30 days of inactivity.]

## Skill Version(s):

1.1.1 (source: server release metadata and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
