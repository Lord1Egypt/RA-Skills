## Description:

PharmaClaw Pharmacology Agent profiles drug candidates from SMILES with drug-likeness, ADME/PK, toxicity, and PAINS risk outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminempharmaclaw](https://clawhub.ai/user/cheminempharmaclaw)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and drug-discovery teams use this skill to profile candidate molecules from SMILES strings, inspect ADME/PK and drug-likeness signals, and route results to downstream toxicology or IP-expansion agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Molecule structures may be sent to ADMETlab and, when present, a local dashboard hook.

Mitigation: Use explicit network opt-in for confidential work and run the skill with limited network access unless external prediction services are approved.

Risk: The skill loads an undeclared sibling dashboard module during execution.

Mitigation: Remove or pin the dashboard hook import before deployment and run the skill in a sandbox with limited filesystem access.

Risk: ADME, toxicity, and drug-likeness outputs are predictive screening signals, not validated clinical or regulatory conclusions.

Mitigation: Require expert review and independent validation before using outputs for candidate selection or downstream scientific decisions.

## Reference(s):

- [ADME Prediction Rules Reference](artifact/references/api_reference.md)
- [ADMETlab 3.0](https://admetlab3.scbdd.com)
- [ADMETlab 3.0 evaluation endpoint](https://admetlab3.scbdd.com/service/evaluation)
- [ClawHub skill page](https://clawhub.ai/cheminempharmaclaw/skills/pcl-pharmacology-agent)

## Skill Output:

**Output Type(s):** [JSON, Analysis, Guidance]

**Output Format:** [JSON object with molecular descriptors, ADME predictions, risk flags, warnings, confidence, and recommended next agents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMILES input; may use ADMETlab 3.0 when available and otherwise falls back to RDKit-based prediction logic.]

## Skill Version(s):

2.0.1 (source: server release evidence; artifact changelog lists v2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
