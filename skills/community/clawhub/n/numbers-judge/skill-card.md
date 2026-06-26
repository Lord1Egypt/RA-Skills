## Description: <br>
Checks whether a text string consists of integer-number segments separated by a specified special character. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wahahasssss](https://clawhub.ai/user/wahahasssss) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents can use this skill when a user asks whether supplied text contains only integer numeric content and a specified separator, and to identify any non-integer segments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Input text passed to the script is echoed in console output. <br>
Mitigation: Avoid using sensitive text with this skill unless command-line argument echoing is acceptable. <br>
Risk: The check is limited to integer segments split by the supplied special character. <br>
Mitigation: Use it only for integer-number validation, and use a different validator when decimals, signs, locale-specific number formats, or broader parsing rules are required. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Plain text command output and agent guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The script prints the command-line arguments before printing comma-separated non-integer segments.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
