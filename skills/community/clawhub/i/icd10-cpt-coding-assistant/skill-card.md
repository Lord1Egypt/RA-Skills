## Description: <br>
Automatically recommends ICD-10 diagnosis codes and CPT procedure codes from clinical notes for medical coding assistance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[AIPOCH-AI](https://clawhub.ai/user/AIPOCH-AI) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare providers, medical coders, billing professionals, and developers can use this skill to analyze clinical notes and draft ICD-10-CM and CPT code recommendations with confidence scores and supporting evidence. Recommendations are intended for qualified human review before billing, compliance, or clinical-documentation use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical notes may contain protected health information or other sensitive patient data. <br>
Mitigation: Use only with de-identified notes or in an environment with compliant PHI handling, access controls, and retention practices. <br>
Risk: Suggested ICD-10 or CPT codes may be incomplete, outdated, payer-specific, or unsuitable for billing. <br>
Mitigation: Treat all recommendations as drafts and verify codes, modifiers, payer rules, CMS guidance, and current AMA CPT materials with qualified coding or compliance staff. <br>
Risk: The skill provides coding assistance for medical documentation and could be mistaken for authoritative clinical or billing advice. <br>
Mitigation: Require human review by a certified medical coder or healthcare provider before relying on recommendations for reimbursement, audit, or compliance decisions. <br>


## Reference(s): <br>
- [ICD-10 Guidelines](references/icd10_guidelines.md) <br>
- [CPT Guidelines](references/cpt_guidelines.md) <br>
- [Coding Guidelines](references/coding_guidelines.md) <br>
- [Common ICD-10 Codes](references/icd10_common_codes.json) <br>
- [Common CPT Codes](references/cpt_common_codes.json) <br>
- [Common Clinical Mappings](references/common_mappings.json) <br>
- [Clinical Coding Examples](references/code_examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Text or JSON containing ICD-10 and CPT recommendations, confidence scores, evidence snippets, warnings, and note summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports configurable confidence thresholds and optional alternative code suggestions.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
