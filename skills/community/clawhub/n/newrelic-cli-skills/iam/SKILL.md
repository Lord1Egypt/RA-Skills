# Identity and Access Management

Use the `usermanagement` command tree for authentication domains, users, groups, and memberships. Use `accessmanagement` for roles, permissions, and group access grants.

Behavioral and completeness caveats in this guide are verified against the upstream CLI
release recorded in [`../VERSION`](../VERSION). Revalidate them whenever that file advances.

## Safety Contract

Identity and access changes can remove access, grant elevated privileges, or delete identities.

1. Default to read-only discovery.
2. Resolve IDs from current CLI output; do not guess an authentication-domain, user, group, role, or account ID.
3. Treat every IAM write as confirmation-gated: show the exact target, requested change, scope, and command, then require explicit confirmation.
4. Treat user/group deletion, membership removal, grant creation/revocation, user email changes, explicit user-tier selection or changes, and group creation/rename as identity-, access-, or billing-sensitive writes.
5. Run the corresponding read command after every write and verify the intended state.
6. Never print, log, or embed `NEW_RELIC_API_KEY` in a command.

## Prerequisites

`NEW_RELIC_API_KEY` must be a User Key belonging to a core or full platform user with the organization-scoped role required for the operation. `usermanagement` writes require Authentication domain manager or Organization manager; prefer Authentication domain manager when it is sufficient. The command documentation for the recorded release requires Organization manager for `accessmanagement` grant writes. Read-only discovery requires at least Authentication domain read-only capability. These roles belong to the user associated with the key; account scoping alone does not authorize organization-level IAM administration.

```bash
newrelic profile list
newrelic usermanagement --help
newrelic accessmanagement --help
```

Use the narrowest profile and account scope that can complete the task. The commands emit JSON by default; add `--format JSON` when scripts should make that requirement explicit.

## Read-Only Discovery

### Authentication domains

```bash
# List authentication domains
newrelic usermanagement auth-domains get

# Read one authentication domain
newrelic usermanagement auth-domains get --id "$AUTH_DOMAIN_ID"
```

### Users

`--authDomainId` is required for user lookups. Optional filters are `--id`, `--email`, and `--name`. The email and name filters use equality matching, unlike the partial role-name match below; do not assume substring or case-insensitive matching.

```bash
newrelic usermanagement users get --authDomainId "$AUTH_DOMAIN_ID"
newrelic usermanagement users get \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --email "$USER_EMAIL"
newrelic usermanagement users get \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --id "$USER_ID"
```

### Groups and membership

`--authDomainId` is required for group lookups. The name filter uses equality matching. Group results include members, but the nested member collection is not paginated by this CLI version.

```bash
newrelic usermanagement groups get --authDomainId "$AUTH_DOMAIN_ID"
newrelic usermanagement groups get \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --name "$GROUP_NAME"
newrelic usermanagement groups get \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --id "$GROUP_ID"
```

If an equality-filtered user or group lookup is empty, retry unfiltered in the same authentication domain and inspect returned names and emails before creating anything. Do not conclude that the target is absent unless the full domain result set has been enumerated: the recorded release does not paginate the nested user/group collections. Use a fully paginated NerdGraph query or another authoritative complete listing when an unfiltered result may be truncated.

### Roles, permissions, and grants

```bash
# Discover role IDs
newrelic accessmanagement roles get
newrelic accessmanagement roles get --name "$ROLE_NAME"
newrelic accessmanagement roles get --groupId "$GROUP_ID"

# Inspect permissions before granting a role
newrelic accessmanagement permissions get --roleId "$ROLE_ID"
newrelic accessmanagement permissions get --scope account
newrelic accessmanagement permissions get --scope organization

# Inspect current grants
newrelic accessmanagement grants get
newrelic accessmanagement grants get --groupId "$GROUP_ID"
```

Role-name matching is partial. If multiple roles match, stop and select the exact role ID from the returned data before making a grant.

`roles get` and `grants get` make one request only, even when filters are present. Before relying on either result, require `totalCount` to equal the number of returned `items`; a present, nonempty `nextCursor` also proves the result is incomplete. Do not conclude that a role or grant is absent from an incomplete result. Prefer `grants get --groupId "$GROUP_ID"` for group-specific decisions, but still apply this completeness check.

## User Administration

### Create

`--authDomainId`, `--email`, and `--name` are required. Valid user tiers are `BASIC_USER_TIER`, `CORE_USER_TIER`, and `FULL_USER_TIER`. Under New Relic's current user-based pricing policy, core and full platform users are billable user types while basic users are not; actual charges depend on the organization's agreement. State the requested tier and this billing impact before confirmation.

```bash
newrelic usermanagement users create \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --email "$USER_EMAIL" \
  --name "$USER_NAME" \
  --userType "$USER_TYPE"
```

Verify:

```bash
newrelic usermanagement users get \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --email "$USER_EMAIL"
```

### Update

`--id` is required. Pass only the fields the user intends to change: `--email`, `--name`, `--userType`, or `--timeZone`. Before changing `--email`, confirm the resolved user ID and the old and new addresses. Before changing `--userType`, state the current and requested tiers and the billing impact described above.

