---
name: kiipu-cli
description: Use when the user wants to create, delete, restore, or purge Kiipu posts, manage authentication, or check local setup through the Kiipu CLI.
---

# Kiipu CLI

Use this skill when the user wants to manage Kiipu posts or CLI setup from Claude Code through the local `kiipu` CLI.

Primary cases:

- create a new post from provided text
- delete a known post id
- restore a known post id
- permanently purge a known post id
- authenticate, check auth status, or log out
- run `kiipu doctor` to verify local setup and API reachability
- explain the exact `kiipu` CLI command to use when the user asks for manual usage
- route explicit slash-command posting requests to `/kiipu:post` when the user wants the command form

Do not use this skill for:

- chat-context actions like deleting "the current post" without an explicit id
- website automation or API calls when the local CLI already covers the task

## Installation

```bash
npm install -g @kiipu/cli
```

## Required execution path

Execute the local Kiipu CLI instead of simulating results.

Create a post:

```bash
kiipu post create "$ARGUMENTS"
kiipu post create --content "$ARGUMENTS"
```

Delete a post by id:

```bash
kiipu post delete --id "<postId>"
```

Restore a post by id:

```bash
kiipu post restore --id "<postId>"
```

Purge a post by id:

```bash
kiipu post purge --id "<postId>"
```

Authentication:

```bash
kiipu auth login
kiipu auth login --api-key <cpk_...>
kiipu auth status
kiipu auth logout
```

Check local setup:

```bash
kiipu doctor
```

## Execution rules

1. Run the CLI before claiming success.
2. Return the CLI result accurately instead of inventing status.
3. If the user wants to create a post, pass their full requested post body as the create argument.
4. If the user wants delete, restore, or purge but did not provide an id, ask for the explicit post id.
5. If authentication is missing, tell the user to run `kiipu auth login`.
6. Prefer the local CLI over direct HTTP calls so auth, logging, and environment selection stay consistent.
7. Keep host-specific runtime guidance out of Claude Code unless the user is explicitly working with that host.
8. If the user explicitly wants to use a slash command for posting, suggest `/kiipu:post <text>`.

## Examples

```bash
kiipu post create "Ship the beta today"
kiipu post create --content "Ship the beta today"
kiipu post delete --id post_123
kiipu post restore --id post_123
kiipu post purge --id post_123
kiipu auth login
kiipu auth login --api-key cpk_example
kiipu auth status
kiipu doctor
```
