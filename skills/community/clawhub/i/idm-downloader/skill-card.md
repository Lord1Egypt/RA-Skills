## Description: <br>
Downloads large files through Internet Download Manager (IDM) on Windows using COM automation or IDM's command-line interface. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxcatt](https://clawhub.ai/user/foxcatt) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill when they want an agent to start IDM downloads for user-provided URLs on Windows, especially for large files where IDM resume and acceleration are useful. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can start an IDM download immediately and write downloaded content to disk. <br>
Mitigation: Confirm the URL, filename, and save directory before running the skill, and use it only for intended downloads. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May start IDM immediately and report download status or failure through console output and process exit code.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
