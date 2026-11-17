## Description:

EmailListVerify (emaillistverify.com). Use this skill for ANY EmailListVerify request — reading, creating, updating, and deleting data. Whenever a task involves EmailListVerify, use this skill instead of calling the API directly.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oomol](https://clawhub.ai/user/oomol)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill through their OOMOL-connected account to verify individual email addresses, check disposable domains, and manage batch email lists. It can also retrieve credits and list progress or download and delete completed lists.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A routine email request may trigger execution of a downloaded CLI installer without a separate approval or verification step.

Mitigation: Review and approve CLI installation separately using a verified release; installer contents were unavailable for inspection.

Risk: Batch verification uploads email-list data to EmailListVerify, and list deletion removes data.

Mitigation: Share only intended email data through OOMOL, and retain the required upload and deletion approvals.

Risk: The oo CLI may automatically synchronize skills.

Mitigation: Consider disabling automatic skill synchronization with the publisher-documented OO_SKILLS_SYNC_DISABLED setting.

## Reference(s):

- [EmailListVerify API documentation](https://www.emaillistverify.com/api)
- [EmailListVerify homepage](https://emaillistverify.com/)
- [oo CLI documentation and source](https://github.com/oomol-lab/oo-cli)
- [ClawHub skill page](https://clawhub.ai/oomol/skills/oo-emaillistverify)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Guidance, Shell commands]

**Output Format:** [JSON action results and Markdown guidance with inline oo CLI commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses depend on the selected EmailListVerify action.]

## Skill Version(s):

1.0.5 (source: frontmatter, server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
