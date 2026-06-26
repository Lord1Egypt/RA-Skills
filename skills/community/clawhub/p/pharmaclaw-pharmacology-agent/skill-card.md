## Description: <br>
PharmaClaw profiles drug candidates from SMILES strings with ADME/PK descriptors, drug-likeness scores, toxicity alerts, and pharmacology risk flags. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Cheminem](https://clawhub.ai/user/Cheminem) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and drug discovery teams use this agent to screen candidate molecules from SMILES strings before downstream toxicology, literature, or IP-expansion work. It is intended for early pharmacology triage and lead-optimization support, not as a clinical or regulatory decision system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Molecule strings may be sent to the external ADMETlab service when using scripts/admetlab3.py. <br>
Mitigation: Use scripts/chain_entry.py for confidential or proprietary molecules, or run the ADMETlab helper only after confirming external submission is acceptable. <br>
Risk: Pharmacology and toxicity predictions are screening estimates and can be wrong or incomplete. <br>
Mitigation: Review outputs with qualified scientific judgment and confirm important findings with validated assays, regulatory workflows, or domain-specific review. <br>
Risk: The skill executes local Python chemistry tooling and depends on packages such as RDKit and requests. <br>
Mitigation: Install in a controlled environment, review dependencies, and scan the skill before deployment. <br>


## Reference(s): <br>
- [ADME Prediction Rules Reference](references/api_reference.md) <br>
- [ADMETlab 3.0](https://admetlab3.scbdd.com) <br>
- [PharmaClaw Pharmacology Agent on ClawHub](https://clawhub.ai/Cheminem/pharmaclaw-pharmacology-agent) <br>
- [Cheminem publisher profile](https://clawhub.ai/user/Cheminem) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON reports and Markdown guidance with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs include canonical SMILES, descriptor tables, ADME predictions, risk flags, recommendations for downstream agents, confidence, warnings, and timestamps.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and skill changelog, released 2026-02-18) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
