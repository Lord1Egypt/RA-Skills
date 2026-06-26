## Description: <br>
LESecure Local/On-Prem encrypts and decrypts text, files, and folders with the local LE desktop tool using pin, password, MFA, time-lock, and geo-location controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[spalgorithm](https://clawhub.ai/user/spalgorithm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to run local LE desktop encryption and decryption workflows for plaintext, files, and folders without sending data to a cloud service. It also helps configure layered locks such as pin, password, MFA, time windows, and location locks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad current-location triggers can lead to a sensitive GPS lookup when the user did not clearly intend to use LESecure. <br>
Mitigation: Require explicit LESecure or location-lookup intent and user confirmation before running the LE location command. <br>
Risk: Destructive LE flags can delete source files after encryption or decryption. <br>
Mitigation: Default to non-destructive flags and require explicit confirmation before using delete-source behavior. <br>
Risk: Plaintext encryption commands can become unsafe if raw user text is interpolated directly into shell commands. <br>
Mitigation: Sanitize quoted plaintext or pass it through a shell variable, and never use eval or backtick interpolation with user-provided text. <br>


## Reference(s): <br>
- [LE source code and documentation](https://github.com/SPAlgorithm/LE) <br>
- [ClawHub skill page](https://clawhub.ai/spalgorithm/lesecurelocal) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local LE command guidance and may request confirmation before privacy-sensitive or destructive operations.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
