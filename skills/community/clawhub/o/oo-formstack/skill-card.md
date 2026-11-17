## Description:

Formstack (formstack.com). Use this skill for ANY Formstack request — reading, creating, updating, and deleting data. Whenever a task involves Formstack, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

Formstack users can retrieve forms, fields, and submissions, or create, update, and delete submissions through an OOMOL-connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup can run unverified downloads and introduce broader changes to agent skills; the remote installer and connector code were not verified.

Mitigation: Review setup, install a verified CLI release yourself, consider disabling automatic skill synchronization with OO_SKILLS_SYNC_DISABLED, and retain approval for changes and deletions.

## Reference(s):

- [Formstack](https://www.formstack.com/)
- [Formstack API documentation](https://developers.formstack.com/reference/api-overview)
- [oo CLI environment variables and controls](https://github.com/oomol-lab/oo-cli/blob/main/docs/commands.md#environment-variables)
- [Formstack skill release](https://clawhub.ai/oomol/skills/oo-formstack)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text, Guidance]

**Output Format:** [Structured JSON action results and natural-language summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Results may contain Formstack form and submission data. Writes require confirmation; updates and deletions can overwrite or remove data.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
