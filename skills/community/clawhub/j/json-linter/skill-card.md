## Description: <br>
Validates JSON syntax across the workspace. Use this skill to check for syntax errors in configuration files, memory files, or data assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wanng-ide](https://clawhub.ai/user/wanng-ide) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to recursively check JSON files in a workspace or target directory and get a syntax report for configuration, memory, and data files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads JSON files recursively from the selected directory, which can include private configuration, secrets, or data files if run from a broad workspace. <br>
Mitigation: Run it from the intended project directory or pass --dir to limit the scan scope before reviewing the generated JSON report. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [JSON report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports scan time, root directory, file counts, and parse error details for invalid JSON files.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
