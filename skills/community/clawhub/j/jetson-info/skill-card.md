## Description: <br>
Queries NVIDIA Jetson device model, JetPack, L4T, CUDA, cuDNN, TensorRT, serial number, and hardware specifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wxd9199](https://clawhub.ai/user/wxd9199) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to inspect local NVIDIA Jetson hardware and software version details during setup, support, inventory, or troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local Jetson reports may include a device serial number or other identifying hardware information. <br>
Mitigation: Review and redact hardware and software details before sharing output outside the intended environment. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown with inline shell commands and local device information summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output may include local Jetson hardware identifiers, software versions, and device serial number when jetson_release is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
