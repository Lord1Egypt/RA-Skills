## Description:

Keigo Mail Generator drafts Japanese business emails with appropriate honorific style, reusable local signature details, and optional internal template phrasing when requested.

This skill is ready for commercial/non-commercial use.

## Publisher:

[transmind](https://clawhub.ai/user/transmind)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and business users use this skill to draft polished Japanese business email for apologies, outreach, invitations, and other external communications. It can reuse locally stored signature details and optionally incorporate internal text templates when the user explicitly asks for template reference.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can save and reuse personal business signature details in a local SQLite database.

Mitigation: Install only when local signature persistence is acceptable, include only necessary contact fields, and use the documented rm flow to remove fields when no longer needed.

Risk: Broad mail-related activation can update or reuse signature details when a user did not intend that behavior.

Mitigation: Use narrow, intentional invocation text and review any signature update notice before relying on the generated email.

Risk: Generated business email may contain inaccurate, inappropriate, or legally unsuitable wording.

Mitigation: Review and edit drafts before sending, especially for apologies, contractual matters, customer communications, or regulated contexts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/transmind/skills/keigo-mail-generator)
- [README](README.md)
- [Demo video](https://www.youtube.com/watch?v=_UD1pcth0Dc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Plain text or Markdown email draft]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include a signature update notice before the draft when local signature storage changes.]

## Skill Version(s):

1.0.4 (source: ClawHub release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
