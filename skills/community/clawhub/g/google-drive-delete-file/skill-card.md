## Description: <br>
Atomic node skill to delete a file in Google Drive using the gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zvirb](https://clawhub.ai/user/zvirb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to move a known Google Drive file to trash through an authenticated gog CLI session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can move Google Drive files to trash if given the wrong file ID. <br>
Mitigation: Use it only for explicit deletion requests and verify the target file ID or metadata before execution. <br>
Risk: Autonomous use could cause costly accidental Drive deletion. <br>
Mitigation: Require user confirmation before running the gog delete command in high-impact or ambiguous contexts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zvirb/google-drive-delete-file) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, text] <br>
**Output Format:** [Markdown with an inline gog command and textual confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the gog binary and an authenticated Google Drive context; expected result is confirmation that the file was moved to trash.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
