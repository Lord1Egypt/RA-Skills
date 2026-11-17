## Description:

Calibrate GLM parameters for water temperature simulation. Use when you need to adjust model parameters to minimize RMSE between simulated and observed temperatures.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and environmental modelers use this skill to tune GLM lake-model parameters and reduce RMSE between simulated and observed water temperatures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The calibration example mutates glm3.nml during optimization.

Mitigation: Run calibration only in an intended project directory and keep a backup of GLM configuration files before optimization.

Risk: The guidance assumes GLM is installed and available to the agent environment.

Mitigation: Confirm GLM is installed before following generated calibration commands or code.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wu-uk/skills/glm-lake-mendota-glm-calibration)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with tables and Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include suggested GLM parameter ranges and example optimization logic.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
