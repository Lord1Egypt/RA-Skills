## Description:

Paperless-ngx (docs.paperless-ngx.com). Use this skill for ANY Paperless-ngx request — reading, creating, updating, and deleting data. Whenever a task involves Paperless-ngx, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to search and manage documents, metadata, and other Paperless-ngx records through a user's connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the oo CLI runs downloaded code.

Mitigation: Review and explicitly approve installation from a verified, pinned release.

Risk: Profile actions may expose an API token to the agent.

Mitigation: Avoid profile actions until API tokens are filtered before reaching the agent.

Risk: Write and destructive actions can change or remove Paperless-ngx data.

Mitigation: Confirm the exact payload and effect before write actions, and get explicit approval for destructive actions.

## Reference(s):

- [Paperless-ngx documentation](https://docs.paperless-ngx.com)
- [Paperless-ngx API documentation](https://docs.paperless-ngx.com/api/)
- [oo CLI](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-paperless-ngx)

## Skill Output:

**Output Type(s):** [API calls, Shell commands, JSON, Guidance, Document and record data]

**Output Format:** [JSON action payloads and results, with Markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Action-dependent; some actions return document text or temporary file links.]

## Skill Version(s):

1.0.3 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
