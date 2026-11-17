## Description:

Internal setup hook that provisions gogcli with Google OAuth credentials supplied by an external orchestrator over the OpenClaw `skills.setup` RPC. Not user-facing — for Google Workspace command usage, see the upstream `gog` skill which loads alongside this one.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maverick](https://clawhub.ai/user/maverick)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this setup hook to provision or rotate Google OAuth credentials for gogcli through OpenClaw's setup flow. It prepares the configuration used by the separate upstream `gog` skill, which provides Google Workspace commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The gogcli OAuth client-secret file is stored in plaintext on disk, even when a keyring password is configured.

Mitigation: Use a trusted provisioning service and restrict access to credential files, the container filesystem, and backups.

Risk: An empty GOG_KEYRING_PASSWORD leaves the refresh-token keyring without at-rest encryption, and the variable must be set consistently for setup and runtime.

Mitigation: Set a strong, nonempty per-instance password and make it available consistently during setup and runtime.

Risk: Rerunning setup with a stale refresh token can replace a token gogcli has already rotated and break the integration.

Mitigation: Run setup only when a newly issued refresh token is available from a completed authorization flow.

## Reference(s):

- [gogcli project](https://github.com/openclaw/gogcli)
- [OpenClaw gog skill documentation](https://github.com/openclaw/openclaw/blob/main/skills/gog/SKILL.md)
- [ClawHub release page](https://clawhub.ai/maverick/skills/maverick-gog)

## Skill Output:

**Output Type(s):** [Configuration]

**Output Format:** [gogcli OAuth credential and account configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Setup-time configuration; the skill exposes no agent-callable commands.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
