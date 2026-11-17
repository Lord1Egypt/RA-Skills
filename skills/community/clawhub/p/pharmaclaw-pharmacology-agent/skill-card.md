## Description:

Profiles drug candidates from SMILES by computing drug-likeness, ADME/PK descriptors and predictions, toxicity-related alerts, and downstream recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:


## Use Case:

Developers and cheminformatics researchers use this skill to turn a SMILES string into screening-oriented ADME/PK, drug-likeness, and risk outputs for lead optimization workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sensitive SMILES strings could disclose confidential research compounds if sent through the optional ADMETlab path.

Mitigation: Use the local chain_entry.py/RDKit path for sensitive molecules and only use scripts/admetlab3.py when external submission is acceptable.

Risk: ADME, toxicity, and drug-likeness outputs are screening predictions and may be incorrect or incomplete for scientific, clinical, or regulatory decisions.

Mitigation: Treat results as triage information and require expert review, validated assays, and appropriate regulatory evidence before acting on them.

## Reference(s):

- [ADME Prediction Rules Reference](references/api_reference.md)
- [ADMETlab 3.0](https://admetlab3.scbdd.com)
- [ClawHub Release Page](https://clawhub.ai/cheminem/skills/pharmaclaw-pharmacology-agent)

## Skill Output:

**Output Type(s):** [json, text, shell commands, guidance]

**Output Format:** [JSON pharmacology profiles with markdown guidance and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Accepts SMILES input and may include descriptor values, ADME predictions, toxicity alerts, risk flags, confidence, warnings, timestamps, and recommended next agents.]

## Skill Version(s):

2.0.0 (source: release metadata and changelog, released 2026-02-18)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
