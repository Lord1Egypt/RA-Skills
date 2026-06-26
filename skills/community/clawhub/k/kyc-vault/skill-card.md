## Description: <br>
Automates KYC identity verification by securely managing and submitting identity documents, while asking user permission before accessing or uploading any file. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[seamao](https://clawhub.ai/user/seamao) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to assist with website KYC flows by matching local identity documents to requested verification fields, filling personal information, and requesting confirmation before each file access, upload, or final submission. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive identity documents and personal information during KYC workflows. <br>
Mitigation: Keep the identity vault private, inspect and edit the manifest before entering real data, and approve each document access, upload, field fill, and final submission deliberately. <br>
Risk: A user could interact with the wrong or malicious KYC domain. <br>
Mitigation: Verify the exact domain before starting a session and stop if a page attempts to bypass permission or upload rules. <br>


## Reference(s): <br>
- [KYC Vault ClawHub listing](https://clawhub.ai/seamao/kyc-vault) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Browser actions] <br>
**Output Format:** [Markdown instructions with inline shell commands and confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requests explicit user confirmation before reading manifest data, accessing files, uploading documents, filling personal information, or submitting KYC forms.] <br>

## Skill Version(s): <br>
0.2.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
