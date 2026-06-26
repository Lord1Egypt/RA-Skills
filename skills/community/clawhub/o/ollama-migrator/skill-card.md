## Description: <br>
Helps users migrate Ollama model files from the C: drive to another disk, check storage usage, set the model path, and verify the moved models. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jjflydudu](https://clawhub.ai/user/jjflydudu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and local Ollama users use this skill when Ollama models consume too much C: drive space and need to be moved to another disk. It guides status checks, migration, environment variable updates, verification with Ollama, and optional cleanup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The cleanup option can delete the original model directory even when migration verification fails. <br>
Mitigation: Run the status check and migration steps first, verify the new model path with `ollama list` and a test model run, and avoid `--cleanup` until the moved models work or a backup exists. <br>
Risk: The migration changes local Ollama configuration and service state. <br>
Mitigation: Review the migration plan before confirming, expect Ollama to be stopped during migration, and open a new terminal after environment variable changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jjflydudu/ollama-migrator) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline PowerShell and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Windows-focused migration steps, status checks, environment variable updates, and cleanup guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
