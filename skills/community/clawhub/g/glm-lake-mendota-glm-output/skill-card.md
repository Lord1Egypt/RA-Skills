## Description: <br>
Read and process GLM output files. Use when you need to extract temperature data from NetCDF output, convert depth coordinates, or calculate RMSE against observations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to read GLM NetCDF output, convert layer heights into depths from the water surface, compare simulated temperatures with observations, and calculate RMSE. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect local paths, missing Python packages, lake depth, or simulation start date can produce failed runs or misleading temperature and RMSE results. <br>
Mitigation: Verify NetCDF and observation file paths, install the required Python packages, and confirm lake depth plus the simulation start date against the local GLM configuration before using the example code. <br>
Risk: Treating GLM z values as surface depth instead of height from the lake bottom can invert the coordinate conversion and distort comparisons with observations. <br>
Mitigation: Use depth_from_surface = lake_depth - z and inspect matched datetime/depth counts before relying on calculated RMSE. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wu-uk/glm-lake-mendota-glm-output) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration guidance] <br>
**Output Format:** [Markdown with Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Examples assume local GLM NetCDF output, observation CSV files, Python data packages, and a lake depth value from glm3.nml.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
