## Description: <br>
Migrate an existing nansen-cli wallet from insecure password storage (env files, .credentials) to the new secure keychain-backed flow. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nansen-devops](https://clawhub.ai/user/nansen-devops) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and wallet operators use this skill to detect old nansen-cli wallet password storage and migrate credentials to the operating system keychain. It also guides post-migration verification, cleanup of insecure password files, and recovery handling when the wallet password is unavailable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet passwords and private keys may appear in agent-visible command output or logs. <br>
Mitigation: Have the user run password and private-key commands directly in a local terminal whenever possible; otherwise suppress or redact output and avoid export-based verification unless output is controlled. <br>
Risk: Migration may require interacting with insecure local password stores such as env files or .credentials files. <br>
Mitigation: Require explicit user authorization before reading local password files, never echo or store secrets, and remove insecure password files only after successful migration and verification. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nansen-devops/nansen-wallet-keychain-migration) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/nansen-devops) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires nansen-cli and NANSEN_API_KEY; wallet password handling should be performed with suppressed or redacted output.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
