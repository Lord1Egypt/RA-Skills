## Description: <br>
Copy a local file into Google Drive for desktop so it can be downloaded from a phone when the phone is not on the same LAN, with size and SHA256 verification after copy. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[neo1307](https://clawhub.ai/user/neo1307) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to relay a specific local file into Google Drive for desktop when direct phone access to the PC or local network is unavailable, then verify the copied file by size and SHA256. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can copy local files into Google Drive, which may expose unintended or sensitive data. <br>
Mitigation: Use it only for a specific file the user intentionally wants copied, and confirm the exact source path and destination folder before copying. <br>
Risk: The referenced PowerShell helper script is not included in the artifact, while the command uses execution-policy bypass. <br>
Mitigation: Do not run the PowerShell command unless the helper script is supplied from a trusted source and reviewed before execution. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Markdown, Guidance] <br>
**Output Format:** [Markdown with PowerShell command guidance and a file verification report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports source path, destination path, byte and MB size, and SHA256 after copy.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
