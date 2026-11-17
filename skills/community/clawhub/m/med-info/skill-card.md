## Description:

Label-backed medication answers with citations and traceable IDs. RxCUI/NDC/set_id, key label sections, optional recalls/shortages/FAERS/interactions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[duncandobbins](https://clawhub.ai/user/duncandobbins)

### License/Terms of Use:


## Use Case:

External users, developers, and agent workflows use this skill to look up medication label information by drug name, RxCUI, NDC, or SPL set_id and produce citation-backed summaries for notes, training, QA, and internal documentation. It is not medical advice and should be verified against the full official label for clinical decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: An optional openFDA API key can be exposed in command output if an HTTP error occurs.

Mitigation: Use the skill without OPENFDA_API_KEY unless higher rate limits are required; avoid CI or agent logs with a configured key unless error handling is patched to redact the key.

Risk: Medication information can be incomplete, stale, or inappropriate for clinical decision-making when used without source review.

Mitigation: Verify clinical decisions against the full official label and do not treat the output as medical advice.

Risk: Queries or logs may include sensitive health information if users enter patient-specific details.

Mitigation: Query only by drug name or identifiers and do not enter PHI.

Risk: Optional dataset features may fetch and cache public files, and the hazardous-drug path may invoke pdftotext.

Mitigation: Review optional flags before use in restricted environments and ensure local cache and helper binaries meet deployment policy.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/duncandobbins/skills/med-info)
- [openFDA Drug Label API](https://open.fda.gov/apis/drug/label/)
- [RxNav RxNorm API](https://lhncbc.nlm.nih.gov/RxNav/APIs/)
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)

## Skill Output:

**Output Type(s):** [text, markdown, json, shell commands, guidance]

**Output Format:** [Markdown-style CLI output with optional JSON for pipelines]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include citations, RxCUI/NDC/SPL identifiers, effective dates, source URLs, label sections, and opt-in safety context.]

## Skill Version(s):

0.2.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
