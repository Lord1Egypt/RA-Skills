## Description: <br>
Provisions the oracle ML inference daemon with onnxruntime via uv. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[athola](https://clawhub.ai/user/athola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to prepare the oracle plugin's local ONNX inference environment and verify that ONNX Runtime is installed before the daemon starts in a later session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup command creates a local Python environment, downloads ONNX Runtime, and imports oracle.provision code that is not included in the submitted artifact. <br>
Mitigation: Run it only from the expected plugins/oracle directory after confirming uv is installed, network access is intended, and the local oracle.provision implementation is trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/athola/skills/nm-oracle-setup) <br>
- [Oracle plugin homepage](https://github.com/athola/claude-night-market/tree/master/plugins/oracle) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes success or failure reporting guidance for the agent.] <br>

## Skill Version(s): <br>
1.9.13 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
