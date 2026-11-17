## Description:

Moosend (moosend.com). Use this skill for ANY Moosend request — reading, creating, and updating data. Whenever a task involves Moosend, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to read Moosend mailing lists and subscriber records, or add and update a subscriber through their connected Moosend account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The setup instructions allow remote CLI installation, and the CLI may install skills automatically.

Mitigation: Review and approve CLI installation separately, prefer a pinned and verified release, and review automatic skill installation; the vendor documents OO_SKILLS_SYNC_DISABLED as an opt-out.

Risk: The OOMOL service intermediates subscriber requests and manages connected Moosend credentials.

Mitigation: Use the skill only with an account connected through a trusted OOMOL account, and avoid handling raw credentials in agent commands.

Risk: Adding or updating a subscriber changes mailing-list data.

Mitigation: Confirm the exact subscriber payload and its effect with the user before running the write action.

## Reference(s):

- [oo CLI project](https://github.com/oomol-lab/oo-cli)
- [Moosend API authentication documentation](https://docs.moosend.com/api-documentation/articles/KnowledgeBase/54552-Authenticate-a-Moosend-API-request)
- [Moosend](https://www.moosend.com/)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read actions return Moosend account data; add_subscriber changes subscriber data after user confirmation.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
