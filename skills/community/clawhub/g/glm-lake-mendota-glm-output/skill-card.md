## Description:

Read and process GLM output files. Use when you need to extract temperature data from NetCDF output, convert depth coordinates, or calculate RMSE against observations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wu-uk](https://clawhub.ai/user/wu-uk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and lake-modeling analysts use this skill to read GLM NetCDF output, convert height coordinates to depth from surface, and compare simulated temperatures with observations using RMSE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect lake depth or coordinate conversion can produce misleading temperature comparisons.

Mitigation: Confirm the lake_depth value from glm3.nml and convert GLM z coordinates with lake_depth - z before comparing with observations.

Risk: Example code reads local NetCDF and CSV files supplied by the user.

Mitigation: Review file paths and input datasets before running the code examples.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown guidance with Python code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [None]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