```bash
newrelic usermanagement users update \
  --id "$USER_ID" \
  --timeZone "$TIME_ZONE"
```

Verify with `users get --authDomainId ... --id ...`.

### Delete

Deletion is permanent. Confirm the resolved user ID and email immediately before execution.

```bash
newrelic usermanagement users delete --id "$USER_ID"
```

Verify that `users get --authDomainId ... --id ...` no longer returns the user.

## Group Administration

### Create or rename

Confirm the authentication-domain ID and exact requested name before creating a group. Before renaming, also confirm the resolved group ID and current name.

```bash
newrelic usermanagement groups create \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --name "$GROUP_NAME"

newrelic usermanagement groups update \
  --id "$GROUP_ID" \
  --name "$NEW_GROUP_NAME"
```

Read the group back by ID after either command.

### Add a member

```bash
newrelic usermanagement groups members add \
  --groupId "$GROUP_ID" \
  --userId "$USER_ID"
```

After the add, read the user and inspect `groups.groups`. Presence of `$GROUP_ID` confirms the membership:

```bash
newrelic usermanagement users get \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --id "$USER_ID"
```

### Remove a member

Before removal, inspect the group's complete grant set, summarize the access the user will lose, and obtain explicit confirmation. Apply the grant-result completeness check above before relying on this output.

```bash
newrelic accessmanagement grants get --groupId "$GROUP_ID"

newrelic usermanagement groups members remove \
  --groupId "$GROUP_ID" \
  --userId "$USER_ID"
```

After removal, read the user by ID and inspect `groups.groups`. The target group's presence proves removal failed, but absence does not conclusively prove removal: both the group's `users` and user's `groups` relationships are cursor-based, while the recorded release returns only their first page and exposes no nested cursor. If absence must be proven, use a fully paginated NerdGraph query; otherwise report that the mutation succeeded but absence could not be conclusively verified.

### Delete

Deleting a group is permanent and removes access inherited through its grants. Inspect current members and grants first.

```bash
newrelic usermanagement groups get \
  --authDomainId "$AUTH_DOMAIN_ID" \
  --id "$GROUP_ID"
newrelic accessmanagement grants get --groupId "$GROUP_ID"

# Execute only after explicit confirmation
newrelic usermanagement groups delete --id "$GROUP_ID"
```

Verify that the group lookup no longer returns the group.

## Access Grants

A grant assigns a role to a group at either account or organization scope. Inspect the role's permissions and the group's existing grants before changing access.

### Account-scoped grant

Resolve the requested account ID and obtain explicit confirmation before setting `TARGET_ACCOUNT_ID`; do not infer the IAM target from the profile or ambient `NEW_RELIC_ACCOUNT_ID`.

```bash
newrelic accessmanagement grants create \
  --groupId "$GROUP_ID" \
  --roleId "$ROLE_ID" \
  --scope account \
  --accountId "$TARGET_ACCOUNT_ID"
```

### Organization-scoped grant

```bash
newrelic accessmanagement grants create \
  --groupId "$GROUP_ID" \
  --roleId "$ROLE_ID" \
  --scope organization
```

### Revoke a grant

Select the exact grant item from a complete `grants get --groupId "$GROUP_ID"` result. Map `.group.id` to `--groupId` and `.role.id` to `--roleId`. Translate `.scope.type` from API value `ACCOUNT` or `ORGANIZATION` to CLI value `account` or `organization`. For `ACCOUNT`, map `.scope.id` to a separately confirmed `TARGET_ACCOUNT_ID`; omit `--accountId` for `ORGANIZATION`. Stop for `GROUP`, `OTHER`, or any unsupported scope.

Inspect `.dataAccessPolicy.id`, not merely whether `dataAccessPolicy` is non-null. If the ID is nonempty, stop: the recorded release exposes no revoke flag for the policy ID and cannot reliably construct the full account-revoke input.

```bash
# Account scope
newrelic accessmanagement grants revoke \
  --groupId "$GROUP_ID" \
  --roleId "$ROLE_ID" \
  --scope account \
  --accountId "$TARGET_ACCOUNT_ID"

# Organization scope
newrelic accessmanagement grants revoke \
  --groupId "$GROUP_ID" \
  --roleId "$ROLE_ID" \
  --scope organization
```

Verify grant creation or revocation with:

```bash
newrelic accessmanagement grants get --groupId "$GROUP_ID"
```

## Safe End-to-End Sequence

1. Run `auth-domains get` and resolve one authentication-domain ID.
2. Read users and groups in that domain; stop on ambiguous matches.
3. For a new identity, create the user and group only after confirmation, then read both back.
4. Add the user to the group after confirmation, then verify membership.
5. Read roles and inspect the chosen role's permissions.
6. Read existing grants for the group.
7. State whether the proposed grant is account- or organization-scoped and identify the account when applicable.
8. Create the grant after confirmation and read the group's grants back.
9. Report the exact IDs and verified final state without exposing credentials.
