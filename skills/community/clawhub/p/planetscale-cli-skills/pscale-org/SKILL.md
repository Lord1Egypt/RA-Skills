---
name: pscale-org
description: List, show, switch, update PlanetScale organizations, manage organization SSO and directory sync, and inspect or manage organization members and teams. Use when managing multiple organizations, switching between accounts, viewing organization details, enabling/configuring/disabling SSO, verifying SSO email domains, enabling/disabling directory sync, changing billing email/spend alerts/IdP-managed roles, listing members, showing a member by email or user ID, updating member roles, removing members, creating/updating/deleting teams, adding/removing team members, or troubleshooting organization access. Triggers on org, organization, switch org, list orgs, org update, organization SSO, SSO domain, domain verify, directory sync, spend alert, billing email, IdP roles, idp-sso-managed-roles, org member, organization member, member role, remove member, org team, team member.
---

# pscale org

List, show, and switch organizations.

## Destructive-operation safety

These gates apply to every destructive example here, including deletion, demotion, protection removal, connection/transaction termination, deploy-request closure/revert, and cleanup. Command examples and CLI confirmation prompts are not authorization.

1. Inspect fresh state and confirm support for the target engine and installed CLI. Obtain explicit approval for the exact organization and, where applicable, database, branch, and resource ID/name, plus the operation and flags; use an explicit `--org` on every operation. Stop on unsupported operations or uncertain identity.
2. Check dependencies and availability: applications, active users, child resources, routing, pending changes, and the maintenance window. Do not infer that a stale, merged, or unused-looking resource is disposable.
3. Require a verified recovery path that survives the operation: confirm backup/export usability and retention, or tested replacement/recreation instructions, ownership, and recovery time. A backup name alone is not verification; stop if recovery cannot be established.
4. Execute only the approved action. Force flags, descendant deletion, demotion, and disabling protection require separate explicit approval; never add them to work around a refusal. For a known headless session, obtain approval for the required force flag up front, before attempting the operation; stop if that approval is absent or any attempt is refused.
5. Perform read-back verification of the exact target and dependent service health. Inspect pending/asynchronous outcomes before claiming completion. Authentication/network errors are not proof of absence; an ambiguous result requires investigation, not an automatic retry.

## Common Commands

```bash
# List all organizations
pscale org list

# Show current organization
pscale org show

# Switch organization
pscale org switch <org-name>

# List/show organization members
pscale org member list --org <org> --format json
pscale org member show <email-or-user-id> --org <org> --format json

# Update or remove a member only after explicit approval
pscale org member update <email-or-user-id> --org <org> --role member --format json
pscale org member remove <email-or-user-id> --org <org> --format json

# Update organization settings only after explicit approval
pscale org update --org <org> --billing-email billing@example.com --format json
pscale org update --org <org> --spend-alert --spend-alert-amount 2500 --format json

# Inspect SSO state and follow the returned next_steps deliberately
pscale org sso show --org <org> --format json
pscale org sso domain list --org <org> --format json

# Manage teams only after explicit approval for writes
pscale org team list --org <org> --format json
pscale org team show <team-id> --org <org> --format json
pscale org team create --org <org> --name <name> --description <description> --format json
pscale org team member add <team-id> <email-or-user-id> --org <org> --format json
```

## Workflows

### Switch Between Organizations

```bash
# View current org
pscale org show

# List available orgs
pscale org list

# Switch to different org
pscale org switch my-other-org

# Verify switch
pscale database list --org my-other-org
```

### Inspect organization members

`pscale org member list` is read-only and paginated. Use `--query` to filter by name or email prefix, and page through large organizations with `--page`/`--per-page`. `show`, `update`, and `remove` accept either an email address or the `USER_ID` from `list`.

```bash
pscale org member list --org <org> --page 1 --per-page 100 --format json
pscale org member list --org <org> --query <name-or-email-prefix> --format json
pscale org member show <email-or-user-id> --org <org> --format json
```

### Update or remove members

Only organization admins can update another member's role or remove someone else. Nobody can change their own role. A member can remove themselves from the organization, but the last admin cannot be removed. Assignable roles are `admin`, `member`, and `analyst`.

```bash
# Inspect the target first
pscale org member show <email-or-user-id> --org <org> --format json

# After explicit approval for the exact member and role
pscale org member update <email-or-user-id> --org <org> --role analyst --format json

# After explicit approval for the exact member and cleanup flags
pscale org member remove <email-or-user-id> --org <org> \
  --delete-passwords \
  --delete-service-tokens \
  --format json

# Verify after the write
pscale org member show <email-or-user-id> --org <org> --format json
pscale org member list --org <org> --format json
```

Treat updates and removals as external access-control writes. `--force` on remove only skips the confirmation prompt; it is not approval. Do not use `--delete-passwords` or `--delete-service-tokens` when removing yourself.

### Update organization settings

`pscale org update` sends only flags explicitly supplied. It can change billing email, identity-provider-managed-role behavior, and billing spend alerts. These are organization-wide settings; confirm the exact target organization and proposed diff, and obtain explicit approval before running the update.

