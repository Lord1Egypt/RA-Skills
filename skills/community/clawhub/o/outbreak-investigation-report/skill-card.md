## Description:

Use this skill when a field epidemiologist, EIS officer, communicable-disease nurse, or public-health investigator needs to draft a CDC Field Epi Manual-aligned outbreak-investigation report for supervising epidemiologist review.

This skill is ready for commercial/non-commercial use.

## Publisher:

[archlab-space](https://clawhub.ai/user/archlab-space)

### License/Terms of Use:

MIT-0

## Use Case:

Public-health investigators, field epidemiologists, communicable-disease nurses, environmental-health specialists, and hospital infection preventionists use this skill to draft de-identified outbreak or cluster investigation reports from supplied investigation data. The skill structures the draft around CDC field epidemiology steps, analytical-study documentation, control-measure records, communication specifications, limitations, action items, and supervisory review requirements.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste direct personal identifiers or protected health information into the drafting workflow.

Mitigation: The skill instructs users to redact names, addresses, dates of birth, medical record numbers, Social Security numbers, phone numbers, emails, exact GPS coordinates, and photos; it uses case IDs and de-identified summaries throughout.

Risk: A draft report could be mistaken for an official public-health decision, public communication, clinician alert, or outbreak closure.

Mitigation: The skill repeatedly labels outputs as drafts for supervising medical epidemiologist or jurisdictional designee review and states that it does not authorize control measures, issue public communications, or declare an outbreak over.

Risk: Incomplete or unsupported investigation data could lead to misleading counts, case definitions, hypotheses, or analytical results.

Mitigation: The workflow asks one intake question at a time, logs unresolved information, requires case definitions before counts, requires line-list export dates for figures, and forbids inferential statistics unless the user supplies the needed data.

Risk: Sensitive bioterrorism or select-agent scenarios could produce inappropriate public-content drafts.

Mitigation: The skill instructs the agent to flag immediate FBI or federal SOC referral and stop drafting public-content specifications while continuing investigation documentation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/archlab-space/skills/outbreak-investigation-report)
- [Feedback and contributions](https://github.com/archlab-space/Open-Skill-Hub/issues)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown draft report with structured sections and tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes a draft banner, edit log, confidentiality self-check, small-cell suppression reminder, and de-identified case IDs.]

## Skill Version(s):

0.1.1 (source: server release evidence and changelog, released 2026-05-28)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
