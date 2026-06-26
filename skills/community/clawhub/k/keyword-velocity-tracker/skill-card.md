## Description: <br>
Calculate literature growth velocity and acceleration to assess research. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research analysts use this skill to analyze keyword publication time series, estimate growth velocity and acceleration, classify research field maturity, and produce bounded trend forecasts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Dependency hygiene issues may affect local execution. <br>
Mitigation: Review, pin, or update dependencies before installation, and run the skill in an isolated environment. <br>
Risk: The script reads input files and can write output files in the workspace. <br>
Mitigation: Validate input and output paths before execution and restrict runs to an intended workspace. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/keyword-velocity-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, json, markdown, shell commands, guidance] <br>
**Output Format:** [JSON analysis results with optional Markdown guidance and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes keyword, analysis period, velocity and acceleration series, stage classification, confidence, trend, predictions, insights, assumptions, and validation caveats.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
