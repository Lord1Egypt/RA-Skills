## Description:

Olares profile and authentication foundation for olares-cli, covering profile login, refresh-token import, profile switching, keychain-backed token storage, automatic token refresh, and auth-error recovery for Olares CLI workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olares](https://clawhub.ai/user/olares)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill as the authentication and profile-management foundation for Olares CLI workflows. It helps users log in safely, import refresh tokens, switch profiles, understand token storage, and recover from common authentication failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Long-lived refresh tokens or 2FA codes may be exposed through shared shells, CI logs, recorded terminals, or monitored systems.

Mitigation: Prefer interactive login where the user enters credentials directly, and avoid refresh-token import or --totp in shared or logged environments.

Risk: Tokens stored through file fallback have different security properties than a system keychain.

Mitigation: Treat file-fallback token storage as sensitive local credential material and review the environment before installing or using the skill.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/olares/skills/olares-shared)
- [Olares publisher profile](https://clawhub.ai/user/olares)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and recovery tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires olares-cli and relies on the active local Olares profile.]

## Skill Version(s):

4.0.1 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
