## Description: <br>
B-only Quick Auth for Moss platform. Use only api-login / api-register (no email code flow). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[helloeveryworlds](https://clawhub.ai/user/helloeveryworlds) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to perform B-only quick authentication against Moss platform quick-auth endpoints with a host and email, retrying registration or login based on returned account status. The skill is intended to report endpoint choice, status, user ID, expiration, and credentials with masking by default. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create or access Moss accounts and may return access tokens, refresh tokens, API keys, or temporary passwords. <br>
Mitigation: Install only when authorized to use the Moss quick-auth endpoints, confirm the exact host and email before use, require explicit approval before registration, and mask credentials by default. <br>
Risk: A temporary password may be returned only once during registration. <br>
Mitigation: Warn the user before registration that the temporary password must be saved immediately and avoid displaying or storing it unless strictly necessary. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/helloeveryworlds/moss-platform-quick-auth) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and response field names] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Credentials should be masked by default unless the user explicitly requests raw values.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
