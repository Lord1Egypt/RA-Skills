## Description: <br>
Generates a professional package.json with standard scripts, dependencies, and configuration best practices. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers use this skill to create a starter package.json for Node.js projects with common scripts, semantic versioning, and dependency organization guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The generator writes package.json in the current directory and can overwrite an existing file. <br>
Mitigation: Run it only in the intended project directory and inspect or back up any existing package.json before execution. <br>
Risk: Name and version values are written directly into JSON. <br>
Mitigation: Use simple trusted name and version values and inspect the generated JSON before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/package-json-generator) <br>


## Skill Output: <br>
**Output Type(s):** [Files, JSON, Shell commands, Configuration] <br>
**Output Format:** [A generated package.json file with shell command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes package.json in the current working directory and may overwrite an existing file.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/_meta.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
