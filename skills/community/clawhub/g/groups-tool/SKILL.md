---
name: groups-tool
description: Display user group memberships on the system. Shows all groups a user belongs to for permission auditing and access control verification.
---
# Groups - User Group Membership Checker

Display all group memberships for the current user or a specified system user. Group membership determines file access permissions and sudo privileges on Unix-like systems.

## Usage

```bash
groups-tool [options] [username]
```

When called without arguments, shows groups for the current user. Specify a username to check another user's memberships.

## Examples

```bash
# Show groups for current user
groups-tool

# Show groups for a specific user
groups-tool www-data

# Show numeric group IDs
groups-tool -id
```

## Notes

Groups are read from /etc/group and can include both primary and supplementary group memberships. Changes to group membership take effect on next login.
