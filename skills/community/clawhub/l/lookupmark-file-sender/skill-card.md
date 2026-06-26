## Description: <br>
Finds local files, sends them to chat channels, and manages encrypted credential files with age encryption. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lookupmark](https://clawhub.ai/user/lookupmark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill when they want an agent to locate a local file, confirm the intended recipient, and send it through a supported chat channel. It also supports encrypted storage and sending workflows for credential files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send readable local files, including sensitive documents, through chat channels. <br>
Mitigation: Require explicit file path and recipient confirmation before each send, and avoid transmitting private keys, passwords, or other high-risk secrets through chat. <br>
Risk: The credential workflow can decrypt and transmit encrypted credential files. <br>
Mitigation: Use the encrypted credential flow only for intentional credential handling, confirm the recipient every time, and add stronger identity checks or allowlists before use on a real machine. <br>
Risk: The security review verdict is suspicious because safeguards are weak for broad local-file access and transmission. <br>
Mitigation: Review the skill before deployment and restrict it to trusted environments where the user understands and accepts local-file sending behavior. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lookupmark/lookupmark-file-sender) <br>
- [age encryption tool](https://github.com/FiloSottile/age) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files, Configuration guidance] <br>
**Output Format:** [Markdown guidance with shell commands and file-send actions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May invoke local Python scripts and OpenClaw CLI commands to stage, encrypt, decrypt, and send files.] <br>

## Skill Version(s): <br>
2.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
