## Description: <br>
Provisions the Oracle ML inference daemon with onnxruntime via uv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to provision a local Oracle ONNX inference environment, verify the onnxruntime installation, and report whether the daemon can start in a later session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Setup creates a local Python virtual environment and downloads Python packages for ONNX inference. <br>
Mitigation: Run it only when that local inference environment is intended, uv is installed, and network package downloads are acceptable for the workspace. <br>


## Reference(s): <br>
- [Oracle plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/oracle) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports provisioning success or failure and suggests checking uv and network access when setup fails.] <br>

## Skill Version(s): <br>
1.9.12 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
