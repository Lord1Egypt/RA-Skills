## Description: <br>
Detects local file content types using the Google Magika CLI and deep learning model. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose and run Magika commands for identifying single files, MIME types, directories, batches, and confidence-scored classifications. It is useful when inspecting uploaded or workspace files by content rather than filename extension. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Recursive or batch scans read local file contents in the selected path to classify them. <br>
Mitigation: Run scans only on files and folders the user intends to inspect, especially when using recursive options. <br>
Risk: The documented curl install option runs a remote install script. <br>
Mitigation: Prefer pipx, pip, or brew installation when possible, and inspect any remote script before executing it. <br>


## Reference(s): <br>
- [Openclaw Magika on ClawHub](https://clawhub.ai/axelhu/openclaw-magika) <br>
- [Google Magika install script](https://securityresearch.google/magika/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Magika JSON or JSONL command examples; actual file classification output is produced locally by the magika CLI.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
