## Description:

Use JSONBin.io to read, create, update, and delete JSON data through an OOMOL-connected account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to read and manage JSONBin.io records through a connected OOMOL account. It supports creating bins, reading records, replacing stored data, and deleting bins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include a remote CLI installer that could run unverified code without separate approval.

Mitigation: Review setup before use, install a verified CLI version yourself, and check its automatic skill synchronization before allowing agent use.

Risk: The connected OOMOL service mediates JSONBin requests and holds access to the connected API key.

Mitigation: Use the connection only if you trust OOMOL with that access.

Risk: Creating, replacing, or deleting stored data can change or remove JSONBin content.

Mitigation: Keep explicit user approval for write and deletion actions, including review of the exact payload or target.

## Reference(s):

- [JSONBin.io API documentation](https://jsonbin.io/api-reference)
- [oo CLI project](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, Shell commands, JSON data, Guidance]

**Output Format:** [Shell commands and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results depend on the selected action and may include records or action metadata.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
