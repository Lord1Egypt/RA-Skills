## Description:

Automatically recommend ICD-10 diagnosis codes and CPT procedure codes from clinical notes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Healthcare providers, medical coders, and billing professionals use this skill to analyze clinical notes, patient encounter summaries, discharge summaries, and procedure reports for reviewable ICD-10-CM and CPT code recommendations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Clinical notes may contain protected health information or other sensitive patient data.

Mitigation: Install and run only in an environment approved for clinical data, and de-identify notes where possible before use.

Risk: Coding recommendations can affect billing, reimbursement, and documentation quality if accepted without review.

Mitigation: Treat outputs as review-only and require verification by a certified medical coder, healthcare provider, or other qualified reviewer before billing or chart changes.

Risk: Embedded code tables or guideline references may not reflect current ICD-10-CM, CPT, CMS/NCCI, payer, or organizational rules.

Mitigation: Verify recommendations against current official coding manuals, payer policy, CMS/NCCI edits, and organizational compliance requirements.

Risk: The release includes an unnecessary dataclasses dependency, increasing supply-chain exposure.

Mitigation: Remove or pin the dependency before installation when reducing supply-chain risk is required.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/skills/icd10-cpt-coding-assistant)
- [Clinical Coding Scenarios and Examples](references/code_examples.md)
- [Medical Coding Guidelines](references/coding_guidelines.md)
- [Common Clinical Condition Mappings](references/common_mappings.json)
- [Common CPT Codes](references/cpt_common_codes.json)
- [CPT Coding Guidelines](references/cpt_guidelines.md)
- [Common ICD-10 Codes](references/icd10_common_codes.json)
- [ICD-10-CM Official Coding Guidelines](references/icd10_guidelines.md)

## Skill Output:

**Output Type(s):** [text, JSON, guidance]

**Output Format:** [JSON or plain text coding recommendations with confidence scores, evidence snippets, alternatives, warnings, and a note summary.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are review-only and may include ICD-10-CM codes, CPT codes, confidence values, evidence snippets, alternatives, warnings, and summaries.]

## Skill Version(s):

0.1.0 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
