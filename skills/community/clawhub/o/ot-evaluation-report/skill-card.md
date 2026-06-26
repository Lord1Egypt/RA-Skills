## Description: <br>
Drafts an initial Occupational Therapy evaluation report from clinician-provided data, aligned to AOTA OTPF-4 and CMS Medicare documentation requirements, and labels the output for licensed OT review and sign-off. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Licensed Occupational Therapists, supervised OTAs, OT students, and rehabilitation documentation specialists use this skill to turn intake notes, occupational profile details, ADL/IADL observations, standardized assessment scores, and clinician impressions into a structured draft OT evaluation report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft OT documentation could be mistaken for a finalized clinical record or payer-ready report. <br>
Mitigation: Keep the output labeled as a draft and require licensed OT review, editing, dating, and signature before record entry or submission. <br>
Risk: Patient identifiers or other PHI may be included in source notes. <br>
Mitigation: Use initials and placeholders in the working draft, remove direct identifiers, and call out substitutions for clinician review. <br>
Risk: The server security evidence marks the bundle suspicious because it includes privileged maintainer workflows. <br>
Mitigation: Install only when those workflows are expected, require explicit approval for production or account-impacting actions, and run nested review tooling without full-access automation unless intentionally approved. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown draft evaluation report with structured sections and tables] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Draft-only output requiring licensed OT review and sign-off before medical record, school record, or payer submission.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata and changelog, released 2026-05-28) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
