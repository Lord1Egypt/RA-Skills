## Description:

Use the OOMOL-connected SignWell account to read account, document, and template details, create documents from templates, and send documents or reminders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can access a connected SignWell account to retrieve account, document, and template information, create documents from templates, and send documents or reminders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The automatic setup fallback can install software on the user's system.

Mitigation: Review and approve CLI setup separately, and prefer a reviewed CLI version.

Risk: Startup skill synchronization may change other installed agent skills.

Mitigation: Consider setting OO_SKILLS_SYNC_DISABLED to prevent startup synchronization.

Risk: The connected OOMOL account provides access to SignWell account and document data, and write actions can create or send documents or reminders.

Mitigation: Use the intended connected account and retain confirmation of the exact payload and effect before document changes or sending.

## Reference(s):

- [SignWell](https://www.signwell.com)
- [SignWell API documentation](https://developers.signwell.com/reference/getting-started-with-your-api-1)
- [oo CLI](https://github.com/oomol-lab/oo-cli)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Shell commands, Guidance]

**Output Format:** [JSON payloads, command results, and Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Write actions require confirmation of the exact payload and effect before execution.]

## Skill Version(s):

1.0.5 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
