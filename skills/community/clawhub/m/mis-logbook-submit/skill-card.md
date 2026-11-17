## Description:

Submit a daily PENS MIS Kerja Praktek logbook entry at online.mis.pens.ac.id after an approval-first workflow that gathers same-day work evidence, drafts Indonesian activity text, logs in with local secrets, saves the entry, and verifies the saved row.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mozaldy](https://clawhub.ai/user/mozaldy)

### License/Terms of Use:

MIT-0

## Use Case:

External users with authorized PENS MIS access use this skill to prepare an evidence-grounded Indonesian activity summary and submit an approved daily Kerja Praktek logbook entry.

### Deployment Geography for Use:

Global, for authorized PENS MIS users.

## Known Risks and Mitigations:

Risk: The skill uses stored MIS credentials to access a live account and submit live logbook data.

Mitigation: Install only when this credential use is acceptable, keep secrets outside the skill folder, and never echo credentials in chat or workspace files.

Risk: The security scan calls out incomplete validation of the exact login.pens.ac.id HTTPS origin before credential entry.

Mitigation: Harden the login flow to require the expected HTTPS origin before entering credentials.

Risk: The submission script can modify live MIS records.

Mitigation: Require explicit runtime confirmation before reading credentials or submitting, and keep the approval-first and duplicate-entry checks in place.

## Reference(s):

- [Daily MIS logbook workflow](references/workflow.md)
- [PENS MIS](https://online.mis.pens.ac.id)
- [PENS CAS login](https://login.pens.ac.id/cas/login)
- [ClawHub skill page](https://clawhub.ai/mozaldy/skills/mis-logbook-submit)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance, Configuration]

**Output Format:** [Markdown guidance, stdin activity text, and JSON status from the submission script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local MIS credentials and explicit user approval before live submission.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
