## Description: <br>
PharmaClaw Pharmacology Agent profiles drug-candidate SMILES for ADME/PK properties, drug-likeness, descriptor-based risks, and follow-on pipeline recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheminempharmaclaw](https://clawhub.ai/user/cheminempharmaclaw) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research teams use this skill to turn SMILES strings into JSON pharmacology profiles covering Lipinski and Veber checks, QED, synthetic accessibility, ADME estimates, PAINS alerts, and recommended next agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports under-disclosed molecular data-sharing paths, which matters for proprietary or unpublished compounds. <br>
Mitigation: Review before installing in sensitive environments and use the local RDKit chain_entry path for confidential compounds. <br>
Risk: The ADMETlab path can submit molecular structures to a third-party service. <br>
Mitigation: Avoid admetlab3.py unless third-party submission is acceptable for the molecules being profiled. <br>
Risk: A neighboring pharmaclaw-lab-ui dashboard hook may receive pharmacology status updates if that directory exists. <br>
Mitigation: Inspect or remove the lab_hook dashboard integration before deployment where compound metadata should stay local. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cheminempharmaclaw/pcl-pharmacology-agent) <br>
- [ADME Prediction Rules Reference](references/api_reference.md) <br>
- [ADMETlab 3.0](https://admetlab3.scbdd.com) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Analysis, API Calls, Shell commands] <br>
**Output Format:** [JSON pharmacology profile with status, descriptors, ADME predictions, risks, recommendations, warnings, and timestamp.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SMILES input; the chain entry path returns success or error JSON, and the ADMETlab path may call ADMETlab 3.0 before falling back to RDKit-based predictions.] <br>

## Skill Version(s): <br>
2.0.1 (source: server release metadata; artifact changelog lists v2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
