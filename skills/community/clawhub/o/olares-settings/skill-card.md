## Description:

Guides agents in using `olares-cli settings` to read and change Olares Settings surfaces for users, appearance, apps, integrations, VPN, network, GPU, video, search, backup, restore, advanced settings, and self-service account checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[olares](https://clawhub.ai/user/olares)

### License/Terms of Use:

MIT-0

## Use Case:

External Olares operators, administrators, and developers use this skill to inspect and manage Olares Settings through an authenticated `olares-cli` profile. It is intended for settings workflows such as user administration, app post-install configuration, integration accounts, VPN ACLs, search, backup, restore, and account self-service checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide administrative settings changes for users, apps, VPN, integrations, search, and backups through an authenticated `olares-cli` profile.

Mitigation: Review proposed commands before write actions, confirm the active profile and role, and prefer read/list commands before mutation.

Risk: Integration account JSON, backup passwords, generated user passwords, app environment values, and SSO tokens may contain secrets.

Mitigation: Use environment variables, stdin, or interactive prompts for secrets; avoid dumping sensitive JSON; keep credentials out of chat, shell history, and logs.

Risk: Some operations are destructive or replace whole vectors, including user deletion, app environment replacement, policy replacement, VPN ACL changes, and backup password rotation.

Mitigation: Inspect current state first, surface irreversible effects to the user, require explicit confirmation for destructive operations, and verify results after changes.

Risk: Several mutating verbs are documented as unverified or experimental.

Mitigation: Treat experimental command output as cautionary, avoid suppressing CLI warnings, and manually verify the resulting state before relying on it.

## Reference(s):

- [Olares Settings documentation](https://docs.olares.com/manual/olares/settings/)
- [ClawHub release page](https://clawhub.ai/olares/skills/olares-settings)
- [Olares Settings apps reference](references/olares-settings-apps.md)
- [Olares Settings backup reference](references/olares-settings-backup.md)
- [Olares Settings integration reference](references/olares-settings-integration.md)
- [Olares Settings users reference](references/olares-settings-users.md)
- [Olares Settings VPN reference](references/olares-settings-vpn.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON-output recommendations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not produce files by itself; command output may include tables or JSON from `olares-cli` depending on flags.]

## Skill Version(s):

4.0.1 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
