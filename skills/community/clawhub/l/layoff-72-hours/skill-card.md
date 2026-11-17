## Description:

Urgent, time-boxed protocol for the first 72 hours after losing a job. Covers immediate document preservation, unemployment filing, health insurance decisions, emergency budgeting, severance review, and family communication. This is about stabilizing, not job searching.

This skill is ready for commercial/non-commercial use.

## Publisher:

[howtousehumans](https://clawhub.ai/user/howtousehumans)

### License/Terms of Use:

MIT-0

## Use Case:

External users who have recently lost a job, are about to lose a job, or are reviewing a severance agreement use this skill to stabilize the first 72 hours: preserve allowed personal records, file for unemployment, assess health insurance, create an emergency budget, and avoid rushed decisions.

### Deployment Geography for Use:

Global, with US-specific legal and benefits guidance that must be localized for non-US users.

## Known Risks and Mitigations:

Risk: The skill may encourage copying employer, client, vendor, CRM, address book, proprietary, or confidential records during urgent document preservation.

Mitigation: Limit preservation to personal employment, pay, benefits, and severance records; request records through HR when possible; avoid copying third-party, proprietary, or confidential information unless policy and legal obligations clearly allow it.

Risk: The skill may save or retain sensitive financial, health, and employment details in files or agent memory.

Mitigation: Ask before storing exact details, minimize or redact sensitive values, keep generated files in user-controlled storage, and delete retained details when they are no longer needed.

Risk: The skill contains US-specific legal and benefits guidance that may not apply to users in other jurisdictions.

Mitigation: Detect or ask for the user's jurisdiction, substitute local official programs and deadlines, warn when guidance has been localized, and recommend local employment lawyer review for severance agreements.

## Reference(s):

- [OWBPA review period, 29 U.S.C. 626(f)](https://www.law.cornell.edu/uscode/text/29/626)
- [COBRA election notice, 29 U.S.C. 1166(a)](https://www.law.cornell.edu/uscode/text/29/1166)
- [Healthcare.gov Special Enrollment Period](https://www.healthcare.gov/glossary/special-enrollment-period/)
- [CareerOneStop Unemployment Benefits Finder](https://www.careeronestop.org/LocalHelp/UnemploymentBenefits/unemployment-benefits.aspx)
- [Bureau of Labor Statistics Duration of Unemployment](https://www.bls.gov/cps/lfcharacteristics.htm)
- [CareerOneStop Local Help](https://www.careeronestop.org/LocalHelp/local-help.aspx)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files, Calendar reminders]

**Output Format:** [Conversational guidance with checklists, saved text files, and reminder suggestions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use email, calendar, and filesystem tools when available; includes session state fields for layoff triage progress.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
