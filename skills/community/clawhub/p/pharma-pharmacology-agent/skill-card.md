## Description:

Pharmacology agent for ADME/PK profiling of drug candidates from SMILES, including drug-likeness rules, QED, SA Score, ADME predictions, PAINS alerts, and chaining from chemistry-query input.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cheminem](https://clawhub.ai/user/cheminem)

### License/Terms of Use:


## Use Case:

Developers and cheminformatics users use this agent to profile drug-candidate SMILES strings for ADME/PK properties, drug-likeness, PAINS alerts, and rule-based pharmacology risks before chaining results to toxicology or IP workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Rule-based ADME and drug-likeness results may be mistaken for validated clinical, safety, regulatory, or medical advice.

Mitigation: Treat outputs as approximate screening heuristics and require qualified review before using results for clinical, safety, regulatory, or medical decisions.

Risk: Automatic recommendations to continue into toxicology or IP workflows could pass preliminary pharmacology results downstream too broadly.

Mitigation: Keep downstream chaining to toxicology or IP workflows under explicit user control and review the JSON output before invoking follow-on agents.

## Reference(s):

- [ADME Prediction Rules Reference](references/api_reference.md)

## Skill Output:

**Output Type(s):** [JSON, analysis, guidance]

**Output Format:** [Structured JSON with descriptors, rule checks, ADME predictions, risk flags, warnings, confidence, and recommended next agents.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces success and error responses as JSON; results are rule-based heuristics and should not be treated as clinical, safety, regulatory, or medical advice.]

## Skill Version(s):

1.1.0 (source: release evidence and artifact changelog, released 2026-02-14)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
