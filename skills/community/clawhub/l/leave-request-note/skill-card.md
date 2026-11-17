## Description:

请假条 helps users draft school leave notes and workplace leave requests, including common leave types, attachment reminders, written follow-up after verbal requests, and basic date-span checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[po-et](https://clawhub.ai/user/po-et)

### License/Terms of Use:

MIT-0

## Use Case:

Students, employees, and agents assisting them use this skill to prepare concise leave-note or leave-request drafts, one-line system reasons, and attachment checklists. It is intended for drafting and process reminders, not for legal, medical, HR entitlement, proof-document, or approval decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may rely on the draft as legal, HR, school-policy, or leave-entitlement advice.

Mitigation: Verify school or employer rules with the relevant handbook, teacher, HR team, union, labor authority, or legal professional before acting on entitlement, pay, approval, absence, or contract questions.

Risk: Users may include unnecessary medical or other sensitive personal details in a leave request.

Mitigation: Keep reasons concise, avoid unnecessary medical detail, and attach only documents required by the school or employer.

Risk: Date-span calculations may not account for public holidays, adjusted workdays, or local attendance rules.

Mitigation: Use the calculation only as a basic check and manually reconcile it against the applicable calendar, attendance system, and institution policy.

Risk: The skill could be misused to create or alter proof documents.

Mitigation: Use it only to draft request text and attachment reminders; do not create, modify, or fabricate proof documents.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/po-et/skills/leave-request-note)
- [Artifact Skill Definition](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with fill-in templates, concise prose, checklists, and optional inline bash command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes bracketed placeholders for missing user details; date spans depend on user-provided dates and require manual holiday or adjusted-workday verification.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
