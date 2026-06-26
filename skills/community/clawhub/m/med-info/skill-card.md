## Description: <br>
Label-backed medication answers with citations and traceable IDs for RxCUI, NDC, SPL set_id, label sections, and optional recalls, shortages, FAERS, and interactions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[DuncanDobbins](https://clawhub.ai/user/DuncanDobbins) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Employees, external users, developers, and agents use this skill to retrieve medication summaries grounded in public labels and identifiers for notes, training, QA, internal documentation, or automated workflows. It is not medical advice and clinical decisions should be verified against the full official label. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Medication summaries can be incomplete or unsuitable for clinical decisions if used without checking the complete source label. <br>
Mitigation: Use the output as reference support only and verify clinical decisions against the full official label. <br>
Risk: Drug names, identifiers, or optional API keys may be sent to public medical APIs, and public reference datasets may be stored in a local cache. <br>
Mitigation: Do not enter patient-specific information or PHI; provide OPENFDA_API_KEY only when higher openFDA rate limits are needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/DuncanDobbins/med-info) <br>
- [openFDA drug label API](https://open.fda.gov/apis/drug/label/) <br>
- [RxNav RxNorm API](https://lhncbc.nlm.nih.gov/RxNav/APIs/) <br>
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest) <br>
- [Resource catalog](artifact/docs/RESOURCES.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown-style CLI output or machine-readable JSON with source identifiers, citations, and optional queried URLs.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include RxCUI, NDC, SPL set_id, effective dates, source links, selected label sections, and opt-in public safety context.] <br>

## Skill Version(s): <br>
0.2.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
