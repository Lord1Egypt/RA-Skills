## Description:

Fetches and analyzes FAERS data from openFDA, resolves SMILES through PubChem, and generates drug safety event lists, yearly trends, top reactions, and top outcomes as JSON summaries and PNG charts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to gather post-market safety and clinical trial landscape summaries for drugs, including adverse event trends, reactions, outcomes, sample reports, and trial status or phase summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Path-like drug names can influence generated output filenames and may write files outside the intended output folder.

Mitigation: Use only trusted drug names or resolved names, avoid path separators and path-like input, and run the skill in a disposable workspace until filename sanitization is fixed.

Risk: The skill queries public biomedical APIs and writes result files locally.

Mitigation: Review generated JSON and PNG outputs before using them for market, safety, or competitive decisions, and keep generated files separate from important workspace data.

## Reference(s):

- [FAERS Fields Reference](artifact/references/faers_fields.md)
- [ClinicalTrials.gov API v2 Reference](artifact/references/clinicaltrials_fields.md)
- [openFDA Drug Event API](https://open.fda.gov/apis/drug/event/)
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, files]

**Output Format:** [Markdown guidance with inline shell commands; generated artifacts are JSON summaries and PNG charts.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Queries public biomedical APIs and writes local result files under the requested output directory when inputs are safe.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
