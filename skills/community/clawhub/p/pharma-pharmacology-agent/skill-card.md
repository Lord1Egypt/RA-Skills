## Description: <br>
Pharmacology agent for ADME/PK profiling of drug candidates from SMILES, including drug-likeness rules, QED, SA Score, rule-based ADME predictions, PAINS alerts, and chemistry-query chaining. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and research teams use this skill to profile candidate molecules from SMILES strings and produce structured ADME, drug-likeness, and risk-triage outputs for downstream chemistry workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Rule-based pharmacology estimates can be misleading if treated as clinical, regulatory, or safety-critical conclusions. <br>
Mitigation: Use the output for research triage only and require expert review and validated assays before medical, clinical, regulatory, or safety decisions. <br>
Risk: The bundled Python script depends on a trusted local RDKit setup and optional RDKit components for some checks. <br>
Mitigation: Run it in a controlled Python environment with a trusted RDKit installation and review warnings or missing optional checks in the JSON output. <br>


## Reference(s): <br>
- [ADME Prediction Rules Reference](references/api_reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/Cheminem/pharma-pharmacology-agent) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, guidance] <br>
**Output Format:** [JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a SMILES string or chained chemistry-query output and returns descriptors, rule-based ADME predictions, risk flags, recommended next agents, confidence, warnings, and a timestamp.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and skill changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
