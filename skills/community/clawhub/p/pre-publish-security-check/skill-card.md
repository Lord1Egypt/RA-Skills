## Description: <br>
Pre-Publish Security Check scans a skill folder before ClawHub publishing for possible API keys, tokens, private keys, precise coordinates, personal email addresses, and Chinese phone numbers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vlalamoon](https://clawhub.ai/user/vlalamoon) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill before publishing to ClawHub to check a local skill directory for common secret and personal-data patterns that should be removed or replaced with placeholders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scanner output can expose real secrets or personal data when matches are found. <br>
Mitigation: Run it only on the intended local skill folder and keep the output private while remediation is in progress. <br>
Risk: A clean scan does not prove the skill is safe to publish. <br>
Mitigation: Treat the result as a pre-check and still review the skill contents, examples, and configuration before release. <br>
Risk: Scanning the wrong path may reveal unrelated local files in terminal output. <br>
Mitigation: Pass the specific skill directory path rather than a broad parent directory. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/vlalamoon/pre-publish-security-check) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/vlalamoon) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Analysis] <br>
**Output Format:** [Markdown guidance with bash commands; terminal text from the scanner] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner output may include matched secrets or personal data and should be kept private.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
