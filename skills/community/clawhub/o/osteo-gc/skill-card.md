## Description: <br>
Models BMD T-score trajectories and 10-year fracture risk in chronic glucocorticoid users with uncertainty estimates and ACR 2022 treatment guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CryptoReuMD](https://clawhub.ai/user/CryptoReuMD) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Healthcare professionals, researchers, and clinical decision-support developers can use this skill to model glucocorticoid-induced osteoporosis risk, project site-specific T-score trajectories, and review guideline-based monitoring or treatment considerations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical modeling outputs may be mistaken for medical advice or definitive treatment recommendations. <br>
Mitigation: Use outputs as decision-support only and verify medication choices, steroid tapering, fracture-risk interpretation, and guideline alignment with a licensed clinician. <br>
Risk: Incorrect patient inputs can materially change projected T-score trajectories and fracture-risk categories. <br>
Mitigation: Confirm glucocorticoid dose, duration, baseline T-scores, fracture history, and other risk factors before relying on the report. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/CryptoReuMD/osteo-gc) <br>
- [CryptoReuMD publisher profile](https://clawhub.ai/user/CryptoReuMD) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, guidance] <br>
**Output Format:** [Python module output and plain-text clinical modeling reports that an agent may summarize in Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Runs locally with Python 3.8+ standard library only; Monte Carlo projections vary with patient inputs, simulation count, and random seed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
