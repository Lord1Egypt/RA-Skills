## Description: <br>
Calibrate GLM parameters for water temperature simulation. Use when you need to adjust model parameters to minimize RMSE between simulated and observed temperatures. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and lake modelers use this skill to tune General Lake Model parameters, compare simulated and observed water temperatures, and reduce RMSE during calibration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The sample calibration workflow modifies glm3.nml and runs the local glm command, which could overwrite model settings or invoke an unexpected executable. <br>
Mitigation: Back up glm3.nml, confirm glm resolves to the expected local GLM binary, and run the workflow from the intended model directory before using the sample optimization code. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wu-uk/glm-lake-mendota-glm-calibration) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, configuration] <br>
**Output Format:** [Markdown with tables and Python code examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides calibration parameter ranges, manual adjustment guidance, common issue diagnosis, and sample optimization code.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
