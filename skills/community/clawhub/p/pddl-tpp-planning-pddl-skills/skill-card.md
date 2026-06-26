## Description: <br>
Automated Planning utilities for loading PDDL domains and problems, generating plans using classical planners, validating plans, and saving plan outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lnj22](https://clawhub.ai/user/lnj22) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and planning practitioners use this skill to load PDDL domain and problem files, generate sequential classical plans, validate plan correctness, and save plan outputs for benchmark or automation workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Untrusted or unpinned planning dependencies can affect planning behavior in the local environment. <br>
Mitigation: Install only trusted planning dependencies, preferably pinned versions, in an isolated project environment. <br>
Risk: Saving plans to a user-specified output path can overwrite an existing file. <br>
Mitigation: Use project-local output directories and review the output path before saving plan files. <br>
Risk: Invalid or mismatched PDDL domain and problem files can produce parse errors, failed planning, or invalid plans. <br>
Mitigation: Check that problem files reference the correct domain and validate every generated plan before relying on it. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Files] <br>
**Output Format:** [Markdown with Python code examples and PDDL plan text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save plan output to a user-specified local path; validation returns boolean status.] <br>

## Skill Version(s): <br>
0.1.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
