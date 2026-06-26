## Description: <br>
Install and authenticate OB1 (OpenBlock One), a multi-model terminal coding agent. Use when asked to install OB1, set up ob1, or when ob1 authentication/login is needed. Covers macOS/Linux install, device code authentication flow, and post-install verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[txc-z](https://clawhub.ai/user/txc-z) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install OB1 on macOS or Linux, complete device-code authentication, and verify that the terminal agent is ready for use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The install flow fetches and executes an external installer URL. <br>
Mitigation: Install only when the user trusts OpenBlockLabs and the installer URL at execution time. <br>
Risk: Device codes and the saved ~/.ob1/ token are sensitive authentication material. <br>
Mitigation: Avoid shared or untrusted machines for authentication, keep the process alive only for the active login, and treat saved tokens as sensitive. <br>
Risk: Non-interactive '-y' usage can proceed with fewer prompts. <br>
Mitigation: Use non-interactive runs only when the user explicitly wants OB1 to proceed with reduced prompting. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/txc-z/ob1-install) <br>
- [OB1 installer](https://dashboard.openblocklabs.com/install) <br>
- [OB1 device authentication](https://auth.openblocklabs.com/device) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and setup notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes install, authentication, verification, token-location, configuration-file, and non-interactive usage guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
