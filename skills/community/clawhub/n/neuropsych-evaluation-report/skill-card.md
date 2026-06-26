## Description: <br>
Drafts comprehensive neuropsychological evaluation reports from clinician-provided intake data, behavioral observations, validity findings, test scores, interpretations, diagnostic formulation, and recommendations for licensed neuropsychologist review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[archlab-space](https://clawhub.ai/user/archlab-space) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Licensed neuropsychologists, post-doctoral fellows, and clinical neuropsychology trainees use this skill to organize neuropsychological intake information, test results, validity findings, interpretations, and recommendations into a draft report. The draft is intended for licensed doctoral-level neuropsychologist review and signature before release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Draft neuropsychological reports may contain preliminary diagnostic formulations or clinical recommendations that are not ready for release. <br>
Mitigation: Require review, correction, and signature by a licensed doctoral-level neuropsychologist before release to referral sources, patients, insurers, or other clinical users. <br>
Risk: Clinical inputs may include patient-identifying or regulated health information. <br>
Mitigation: Use initials plus case number only, avoid full names, dates of birth, and MRNs, and verify institutional HIPAA compliance and business associate agreement status before using external AI systems. <br>
Risk: Missing or invalid test scores can lead to misleading interpretations. <br>
Mitigation: Do not fabricate or estimate scores; preserve explicit placeholders for missing data and resolve open items from testing records before final review. <br>
Risk: Performance validity concerns can make subsequent cognitive interpretations unreliable. <br>
Mitigation: Gate interpretation on performance validity findings and include the required validity warning when any PVT fails or is atypical. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/archlab-space/neuropsych-evaluation-report) <br>
- [Open-Skill-Hub issues](https://github.com/archlab-space/Open-Skill-Hub/issues) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Text] <br>
**Output Format:** [Markdown draft report with labeled clinical sections, tables, warnings, open items, and a review block] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces draft clinical documentation only; missing scores remain as placeholders and diagnostic content is preliminary pending licensed review.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata and changelog, released 2026-05-31) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
