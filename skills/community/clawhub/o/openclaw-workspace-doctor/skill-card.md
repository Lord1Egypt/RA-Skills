## Description: <br>
Diagnoses and helps repair nested OpenClaw workspace directory issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maxkandel99-arch](https://clawhub.ai/user/maxkandel99-arch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to diagnose workspace path and configuration problems, detect recursively nested `.openclawworkspace` directories, and receive cautious repair steps such as dry-run fixes and backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Workspace repair scripts may change or delete files if run without review. <br>
Mitigation: Inspect the scripts first, back up relevant configuration, verify every path, and run dry-run mode before approving any repair. <br>


## Reference(s): <br>
- [OpenClaw Workspace Health Scripts](https://github.com/maxkandel99-arch/workspace-health) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommends dry-run mode, backups, and user confirmation before file-changing repairs.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
