## Description: <br>
Prediction and forecasting system for trends, outcomes, and risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ProjectSnowWork](https://clawhub.ai/user/ProjectSnowWork) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to structure trend forecasts, scenario planning, probability estimates, and risk assessments while keeping local records of forecast runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill materially overstates its forecasting abilities. <br>
Mitigation: Treat outputs as a lightweight forecasting checklist and require reviewed analysis logic before using it for business, financial, safety, or risk decisions. <br>
Risk: Forecast helper runs can retain local forecast records. <br>
Mitigation: Review or delete ~/.openclaw/workspace/memory/predict when retained forecast records are no longer wanted. <br>
Risk: Several workflows described by the skill reference helper scripts that are not present in the artifact. <br>
Mitigation: Review installed files before relying on scenario generation, risk assessment, probability evaluation, accuracy tracking, or model-building workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and local JSON recordkeeping] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Forecast helper output is advisory and can retain local forecast records under ~/.openclaw/workspace/memory/predict.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
