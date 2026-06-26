## Description: <br>
Calculates a weighted composite score predicting adverse pregnancy outcomes in patients with SLE and/or APS to support risk stratification and management planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoReuMD](https://clawhub.ai/user/CryptoReuMD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Clinicians and clinical teams can use this skill as supervised decision support for estimating pregnancy risk in SLE and/or APS patients and planning monitoring intensity. It should not be used to make pregnancy, medication, monitoring, or delivery decisions without qualified MFM/rheumatology review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: High-stakes pregnancy, medication, monitoring, or delivery recommendations may be clinically inappropriate if used without specialist oversight. <br>
Mitigation: Use only as clinician-supervised decision support and require qualified MFM/rheumatology review before acting on scores or recommendations. <br>
Risk: Patient identifiers or clinical factors may expose health data when entered into the local tool or shared in generated reports. <br>
Mitigation: Avoid real patient identifiers unless operating in an approved health-data environment; prefer anonymous IDs and control report storage. <br>


## Reference(s): <br>
- [PREGNA-RISK ClawHub listing](https://clawhub.ai/CryptoReuMD/pregna-risk) <br>
- [Artifact documentation](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Clinical risk report text or JSON, with Markdown documentation and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a composite score, risk category, recommendation, monitoring timeline, and Monte Carlo confidence interval.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
