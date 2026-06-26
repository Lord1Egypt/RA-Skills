## Description: <br>
Olares profile and authentication foundation for olares-cli, covering profile login, token import, profile switching, keychain-backed token storage, automatic access token refresh, and auth-error recovery for Olares CLI workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[olares](https://clawhub.ai/user/olares) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill when an agent needs to authenticate olares-cli, manage Olares profiles, recover from token errors, or prepare the active profile required by other Olares CLI skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires sensitive Olares credentials and token handling. <br>
Mitigation: Use interactive entry, `--password-stdin`, environment variables, or a secret manager; do not place passwords, refresh tokens, or access tokens directly in commands or shared scripts. <br>
Risk: The security scan flagged suspicious behavior in the broader release because review helpers may run nested reviewers with broad local access or send diffs to fallback AI review CLIs. <br>
Mitigation: Install only from trusted maintainers; run autoreview with `--no-yolo` or `AUTOREVIEW_YOLO=0`, and set fallback reviewers to `none` if local diffs should not be shared with other review CLIs. <br>
Risk: Profile removal or overwrite operations can delete stored authentication state. <br>
Mitigation: Confirm user intent before running write or delete actions such as `olares-cli profile remove`, token import, or overwrite-style commands. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/olares/olares-shared) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guidance may include credential-handling instructions, profile-management commands, and auth-error recovery steps.] <br>

## Skill Version(s): <br>
4.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
