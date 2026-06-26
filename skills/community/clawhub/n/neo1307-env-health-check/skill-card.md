## Description: <br>
Inspect environment variables, critical directories, and write permissions, then produce a health report for deployment readiness and local runtime checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check required environment variables and directory write access before running local or deployment workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generated report can disclose the names of checked environment variables and absolute directory paths. <br>
Mitigation: Pass only environment variable names and directory paths that are acceptable to include in a local report. <br>
Risk: The --out path creates or overwrites a local report file. <br>
Mitigation: Choose an output path that is safe to create or overwrite before running the check. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/neo1307/neo1307-env-health-check) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Text] <br>
**Output Format:** [Markdown report file with JSON console summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports OK/WARN/FAIL status for user-specified environment variable names and directories.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence and skill.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
