---
name: id-tool
description: Display user and group identity information. Shows real and effective user ID, group ID, and supplementary groups for the current process.
---
# ID - User Identity Display

Print user and group identity information including UID (user ID), GID (group ID), and all supplementary group memberships. Essential for permission debugging and understanding process security context.

## Usage

```bash
id-tool [options] [username]
```

Without arguments, shows information for the current user. Specify a username to query another user's identity details.

## Options

- `-u`: Show only effective user ID
- `-g`: Show only effective group ID
- `-G`: Show all supplementary group IDs
- `-n`: Display names instead of numeric IDs

## Examples

```bash
# Show full identity
id-tool

# Show user ID only
id-tool -u

# Show all groups for user
id-tool -G www-data
```