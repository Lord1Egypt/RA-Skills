## Description: <br>
Pharmaclaw Tox Agent screens SMILES strings with RDKit descriptors, Lipinski and Veber rules, QED scoring, and simplified PAINS alerts to produce a local drug-safety risk report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Drug discovery developers and researchers use this skill to run early local screening of candidate molecules from SMILES strings and produce a property, rule-violation, PAINS, and risk summary for downstream review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The screening output could be mistaken for authoritative toxicology, clinical, regulatory, or drug-safety advice. <br>
Mitigation: Use it only as an early local heuristic and require qualified scientific, toxicology, regulatory, and experimental validation before making drug-safety decisions. <br>
Risk: Confidential compound structures may be exposed if SMILES strings are passed to downstream agents, logs, or external systems. <br>
Mitigation: Keep sensitive structures local where required and review downstream pipeline data handling before sharing SMILES or generated reports. <br>
Risk: The PAINS and toxicity coverage is incomplete, including a simplified PAINS set and no Ames, hERG, LD50, or comprehensive QSAR prediction. <br>
Mitigation: Treat flags and non-flags as limited screening signals, and use fuller PAINS catalogs, specialized models, assays, and expert review for comprehensive safety assessment. <br>
Risk: Installing an unverified chemistry dependency can introduce supply-chain risk. <br>
Mitigation: Verify the RDKit package source and pin trusted dependency versions before installation or execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Shell commands, Code] <br>
**Output Format:** [JSON report with concise Markdown and shell-command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a SMILES string and returns descriptor values, rule-violation counts, QED score, simplified PAINS count, and a Low or Medium/High risk label.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
