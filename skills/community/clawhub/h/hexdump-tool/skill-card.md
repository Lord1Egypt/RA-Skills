## Description: <br>
Display file contents in hexadecimal and ASCII format. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dinghaibin](https://clawhub.ai/user/dinghaibin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and analysts use this skill to inspect binary files, stdin data, or encoded strings as hexadecimal and printable ASCII. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The tool prints the contents of whichever file or stdin data is provided, which can expose sensitive data in shared logs or chats. <br>
Mitigation: Inspect only intended files and avoid dumping secrets, credentials, or private data into shared channels. <br>
Risk: Some documented display features may not be implemented, so output may be plainer than expected. <br>
Mitigation: Verify output formatting against a small sample before relying on it for review or reporting workflows. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text hexdump output and command-line usage guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads local files or stdin and prints selected content without network access or system changes.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