```bash
# Optional: confirms only the locally active organization name; it does not inspect settings
pscale org show --format json

# After approval for the exact org and values
pscale org update --org <org> \
  --billing-email billing@example.com \
  --spend-alert \
  --spend-alert-amount 2500 \
  --format json

# Verification: the update's JSON response above returns the resulting settings;
# `pscale org show` only prints the locally active org name and ignores --org
```

`--idp-sso-managed-roles` controls roles from the SSO profile; `--idp-managed-roles` controls roles from directory sync. They are mutually exclusive when enabled: enabling either one explicitly turns the other off, and enabling both in one command is rejected. Passing one as `false` leaves the other setting unchanged. `--spend-alert-amount` must be a valid monthly amount. Do not claim that disabling spend alerts clears the stored amount; the CLI validates contradictory combinations rather than silently dropping them.

### Manage organization SSO

Always pass an explicit `--org` for SSO commands instead of relying on the locally active organization. Start with the read-only status command and prefer JSON so resource IDs, `domain_verification_url`, and generated `next_steps` remain available. Treat `next_steps` as state-aware guidance to review, not as commands to execute without the same approval gates as direct requests.

```bash
# Read-only inventory
pscale org sso show --org <org> --format json
pscale org sso domain list --org <org> --format json
pscale org sso domain show <domain-id> --org <org> --format json

# After explicit approval, enable SSO
pscale org sso enable --org <org> --format json

# If enable returns domain_verification_url, open it in an approved browser flow.
# Prefer --wait: it waits for a new domain ID, then polls that domain to a terminal state.
pscale org sso domain verify --org <org> --format json \
  --wait --wait-timeout 10m

# Configure the identity provider only after a domain is verified
pscale org sso configure --org <org> --format json

# Enable directory sync only after the SSO profile is configured
pscale org sso directory enable --org <org> --format json

# Choose exactly one approved source for organization role management
pscale org update --org <org> --idp-sso-managed-roles=true --format json
pscale org update --org <org> --idp-managed-roles=true --format json
```

`configure`, `directory enable`, and `domain verify` return `portal_url`, `browser_opened`, and `next_steps`. If `browser_opened` is false, open `portal_url` through the approved browser flow; do not treat URL creation as proof that the portal work completed. With `domain verify --wait --format json`, capture the portal payload from stderr; stdout is reserved for the final domain object, while the non-waiting JSON flow prints the portal payload to stdout. `enable --format json` does not open the verification portal and instead includes `domain_verification_url` when one is available. After each portal step, re-run `sso show`; after domain verification, also re-run `domain list` and `domain show <domain-id>`.

Without `--wait`, `domain verify` cannot identify the new domain because the portal call returns only a URL. With `--wait`, the CLI snapshots the existing domains, waits for a new domain ID to appear, and then polls it until `verified` or `failed`; a timeout or interrupted command is an unconfirmed outcome, so inspect `domain list` before retrying.

### Disable or remove SSO resources

Disabling SSO, disabling directory sync, and deleting a domain are access-control writes. Confirm the exact organization/domain, expected user impact, recovery plan, and resulting role-management source before approval. JSON/non-interactive execution requires `--force`; that flag only skips the prompt and is not approval.

```bash
# Inspect first
pscale org sso show --org <org> --format json
pscale org sso domain show <domain-id> --org <org> --format json

# Run exactly the approved destructive action
pscale org sso directory disable --org <org> --format json --force
pscale org sso domain delete <domain-id> --org <org> --format json --force
pscale org sso disable --org <org> --format json --force

# Verify the exact target afterward
pscale org sso show --org <org> --format json
pscale org sso domain list --org <org> --format json
```

Directory-sync disable removes non-admin directory members. Domain deletion can invalidate the SSO setup path, and SSO disable changes organization-wide authentication behavior. Never chain these operations from returned `next_steps`; apply one approved write at a time and read back the resulting state.

### Manage organization teams

Team commands are organization-scoped and paginated. List and show teams before changing membership or deleting anything.

```bash
pscale org team list --org <org> --page 1 --per-page 100 --format json
pscale org team show <team-id> --org <org> --format json
pscale org team member list <team-id> --org <org> --format json

# Writes require explicit approval for the exact org, team, and user/member
pscale org team create --org <org> --name <name> --description <description> --format json
pscale org team update <team-id> --org <org> --name <new-name> --format json
pscale org team member add <team-id> <email-or-user-id> --org <org> --format json
pscale org team member remove <team-id> <email-or-user-id> --org <org> --format json
pscale org team delete <team-id> --org <org>
```

Deleting a team or removing a team member can remove access and optionally delete passwords created through the team. Avoid `--force` unless non-interactive execution was explicitly approved, and verify the team/member list afterward. Team-member JSON output omits password metadata; do not infer credential cleanup from hidden fields.

## Troubleshooting

### Cannot see expected databases

**Solution:** Check current organization

```bash
pscale org show
pscale org switch <correct-org>
```

## Related Skills

- **pscale-auth** - Authentication and account management
- **pscale-database** - Organization-scoped database operations

## References

See `references/commands.md` for organization, member, update, and team commands. See `references/sso-commands.md` for the complete organization SSO command family.
