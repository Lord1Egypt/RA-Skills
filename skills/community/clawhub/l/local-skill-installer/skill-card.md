## Description: <br>
Install a local OpenClaw skill from a zip file by unzipping, validating, moving it into the active Skills directory, and verifying the result. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[LeiAlexZhang](https://clawhub.ai/user/LeiAlexZhang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to install a local skill package from a Linux-accessible zip file into the active Skills directory while checking required files and avoiding overwrite conflicts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Installing an untrusted local zip can persist instructions that influence future agent behavior. <br>
Mitigation: Install only trusted zip files, inspect the extracted SKILL.md and metadata before moving the folder, and confirm the destination path. <br>
Risk: A target skill folder conflict could overwrite or obscure an existing local skill. <br>
Mitigation: Stop when the destination folder already exists and report the conflict instead of overwriting. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with installation status fields and inline shell commands when needed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports the source zip path, extracted skill folder name, final installed path, validation result, conflict result, and reload or restart recommendation.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
