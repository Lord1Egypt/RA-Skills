## Description: <br>
Internal setup hook that provisions gogcli with Google OAuth credentials supplied by an external orchestrator over the OpenClaw `skills.setup` RPC. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[maverick](https://clawhub.ai/user/maverick) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to provision gogcli OAuth state non-interactively for Google Workspace access through the companion upstream `gog` skill. It is intended for install and credential-rotation workflows, not for direct agent-facing commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The setup hook handles Google OAuth client secrets and refresh tokens and persists credential state through gogcli. <br>
Mitigation: Install only where an orchestrator is expected to provide these credentials, protect the container filesystem, and use a non-empty per-instance GOG_KEYRING_PASSWORD. <br>
Risk: Running setup with a stale or unintended refresh token can overwrite existing gogcli authentication state. <br>
Mitigation: Run setup only after a fresh intended OAuth authorization callback provides a new refresh token. <br>


## Reference(s): <br>
- [gogcli homepage](https://github.com/openclaw/gogcli) <br>
- [Upstream gog skill](https://github.com/openclaw/openclaw/blob/main/skills/gog/SKILL.md) <br>
- [ClawHub skill page](https://clawhub.ai/maverick/maverick-gog) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell command behavior documented in setup scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No direct agent-facing command output; setup imports OAuth credentials into gogcli-managed local state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
