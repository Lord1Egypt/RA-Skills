## Description: <br>
Fetches and analyzes openFDA FAERS adverse event data and ClinicalTrials.gov study data for drug safety, trial pipeline, and market intelligence workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to query public post-market safety reports and clinical trial records for drugs, compounds, conditions, and competitive landscape research. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Drug names, SMILES strings, and conditions are sent to public openFDA, PubChem, and ClinicalTrials.gov endpoints. <br>
Mitigation: Use the skill only when public endpoint disclosure is acceptable, and avoid proprietary compounds or sensitive research queries unless disclosure has been approved. <br>
Risk: Report filenames are built from user-provided queries and may be unsafe or confusing when queries contain unusual characters. <br>
Mitigation: Run the skill in a constrained workspace, choose an explicit safe output directory, and review generated filenames before relying on or sharing outputs. <br>
Risk: The release metadata under-discloses the ClinicalTrials.gov workflow. <br>
Mitigation: Review the clinical trial querying behavior and expected public API calls before deployment. <br>


## Reference(s): <br>
- [FAERS Fields Reference](references/faers_fields.md) <br>
- [ClinicalTrials.gov API v2 Reference](references/clinicaltrials_fields.md) <br>
- [openFDA Drug Event API](https://open.fda.gov/apis/drug/event/) <br>
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api) <br>
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Analysis] <br>
**Output Format:** [JSON summaries, PNG charts, and status text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports and visualizations to a user-selected output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
