## Description: <br>
OAuth token refresh management for Google APIs via gog CLI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[herry3zz](https://clawhub.ai/user/herry3zz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators who use the gog CLI use this skill to configure Google OAuth refresh-token handling and run common Gmail, Drive, and Calendar commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Google OAuth credentials and refresh tokens can grant access to Gmail, Drive, or Calendar data. <br>
Mitigation: Grant only the OAuth scopes needed for the intended services and keep credential files restricted to the user account. <br>
Risk: Using a file-based keyring backend for automation can expose long-lived secrets if passwords are stored insecurely. <br>
Mitigation: Prefer an OS-native keychain or secret manager, and avoid placing long-lived keyring passwords in environment variables when possible. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/herry3zz/google-gog) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
