## Description:

A Chinese-language private-domain operations assistant that drafts outreach content, diagnoses customer-growth workflows, checks current vendor and platform information, and supports client notes and follow-up reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maojiebc](https://clawhub.ai/user/maojiebc)

### License/Terms of Use:

MIT

## Use Case:

Chinese-speaking operators and business owners use the skill to plan private-channel customer growth, draft social posts and group messages, assess vendor choices using current sources, and carry conclusions across consultations with client records and reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local client records are unencrypted plain text and may contain sensitive business or personal information.

Mitigation: Use redacted storage and review reports before sharing; manage access to local records.

Risk: Restore and report actions can select a customer based on the working directory, and drafting may reuse that customer's saved context.

Mitigation: Specify the customer explicitly for restore and report tasks, and opt out of saved-context reuse when it is not wanted.

Risk: A requested update downloads and runs an unpinned installer and changes globally available project skills.

Mitigation: Review the update source before requesting an update.

## Reference(s):

- [ClawHub release](https://clawhub.ai/maojiebc/skills/majia-siyu)
- [Project documentation](https://github.com/maojiebc/majia-siyu-team)
- [Answer verification guide](references/回答核验.md)
- [Private-domain operating blueprint](references/整盘怎么搭-老板版.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese prose and Markdown drafts, plans, checklists, client notes, and reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content is tailored to the user's business context; current external claims should include supporting sources.]

## Skill Version(s):

2.1.1 (source: frontmatter, server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
