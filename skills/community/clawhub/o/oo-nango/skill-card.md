## Description:

Nango (nango.dev). Use this skill for ANY Nango request — reading, creating, updating, and deleting data. Whenever a task involves Nango, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use the OOMOL-connected Nango account to inspect connections, integrations, and providers, and to manage connection tags, metadata, or deletions through documented actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the oo CLI can affect other installed agent skills, and remote installer behavior was not verified.

Mitigation: Review the CLI and its effects before installation; do not treat the remote installer as verified.

Risk: Retrieving a Nango connection can return credential details.

Mitigation: Use a narrowly scoped Nango key, exclude credential-reading permissions unless needed, and handle returned connection details as secrets.

Risk: Write and destructive actions can change or remove connection data.

Mitigation: Keep the skill's approval steps for writes and deletions, and confirm the target and payload before execution.

## Reference(s):

- [Nango API authentication documentation](https://nango.dev/docs/reference/backend/http-api/authentication)
- [Nango homepage](https://nango.dev)
- [oo CLI on GitHub](https://github.com/oomol-lab/oo-cli)
- [Nango skill on ClawHub](https://clawhub.ai/oomol/skills/oo-nango)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, API Calls, Guidance]

**Output Format:** [Shell commands with JSON action payloads and JSON responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action inputs are checked against the live connector schema before use.]

## Skill Version(s):

1.0.6 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
