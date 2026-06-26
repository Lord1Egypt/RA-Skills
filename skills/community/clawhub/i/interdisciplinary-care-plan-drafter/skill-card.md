## Description: <br>
Drafts CMS Conditions of Participation-compliant interdisciplinary care plan documentation for hospice and palliative care teams, including goals of care, comfort care planning, IDT roles, visit frequencies, and compliance flags for licensed clinician and IDT review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Hospice and palliative care clinicians and interdisciplinary team coordinators use this skill to assemble draft ICP documentation from clinician-led assessments, goals-of-care information, comfort care plans, discipline assignments, visit schedules, and open compliance items. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft care plan content could be mistaken for finalized clinical documentation, medical orders, or billing-ready material. <br>
Mitigation: The skill labels outputs as draft documentation and requires licensed clinician and IDT review and co-signature before care delivery, medical record entry, or Medicare or Medicaid billing use. <br>
Risk: Sensitive patient information could be entered into the conversation. <br>
Mitigation: The skill instructs users to collect only patient initials and a case reference and not to record full names, dates of birth, MRNs, addresses, or insurance numbers. <br>
Risk: Generated symptom, prognosis, code status, or compliance language could be incomplete or clinically misleading. <br>
Mitigation: The skill requires clinician-supplied assessments, flags uncontrolled symptoms and CMS CoP gaps, avoids generating prognoses or orders, and directs POLST/MOLST and medication decisions to the appropriate clinical workflow. <br>
Risk: Security review confidence is limited by the supplied scan context. <br>
Mitigation: Install with normal caution and review the README and SKILL.md for data handling, requested commands, network behavior, credential use, and background behavior before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/interdisciplinary-care-plan-drafter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Structured Markdown draft care plan, role and visit-frequency table, open-items checklist, and review note] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only clinical documentation; requires licensed clinician and IDT review before care delivery, medical record entry, or billing use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and CHANGELOG.md, released 2026-06-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
