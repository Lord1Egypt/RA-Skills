## Description: <br>
Calculate the relative contribution of different factors to a response variable using R² decomposition. Use when you need to quantify how much each factor explains the variance of an outcome. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wu-uk](https://clawhub.ai/user/wu-uk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, data analysts, and developers use this skill to estimate how groups of factors explain variance in a response variable and identify the dominant contributor. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The example output writes only the dominant contribution row, which can make a partial result look complete. <br>
Mitigation: Write all contribution rows and clearly label any dominant-factor summary. <br>
Risk: The example writes to output.csv and could overwrite an existing local file. <br>
Mitigation: Choose an explicit output path and check for existing files before writing. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, files] <br>
**Output Format:** [Markdown guidance with Python code blocks and a CSV output example] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local example output.csv content; review generated code and filenames before use.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
