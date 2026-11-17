## Description:

Get Biji (biji.com). Use this skill for ANY Get Biji request — reading, creating, updating, and deleting data. Whenever a task involves Get Biji, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

People using an OOMOL-connected Get Biji account can ask an agent to find and read notes, save and organize content, manage knowledge bases, or update, share, and remove notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Initial setup may execute remote installer code whose effects were unavailable for inspection, and CLI synchronization can introduce broader agent changes.

Mitigation: Review and install the CLI separately, inspect its agent-skill synchronization settings, and approve any additional host changes before setup.

## Reference(s):

- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [Get Biji](https://www.biji.com/)
- [Get Biji API documentation](https://doc.biji.com/docs/WOxgwObNNiyMHWk1dl0cJqSxnEd/)

## Skill Output:

**Output Type(s):** [API Calls, Text, Guidance]

**Output Format:** [Shell commands with JSON payloads; Get Biji results returned as JSON and summarized in text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Link and image saves may return asynchronous task identifiers.]

## Skill Version(s):

1.0.7 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
