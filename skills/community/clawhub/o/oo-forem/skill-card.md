## Description:

Forem (forem.com). Use this skill for ANY Forem request — reading, creating, and updating data. Whenever a task involves Forem, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use the skill to read Forem articles, comments, tags, and account data, and to create or update articles through their connected Forem account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup fallback may run downloaded installation code without verification or explicit approval.

Mitigation: Review and approve CLI setup separately, verify the downloaded code, and check its bundled-skill installation behavior before running it.

Risk: Connecting Forem gives OOMOL access to the account, and article creation or updates can change account content.

Mitigation: Retain the skill's explicit user-approval requirement for article creation and updates.

## Reference(s):

- [Forem API documentation](https://developers.forem.com/api/v1)
- [Forem homepage](https://www.forem.com)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON]

**Output Format:** [Forem content and structured JSON responses; article bodies may be Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Article creation and updates change Forem content and require user approval.]

## Skill Version(s):

1.0.5 (source: frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
