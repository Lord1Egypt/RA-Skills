## Description:

Use Monica CRM through an OOMOL-connected account to read and search contacts and notes, and to create, update, or delete notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People managing relationships in Monica CRM can use an agent to look up contacts and notes, search records, and manage notes. Confirm the exact effect before creating, updating, or deleting CRM data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback runs remote installer code without requiring separate user approval.

Mitigation: Review and explicitly approve CLI installation before using the fallback; prefer a verified fixed release.

Risk: The OOMOL connector mediates access to private CRM data, and its hosted implementation was not verified.

Mitigation: Use an account with appropriate access and retain explicit confirmation before creating, updating, or deleting CRM data.

## Reference(s):

- [Monica CRM](https://www.monicahq.com/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, JSON, API responses, Shell commands, Guidance]

**Output Format:** [CLI commands with JSON payloads and text or JSON action results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports contact and note lookups, searches, and note creation, updates, and deletion.]

## Skill Version(s):

1.0.5 (source: artifact frontmatter, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
