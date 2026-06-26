## Description: <br>
Use this skill when a clinician, biller, or practice manager needs to look up ICD-10 diagnosis codes, CPT procedure codes, or E&M visit level codes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[optimusprime19](https://clawhub.ai/user/optimusprime19) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External clinicians, billers, and practice managers use this skill to generate candidate ICD-10-CM, CPT, and E&M billing codes from de-identified clinical descriptions, then review denial, coding-level, and superbill guidance before qualified human approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: AI-assisted billing code suggestions may be incorrect or insufficiently supported for claim submission. <br>
Mitigation: Require review and approval by a qualified medical coder or clinician before billing or claim submission. <br>
Risk: Clinical prompts could expose PHI if users paste patient identifiers. <br>
Mitigation: Use only de-identified clinical descriptions and do not include names, MRNs, DOBs, addresses, or other patient-identifiable information. <br>
Risk: Optional CMS API use may send billing code pairs to an external CMS endpoint. <br>
Mitigation: Verify CMS_API_KEY use and confirm that only code pairs, not clinical text or PHI, are transmitted. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/optimusprime19/medical-billing-coder) <br>
- [Source homepage](https://github.com/optimusprime19/medical-billing-coder) <br>
- [CMS Medicare Coverage Database API](https://api.cms.gov/medicare-coverage-database/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with billing code suggestions, confidence notes, validation findings, and review warnings] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include ICD-10-CM, CPT, E&M, modifier, denial-risk, reimbursement, and superbill guidance for qualified human review.] <br>

## Skill Version(s): <br>
1.0.3 (source: evidence.release.version and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
